"""Tests for transform_shamela (temp data only, never data/raw/)."""
import csv

import pytest
from catalog.models import Author, Category, Edition, RawShamelaBook, Work
from django.core.management import call_command


def _raw(book_id, title="Title", author_id=1, slug="test-a", blob=None, author_name="Short Author"):
    return RawShamelaBook.objects.create(
        source_book_id=str(book_id),
        book_url=f"https://shamela.ws/book/{book_id}",
        title=title,
        author_name=author_name,
        author_url=f"https://shamela.ws/author/{author_id}",
        details_text=blob or "الكتاب: MyTitleالمؤلف: Full Author (ت ١٠٠هـ)المحقق: Ed",
        category_slug=slug,
        source_file=f"shamela__{slug}.csv",
    )


@pytest.mark.django_db
def test_transform_idempotent(tmp_path):
    Category.objects.create(slug="test-a", name_ar="A", name_fr="A")
    _raw(1)
    call_command("transform_shamela", "--review-dir", str(tmp_path))
    assert Author.objects.count() == 1
    assert Work.objects.count() == 1
    assert Edition.objects.count() == 1
    ed = Edition.objects.get(work__shamela_book_id="1")
    assert ed.publisher is None and ed.isbn is None and ed.price_dzd is None
    assert ed.is_published is False and ed.stock == 0
    # Set privileged fields, then re-run must not touch them.
    ed.price_dzd = 500
    ed.isbn = "9780000000000"
    ed.stock = 3
    ed.is_published = True
    ed.save(update_fields=["price_dzd", "isbn", "stock", "is_published"])
    call_command("transform_shamela", "--review-dir", str(tmp_path))
    assert Author.objects.count() == 1
    assert Work.objects.count() == 1
    assert Edition.objects.count() == 1
    ed.refresh_from_db()
    assert ed.price_dzd == 500 and ed.isbn == "9780000000000"
    assert ed.stock == 3 and ed.is_published is True


@pytest.mark.django_db
def test_book_in_two_categories_one_work(tmp_path):
    Category.objects.create(slug="test-a", name_ar="A", name_fr="A")
    Category.objects.create(slug="test-b", name_ar="B", name_fr="B")
    _raw(7, slug="test-a")
    _raw(7, slug="test-b")
    call_command("transform_shamela", "--review-dir", str(tmp_path))
    assert Work.objects.count() == 1
    assert Edition.objects.count() == 1
    w = Work.objects.get(shamela_book_id="7")
    assert set(w.categories.values_list("slug", flat=True)) == {"test-a", "test-b"}


@pytest.mark.django_db
def test_review_file_only_needs_review(tmp_path):
    Category.objects.create(slug="test-a", name_ar="A", name_fr="A")
    _raw(1)
    # Row with no labels -> needs_review
    RawShamelaBook.objects.create(
        source_book_id="2",
        book_url="https://shamela.ws/book/2",
        title="T2",
        author_name="A",
        author_url="https://shamela.ws/author/2",
        details_text="plain text no labels",
        category_slug="test-a",
        source_file="shamela__test-a.csv",
    )
    call_command("transform_shamela", "--review-dir", str(tmp_path))
    out = tmp_path / "test-a_to_check.csv"
    assert out.exists()
    with out.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["row"] == "2"


@pytest.mark.django_db
def test_author_death_year_not_erased_both_orders(tmp_path):
    Category.objects.create(slug="test-a", name_ar="A", name_fr="A")
    with_death = "الكتاب: Aالمؤلف: Full (ت ١٠٠هـ)"
    without_death = "الكتاب: Bالمؤلف: Full"
    # Order 1: with year first, then without -> death year stays (never erased).
    _raw(10, blob=with_death, author_id=9)
    _raw(11, blob=without_death, author_id=9)
    call_command("transform_shamela", "--review-dir", str(tmp_path))
    a = Author.objects.get(shamela_author_id="9")
    assert a.death_year_hijri == 100
    assert a.full_name_text  # stays non-empty
    # Order 2 (fresh DB simulation via new author): without first, then with.
    RawShamelaBook.objects.all().delete()
    Edition.objects.all().delete()
    Work.objects.all().delete()
    Author.objects.all().delete()
    _raw(12, blob=without_death, author_id=8)
    _raw(13, blob=with_death, author_id=8)
    call_command("transform_shamela", "--review-dir", str(tmp_path))
    a2 = Author.objects.get(shamela_author_id="8")
    assert a2.death_year_hijri == 100
    assert a2.full_name_text == "Full (ت ١٠٠هـ)"


@pytest.mark.django_db
def test_locked_edition_keeps_edited_publisher(tmp_path):
    Category.objects.create(slug="test-a", name_ar="A", name_fr="A")
    _raw(1)
    call_command("transform_shamela", "--review-dir", str(tmp_path))
    ed = Edition.objects.get(work__shamela_book_id="1")
    ed.publisher = "My Edited Publisher"
    ed.locked = True
    ed.save(update_fields=["publisher", "locked"])
    call_command("transform_shamela", "--review-dir", str(tmp_path))
    ed.refresh_from_db()
    assert ed.publisher == "My Edited Publisher"
    assert ed.locked is True

"""Tests for transform_shamela (temp data only, never data/raw/)."""
import csv

import pytest
from catalog.models import Author, Category, Edition, RawShamelaBook, Work
from django.core.management import call_command


def _raw(book_id, title="Title", author_id=1, slug="test-a"):
    return RawShamelaBook.objects.create(
        source_book_id=str(book_id),
        book_url=f"https://shamela.ws/book/{book_id}",
        title=title,
        author_name="Short Author",
        author_url=f"https://shamela.ws/author/{author_id}",
        details_text="الكتاب: MyTitleالمؤلف: Full Author (ت ١٠٠هـ)المحقق: Ed",
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

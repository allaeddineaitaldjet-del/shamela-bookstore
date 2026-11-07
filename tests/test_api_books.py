"""Tests for /api books (published only)."""
import pytest
from catalog.models import Author, Category, Edition, Work
from django.test import Client


def _make_book(db, title_ar="تفسيرُ مجاهد", author_name="مجاهد", slug="tafsir"):
    a, _ = Author.objects.get_or_create(
        shamela_author_id="124", defaults={"name": author_name, "full_name_text": "x"}
    )
    a.name = author_name
    a.save(update_fields=["name"])
    c, _ = Category.objects.get_or_create(slug=slug, defaults={"name_ar": "Tafsir"})
    w, _ = Work.objects.get_or_create(
        shamela_book_id="12810",
        defaults={"title_ar": title_ar, "title_from_blob": "تفسير مجاهد", "author": a},
    )
    w.title_ar = title_ar
    w.author = a
    w.save()
    from catalog.search import normalize_arabic

    w.categories.add(c)
    w.search_text = normalize_arabic(f"{w.title_ar} {w.title_from_blob} {a.name}")
    w.save(update_fields=["search_text"])
    e = Edition.objects.create(
        work=w, publisher="Dar", pages=100, price_dzd=1000, stock=5, is_published=True
    )
    return w, e


@pytest.mark.django_db
def test_unpublished_invisible(client: Client):
    a = Author.objects.create(shamela_author_id="1", name="A")
    w = Work.objects.create(shamela_book_id="999", title_ar="Hidden", author=a)
    Edition.objects.create(work=w, price_dzd=500, is_published=False)
    r = client.get("/api/books")
    assert r.status_code == 200
    data = r.json()
    items = data.get("items", data) if isinstance(data, dict) else data
    assert all(x.get("title_ar") != "Hidden" for x in items)
    r2 = client.get("/api/books/999")
    assert r2.status_code == 404


@pytest.mark.django_db
def test_search_without_diacritics_finds_diacritics(client: Client):
    _make_book(db=None)
    r = client.get("/api/books", {"q": "تفسير مجاهد"})
    assert r.status_code == 200
    data = r.json()
    items = data.get("items", data) if isinstance(data, dict) else data
    assert len(items) == 1
    assert isinstance(items[0]["price_dzd"], int)


@pytest.mark.django_db
def test_pagination_and_category(client: Client):
    _make_book(db=None, slug="tafsir")
    r = client.get("/api/books", {"category": "tafsir", "page": "1"})
    assert r.status_code == 200
    r2 = client.get("/api/books", {"category": "nope"})
    assert r2.status_code == 200
    data = r2.json()
    items = data.get("items", data) if isinstance(data, dict) else data
    assert len(items) == 0

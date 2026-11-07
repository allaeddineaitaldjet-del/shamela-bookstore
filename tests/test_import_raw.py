"""Tests for import_raw command (never reads data/raw/)."""
import csv

import pytest
from catalog.models import Category, RawShamelaBook
from django.core.management import CommandError, call_command

HEADER = ["book_title", "book_title href", "text-gray", "text-gray href", "margin-top-3"]


def _write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        for r in rows:
            w.writerow(r)


def _categories(tmp_path):
    p = tmp_path / "categories.csv"
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["slug", "name_ar", "name_fr"])
        w.writerow(["test-a", "فقه", "Fiqh"])
        w.writerow(["test-b", "أصول", "Usul"])
    return p


def _row(book_id, title="Title"):
    return [
        title,
        f"https://shamela.ws/book/{book_id}",
        "Author",
        "https://shamela.ws/author/1",
        "الكتاب: t",
    ]


@pytest.mark.django_db
def test_run_twice_same_counts(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    _write_csv(raw / "shamela__test-a.csv", [_row(1), _row(2, "T2")])
    cats = _categories(tmp_path)
    call_command("import_raw", "--raw-dir", str(raw), "--categories", str(cats))
    assert RawShamelaBook.objects.count() == 2
    call_command("import_raw", "--raw-dir", str(raw), "--categories", str(cats))
    assert RawShamelaBook.objects.count() == 2
    # Second run must not duplicate; update_or_create by natural key.
    assert RawShamelaBook.objects.filter(category_slug="test-a").count() == 2
    assert Category.objects.filter(slug="test-a").exists()


@pytest.mark.django_db
def test_unknown_slug_errors_and_imports_nothing(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    _write_csv(raw / "shamela__nope.csv", [_row(99)])
    cats = _categories(tmp_path)
    with pytest.raises(CommandError, match="Unknown slug"):
        call_command("import_raw", "--raw-dir", str(raw), "--categories", str(cats))
    assert RawShamelaBook.objects.count() == 0


@pytest.mark.django_db
def test_same_book_in_two_categories_two_rows(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    _write_csv(raw / "shamela__test-a.csv", [_row(7)])
    _write_csv(raw / "shamela__test-b.csv", [_row(7)])
    cats = _categories(tmp_path)
    call_command("import_raw", "--raw-dir", str(raw), "--categories", str(cats))
    assert RawShamelaBook.objects.filter(source_book_id="7").count() == 2
    q = RawShamelaBook.objects.filter(source_book_id="7")
    slugs = set(q.values_list("category_slug", flat=True))
    assert slugs == {"test-a", "test-b"}


@pytest.mark.django_db
def test_row_without_book_id_skipped(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    _write_csv(raw / "shamela__test-a.csv", [["No ID", "", "A", "", "x"]])
    cats = _categories(tmp_path)
    call_command("import_raw", "--raw-dir", str(raw), "--categories", str(cats))
    assert RawShamelaBook.objects.count() == 0

"""Tests for backend/catalog/shamela_parser.py.

Uses tests/fixtures/shamela_sample.csv (first 20 raw rows). Never reads data/raw/.
Expected values were checked by hand against the raw text, not copied from the
old cleaned prototype (which had mistakes in rows 6, 7, 17).
"""
import csv
from pathlib import Path

import pytest
from catalog.shamela_parser import parse_details, to_ascii_digits

FIXTURE = Path(__file__).parent / "fixtures" / "shamela_sample.csv"


def _blob(row_number: int) -> str:
    """row_number is 1-based, not counting the header."""
    with FIXTURE.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return rows[row_number - 1]["margin-top-3"]


def test_fixture_has_20_rows():
    with FIXTURE.open(encoding="utf-8", newline="") as f:
        assert len(list(csv.DictReader(f))) == 20


def test_row_6_glued_publisher_and_edition_are_separated():
    r = parse_details(_blob(6))
    assert r.publisher == "دار التدمرية - المملكة العربية السعودية"
    assert r.edition_text == "الأولى ١٤٢٧ - ٢٠٠٦ م"
    assert r.year_hijri == 1427
    assert r.year_gregorian == 2006
    # Compare around the name: the shadda/fatha order inside "الفرّان" differs
    # between sources (a classic Arabic Unicode trap), so we do not hard-code it.
    assert r.editor.startswith("د. أحمد بن مصطفى")
    assert r.editor.endswith("(رسالة دكتوراه)")
    assert r.death_year_hijri == 204
    assert r.volumes == 3
    assert r.pages is None
    assert not r.needs_review


def test_row_7_label_variants_editor_and_publication_year():
    r = parse_details(_blob(7))
    assert r.editor == "جابر بن عبد الله السريع"  # label "ضبطه وصححه"
    assert r.publisher is None  # the source has no publisher: do not invent one
    assert r.edition_text == "١٤٣٥هـ"  # label "عام النشر"
    assert r.year_hijri == 1435
    assert r.pages == 163
    assert r.death_year_hijri == 207
    assert not r.needs_review


def test_row_13_thesis_credits_go_to_review_not_to_editor_guess():
    r = parse_details(_blob(13))
    assert r.death_year_hijri == 307
    assert r.publisher is None
    assert r.needs_review
    assert "editor_too_long" in r.review_reasons


def test_row_17_publisher_label_variant_and_credits_after_author():
    r = parse_details(_blob(17))
    assert r.publisher == "دار المآثر - المدينة النبوية"  # label "دار النشر"
    assert r.year_hijri == 1423
    assert r.year_gregorian == 2002
    assert r.volumes == 2
    assert r.death_year_hijri == 319
    # editor text is glued after the author: kept in notes, flagged, never guessed
    assert r.editor is None
    assert any(n.startswith("after author:") for n in r.notes)
    assert "editor_may_be_in_author_text" in r.review_reasons


def test_row_20_missing_fields_stay_empty():
    r = parse_details(_blob(20))
    assert r.title == "بحر العلوم"
    assert r.death_year_hijri == 373
    assert r.editor is None
    assert r.publisher is None
    assert r.edition_text is None
    assert r.pages is None and r.volumes is None
    assert not r.needs_review


def test_numbers_are_integers_not_floats():
    r = parse_details(_blob(1))
    assert r.pages == 762 and isinstance(r.pages, int)


def test_parser_is_deterministic():
    assert parse_details(_blob(6)) == parse_details(_blob(6))


def test_every_sample_row_parses_without_error():
    for i in range(1, 21):
        r = parse_details(_blob(i))
        assert r.title


def test_digits_conversion():
    assert to_ascii_digits("١٤١٠ هـ - ١٩٨٩ م") == "1410 هـ - 1989 م"


@pytest.mark.parametrize("text", ["", None, "   "])
def test_empty_input_gives_empty_result(text):
    r = parse_details(text)
    assert r.title is None and r.publisher is None and not r.needs_review


def test_text_without_labels_is_flagged():
    r = parse_details("نص بلا أي وسوم")
    assert r.needs_review
    assert "no_labels_found" in r.review_reasons

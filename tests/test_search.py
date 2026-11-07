"""Tests for normalize_arabic."""
from catalog.search import normalize_arabic


def test_without_diacritics_matches_with():
    assert normalize_arabic("تفسيرُ مجاهد") == normalize_arabic("تفسير مجاهد")


def test_ta_marbuta_and_ha():
    assert normalize_arabic("مدرسة") == normalize_arabic("مدرسه")


def test_alef_variants():
    assert normalize_arabic("أحمد") == normalize_arabic("احمد")
    assert normalize_arabic("إسلام") == normalize_arabic("اسلام")


def test_alef_maqsura_and_digits():
    assert normalize_arabic("مستشفى ٢") == normalize_arabic("مستشفي 2")


def test_tatweel_and_spaces():
    assert normalize_arabic("تــفسير   مجاهد") == normalize_arabic("تفسير مجاهد")

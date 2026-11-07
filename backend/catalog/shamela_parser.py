"""Parse the Shamela "details" blob into clean fields.

Pure Python: no Django, no database, no internet. Easy to test.

The blob (column "margin-top-3" of the scraped CSV) is ONE string where labelled
fields are glued together without separators, for example:

    الكتاب: تفسير مجاهدالمؤلف: أبو الحجاج ... (ت ١٠٤هـ)المحقق: ...الناشر: ...الطبعة: ...

Strategy: find every KNOWN label followed by ":" and cut the text there.
Unknown text stays inside the previous value and raises a review flag, so we
never guess silently.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")

# field -> labels. Longest labels are matched first (see _LABEL_RE).
LABELS: dict[str, list[str]] = {
    "title": ["الكتاب"],
    "author": ["المؤلف"],
    "editor": [
        "جمع وتحقيق ودراسة", "دراسة وتحقيق", "تقديم وتحقيق", "تحقيق وتعليق",
        "ضبطه وصححه", "المحقق", "التحقيق", "تحقيق", "حققه", "راجعه", "إعداد",
    ],
    "publisher": ["دار النشر", "الناشر", "توزيع"],
    "edition": [
        "الطبعة", "عام النشر", "تاريخ النشر", "سنة النشر",
        "الطبعة الأولى", "الطبعة الثانية", "الطبعة الثالثة", "الطبعة الرابعة",
        "الطبعة الخامسة", "الطبعة السادسة", "الطبعة السابعة", "الطبعة الثامنة",
        "الطبعة التاسعة", "الطبعة العاشرة",
    ],
    "pages": ["عدد الصفحات"],
    "volumes": ["عدد الأجزاء"],
    # known but not stored as columns: kept in notes
    "note": [
        "أعده للشاملة", "أهداه للشاملة", "مصدر الكتاب", "تنبيه", "أصل التحقيق",
        "تقديم", "مراجعة", "إشراف", "بحث منشور في",
    ],
}

_LABEL_TO_FIELD = {lab: f for f, labs in LABELS.items() for lab in labs}
_ALL = sorted(_LABEL_TO_FIELD, key=len, reverse=True)
_LABEL_RE = re.compile("(" + "|".join(map(re.escape, _ALL)) + r")\s*:")

_NOISE_RE = re.compile(r"\[\s*ترقيم الكتاب[^\]]*\]")
_DEATH_RE = re.compile(
    r"[\(\[]\s*(?:ت|المتوفى)\s*:?\s*(\d{1,4})\s*ه?ـ?\s*[\)\]]"
)
_DEATH_RANGE_RE = re.compile(r"\(\s*\d{1,4}\s*-\s*(\d{1,4})\s*ه?ـ?\s*\)")
_HIJRI_RE = re.compile(r"(\d{3,4})\s*ه")
_GREG_RE = re.compile(r"(\d{4})\s*م(?![\u0600-\u06FF])")


def to_ascii_digits(text: str) -> str:
    return text.translate(_DIGITS)


@dataclass
class ParsedDetails:
    title: str | None = None
    author_full_text: str | None = None
    death_year_hijri: int | None = None
    editor: str | None = None
    publisher: str | None = None
    edition_text: str | None = None
    year_hijri: int | None = None
    year_gregorian: int | None = None
    pages: int | None = None
    volumes: int | None = None
    numbering_matches_print: bool = False
    notes: list[str] = field(default_factory=list)
    review_reasons: list[str] = field(default_factory=list)

    @property
    def needs_review(self) -> bool:
        return bool(self.review_reasons)


def _clean(value: str) -> str | None:
    value = re.sub(r"\s+", " ", value).strip(" \t\r\n.،,؛;-–—")
    return value or None


def _first_int(value: str) -> tuple[int | None, str]:
    """First number in value, and the text left over after it."""
    value = to_ascii_digits(value)
    m = re.search(r"\d+", value)
    if not m:
        return None, value.strip()
    rest = (value[: m.start()] + " " + value[m.end():]).strip(" .،-:")
    return int(m.group()), rest


def parse_details(blob: str | None) -> ParsedDetails:
    out = ParsedDetails()
    text = blob or ""
    if "ترقيم الكتاب موافق للمطبوع" in text:
        out.numbering_matches_print = True
    text = _NOISE_RE.sub(" ", text)

    matches = list(_LABEL_RE.finditer(text))
    if not matches:
        if text.strip():
            out.notes.append(text.strip())
            out.review_reasons.append("no_labels_found")
        return out

    lead = _clean(text[: matches[0].start()])
    if lead:
        out.notes.append(f"before first label: {lead}")
        out.review_reasons.append("text_before_first_label")

    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        label = m.group(1)
        value = _clean(text[m.end():end])
        fld = _LABEL_TO_FIELD[label]
        if value is None:
            continue
        if fld == "edition" and label.startswith("الطبعة "):
            value = label.split(None, 1)[1] + " " + value  # keep "الأولى"

        if fld == "title":
            out.title = out.title or value
        elif fld == "author":
            out.author_full_text = out.author_full_text or value
        elif fld == "editor":
            if out.editor is None:
                out.editor = value
            else:
                out.notes.append(f"{label}: {value}")
        elif fld == "publisher":
            if out.publisher is None:
                out.publisher = value
            else:
                out.notes.append(f"{label}: {value}")
        elif fld == "edition":
            if out.edition_text is None:
                out.edition_text = value
            else:
                out.notes.append(f"{label}: {value}")
        elif fld in ("pages", "volumes"):
            number, rest = _first_int(value)
            if number is None:
                out.notes.append(f"{label}: {value}")
                out.review_reasons.append(f"{fld}_not_a_number")
            else:
                if getattr(out, fld) is None:
                    setattr(out, fld, number)
                if len(rest) > 3:
                    out.notes.append(f"{label}: {value}")
                    if re.search(r"\d", rest):
                        out.review_reasons.append(f"{fld}_has_extra_numbers")
        else:  # note
            out.notes.append(f"{label}: {value}")

    _fill_death_year(out)
    _fill_edition_years(out)
    _add_review_flags(out)
    return out


def _fill_death_year(out: ParsedDetails) -> None:
    if not out.author_full_text:
        return
    text = to_ascii_digits(out.author_full_text)
    m = _DEATH_RE.search(text) or _DEATH_RANGE_RE.search(text)
    if not m:
        return
    year = int(m.group(1))
    if 1 <= year <= 1500:
        out.death_year_hijri = year
    # Text after the closing parenthesis is NOT the author: it is glued credits
    # (editor, thesis supervisor, ...). Keep it in notes, do not guess a field.
    tail = _clean(out.author_full_text[m.end():])
    out.author_full_text = out.author_full_text[: m.end()].strip()
    if tail:
        out.notes.append(f"after author: {tail}")
        if out.editor is None and re.search(r"تحقيق|حقق|ضبط|صحح", tail):
            out.review_reasons.append("editor_may_be_in_author_text")


def _fill_edition_years(out: ParsedDetails) -> None:
    if not out.edition_text:
        return
    text = to_ascii_digits(out.edition_text)
    # "١٤٢٧ - ٢٠٠٦ م": hijri/gregorian pair where the hijri year has no "هـ"
    pair = re.search(r"(\d{4})\s*-\s*(\d{4})\s*م", text)
    if pair and 1300 <= int(pair.group(1)) <= 1500:
        out.year_hijri = int(pair.group(1))
    h = _HIJRI_RE.search(text)
    if h and 100 <= int(h.group(1)) <= 1500:
        out.year_hijri = int(h.group(1))
    g = _GREG_RE.search(text)
    if g and 1800 <= int(g.group(1)) <= 2100:
        out.year_gregorian = int(g.group(1))


def _add_review_flags(out: ParsedDetails) -> None:
    for name in ("editor", "publisher", "edition_text"):
        value = getattr(out, name)
        if value and len(value) > 120:
            out.review_reasons.append(f"{name}_too_long")
        if value and ":" in value:
            out.review_reasons.append(f"{name}_contains_colon")
    if out.author_full_text and ":" in out.author_full_text:
        out.review_reasons.append("author_contains_colon")

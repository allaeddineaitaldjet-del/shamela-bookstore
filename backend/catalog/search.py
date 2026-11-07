"""Arabic search normalization — ONE function used everywhere."""

import re
import unicodedata

_TASHKEEL_RE = re.compile(r"[\u064B-\u0652\u0670\u0654-\u065F\u0640]")
_AR_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
_ALEF_MAP = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا"})


def normalize_arabic(text: str | None) -> str:
    if not text:
        return ""
    s = unicodedata.normalize("NFKC", text)
    s = _TASHKEEL_RE.sub("", s)
    s = s.translate(_AR_DIGITS)
    s = s.translate(_ALEF_MAP)
    s = s.replace("ى", "ي").replace("ة", "ه")
    s = s.replace("ـ", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s

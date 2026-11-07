"""Scan data/raw/*.csv for rows, book-ID duplicates and label usage.

Usage (inside container, from project root):
    python scripts/scan_labels.py

Prints 3 sections:
1. rows per file and book IDs seen in >1 file
2. every "label:" token in margin-top-3 with count per file + total, sorted
3. which labels the parser (backend/catalog/shamela_parser.LABELS) does NOT know
"""
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

BACKEND = Path(__file__).resolve().parent.parent / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from catalog.shamela_parser import LABELS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"

KNOWN = {lab for labs in LABELS.values() for lab in labs}
# Known labels are matched first (longest first) so glued text like
# "مصرالطبعة:" is counted as "الطبعة", not as a new label.
_KNOWN_SORTED = sorted(KNOWN, key=len, reverse=True)
_KNOWN_RE = re.compile("(" + "|".join(map(re.escape, _KNOWN_SORTED)) + r")\s*:")
# Generic candidate for discovery: Arabic words before ":".
_GENERIC_RE = re.compile(r"([^\s:,]{1,30}(?:\s[^\s:,]{1,30}){0,4})\s*:")


def book_id_from_url(url: str) -> str | None:
    if not url:
        return None
    m = re.search(r"/book/(\d+)", url)
    return m.group(1) if m else None


def main() -> None:
    files = sorted(RAW.glob("*.csv"))
    if not files:
        print("No CSV files in data/raw/")
        return

    per_file_rows: list[tuple[str, int]] = []
    per_file_ids: list[tuple[str, set[str]]] = []
    id_to_files: dict[str, list[str]] = defaultdict(list)

    # label -> per-file counter, and total counter
    per_file_label_counts: dict[str, Counter[str]] = {}
    total_label_counts: Counter[str] = Counter()

    for f in files:
        with f.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
        per_file_rows.append((f.name, len(rows)))
        ids = set()
        lc: Counter[str] = Counter()
        for r in rows:
            bid = book_id_from_url((r.get("book_title href") or "").strip())
            if bid:
                ids.add(bid)
            blob = r.get("margin-top-3") or ""
            # First: known labels (correct even when glued to previous value).
            known_spans = []
            for m in _KNOWN_RE.finditer(blob):
                lab = m.group(1)
                lc[lab] += 1
                total_label_counts[lab] += 1
                known_spans.append((m.start(), m.end()))
            # Then: generic candidates, but skip any match that overlaps
            # a known label (that bit is already counted).
            for m in _GENERIC_RE.finditer(blob):
                start, end = m.start(), m.end()
                if any(not (end <= ks or start >= ke) for ks, ke in known_spans):
                    continue
                lab = m.group(1).strip()
                if not re.search(r"[A-Za-z\u0600-\u06FF]", lab):
                    continue
                if lab in KNOWN:
                    continue
                lc[lab] += 1
                total_label_counts[lab] += 1
        per_file_ids.append((f.name, ids))
        per_file_label_counts[f.name] = lc
        for bid in ids:
            id_to_files[bid].append(f.name)

    print("=== 1. Rows per file ===")
    for name, n in per_file_rows:
        print(f"{name}: {n}")
    print(f"Total rows: {sum(n for _, n in per_file_rows)}")
    print()
    print("=== 1b. Book IDs in more than one file ===")
    dup = {bid: fs for bid, fs in id_to_files.items() if len(fs) > 1}
    if not dup:
        print("None — every Shamela book ID is unique across files.")
    else:
        print(f"{len(dup)} IDs appear in multiple files:")
        for bid, fs in sorted(dup.items()):
            print(f"  book/{bid}: {', '.join(fs)}")
    print()

    print("=== 2. Label tokens in margin-top-3 (per file + total) ===")
    all_labels = sorted(total_label_counts, key=total_label_counts.get, reverse=True)
    header = ["label", *[name for name, _ in per_file_rows], "TOTAL"]
    print(" | ".join(header))
    for lab in all_labels:
        row = [lab]
        for name, _ in per_file_rows:
            row.append(str(per_file_label_counts[name].get(lab, 0)))
        row.append(str(total_label_counts[lab]))
        print(" | ".join(row))
    print()

    print("=== 3. Labels NOT in parser.LABELS ===")
    unknown = [lab for lab in all_labels if lab not in KNOWN]
    if not unknown:
        print("None — parser knows every label seen.")
    else:
        for lab in unknown:
            print(f"  {lab!r} (total {total_label_counts[lab]})")
    print()
    print(f"Known labels in parser: {len(KNOWN)}")


if __name__ == "__main__":
    main()

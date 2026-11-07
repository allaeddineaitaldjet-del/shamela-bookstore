"""Load Shamela CSV files into RawShamelaBook (staging only).

Usage:
    python manage.py import_raw [--raw-dir PATH] [--categories PATH]

Reads every ``shamela__<slug>.csv`` (utf-8-sig), syncs categories from
``data/categories.csv`` first, then upserts by (source_book_id, category_slug).
Prints per file: rows, new, updated, unchanged, skipped.
"""
import csv
import re
from datetime import datetime, timezone
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from catalog.models import Category, RawShamelaBook

BOOK_ID_RE = re.compile(r"/book/(\d+)")


def _slug_from_name(name: str) -> str | None:
    if not name.startswith("shamela__") or not name.endswith(".csv"):
        return None
    return name[len("shamela__") : -len(".csv")]


class Command(BaseCommand):
    help = "Load data/raw/shamela__<slug>.csv into RawShamelaBook"

    def add_arguments(self, parser):
        parser.add_argument(
            "--raw-dir",
            default=None,
            help="Directory with shamela__*.csv (default: <root>/data/raw)",
        )
        parser.add_argument(
            "--categories",
            default=None,
            help="Path to categories.csv (default: <root>/data/categories.csv)",
        )

    def handle(self, *args, **options):
        root = Path(__file__).resolve().parent.parent.parent.parent.parent
        raw_dir = Path(options["raw_dir"]) if options["raw_dir"] else root / "data" / "raw"
        categories_path = (
            Path(options["categories"])
            if options["categories"]
            else root / "data" / "categories.csv"
        )

        # 1. Sync categories first (source of truth).
        if not categories_path.exists():
            raise CommandError(f"categories file missing: {categories_path}")
        with categories_path.open(encoding="utf-8-sig", newline="") as f:
            cat_rows = list(csv.DictReader(f))
        cat_slugs = set()
        for row in cat_rows:
            slug = (row.get("slug") or "").strip()
            if not slug:
                continue
            cat_slugs.add(slug)
            Category.objects.update_or_create(
                slug=slug,
                defaults={
                    "name_ar": (row.get("name_ar") or "").strip(),
                    "name_fr": (row.get("name_fr") or "").strip(),
                },
            )

        files = sorted(raw_dir.glob("shamela__*.csv"))
        if not files:
            raise CommandError(f"No shamela__*.csv files in {raw_dir}")

        # 2. Validate every slug before importing anything.
        plans = []  # (path, slug)
        for path in files:
            slug = _slug_from_name(path.name)
            if not slug:
                raise CommandError(f"Cannot parse slug from filename: {path.name}")
            if slug not in cat_slugs:
                raise CommandError(
                    f"Unknown slug {slug!r} from {path.name} — "
                    f"not in {categories_path}. Import aborted, no books imported."
                )
            plans.append((path, slug))

        # 3. Upsert per file, atomically per file: all rows or none.
        for path, slug in plans:
            with transaction.atomic():
                fetched_at = datetime.fromtimestamp(
                    path.stat().st_mtime, tz=timezone.utc
                )
                rows = new = updated = unchanged = skipped = 0
                with path.open(encoding="utf-8-sig", newline="") as f:
                    for row in csv.DictReader(f):
                        rows += 1
                        book_url = (row.get("book_title href") or "").strip()
                        m = BOOK_ID_RE.search(book_url)
                        if not m:
                            skipped += 1
                            continue
                        source_book_id = m.group(1)
                        defaults = {
                            "book_url": book_url,
                            "title": (row.get("book_title") or "").strip(),
                            "author_name": (row.get("text-gray") or "").strip(),
                            "author_url": (row.get("text-gray href") or "").strip(),
                            "details_text": row.get("margin-top-3") or "",
                            "category_slug": slug,
                            "source_file": path.name,
                            "fetched_at": fetched_at,
                        }
                        existing = RawShamelaBook.objects.filter(
                            source_book_id=source_book_id, category_slug=slug
                        ).first()
                        if existing is None:
                            RawShamelaBook.objects.create(
                                source_book_id=source_book_id, **defaults
                            )
                            new += 1
                            continue
                        changed = any(
                            getattr(existing, k) != v for k, v in defaults.items()
                        )
                        if changed:
                            for k, v in defaults.items():
                                setattr(existing, k, v)
                            existing.save(
                                update_fields=list(defaults) + ["imported_at"]
                            )
                            updated += 1
                        else:
                            unchanged += 1
            self.stdout.write(
                f"{path.name}: rows={rows} new={new} updated={updated} "
                f"unchanged={unchanged} skipped={skipped}"
            )

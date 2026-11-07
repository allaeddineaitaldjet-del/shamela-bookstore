"""Transform RawShamelaBook staging into Author/Work/Edition (metadata only).

Usage:
    python manage.py transform_shamela [--review-dir PATH]

Idempotent inside transaction.atomic(): run twice = no new rows, no changes.
Never touches price_dzd, isbn, stock, is_published. Empty stays NULL.
Rows needing review are written to data/review/<slug>_to_check.csv.
"""
import csv
import re

from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import Author, Category, Edition, RawShamelaBook, Work
from catalog.shamela_parser import parse_details

AUTHOR_ID_RE = re.compile(r"/author/(\d+)")


class Command(BaseCommand):
    help = "Transform staged Shamela rows into Author/Work/Edition"

    def add_arguments(self, parser):
        parser.add_argument(
            "--review-dir",
            default=None,
            help="Directory for <slug>_to_check.csv (default: <root>/data/review)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        from pathlib import Path

        root = Path(__file__).resolve().parent.parent.parent.parent.parent
        review_dir = (
            Path(options["review_dir"]) if options.get("review_dir") else root / "data" / "review"
        )
        review_dir.mkdir(parents=True, exist_ok=True)

        rows = list(
            RawShamelaBook.objects.all().order_by("category_slug", "source_book_id")
        )
        # Group staged rows by book ID so ALL categories are linked to one Work.
        by_book: dict[str, list[RawShamelaBook]] = {}
        for r in rows:
            by_book.setdefault(r.source_book_id, []).append(r)

        author_ids_seen: set[str] = set()
        work_count = 0
        edition_count = 0
        needs_review_per_file: dict[str, int] = {}

        for book_id in sorted(by_book):
            staged_list = by_book[book_id]
            # For Edition fields use the first staged row by category slug.
            first = sorted(staged_list, key=lambda x: x.category_slug)[0]
            parsed = parse_details(first.details_text)

            # Author upsert — never replace non-empty with empty.
            # Only set death_year_hijri/full_name_text when parser found a value.
            author = None
            m = AUTHOR_ID_RE.search(first.author_url or "")
            if m:
                author_id = m.group(1)
                author, created_a = Author.objects.get_or_create(
                    shamela_author_id=author_id,
                    defaults={
                        "name": first.author_name,
                        "full_name_text": parsed.author_full_text or "",
                        "death_year_hijri": parsed.death_year_hijri,
                    },
                )
                if not created_a:
                    changed = False
                    if first.author_name and author.name != first.author_name:
                        author.name = first.author_name
                        changed = True
                    if parsed.author_full_text and author.full_name_text != parsed.author_full_text:
                        author.full_name_text = parsed.author_full_text
                        changed = True
                    if (
                        parsed.death_year_hijri is not None
                        and author.death_year_hijri != parsed.death_year_hijri
                    ):
                        author.death_year_hijri = parsed.death_year_hijri
                        changed = True
                    if changed:
                        author.save(update_fields=["name", "full_name_text", "death_year_hijri"])
                author_ids_seen.add(author_id)

            work, _ = Work.objects.update_or_create(
                shamela_book_id=book_id,
                defaults={
                    "title_ar": first.title,
                    "title_from_blob": parsed.title,
                    "author": author,
                },
            )
            work_count += 1

            # Link ALL categories where this book ID appears in staging.
            for staged in staged_list:
                cat, _ = Category.objects.get_or_create(
                    slug=staged.category_slug,
                    defaults={"name_ar": staged.category_slug},
                )
                work.categories.add(cat)

            existing_ed = Edition.objects.filter(work=work, source="shamela").first()
            if existing_ed is not None and existing_ed.locked:
                # Locked: do not touch any metadata field.
                pass
            else:
                edition, _ = Edition.objects.update_or_create(
                    work=work,
                    source="shamela",
                    defaults={
                        "publisher": parsed.publisher,
                        "editor": parsed.editor,
                        "edition_text": parsed.edition_text,
                        "year_hijri": parsed.year_hijri,
                        "year_gregorian": parsed.year_gregorian,
                        "pages": parsed.pages,
                        "volumes": parsed.volumes,
                        "notes": " | ".join(parsed.notes),
                        "needs_review": parsed.needs_review,
                        "review_reasons": ",".join(parsed.review_reasons),
                    },
                )
            edition_count += 1

        # Review files: only needs_review rows, per slug.
        for slug in sorted({r.category_slug for r in rows}):
            slug_rows = [r for r in rows if r.category_slug == slug]
            needs = []
            for staged in slug_rows:
                parsed = parse_details(staged.details_text)
                if parsed.needs_review:
                    needs.append(
                        {
                            "row": staged.source_book_id,
                            "book_url": staged.book_url,
                            "title": staged.title,
                            "reasons": ",".join(parsed.review_reasons),
                            "author_full_text": parsed.author_full_text or "",
                            "editor": parsed.editor or "",
                            "publisher": parsed.publisher or "",
                            "edition_text": parsed.edition_text or "",
                            "notes": " | ".join(parsed.notes),
                        }
                    )
            needs_review_per_file[slug] = len(needs)
            out_path = review_dir / f"{slug}_to_check.csv"
            if needs:
                with out_path.open("w", encoding="utf-8-sig", newline="") as f:
                    w = csv.DictWriter(
                        f,
                        fieldnames=[
                            "row",
                            "book_url",
                            "title",
                            "reasons",
                            "author_full_text",
                            "editor",
                            "publisher",
                            "edition_text",
                            "notes",
                        ],
                    )
                    w.writeheader()
                    w.writerows(needs)
            elif out_path.exists():
                # Keep file fresh: clear it when nothing needs review.
                with out_path.open("w", encoding="utf-8-sig", newline="") as f:
                    w = csv.DictWriter(
                        f,
                        fieldnames=[
                            "row",
                            "book_url",
                            "title",
                            "reasons",
                            "author_full_text",
                            "editor",
                            "publisher",
                            "edition_text",
                            "notes",
                        ],
                    )
                    w.writeheader()

        self.stdout.write(
            f"authors={len(author_ids_seen)} works={work_count} editions={edition_count}"
        )
        for slug in sorted(needs_review_per_file):
            self.stdout.write(f"{slug}: needs_review={needs_review_per_file[slug]}")

import csv
from pathlib import Path

from django.db import migrations


def seed_categories(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    csv_path = Path(__file__).resolve().parent.parent.parent.parent / "data" / "categories.csv"
    if not csv_path.exists():
        return
    with csv_path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            slug = (row.get("slug") or "").strip()
            if not slug:
                continue
            Category.objects.update_or_create(
                slug=slug,
                defaults={
                    "name_ar": (row.get("name_ar") or "").strip(),
                    "name_fr": (row.get("name_fr") or "").strip(),
                },
            )


def unseed_categories(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    Category.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_categories, unseed_categories),
    ]

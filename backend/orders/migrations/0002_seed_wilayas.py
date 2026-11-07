"""Seed wilayas from data/wilayas.csv (58 official wilayas)."""
import csv
from pathlib import Path

from django.db import migrations


def seed(apps, schema_editor):
    Wilaya = apps.get_model("orders", "Wilaya")
    p = Path(__file__).resolve().parent.parent.parent.parent / "data" / "wilayas.csv"
    if not p.exists():
        return
    with p.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            code = (row.get("code") or "").strip()
            if not code:
                continue
            Wilaya.objects.update_or_create(
                code=int(code),
                defaults={
                    "name_ar": (row.get("name_ar") or "").strip(),
                    "name_fr": (row.get("name_fr") or "").strip(),
                },
            )


def unseed(apps, schema_editor):
    Wilaya = apps.get_model("orders", "Wilaya")
    Wilaya.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]

"""DEV ONLY demo seed — refuses unless DEBUG=True. FAKE prices, delete before launch."""
import random

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from catalog.models import Edition


class Command(BaseCommand):
    help = "DEV ONLY: fake prices for first 12 editions"

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("seed_demo refuses unless DEBUG=True")
        msg = "WARNING: FAKE prices — see BACKLOG.md, delete before launch"
        self.stdout.write(self.style.WARNING(msg))
        editions = Edition.objects.filter(work__title_ar__isnull=False)
        # First 12 with clean title and author.
        qs = editions.filter(work__author__isnull=False).order_by("id")[:50]
        picked = []
        for e in qs:
            if e.work.title_ar and e.work.author and len(e.work.title_ar) >= 3:
                picked.append(e)
            if len(picked) == 12:
                break
        rng = random.Random(42)
        for e in picked:
            e.price_dzd = rng.randint(800, 4500)
            e.stock = 20
            e.is_published = True
            e.save(update_fields=["price_dzd", "stock", "is_published"])
        self.stdout.write(f"Seeded {len(picked)} editions with FAKE prices")

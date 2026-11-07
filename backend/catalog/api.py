"""Read-only API (Django Ninja). Money is integer DZD, never floats."""

from django.http import Http404
from ninja import NinjaAPI

from catalog.models import Category, Edition
from catalog.search import normalize_arabic

api = NinjaAPI(version="1.0", urls_namespace="api")


def _book_row(edition):
    w = edition.work
    return {
        "work_id": w.id,
        "title_ar": w.title_ar,
        "author": w.author.name if w.author else None,
        "category_slugs": list(w.categories.values_list("slug", flat=True)),
        "price_dzd": int(edition.price_dzd) if edition.price_dzd is not None else None,
        "in_stock": bool(edition.stock and edition.stock > 0),
        "publisher": edition.publisher,
        "pages": edition.pages,
    }


@api.get("/categories")
def list_categories(request):
    return [
        {"slug": c.slug, "name_ar": c.name_ar, "name_fr": c.name_fr}
        for c in Category.objects.all().order_by("slug")
    ]


@api.get("/books")
def list_books(request, category: str | None = None, q: str | None = None, page: int = 1):
    qs = (
        Edition.objects.filter(is_published=True)
        .select_related("work", "work__author")
        .prefetch_related("work__categories")
    )
    if category:
        qs = qs.filter(work__categories__slug=category)
    if q:
        nq = normalize_arabic(q)
        if nq:
            qs = qs.filter(work__search_text__icontains=nq)
    qs = qs.order_by("work__title_ar")
    total = qs.count()
    page_size = 20
    start = (max(page, 1) - 1) * page_size
    items = [_book_row(e) for e in qs[start : start + page_size]]
    return {"items": items, "count": total, "page": max(page, 1), "page_size": page_size}


@api.get("/books/{work_id}")
def get_book(request, work_id: int):
    try:
        edition = Edition.objects.select_related("work", "work__author").prefetch_related(
            "work__categories"
        ).get(work_id=work_id, is_published=True)
    except (Edition.DoesNotExist, ValueError):
        raise Http404("Book not found")
    row = _book_row(edition)
    row.update(
        {
            "editor": edition.editor,
            "volumes": edition.volumes,
            "year_hijri": edition.year_hijri,
            "year_gregorian": edition.year_gregorian,
        }
    )
    return row

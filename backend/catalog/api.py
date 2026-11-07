"""Read-only API (Django Ninja) + POST orders. Money is integer DZD, never floats."""

import logging
import os
import re

from django.http import Http404
from ninja import NinjaAPI
from ninja.errors import ValidationError
from orders.models import STATUS_NEW, Order, OrderItem, Wilaya
from pydantic import BaseModel

from catalog.models import Category, Edition
from catalog.search import normalize_arabic

logger = logging.getLogger(__name__)

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


PHONE_RE = re.compile(r"^(?:\+213|0)(5|6|7)\d{8}$")


def _normalize_phone(raw: str) -> str | None:
    s = re.sub(r"[\s\-()]", "", (raw or "").strip())
    if s.startswith("+213"):
        s = "0" + s[4:]
    if not re.match(r"^0(5|6|7)\d{8}$", s):
        return None
    return s


class OrderItemIn(BaseModel):
    work_id: int
    qty: int
    price_dzd: int | None = None  # ignored, server recalculates


class OrderIn(BaseModel):
    customer_name: str
    phone: str
    wilaya_code: int
    address: str
    items: list[OrderItemIn]


@api.post("/orders")
def create_order(request, payload: OrderIn):
    phone = _normalize_phone(payload.phone)
    if not phone:
        raise ValidationError("Invalid Algerian phone (05/06/07 + 8 digits)")
    try:
        wilaya = Wilaya.objects.get(code=payload.wilaya_code)
    except Wilaya.DoesNotExist:
        raise ValidationError("Unknown wilaya_code")
    if not payload.items:
        raise ValidationError("items empty")
    # Server recalculates prices — never trust client prices.
    total = 0
    resolved = []
    for it in payload.items:
        if it.qty is None or it.qty < 1 or it.qty > 10:
            raise ValidationError("qty must be 1..10")
        try:
            edition = Edition.objects.select_related("work").get(
                work_id=it.work_id, is_published=True
            )
        except (Edition.DoesNotExist, ValueError):
            raise ValidationError(f"Book {it.work_id} not published")
        if edition.price_dzd is None:
            raise ValidationError(f"Book {it.work_id} has no price")
        unit = int(edition.price_dzd)
        resolved.append((edition, int(it.qty), unit))
        total += unit * int(it.qty)
    delivery = int(os.environ.get("DEFAULT_DELIVERY_FEE_DZD", "0") or 0)
    # TODO real fees per wilaya; currently one flat env value.
    total += delivery
    order = Order.objects.create(
        status=STATUS_NEW,
        customer_name=payload.customer_name.strip(),
        phone=phone,
        wilaya=wilaya,
        address=payload.address.strip(),
        delivery_fee_dzd=delivery,
        total_dzd=total,
    )
    for edition, qty, unit in resolved:
        OrderItem.objects.create(order=order, edition=edition, qty=qty, unit_price_dzd=unit)
    # Do NOT log phone or address.
    logger.info("order created id=%s total=%s", order.id, total)
    return {"id": order.id, "total_dzd": int(total)}

"""Tests for orders: prices, transitions, stock, phone."""
import json

import pytest
from catalog.models import Author, Category, Edition, Work
from django.test import Client
from orders.models import Order, OrderItem, Wilaya
from orders.state import InvalidTransition, change_status


def _setup(db):
    a = Author.objects.create(shamela_author_id="124", name="A")
    c, _ = Category.objects.get_or_create(slug="cat", defaults={"name_ar": "C", "name_fr": "C"})
    w = Work.objects.create(shamela_book_id="12810", title_ar="T", author=a)
    w.categories.add(c)
    e = Edition.objects.create(
        work=w, publisher="P", price_dzd=1200, stock=10, is_published=True
    )
    wilaya, _ = Wilaya.objects.get_or_create(
        code=16, defaults={"name_ar": "الجزائر", "name_fr": "Alger"}
    )
    return w, e, wilaya


@pytest.mark.django_db
def test_price_recalculated_ignores_client(client: Client):
    w, e, wilaya = _setup(db=None)
    body = {
        "customer_name": "N",
        "phone": "0550123456",
        "wilaya_code": 16,
        "address": "Addr",
        "items": [{"work_id": w.id, "qty": 2, "price_dzd": 1}],
    }
    r = client.post("/api/orders", data=json.dumps(body), content_type="application/json")
    assert r.status_code == 200, r.content
    data = r.json()
    assert data["total_dzd"] == 2400
    o = Order.objects.get(id=data["id"])
    assert o.total_dzd == 2400
    assert o.items.first().unit_price_dzd == 1200


@pytest.mark.django_db
def test_unpublished_rejected(client: Client):
    w, e, wilaya = _setup(db=None)
    e.is_published = False
    e.save(update_fields=["is_published"])
    body = {
        "customer_name": "N",
        "phone": "0661123456",
        "wilaya_code": 16,
        "address": "A",
        "items": [{"work_id": w.id, "qty": 1}],
    }
    r = client.post("/api/orders", data=json.dumps(body), content_type="application/json")
    assert r.status_code in (400, 422)
    assert Order.objects.count() == 0


@pytest.mark.django_db
def test_valid_and_invalid_transitions():
    w, e, wilaya = _setup(db=None)
    o = Order.objects.create(customer_name="N", phone="0550123456", wilaya=wilaya, total_dzd=1200)
    OrderItem.objects.create(order=o, edition=e, qty=1, unit_price_dzd=1200)
    change_status(o, "TO_CALL")
    assert o.status == "TO_CALL"
    change_status(o, "CONFIRMED")
    assert o.status == "CONFIRMED"
    with pytest.raises(InvalidTransition):
        change_status(o, "NEW")


@pytest.mark.django_db
def test_stock_reserved_only_at_confirmed():
    w, e, wilaya = _setup(db=None)
    e.stock = 5
    e.save(update_fields=["stock"])
    o = Order.objects.create(customer_name="N", wilaya=wilaya, total_dzd=1200)
    OrderItem.objects.create(order=o, edition=e, qty=2, unit_price_dzd=1200)
    change_status(o, "TO_CALL")
    e.refresh_from_db()
    assert e.stock == 5
    change_status(o, "CONFIRMED")
    e.refresh_from_db()
    assert e.stock == 3
    change_status(o, "CANCELLED")
    e.refresh_from_db()
    assert e.stock == 5


@pytest.mark.django_db
def test_no_answer_increments():
    w, e, wilaya = _setup(db=None)
    o = Order.objects.create(customer_name="N", wilaya=wilaya)
    change_status(o, "TO_CALL")
    change_status(o, "NO_ANSWER")
    o.refresh_from_db()
    assert o.call_attempts == 1


@pytest.mark.django_db
def test_phone_validation(client: Client):
    w, e, wilaya = _setup(db=None)
    for bad in ["041...", "081...", "123"]:
        body = {
            "customer_name": "N",
            "phone": bad,
            "wilaya_code": 16,
            "address": "A",
            "items": [{"work_id": w.id, "qty": 1}],
        }
        r = client.post("/api/orders", data=json.dumps(body), content_type="application/json")
        assert r.status_code in (400, 422), (bad, r.content)
    for good, expected in [("0550123456", "0550123456"), ("+213550123456", "0550123456")]:
        body = {
            "customer_name": "N",
            "phone": good,
            "wilaya_code": 16,
            "address": "A",
            "items": [{"work_id": w.id, "qty": 1}],
        }
        r = client.post("/api/orders", data=json.dumps(body), content_type="application/json")
        assert r.status_code == 200, r.content
        o = Order.objects.get(id=r.json()["id"])
        assert o.phone == expected

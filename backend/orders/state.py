"""ONE state-machine function — all status changes go through here."""

from django.db import transaction

from orders.models import (
    STATUS_CANCELLED,
    STATUS_CONFIRMED,
    STATUS_DELIVERED,
    STATUS_NEW,
    STATUS_NO_ANSWER,
    STATUS_REFUSED,
    STATUS_RETURNED,
    STATUS_SHIPPED,
    STATUS_TO_CALL,
)

ALLOWED: dict[str, set[str]] = {
    STATUS_NEW: {STATUS_TO_CALL, STATUS_CANCELLED, STATUS_REFUSED},
    STATUS_TO_CALL: {
        STATUS_CONFIRMED,
        STATUS_NO_ANSWER,
        STATUS_CANCELLED,
        STATUS_REFUSED,
    },
    STATUS_CONFIRMED: {STATUS_SHIPPED, STATUS_CANCELLED, STATUS_RETURNED, STATUS_NO_ANSWER},
    STATUS_SHIPPED: {STATUS_DELIVERED, STATUS_RETURNED, STATUS_REFUSED},
    STATUS_NO_ANSWER: {STATUS_TO_CALL, STATUS_CANCELLED, STATUS_REFUSED},
    STATUS_DELIVERED: set(),
    STATUS_CANCELLED: set(),
    STATUS_REFUSED: set(),
    STATUS_RETURNED: set(),
}


class InvalidTransition(ValueError):
    pass


@transaction.atomic
def change_status(order, new_status: str):
    allowed = ALLOWED.get(order.status, set())
    if new_status not in allowed:
        raise InvalidTransition(f"Cannot go from {order.status} to {new_status}")
    old = order.status
    if new_status == STATUS_NO_ANSWER:
        order.call_attempts = (order.call_attempts or 0) + 1
    if new_status == STATUS_CONFIRMED:
        for item in order.items.all():
            item.edition.refresh_from_db()
            if item.edition.stock < item.qty:
                raise InvalidTransition("Not enough stock")
            item.edition.stock -= item.qty
            item.edition.save(update_fields=["stock"])
    if old == STATUS_CONFIRMED and new_status in (STATUS_CANCELLED, STATUS_RETURNED):
        for item in order.items.all():
            item.edition.refresh_from_db()
            item.edition.stock += item.qty
            item.edition.save(update_fields=["stock"])
    order.status = new_status
    order.save(update_fields=["status", "call_attempts"])
    return order

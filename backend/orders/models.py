from catalog.models import Edition
from django.db import models

STATUS_NEW = "NEW"
STATUS_TO_CALL = "TO_CALL"
STATUS_CONFIRMED = "CONFIRMED"
STATUS_SHIPPED = "SHIPPED"
STATUS_DELIVERED = "DELIVERED"
STATUS_NO_ANSWER = "NO_ANSWER"
STATUS_CANCELLED = "CANCELLED"
STATUS_REFUSED = "REFUSED"
STATUS_RETURNED = "RETURNED"

STATUS_CHOICES = [
    (STATUS_NEW, "NEW"),
    (STATUS_TO_CALL, "TO_CALL"),
    (STATUS_CONFIRMED, "CONFIRMED"),
    (STATUS_SHIPPED, "SHIPPED"),
    (STATUS_DELIVERED, "DELIVERED"),
    (STATUS_NO_ANSWER, "NO_ANSWER"),
    (STATUS_CANCELLED, "CANCELLED"),
    (STATUS_REFUSED, "REFUSED"),
    (STATUS_RETURNED, "RETURNED"),
]


class Wilaya(models.Model):
    code = models.PositiveSmallIntegerField(unique=True)
    name_ar = models.CharField(max_length=200, blank=True)
    name_fr = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.code} {self.name_ar}"


class Order(models.Model):
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    customer_name = models.CharField(max_length=500, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.PROTECT, null=True, blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    delivery_fee_dzd = models.PositiveIntegerField(default=0)
    total_dzd = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    call_attempts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Order {self.pk} {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    edition = models.ForeignKey(Edition, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField()
    unit_price_dzd = models.PositiveIntegerField()

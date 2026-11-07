from django.contrib import admin

from .models import Order, OrderItem, Wilaya
from .state import InvalidTransition, change_status


@admin.register(Wilaya)
class WilayaAdmin(admin.ModelAdmin):
    list_display = ("code", "name_ar", "name_fr")
    search_fields = ("name_ar", "name_fr")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("qty", "unit_price_dzd", "edition")


ACTIONS = {
    "to_call": "TO_CALL",
    "confirmed": "CONFIRMED",
    "shipped": "SHIPPED",
    "delivered": "DELIVERED",
    "no_answer": "NO_ANSWER",
    "cancelled": "CANCELLED",
}
# Include refused/returned too for completeness.
ACTIONS.update({"refused": "REFUSED", "returned": "RETURNED"})


def _make_action(key, new_status):
    @admin.action(description=f"Mark {key}")
    def func(model_admin, request, queryset):
        ok = 0
        failed = 0
        for order in queryset:
            try:
                change_status(order, new_status)
                ok += 1
            except InvalidTransition:
                failed += 1
        model_admin.message_user(request, f"OK {ok} / failed {failed} -> {new_status}")

    func.__name__ = f"mark_{key}"
    return func


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "customer_name", "wilaya", "status", "total_dzd")
    list_filter = ("status", "wilaya", "created_at")
    search_fields = ("customer_name", "phone")
    inlines = [OrderItemInline]
    readonly_fields = ("status", "delivery_fee_dzd", "total_dzd", "created_at", "call_attempts")
    actions = [_make_action(k, v) for k, v in ACTIONS.items()]

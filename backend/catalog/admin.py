from django.contrib import admin

from .models import Author, Category, Edition, RawShamelaBook, Work


class HasPriceFilter(admin.SimpleListFilter):
    title = "has price"
    parameter_name = "has_price"

    def lookups(self, request, model_admin):
        return [("yes", "Has price"), ("no", "No price")]

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(price_dzd__isnull=False)
        if self.value() == "no":
            return queryset.filter(price_dzd__isnull=True)
        return queryset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("slug", "name_ar", "name_fr")
    search_fields = ("slug", "name_ar", "name_fr")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("shamela_author_id", "name", "death_year_hijri")
    search_fields = ("name", "full_name_text", "shamela_author_id")


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ("shamela_book_id", "title_ar", "title_from_blob", "author")
    search_fields = ("title_ar", "title_from_blob", "author__name")
    autocomplete_fields = ("author",)
    filter_horizontal = ("categories",)


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = (
        "work",
        "publisher",
        "editor",
        "year_hijri",
        "is_published",
        "needs_review",
        "locked",
        "price_dzd",
        "stock",
    )
    list_editable = ("price_dzd", "stock", "is_published")
    search_fields = ("publisher", "editor", "work__title_ar")
    list_filter = ("is_published", "needs_review", "locked", HasPriceFilter, "work__categories")
    autocomplete_fields = ("work",)
    actions = ["lock_selected", "unlock_selected", "publish_selected"]

    def save_model(self, request, obj, form, change):
        obj.locked = True
        super().save_model(request, obj, form, change)

    @admin.action(description="Lock selected")
    def lock_selected(self, request, queryset):
        queryset.update(locked=True)

    @admin.action(description="Unlock selected")
    def unlock_selected(self, request, queryset):
        queryset.update(locked=False)

    @admin.action(description="Publish selected")
    def publish_selected(self, request, queryset):
        published = 0
        skipped = 0
        for ed in queryset:
            if ed.price_dzd is not None:
                if not ed.is_published:
                    ed.is_published = True
                    ed.save(update_fields=["is_published"])
                published += 1
            else:
                skipped += 1
        self.message_user(request, f"Published {published} edition(s). Skipped {skipped} (no price).")


@admin.register(RawShamelaBook)
class RawShamelaBookAdmin(admin.ModelAdmin):
    list_display = (
        "source_book_id",
        "category_slug",
        "title",
        "source_file",
        "imported_at",
        "fetched_at",
    )
    search_fields = ("title", "author_name", "source_book_id", "details_text")
    list_filter = ("category_slug", "source_file")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

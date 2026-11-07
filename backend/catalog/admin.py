from django.contrib import admin

from .models import Author, Category, Edition, RawShamelaBook, Work


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
    )
    search_fields = ("publisher", "editor", "work__title_ar")
    list_filter = ("is_published", "needs_review", "locked")
    autocomplete_fields = ("work",)
    actions = ["lock_selected", "unlock_selected"]

    def save_model(self, request, obj, form, change):
        obj.locked = True
        super().save_model(request, obj, form, change)

    @admin.action(description="Lock selected")
    def lock_selected(self, request, queryset):
        queryset.update(locked=True)

    @admin.action(description="Unlock selected")
    def unlock_selected(self, request, queryset):
        queryset.update(locked=False)


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

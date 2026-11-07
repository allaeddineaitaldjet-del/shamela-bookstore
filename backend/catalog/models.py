from django.db import models


class RawShamelaBook(models.Model):
    """Staging: one CSV row kept verbatim (source + URLs + date)."""

    source_book_id = models.CharField(max_length=32)
    book_url = models.URLField(max_length=500, blank=True)
    title = models.CharField(max_length=500, blank=True)
    author_name = models.CharField(max_length=500, blank=True)
    author_url = models.URLField(max_length=500, blank=True)
    details_text = models.TextField(blank=True)
    category_slug = models.SlugField(max_length=100, blank=True)
    source_file = models.CharField(max_length=200, blank=True)
    imported_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("source_book_id", "category_slug")
        verbose_name_plural = "Raw Shamela books"

    def __str__(self):
        return f"{self.source_book_id} [{self.category_slug}] {self.title}"


class Category(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    name_ar = models.CharField(max_length=200, blank=True)
    name_fr = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name_ar or self.slug


class Author(models.Model):
    shamela_author_id = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=500, blank=True)
    full_name_text = models.TextField(blank=True)
    death_year_hijri = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name or self.shamela_author_id


class Work(models.Model):
    shamela_book_id = models.CharField(max_length=32, unique=True)
    # Book title from the book_title column (storefront display title).
    title_ar = models.CharField(max_length=500, blank=True)
    # Official title from inside the blob (parser "الكتاب:" label).
    title_from_blob = models.CharField(max_length=500, null=True, blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, null=True, blank=True
    )
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.title_ar or self.shamela_book_id


class Edition(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    publisher = models.CharField(max_length=500, null=True, blank=True)
    editor = models.CharField(max_length=500, null=True, blank=True)
    edition_text = models.TextField(null=True, blank=True)
    year_hijri = models.PositiveSmallIntegerField(null=True, blank=True)
    year_gregorian = models.PositiveSmallIntegerField(null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    volumes = models.PositiveIntegerField(null=True, blank=True)
    # Never invented — left NULL until a human fills them.
    isbn = models.CharField(max_length=20, null=True, blank=True)
    price_dzd = models.PositiveIntegerField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    notes = models.TextField(blank=True, default="")
    needs_review = models.BooleanField(default=False)
    review_reasons = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.work} — {self.edition_text or 'no edition'}"

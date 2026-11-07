import { Suspense } from "react";
import { Reveal } from "@/components/motion/reveal";
import { listBooks, listCategories } from "@/lib/api";
import { BookCard } from "@/components/book-card";

export default function BooksPage(props: {
  params: Promise<{ locale: string }>;
  searchParams?: Promise<{ category?: string; q?: string; page?: string }>;
}) {
  return (
    <Suspense fallback={null}>
      <BooksContent {...props} />
    </Suspense>
  );
}

async function BooksContent({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string }>;
  searchParams?: Promise<{ category?: string; q?: string; page?: string }>;
}) {
  const { locale } = await params;
  const sp = (await searchParams?.catch(() => ({}))) as {
    category?: string;
    q?: string;
    page?: string;
  };
  const category = sp?.category || undefined;
  const q = sp?.q || undefined;
  const page = Math.max(parseInt(sp?.page || "1", 10) || 1, 1);
  const [cats, data] = await Promise.all([
    listCategories().catch(() => []),
    listBooks({ category, q, page }).catch(() => ({ items: [], count: 0, page, page_size: 20 })),
  ]);
  const { count, page_size } = data;
  const totalPages = Math.max(1, Math.ceil(count / page_size));
  const dir = locale === "ar" ? "rtl" : "ltr";
  const qs = (extra: Record<string, string>) => {
    const p = new URLSearchParams({
      ...(page ? { page: String(page) } : {}),
      ...(category ? { category } : {}),
      ...(q ? { q } : {}),
      ...extra,
    });
    return p.toString();
  };
  const t = await import("next-intl/server").then((m) => m.getTranslations("Common"));
  return (
    <main
      style={{
        maxWidth: 1100,
        marginInlineStart: "auto",
        marginInlineEnd: "auto",
        paddingInlineStart: "1rem",
        paddingInlineEnd: "1rem",
        paddingBlockStart: "2rem",
      }}
    >
      <form
        method="get"
        style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginBlockEnd: "1rem" }}
      >
        <input
          name="q"
          defaultValue={q || ""}
          placeholder={locale === "ar" ? "بحث..." : "Search..."}
          style={{
            flex: 1,
            minHeight: 44,
            paddingInlineStart: "0.75rem",
            borderRadius: 6,
            border: "1px solid var(--line)",
            background: "var(--surface)",
            color: "var(--ink)",
          }}
        />
        <button
          type="submit"
          style={{
            minHeight: 44,
            paddingInlineStart: "1rem",
            paddingInlineEnd: "1rem",
            borderRadius: 6,
            background: "var(--primary)",
            color: "#fff",
            border: "none",
          }}
        >
          {t("search")}
        </button>
      </form>
      <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginBlockEnd: "1rem" }}>
        <a
          href={`/${locale}/books?${qs({ category: "", page: "1" })}`}
          style={{
            border: "1px solid var(--line)",
            borderRadius: 999,
            paddingInlineStart: "0.75rem",
            paddingInlineEnd: "0.75rem",
            paddingBlockStart: "0.35rem",
            paddingBlockEnd: "0.35rem",
            background: !category ? "var(--primary)" : "var(--surface)",
            color: !category ? "#fff" : "var(--ink)",
            textDecoration: "none",
          }}
        >
          {locale === "ar" ? "الكل" : "All"}
        </a>
        {cats.map((cat) => (
          <a
            key={cat.slug}
            href={`/${locale}/books?${qs({ category: cat.slug, page: "1" })}`}
            style={{
              border: "1px solid var(--line)",
              borderRadius: 999,
              paddingInlineStart: "0.75rem",
              paddingInlineEnd: "0.75rem",
              paddingBlockStart: "0.35rem",
              paddingBlockEnd: "0.35rem",
              background: category === cat.slug ? "var(--primary)" : "var(--surface)",
              color: category === cat.slug ? "#fff" : "var(--ink)",
              textDecoration: "none",
            }}
          >
            {locale === "ar" ? cat.name_ar : cat.name_fr}
          </a>
        ))}
      </div>
      {data.items.length === 0 ? (
        <p style={{ color: "var(--ink-soft)" }}>{t("empty")}</p>
      ) : (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, 1fr)",
            gap: "1rem",
          }}
        >
          {data.items.map((b, i) => (
            <Reveal key={b.work_id} dir={dir} delay={i * 0.04}>
              <BookCard book={b} locale={locale} inStockText={t("inStock")} outOfStockText={t("outOfStock")} />
            </Reveal>
          ))}
        </div>
      )}
      {totalPages > 1 && (
        <div style={{ display: "flex", gap: "0.5rem", marginBlockStart: "1.5rem" }}>
          {page > 1 && (
            <a href={`/${locale}/books?${qs({ page: String(page - 1) })}`}>{t("prev")}</a>
          )}
          <span>
            {page} / {totalPages}
          </span>
          {page < totalPages && (
            <a href={`/${locale}/books?${qs({ page: String(page + 1) })}`}>{t("next")}</a>
          )}
        </div>
      )}
    </main>
  );
}

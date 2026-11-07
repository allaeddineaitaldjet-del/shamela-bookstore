import { Suspense } from "react";
import { Reveal } from "@/components/motion/reveal";
import { listBooks, listCategories } from "@/lib/api";
import { BookCard } from "@/components/book-card";
import { redirect } from "next/navigation";

export default async function HomePage({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string }>;
  searchParams?: Promise<{ q?: string }>;
}) {
  return (
    <Suspense fallback={null}>
      <HomeContent params={params} searchParams={searchParams} />
    </Suspense>
  );
}

async function HomeContent({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string }>;
  searchParams?: Promise<{ q?: string }>;
}) {
  const { locale } = await params;
  const sp = (await searchParams?.catch(() => ({}))) as { q?: string } | undefined;
  const q = sp?.q?.trim();
  if (q) {
    const qs = new URLSearchParams({ q });
    redirect(`/${locale}/books?${qs.toString()}`);
  }
  const [cats, books] = await Promise.all([
    listCategories().catch(() => []),
    listBooks({ page: 1 }).catch(() => ({ items: [], count: 0 })),
  ]);
  const t = await import("next-intl/server").then((m) => m.getTranslations("HomePage"));
  const c = await import("next-intl/server").then((m) => m.getTranslations("Common"));
  const dir = locale === "ar" ? "rtl" : "ltr";
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
      <Reveal dir={dir}>
        <h1>{t("title")}</h1>
        <p>{t("subtitle")}</p>
        <form
          action={`/${locale}/books`}
          method="get"
          style={{ display: "flex", gap: "0.5rem", marginBlockStart: "1rem" }}
        >
          <input
            name="q"
            placeholder={t("searchPlaceholder")}
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
            {c("search")}
          </button>
        </form>
      </Reveal>
      <section style={{ marginBlockStart: "2rem" }}>
        <h2>{t("categories")}</h2>
        <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
          {cats.map((cat) => (
            <a
              key={cat.slug}
              href={`/${locale}/books?category=${cat.slug}`}
              style={{
                border: "1px solid var(--line)",
                borderRadius: 6,
                paddingInlineStart: "0.75rem",
                paddingInlineEnd: "0.75rem",
                paddingBlockStart: "0.5rem",
                paddingBlockEnd: "0.5rem",
                background: "var(--surface)",
                color: "var(--ink)",
                textDecoration: "none",
              }}
            >
              {locale === "ar" ? cat.name_ar : cat.name_fr}
            </a>
          ))}
        </div>
      </section>
      <section style={{ marginBlockStart: "2rem" }}>
        <h2>{t("latest")}</h2>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, 1fr)",
            gap: "1rem",
          }}
        >
          {books.items.slice(0, 8).map((b, i) => (
            <Reveal key={b.work_id} dir={dir} delay={i * 0.05}>
              <BookCard book={b} locale={locale} inStockText={c("inStock")} outOfStockText={c("outOfStock")} />
            </Reveal>
          ))}
        </div>
      </section>
    </main>
  );
}

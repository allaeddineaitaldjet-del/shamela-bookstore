import { BookCover } from "@/components/book-card";
import { formatPrice, getBook } from "@/lib/api";
import { OrderForm } from "./order-form";
import { Suspense } from "react";

export default function BookDetailPage(props: { params: Promise<{ locale: string; id: string }> }) {
  return (
    <Suspense fallback={null}>
      <BookDetailContent {...props} />
    </Suspense>
  );
}

async function BookDetailContent({
  params,
}: {
  params: Promise<{ locale: string; id: string }>;
}) {
  const { locale, id } = await params;
  const book = await getBook(id).catch(() => null);
  if (!book) {
    return (
      <main style={{ padding: "2rem", textAlign: "start" }}>
        <p>Not found</p>
      </main>
    );
  }
  const c = await import("next-intl/server").then((m) => m.getTranslations("Common"));
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
      <div style={{ display: "grid", gridTemplateColumns: "160px 1fr", gap: "1.5rem", alignItems: "start" }}>
        <BookCover title={book.title_ar} author={book.author} />
        <div>
          <h1>{book.title_ar}</h1>
          <p style={{ color: "var(--ink-soft)" }}>{book.author}</p>
          <p style={{ color: "var(--primary)", fontWeight: 700 }}>
            {formatPrice(book.price_dzd, locale)}
          </p>
          <p>{book.in_stock ? c("inStock") : c("outOfStock")}</p>
          {book.publisher && (
            <p>
              {c("publisher")}: {book.publisher}
            </p>
          )}
          {book.editor && (
            <p>
              {c("editor")}: {book.editor}
            </p>
          )}
          {book.pages != null && (
            <p>
              {c("pages")}: {book.pages}
            </p>
          )}
          {book.volumes != null && (
            <p>
              {c("volumes")}: {book.volumes}
            </p>
          )}
          {book.year_hijri != null && (
            <p>
              {c("yearHijri")}: {book.year_hijri}
            </p>
          )}
          {book.year_gregorian != null && (
            <p>
              {c("yearGregorian")}: {book.year_gregorian}
            </p>
          )}
        </div>
      </div>
      <OrderForm workId={book.work_id} />
    </main>
  );
}

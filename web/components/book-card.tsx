import Link from "next/link";
import type { BookRow } from "@/lib/api";
import { formatPrice } from "@/lib/api";
import { StarMotif } from "./star-motif";

export function BookCover({ title, author }: { title: string; author: string | null }) {
  return (
    <div
      className="flex aspect-[2/3] w-full flex-col items-center justify-between"
      style={{
        background: "var(--surface)",
        border: "1px solid var(--line)",
        borderRadius: 6,
        paddingInlineStart: "0.75rem",
        paddingInlineEnd: "0.75rem",
        paddingBlockStart: "1rem",
        paddingBlockEnd: "0.75rem",
        textAlign: "center",
      }}
      aria-label={`${title}${author ? ` — ${author}` : ""}`}
    >
      <span style={{ color: "var(--gold)" }}>
        <StarMotif />
      </span>
      <span
        style={{
          display: "-webkit-box",
          WebkitLineClamp: 4,
          WebkitBoxOrient: "vertical",
          overflow: "hidden",
          fontFamily: "var(--font-reem-kufi), serif",
          fontSize: 16,
          lineHeight: 1.5,
        }}
      >
        {title}
      </span>
      <span style={{ fontSize: 13, color: "var(--ink-soft)" }}>{author}</span>
    </div>
  );
}

export function BookCard({
  book,
  locale,
  inStockText,
  outOfStockText,
}: {
  book: BookRow;
  locale: string;
  inStockText: string;
  outOfStockText: string;
}) {
  return (
    <Link
      href={`/${locale}/books/${book.work_id}`}
      className="block"
      style={{ textDecoration: "none", color: "var(--ink)" }}
    >
      <BookCover title={book.title_ar} author={book.author} />
      <div style={{ marginBlockStart: "0.5rem" }}>
        <div
          style={{
            display: "-webkit-box",
            WebkitLineClamp: 2,
            WebkitBoxOrient: "vertical",
            overflow: "hidden",
            fontWeight: 600,
            lineHeight: 1.4,
          }}
        >
          {book.title_ar}
        </div>
        <div style={{ color: "var(--ink-soft)", fontSize: 14 }}>{book.author}</div>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <strong style={{ color: "var(--accent)" }}>{formatPrice(book.price_dzd, locale)}</strong>
          <span style={{ fontSize: 13 }}>
            {book.in_stock ? inStockText : outOfStockText}
          </span>
        </div>
      </div>
    </Link>
  );
}

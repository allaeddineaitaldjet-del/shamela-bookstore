import Link from "next/link";
import { useLocale } from "next-intl";

export function SiteHeader() {
  const locale = useLocale();
  const other = locale === "ar" ? "fr" : "ar";
  return (
    <header
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        paddingInlineStart: "1rem",
        paddingInlineEnd: "1rem",
        paddingBlockStart: "0.75rem",
        paddingBlockEnd: "0.75rem",
        borderBlockEnd: "1px solid var(--line)",
        background: "var(--surface)",
        maxWidth: 1100,
        marginInlineStart: "auto",
        marginInlineEnd: "auto",
        width: "100%",
      }}
    >
      <Link href={`/${locale}`} style={{ color: "var(--primary)", fontWeight: 700, textDecoration: "none" }}>
        {locale === "ar" ? "مكتبة الشاملة" : "Librairie Shamela"}
      </Link>
      <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
        <Link href={`/${locale}/books`} style={{ color: "var(--ink)", textDecoration: "none" }}>
          {locale === "ar" ? "الكتب" : "Livres"}
        </Link>
        <Link
          href={`/${other}`}
          style={{
            color: "var(--primary)",
            textDecoration: "none",
            border: "1px solid var(--primary)",
            borderRadius: 6,
            paddingInlineStart: "0.5rem",
            paddingInlineEnd: "0.5rem",
            minHeight: 32,
            display: "inline-flex",
            alignItems: "center",
          }}
        >
          {other === "ar" ? "العربية" : "Français"}
        </Link>
      </div>
    </header>
  );
}

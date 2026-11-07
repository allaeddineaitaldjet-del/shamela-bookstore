import { useLocale } from "next-intl";

export function SiteFooter() {
  const locale = useLocale();
  const ar = locale === "ar";
  return (
    <footer
      style={{
        borderBlockStart: "1px solid var(--line)",
        background: "var(--surface)",
        paddingInlineStart: "1rem",
        paddingInlineEnd: "1rem",
        paddingBlockStart: "2rem",
        paddingBlockEnd: "2rem",
        marginBlockStart: "3rem",
      }}
    >
      <div
        style={{
          maxWidth: 1100,
          marginInlineStart: "auto",
          marginInlineEnd: "auto",
          display: "flex",
          flexWrap: "wrap",
          gap: "1.5rem",
          justifyContent: "space-between",
        }}
      >
        <div>
          <strong>{ar ? "مكتبة الشاملة" : "Librairie Shamela"}</strong>
          <p style={{ color: "var(--ink-soft)", margin: "0.5rem 0 0 0" }}>
            {ar ? "تواصل معنا" : "Contact"} — {ar ? "الهاتف، الولاية" : "phone, wilaya"}
          </p>
        </div>
        <p style={{ color: "var(--ink-soft)", margin: 0 }}>
          {ar ? "الدفع عند الاستلام" : "Paiement à la livraison"}
        </p>
      </div>
    </footer>
  );
}

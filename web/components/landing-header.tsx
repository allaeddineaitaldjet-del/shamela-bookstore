"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useEffect, useState } from "react";

export function LandingHeader() {
  const locale = useLocale();
  const other = locale === "ar" ? "fr" : "ar";
  const [solid, setSolid] = useState(false);

  useEffect(() => {
    const onScroll = () => setSolid(window.scrollY > 40);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header style={{ position: "absolute", top: 0, insetInlineStart: 0, insetInlineEnd: 0, zIndex: 20, pointerEvents: "none" }}>
      <div
        aria-hidden
        style={{
          position: "absolute",
          inset: 0,
          background: "var(--surface)",
          opacity: solid ? 0.96 : 0,
          transition: "opacity 250ms ease-out",
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "relative",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          paddingInlineStart: "1rem",
          paddingInlineEnd: "1rem",
          paddingBlockStart: "0.75rem",
          paddingBlockEnd: "0.75rem",
          maxWidth: 1100,
          marginInlineStart: "auto",
          marginInlineEnd: "auto",
          pointerEvents: "auto",
        }}
      >
        <Link href={`/${locale}`} style={{ color: "var(--primary)", fontWeight: 700, textDecoration: "none" }}>
          {locale === "ar" ? "مكتبة الشاملة" : "Librairie Shamela"}
        </Link>
        <nav style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          <Link href={`/${locale}/books`} style={{ color: "var(--ink)", textDecoration: "none" }}>
            {locale === "ar" ? "الكتب" : "Livres"}
          </Link>
          <a href="#how" style={{ color: "var(--ink)", textDecoration: "none" }}>
            {locale === "ar" ? "كيف نعمل" : "Comment ça marche"}
          </a>
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
        </nav>
      </div>
    </header>
  );
}

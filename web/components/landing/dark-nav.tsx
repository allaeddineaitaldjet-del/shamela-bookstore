"use client";

import Link from "next/link";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useState } from "react";

function useScrollY() {
  const [y, setY] = useState(0);
  useEffect(() => {
    const onScroll = () => setY(window.scrollY);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  return y;
}

export function DarkNav() {
  const t = useTranslations("HomePage");
  const locale = useLocale();
  const ar = locale === "ar";
  const other = ar ? "fr" : "ar";
  const scrollY = useScrollY();
  const [menuOpen, setMenuOpen] = useState(false);

  const isSolid = scrollY > 40;
  const opacity = isSolid ? Math.min(1, (scrollY - 40) / 120) : 0;

  // Close the overlay when the desktop layout returns.
  useEffect(() => {
    const onResize = () => {
      if (window.innerWidth >= 768 && menuOpen) setMenuOpen(false);
    };
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, [menuOpen]);

  // Lock page scroll while the full-screen menu is open.
  useEffect(() => {
    document.body.style.overflow = menuOpen ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [menuOpen]);

  const linkClass = ar
    ? "text-sm font-medium text-[#A59C88] no-underline"
    : "text-sm font-medium uppercase tracking-[0.08em] text-[#A59C88] no-underline";

  return (
    <nav
      className="fixed inset-x-0 top-0 z-[100] flex h-[72px] items-center justify-between border-b border-[rgba(169,139,78,0.2)] px-4 transition-[background-color,backdrop-filter] duration-200"
      style={{
        background: isSolid ? `rgba(13,15,14,${opacity})` : "transparent",
        backdropFilter: isSolid ? "blur(8px)" : "none",
      }}
    >
      {/* Wordmark — start side */}
      <Link
        href={`/${locale}`}
        className={`text-base font-bold text-[#EDE6D6] no-underline ${
          ar ? "" : "uppercase tracking-[0.02em]"
        }`}
      >
        {t("title")}
      </Link>

      {/* Desktop links + language switch — end side */}
      <div className="nav-desktop flex items-center gap-6">
        <Link href={`/${locale}/books`} className={linkClass}>
          {t("browse")}
        </Link>
        <a href="#how" className={linkClass}>
          {t("howItWorks")}
        </a>
        <Link
          href={`/${other}`}
          className="inline-flex min-h-8 items-center rounded-[2px] border border-[#A98B4E] px-2.5 text-[13px] font-semibold text-[#A98B4E] no-underline"
        >
          {other === "ar" ? "العربية" : "Français"}
        </Link>
      </div>

      {/* Mobile menu button */}
      <button
        type="button"
        className="nav-menu-btn hidden cursor-pointer border-0 bg-transparent p-2 text-2xl leading-none text-[#A59C88]"
        aria-label={menuOpen ? t("menuClose") : t("menuOpen")}
        aria-expanded={menuOpen}
        aria-controls="landing-mobile-menu"
        onClick={() => setMenuOpen((v) => !v)}
      >
        {menuOpen ? "✕" : "☰"}
      </button>

      {/* Mobile full-screen overlay */}
      {menuOpen && (
        <div
          id="landing-mobile-menu"
          className="fixed inset-0 z-[99] flex flex-col items-center justify-center gap-8 bg-[rgba(13,15,14,0.97)]"
        >
          <Link
            href={`/${locale}/books`}
            className="text-2xl font-medium text-[#A59C88] no-underline"
            onClick={() => setMenuOpen(false)}
          >
            {t("browse")}
          </Link>
          <a
            href="#how"
            className="text-2xl font-medium text-[#A59C88] no-underline"
            onClick={() => setMenuOpen(false)}
          >
            {t("howItWorks")}
          </a>
          <Link
            href={`/${other}`}
            className="rounded-[2px] border border-[#A98B4E] px-4 text-xl font-semibold text-[#A98B4E] no-underline"
            onClick={() => setMenuOpen(false)}
          >
            {other === "ar" ? "العربية" : "Français"}
          </Link>
          <button
            type="button"
            className="mt-4 cursor-pointer border-0 bg-transparent text-sm text-[#A59C88] underline"
            onClick={() => setMenuOpen(false)}
          >
            {t("menuClose")}
          </button>
        </div>
      )}
    </nav>
  );
}
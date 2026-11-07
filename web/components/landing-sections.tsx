"use client";

import { useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useGSAP } from "@gsap/react";
import { motion, useReducedMotion } from "motion/react";
import { useLocale, useTranslations } from "next-intl";
import Link from "next/link";
import type { BookRow, CategoryRow } from "@/lib/api";
import { BookCard } from "@/components/book-card";
import { DarkHero } from "@/components/landing/dark-hero";
import { useLenisScrollTrigger } from "@/components/motion/use-lenis-gsap";

gsap.registerPlugin(ScrollTrigger, useGSAP);

export function LandingSections({
  categories,
  books,
  total,
}: {
  categories: CategoryRow[];
  books: BookRow[];
  total: number;
}) {
  const t = useTranslations("HomePage");
  const c = useTranslations("Common");
  const locale = useLocale();
  const dir = locale === "ar" ? "rtl" : "ltr";
  const reduce = useReducedMotion();
  const scope = useRef<HTMLElement>(null);
  useLenisScrollTrigger();

  useGSAP(
    () => {
      if (reduce) return;
      // Featured horizontal parallax — vertical fallback in RTL safety:
      // we animate x only, flipped for RTL, pinned section.
      const track = gsap.utils.selector(".feat-track");
      const getAmt = () => (track(".feat-item").length * 240) - window.innerWidth * 0.6;
      gsap.to(".feat-track", {
        x: () => (dir === "rtl" ? getAmt() : -getAmt()),
        ease: "none",
        scrollTrigger: {
          trigger: ".feat-pin",
          start: "top top+=80",
          end: () => `+=${getAmt()}`,
          scrub: true,
          pin: true,
          anticipatePin: 1,
          invalidateOnRefresh: true,
        },
      });
      // SVG line draw
      const path = scope.current?.querySelector<SVGPathElement>(".how-line");
      if (path) {
        const len = path.getTotalLength();
        gsap.fromTo(
          path,
          { strokeDashoffset: len },
          {
            strokeDashoffset: 0,
            duration: 1.2,
            ease: "power2.out",
            scrollTrigger: { trigger: "#how", start: "top 70%" },
          }
        );
      }
    },
    { scope, dependencies: [dir] }
  );

  return (
    <main ref={scope} style={{ overflowX: "hidden" }}>
      {/* Hero */}
      <DarkHero total={total} />

      {/* Categories */}
      <section style={{ maxWidth: 1100, marginInlineStart: "auto", marginInlineEnd: "auto", paddingInlineStart: "1rem", paddingInlineEnd: "1rem", paddingBlockStart: "4rem" }}>
        <h2>{t("categories")}</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px,1fr))", gap: "1rem", marginBlockStart: "1rem" }}>
          {categories.map((cat, i) => (
            <motion.a
              key={cat.slug}
              href={`/${locale}/books?category=${cat.slug}`}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.05, ease: "easeOut" }}
              whileHover={reduce ? undefined : { rotateX: 3, rotateY: dir === "rtl" ? -3 : 3 }}
              style={{
                border: "1px solid var(--line)",
                outline: "2px solid var(--gold)",
                outlineOffset: 2,
                borderRadius: 6,
                padding: "1.5rem",
                background: "var(--surface)",
                color: "var(--ink)",
                textDecoration: "none",
                textAlign: "center",
                fontWeight: 700,
              }}
              id={cat.slug}
            >
              {locale === "ar" ? cat.name_ar : cat.name_fr}
            </motion.a>
          ))}
        </div>
      </section>

      {/* Featured horizontal */}
      <section className="feat-pin" style={{ paddingBlockStart: "4rem", overflow: "hidden" }}>
        <div style={{ maxWidth: 1100, marginInlineStart: "auto", marginInlineEnd: "auto", paddingInlineStart: "1rem", paddingInlineEnd: "1rem" }}>
          <h2>{t("latest")}</h2>
        </div>
        <div className="feat-track" style={{ display: "flex", gap: "1rem", paddingInlineStart: "1rem", paddingInlineEnd: "1rem", marginBlockStart: "1rem" }}>
          {books.slice(0, 6).map((b) => (
            <div key={b.work_id} className="feat-item" style={{ minWidth: 220, width: 220 }}>
              <BookCard book={b} locale={locale} inStockText={c("inStock")} outOfStockText={c("outOfStock")} />
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section id="how" style={{ maxWidth: 1100, marginInlineStart: "auto", marginInlineEnd: "auto", paddingInlineStart: "1rem", paddingInlineEnd: "1rem", paddingBlockStart: "4rem" }}>
        <h2>{t("howTitle")}</h2>
        <svg width="100%" height="24" viewBox="0 0 600 24" preserveAspectRatio="none" style={{ marginBlockStart: "1rem", opacity: 0.9 }}>
          <path className="how-line" d="M10 12 H590" stroke="var(--gold)" strokeWidth="2" fill="none" />
        </svg>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(240px,1fr))", gap: "1rem", marginBlockStart: "1rem" }}>
          {[t("step1"), t("step2"), t("step3")].map((s, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1, ease: "easeOut" }}
              style={{
                border: "1px solid var(--line)",
                outline: "2px solid var(--gold)",
                outlineOffset: 2,
                borderRadius: 6,
                padding: "1.5rem",
                background: "var(--surface)",
                textAlign: "center",
              }}
            >
              <div style={{ fontSize: 28, color: "var(--primary)", fontWeight: 700 }}>{i + 1}</div>
              <div style={{ marginBlockStart: "0.5rem" }}>{s}</div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section style={{ textAlign: "center", paddingBlockStart: "4rem", paddingBlockEnd: "2rem" }}>
        <Link
          href={`/${locale}/books`}
          style={{
            background: "var(--primary)",
            color: "#fff",
            paddingInlineStart: "2rem",
            paddingInlineEnd: "2rem",
            minHeight: 48,
            display: "inline-flex",
            alignItems: "center",
            borderRadius: 6,
            textDecoration: "none",
            fontWeight: 700,
          }}
        >
          {t("browse")}
        </Link>
      </section>
    </main>
  );
}
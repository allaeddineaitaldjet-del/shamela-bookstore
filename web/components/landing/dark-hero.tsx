"use client";

import Link from "next/link";
import { useLocale, useTranslations } from "next-intl";
import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";
import { useReducedMotion } from "motion/react";
import { Hero3DWrapper } from "@/components/hero-3d-wrapper";
import { splitWords } from "@/lib/utils";

gsap.registerPlugin(useGSAP);

export function DarkHero({ total }: { total: number }) {
  const t = useTranslations("HomePage");
  const locale = useLocale();
  const ar = locale === "ar";
  const reduce = useReducedMotion();
  const scope = useRef<HTMLElement>(null);
  const words = splitWords(t("heroTitle"));

  useGSAP(
    () => {
      const q = gsap.utils.selector(scope);

      // Reduced motion: fade only, no movement.
      if (reduce) {
        gsap.from(
          [q(".hero-label"), q(".hero-word"), q(".hero-sub"), q(".hero-btns"), q(".hero-book")],
          { opacity: 0, duration: 0.3, stagger: 0.04, ease: "none" }
        );
        return;
      }

      // Entrances: headline words -> subline -> buttons, book fades and rises. ~0.85s total.
      const tl = gsap.timeline({ defaults: { ease: "power2.out" } });
      tl.from(q(".hero-label"), { opacity: 0, y: 12, duration: 0.3 }, 0)
        .from(
          q(".hero-word"),
          { opacity: 0, y: 24, duration: 0.5, stagger: 0.06 },
          0.05
        )
        .from(q(".hero-sub"), { opacity: 0, y: 16, duration: 0.45, stagger: 0.08 }, 0.3)
        .from(q(".hero-btns"), { opacity: 0, y: 12, duration: 0.4 }, 0.45)
        .from(q(".hero-book"), { opacity: 0, y: 30, duration: 0.6 }, 0.2);
    },
    { scope, dependencies: [locale, reduce] }
  );

  return (
    <section
      ref={scope}
      aria-label={ar ? "الواجهة" : "Bannière"}
      className="relative z-10 mx-auto grid min-h-screen w-full max-w-[1280px] grid-cols-12 content-center items-center pt-[120px] pb-16"
    >
      {/* Text — first in DOM (accessibility), start side on desktop */}
      <div className="hero-text z-10 col-span-5 flex flex-col justify-center gap-6 px-4">
        <span
          className={`hero-label text-[13px] font-semibold uppercase text-[#A98B4E] ${
            ar ? "" : "tracking-[0.15em]"
          }`}
        >
          {t("heroLabel")}
        </span>

        <h1
          className="hero-title m-0 flex flex-wrap gap-[0.3em] text-[#EDE6D6]"
          style={{
            fontFamily: "var(--font-reem-kufi), 'Reem Kufi', serif",
            fontSize: "clamp(3.2rem, 8vw, 7.5rem)",
            lineHeight: 1.05,
          }}
        >
          {words.map((w, i) => (
            <span key={i} className="hero-word inline-block">
              {w}
            </span>
          ))}
        </h1>

        <p
          className="hero-sub m-0 max-w-[480px] text-lg text-[#A59C88]"
          style={{
            fontFamily: "var(--font-noto-naskh), 'Noto Naskh Arabic', serif",
            lineHeight: 1.7,
          }}
        >
          {t("heroLine")}
        </p>

        <p
          className="hero-sub m-0 text-base text-[#A59C88]"
          style={{
            fontFamily: "var(--font-noto-naskh), 'Noto Naskh Arabic', serif",
            lineHeight: 1.5,
          }}
        >
          {t("bookCount", { count: total })}
        </p>

        <div className="hero-btns mt-2 flex flex-wrap gap-4">
          <Link
            href={`/${locale}/books`}
            className="inline-flex h-11 items-center rounded-[2px] border-0 bg-[var(--primary)] px-6 text-[15px] font-bold text-[#EDE6D6] no-underline"
          >
            {t("browse")}
          </Link>
          <a
            href="#how"
            className={`inline-flex h-11 items-center rounded-[2px] border border-[#A98B4E] px-6 text-[15px] font-medium text-[#A98B4E] no-underline ${
              ar ? "" : "tracking-[0.05em]"
            }`}
          >
            {t("howItWorks")}
          </a>
        </div>
      </div>

      {/* 3D book — second in DOM, end side on desktop; lower z than the text column */}
      <div className="hero-book relative z-[5] col-span-7 flex items-center justify-center lg:-ms-8">
        <div className="hero-book-slot relative">
          {/* Soft blurred floor shadow (CSS ellipse) */}
          <div
            aria-hidden
            className="absolute bottom-4 left-1/2 h-5 w-1/2 -translate-x-1/2 rounded-[50%] bg-black/40 blur-xl"
          />
          <Hero3DWrapper />
        </div>
      </div>
    </section>
  );
}
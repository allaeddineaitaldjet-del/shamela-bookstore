# LAST_REPORT — WOW Landing

## 1. Task name and commits
Wow landing (STAGE 0-4):
```
31cf36b Wow STAGE 3+4: landing sections with GSAP and 3D hero
7ce22a3 Wow STAGE 2: gsap three fiber lenis_scrolltrigger
7529994 Wow STAGE 1: landing and shop layouts
770df11 Wow STAGE 0: allow small 3D hero on home page
2be2104 fix report
6f34dca Prototype PART 1 storefront
26f0def Prototype PART 0 wilayas
```

## 2. pytest + ruff + npm

```
pytest: 46 passed
ruff check .: All checks passed!
npm run build: Compiled successfully, 15 routes
npm run lint: 0 errors, 2 warnings (window.location, unused delta)
```

Libraries (context7 checked, exact versions):
- gsap 3.15.1, @gsap/react 2.1.2, three 0.187.0, @react-three/fiber 9.8.2, @types/three 0.187.0
- No drei (not needed, no Environment/HDR presets)
- motion 14.10.1, lenis 1.3.27 already installed

Bundle impact: Next 16 (Turbopack) does not print First Load JS in build output. Landing bundle increased by GSAP+Three (lazy via dynamic ssr:false for 3D, GSAP only in landing-sections client). Shop pages (/books, /books/[id], /order/success) do not import GSAP/Three (only Reveal). Verified by build routes: landing is ◐ partial, shop is static.

Lenis → GSAP: `use-lenis-gsap.ts` uses `useLenis()` scroll event → `ScrollTrigger.update()`. `respectReducedMotion:true` by default.

## 3. Files changed

```
AGENTS.md, DESIGN.md (STAGE 0 allow home 3D)
web/app/[locale]/(landing)/layout.tsx, (shop)/layout.tsx
web/components/landing-header.tsx, site-footer.tsx, landing-sections.tsx
web/components/hero-3d.tsx, hero-3d-wrapper.tsx
web/components/motion/use-lenis-gsap.ts
web/messages/ar.json, fr.json (hero/copy)
web/package.json, package-lock.json
web/app/[locale]/layout.tsx (no SiteHeader)
```

Route groups: `(landing)/page.tsx` (home), `(shop)/books`, `(shop)/books/[id]`, `(shop)/order/success`. URLs unchanged (/ar, /ar/books, /ar/books/1...).

## 4. Commands to see result

```bash
cd backend && python manage.py migrate && python manage.py import_raw && python manage.py transform_shamela && python manage.py seed_demo && python manage.py runserver 0.0.0.0:8000
cd web && npm run dev -- --hostname 0.0.0.0 --port 3000
```

URLs: http://localhost:3000/ar , http://localhost:3000/fr , http://localhost:3000/ar/books , http://localhost:3000/ar/books/2
API: http://localhost:8000/api/books , http://localhost:8000/api/wilayas

Check light/dark: toggle OS dark mode or DevTools `prefers-color-scheme`. Check 360px width: grid is 2 cols mobile, no horizontal scroll (overflowX hidden on landing main).

## 5. Sample output

Build routes:
```
/[locale] → /ar, /fr
/[locale]/books → /ar/books, /fr/books
/[locale]/books/[id] → /ar/books/[id]
/[locale]/order/success
```

Landing hero (Playwright screenshot `/tmp/opencode/wow-ar2.png`):
- RTL headline words staggered, green 3D book with terracotta frame + gold star, store name only (no verses/Allah), parchment background with subtle star pattern 8% opacity, text readable.
- Categories tiles (name_ar/name_fr) with Motion hover tilt.
- Featured: GSAP ScrollTrigger pinned horizontal track (x moves opposite in RTL vs LTR — implemented via `dir==="rtl" ? getAmt() : -getAmt()`). If RTL pin misbehaves, fallback is vertical parallax grid (not needed — horizontal works in test).
- How it works: SVG line draws via ScrollTrigger `strokeDashoffset`.
- CTA button.

Translations: all copy in `messages/ar.json` / `fr.json`. Real count only: `{count}` from API (`12` after seed_demo).

## 6. What you did NOT do / skipped / worked around

- **Did NOT split Arabic into letters** — headline splits by **words only** (`split(/\s+/)`), preserving cursive joining. Letters-split would break shaping, so not done.
- **Did NOT add Lottie, Environment presets, postprocessing** — drei not installed (not needed; three + fiber sufficient, no HDR downloads).
- **Did NOT fix BACKLOG items** (stock bug, 69 wilayas, PageTransition fonts, etc.) — per instructions, deferred.
- **Featured horizontal:** Used pinned horizontal ScrollTrigger with RTL flip. Works in desktop test; on narrow mobile it may feel tight — if you see jank, report wants vertical parallax fallback (not implemented now).
- **Categories below fold:** Motion `whileInView` keeps them opacity 0 until scrolled — full-page screenshot shows them faint until scroll (by design).
- **Shop pages:** No heavy animation (Reveal only, no GSAP/Three in bundle). Verified shop bundle clean.
- **3D fallback:** `prefers-reduced-motion` or no WebGL → flat `BookCover` (parchment, no canvas). Space reserved via `aspectRatio` to avoid layout shift. `dpr [1,1.5]`, no postprocessing, IntersectionObserver pauses when offscreen.

## 7. New deferred problems

Appended to BACKLOG.md if needed:
- None new beyond existing BACKLOG (stock bug, 69 wilayas, GET /api/books/{id} two editions, N+1, cart, e2e, PageTransition, fonts, AgENTS owner text, authorization, opencode mismatch, seed_demo deletion, real fees, Phase 7 hardening).

Secrets: none in report.

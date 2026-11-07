# DESIGN.md: Al-Shamela Bookstore visual rules

Read this before any UI work. If a rule here conflicts with a request, say so and ask.

## Principles
- Arabic first (RTL), French second (mirrored LTR). Design the Arabic page, then check French.
- Calm, scholarly, warm: a good bookshop, not a flashy shop.
- Rich motion is welcome (see Animation). Old phones are not a target, but keep the first page load light: heavy libraries load only where used.
- Text must always be readable. Ornament never sits behind body text.

## Colors (CSS variables in web/app/globals.css)
Light mode:
- --bg: #F6EFE0 (parchment)
- --surface: #FFFBF2 (cards)
- --ink: #2A2118 (main text)
- --ink-soft: #6B5B49 (secondary text)
- --primary: #1F5C4A (deep green: buttons, links)
- --accent: #B5532F (terracotta: highlights, prices)
- --gold: #B8913A (thin borders, small ornaments only)
- --line: #D9CBB0 (dividers)

Dark mode (prefers-color-scheme: dark):
- --bg: #16130F, --surface: #201B15, --ink: #F1E7D3, --ink-soft: #B8A98E,
  --primary: #4FA088, --accent: #D9774F, --gold: #C9A24D, --line: #3A3126

Rules: body text contrast at least 4.5:1. Never use color alone to show state (add text or icon). Gold is for decoration only, never for text.

## Typography
- Arabic body: Noto Naskh Arabic (or Amiri). Size 18px minimum, line-height 1.9.
- Arabic headings and book titles on covers: Reem Kufi or Amiri bold.
- French/Latin: a readable serif for headings (for example Lora), system sans for UI.
- Load at most 2 Arabic font files, subset if possible, `font-display: swap`. Self-host through next/font.
- Do NOT use Geist for Arabic (it has no Arabic glyphs).
- Digits: Western digits (0-9) for prices, phone numbers and quantities, in both languages.
- Prices: integer DZD, shown as `1 200 د.ج` (ar) and `1 200 DA` (fr).

## Ornament
- One signature motif: an eight-pointed star / geometric (girih style) pattern as a small inline SVG, under 2 KB.
- Use it for: section dividers, page header band, empty states, 3D book edge. Opacity 6-12% as a background, 100% only as a small divider.
- Thin double border (line + gold) around feature cards. Rounded corners: 6px max.
- No figurative imagery (people, animals). No stock photos of mosques or desert scenes.

## Sacred text: what NOT to do
- Never use Quranic verses, hadith, or the name of Allah as decoration on buttons, footers, error pages, loading states, or anything easily scrolled over or tapped.
- Never put them in images that could be cropped or in text that could be truncated.
- Basmala only on a dedicated page header, in a clean Naskh font, fully shown, never cropped, never behind other content.
- Book titles and quotations from books are content (shown in full), not decoration.

## Layout
- Mobile first. Breakpoints: 640, 1024.
- Use CSS logical properties (margin-inline-start, padding-inline-end, text-align: start) everywhere, never left/right, so RTL and LTR both work.
- Icons that show direction (arrows, chevrons) must flip in RTL.
- Max content width 1100px. Generous spacing.
- Book grid: 2 columns on phone, 3 on tablet, 4-5 on desktop. Cover ratio 2:3.

## Components (build these first, reuse everywhere)
- Button: primary (green, white text), secondary (outline), danger. Min height 44px.
- Book card: cover, title (max 2 lines), author, price. No "add to cart" (orders use a form).
- Order form: big inputs, labels above, inline Arabic error messages, one primary button "اطلب الآن" / "Commander".
- Header: logo text, search box, language switch (AR / FR).
- Footer: contact (phone, wilaya), delivery note, "paiement à la livraison / الدفع عند الاستلام".

## Covers (generated, no AI image model)
- HTML/CSS template rendered with Playwright: parchment background, terracotta frame, geometric corner motif, Arabic title centered (Naskh/Kufi), author at the bottom.
- Same template for every book. Long titles shrink to fit (never overflow, never cut mid-word).
- Size 600x900 PNG/WebP, under 80 KB each.

## 3D book (book page only)
- Lazy-loaded, never on the home or list pages.
- Plain CSS flat cover as the fallback (used when WebGL is unavailable or the user has prefers-reduced-motion).
- Idle: gentle float and slow tilt are allowed. Drag to rotate, with inertia. Open-book / page-flip animation on click is welcome.
- All of it off when prefers-reduced-motion is set (flat CSS cover instead).

## Animation
Libraries (ask context7 for current docs and install exact versions; do not guess APIs):
- **Motion** (package `motion`, import from `motion/react`): page transitions, fade/slide-in on scroll, staggered book grids, hover and tap effects, shared-element transition from book card to book page.
- **GSAP** (+ ScrollTrigger): scroll-driven storytelling on the home page (hero, featured books, category sections). Use only on pages that need it.
- **Lenis**: smooth scrolling. Must work in RTL. Disable when prefers-reduced-motion is set.
- **React Three Fiber + drei**: 3D book on the book page only (already planned).
Do not add Lottie or other libraries without asking.

Rules:
- Animate `transform` and `opacity` only (never width, height, top, left).
- Durations: UI feedback 150-250 ms, entrances 400-700 ms, hero effects up to 1.2 s. Easing: ease-out for entrances.
- RTL: slide-ins come from the reading direction side. Use logical values, flip x offsets when dir="rtl".
- Always honor prefers-reduced-motion: replace movement with a simple fade or nothing.
- Heavy libraries (GSAP, Three.js) are dynamically imported, never in the shared layout bundle.
- Never animate the order form or error messages in a way that delays input. No motion on sacred text.
- Never animate while content is loading in a way that causes layout shift.

## Accessibility
- Visible focus outline (2px --primary offset 2px).
- Alt text on every cover: title + author.
- `lang` and `dir` set on <html>; mixed Arabic/Latin text wrapped with `dir="auto"` where needed.
- Respect prefers-reduced-motion and prefers-color-scheme.

## Phase check
Before finishing any UI task, check: (1) /ar looks right in RTL, (2) /fr mirrors correctly, (3) text readable in light and dark mode, (4) no horizontal scroll at 360px width, (5) animations work in RTL and stop with reduced-motion on.

# LAST_REPORT — Landing step 1: dark editorial nav + hero

## 1. Task name and commits

Landing redesign step 1 (navigation bar + hero section only):
```
3a80193 Landing step 1: dark editorial nav and hero
(latest commit) Landing step 1: report
```
The latest commit only contains this report.

Scope respected: shop pages, backend, API code, i18n key meanings and the landing sections below the hero were not redesigned. The landing wrapper now darkens those existing sections and the footer by overriding the design tokens, as requested.

## 2. pytest, ruff, npm

- `ruff check .`: **All checks passed!** (run with `uvx ruff` because the container toolchain is not present here).
- `pytest`: **NOT RUN — honest limitation.** This session runs on the host, not inside the Dev Container: pytest/pytest-django are not installed and PostgreSQL is not reachable at the expected host. No backend file was touched, so the backend test suite is unaffected, but I could not produce its output. `docker compose ps` shows no running services.
- `npm run lint`: **0 errors**, 1 warning already present before this task (`order-form.tsx`, `window.location.href`).
- `npm run build`: **success**, 15 routes generated (same route list as before).

## 3. Files created or changed (`git diff --stat ae3c1f8 HEAD`)

```
 BACKLOG.md                            |   1 +
 DESIGN.md                             |  25 +++++
 reports/screens/hero-ar-1440.png      | Bin 0 -> 1056203 bytes
 reports/screens/hero-ar-390.png       | Bin 0 -> 262007 bytes
 reports/screens/hero-ar-768.png       | Bin 0 -> 657932 bytes
 reports/screens/hero-fr-1440.png      | Bin 0 -> 1078424 bytes
 reports/screens/metrics.json          | 174 ++++++++++++++++++++++++++++++++++
 web/app/[locale]/(landing)/layout.tsx |  18 ++--
 web/app/globals.css                   |  91 ++++++++++++++++++
 web/components/hero-3d-wrapper.tsx    |  31 +++---
 web/components/hero-3d.tsx            | 111 +++++++++++++++++-----
 web/components/landing-sections.tsx   | 101 +-------------------
 web/components/landing/dark-bg.tsx    |  29 ++++++
 web/components/landing/dark-hero.tsx  | 132 ++++++++++++++++++++++++++
 web/components/landing/dark-nav.tsx   | 134 ++++++++++++++++++++++++++
 web/lib/utils.ts                      |   3 +
 web/messages/ar.json                  |   3 +
 web/messages/fr.json                  |   3 +
 18 files changed, 712 insertions(+), 144 deletions(-)
```

Created: `web/components/landing/dark-bg.tsx`, `dark-nav.tsx`, `dark-hero.tsx`, `web/lib/utils.ts`, `reports/screens/*`.
Modified: landing layout, `globals.css`, `hero-3d.tsx`, `hero-3d-wrapper.tsx`, `landing-sections.tsx`, `ar.json`, `fr.json`, `DESIGN.md`, `BACKLOG.md`.

## 4. Commands to see the result

```bash
cd backend && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
cd web && npm run dev -- --hostname 0.0.0.0 --port 3000
```

URLs:
- http://localhost:3000/ar (RTL)
- http://localhost:3000/fr (LTR)

Both servers were already running while I checked. Screenshots are in `reports/screens/`.

## 5. Sample output (objective checks only)

Screenshots saved: `hero-ar-1440.png`, `hero-ar-768.png`, `hero-ar-390.png`, `hero-fr-1440.png` (viewport screenshots, 2 s after load).

| case | viewport | horizontal overflow | headline font-size | book slot / canvas height | console errors |
|---|---|---|---|---|---|
| ar | 1440x900 | no (1440 = 1440) | 115.2px | 576 / 576 px | 1 |
| ar | 768x1024 | no (768 = 768) | 61.44px | 420 / 420 px | 1 |
| ar | 390x844 | no (390 = 390) | 51.2px | 320 / 320 px | 1 |
| fr | 1440x900 | no (1440 = 1440) | 115.2px | 576 / 576 px | 1 |

Contrast ratios (computed from computed styles, WCAG formula):
- headline `#EDE6D6` on `#0D0F0E`: **15.47:1**
- body/subline `#A59C88` on `#0D0F0E`: **7.06:1**
- primary button text `#EDE6D6` on `#1F5C4A`: **6.28:1**
- outline button text `#A98B4E` on `#0D0F0E`: **5.94:1**

Layout audit (bounding boxes, CSS px):
```
ar 1440: text x=827..1360, book x=80..859   (32px overlap, text right / book left)
fr 1440: text x=80..613,   book x=581..1360 (32px overlap, text left / book right)
ar 768:  book y=184..604 (420px), text y=604..896 (book above text)
ar 390:  book y=120..440 (320px), text y=440..850; both buttons 358x44 px (full width)
DOM order in every case: text first, then book. Buttons pass elementFromPoint hit test.
Entrance finished: word opacity 1, book opacity 1 after 2.2 s.
```

Navigation:
```
top of page: nav background rgba(0,0,0,0)
after 300px scroll: nav background rgb(13,15,14)
mobile 390px: menu button visible -> overlay opens with 3 links, body scroll locked
reduced motion: canvas=false (flat cover), slot height 520px, emerald animation="none"
```

The single console error on every page is a **pre-existing Next.js 16 dev warning** (`Date.now()` while prerendering, from the API helper with `revalidate: 0`). It reproduces identically on the untouched `/ar/books` page, so it is not caused by this redesign. It was added to BACKLOG.

## 6. What I did NOT do / skipped / was unsure about

- **Did not judge the visuals** (per your instruction). Only DOM measurements are reported.
- **Did not run pytest** (see section 2): no Dev Container/Postgres/pytest in this session.
- **Did not use the Playwright MCP browser**: it expects `/ms-playwright`, which does not exist here and cannot be created without root. I installed Chromium into the user cache (`/tmp/opencode/pw`) and ran Playwright scripts directly. Screenshots are still real browser renders.
- **Did not fix the `Date.now()` dev warning** (pre-existing, also on untouched pages; logged in BACKLOG).
- **Did not migrate shop pages** to the dark theme; they stay light on purpose.
- **No new image assets**: background is CSS gradients + SVG feTurbulence only.
- **Hero 3D**: pointer parallax listens on `window` (not canvas events), so the text/buttons stay clickable; the canvas and the flat fallback share one slot box (no layout jump).

## 7. New deferred problems

Added to BACKLOG.md:
- Next 16 dev-mode `Date.now()` prerender error on API-backed pages (pre-existing; verify in production output when Cache Components is finalized).

No secrets, `.env` content, customer phone numbers or addresses appear in this report.

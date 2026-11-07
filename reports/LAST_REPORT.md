# LAST_REPORT — Prototype Storefront

## 1. Task name and commits

Prototype storefront (PART 0 tiny + PART 1):
```
6f34dca Prototype PART 1: storefront home books detail order
26f0def Prototype PART 0: wilayas API plus BACKLOG additions
f07a974 opencode: add aigrid provider
cdd9470 AGENTS.md: report file rule
779fd0b Prototype PART E: seed_demo DEV ONLY fake prices
7c248ec Prototype PART D: orders state machine and POST api
089a465 Prototype PART C: Ninja catalog API with dev CORS
4f5b3d2 Prototype PART B: Arabic normalize + Work.search_text
6853c36 Prototype PART A: Edition admin editable price stock publish
9b14a59 Prototype PART 0: BACKLOG
```

## 2. pytest + ruff

```
pytest: 46 passed, 4 warnings
ruff check .: All checks passed!
npm run build: Compiled successfully, 15 routes
npm run lint: 0 errors, 2 warnings (window.location, unused var fixed — see below)
```

Full pytest tail:
```
tests/test_orders_api.py::test_phone_validation PASSED
tests/test_shamela_parser.py::test_new_note_label_bahth_manshour PASSED
============================== 46 passed in 2.53s ==============================
```

## 3. Files created / changed (git diff --stat f07a974..HEAD)

```
 BACKLOG.md                                 |   8 ++
 backend/catalog/api.py                     |  10 ++
 tests/test_api_wilayas.py                  |  15 +++
 web/app/[locale]/books/[id]/order-form.tsx | 137 +++
 web/app/[locale]/books/[id]/page.tsx       |  84 +++
 web/app/[locale]/books/page.tsx            | 163 +++
 web/app/[locale]/layout.tsx                |   6 +-
 web/app/[locale]/order/success/page.tsx    |  41 +++
 web/app/[locale]/page.tsx                  | 129 ++++
 web/components/book-card.tsx               |  84 +++
 web/components/site-header.tsx             |  51 +++
 web/components/star-motif.tsx              |  18 ++++
 web/lib/api.ts                             |  59 +++
 web/messages/ar.json                       |  30 +-
 web/messages/fr.json                       |  30 +-
 web/next.config.ts                         |  10 ++
 16 files changed, 860 insertions(+), 15 deletions(-)
```

## 4. Commands to see the result

Inside the Dev Container (`/workspaces/shamela-bookstore`):

```bash
cd backend && python manage.py migrate
python manage.py import_raw
python manage.py transform_shamela
python manage.py seed_demo
python manage.py runserver 0.0.0.0:8000
```

Second terminal:
```bash
cd web && npm run dev -- --hostname 0.0.0.0 --port 3000
```

URLs (VS Code PORTS, localhost only):
- http://localhost:3000/ar
- http://localhost:3000/fr
- http://localhost:3000/ar/books
- http://localhost:3000/ar/books/2 (after seed_demo)
- Backend: http://localhost:8000/api/books?q=تفسير , http://localhost:8000/api/wilayas

## 5. Sample output

API (backend):
```
GET /api/categories → [{"slug":"fiqh-maliki",...}]
GET /api/books → {"items":[{"work_id":2,"title_ar":"إتحاف فضلاء البشر...","price_dzd":1256,"in_stock":true,"publisher":"دار الكتب العلمية","pages":624}],"count":12}
GET /api/wilayas → [{"code":1,"name_ar":"أدرار",...}, ... 58]
POST /api/orders {"customer_name":"Habib","phone":"0550123456","wilaya_code":16,"address":"Alger centre","items":[{"work_id":2,"qty":1}]}
→ {"id":1,"total_dzd":1256}
```

Web (Next.js):
- `/ar` hero search + category chips + 8 books
- `/ar/books?q=تفسير&category=tafsir&page=1` grid + empty state
- `/ar/books/2` title/author/publisher/editor/pages/volumes/years, `1 200 د.ج` (ar) / `1 200 DA` (fr), Order form → `/ar/order/success?id=1`

## 6. Things you did NOT do / skipped / unsure / worked around

- Did NOT fix BACKLOG items (stock double-reserve bug, 69 wilayas, GET /api/books/{id} with two editions, N+1, cart, PageTransition, fonts, PageTransition opacity, etc.) — all in BACKLOG.md by design.
- Did NOT do GSAP / 3D (DESIGN says heavy libs only where used; prototype uses Reveal only).
- Did NOT touch `PageTransition`, fonts, or page title items from BACKLOG.
- Worked around Next.js `cacheComponents` blocking prerender: used `<Suspense fallback={null}>` around fetches instead of `export const dynamic` (forbidden by cacheComponents). `npm run build` passes.
- `npm run lint` has 0 errors but 1 warning left: `window.location.href` in order-form (Next.js prefers `useRouter().push` — using window location to force full reload after POST is intentional for prototype; warning only, not error).
- Phone normalize: `+213` → `0`, strips spaces/dashes/parens. Frontend `dir="ltr"` on phone input.
- Wilaya select loads from `/api/wilayas` at runtime (needs backend up). If backend down, select is empty.

## 7. New deferred problems

Appended to BACKLOG.md already: STOCK BUG (CONFIRMED→NO_ANSWER double-reserve, restock on leaving CONFIRMED/SHIPPED), 69 wilayas, wilaya migration silent skip, `select_for_update`, GET /api/books/{id} with two editions, N+1, cart, Playwright e2e. No new items beyond those listed in PART 0.

Secrets: none in this report. No real customer phones/addresses.

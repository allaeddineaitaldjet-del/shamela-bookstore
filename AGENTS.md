# Al-Shamela Bookstore: project rules for AI agents

You are building an online bookstore for classical and contemporary Islamic books, for the Algerian market.
The owner is NOT a programmer. Explain what you did in plain English (business words in Arabic/French are fine),
keep every step small, and never make big silent changes.

## What the product is
Two interfaces, one backend:
1. **Storefront** (customers): browse, search (Arabic + French), book page with a 3D cover, "Order now" form.
2. **Seller/Admin desk** (the owner): every order arrives here with customer name, phone, wilaya, address and product.
   The seller phones the customer to confirm delivery. There is NO online payment. Payment is cash on delivery (paiement a la livraison).

## Stack (decided, do not change without asking)
- Backend: Python 3.12, Django 5.2 LTS, PostgreSQL 16 (via Docker/Dev Container), Django Ninja for the storefront API. All commands run inside the Dev Container; the host only runs Docker.
- Seller/Admin desk: customized Django admin (do not build a separate React admin).
- Storefront: Next.js + TypeScript (Node LTS, inside Dev Container), next-intl (ar/fr), RTL support. Three.js / React Three Fiber ONLY on the book page, lazy-loaded.
- Tests: pytest + pytest-django. Lint: ruff.

## Hard rules
- Money is an integer in DZD. Never floats.
- Every database change is a Django migration. Never edit an old migration.
- Order status changes ONLY through one function (the state machine). States:
  NEW -> TO_CALL -> CONFIRMED -> SHIPPED -> DELIVERED; side exits: NO_ANSWER (counted attempts), CANCELLED, REFUSED, RETURNED.
- Stock is reserved only when an order becomes CONFIRMED.
- The server recalculates prices and delivery fees. Never trust prices sent by the browser.
- Customer phone and address are personal data: visible only to Seller/Admin roles, never written to logs, never in test fixtures with real data.
- Arabic search text goes through ONE normalization function (strip tashkeel, unify alef/hamza forms, ya/alef-maqsura, ta-marbuta).
- Secrets live in environment variables / `.env` (git-ignored). Never read, print or commit `.env`.
- Tests never call the internet.
- Never invent data. Book metadata (ISBN, publisher, price, cover) must come from a named source. If unknown, leave it empty.
- No online payment code, no JWT, no gRPC.

## Data sourcing rules
- Shamela data is used under the owner's written authorization (see docs/shamela-authorization.md).
- Everything imported goes first into raw/staging tables (keep the original source + source URL + fetch date), then is transformed. The import must be re-runnable without creating duplicates.
- Data found by AI research (web search) goes ONLY into `data/review/*.csv` with columns: field, value, source_url, confidence. A human approves it before it enters the database.
- Respect robots.txt and rate limits on any site. Slow and polite beats fast.

## How to work
1. Start in **Plan** mode: write a short plan, wait for the owner to say "go".
2. Then implement ONE phase/task at a time (see PROMPTS.md).
3. After every task: run the tests and ruff, fix failures, then tell the owner exactly how to see the result (which command, which URL).
4. Commit after each working task with a clear message.
5. If a rule here blocks something the owner asks, say so and ask, do not silently break the rule.

## Commands (run inside the Dev Container, except docker compose)
- Start everything: Reopen folder in VS Code Dev Containers (uses `.devcontainer/docker-compose.yml`). Or from host: `docker compose -f .devcontainer/docker-compose.yml up -d --build`
- Run backend (from `backend/`): `cd backend && python manage.py migrate` then `cd backend && python manage.py runserver 0.0.0.0:8000`
- Run web (in `web/`): `cd web && npm run dev -- --hostname 0.0.0.0 --port 3000`
- Tests (from project root): `pytest`
- Lint (from project root): `ruff check .`

## Current phase
Phase 0 done. Next: Phase 1. Out of scope for now: online payment, user accounts for customers, reviews, coupons.

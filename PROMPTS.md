# Prompts to paste, one phase at a time (use Plan mode first)

Always start a session with: `Read AGENTS.md first. We are on Phase N.`

## Phase 0: scaffolding
Create the project skeleton following AGENTS.md: Django project with settings read from environment, docker-compose.yml with PostgreSQL, pytest + ruff configured, a Next.js app in /web with next-intl for Arabic and French and RTL. Add a README with the exact commands to start everything. Do not build features yet. Tell me how to see "hello" on both the backend and the web page.

## Phase 1: database and importer
Design and create the Django models: Author, Category, Work, Edition (ISBN, publisher, muhaqqiq, year, volumes, price in DZD integer, cover image, stock), Order, OrderLine, CallAttempt, DeliveryFee per wilaya (all 58 wilayas, fees empty for me to fill in). Add the raw staging tables for imports. Then write a re-runnable importer for the data I will place in data/raw/ (I will tell you the file format). Include tests proving re-running does not duplicate rows.

## Phase 2: catalog and Arabic search
Build the catalog API and storefront pages: home, category, search, book page. Implement the Arabic normalization function and PostgreSQL search (unaccent + trigram). Tests: searching with and without tashkeel and with alef variants finds the same book. Check RTL layout with Playwright and show me screenshots.

## Phase 3: ordering
Build the "Order now" form (name, phone validated for Algerian mobile numbers, wilaya, commune, address, note, quantity). Server computes totals and delivery fee. Add anti-spam: honeypot field, rate limit per IP and per phone, flag repeated phones. Create the order in status NEW then TO_CALL through the state-machine function.

## Phase 4: seller desk
Customize Django admin into the seller desk: default list "orders to call today", phone as clickable tel: link, buttons to move status, a call log with outcome and note, NO_ANSWER attempt counter, stock reserved only on CONFIRMED, two roles (Seller, Admin). Send a Telegram message to the seller on each new order (token from environment).

## Phase 5: data enrichment
Use @data-researcher to find editions and ISBNs for these books: (paste a list of 20 titles). Output to data/review/. Then help me review the CSV and write an importer for the approved rows.

## Phase 6: covers and 3D
Generate a typographic cover (parchment background, terracotta accents, Arabic title in a good Naskh font) for editions without an image. Build the 3D book viewer on the book page only: lazy-loaded, with a plain CSS fallback and respect for prefers-reduced-motion. Keep the page fast on a mid-range phone on 4G.

## Phase 7: hardening
Review everything against AGENTS.md. Add login rate limiting, secure cookie settings, CSRF, security headers, dependency scan, database backup script and a tested restore. Write a deployment guide for a small VPS in simple steps.

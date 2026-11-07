# BACKLOG (deferred, prototype scope)

- EditionAdmin.save_model locks on any save, including price-only edits: lock only when metadata fields change.
- transform_shamela review CSVs should skip locked editions.
- import_raw should check slugs before syncing categories.
- WorkAdmin.save_model should refresh Work.search_text.
- Web: PageTransition starts at opacity 0 (use a CSS keyframe fade), font weights (use variable fonts, max 2 Arabic font files), localized page title.
- AGENTS.md: owner is a CS student (not "NOT a programmer"); add "Read DESIGN.md before any UI work".
- Fill docs/shamela-authorization.md; make the repo private.
- opencode V1/V2 config mismatch in the container.
- DELETE seed_demo command and all demo prices before launch; real prices/stock from the supplier.
- Real delivery fees per wilaya (currently one flat env value).
- Phase 7 hardening: ALLOWED_HOSTS, SECRET_KEY, rate limiting on POST /api/orders, backups, deploy.

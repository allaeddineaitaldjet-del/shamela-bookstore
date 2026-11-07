# Al-Shamela Bookstore

Online bookstore for classical and contemporary Islamic books (Algeria).
Backend: Django + PostgreSQL in `backend/`. Web: Next.js (ar/fr, RTL) in `web/`.
Payment: cash on delivery. Phase 0 = skeleton only. No features yet.

## Rule: host runs only Docker

Your Fedora host **only** runs `docker` / `docker compose`.
Never run `pip`, `npm`, `sudo`, or Python/Node on the host.
Everything else runs inside the Dev Container (Python 3.12, Node LTS).

## Reopen in the container (step by step)

1. Open this folder in VS Code: `File -> Open Folder -> /home/spike/Documents/shamela-bookstore`
2. Install the VS Code extension **Dev Containers** (from the Marketplace) once.
3. Bottom-left green button in VS Code -> **Reopen in Container**. Wait for `app` + `postgres` to become healthy (first build takes ~10 min, later starts are fast).
4. Your VS Code terminal now runs **inside** the container (`/workspaces/shamela-bookstore`). All commands below run there, not on Fedora.

## Start opencode inside the container

In the container terminal:
```
opencode
```
opencode is pre-installed in the `app` image (`~/.opencode/bin/opencode`).
It reads `./opencode.json` at the project root. Login is saved in a named Docker volume (`opencode-data` -> `/home/vscode/.local/share/opencode`) and survives rebuilds.

To connect your AI provider:
- Inside opencode, type `/connect` and choose your provider (account or API key).
- If the browser callback does not open, use “API key in environment” — never paste keys into files.

Check integrations (in a separate terminal, not inside opencode):
```
opencode mcp list
```
You should see `context7` and `playwright` enabled, `perplexity` disabled.

## See “hello” on the backend

Inside the container (from project root):
```
cd backend && python manage.py migrate
cd backend && python manage.py runserver 0.0.0.0:8000
```
Open  http://localhost:8000/  (VS Code forwards `8000` to localhost only) -> you see:
```
Hello Al-Shamela Bookstore backend
```
Health check: `curl http://localhost:8000/health/` -> `{"status": "ok"}`

## See “hello” on the web page

Inside the container, in a second terminal:
```
cd web && npm run dev -- --hostname 0.0.0.0 --port 3000
```
Open:
- http://localhost:3000/ar -> Arabic, RTL (`dir="rtl"`), “مرحبا مكتبة الشاملة”
- http://localhost:3000/fr -> French, LTR, “Hello Librairie Shamela”

Ports are **only** forwarded to localhost via `forwardPorts` in `.devcontainer/devcontainer.json`. They are not published to your Wi-Fi.

## Tests and lint (inside container)

From project root:
```
pytest
ruff check .
```

Install dependencies (inside container, fresh container already does this via postCreate):
```
pip install -r backend/requirements-dev.txt
```

## Playwright inside the container

Browsers live at `/ms-playwright` (`PLAYWRIGHT_BROWSERS_PATH`). The MCP is headless:
```
PLAYWRIGHT_BROWSERS_PATH=/ms-playwright npx -y @playwright/mcp@latest --headless --browser chromium --help
```
If you see “Executable doesn't exist”, reinstall the browser with the same version:
```
PLAYWRIGHT_BROWSERS_PATH=/ms-playwright npx -y @playwright/mcp@latest --help
PLAYWRIGHT_BROWSERS_PATH=/ms-playwright npx -y playwright@latest install --with-deps chromium
```
If it still fails, stop and show the logs.

## Docker (host)

From the host (only these commands):
```
docker compose -f .devcontainer/docker-compose.yml up -d --build
docker compose -f .devcontainer/docker-compose.yml down
```
Do not use `down -v` — it deletes the `opencode-data` login volume.
Postgres is `postgres:16-bookworm`, service name `postgres`. Django connects via `DATABASE_URL` with `@postgres:5432`.

## Secrets

Copy `.env.example` to `.env` once (never commit `.env`). Your `.env` already exists with:
`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `POSTGRES_USER`, `POSTGRES_DB`, `POSTGRES_PASSWORD`, `DATABASE_URL` (@postgres:5432), `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.

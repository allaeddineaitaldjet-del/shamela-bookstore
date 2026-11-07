# syntax=docker/dockerfile:1
# Python 3.12 pinned (not host 3.14) + Node LTS + opencode + Playwright Chromium
FROM python:3.12-bookworm

ARG DEBIAN_FRONTEND=noninteractive

# OS deps for Node, opencode, postgres client and Playwright headless
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg git postgresql-client \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libasound2 libpango-1.0-0 libcairo2 libatspi2.0-0 \
 && rm -rf /var/lib/apt/lists/*

# Node.js LTS (24.x line - current LTS in 2026)
RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - \
 && apt-get install -y nodejs \
 && rm -rf /var/lib/apt/lists/*

# vscode user (UID 1000 matches Fedora host user) + opencode data dir for named volume
RUN groupadd -g 1000 vscode || true \
 && useradd -m -u 1000 -g 1000 -s /bin/bash vscode \
 && mkdir -p /home/vscode/.local/share/opencode /home/vscode/.local/state \
 && chown -R vscode:vscode /home/vscode/.local \
 && mkdir -p /ms-playwright \
 && chown vscode:vscode /ms-playwright

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV PLAYWRIGHT_SKIP_BROWSER_GC=1
ENV PATH=/home/vscode/.opencode/bin:$PATH

# opencode (installed for vscode user, binary at ~/.opencode/bin/opencode)
RUN su vscode -c 'curl -fsSL https://opencode.ai/install | bash' \
 && /home/vscode/.opencode/bin/opencode --version

# Playwright browsers (headless Chromium) shared readable path
# Installed as root so --with-deps can apt install libs; files owned by vscode after.
RUN PLAYWRIGHT_BROWSERS_PATH=/ms-playwright npx -y playwright@latest install --with-deps chromium \
 && PLAYWRIGHT_BROWSERS_PATH=/ms-playwright npx -y @playwright/mcp@latest --help >/dev/null 2>&1 || true \
 && chown -R vscode:vscode /ms-playwright \
 && chmod -R a+rX /ms-playwright

WORKDIR /workspaces/shamela-bookstore
USER vscode

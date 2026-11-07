# START HERE: setup in order (about 1 hour)

You do not write code. Your job: give clear instructions, check the result, and keep the project safe with git.

## 1. Install these (once)
- **VS Code**: https://code.visualstudio.com
- **Git**: https://git-scm.com
- **Docker**: https://docker.com — on Fedora install moby-engine (Docker). Docker is the only thing of the stack that runs on your host.
- **Python 3.12 and Node LTS**: you do NOT install them on your computer. They live inside the Dev Container (see `.devcontainer/`). On your host you only run `docker` / `docker compose` commands. Never use `sudo`, `pip`, or `npm` on the host.
- opencode: install and run it **inside** the Dev Container (see README.md), not on the host.
- Fedora/SELinux: the container mounts your project folder with a `:z` SELinux label so files stay readable (see `.devcontainer/docker-compose.yml`).

## 2. Create the project folder
1. Create a folder `shamela-bookstore` and copy ALL files from this kit into it (including the hidden `.opencode` folder, `.gitignore`).
2. Open the folder in VS Code (File -> Open Folder).
3. Open the VS Code terminal (Ctrl+`) and run:
   ```
   git init
   git add .
   git commit -m "Starter kit"
   ```
   Git is your undo button: commit after every task that works.

## 3. Install opencode (inside the Dev Container, not on the host)
opencode is already installed in the `app` container image via `.devcontainer/Dockerfile` (binary at `~/.opencode/bin/opencode` for user `vscode`). You do not run the curl installer on your Fedora host.

In the VS Code terminal (which after Reopen in Container runs inside the container):
```
opencode --version
```
Then run `opencode` in the VS Code terminal. The VS Code extension installs itself. Afterwards:
- `Ctrl+Esc` opens opencode in a split terminal; `Ctrl+Shift+Esc` starts a new session.
- Type `/connect` and pick your AI provider (you need an account or API key with one). Your login is saved in a named Docker volume (`opencode-data` -> `/home/vscode/.local/share/opencode`) and survives rebuilds.
- Press `Tab` to switch between **Plan** (thinks, writes plans, changes nothing) and **Build** (edits files).

## 4. Check the integrations loaded
In the terminal (not inside opencode): `opencode mcp list`
You should see `context7` and `playwright` enabled and `perplexity` disabled.
If opencode complains about the config format, tell me the exact error and your `opencode --version`.

## 5. What each integration is for
| Item | What it does | Needed? |
|---|---|---|
| **AGENTS.md** | The rules the AI reads every session | Yes, the most important file |
| **context7** (MCP) | Gives the AI up-to-date docs for Django, Next.js, Three.js | Yes, free |
| **playwright** (MCP) | The AI opens your site in a browser and checks pages, Arabic RTL, the order form | Yes, free |
| **reviewer** agent | Read-only inspector. Run it after every task: `@reviewer review my changes` | Yes |
| **data-researcher** agent | Finds book metadata on the web, writes proposals to `data/review/` | When you reach the data phase |
| **perplexity** (MCP) | Web research for the data-researcher. Needs a paid API key from Perplexity | Optional, off by default |

To turn Perplexity on: get an API key, set it as an environment variable named `PERPLEXITY_API_KEY` on your computer (do NOT paste it in files), then delete the line `"disabled": true` (and the comma before it) for `perplexity` in `opencode.json`.

Note: this kit is written for OpenCode v2 (config uses `mcp.servers`, a `permissions` list and `shell`). If your `opencode --version` starts with 1., the format is different, so ask for the v1 version of the files.

Not needed: a Postgres MCP, a filesystem MCP, GitHub MCP (they eat context and add risk). Skip plugins for now.

## 6. Your routine for every task
1. In **Plan** mode: paste the task prompt from PROMPTS.md. Read the plan. Reply "go" or ask for changes.
2. Switch to **Build**. Let it work.
3. Ask: `Run the tests and tell me exactly how to see the result.` Open that URL and click around yourself.
4. Run `@reviewer review my changes`. If it lists blocking problems, paste its fix instructions to the main agent.
5. `git add . && git commit -m "short description"`. Only then start the next task.

## 7. Safety rules for a non-programmer
- Never put passwords/API keys in files or chat. Environment variables only.
- Do not go public with real customer phone numbers and addresses until someone technical has reviewed security once (a freelancer for a few hours is enough).
- If the AI says everything works but you cannot see it working, it is not done.

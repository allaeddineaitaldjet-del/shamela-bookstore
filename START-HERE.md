# START HERE: setup in order (about 1 hour)

You do not write code. Your job: give clear instructions, check the result, and keep the project safe with git.

## 1. Install these (once)
- **VS Code**: https://code.visualstudio.com
- **Git**: https://git-scm.com
- **Node.js (LTS)**: https://nodejs.org
- **Python 3.12+**: https://python.org (Windows: tick "Add to PATH")
- **Docker Desktop**: https://docker.com (runs the database)
- Windows users: opencode usually works more smoothly inside **WSL** (Ubuntu). If the steps below give you errors, install WSL, open VS Code "in WSL", and repeat there.

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

## 3. Install opencode
In the VS Code terminal:
```
curl -fsSL https://opencode.ai/install | bash
opencode --version
```
(If that fails on Windows without WSL, check https://opencode.ai for the current install command.)

Then run `opencode` in the VS Code terminal. The VS Code extension installs itself. Afterwards:
- `Ctrl+Esc` opens opencode in a split terminal; `Ctrl+Shift+Esc` starts a new session.
- Type `/connect` and pick your AI provider (you need an account or API key with one).
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

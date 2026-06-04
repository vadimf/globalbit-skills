# hebrew-gpt — Globalbit Hebrew generation via OpenAI

An MCP server that produces native-quality Hebrew copy through OpenAI GPT, using
Globalbit's curated style guides. Built because ChatGPT's Hebrew register reads
better than most models' default Hebrew.

When connected to Claude Code, it exposes one tool, `generate_hebrew`, which any
agent calls instead of writing Hebrew directly.

## What's in this folder

| File | Purpose |
|---|---|
| `server.mjs` | The MCP server (Node, stdio). |
| `install.mjs` | Cross-platform installer (skills + deps + key + registration). |
| `package.json` / `package-lock.json` | Dependencies (`@modelcontextprotocol/sdk`). |
| `.env.example` | Template for the API key on Windows/Linux. |

## Requirements

- **Node.js 18+** (`node --version`)
- **Claude Code** installed (`claude --version`)
- **Your own OpenAI API key** — https://platform.openai.com/api-keys

## Install (recommended)

From this folder:

```bash
node install.mjs
```

The installer will:
1. Copy the `globalbit-hebrew` and `globalbit-hebrew-website-copy` skills into `~/.claude/skills/`
2. Run `npm install`
3. Store your OpenAI key (macOS Keychain, or a local `.env` on Windows/Linux)
4. Register the server with Claude Code (`claude mcp add --scope user`)
5. Optionally add a global rule to `~/.claude/CLAUDE.md`

Then **quit and reopen Claude Code**.

## Manual install

```bash
npm install

# API key — pick ONE:
#   macOS:
security add-generic-password -a "$USER" -s openai-api-key -w "sk-proj-..." -U
#   Windows/Linux: copy .env.example to .env and paste your key
cp .env.example .env   # then edit

# Register with Claude Code:
claude mcp add --scope user hebrew-gpt node "$(pwd)/server.mjs"
```

Copy the two `globalbit-hebrew*` skill folders from the repo root into
`~/.claude/skills/` yourself if you skip the installer.

## Usage

Once registered, Claude calls it automatically. The tool:

| `content_type` | Use for | Style source |
|---|---|---|
| `proposal` | proposals, PRDs, SOWs, exec summaries, formal emails | `globalbit-hebrew` skill |
| `website` | Hero, services/About pages, case studies, marketing | `globalbit-hebrew-website-copy` skill |
| `microcopy` | button labels, form labels, error/success messages | website skill + brevity rule |
| `casual` | internal chat-style Hebrew | none |
| `auto` (default) | server picks from the prompt | — |

## Key resolution order

The server looks for the OpenAI key in this order:
1. `OPENAI_API_KEY` environment variable
2. `.env` file next to `server.mjs`
3. macOS Keychain (service `openai-api-key`, current user) — Mac only

## Security notes

- **Never share API keys.** Each person installs their own.
- `.env` and `node_modules/` are gitignored — they never get committed.
- Default model: `gpt-5.5`. Override per-call (`model` arg) or globally (`HEBREW_GPT_MODEL`).

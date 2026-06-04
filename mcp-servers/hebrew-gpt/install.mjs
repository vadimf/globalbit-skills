#!/usr/bin/env node
/**
 * Cross-platform installer for the hebrew-gpt MCP server + Globalbit Hebrew skills.
 *
 * Usage:  node install.mjs
 *
 * What it does:
 *   1. Copies the Globalbit Hebrew skills into ~/.claude/skills/
 *   2. Installs the MCP server's npm dependencies
 *   3. Stores your OpenAI API key (macOS Keychain, or a local .env elsewhere)
 *   4. Registers the MCP server with Claude Code (user scope)
 *   5. Optionally adds a global CLAUDE.md rule to route Hebrew through the tool
 */
import { execFileSync, spawnSync } from "node:child_process";
import {
  existsSync, mkdirSync, cpSync, writeFileSync, readFileSync, appendFileSync,
} from "node:fs";
import { homedir, userInfo, platform } from "node:os";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createInterface } from "node:readline/promises";
import { stdin, stdout } from "node:process";

const HERE = dirname(fileURLToPath(import.meta.url));      // .../mcp-servers/hebrew-gpt
const REPO_ROOT = resolve(HERE, "..", "..");               // repo root (skills live here)
const HOME = homedir();
const SKILLS_DST = join(HOME, ".claude", "skills");
const IS_MAC = platform() === "darwin";

const SKILLS = ["globalbit-hebrew", "globalbit-hebrew-website-copy"];

const rl = createInterface({ input: stdin, output: stdout });
const ask = (q) => rl.question(q);
const log = (m) => console.log(m);
const ok = (m) => console.log(`  ✓ ${m}`);

async function main() {
  log("\n=== Globalbit hebrew-gpt installer ===\n");

  // 1. Copy skills
  log("1. Installing Hebrew skills into ~/.claude/skills/");
  mkdirSync(SKILLS_DST, { recursive: true });
  for (const s of SKILLS) {
    const src = join(REPO_ROOT, s);
    if (!existsSync(src)) { log(`  ! missing in repo: ${s} (skipped)`); continue; }
    cpSync(src, join(SKILLS_DST, s), { recursive: true });
    ok(s);
  }

  // 2. npm install
  log("\n2. Installing MCP server dependencies (npm install)");
  const npm = spawnSync(IS_MAC || platform() !== "win32" ? "npm" : "npm.cmd",
    ["install", "--omit=dev", "--silent"], { cwd: HERE, stdio: "inherit", shell: true });
  if (npm.status !== 0) { log("  ! npm install failed. Is Node.js installed?"); process.exit(1); }
  ok("dependencies installed");

  // 3. API key
  log("\n3. OpenAI API key");
  log("   Each person uses their OWN key. Get one at https://platform.openai.com/api-keys");
  const key = (await ask("   Paste your OpenAI API key (or leave blank to skip): ")).trim();
  if (key) {
    if (IS_MAC) {
      execFileSync("security", [
        "add-generic-password", "-a", userInfo().username,
        "-s", "openai-api-key", "-w", key, "-U",
      ]);
      ok("stored in macOS Keychain (service: openai-api-key)");
    } else {
      writeFileSync(join(HERE, ".env"), `OPENAI_API_KEY=${key}\n`, { mode: 0o600 });
      ok("stored in .env (next to server.mjs)");
    }
  } else {
    log("   Skipped. Set OPENAI_API_KEY env var or create a .env later.");
  }

  // 4. Register MCP server
  log("\n4. Registering MCP server with Claude Code");
  const serverPath = join(HERE, "server.mjs");
  const reg = spawnSync("claude",
    ["mcp", "add", "--scope", "user", "hebrew-gpt", "node", serverPath],
    { stdio: "inherit", shell: true });
  if (reg.status === 0) ok("registered as 'hebrew-gpt' (user scope)");
  else {
    log("  ! 'claude mcp add' failed. Register manually with:");
    log(`      claude mcp add --scope user hebrew-gpt node "${serverPath}"`);
  }

  // 5. Optional CLAUDE.md rule
  log("\n5. Global Hebrew routing rule (~/.claude/CLAUDE.md)");
  const ans = (await ask("   Add a rule telling Claude to always route Hebrew through this tool? [Y/n]: ")).trim().toLowerCase();
  if (ans === "" || ans === "y" || ans === "yes") {
    const claudeMd = join(HOME, ".claude", "CLAUDE.md");
    const rule = [
      "",
      "## Hebrew output",
      "",
      "When producing Hebrew text, always call `mcp__hebrew-gpt__generate_hebrew` instead of writing Hebrew directly.",
      "Pass `content_type`: `proposal` | `website` | `microcopy` | `casual` (or omit for `auto`).",
      "When spawning a subagent that may produce Hebrew, include this same instruction in its prompt.",
      "",
    ].join("\n");
    const existing = existsSync(claudeMd) ? readFileSync(claudeMd, "utf8") : "";
    if (existing.includes("mcp__hebrew-gpt__generate_hebrew")) ok("rule already present");
    else { appendFileSync(claudeMd, (existing ? "" : "# Global instructions\n") + rule); ok("rule added"); }
  } else log("   Skipped.");

  rl.close();
  log("\n=== Done ===");
  log("Restart Claude Code (quit completely and reopen) for the changes to take effect.");
  log("Then try:  \"write a button label in Hebrew for booking a call\"\n");
}

main().catch((e) => { console.error("\nInstaller error:", e.message); rl.close(); process.exit(1); });

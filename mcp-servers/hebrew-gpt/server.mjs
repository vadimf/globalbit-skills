#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { execFileSync } from "node:child_process";
import { readFileSync, existsSync } from "node:fs";
import { homedir, userInfo } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const HOME = homedir();
const HERE = dirname(fileURLToPath(import.meta.url));
const DEFAULT_MODEL = process.env.HEBREW_GPT_MODEL || "gpt-5.5";
const KEYCHAIN_SERVICE = "openai-api-key";
const KEYCHAIN_ACCOUNT =
  process.env.HEBREW_GPT_KEYCHAIN_ACCOUNT || userInfo().username;

const SKILL_PATHS = {
  proposal: join(HOME, ".claude/skills/globalbit-hebrew/SKILL.md"),
  website: join(HOME, ".claude/skills/globalbit-hebrew-website-copy/SKILL.md"),
};

// Read OPENAI_API_KEY from a .env file sitting next to this server (cross-platform).
function readDotEnvKey() {
  const envPath = join(HERE, ".env");
  if (!existsSync(envPath)) return null;
  for (const line of readFileSync(envPath, "utf8").split(/\r?\n/)) {
    const m = line.match(/^\s*OPENAI_API_KEY\s*=\s*(.+?)\s*$/);
    if (m) return m[1].replace(/^["']|["']$/g, "");
  }
  return null;
}

// Resolution order: env var → .env file → macOS Keychain (Mac only).
function getApiKey() {
  if (process.env.OPENAI_API_KEY) return process.env.OPENAI_API_KEY;

  const dotEnvKey = readDotEnvKey();
  if (dotEnvKey) return dotEnvKey;

  if (process.platform === "darwin") {
    try {
      return execFileSync(
        "security",
        ["find-generic-password", "-a", KEYCHAIN_ACCOUNT, "-s", KEYCHAIN_SERVICE, "-w"],
        { encoding: "utf8" },
      ).trim();
    } catch {
      /* fall through to error */
    }
  }

  throw new Error(
    `No OpenAI API key found. Provide one of:\n` +
      `  1. OPENAI_API_KEY environment variable, or\n` +
      `  2. a .env file next to server.mjs containing OPENAI_API_KEY=sk-..., or\n` +
      `  3. (macOS only) Keychain entry: security add-generic-password -a ${KEYCHAIN_ACCOUNT} -s ${KEYCHAIN_SERVICE} -w <key> -U`,
  );
}

function loadSkill(name) {
  const path = SKILL_PATHS[name];
  if (!path || !existsSync(path)) {
    throw new Error(`Skill file not found for "${name}" at ${path}`);
  }
  return readFileSync(path, "utf8").replace(/^---\n[\s\S]*?\n---\n/, "").trim();
}

const MICROCOPY_OVERRIDE = `
=== MICROCOPY MODE — STRICT OVERRIDE ===
You are generating a SINGLE micro-element: a button label, form field label, error message, success message, empty state, menu item, or similar UI string.
- Output ONLY the requested element. No surrounding sentence, no introduction, no explanation.
- Length: typically 2–7 words for buttons/labels; one short sentence for error/success/empty.
- Match the requested register (premium, precise, conversion-oriented per the website style guide above).
- Do not invent surrounding context. If multiple options were requested (e.g., "give me 3 button options"), return them as a bare list, one per line.
`;

function detectStyle(prompt) {
  const p = prompt.toLowerCase();
  const any = (rs) => rs.some((r) => r.test(p) || r.test(prompt));

  const proposalSignals = [
    /\bproposal\b/, /\bprd\b/, /\bsow\b/, /\bscope of work\b/, /\bexecutive summary\b/,
    /\barchitecture (document|doc)\b/, /\brisk register\b/, /\bcommercial terms\b/,
    /\bstatement of work\b/, /\bclarifying questions?\b/,
    /הצעה/, /הצעת מחיר/, /תקציר מנהלים/, /היקף עבודה/, /מסמך ארכיטקטורה/, /טבלת סיכונים/,
    /מסמך אפיון/, /שאלות הבהרה/,
  ];
  if (any(proposalSignals)) return "proposal";

  const websiteSignals = [
    /\bhero (section|block|copy|area)?\b/, /\blanding page\b/, /\babout (page|section)\b/,
    /\bservices? page\b/, /\bpricing page\b/, /\bnav(igation)? menu\b/, /\bfooter\b/,
    /\btestimonial/, /\bcase stud(y|ies) (card|section)\b/, /\bsite copy\b/, /\bwebsite copy\b/,
    /\bfeatures section\b/,
    /דף נחיתה/, /דף שירותים/, /דף אודות/, /סקשן Hero/i, /קופי לאתר/, /עמוד שירותים/,
    /עמוד הבית/,
  ];
  if (any(websiteSignals)) return "website";

  const isShort = prompt.length < 220;
  const microSignals = [
    /\bbutton (label|text|copy)\b/,
    /\b(write|give me|need|suggest) (a|the|one|3|three|5|five) (button|cta|label|tooltip|error|placeholder|empty state)\b/,
    /\berror message\b/, /\btooltip\b/, /\bempty state\b/, /\bplaceholder text\b/,
    /\bcta (label|text|button)\b/, /\bmenu item\b/, /\bform (label|field) label\b/,
    /כפתור (ל|של|עבור|אחד|בודד)/, /תווית (טופס|שדה|כפתור)/, /הודעת שגיאה/, /הודעת הצלחה/,
    /placeholder/, /microcopy/, /מיקרוקופי/, /מצב ריק/,
  ];
  if (isShort && any(microSignals)) return "microcopy";

  return "proposal";
}

function buildSystemPrompt(style) {
  const HEAD = `You are a senior Hebrew copywriter for Globalbit, an Israeli software consultancy. ` +
    `Follow the style guide below EXACTLY. Output only the Hebrew text — no preamble, no explanation, no English commentary, no markdown headings unless explicitly requested.\n\n`;

  switch (style) {
    case "proposal":
      return HEAD +
        `=== GLOBALBIT HEBREW STYLE GUIDE (proposals / formal documents) ===\n` +
        loadSkill("proposal");

    case "website":
      return HEAD +
        `=== GLOBALBIT HEBREW WEBSITE COPY GUIDE ===\n` +
        loadSkill("website");

    case "microcopy":
      return HEAD +
        `=== GLOBALBIT HEBREW WEBSITE COPY GUIDE ===\n` +
        loadSkill("website") +
        `\n\n${MICROCOPY_OVERRIDE}`;

    case "casual":
      return `You are a native Hebrew speaker writing casual, natural Hebrew — the way a smart Israeli would speak in a chat. ` +
        `Avoid AI-isms ("אז...", "בהחלט", "חשוב לזכור ש..."). No stiffness. Output only Hebrew.`;

    default:
      throw new Error(`Unknown style: ${style}`);
  }
}

async function callOpenAI({ systemPrompt, userPrompt, model, maxTokens }) {
  const key = getApiKey();
  const res = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${key}`,
    },
    body: JSON.stringify({
      model,
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt },
      ],
      ...(maxTokens ? { max_completion_tokens: maxTokens } : {}),
    }),
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`OpenAI API ${res.status}: ${body}`);
  }
  const json = await res.json();
  const text = json.choices?.[0]?.message?.content;
  if (!text) throw new Error(`No content in OpenAI response: ${JSON.stringify(json)}`);
  return { text, usage: json.usage, model: json.model };
}

const server = new Server(
  { name: "hebrew-gpt", version: "2.0.0" },
  { capabilities: { tools: {} } },
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "generate_hebrew",
      description:
        "Generate native-quality Hebrew via OpenAI GPT, using Globalbit's curated style guides. " +
        "USE THIS TOOL whenever you need to output Hebrew text — do not write Hebrew directly. " +
        "Pick `content_type` to match the artifact:\n" +
        "  - `proposal`: formal documents — proposals, PRDs, SOWs, architecture docs, executive summaries, formal client emails. Uses the long-form Globalbit register with em-dashes and two-beat sentences.\n" +
        "  - `website`: site pages — Hero sections, services pages, About, case study cards, longer marketing copy. Premium conversion-oriented register, no em-dash.\n" +
        "  - `microcopy`: SHORT UI elements — single button label, single form field label, single error/success message, empty state, menu item. Returns just the element, no surrounding text.\n" +
        "  - `casual`: chat-style Hebrew with no formal style guide. For internal notes, chat replies.\n" +
        "  - `auto` (default): the server picks based on keywords in `prompt`. Use when unsure.",
      inputSchema: {
        type: "object",
        properties: {
          prompt: {
            type: "string",
            description:
              "What to write. English brief, Hebrew draft to polish, or source text to translate. Be specific about audience, length, and purpose.",
          },
          content_type: {
            type: "string",
            enum: ["proposal", "website", "microcopy", "casual", "auto"],
            description:
              "Which style guide to apply. See tool description for when to use each. Default: auto.",
            default: "auto",
          },
          context: {
            type: "string",
            description:
              "Optional surrounding context — the rest of the page/document, the prior paragraph, the artifact's purpose. Helps the model match tone and avoid repetition.",
          },
          max_tokens: {
            type: "number",
            description:
              "Optional cap on output length (tokens). For microcopy, ~100 is plenty. Omit for proposal/website.",
          },
          model: {
            type: "string",
            description: `OpenAI model. Default: ${DEFAULT_MODEL}. Examples: gpt-5.5, gpt-5.5-pro, gpt-5.4.`,
          },
        },
        required: ["prompt"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  if (req.params.name !== "generate_hebrew") {
    throw new Error(`Unknown tool: ${req.params.name}`);
  }
  const {
    prompt,
    content_type = "auto",
    context,
    max_tokens,
    model = DEFAULT_MODEL,
  } = req.params.arguments ?? {};

  if (!prompt || typeof prompt !== "string") {
    throw new Error("`prompt` is required and must be a string");
  }

  const resolvedStyle = content_type === "auto" ? detectStyle(prompt) : content_type;

  let systemPrompt;
  try {
    systemPrompt = buildSystemPrompt(resolvedStyle);
  } catch (e) {
    return { isError: true, content: [{ type: "text", text: `Error: ${e.message}` }] };
  }

  const userPrompt = context
    ? `Context (for tone matching, do not repeat verbatim):\n${context}\n\n---\n\nTask:\n${prompt}`
    : prompt;

  try {
    const { text, usage, model: usedModel } = await callOpenAI({
      systemPrompt,
      userPrompt,
      model,
      maxTokens: max_tokens,
    });
    const autoNote = content_type === "auto" ? `, auto-detected as ${resolvedStyle}` : "";
    return {
      content: [
        { type: "text", text },
        {
          type: "text",
          text: `\n---\n_${usedModel} · ${resolvedStyle}${autoNote} · ${usage?.total_tokens ?? "?"} tokens_`,
        },
      ],
    };
  } catch (e) {
    return { isError: true, content: [{ type: "text", text: `Error: ${e.message}` }] };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);

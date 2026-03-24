#!/usr/bin/env node
/**
 * Stitch CLI — REST API wrapper for Google Stitch AI design tool.
 * Any agent can call this via run_command. No MCP server required.
 *
 * Usage:
 *   node stitch-cli.mjs <command> [args...]
 *
 * Env:
 *   STITCH_API_KEY — Google API key with Stitch access (required)
 *
 * Commands:
 *   create-project <title>
 *   list-projects
 *   generate <projectId> <promptFile> [--device DESKTOP|MOBILE|TABLET]
 *   edit <projectId> <screenId> <promptFile>
 *   get-screen <projectId> <screenId>
 *   download <projectId> <screenId> <outputDir>
 *   list-screens <projectId>
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { basename, join, resolve, extname } from 'path';

const API_KEY = process.env.STITCH_API_KEY;
const BASE_URL = 'https://stitch.googleapis.com/mcp';

// ── Helpers ──────────────────────────────────────────────────────────

function die(msg) {
  console.error(`Error: ${msg}`);
  process.exit(1);
}

let rpcId = 0;

async function callStitch(toolName, args = {}) {
  if (!API_KEY) die('STITCH_API_KEY env var is required');

  const body = {
    jsonrpc: '2.0',
    id: ++rpcId,
    method: 'tools/call',
    params: { name: toolName, arguments: args },
  };

  const res = await fetch(BASE_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Goog-Api-Key': API_KEY,
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    die(`HTTP ${res.status}: ${text.slice(0, 500)}`);
  }

  const data = await res.json();
  if (data.error) {
    die(`Stitch RPC Error: ${JSON.stringify(data.error)}`);
  }
  return data.result;
}

/** Extract the first JSON text content from a Stitch MCP response. */
function extractContent(result) {
  const content = result?.content;
  if (!Array.isArray(content)) return result;
  for (const c of content) {
    if (c.type === 'text') {
      try { return JSON.parse(c.text); } catch { return c.text; }
    }
  }
  return result;
}

/** Read a prompt from file — supports .txt, .md, .json */
function readPrompt(filePath) {
  const resolved = resolve(filePath);
  if (!existsSync(resolved)) die(`Prompt file not found: ${resolved}`);

  const ext = extname(resolved).toLowerCase();
  const raw = readFileSync(resolved, 'utf8');

  if (ext === '.json') {
    const parsed = JSON.parse(raw);
    return typeof parsed === 'string' ? parsed : parsed.prompt || JSON.stringify(parsed);
  }
  return raw.trim();
}

// ── Commands ─────────────────────────────────────────────────────────

async function createProject(title) {
  console.error(`Creating project: ${title}`);
  const result = await callStitch('create_project', { title });
  const data = extractContent(result);
  console.log(JSON.stringify(data, null, 2));
  return data;
}

async function listProjects() {
  const result = await callStitch('list_projects', {});
  const data = extractContent(result);
  console.log(JSON.stringify(data, null, 2));
  return data;
}

async function generate(projectId, promptFile, device = 'DESKTOP') {
  const prompt = readPrompt(promptFile);
  console.error(`Generating screen for project ${projectId} (${device})...`);
  console.error(`Prompt: ${prompt.slice(0, 120)}...`);

  const result = await callStitch('generate_screen_from_text', {
    projectId,
    prompt,
    deviceType: device,
  });

  const data = extractContent(result);

  // Extract key information for agent consumption
  const output = {
    projectId: data?.projectId || projectId,
    sessionId: data?.sessionId,
    screens: [],
    designSystem: null,
    suggestions: [],
    text: '',
  };

  if (data?.outputComponents) {
    for (const comp of data.outputComponents) {
      if (comp.designSystem) {
        output.designSystem = {
          name: comp.designSystem?.designSystem?.displayName,
          font: comp.designSystem?.designSystem?.theme?.headlineFont,
          bodyFont: comp.designSystem?.designSystem?.theme?.bodyFont,
          accent: comp.designSystem?.designSystem?.theme?.customColor,
          designMd: comp.designSystem?.designSystem?.theme?.designMd,
        };
      }
      if (comp.design?.screens) {
        for (const s of comp.design.screens) {
          const idMatch = s.name?.match(/screens\/([a-f0-9]+)$/);
          output.screens.push({
            name: s.name,
            screenId: idMatch?.[1],
            title: s.title,
          });
        }
      }
      if (comp.text) output.text += comp.text + '\n';
      if (comp.suggestion) output.suggestions.push(comp.suggestion);
    }
  }

  console.log(JSON.stringify(output, null, 2));
  return output;
}

async function edit(projectId, screenId, promptFile) {
  const prompt = readPrompt(promptFile);
  console.error(`Editing screen ${screenId} in project ${projectId}...`);
  console.error(`Prompt: ${prompt.slice(0, 120)}...`);

  const result = await callStitch('edit_screens', {
    projectId,
    selectedScreenIds: [screenId],
    prompt,
  });

  const data = extractContent(result);
  console.log(JSON.stringify(data, null, 2));
  return data;
}

async function getScreen(projectId, screenId) {
  const result = await callStitch('get_screen', {
    projectId,
    screenId,
    name: `projects/${projectId}/screens/${screenId}`,
  });

  const data = extractContent(result);
  console.log(JSON.stringify(data, null, 2));
  return data;
}

async function download(projectId, screenId, outputDir) {
  const resolvedDir = resolve(outputDir);
  mkdirSync(resolvedDir, { recursive: true });

  console.error(`Fetching screen ${screenId}...`);
  const result = await callStitch('get_screen', {
    projectId,
    screenId,
    name: `projects/${projectId}/screens/${screenId}`,
  });
  const screen = extractContent(result);

  const slug = screen?.title?.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-+$/, '') || screenId;

  // Download HTML
  if (screen?.htmlCode?.downloadUrl) {
    console.error(`Downloading HTML...`);
    const htmlRes = await fetch(screen.htmlCode.downloadUrl);
    const html = await htmlRes.text();
    const htmlPath = join(resolvedDir, `${slug}.html`);
    writeFileSync(htmlPath, html);
    console.error(`HTML saved: ${htmlPath} (${html.length} chars)`);
  }

  // Download screenshot
  if (screen?.screenshot?.downloadUrl) {
    console.error(`Downloading screenshot...`);
    const ssRes = await fetch(screen.screenshot.downloadUrl);
    const ssBuf = Buffer.from(await ssRes.arrayBuffer());
    const ssPath = join(resolvedDir, `${slug}.png`);
    writeFileSync(ssPath, ssBuf);
    console.error(`Screenshot saved: ${ssPath} (${ssBuf.length} bytes)`);
  }

  // Save metadata
  const meta = {
    screenId,
    projectId,
    title: screen?.title,
    width: screen?.width,
    height: screen?.height,
    deviceType: screen?.deviceType,
    htmlFile: screen?.htmlCode?.downloadUrl ? `${slug}.html` : null,
    screenshotFile: screen?.screenshot?.downloadUrl ? `${slug}.png` : null,
  };
  writeFileSync(join(resolvedDir, `${slug}.meta.json`), JSON.stringify(meta, null, 2));
  console.log(JSON.stringify(meta, null, 2));
  return meta;
}

async function listScreens(projectId) {
  const result = await callStitch('list_screens', { projectId });
  const data = extractContent(result);
  console.log(JSON.stringify(data, null, 2));
  return data;
}

// ── Main ─────────────────────────────────────────────────────────────

const [, , command, ...args] = process.argv;

const HELP = `
Stitch CLI — REST API wrapper for Google Stitch AI design tool.

Usage:
  node stitch-cli.mjs <command> [args...]

Commands:
  create-project <title>                      Create a new Stitch project
  list-projects                               List all projects
  generate <projectId> <promptFile> [--device DESKTOP|MOBILE]
                                              Generate a screen from a prompt file
  edit <projectId> <screenId> <promptFile>    Edit an existing screen
  get-screen <projectId> <screenId>           Get screen metadata
  download <projectId> <screenId> <outputDir> Download HTML + screenshot
  list-screens <projectId>                    List all screens in a project

Environment:
  STITCH_API_KEY  Google API key with Stitch access (required)

Prompt files:
  Supports .txt, .md, and .json formats.
  For .json, include a "prompt" key or the entire file is used as prompt text.
`.trim();

if (!command || command === '--help' || command === '-h') {
  console.log(HELP);
  process.exit(0);
}

try {
  switch (command) {
    case 'create-project':
      if (!args[0]) die('Usage: create-project <title>');
      await createProject(args[0]);
      break;
    case 'list-projects':
      await listProjects();
      break;
    case 'generate': {
      if (args.length < 2) die('Usage: generate <projectId> <promptFile> [--device DESKTOP|MOBILE]');
      const deviceIdx = args.indexOf('--device');
      const device = deviceIdx >= 0 ? args[deviceIdx + 1] : 'DESKTOP';
      await generate(args[0], args[1], device);
      break;
    }
    case 'edit':
      if (args.length < 3) die('Usage: edit <projectId> <screenId> <promptFile>');
      await edit(args[0], args[1], args[2]);
      break;
    case 'get-screen':
      if (args.length < 2) die('Usage: get-screen <projectId> <screenId>');
      await getScreen(args[0], args[1]);
      break;
    case 'download':
      if (args.length < 3) die('Usage: download <projectId> <screenId> <outputDir>');
      await download(args[0], args[1], args[2]);
      break;
    case 'list-screens':
      if (!args[0]) die('Usage: list-screens <projectId>');
      await listScreens(args[0]);
      break;
    default:
      die(`Unknown command: ${command}. Run with --help for usage.`);
  }
} catch (err) {
  die(err.message || err);
}

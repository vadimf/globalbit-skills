---
name: create-html-proposal
description: |
  Create, encrypt, and deploy a password-protected Globalbit client proposal at
  globalbit.co.il/portal/<client>/proposal. Uses a fixed gated portal architecture
  (encrypted HTML payload + encrypted PDF) so the deployed bundle never contains
  plaintext.

  Use when: "create a proposal for <client>", "new proposal for X", "add a section
  to the proposal", "update the proposal", "deploy the proposal",
  "password-protect this doc", "client proposal portal".
user-invocable: true
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# Globalbit Proposal Portal

Proposals are **encrypted single-client web pages** served at `/portal/<client>/proposal`.
The deployed bundle contains only AES-256-GCM ciphertext (HTML *and* PDF). The
client decrypts in-browser with a per-client passphrase.

> **House rule**: never tell the user to run the steps — do them.
> Always finish with build + deploy + Cloudflare purge.
> Never commit `portal-secrets.json`.

For deeper reading, see **`WRITING-GUIDE.md`** (how to write good proposals,
not walls of text), **`COMMON-MISTAKES.md`** (gotchas learned the hard way),
and **`COMPOSITION.md`** (how this skill fits with `create-proposal`,
`globalbit-document`, and the other proposal-adjacent skills).
Read those before writing your first proposal — they save hours.

---

## What's hardcoded, what's templated, what changes per proposal

| Layer | What | Where |
|---|---|---|
| **HARDCODED** — never edit per proposal | The gate component (decrypt, render, all CSS, JS enhancements). Build scripts. Firebase rules. Header/Footer hiding. GTM-on-portal disable. | `app/portal/klapton/proposal/proposal-gate.tsx` (canonical), `scripts/encrypt-proposal.mjs`, `scripts/render-and-encrypt-pdf.mjs`, `firebase.json`, `app/layout.tsx` |
| **TEMPLATED** — structure fixed, content varies | Section skeleton (cover → exec → … → next). About-Globalbit block. Hourly rates table. Generic terms. | `templates/proposal-skeleton.html`, `templates/about-globalbit.html` |
| **PER-PROPOSAL** — write fresh each time | Project title, reference, dates, exec summary, background, goals, solution components, scope, phases, team, timeline, risks, value, commercial estimate, next steps. | `content/<client>-proposal.html` |

**Do not edit the gate component or CSS per client.** When the design needs to
change, change it once in the klapton gate and it propagates to every proposal
(via copy/sync) and to every PDF (the render script reads the gate's CSS).

---

## Architecture in 30 seconds

```
content/<client>-proposal.html        ─┐
                                       ├─► encrypt-proposal.mjs        ─► app/portal/<client>/proposal/payload.json     (ciphertext, bundled)
portal-secrets.json (git-ignored)     ─┘
                                       │
                                       └─► render-and-encrypt-pdf.mjs  ─► public/portal/<client>/proposal/payload.pdf.json (ciphertext, fetched on demand)

browser:  user opens /portal/<client>/proposal
          → enters password
          → JS decrypts payload.json with AES-GCM (PBKDF2-SHA256, 600k iters)
          → renders the HTML; runs enhancements (TOC, Gantt, exec digest, glossary…)
          → "Download PDF" click → fetch payload.pdf.json → decrypt → Blob → download
```

Security: same passphrase decrypts both payloads. The plaintext content is in
the repo (so you can edit) but the app never imports it — only the encryptor
scripts read it. The deployed Next bundle contains only ciphertext.

---

## Create a NEW proposal

### 1. Write the content → `content/<client>-proposal.html`

Start from `templates/proposal-skeleton.html`. It is a raw HTML **fragment**
(no `<html>/<head>/<body>` — the gate injects it). Required structure:

```
<div class="progress" id="gp-progress"></div>
<header class="cover"> … cover h1, meta, "Confidential" … </header>
<div class="gp-main"><div class="wrap"><div class="layout">
  <aside class="toc" id="gp-toc"> … TOC + Download PDF button … </aside>
  <div class="content">
    <section id="summary" class="wide"> … exec summary in dark .summary card … </section>
    <section id="background"> … </section>
    <section id="business-goals"> … </section>
    <section id="project-goals"> … </section>
    <section id="solution" class="wide"> … </section>
    <!-- paste templates/about-globalbit.html here -->
    <section id="scope"> … </section>
    <section id="phases"> … </section>
    <section id="team"> … </section>
    <section id="timeline"> … </section>
    <section id="risk" class="wide"> … </section>
    <section id="value" class="wide"> … </section>
    <section id="commercial"> … </section>
    <section id="terms"> … </section>
    <!-- optional --> <section id="appendix-architecture" class="wide appendix"> … </section>
    <section id="next"> … </section>     ← **last section, always**
  </div>
</div></div></div>
```

**Section order is fixed and matters.** The TOC `<ol>` must list sections in the
same order. Appendices use `class="appendix"` on the `<section>` — CSS suppresses
the auto-number and the JS folds the content (always expanded in the PDF).

Chapter eyebrows: `<div class="kicker">Label</div>` with **no number** (CSS
counter auto-numbers). Do not hardcode "01", "02", etc.

For how to write each section so it doesn't read as a wall of text, see
**`WRITING-GUIDE.md`**.

### 2. Create the route — copy klapton's verbatim

```bash
mkdir -p app/portal/<client>/proposal
cp app/portal/klapton/proposal/page.tsx          app/portal/<client>/proposal/page.tsx
cp app/portal/klapton/proposal/proposal-gate.tsx app/portal/<client>/proposal/proposal-gate.tsx
```

In the new `page.tsx`, change only:
- `title` and `description` in metadata
- `storageKey="gbp:<client>"`
- `client="<client>"` (slug used to fetch the PDF payload)

Leave `proposal-gate.tsx` byte-identical to klapton's. It's the same component
for every proposal — the only per-client thing the gate sees is the props.

### 3. Set the passphrase in `portal-secrets.json`

```json
{ "klapton": "...", "<client>": "<STRONG-PASSPHRASE>" }
```

Generate strong:

```bash
echo "$(tr '[:lower:]' '[:upper:]' <<< ${client:0:1})${client:1}-$(openssl rand -hex 8)-$(openssl rand -hex 8)-GB$(date +%y)"
# example: Klapton-4a641d8a-fcd7c585-GB26
```

The encryptor refuses passwords < 8 chars. Don't weaken them.

### 4. Encrypt + render PDF + verify

```bash
node scripts/encrypt-proposal.mjs <client>          # → app/portal/<client>/proposal/payload.json
node scripts/render-and-encrypt-pdf.mjs <client>    # → public/portal/<client>/proposal/payload.pdf.json
```

The PDF render takes ~10s (puppeteer launches headless Chrome). Confirm it ran:
`ls public/portal/<client>/proposal/payload.pdf.json` and check the byte size
matches "~700 KB pdf → ~950 KB b64" range for a normal-length proposal.

### 5. Local smoke test

```bash
npm run dev
# open http://localhost:3000/portal/<client>/proposal
# enter the passphrase, scroll, click Download PDF
```

PDF download should be **<1 second** click-to-file (it's pre-rendered ciphertext,
not a Safari `window.print()`).

### 6. Publish (see "Publish" below)

### 7. Hand off

Give the URL and password to the user, with explicit guidance to send them via
**separate channels** (URL by email, password by phone/WhatsApp/Signal). Never
put them in the same message.

---

## Update an EXISTING proposal

Edit `content/<client>-proposal.html` only — never the gate, never the CSS per
client. Then republish (Publish below). The session cache (`sessionStorage`
keyed by IV) auto-invalidates because the IV changes on every encryption —
returning viewers re-enter the password once and see fresh content (never stale).

---

## Publish (encrypt + render + build + deploy + purge)

Run from the repo root. `npm run build` triggers `prebuild`, which **re-encrypts
HTML and re-renders the PDF for every client** in `portal-secrets.json`.

```bash
# 1. Build (static export to out/). Triggers prebuild: encrypt + render-pdf.
npm run build

# 2. Verify the exported page is gated, leak-free, and PDF payload is in place.
f=out/portal/<client>/proposal.html
echo "gate:$(grep -c 'Protected document' $f)  leak:$(grep -cE '<unique secret marker from your content>' $f)"
ls -la out/portal/<client>/proposal/payload.pdf.json    # should exist, ~1 MB

# 3. Deploy hosting.
firebase deploy --only hosting

# 4. Purge Cloudflare edge cache. Creds live in the PARENT project .env.local.
set -a && source "/Users/vadim/Documents/Code/Globalbit Website/Globalbit Surf/.env.local" && set +a
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/purge_cache" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" -H "Content-Type: application/json" \
  --data '{"purge_everything":true}' \
  | python3 -c "import sys,json;r=json.load(sys.stdin);print('CF purged' if r.get('success') else 'CF FAILED '+str(r.get('errors')))"

# 5. Confirm production.
curl -s -D - -o /tmp/p.html "https://globalbit.co.il/portal/<client>/proposal" \
  | grep -i -E '^HTTP/|x-robots-tag'
echo "gate:$(grep -c 'Protected document' /tmp/p.html)  ciphertext:$(grep -c 'AES-256-GCM' /tmp/p.html)"
curl -sI "https://globalbit.co.il/portal/<client>/proposal/payload.pdf.json" | head -3
```

Expect: `HTTP/2 200`, `x-robots-tag: noindex, …`, `gate:1`, `ciphertext:1`,
PDF payload returns `200 OK`.

Deploy of confidential content is a production push — needs explicit user
approval. If the safety classifier blocks `firebase deploy`, ask the user.

---

## The PDF pipeline — how it works (so you don't re-invent it)

- **Build-time, headless Chrome**: `scripts/render-and-encrypt-pdf.mjs` reads the
  proposal HTML, **reads the exact same CSS** out of `proposal-gate.tsx` (single
  source of truth), wraps in `<div class="gb-proposal">` + a few print overrides
  (single-column layout, hide TOC/progress/mode bar, force appendix open, full-color
  logos), writes to a temp file in `/public`, navigates puppeteer to that file
  via `file://`, and saves an A4 PDF.
- **Why file://, not setContent()**: Chrome blocks `file://` resource loads from
  an `about:blank` origin. Using `goto(file://…)` makes the page's origin file://,
  which trusts other file:// resources. **Without this fix, every `<img src="/…">`
  silently fails.**
- **Same encryption as HTML**: AES-256-GCM, PBKDF2-SHA256 @ 600k iters, random
  salt + IV, same per-client passphrase.
- **Output**: `public/portal/<client>/proposal/payload.pdf.json` — served as a
  static asset (not bundled into JS, which would add ~1 MB to every page load).
- **Click handler**: fetches the ciphertext, decrypts with Web Crypto, creates a
  Blob, triggers a real `.pdf` download. **<1 second** click-to-file.
- **Do not use `window.print()`**: Safari's print on a 25-page complex document
  takes 40+ seconds and looks worse than the pre-rendered PDF anyway.

Appendices: always fully expanded in the PDF (override the `[data-appendix-hide]`
rule). Confirm with `pdftotext` or `pypdf` after rendering if you're unsure.

---

## Security model (don't weaken)

- `portal-secrets.json` is git-ignored. **Never commit it.** Only ciphertext
  payloads ever land in git.
- `content/<client>-proposal.html` is plaintext but **must never be imported by
  any app file**. The encryptor scripts are the only readers.
- Repo is private (`gh repo view`).
- One strong passphrase per client. `openssl rand -hex` for entropy.
- Cache: 5 attempts → escalating throttle (already wired in the gate).
- noindex: enforced by **both** the page `metadata.robots` and the Firebase
  `X-Robots-Tag` header on `/portal/**`.
- No remote revocation. To revoke: rotate the passphrase in
  `portal-secrets.json` and republish — the next encryption uses a new salt+IV
  and old sessionStorage caches are invalidated.

---

## Optional: client-opened email/Telegram beacon

A `trackProposalOpen` Cloud Function (CRM project) sends an email + Telegram alert
when a client unlocks the proposal. Wired via `app/layout.tsx` + a beacon endpoint
`/t/proposal-open` (Firebase rewrite). If a new client needs this, no code change
— the gate already fires the beacon on successful unlock for any `client` slug.

---

## Canonical example

`content/klapton-proposal.html` + `app/portal/klapton/proposal/*` +
`public/portal/klapton/proposal/payload.pdf.json` is the reference implementation.
Every new client should mirror this exactly.

If something is unclear or broken, read **`COMMON-MISTAKES.md`** before
re-architecting anything.

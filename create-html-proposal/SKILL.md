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
> Never commit the secrets file.

Companion docs in the same folder:
- **`WRITING-GUIDE.md`** — how to write proposals that don't read as walls of text.
- **`COMMON-MISTAKES.md`** — gotchas learned the hard way. Read before debugging.

---

## What's hardcoded, what's templated, what changes per proposal

| Layer | What | Notes |
|---|---|---|
| **HARDCODED** | The gate component (decrypt, render, CSS, all JS enhancements). Build scripts. Firebase rules. GTM-disable + chrome-hiding on `/portal/*`. | Reused byte-identical across every client. The PDF render script reads the gate's CSS string at build time → single source of truth for the design. |
| **TEMPLATED** | Section skeleton. About-Globalbit block. Hourly rates. Generic terms. | `templates/proposal-skeleton.html`, `templates/about-globalbit.html`. Only token-replacements per client. |
| **PER-PROPOSAL** | Project title, reference, dates, exec summary, background, goals, solution components, scope, phases, team, timeline, risks, value, commercial estimate, next steps. | `content/<client>-proposal.html` |

**Do not edit the gate component or CSS per client.** When the design needs to
change, change it once in the canonical (klapton) gate and it propagates.

---

## Architecture in 30 seconds

```
content/<client>-proposal.html        ─┐
                                       ├─► encrypt-proposal.mjs        ─► payload.json     (ciphertext, bundled)
portal-secrets.json (git-ignored)      │
                                       └─► render-and-encrypt-pdf.mjs  ─► payload.pdf.json (ciphertext, fetched on demand)

browser:  user opens /portal/<client>/proposal
          → enters password
          → JS decrypts payload.json with AES-GCM (PBKDF2-SHA256, 600k iters)
          → renders the HTML; runs enhancements (TOC, Gantt, glossary, …)
          → "Download PDF" click → fetch payload.pdf.json → decrypt → Blob → download
```

Same passphrase decrypts both payloads. The plaintext content is in the repo
(so you can edit) but the app never imports it — only the encryptor scripts
read it. The deployed Next bundle contains only ciphertext.

---

## Create a NEW proposal

### 1. Write the content → `content/<client>-proposal.html`

Start from `templates/proposal-skeleton.html`. It is a raw HTML **fragment**
(no `<html>/<head>/<body>` — the gate injects it).

**Section order is fixed** (see template). The TOC `<ol>` must list sections
in the same order. Appendices use `class="appendix"` on the `<section>`.

Chapter eyebrows use `<div class="kicker">Label</div>` with **no number** (CSS
auto-numbers via counter). Do not hardcode "01", "02".

For how to write each section so it doesn't read as a wall of text, see
**`WRITING-GUIDE.md`**.

### 2. Create the route — copy the canonical client's files verbatim

```bash
mkdir -p app/portal/<client>/proposal
cp app/portal/<canonical>/proposal/page.tsx          app/portal/<client>/proposal/page.tsx
cp app/portal/<canonical>/proposal/proposal-gate.tsx app/portal/<client>/proposal/proposal-gate.tsx
```

In the new `page.tsx`, change only:
- `title` / `description` in metadata
- `storageKey="gbp:<client>"`
- `client="<client>"` (slug used to fetch the PDF payload)

`proposal-gate.tsx` stays byte-identical to the canonical version.

### 3. Set the passphrase in `portal-secrets.json` (git-ignored)

Generate strong (24+ chars of entropy):

```bash
echo "$(tr '[:lower:]' '[:upper:]' <<< ${client:0:1})${client:1}-$(openssl rand -hex 8)-$(openssl rand -hex 8)-GB$(date +%y)"
```

The encryptor refuses passwords < 8 chars. Don't weaken them.

### 4. Encrypt + render PDF + verify

```bash
node scripts/encrypt-proposal.mjs <client>          # → app/portal/<client>/proposal/payload.json
node scripts/render-and-encrypt-pdf.mjs <client>    # → public/portal/<client>/proposal/payload.pdf.json
```

The PDF render takes ~10s (puppeteer launches headless Chrome).

### 5. Local smoke test

```bash
npm run dev
# open http://localhost:3000/portal/<client>/proposal
# enter the passphrase, scroll, click Download PDF (<1s click-to-file)
```

### 6. Publish (build + deploy + purge)

```bash
npm run build              # prebuild re-encrypts + re-renders PDF for every client
firebase deploy --only hosting
# Then purge Cloudflare edge cache (CF_ZONE_ID + CF_API_TOKEN from .env.local)
```

Confirm production:
```bash
curl -s -D - -o /tmp/p.html "https://globalbit.co.il/portal/<client>/proposal" \
  | grep -i -E '^HTTP/|x-robots-tag'
```
Expect `HTTP/2 200`, `x-robots-tag: noindex, …`, ciphertext markers present.

### 7. Hand off

Give the URL and password to the user, with explicit guidance to send them via
**separate channels** (URL by email, password by phone/WhatsApp/Signal). Never
put them in the same message.

---

## Update an EXISTING proposal

Edit `content/<client>-proposal.html` only — never the gate, never the CSS per
client. Then republish. The session cache (`sessionStorage` keyed by IV)
auto-invalidates on every re-encryption.

---

## The PDF pipeline — how it works (so you don't re-invent it)

- **Build-time, headless Chrome**: the render script reads the proposal HTML,
  reads the exact same CSS out of the gate (single source of truth), wraps in
  `<div class="gb-proposal">` + a few print overrides, writes the doc to a temp
  file under `/public`, navigates puppeteer to that file via `file://`, and
  saves an A4 PDF.
- **Why file://, not setContent**: Chrome blocks `file://` resource loads from
  an `about:blank` origin. Using `goto(file://…)` makes the page's origin
  file://, which trusts other file:// resources. **Without this, every
  `<img src="/…">` silently fails.**
- **Same encryption as HTML**: AES-256-GCM, PBKDF2-SHA256 @ 600k iters, random
  salt + IV, same per-client passphrase.
- **Output**: encrypted PDF lives under `public/portal/<client>/proposal/payload.pdf.json` —
  served as a static asset (not bundled into JS).
- **Click handler**: fetches the ciphertext, decrypts with Web Crypto, creates
  a Blob, triggers a real `.pdf` download. <1 second click-to-file.
- **Do not use `window.print()`**: Safari's print on a 25-page complex
  document takes 40+ seconds and looks worse than the pre-rendered PDF.

Appendices are always fully expanded in the PDF (override the
`[data-appendix-hide]` rule).

---

## Security model (don't weaken)

- `portal-secrets.json` is git-ignored. **Never commit it.** Only ciphertext
  payloads ever land in git.
- `content/<client>-proposal.html` is plaintext but **must never be imported by
  any app file**. The encryptor scripts are the only readers.
- Repo is private.
- One strong passphrase per client.
- 5-attempt brute-force throttle is wired in the gate.
- noindex enforced by **both** the page metadata and the Firebase `X-Robots-Tag`
  header on `/portal/**`.
- No remote revocation. To revoke: rotate the passphrase and republish.

---

## Canonical example

The `klapton` proposal is the reference implementation. Every new client should
mirror it exactly: same directory structure, same `proposal-gate.tsx`, same
section order, same About-Globalbit block.

If something is unclear or broken, read **`COMMON-MISTAKES.md`** before
re-architecting anything.

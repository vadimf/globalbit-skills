---
name: create-html-proposal
description: |
  Create, encrypt, and deploy a password-protected Globalbit client proposal
  at globalbit.co.il/portal/<client>/proposal — using the static reusable
  parts (cover, About Globalbit, awards, gate, CSS) and the build/deploy/purge
  pipeline.

  Use when: "create a proposal", "new proposal for <client>", "add a section
  to the proposal", "update the proposal", "deploy the proposal",
  "password-protect this doc", "client proposal portal".
user-invocable: true
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# Globalbit Proposal Portal Skill

Proposals are **encrypted single-client web pages** served from the static
Next.js site at **`/portal/<client>/proposal`**. Plaintext never ships — the
deployed bundle only contains AES-256-GCM ciphertext; the client decrypts it
in-browser with a per-client password.

> RULE: never tell the user to run the steps — do them. Always finish by
> building, deploying, and purging Cloudflare. Never commit `portal-secrets.json`.

---

## Architecture (how it works)

| Piece | Path | Static? |
|---|---|---|
| Proposal content (plaintext, **never imported by the app**) | `content/<client>-proposal.html` | per-client |
| Per-client passwords (git-ignored) | `portal-secrets.json` | per-client |
| Encryptor (PBKDF2-SHA256 600k → AES-256-GCM) | `scripts/encrypt-proposal.mjs` | **static** |
| Encrypted payload (ciphertext only, safe to deploy) | `app/portal/<client>/proposal/payload.json` | generated |
| Route page (noindex metadata + gate) | `app/portal/<client>/proposal/page.tsx` | static template |
| Unlock gate + ALL proposal CSS + behaviors | `app/portal/<client>/proposal/proposal-gate.tsx` | **static** |
| Server `X-Robots-Tag` for `/portal/**` | `firebase.json` | already set |
| Reusable "About Globalbit" block | this skill → `templates/about-globalbit.html` | **static** |
| Body skeleton | this skill → `templates/proposal-skeleton.html` | static template |

Static, site-wide behavior already in place (do not re-implement):
- Real site `<Header/>`/`<Footer/>` come from the root layout automatically.
- `/portal/*` disables GTM/analytics (`app/layout.tsx`), and hides
  ScrollCTA / StickyBanner / MobileFooterMenu.
- `globals.css` uses `overflow-x: clip` so the sticky TOC works.
- The gate CSS is fully scoped under `.gb-proposal`; print isolation hides
  `body > header/footer` + TOC + progress and paginates cleanly.

---

## Create a NEW proposal

1. **Write the content** → `content/<client>-proposal.html`.
   - Start from `templates/proposal-skeleton.html`.
   - Paste `templates/about-globalbit.html` verbatim where `{{ABOUT_GLOBALBIT}}`
     is; replace its two tokens `{{DOMAIN_FIT}}` and `{{QUALITY_CONTEXT}}`.
   - It is a raw HTML **fragment** (no `<html>/<head>/<body>`).
   - Chapter eyebrows: `<div class="kicker">Label</div>` with **no number**
     (CSS auto-numbers). Appendices: add class `appendix` to the `<section>`
     and the number is suppressed.
   - Keep the cover, `#gp-progress`, `#gp-toc`, Download-PDF button, and the
     four closing `</div>`s exactly as in the skeleton.
   - No Mermaid / external CDNs (CSP blocks them and async render breaks PDF).
     Render diagrams as native HTML (see `arch-layer`, `flow`, `pipeline`,
     `ent-grid`, `stack` classes already in the gate CSS — see klapton example).

2. **Create the route** (copy klapton's, change the storage key):
   ```
   mkdir -p app/portal/<client>/proposal
   cp app/portal/klapton/proposal/page.tsx        app/portal/<client>/proposal/page.tsx
   cp app/portal/klapton/proposal/proposal-gate.tsx app/portal/<client>/proposal/proposal-gate.tsx
   ```
   In the new `page.tsx`: keep the `robots` metadata; set
   `storageKey="gbp:<client>"` and a fitting `title`/`metadata`.
   `proposal-gate.tsx` is reusable as-is (it holds the static CSS + crypto +
   progress/TOC/PDF + session cache logic).

3. **Set the password** in `portal-secrets.json` (git-ignored; create from
   `portal-secrets.example.json` if missing):
   ```json
   { "klapton": "...", "<client>": "<STRONG-PASSPHRASE>" }
   ```
   Generate strong: `echo "<Client>-$(openssl rand -hex 4)-$(openssl rand -hex 4)-GB$(date +%y)"`.
   The encryptor refuses passwords < 8 chars.

4. **Encrypt, build, deploy, purge** (see Publish below).

5. **Hand off**: give the user the URL and password to send to the client
   **via separate channels** (link by email, password by phone/WhatsApp).

---

## Update an EXISTING proposal

Edit `content/<client>-proposal.html` only (and gate CSS if adding a new
component). Then Publish. The session cache auto-invalidates because the
payload IV changes each encryption — returning viewers re-enter the password
once and see fresh content (never stale).

---

## Publish (encrypt → build → deploy → purge)

Run from the repo root. `npm run build` triggers the `prebuild` hook that
re-encrypts every client in `portal-secrets.json`.

```bash
# 1. (optional sanity) encrypt now + verify it decrypts with the password
node scripts/encrypt-proposal.mjs
node -e 'const p=require("./app/portal/<client>/proposal/payload.json"),c=require("crypto");const k=c.pbkdf2Sync(process.env.PW,Buffer.from(p.salt,"base64"),p.iter,32,"sha256");const r=Buffer.from(p.ct,"base64");const d=c.createDecipheriv("aes-256-gcm",k,Buffer.from(p.iv,"base64"));d.setAuthTag(r.subarray(r.length-16));console.log("decrypt OK",Buffer.concat([d.update(r.subarray(0,r.length-16)),d.final()]).length)' # PW=<passphrase>

# 2. build (static export to out/) — prebuild re-encrypts automatically
npm run build

# 3. verify the exported page is gated and leak-free (expect gate=1, leak=0)
f=out/portal/<client>/proposal.html
echo "gate:$(grep -c 'Protected document' $f) leak:$(grep -cE 'PRICE|₪|<secret marker>' $f)"

# 4. deploy hosting
firebase deploy --only hosting

# 5. purge the Cloudflare edge cache — REQUIRED after every content change.
#    Reuse the existing `deploy` skill's purge step (it loads the project's
#    CF_ZONE_ID / CF_API_TOKEN from the deploy environment and POSTs
#    purge_everything to the Cloudflare API). Credentials are NOT stored in,
#    or referenced by, this skills repo.
```

Then confirm production:
```bash
curl -s -D - -o /tmp/p.html "https://globalbit.co.il/portal/<client>/proposal" \
  | grep -i -E '^HTTP/|x-robots-tag'
echo "gate:$(grep -c 'Protected document' /tmp/p.html) ciphertext:$(grep -c 'AES-256-GCM' /tmp/p.html)"
```
Expect `HTTP/2 200`, `x-robots-tag: noindex, ...`, `gate:1`, `ciphertext:1`.

---

## Guardrails & gotchas

- **Deploy is a production push of confidential content.** It needs explicit
  user approval; the safety classifier blocks it otherwise. Don't bypass —
  ask the user to approve or run `firebase deploy --only hosting` themselves.
- **`portal-secrets.json` is git-ignored. Never commit it.** Only the
  ciphertext `payload.json` is safe in git/deploy.
- **`content/<client>-proposal.html` must never be imported by any app file**
  — that would ship plaintext. Only `scripts/encrypt-proposal.mjs` reads it.
- After every content change you MUST rebuild + redeploy + **purge Cloudflare**
  (3 cache layers: CF edge, browser HTTP, per-tab `sessionStorage`-by-IV).
- Cloudflare credentials are supplied by the deploy environment (see the
  `deploy` skill) — never stored in or referenced by this skills repo.
- Route is `/portal/<client>/proposal` (Next exports `proposal.html`; Firebase
  serves it at the clean path). Old/bare `/portal/<client>` 404s — fine.
- Threat model: real confidentiality (content cryptographically unreadable
  without the password) but **no access logging or remote revocation** — to
  revoke, rotate the password in `portal-secrets.json` and republish. Don't
  weaken the generated passphrase.
- Optional, not yet built: "client opened the proposal" email/Telegram alert
  via the CRM (`trackVisit` Cloud Function / `notifyTelegramAdmins`). Wire a
  beacon from the gate on successful unlock when requested.

## Canonical example

`content/klapton-proposal.html` + `app/portal/klapton/proposal/*` is the
reference implementation — mirror its structure for new clients.

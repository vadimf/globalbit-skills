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
Only AES-256-GCM ciphertext (HTML *and* PDF) is ever exposed. The client decrypts
in-browser with a per-client passphrase. Every open is tracked in the CRM with
cookie-based visitor identification and email + Telegram alerts. Clients can leave
inline comments (Google-Docs style); the gate auto-localizes to Hebrew for RTL
proposals.

> **ARCHITECTURE (2026-06): ONE gate + ONE shell, served from Firebase Storage.**
> There is exactly **one** gate component — `components/portal/ProposalGate.tsx` —
> and **one** shell route — `app/portal/view` — that serves *every* proposal. A
> proposal is pure **data**: encrypted payloads in Storage + a Firestore doc.
> **Creating/updating a proposal needs NO route file and NO site rebuild.** See
> `docs/plans/2026-06-01-proposal-platform-scale-design.md`.

> **House rules**:
> - Never tell the user to run the steps — do them.
> - **NEVER copy the gate or create a per-proposal route.** That duplication is
>   the bug this architecture eliminated. One gate, one shell, forever.
> - Publish a proposal with **`npm run publish-proposal -- <slug>`** (data-only,
>   no rebuild). Use the full-site `npm run publish` ONLY when the gate/shell
>   *code* changes.
> - Never commit `portal-secrets.json`.
> - `git add` the proposal **source** (`content/<slug>-proposal.html` + any
>   `public/images/<slug>/`) after publishing.

For deeper reading, see **`WRITING-GUIDE.md`** (how to write good proposals,
not walls of text), **`COMMON-MISTAKES.md`** (gotchas learned the hard way),
and **`COMPOSITION.md`** (how this skill fits with `create-proposal`,
`globalbit-document`, and the other proposal-adjacent skills).
Read those before writing your first proposal — they save hours.

---

## Quick Start — full lifecycle in one screen

> **Architecture note (2026-06):** proposals are moving to a **single shared
> gate + single shell route, served from Firebase Storage**. New proposals use
> the **Storage-served flow below** — there is NO per-proposal route file and NO
> site rebuild. The old "copy the gate / create a route / npm run publish" flow
> is **legacy** (klapton + mtc are still on it until migrated). NEVER copy the
> gate again — there is exactly one gate at `components/portal/ProposalGate.tsx`.
> See `docs/plans/2026-06-01-proposal-platform-scale-design.md`.

For a new proposal called `acme`:

```bash
# 1. WRITE   → content/acme-proposal.html  (raw HTML fragment, see templates/)
# 2. SECRET  → add "acme": "Acme-<hex>-<hex>-GB<yy>" to portal-secrets.json (git-ignored)
# 3. IMAGES  → put any bespoke images under public/images/acme/  (optional)
# 4. PUBLISH → data-only: encrypt + render PDF + upload to Storage + register.
#             NO site build, NO hosting deploy.
npm run publish-proposal -- acme
# 5. COMMIT  → git add content/acme-proposal.html public/images/acme/   (source only)
```

After `npm run publish-proposal -- acme`:
- **Live immediately** at `https://globalbit.co.il/portal/acme/proposal` — the
  single shell route serves it; no new route file exists, the marketing site is
  not rebuilt or redeployed.
- Encrypted payloads in Storage: `proposals/acme/latest.{html,pdf}.json`
  (public-read ciphertext, fetched by the shell) + `v<N>.*` history (admin-only).
- Registered in CRM at `https://crm.globalbit.co.il/proposals/acme`; passphrase
  mirrored to `proposal_secrets/acme`.
- Send the URL by email + the passphrase by WhatsApp (separate channels) — on you.

**To UPDATE** an existing proposal: edit `content/acme-proposal.html`, rerun
`npm run publish-proposal -- acme`. Done — live instantly, new version snapshotted.

**When does a site deploy happen?** Only when the **gate/site CODE** changes
(`components/portal/ProposalGate.tsx`, the shell, etc.) — then `npm run publish`
rebuilds + deploys the site once and the fix covers every proposal at once.
Publishing/updating a *proposal* never needs it.

One-time bucket CORS (already set): `node scripts/set-storage-cors.mjs`.

---

### Legacy per-route flow (klapton + mtc only — do NOT use for new proposals)

The two original proposals still have `app/portal/<slug>/proposal/page.tsx` +
bundled `payload.json` and are published by the full-site `npm run publish`
chain. They keep working because a static file beats the shell rewrite. They'll
be migrated to the Storage-served shell later via `publish-proposal` + deleting
their route dir. Until then, do not copy their route as a template.

---

## System map — what talks to what

```
   YOU author:
     content/<slug>-proposal.html   (plaintext HTML, in git)
     portal-secrets.json            (passphrase, git-IGNORED)

       │
       │  npm run publish-proposal -- <slug>     (data-only — NO site build)
       ▼
   ENCRYPT HTML  ─┐
   RENDER  PDF   ─┤→  upload ciphertext to Firebase Storage:
                  │     proposals/<slug>/latest.{html,pdf}.json   (public-read, shell fetches)
                  │     proposals/<slug>/v<N>.{html,pdf}.json      (admin-only history)
                  └→  Firestore proposals/<slug> (+ deployments/{id})
                      + proposal_secrets/<slug>.passphrase

   CLIENT opens  https://globalbit.co.il/portal/<slug>/proposal:
     Firebase rewrite  /portal/*/proposal → /portal/view.html  (the ONE shell)
       → shell reads <slug> from the URL
       → fetches proposals/<slug>/latest.html.json from Storage (ciphertext)
       → password → AES-GCM decrypt in-browser → renders via ProposalGate
       → fires /t/proposal-open?client=<slug>
                                       │
                                       ▼
                          trackProposalOpen Cloud Function:
                          reads gb_visitor/gb_lead cookies, maps to a lead,
                          writes portal_opens + lead activity, emails + Telegram.
                                       │
                                       ▼
              CRM /proposals/<slug> "Opens" tab + /leads/<id> activity show it
```

**One Firestore database, one Firebase Storage bucket**, shared by main
site + CRM. **One canonical `firestore.rules` / `firestore.indexes.json` and
`storage.rules` at the repo root.** Storage `proposals/<slug>/latest.*` is
public-read (safe — ciphertext); `v<N>.*` is admin-only.

---

## What's hardcoded, what's templated, what changes per proposal

| Layer | What | Where |
|---|---|---|
| **HARDCODED** — never edit per proposal | The ONE gate component (decrypt, render, all CSS, JS enhancements, comments, EN/HE i18n). The ONE shell route. Build/publish scripts. Firebase + Storage rules. | `components/portal/ProposalGate.tsx`, `app/portal/view/{page,layout}.tsx`, `scripts/{encrypt-proposal,render-and-encrypt-pdf,publish-proposal}.mjs`, `firebase.json`, `storage.rules` |
| **TEMPLATED** — structure fixed, content varies | Section skeleton (cover → exec → … → next). About-Globalbit block. Hourly rates table. Generic terms. | `templates/proposal-skeleton.html`, `templates/about-globalbit.html` |
| **PER-PROPOSAL** — write fresh each time | The whole `content/<slug>-proposal.html`: title, reference, dates, exec summary, background, goals, solution, scope, phases, team, timeline, risks, value, commercial, next steps. Plus any per-proposal inline `<style>` (incl. the RTL block for Hebrew). | `content/<slug>-proposal.html` |

**Do not edit the gate component or its CSS per client.** Change it once in
`components/portal/ProposalGate.tsx` and it propagates to **every** proposal
(all served by the one shell) and to every PDF (the render script reads the
gate's CSS as the single source of truth). A gate change is a *code* change →
`npm run publish` (full build+deploy), which is rare.

---

## Architecture in 30 seconds

```
content/<slug>-proposal.html      ─┐  publish-proposal.mjs
portal-secrets.json (git-ignored) ─┘   ├─ encrypt HTML  ─► Storage proposals/<slug>/latest.html.json
                                       └─ render+encrypt PDF ─► Storage proposals/<slug>/latest.pdf.json
                                          (+ v<N>.* history, + Firestore proposals/<slug>, + secret)

browser:  user opens /portal/<slug>/proposal
          → Firebase rewrite serves the ONE shell (/portal/view.html)
          → shell reads <slug> from URL, fetches latest.html.json from Storage
          → enters password
          → JS decrypts with AES-GCM (PBKDF2-SHA256, 600k iters)
          → renders the HTML; runs enhancements (TOC, Gantt, exec digest, glossary,
            comments; EN/HE strings auto-selected from the content's direction)
          → "Download PDF" → fetch latest.pdf.json from Storage → decrypt → download
```

Security: same passphrase decrypts both payloads. Plaintext content lives in the
repo (so you can edit) but the app never imports it — only the encrypt scripts
read it. The deployed bundle contains **no** ciphertext at all; ciphertext lives
only in Storage and is fetched at runtime.

---

## Built-in reader controls (gate features — no per-client work)

The gate component ships with reader-side tools that every proposal gets for
free. Don't duplicate any of this in `content/<client>-proposal.html`.

### Reading-mode toggle: Full / Executive — 3 min

Two synchronised mode switches live on every proposal:

- **In-content `.mode-bar`** — appears right after the `#summary` card with
  descriptive copy ("We know your time matters…"). Built by
  `setupModeToggle(root)`.
- **TOC quick toggle `.toc-mode-sw`** — compact pill-shaped switch in the
  sticky TOC sidebar, sits just above `#gp-dl` (Download PDF). Built by
  `setupTocControls(root)`.

Both call a shared `setMode(root, mode)` helper that toggles `mode-exec` on
the `.gb-proposal` root **and** syncs `.on` state across every visible
mode-switch (so flipping one updates the other instantly). Executive mode
hides everything not whitelisted as a "hero" (stats grids, estimate band,
gantt, summary card) and shows per-section digests built by
`buildExecDigest(root)`.

### Share button

`#gp-toc-share` lives in the TOC sidebar between the mode toggle and the
Download PDF button. On click it:

1. Tries the **Web Share API** (`navigator.share`) — mobile + modern browsers
   open the native share sheet. Cancelling with `AbortError` is silent.
2. Falls back to **`navigator.clipboard.writeText`** and shows a transient
   "Link copied" tooltip via the `.copied` class.
3. Last-resort fallback: `window.prompt("Copy this link:", url)` so the link
   is always recoverable even in locked-down environments.

The shared URL is `window.location.href` and the title is `document.title`
(set from the route's `metadata.title` in `app/portal/<client>/proposal/page.tsx`).

### Idempotency (mandatory for any new gate enhancement)

`setupTocControls` (and every other enhancement) MUST be idempotent:

```ts
if (toc.querySelector(":scope > .toc-mode-sw")) return;
```

This is non-negotiable. React Fast Refresh, the recovery `MutationObserver`,
and `dangerouslySetInnerHTML` re-application can all re-run enhancement
helpers. Without an idempotency guard you double-inject and break event
listeners. See COMMON-MISTAKES.md #4.

### Adding more reader-side tools later

Follow the same shape: a new `setupX(root)` function in `components/portal/ProposalGate.tsx`,
an idempotency guard, a call from `enhanceProposal()`, CSS inside the gate's
CSS template literal (watch for backticks — see COMMON-MISTAKES.md #2). Edit the
ONE gate at `components/portal/ProposalGate.tsx` — it serves every proposal, so
there is nothing to sync. Any new user-facing string also needs an `en` + `he`
entry in `GATE_STRINGS`.

---

## Embedding images in a proposal

Two figure patterns are already wired up. Use them — don't roll your own.

### File layout

| Where it goes | What it's for |
|---|---|
| `public/images/<client>/` | Client-specific design mockups, building photos, anything bespoke to one proposal |
| `public/images/crm/` | Product screenshots of the Globalbit Sales Copilot CRM (shared across proposals) |
| `public/images/` (root) | Hero backgrounds, logos, awards — global Globalbit assets |

**Filename rule**: use descriptive, hyphenated names (`homepage-hero.png`,
`visitor-intelligence-card.png`, `facilities.png`). Never `1.png` /
`screenshot-final-v3.png`. The filename is the alt-text fallback when an
image fails to load and shows up in CMS-style file pickers later.

### Two figure styles

Both styles live in the per-client `<style>` block in
`content/<client>-proposal.html` so they can be tuned per proposal without
touching the gate.

**`.design-mockup`** — frameless, no background, no shadow. For client
design mockups, building photos, brand visuals. The image speaks for
itself; the mono caption sits cleanly below.

```html
<figure class="design-mockup">
  <img src="/images/mtc/homepage-hero.png" alt="MTC website homepage mockup — UAV hero with &quot;Who we are — Multiple Solutions One Roof&quot; tagline" />
  <figcaption>Homepage hero — the approved MTC design that Globalbit will implement faithfully in WordPress.</figcaption>
</figure>
```

```css
.gb-proposal .design-mockup { margin: 28px auto; max-width: 880px; background: transparent; padding: 0; border: 0; box-shadow: none; }
.gb-proposal .design-mockup img { display: block; width: 100%; height: auto; border-radius: 8px; background: transparent; box-shadow: none; }
.gb-proposal .design-mockup figcaption { font-family: var(--mono); font-size: 11px; color: var(--muted); text-align: center; margin-top: 12px; }
```

**`.crm-shot`** — soft drop shadow, rounded corners. For product
screenshots of the CRM, analytics dashboards, our own UI. Has a `.crm-shot-narrow`
size variant (520px max-width) for small UI elements like a Page Journey row.

```html
<figure class="crm-shot crm-shot-narrow">
  <img src="/images/crm/page-journey.png" alt="Sales Copilot CRM — Page Journey breakdown showing pages visited, time per page, and scroll depth per visit" />
  <figcaption>Page Journey: every page the visitor opened, how long they stayed, and how deep they scrolled.</figcaption>
</figure>
```

### Alt text discipline

Every `<img>` gets a real `alt` — a one-line description of what's *in* the
image (engagement score, UAV hero, Air/Land/Naval product tabs), not what
it *means* (the design we'll build, our beautiful CRM). The PDF render
captures alt text in the document's accessibility tree; assistive tech and
PDF search both rely on it.

### PDF page-break protection (automatic)

Figures, `.design-mockup`, `.crm-shot`, and bare `<img>` are all in the
PDF's `break-inside: avoid` list (see `scripts/render-and-encrypt-pdf.mjs`).
Composite blocks (`.awards-block`, `.client-grid`, `.stats-grid`) are also
kept together. If you add a new composite block that contains multiple
images or items and shouldn't split, add its selector to PRINT_OVERRIDES.

---

## Per-client visual overrides (the inline `<style>` block)

When a single proposal needs design treatment that doesn't belong in the
shared gate (lightening the exec summary card for a particular client,
forcing a smaller subheader for one chapter, hiding the auto-injected
Gantt because the project is too small to need it), put it in an inline
`<style>` block at the very top of `content/<client>-proposal.html`.

```html
<div class="progress" id="gp-progress"></div>

<style>
  /* <CLIENT>-specific overrides (kept in content per skill rule —
     never edit the shared gate per-client). */

  /* Hide the shared 6-month Gantt — this is a 6-week project. */
  #phases > .gantt { display: none; }

  /* Lighten the exec summary card from pure-black to soft grey. */
  .gb-proposal #summary .summary             { background: #f2f2f2; color: #1a1a1a; }
  .gb-proposal #summary .summary h2          { color: #1a1a1a; }
  .gb-proposal #summary .summary .rule       { background: #1a1a1a; }
  .gb-proposal #summary .summary .bullet::before { background: #1a1a1a; }

  /* Compact subheader for this chapter only. */
  .gb-proposal #crm .lead-xl,
  .gb-proposal #ai-first .lead-xl { font-size: clamp(18px,1.8vw,22px); font-weight: 600; }
</style>

<header class="cover">
  ...
</header>
```

### Why this, not a gate edit

There is ONE gate for every client by design. Per-client divergence in the gate
means future drift, broken PDF rendering (the render script reads the gate's CSS
as the single source of truth), and impossible-to-maintain proposals. The inline
`<style>` is the prescribed escape hatch: the divergence lives in the content,
not the gate, and stays scoped to a single client's payload.

### When to promote a per-client style to the gate

If three different proposals end up with the same override, that's
evidence the gate's default is wrong. Promote the rule into the gate
(`components/portal/ProposalGate.tsx`), delete it from each content fragment,
and `npm run publish` (a gate/code change → full deploy).

### When to use PRINT_OVERRIDES instead

The inline `<style>` block applies to BOTH screen and PDF. If a style
should only apply in the PDF (e.g., a tighter logo grid for paper, a
forced 2×2 card layout that the on-screen version doesn't need), put it
in `scripts/render-and-encrypt-pdf.mjs > PRINT_OVERRIDES`. That stylesheet
is appended only when puppeteer renders, never to the deployed page.

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

> **NO route file.** Do NOT create `app/portal/<slug>/`. Do NOT copy the gate.
> The one shell at `app/portal/view` already serves your slug via the
> `/portal/*/proposal` rewrite the moment the Storage payload exists.

### 2. Set the passphrase in `portal-secrets.json` (git-ignored)

```json
{ "klapton": "...", "<slug>": "<STRONG-PASSPHRASE>" }
```

Generate strong:

```bash
echo "$(tr '[:lower:]' '[:upper:]' <<< ${slug:0:1})${slug:1}-$(openssl rand -hex 8)-$(openssl rand -hex 8)-GB$(date +%y)"
# example: Acme-4a641d8a-fcd7c585-GB26
```

The encryptor refuses passwords < 8 chars. Don't weaken them.

### 3. Add bespoke images (optional)

`public/images/<slug>/` for client-specific mockups/photos. These ARE part of
the deployed static assets, so if you add new images run a one-time
`npm run publish` (full deploy) so they ship — OR reference images that already
exist under `public/`. (Most proposals reuse shared `/images/crm/`, logos, etc.,
and need no new image deploy.)

### 4. Publish — data-only, no rebuild

```bash
npm run publish-proposal -- <slug>
```

This encrypts the HTML, renders + encrypts the PDF (headless Chrome, ~10s),
uploads `latest.{html,pdf}.json` + `v<N>.*` to Storage, and registers Firestore +
the passphrase. **Live immediately** at `https://globalbit.co.il/portal/<slug>/proposal`
— no `app/portal` route, no site build, no hosting deploy.

Requires Application Default Credentials (`gcloud auth application-default login`
once, or `GOOGLE_APPLICATION_CREDENTIALS`).

### 5. Verify on production

```bash
curl -sI "https://globalbit.co.il/portal/<slug>/proposal" | grep -i 'x-robots-tag'   # → noindex
# Storage payload is public-read ciphertext:
curl -s "https://firebasestorage.googleapis.com/v0/b/globalbit-website-2026.firebasestorage.app/o/proposals%2F<slug>%2Flatest.html.json?alt=media" | head -c 80
```
Or open the URL, enter the passphrase, scroll, click Download PDF (<1s).

### 6. Commit the SOURCE

```bash
git add content/<slug>-proposal.html public/images/<slug>/   # source only
git commit -m "feat(portal): <slug> proposal"
```
`portal-secrets.json` stays git-ignored — the passphrase reaches the CRM via
`proposal_secrets/<slug>` (written by publish-proposal).

### 7. Hand off

Give the URL and password to the user, via **separate channels** (URL by email,
password by phone/WhatsApp/Signal). Never put them in the same message. The CRM
admin at `https://crm.globalbit.co.il/proposals/<slug>` lists it and logs opens.

---

## Update an EXISTING proposal

Edit `content/<slug>-proposal.html`, then `npm run publish-proposal -- <slug>`.
Live instantly with a new `v<N>` snapshot. Never edit the gate per client. The
gate's `sessionStorage` cache auto-invalidates (the IV changes each encryption),
so returning viewers re-enter the password once and see fresh content.

---

## Hebrew / RTL proposals

The gate is LTR by default but **auto-detects RTL** and switches all injected UI
strings (mode toggle, "A note for you", Share, Comments pill/panel/composer, name
modal, exec-digest, appendix) to Hebrew — via `GATE_STRINGS.he` +
`detectGateLang()` in `components/portal/ProposalGate.tsx`, keyed off the rendered
root's computed `direction`.

To make a proposal Hebrew, your `content/<slug>-proposal.html` must:
1. Write the body content in Hebrew.
2. Open with an inline `<style>` block that sets `.gb-proposal { direction: rtl }`
   and mirrors the gate's physical-direction rules + fixes Hebrew font sizing
   (the gate uses a mono font with no Hebrew glyphs for some labels). **Copy
   `content/kablan-chacham-proposal.html`'s top `<style>` block as the canonical
   RTL starting point** — it handles tables, gantt, comments panel flip, and the
   mono→sans font swaps.
3. Set Hebrew `title`/`description`… nothing else — there is no per-proposal
   route metadata anymore; the shell ships a generic title and the gate upgrades
   `document.title` from the cover **after** unlock.

If you add a NEW Hebrew UI string to the gate, add BOTH `en` and `he` entries to
`GATE_STRINGS`.

---

## Publish reference

| You changed… | Run | Effect |
|---|---|---|
| A **proposal** (`content/<slug>-proposal.html`, images already present) | `npm run publish-proposal -- <slug>` | Data-only. Live instantly. No build, no deploy. |
| The **gate/shell CODE** (`components/portal/ProposalGate.tsx`, `app/portal/view`, scripts) | `npm run publish` | Full build + hosting deploy + record-deployment. Covers every proposal at once. Rare. Then CF purge. |
| **New images** under `public/images/<slug>/` | `npm run publish` once | Ships the static assets. |

`npm run publish` is defined in `package.json` as:

```json
"publish": "npm run build && firebase deploy --only hosting && node scripts/record-deployment.mjs"
```

The chain in order:

1. **`prebuild`** (auto-fires before `build`): re-encrypts every
   `content/*-proposal.html` and re-renders every PDF for every client in
   `portal-secrets.json`. ~10s per client for the PDF render. Output:
   `app/portal/<client>/proposal/payload.json` and
   `public/portal/<client>/proposal/payload.pdf.json`.
2. **`next build`**: produces the static export at `out/`.
3. **`postbuild`** (auto-fires after `build`): runs `sync-articles.ts` —
   unrelated to proposals, just blog sync. Harmless.
4. **`firebase deploy --only hosting`**: pushes `out/` to Firebase Hosting
   at `globalbit.co.il`. ~1-3 minutes depending on file count.
5. **`scripts/record-deployment.mjs`**: the CRM bridge. For each client in
   `portal-secrets.json`:
   - Parses `content/<slug>-proposal.html` for cover title, eyebrow, and
     `GB-YYYY-XXX-NNN` reference
   - Reads the just-deployed encrypted payloads
   - Bumps `proposals/<slug>.current_version` by one
   - Writes immutable `proposals/<slug>/deployments/{id}` doc with git SHA,
     deployer email, content checksum, byte sizes
   - Uploads the encrypted payloads to Storage
     `proposals/<slug>/v<N>.{html,pdf}.json`
   - Upserts `proposal_secrets/<slug>.passphrase` from `portal-secrets.json`
   - On first ever deploy for a slug: also creates the parent
     `proposals/<slug>` doc with `lead_id = null`, `status = "deployed"`
6. **Cloudflare cache purge** — currently NOT in `npm run publish`. Run
   manually after:

   ```bash
   set -a && source .env.local && set +a
   curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/purge_cache" \
     -H "Authorization: Bearer ${CF_API_TOKEN}" -H "Content-Type: application/json" \
     --data '{"purge_everything":true}'
   ```

   (If you're seeing a lot of CF-stale issues, add this to the `publish`
   script chain.)

### Post-publish verification (Storage-served proposals)

```bash
B=globalbit-website-2026.firebasestorage.app
# 1. Page serves the shell + noindex header
curl -s -D - -o /dev/null "https://globalbit.co.il/portal/<slug>/proposal" | grep -i -E '^HTTP/|x-robots-tag'
# 2. Storage payload is a valid public-read ciphertext
curl -s "https://firebasestorage.googleapis.com/v0/b/$B/o/proposals%2F<slug>%2Flatest.html.json?alt=media" \
  | grep -o '"alg":"AES-256-GCM"'
# 3. Versioned history is admin-only (expect 403)
curl -s -o /dev/null -w '%{http_code}\n' "https://firebasestorage.googleapis.com/v0/b/$B/o/proposals%2F<slug>%2Fv1.html.json?alt=media"
```

Expect: `HTTP/2 200`, `x-robots-tag: noindex, …`, `"alg":"AES-256-GCM"`, and `403`
on the versioned file.

### Auth for the Admin-SDK scripts (`publish-proposal.mjs`, `record-deployment.mjs`)

Uses Firebase Admin SDK. Requires either:

- `GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json` env var (CI),
  OR
- A one-time `gcloud auth application-default login` on the local machine

If it errors with "Application Default Credentials not found", run the
gcloud command once and retry.

### Deployer label

`record-deployment.mjs` writes `deployed_by: "vadim@globalbit.co.il"` by
default. Override with `DEPLOYER_EMAIL=...` env var if someone else publishes.
This is purely an audit-log label — actual auth comes from gcloud ADC.

Deploy of confidential content is a production push — needs explicit user
approval. If the safety classifier blocks `firebase deploy`, ask the user.

---

## CRM integration — what auto-registers

The CRM at `https://crm.globalbit.co.il` reads from the same Firestore +
Storage that proposals write to. No manual sync.

### Collections written by the pipeline

| Collection | Written by | When |
|---|---|---|
| `proposals/{slug}` | `publish-proposal.mjs` (Storage-served) / `record-deployment.mjs` (legacy) | First publish; updated each subsequent publish |
| `proposals/{slug}/deployments/{id}` | same | Every publish, immutable |
| `proposal_secrets/{slug}` | same | Every publish, upserts passphrase |
| `portal_opens/{id}` | `trackProposalOpen` function | Every gate unlock (30s per-visitor dedupe) |
| `leads/{leadId}/activity/{id}` | `trackProposalOpen` function | Open events for cookie-matched leads (`proposal_opened`); comments → `proposal_commented` |

### Storage paths

| Path | Written by | Access |
|---|---|---|
| `proposals/{slug}/latest.{html,pdf}.json` | `publish-proposal.mjs` | **public-read** (the shell fetches it) |
| `proposals/{slug}/v{N}.{html,pdf}.json` | `publish-proposal.mjs` / `record-deployment.mjs` | admin-only (history) |

### What the CRM admin shows (no extra work from you)

- **`/proposals`** — list of every registered proposal, real-time, sortable, searchable, status-filterable
- **`/proposals/{slug}`** — 4 tabs:
  - **Overview** — cover metadata + portal URL + lead link + **"Portal access" card with the per-client passphrase** (masked, Show / Copy buttons, "send via separate channel" reminder)
  - **Versions** — every deployment, each downloadable as PDF (decrypts in-browser via Web Crypto, plaintext never touches disk)
  - **Opens** — every portal unlock, lead label if matched, anon visitor ID otherwise
  - **Lead** — link/unlink to a CRM lead, change cached label
  - **Settings** — status (`draft` / `deployed` / `archived`) + free-text notes
- **`/leads/{id}` activity timeline** — entries of type `proposal_opened` appear inline with emails, calls, stage changes

### What you need to do per new client

**Nothing.** The first `npm run publish-proposal -- <slug>` creates the
`proposals/{slug}` doc, uploads v1 to Storage, mirrors the passphrase, and
that's it. The CRM picks it up via real-time listeners — no route, no rebuild,
no manual import.

---

## Where Firestore rules + indexes live

**One canonical pair at the repo root:**

```
/firestore.rules
/firestore.indexes.json
```

The main site's `firebase.json` references them. The CRM's
`crm/firebase.json` does NOT have a `firestore` section anymore — it
only ships the Cloud Functions. Deploying rules/indexes is done from
the **repo root**:

```bash
firebase deploy --only firestore:rules,firestore:indexes
```

Never duplicate these files into `crm/`. The two used to diverge, and
the most recently-deployed copy won — which silently broke the proposals
admin when the main site got a full deploy. See COMMON-MISTAKES #22.

---

## The PDF pipeline — how it works (so you don't re-invent it)

- **Build-time, headless Chrome**: `scripts/render-and-encrypt-pdf.mjs` reads the
  proposal HTML, **reads the exact same CSS** out of `components/portal/ProposalGate.tsx` (single
  source of truth), wraps in `<div class="gb-proposal">` + a few print overrides
  (single-column layout, hide TOC/progress/mode bar, force appendix open, full-color
  logos), writes to a temp file in `/public`, navigates puppeteer to that file
  via `file://`, and saves an A4 PDF.
- **`emulateMediaType("screen")` before `page.pdf()`** — non-obvious but
  critical. The gate's CSS contains a "Nuclear print theme" `@media print` block
  (`.gb-proposal,.gb-proposal *{background:transparent!important;color:#000!important;...}`)
  that exists to keep Chrome's *browser print dialog* fast on long documents.
  Without `emulateMediaType("screen")`, puppeteer triggers that block and the
  PDF comes out with every background, color, and image stripped. With screen
  emulation the nuclear theme stays dormant and the deliverable PDF matches the
  on-screen view 1:1. (`printBackground: true` alone does NOT save you here —
  the nuclear block uses `background:transparent`, which prints transparent.)
- **Header / footer templates** (`displayHeaderFooter: true` with
  `headerTemplate` / `footerTemplate`): the header carries the Globalbit logo
  (loaded once as a `data:image/webp;base64,...` URI; header/footer iframes can't
  reliably load `file://`), the footer carries a per-client label extracted from
  `.cover .eyebrow` and Chrome's native `<span class="pageNumber"></span> /
  <span class="totalPages"></span>` page counters. Every style in those
  templates must be inline (the templates inherit no page CSS) and include
  `-webkit-print-color-adjust:exact;print-color-adjust:exact;` for backgrounds.
  Margins in `page.pdf()` must reserve enough room for both (~20mm top, 18mm
  bottom in the current setup).
- **TOC page numbers (NOT supported)** — Chrome's PDF rendering does not
  implement `target-counter()` from CSS Paged Media Level 3, so an in-document
  TOC with computed cross-reference page numbers ("Section 5 ........ page 12")
  is impossible via pure CSS. Workarounds require a post-processing toolchain
  (paged.js, PrinceXML, or a Node PDF library to inject page numbers after
  render). Today the on-screen sticky `.toc` is hidden in the PDF entirely —
  navigation in the PDF relies on Chrome's bookmark sidebar + internal anchor
  links instead.
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

For a **new English proposal**, `content/klapton-proposal.html` is the reference
for content + section structure (note: klapton is still a LEGACY route-based
proposal, but its *content fragment* is the canonical example). For a **Hebrew
RTL proposal**, copy `content/kablan-chacham-proposal.html`'s top inline `<style>`
block as the RTL starting point. In both cases you only author the content
fragment + a passphrase, then `npm run publish-proposal -- <slug>` — there are no
route files to mirror.

If something is unclear or broken, read **`COMMON-MISTAKES.md`** before
re-architecting anything.

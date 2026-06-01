# Common Mistakes — Lessons From the Field

Every entry below cost real time to figure out. Read this before you start
"fixing" something that looks wrong.

---

## 1. Editing files in `.claude/worktrees/<name>/` while dev server runs from the parent dir

**Symptom**: you keep editing the gate or content, save, reload — nothing
changes. You become convinced the cache is broken.

**Cause**: the project has git worktrees under `.claude/worktrees/`. If you `cd`
into one and edit there, but the user's `npm run dev` is running from the
parent project dir, your edits are in a *different copy of the file*. Next.js
serves the parent's files; your changes go nowhere.

**Fix**: always check the absolute path of the file you're editing matches the
absolute path Next is serving. If you're in a worktree, either:
- Edit files at `/Users/vadim/Documents/Code/Globalbit Website/Globalbit Surf/…`
  (the parent), or
- Restart the dev server from inside the worktree.

The Read tool tells you the absolute path. Use it. Never trust your `cd` mental
model.

---

## 2. Backticks inside the CSS template literal close the string

**Symptom**: the page renders white, or with no styling. Build/console may show
a parse error pointing somewhere unrelated.

**Cause**: the gate's CSS lives inside a JS template literal:

```ts
const CSS = `
  /* don't put a literal backtick like ` in this comment */
  .gb-proposal …
`;
```

A backtick inside the template (even in a comment) closes the string. The
parser then sees JS where CSS should be and fails confusingly.

**Fix**: never put `` ` `` inside the CSS string. Not in comments, not in
content. Use straight quotes only.

---

## 3. `display: revert` resets grid/flex to UA default `block`

**Symptom**: in Executive mode (or any "show only some children" mode), grids
suddenly stack 1-column. `.stats-grid` and `.av` collapse vertically.

**Cause**: trying to do "show only whitelisted children" via:

```css
.mode-exec .content section > * { display: none }
.mode-exec .content section > .stats-grid { display: revert }
```

The `revert` value resets `display` to the *user-agent default*, which is
`block` for `<div>` — even though we set `.stats-grid { display: grid }`
elsewhere. Grids stack vertically.

**Fix**: use a data attribute approach instead. Apply `data-exec-hide="1"` to
elements that should hide; whitelist by simply NOT setting the attribute. CSS:
`.gb-proposal [data-exec-hide]{ display: none !important }`. Whitelisted
elements keep their natural `display`.

---

## 4. HMR / Fast Refresh wipes injected DOM

**Symptom**: you save the gate, the page reloads, and the JS-injected widgets
(`.mode-sw`, `.exec-more`, gantt, summary facts) disappear. Texts also vanish
intermittently.

**Cause**: React Fast Refresh re-runs the component, which re-runs the
`dangerouslySetInnerHTML`, which replaces the inner DOM — wiping anything the
enhancement helpers had injected.

**Fix**: the gate runs a `MutationObserver` on its root. If `.mode-sw` (or any
sentinel widget) goes missing, the observer re-runs `enhanceProposal(root)`.
Every helper has its own idempotency guard (`if (sec.dataset.gpInit) return`)
so re-running doesn't double-inject. **If you add a new enhancement, give it an
idempotency guard.**

---

## 5. Direct click handlers don't survive DOM replacement

**Symptom**: Download PDF button or TOC minimize button stops working after a
Fast Refresh or any re-render.

**Cause**: direct `btn.addEventListener("click", …)` attaches the listener to a
specific DOM node. When the DOM is replaced (HMR, re-applied innerHTML), the
node is gone, but a new node with the same `id` exists — and has no listener.

**Fix**: event-delegate on the root. Attach one listener on the proposal root
element, check `target.closest("#gp-dl")` inside the handler. Listener survives
inner-DOM replacement because the root isn't replaced.

---

## 5a. PDF renders with no backgrounds, no colors, no hero image

**Symptom**: the deployed PDF is monochrome — white covers (no hero UAV
background), no dark `.summary` card, no dark `.estimate` band, design mockups
print but their context loses color. The on-screen view is fine; only the PDF
strips colors.

**Cause**: the gate's CSS has a "Nuclear print theme" `@media print` block
(`proposal-gate.tsx` around line 365) that forces
`background:transparent!important;color:#000!important` on every element. It
exists to keep Chrome's browser print dialog fast on a 25-page proposal —
without it, Safari and Chrome rasterize every dark panel and pre-print preview
takes 40+ seconds. But that same block fires when puppeteer's `page.pdf()`
runs, because puppeteer defaults to `media: 'print'`.

`printBackground: true` does NOT fix this — the nuclear block sets
`background:transparent`, so there's nothing to print.

**Fix**: in `scripts/render-and-encrypt-pdf.mjs`, call
`await page.emulateMediaType('screen')` **before** `page.goto(...)`. The
deliverable PDF then renders the full on-screen treatment (hero, dark summary,
estimate band, design mockups in full color). The nuclear print theme stays
dormant — and your *browser* print dialog still flattens things to white the
moment a user invokes it manually, which is the whole point.

Do not "fix" this by deleting the nuclear print theme from the gate. The
browser-print-dialog performance protection is real and load-bearing.

---

## 5b. PDF pages with a heading and then huge empty space

**Symptom**: a chapter shows its `<h2>` + a couple of lines, then a half-page
of whitespace, then the chapter actually begins on the next page. Common
victims: Risk management (heading alone on one page, table on the next),
Commercial terms (Strategic project designation card alone, components table
on the next), Added Value (one card per page).

**Cause**: `PRINT_OVERRIDES` previously listed `section` in the
`break-inside:avoid` rule. Chrome interprets that as "do not split the
section across pages". When the entire section doesn't fit in the remaining
space on the current page, Chrome pushes the *whole* section to the next
page — leaving the previous page short.

**Fix**: only protect ATOMS from splitting (cards, table rows, blockquotes,
figures, individual mockups). Let sections flow across page boundaries.
The shape of the rule:

```css
/* DO NOT include `section` here */
.gb-proposal .card,
.gb-proposal .ac,
.gb-proposal blockquote,
.gb-proposal figure,
.gb-proposal table,
.gb-proposal tr { break-inside: avoid; page-break-inside: avoid; }
```

This produces clean, dense pagination — atoms stay intact, sections flow.

---

## 5c. Awards / clients sections eat a whole A4 page each

**Symptom**: the "Our clients" logo grid (28 logos) takes a full A4 page on
its own. The awards block (`14 @ TOP 1 / App of the Year / Editor Choice /
e-Gov Standard`) takes another full page, with cards stacked one per row.
On screen the same blocks look balanced.

**Cause**: the on-screen `.client-grid` uses `auto-fit` with
`minmax(110px,1fr)`, 32×24px gaps, and 36px padding — designed for
breathing room on a wide monitor. The on-screen `.awards-cards` is a
4-column grid that collapses to 1 column below 720px width, which can
inadvertently fire in the rendered PDF layout. Result: vast whitespace at
A4.

**Fix**: in `PRINT_OVERRIDES`, force compact PDF-only layouts:

```css
.gb-proposal .client-grid{
  grid-template-columns:repeat(6,1fr)!important;
  gap:14px 18px!important;
  padding:18px 20px!important;
}
.gb-proposal .client-grid img{height:30px!important}

.gb-proposal .awards-cards{
  grid-template-columns:repeat(2,1fr)!important;
  gap:10px!important;
}
.gb-proposal .ac{min-height:0!important;padding:16px 18px!important}
```

Keep these in `PRINT_OVERRIDES` (the PDF-only stylesheet), not in the gate
CSS. The on-screen design intentionally uses the airier layout.

---

## 5d. Composite visual blocks (awards, client logos, stats) split across pages

**Symptom**: the "Our clients" 28-logo grid is half on page N and half on
page N+1. The peach awards block has its first two cards on one page and
the last two on the next. The 6-card stats grid splits 3-and-3.

**Cause**: PRINT_OVERRIDES protects individual `.card`, `.ac`, `.stat`,
`.ent` elements with `break-inside: avoid`, but the *containers* that
group them (`.client-grid`, `.awards-block`, `.stats-grid`) are not in
the list. Chrome happily breaks between the children.

**Fix**: add every grouped composite block to the keep-together rule in
PRINT_OVERRIDES:

```css
.gb-proposal .awards-block,
.gb-proposal .client-grid,
.gb-proposal .stats-grid { break-inside: avoid !important; page-break-inside: avoid !important; }
```

**Side effect to know**: if a block is so tall it doesn't fit on any
single A4 page, Chrome can't honor `break-inside: avoid` and falls back
to splitting anyway — usually after leaving the previous page short. The
compact PDF sizing rules earlier in PRINT_OVERRIDES (6-col client grid,
2×2 awards, tighter padding on `.stat`) are what keep these blocks fitting
on one page. Don't unwind those overrides without re-checking page breaks.

---

## 5e. `.av` grid renders 3-then-1-full-width in the PDF (inline `grid-column:1/-1`)

**Symptom**: the "Agile delivery" and "Managing scope, budget, and quality"
card grids in About Globalbit render as 3 cards on row 1 + a single
full-width card on row 2 in the PDF. The on-screen version looks fine.

**Cause**: the 4th card in each grid has `style="grid-column:1/-1"`
hardcoded inline — the on-screen design intentionally spans it across
the full row at desktop widths. In the PDF's effective column width,
`auto-fit minmax(220px,1fr)` collapses to 3 columns, and the inline-style
4th card still spans full width, producing an awkward 3+1 layout.

**Fix**: force a 2×2 grid in PRINT_OVERRIDES and override the inline
`grid-column` with `!important` (which beats inline `style="..."`):

```css
.gb-proposal .av { grid-template-columns: repeat(2, 1fr) !important; gap: 12px !important; }
.gb-proposal .av .card { grid-column: auto !important; padding: 18px 20px !important; }
.gb-proposal .av .card h4 { margin: 0 0 8px !important; font-size: 16px !important; }
.gb-proposal .av .card p { font-size: 13px !important; line-height: 1.5 !important; margin: 0 !important; }
```

`grid-column: auto !important` beats inline `style="grid-column:1/-1"` —
this is one of the few cases where CSS specificity rules actually work
in your favor against inline styles.

---

## 6. `file://` resources from `about:blank` are blocked by Chrome

**Symptom**: in the PDF render script, images don't load. Console:
> Not allowed to load local resource: file:///…/public/images/…

The PDF generates but `<img>` tags are empty boxes and `bg-desktop.webp` falls
back to the solid color.

**Cause**: `page.setContent(html)` makes the page origin `about:blank`. Chrome
refuses to load `file://` resources from non-file:// origins, regardless of
`--allow-file-access-from-files`.

**Fix**: write the HTML to a temp file under `/public` and use
`page.goto("file://" + tempPath)`. Now the page origin IS `file://`, and all
the rewritten asset paths load. Already implemented in
`scripts/render-and-encrypt-pdf.mjs` — don't undo it.

---

## 7. Safari's `window.print()` takes 30-60s on a long document

**Symptom**: user clicks Download PDF, the print dialog takes 40+ seconds to
appear in Safari. (Chrome is faster but also slow.)

**Cause**: Safari re-runs synchronous layout for the entire React tree,
including the site header/footer, all web fonts, all observers, and every CSS
Grid in the document — for the print preview. On a 25-page proposal that's
30-60 seconds.

**Fix**: do not use `window.print()`. The system uses a pre-rendered, encrypted
PDF served as a static asset. Click → fetch → decrypt → Blob → download.
**<1 second click-to-file.**

Do not "fix" the slow print by reverting to popup-window-print. Tried. Safari's
popup blocker treats scripted `window.open()` + `document.write` as suspicious
and routinely produces `about:blank`.

---

## 8. The encrypted PDF is too big to import into the JS bundle

**Symptom**: if you `import payload from "./payload.pdf.json"` in the route
page, every page load downloads ~1 MB of base64 ciphertext upfront.

**Fix**: keep `payload.pdf.json` under `public/portal/<client>/proposal/` and
**fetch on demand** when the user clicks Download PDF. The HTML payload
(~300 KB) is safe to bundle; the PDF is not.

---

## 9. `window.lintrk is not a function` on the proposal page

**Symptom**: console error. LinkedIn Insight Tag failed.

**Cause**: GTM is firing on the portal route, but the proposal page isn't a
normal marketing route — analytics tags don't belong there (privacy + noise +
errors).

**Fix**: `app/layout.tsx` checks `pathname.startsWith("/portal/")` and skips
loading GTM. Same gate hides `ScrollCTA`, `StickyBanner`, `MobileFooterMenu`.
**Do not weaken this gate** to add analytics to the portal "just for this
proposal" — confidential content must not phone home to third parties.

---

## 10. Sticky TOC sidebar is not actually sticky

**Symptom**: TOC scrolls with the page instead of sticking.

**Cause**: somewhere up the ancestor chain has `overflow: hidden`. Sticky
positioning fails inside any `overflow:hidden` container.

**Fix**: `app/globals.css` uses `overflow-x: clip` (not `hidden`) for the
horizontal-scroll guard. `clip` clips overflow without creating a containing
block, so sticky still works. **Don't change this back to `hidden`.**

---

## 11. SessionStorage cache shows stale content

**Symptom**: you re-encrypt the proposal with new content, reload — the user
sees the old content.

**Cause**: the cache key was just `${storageKey}` (e.g., `gbp:klapton`) — same
key across encryptions.

**Fix (already in place)**: cache key is `${storageKey}:${payload.iv.slice(0, 22)}`.
Each encryption uses a fresh random IV, so the cache key changes automatically.
The gate also purges any other keys starting with `${storageKey}:` on mount,
so stale caches don't accumulate.

---

## 12. Cloudflare serves stale `/portal/<client>/proposal` after deploy

**Symptom**: you deploy, but production still shows the old proposal.

**Cause**: Cloudflare edge cache. Firebase Hosting deploy doesn't purge CF.

**Fix**: always purge after deploy. The publish flow in `SKILL.md` has the
curl command. Forgetting this step has burned hours.

(Three cache layers, in order: CF edge → browser HTTP cache → per-tab
`sessionStorage` keyed by IV. The third clears itself; the second clears via
HTTP `Cache-Control: private, no-store` on `/portal/**` (set in `firebase.json`);
the first must be manually purged.)

---

## 13. `--no-edit` on `git rebase` is not a flag

Filed under "don't help future agents do this". `git rebase` has no `--no-edit`
option; the harness blocks `-i` (interactive) rebases anyway. If you need to
rebase, sequence commits manually or use `git rebase --continue` after each.

---

## 14. Don't sleep waiting for background tasks

If you ran `npm run dev` in the background, the harness notifies you when it
exits. Polling with `sleep 5 && check && sleep 5 && check…` wastes time and
context. The Monitor / background-process notification flow is built for this.

---

## 15. The Header/Footer hiding is per-component, not per-route

**Symptom**: a new shared component shows up on the proposal page when it
shouldn't.

**Cause**: there's no route-level "hide all chrome" rule. Each shared component
that should hide on `/portal/*` has its own pathname check:

```tsx
const pathname = usePathname();
if (pathname?.startsWith("/portal")) return null;
```

**Fix**: when you add a new shared component (CTA, banner, popover, anything
positioned), add the pathname check. Confidential content must not be visually
adjacent to marketing chrome.

---

## 16. Copying the gate / creating a per-proposal route (THE big one, 2026)

**Symptom**: to add a new proposal you `mkdir app/portal/<slug>/`, copy
`page.tsx` + `proposal-gate.tsx`, and tweak. Or you "edit the gate just for this
client."

**Cause**: old muscle memory. The system USED to work that way (a route + a
duplicated gate per proposal) and it caused exactly the drift this architecture
killed — a stale copy shipped broken comments on one client for weeks.

**Fix**: there is now **ONE gate** (`components/portal/ProposalGate.tsx`) and
**ONE shell** (`app/portal/view`) that serves every proposal via the
`/portal/*/proposal` rewrite. A new proposal is **data only**:

```bash
# write content/<slug>-proposal.html, add passphrase to portal-secrets.json
npm run publish-proposal -- <slug>     # live instantly, no route, no rebuild
```

Never create `app/portal/<slug>/`. Never copy the gate. For true per-client
styling (rare), use an inline `<style>` inside `content/<slug>-proposal.html` —
the divergence lives in the content, not the gate. To change the gate for
EVERYONE, edit `components/portal/ProposalGate.tsx` once and `npm run publish`
(full deploy). For a new Hebrew UI string, add both `en` and `he` to
`GATE_STRINGS` in the gate.

---

## 17. Forgetting to run the PDF render after a content change

**Symptom**: user reports the PDF download still shows old content.

**Cause**: the npm `prebuild` runs both `encrypt-proposal.mjs` and
`render-and-encrypt-pdf.mjs` — but if you encrypted manually (`node
scripts/encrypt-proposal.mjs`) you may have skipped the PDF render.

**Fix**: always run both, in order. Or just run `npm run build` and let the
prebuild handle it.

```bash
node scripts/encrypt-proposal.mjs <client>
node scripts/render-and-encrypt-pdf.mjs <client>
```

---

## 18. Don't trust an agent's summary — verify with the file

If a previous agent says "I deployed the fix", verify by running the actual
commands (`git status`, `git log`, `firebase hosting:releases:list`). The
summary is what the agent *intended*; the file system is what *happened*.

---

## 19. The build adds ~10 seconds for the PDF render

**Symptom**: `npm run build` feels slower than before.

**Cause**: the `prebuild` hook now also runs `render-and-encrypt-pdf.mjs`,
which spawns headless Chrome. Each client adds ~8-12 seconds.

**Fix**: it's expected. If you want a fast iteration loop while editing the
proposal CSS, run only the HTML encrypt: `npm run encrypt-proposals` (not
`build`). The screen view reflects CSS changes immediately via dev server; the
PDF only needs re-rendering before deploy or when you specifically test
download.

---

## 20. Production confirms 200/noindex — but the password is wrong

**Symptom**: client emails saying the password doesn't work.

**Cause**: either the passphrase you sent doesn't match `portal-secrets.json`,
or `portal-secrets.json` itself was updated after the last encryption.

**Fix**:
1. Re-run encryption: `node scripts/encrypt-proposal.mjs <client>`.
2. Verify by decrypting locally:
   ```bash
   PW='<the passphrase you sent>' node -e '
   const p=require("./app/portal/<client>/proposal/payload.json"),c=require("crypto");
   const k=c.pbkdf2Sync(process.env.PW,Buffer.from(p.salt,"base64"),p.iter,32,"sha256");
   const r=Buffer.from(p.ct,"base64");
   const d=c.createDecipheriv("aes-256-gcm",k,Buffer.from(p.iv,"base64"));
   d.setAuthTag(r.subarray(r.length-16));
   const pt=Buffer.concat([d.update(r.subarray(0,r.length-16)),d.final()]);
   console.log("OK, plaintext bytes:", pt.length);
   '
   ```
3. If that prints OK, the passphrase you have matches the deployed ciphertext.
   The client probably typed it wrong (autocorrect on iOS commonly capitalizes
   the first letter). Resend with explicit "lowercase k", or send via WhatsApp
   where it can be copy-pasted.

---

## 21. (Mostly obsolete) Uncommitted route files → clean deploy wipes them

**Historical**: under the OLD per-route architecture, a new proposal lived in
`app/portal/<client>/` + bundled payloads. If those weren't `git add`ed, the
next clean-checkout `firebase deploy` rebuilt from the git tree without your
client and **overwrote** the live site, 404ing the proposal (this took down MTC
for ~half a day).

**Why it (mostly) can't happen now**: Storage-served proposals have **no route
files and no bundled payloads**. The proposal lives in Firebase Storage +
Firestore (written by `publish-proposal.mjs`), which a site rebuild never
touches. A clean `npm run publish` deploys only the shell — it cannot wipe a
proposal. Just commit `content/<slug>-proposal.html` (+ any
`public/images/<slug>/`) so the source is recoverable.

**Still applies to the LEGACY proposals** (klapton, mtc) until they're migrated:
they keep route files under `app/portal/<slug>/` that must stay committed.

---

## 22. Firestore rules/indexes duplicated in `crm/` → one deploy overwrites the other

**Symptom**: the CRM proposals admin shows "No proposals yet" or
"Proposal not found" even though the docs exist in Firestore. Console
shows `permission-denied` reads. You're sure you deployed rules.

**Cause**: the main site (`/firebase.json`) and the CRM (`crm/firebase.json`)
used to each carry their own `firestore.rules` and `firestore.indexes.json`,
both deploying to the same `(default)` database. Whoever deployed last
won. A full main-site deploy would replace CRM-only rules (proposals,
proposal_secrets) with main-site rules that didn't know about those
collections.

**Fix**: **one canonical pair at the repo root only.**

```
/firestore.rules              ← canonical
/firestore.indexes.json       ← canonical
crm/firebase.json             ← has NO firestore section
```

Deploy from main site dir:

```bash
firebase deploy --only firestore:rules,firestore:indexes
```

If you ever find yourself adding `crm/firestore.rules` back — **don't.**
The Firebase CLI also rejects `../firestore.rules` relative paths from
subdirs ("outside project directory" error), so the consolidation has to
be one-way: main owns it.

If you need to add new rules for a CRM-only collection (e.g., a future
`crm_widgets/`), edit `/firestore.rules` at the repo root, then deploy
from the repo root.

---

## 23. Hosting rewrite to Gen 2 Cloud Function returns 404 after function redeploy

**Symptom**: `/t/proposal-open` (or any other `firebase.json` rewrite to
a function) returns 404 even though the function itself works via its
direct `*.run.app` URL. Stays broken until you redeploy hosting.

**Cause**: Firebase Hosting rewrites to Gen 2 functions pin to a specific
backing Cloud Run revision URL at *hosting deploy time*. When the
function is redeployed and a new revision is created, the hosting layer
keeps pointing at the now-outdated revision — but the revision is gone,
so the rewrite 404s. Gen 1 functions auto-tracked the latest revision;
Gen 2 doesn't.

**Fix**: after any `firebase deploy --only functions:funcName` for a
function that's behind a hosting rewrite, also run:

```bash
firebase deploy --only hosting
```

This refreshes the rewrite to point at the new revision. Cheap (no
content changes if `out/` hasn't moved), takes ~2 minutes.

Add this to your function-edit muscle memory: **edit function → deploy
function → deploy hosting → purge Cloudflare**. Skip the third step and
silent 404s eat your alerts.

---

## 24. Storing request IP behind Cloudflare is useless and breaks dedupe

**Symptom**: `portal_opens` rows all show `ip: "172.69.X.X"` (or similar
non-residential ranges). Dedupe lumps every CF-proxied visitor into one
bucket. Notifications either spam (when dedupe misses) or under-fire
(when two real visitors share the bucket).

**Cause**: behind Cloudflare, `req.ip` is the CF edge POP's IP, not the
visitor's. `x-forwarded-for` *should* contain the real client first but
isn't always present, and the leftmost-IP-is-client convention breaks
behind multi-hop proxies.

**Fix**: don't store IP at all for proposal opens. Identity comes from
the cookies the marketing site already sets on `globalbit.co.il`:

- **`gb_visitor`** — persistent 90-day visitor ID (set by
  `lib/visitor-tracker.ts`)
- **`gb_lead`** — `<leadDocId>|<YYYY-MM-DD>`, set when a lead is created
  via the contact form (`components/layout/Contact.tsx`)

The `trackProposalOpen` function reads both, resolves to a lead in
priority order (direct `gb_lead` → latest `visitor_session` for the
`gb_visitor`), and dedupes on `(client, visitor_id)`. Anonymous
visitors bucket as `visitor_id == "anon"` — coarse but rare in
practice (every real client has `gb_visitor` after their first
marketing-site visit).

If you ever need a real client IP for security analysis, use the
`CF-Connecting-IP` header — Cloudflare always sets it. Don't fall back
to `req.ip` or `x-forwarded-for`.

---

## 25. Firestore composite indexes need 1–10 min build time — silence ≠ failure

**Symptom**: you deployed a new composite index. The Firebase CLI says
"successfully deployed". But your queries that use it still return
"FAILED_PRECONDITION: The query requires an index. That index is
currently building and cannot be used yet."

**Cause**: `firebase deploy --only firestore:indexes` only **registers**
the index. Firestore then builds it asynchronously — on an empty
collection this is seconds, on a large one it can be minutes to hours.
During the build window, queries using the index fail.

**Fix**: don't conflate "deploy succeeded" with "queries work". Verify
the query works by actually trying it — the cheapest signal is to
trigger the query and check the target collection's doc count goes up
(if the query writes anything) or compare expected vs returned results.

```bash
# Poll until the query succeeds:
while true; do
  count=$(node -e '...query and print count...')
  if [ "$count" -gt "0" ]; then echo "index live"; break; fi
  sleep 30
done
```

---

## 26. Storage-served proposal renders "not found" in the browser but `curl` works

**Symptom**: `publish-proposal` succeeded, `curl` of `latest.html.json` returns
200, but the live page shows "Proposal not found" / stays on "Loading…".

**Cause**: the browser blocks the cross-origin fetch from `globalbit.co.il` to
`firebasestorage.googleapis.com` because the **bucket has no CORS policy** for
the origin. `curl` doesn't enforce CORS, so it lies to you.

**Fix**: the bucket CORS is already set, but if it's ever reset run
`node scripts/set-storage-cors.mjs` (allows GET from the globalbit origins).
Confirm: `curl -s -D - -o /dev/null -H "Origin: https://globalbit.co.il" "<storage-url>" | grep -i access-control-allow-origin`.

---

## 27. `publish-proposal` fails with "Application Default Credentials not found"

**Cause**: the script uses the Firebase Admin SDK to write Storage + Firestore;
it needs ADC.

**Fix**: `gcloud auth application-default login` once on the machine (or set
`GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json`). Same auth as
`record-deployment.mjs`.

---

## 28. Editing a proposal but it's a LEGACY (route-based) one

**Symptom**: you edit `content/<slug>-proposal.html`, run `publish-proposal`, but
the live page doesn't change.

**Cause**: klapton + mtc still have `app/portal/<slug>/proposal/` route files,
and a static file beats the shell rewrite — so the page serves the BUNDLED
payload, not your Storage upload. `publish-proposal` updated Storage, which the
route ignores.

**Fix**: for a legacy proposal, either (a) republish via the full `npm run
publish` (rebuilds the bundled payload), or (b) migrate it to the shell:
`publish-proposal -- <slug>` → delete `app/portal/<slug>/` → `npm run publish`.
Check whether a slug is legacy: `ls app/portal/<slug>/proposal/page.tsx`.

For functions that catch their own errors silently (like
`trackProposalOpen`'s outer `try/catch` around the dedupe query), the
HTTP response will be 200 even while the index is building — the
function logs are the only place you'll see "currently building". Tail
them with `firebase functions:log --only <funcName>` and grep for
"building" or "Error".

Don't add a new composite index right before declaring the feature done.
Build the index first (deploy + wait), THEN test.

---

If you hit a bug not in this list, **add it before moving on**. Future you
will thank present you.

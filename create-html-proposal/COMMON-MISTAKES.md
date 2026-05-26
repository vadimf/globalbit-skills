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
- Edit files at the parent project root (the path Next is actually serving), or
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

## 16. Editing the gate component "just for this client"

**Symptom**: you copy the klapton gate, then "tweak the CSS for the new client"
or add a special enhancement.

**Cause**: tempting because the gate is right there.

**Fix**: don't. The gate is shared across all clients by design. Any per-client
divergence guarantees future drift, broken PDF rendering (the render script
reads klapton's gate for CSS), and impossible-to-maintain proposals. If the
design needs to evolve, evolve it in the klapton gate and propagate to other
clients via copy/sync.

If you ever need true per-client styling (rare), do it via an inline `<style>`
inside the client's `content/<client>-proposal.html` file — that way the
divergence is in the content, not the gate.

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

If you hit a bug not in this list, **add it before moving on**. Future you
will thank present you.

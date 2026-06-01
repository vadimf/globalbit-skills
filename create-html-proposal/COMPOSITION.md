# How This Skill Composes With Other Proposal-Adjacent Skills

There are several proposal-related skills installed. They DON'T all do the same
thing — they compose into a pipeline. This doc tells you which one to invoke
when, and how the handoff works.

---

## TL;DR: the three-stage pipeline

```
┌────────────────────────────────────┐      ┌──────────────────────────────────────┐      ┌────────────────────────────────────┐
│  create-proposal                   │  →   │  create-html-proposal                │  →   │  CRM proposals admin (auto)        │
│  (anthropic-skills, global)        │      │  (this skill, in-repo)               │      │  (the system, no skill needed)     │
│                                    │      │                                      │      │                                    │
│  WHAT it owns:                     │      │  WHAT it owns:                       │      │  WHAT it owns:                     │
│  - Stakeholder analysis            │      │  - HTML fragment formatting          │      │  - List / detail / versions tab    │
│  - Service-type playbook selection │      │  - Encryption (HTML + PDF)           │      │  - Lead-picker linking             │
│  - Writing each section            │      │  - publish-proposal: encrypt →       │      │  - Encryption-aware PDF download   │
│    section-by-section with user    │      │    upload to Storage → register      │      │  - Opens tab + lead activity feed  │
│    review                          │      │    (data-only, NO route, NO rebuild) │      │  - Email/Telegram open alerts      │
│  - Bilingual EN/HE                 │      │  - Per-client passphrase             │      │  - Comments tab + alerts           │
│  - Boilerplate insertion           │      │  - Hand-off (URL + password)         │      │                                    │
│                                    │      │  - EN/HE gate i18n (auto RTL)        │      │  HOW it auto-syncs:                │
│  OUTPUT: a Google Doc OR markdown  │      │  - First-publish CRM registration    │      │  - `publish-proposal.mjs` writes   │
│                                    │      │                                      │      │    proposals/<slug> doc, deploy-   │
│                                    │      │  OUTPUT: a live encrypted page       │      │    ments subcoll, Storage payloads │
│                                    │      │  (one shell + Storage payloads)      │      │  - `trackProposalOpen` function    │
│                                    │      │  + downloadable encrypted PDF        │      │    writes portal_opens + lead      │
│                                    │      │  + Firestore record                  │      │    activity on each gate unlock    │
└────────────────────────────────────┘      └──────────────────────────────────────┘      └────────────────────────────────────┘
```

The CRM stage is **not a skill** — no separate prompt to invoke, no
sub-agent to run. It's the consumer side of what `create-html-proposal`
produces. Every deploy auto-registers in the CRM via the post-deploy
snapshot script; opens auto-log via the trackProposalOpen Cloud Function.
The skill's only responsibility wrt the CRM is **shaping the cover so the
parser picks up title/eyebrow/reference correctly** (see WRITING-GUIDE.md
"Cover page" — there's a parser-discipline subsection).

**Rule of thumb**:
- "Help me write a proposal" → **`create-proposal`** first.
- "Deploy this proposal to the client portal" → **`create-html-proposal`**.
- "Create AND deploy" → run them in sequence: write with `create-proposal`,
  then hand the output to `create-html-proposal`.

---

## Routing decisions — when to invoke which

| User says… | Trigger this skill | Why |
|---|---|---|
| "Write a proposal for `<client>` for `<service>`." | **`create-proposal`** | Content creation. They need the section-by-section workflow, playbooks, stakeholder analysis. Output is a Google Doc. |
| "Create a new proposal portal for `<client>`." | **`create-html-proposal`** | They already have or will provide the content; this skill is about the gated portal. |
| "Make a proposal for `<client>` and deploy it as a confidential web page." | **Both** (in order) | Use `create-proposal` for the content, then `create-html-proposal` to convert + deploy. |
| "Update the Klapton proposal — change the timeline." | **`create-html-proposal`** | Existing portal proposal. Edit `content/klapton-proposal.html`, republish. |
| "Add a new section to the proposal." | Depends on output format. Google Doc → `create-proposal`. Portal → `create-html-proposal`. |
| "Make a Hebrew version of the proposal." | **`create-proposal`** | Bilingual support is in `create-proposal`'s boilerplate files; the portal doesn't currently host RTL proposals (would need gate CSS work). |
| "Send me a PDF version of the proposal." | **`create-html-proposal`** | The portal already ships an encrypted PDF; the encrypted-PDF flow lives here. |

---

## The handoff: Google Doc / markdown → portal HTML fragment

When you go from `create-proposal` to `create-html-proposal`, you have content
in one of three formats:

1. **Google Doc** (the default `create-proposal` output)
2. **Markdown** (the fallback)
3. **Direct draft in chat** (rare but possible)

The portal needs a **raw HTML fragment** at `content/<client>-proposal.html`
with very specific section IDs and CSS classes (see `templates/proposal-skeleton.html`).
The handoff is a **format conversion**, not just a copy-paste.

### Conversion rules

| Source (markdown / GDoc) | Target (portal HTML) |
|---|---|
| `# Executive Summary` heading | `<section id="summary" class="wide"><div class="summary">…<h2 class="sec">Executive summary</h2>` |
| `## Background & Context` | `<section id="background"><div class="kicker">Background</div><h2 class="sec">Background &amp; Context</h2><div class="rule"></div>` |
| Bold lead "**1. Title** — body" inside Solution | `<div class="card"><h4>1. Title</h4><p>body</p><span class="impact"><b>Business impact — </b>…</span></div>` |
| Numbered list (Business / Project goals) | `<ol><li><strong>Goal Name</strong> — body</li></ol>` |
| "Phase 0: Discovery and specification…" | `<h3>Phase 0: Discovery and specification (N-M weeks)</h3><p>…</p>` |
| Risk table (markdown) | `<div class="tbl-scroll"><table>…<span class="risk med">12</span>…</table></div>` |
| Commercial 3-number band | `<div class="estimate"><div class="e">…</div>×3</div>` |
| Stats / awards / clients block in "About Globalbit" | Use `templates/about-globalbit.html` verbatim — **do not regenerate** |
| "Next Steps" boilerplate from `create-proposal` | `<section id="next">` AS LAST SECTION (after appendix). The portal puts CTAs last; `create-proposal` had them as #14. |
| "Client Commitment" + "General Terms" boilerplate | Merge under one `<section id="terms">` with `<h3>Client commitment</h3>` + `<h3>General terms</h3>`. |

**Section model mismatch** (important):

```
create-proposal             create-html-proposal
─────────────────────       ───────────────────────────
1.  Executive Summary   →   #summary
2.  Background          →   #background
3.  Business Goals      →   #business-goals
4.  Project Goals       →   #project-goals
5.  Proposed Solution   →   #solution
6.  About Globalbit     →   #about (paste templates/about-globalbit.html)
7.  Scope               →   #scope
8.  Methodology         →   #phases       ← rename: "Methodology & Approach" → "Project phases"
9.  Team Structure      →   #team
10. Timeline            →   #timeline
11. Risk Management     →   #risk
12. Added Value         →   #value
13. Commercial Terms    →   #commercial
14. Next Steps          →   #next         ← moved to LAST section (after #terms / appendix)
15. Client Commitment   ┐
16. General Terms       ┘   #terms        ← merged into one section
                       +    #appendix-architecture (optional, portal-only)
```

When the user has a Google Doc from `create-proposal` and wants it in the
portal, the agent's job is to:

1. **Read the doc** (via `globalbit-document` skill if needed for API access).
2. **Translate each section** following the mapping above.
3. **Write the converted fragment** to `content/<client>-proposal.html`.
4. **Apply portal-specific rendering** (anchor IDs, kicker labels, card
   structure, risk severity spans, etc.).
5. **Encrypt + render PDF + deploy** per the main `SKILL.md` steps.

---

## Adjacent skills that may help

These aren't proposal-specific but get invoked from within the pipeline:

| Skill | When invoked from the proposal pipeline |
|---|---|
| **`globalbit-document`** (anthropic-skills) | When `create-proposal` needs to write to / read from a Google Doc. The `create-proposal` SKILL.md already references it. |
| **`copywriting`** (anthropic-skills) | If a section feels weak and the user asks "improve this copy", invoke `copywriting` for the rewrite. Don't try to be a copywriter inline. |
| **`humanizer`** (anthropic-skills) | If the user says "this reads AI-generated, humanize it". Pass the specific section, not the whole proposal. |
| **`pdf`** (anthropic-skills) | Generic PDF ops (merging, splitting). Not needed for portal — the portal has its own encrypted PDF pipeline. Only invoke if the user has a **separate** PDF need. |
| **`docx`** (anthropic-skills) | If the user wants a Word version (rare — Google Doc is the default deliverable). |
| **`pptx`** (anthropic-skills) | If the user wants a deck instead of a proposal. Different deliverable; don't fold into the proposal flow. |
| **`brainstorming`** (anthropic-skills) | Pre-content phase. If the user is still figuring out *what* to propose (scope unclear, multiple paths), invoke this BEFORE `create-proposal`. |
| **`account-research`** / **`call-prep`** (sales:* family) | If the user needs deep prospect research before the proposal, run these first. `create-proposal` does light client research but isn't an OSINT tool. |

---

## What this skill does NOT do (route elsewhere)

- **Writing the content from scratch** → that's `create-proposal`. This skill
  assumes you have content and want to deploy it as a portal page.
- **Hebrew proposals** → `create-proposal` supports them via
  `boilerplate-sections-he.md`, but the portal CSS isn't RTL-tested. If the
  user wants a Hebrew portal page, raise the RTL work as a separate item.
- **Google Doc rendering** → `globalbit-document` owns the doc API.
- **PowerPoint / Word output** → `pptx` / `docx`.
- **Marketing landing pages** (public, indexed, no password) → that's a
  regular `app/` route, not the portal. Don't accidentally drop confidential
  content into `app/<page>/` thinking the gate will protect it.

---

## How to know which skill is running

Both skills are user-invocable. Triggers:

- **`create-proposal`**: any phrase matching "write/draft a proposal", "create
  a proposal" without portal context, "proposal for `<client>`", "I need a
  proposal" — anything that implies content creation.
- **`create-html-proposal`** (this one): phrases mentioning `/portal/`,
  "client portal", "password-protected proposal", "confidential web page",
  "encrypted proposal", "deploy the proposal", "the Klapton proposal", or any
  edits to `content/*-proposal.html` / `app/portal/*`.

If the user's request is ambiguous ("make a proposal for X"), **clarify the
output format** (Google Doc vs portal page) before committing to a skill.
They are not interchangeable — the workflow, output, and storage differ.

---

## Future-proofing: when to merge or split

These two skills will eventually be combined if:

- The portal becomes the only delivery format (no more Google Docs).
- The `create-proposal` workflow is rewritten to output HTML fragments directly.

Until then, **keep them separate**. Two narrow skills with clear handoff beat
one bloated skill that tries to do everything. The handoff cost is documented
above; the bloat cost would be paid in every invocation.

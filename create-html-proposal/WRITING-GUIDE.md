# How to Write Proposals That Don't Read as Walls of Text

The biggest single lesson from the Klapton proposal: **dense paragraphs lose
executive readers**. Even a brilliant technical proposal that reads as a wall
of text feels generic and unconvincing. Visual structure earns trust before a
single sentence is read.

This guide is the playbook. Follow it before "just writing in markdown" — the
on-screen experience is what closes deals, not the raw word count.

---

## The reader you're writing for

Two readers, simultaneously:

1. **The decision-maker** — skims the cover, exec summary, commercial estimate,
   maybe risks. Three minutes. Needs to feel: *"these people understand my
   problem and have done this before"*.
2. **The technical reviewer** — reads everything. Wants to see: *"the scope is
   well-defined, the architecture is sane, the team can deliver"*.

The proposal must serve both without compromising either. The cover + exec
summary + commercial + next steps form the decision-maker's read. The full
sections are the technical reviewer's. The "Executive / Full" mode toggle in
the live proposal is exactly this — but only works if the bullets and
business-impact lines are written tightly.

---

## The "wall of text" rule

If a section is 3+ paragraphs of plain `<p>` with no visual interruption,
**break it up**. Use:

- **Numbered cards** for solution components (`<div class="card"><h4>1. Title</h4>…`).
- **Pull-quotes** for business impact (`<span class="impact"><b>Business impact — </b>…`).
- **Tables** for any list of >3 parallel items (deliverables, risks, rates).
- **Stat blocks** for proof points (`<div class="stat"><div class="k">…</div><div class="v">…</div></div>`).
- **Blockquotes** for callouts (`<blockquote>Total timeline: ~4-6 months</blockquote>`).

A useful test: scroll the rendered page from top to bottom in 5 seconds. If
nothing visually anchors your eye except headings, the section needs structure.

---

## Section-by-section principles

### Cover page

- **One-line title** that *names the platform*, not the project. ("Klapton
  Reinsurance Trading Platform" — not "Reinsurance Marketplace Software
  Development Proposal").
- Reference like `GB-<YEAR>-<CLIENT-CODE>-001`.
- `<div class="confidential">Confidential</div>` at the end of cover-inner.
- Hero `bg-desktop.webp` background is automatic — leave it alone.

### Executive summary (`#summary` in dark `.summary` card)

The hardest 4 paragraphs to write in the whole proposal. The dark panel is
designed to be skim-friendly, and the executive-mode toggle uses these bullets
as the entire collapsed view.

**Structure**:

1. **Para 1** — what you are building, for whom, in plain English. No jargon.
2. **Para 2** — how you'll build it (one sentence per major capability, ~5
   capabilities max). This is where the project's substance lives.
3. **Para 3** — why Globalbit (one sentence: "Phoenix / Clal / Menora / IBI;
   200M users; 30 years"). Don't oversell — let the About section do the work.
4. **4 bullets** — the keystones of the project, in `<div class="bullet"><span>…</span></div>`:
   - The platform supports the full lifecycle from X to Y
   - Two algorithmic engines: distillation + optimization
   - Architecture designed for multi-jurisdiction compliance
   - Estimated investment of N-M ₪ over ~N-M months
5. **Para 4 (final)** — the de-risking statement ("Discovery phase produces
   complete spec before significant dev begins, protecting both parties").

### Background & Context (`#background`)

Three paragraphs:
1. Who the client is (one paragraph of context).
2. The current market state / pain.
3. Why the client's vision matters now (regulatory / market opportunity).

### Business Goals (`#business-goals`)

Numbered `<ol>` of **6 goals**, each as `<strong>Goal Name</strong> — body`.
Goals are *outcomes* (Accelerate Market Access, Establish Market Infrastructure
Leadership) not *features* (Build a marketplace, Add KYC). If you can replace
"Goal" with "Feature" in your sentence, rewrite it.

### Project Goals (`#project-goals`)

Numbered `<ol>` of **5 goals**, each as `<strong>Goal Name</strong> — body`.
These ARE concrete deliverables ("Deliver a Production-Ready Platform",
"Implement Intelligent Deal Processing"). The line between Business and Project
goals is: business goals are the client's; project goals are yours.

### Proposed Solution (`#solution`, `class="wide"`)

The longest section, and where structure matters most.

- Open with `<h3>Our approach: building <noun></h3>` + 2 paragraphs setting the
  technical worldview. ("A reinsurance trading platform is market
  infrastructure. Every design decision balances…").
- Then `<h3>Key components</h3>`.
- Each component is a **numbered card**:
  ```html
  <div class="card">
    <h4>1. Identity and organization management</h4>
    <p>…description, 1-2 paragraphs…</p>
    <span class="impact"><b>Business impact — </b>a verified participant network…</span>
  </div>
  ```
- Aim for **6-10 cards**. Fewer than 6 looks thin; more than 10 looks bloated.
- Every card MUST have a `.impact` pull-quote. This is the line the
  decision-maker reads.

### About Globalbit (`#about`)

**Use `templates/about-globalbit.html` verbatim.** Only swap the two tokens:
- `{{DOMAIN_FIT}}` — one sentence on why Globalbit fits *this client's domain*.
- `{{QUALITY_CONTEXT}}` — one paragraph naming relevant past clients.

Don't rewrite the awards, stats, or clients block. Those are vetted and the
client-logo grid is hardcoded.

### Scope and Deliverables (`#scope`)

A `<table>` with columns `# | Deliverable | Description`. 8-12 rows. No more.

(Old "In Scope / Out of Scope" lists were removed deliberately — they tend to
be either obvious or argument-fuel. Stick to deliverables.)

### Project Phases (`#phases`)

- 1 paragraph of opening framing.
- Phases as `<h3>Phase N: Name (N-M weeks)</h3>` + 1 paragraph each.
- Always include **Phase 0: Discovery and Specification** (4-8 weeks) — it's
  Globalbit's de-risking signature.
- Always include **UAT** and **Ongoing Support** phases at the end.
- Close with a `<blockquote><strong>Total estimated timeline: ~N-M months</strong></blockquote>`.

### Team Structure (`#team`)

A `<table>`: Role | Responsibility. 5-7 roles. Roles like:
- CTO / Technical Director
- Project Manager
- Senior Software Developer × 2-3
- UI/UX Designer
- DevOps Engineer
- QA Engineer

### Timeline and Effort (`#timeline`)

A `<table>`: Module | Estimated hours. End with a `class="total"` row.
Add a `<blockquote>` disclaimer ("Estimates refined after Discovery").

### Risk Management (`#risk`, `class="wide"`)

A `<table>` with columns: Risk | Sev | Prob | Level | Mitigation.
- `Sev` and `Prob` are integers 1-5.
- `Level = Sev × Prob`, displayed as `<span class="risk low|med|high">12</span>`.
  - `low` (1-6) = green
  - `med` (7-14) = amber
  - `high` (15-25) = red
- 6-8 risks. Each mitigation must be a concrete action, not a platitude.
- **Do not add a "severity/probability legend".** That was tried and removed.
  The colors speak for themselves.

### Added Value (`#value`, `class="wide"`)

A `.av` grid of 4-6 cards. Each card is a *non-deliverable* value-add:
ongoing maintenance options, internal training, IP transfer, knowledge transfer
sessions, code ownership.

### Commercial Terms (`#commercial`)

Three pieces:
1. **`.estimate` band** — three big numbers: investment range, effort hours,
   timeline. Uses the dark band CSS (`#commercial .estimate`). Never truncate
   the numbers.
2. **Hourly rates table** — copy from skeleton; rates don't change per client.
3. **"All prices exclude VAT."** — one bold line.

### Commitments & Terms (`#terms`)

- `<h3>Client commitment</h3>` + `<ul>` of what you need from the client
  (designated PM, timely feedback, content/data access, decisions within N days).
- `<h3>General terms</h3>` + `<ul>` of standard terms (proposal valid 30 days,
  IP transferred on payment, NDA available, etc.).

### Appendix · Architecture (`#appendix-architecture`, `class="wide appendix"`)

Optional but recommended. Goes between `#terms` and `#next`. Opens with a
caveat: *"a starting point for discussion, not a final design — the definitive
architecture is produced during Discovery."*

Use the `arch-layer`, `flow`, `ent-grid`, `stack`, `pipeline` classes already
in the gate CSS. Never embed Mermaid, draw.io, or any external diagram (CSP
blocks them and they break PDF rendering). Render diagrams as native HTML.

The appendix is **collapsed by default in screen view** (a "Show appendix ↓"
link reveals it), and **always fully expanded in the PDF**.

### Next Steps (`#next`)

The **last section of the proposal**, after appendix. A numbered `<ol>` with
4-6 items. Each item is a concrete next action with an owner:

```html
<li><strong>Sign-off on this proposal</strong> — review and approve, or send
feedback. Globalbit holds capacity for 14 days from the date of issuance.</li>
<li><strong>Kickoff meeting</strong> — 90-minute working session …</li>
```

---

## Tone, voice, and language

- **Direct, confident, declarative.** "The platform supports…" not "We can build
  a platform that may support…".
- **Specific over generic.** "ACORD-aligned data structures" beats "industry-
  standard data formats". Name standards, name regulators, name competing
  approaches.
- **No marketing fluff.** No "leveraging cutting-edge synergies". No
  "best-in-class". No "world-class". The proposal has to be defensible to the
  client's CTO.
- **British or American English — pick and be consistent** (the rest of the
  Globalbit site is American English; default to that).
- **"Globalbit", not "we"** in the About section; "we" is fine elsewhere.
- **Numbers**: use real numbers, not ranges where you can avoid it. "~400,000
  ILS" beats "around 400k ILS"; "4-6 months" is fine because the range is real.

---

## Visual rhythm checklist (before deploy)

Open the rendered proposal in a browser. Scroll top to bottom. Check:

- [ ] Cover has hero background, "Confidential" marker, real client name + reference.
- [ ] Exec summary is the dark panel, scrollable in <3 seconds, with 4 bullets.
- [ ] Background, Business Goals, Project Goals fit on 2-3 pages each.
- [ ] Solution has 6-10 numbered cards, each with `.impact` pull-quote.
- [ ] About Globalbit shows colored client logos and the peach awards block.
- [ ] Scope is a table.
- [ ] Phases section has clear `<h3>Phase N: …</h3>` headings.
- [ ] Team is a table.
- [ ] Timeline is a table ending with a `.total` row.
- [ ] Risk table uses the colored severity spans.
- [ ] Commercial estimate uses the dark `.estimate` band.
- [ ] Terms is short and to the point.
- [ ] Appendix is collapsed by default; "Show appendix ↓" works.
- [ ] Next Steps is the last section, numbered, action-oriented.
- [ ] Download PDF works in <1 second; the PDF has all appendix content fully
      expanded.

If any of those fail, fix the content — don't patch the CSS per client.

---

## Anti-patterns (don't do these)

- ❌ Embedding Mermaid or any CDN-loaded diagram library. CSP blocks them.
- ❌ Per-client CSS overrides. The CSS is shared across every client by design.
- ❌ Hardcoded chapter numbers ("01 Background"). The CSS counter does it.
- ❌ Long blockquotes used as paragraphs. Blockquotes are for short callouts.
- ❌ Tables for layout. Use `.av`, `.stats-grid`, `.ent-grid` grids instead.
- ❌ Mixing English and Hebrew in the proposal body. Pick one (default English).
- ❌ Headlines like "Awesome Tech Solution". Headlines are descriptive nouns.
- ❌ Promising things the contract won't promise (security guarantees, uptime SLAs,
  fixed-price scope changes). Discovery and Terms are where guarantees live.

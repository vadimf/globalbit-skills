# START HERE — writing a Globalbit proposal end to end

This is the reading order. Two skills compose into one pipeline:

```
create-proposal  →  create-html-proposal  →  live encrypted portal
(shape content)     (HTML + publish, data-only)   (no route, no rebuild)
```

`create-proposal` lives here (globalbit-skills). `create-html-proposal` lives in
the Globalbit website repo at `.agents/skills/create-html-proposal/`.

---

## Stage 1 — Shape the content (this skill)

1. **`SKILL.md`** — master workflow: stakeholder analysis, the section model,
   section-by-section review with the user, EN/HE, output choice (Google Doc vs
   encrypted portal), and the handoff to `create-html-proposal`.
2. **`playbooks/<service>.md`** — read the ONE that matches the deal:
   `software-development`, `qa-automation`, `uiux-design`, `team-augmentation`,
   `specification-discovery`, `performance-analysis`, `maintenance-support`.
3. **`resources/`** — the building blocks. Don't invent facts or numbers:
   - `company-profile.md`, `hourly-rates.md` — facts + rates
   - `section-guides.md`, `tone-guide.md` — how each section should read
   - `boilerplate-sections-en.md` / `boilerplate-sections-he.md` — reusable
     terms/about blocks (pick by language)
   - `security-compliance-annex.md` — for regulated/financial clients
   - `learnings.md` — accumulated do/don't

---

## Stage 2 — Convert to the portal HTML and publish (`create-html-proposal`)

> **Architecture (2026):** ONE shared gate (`components/portal/ProposalGate.tsx`)
> + ONE shell route (`app/portal/view`) serve EVERY proposal. A proposal is pure
> DATA. **NEVER copy the gate or create a per-proposal route.**

4. **`create-html-proposal/SKILL.md`** — the lifecycle: write
   `content/<slug>-proposal.html` → add passphrase to `portal-secrets.json` →
   `npm run publish-proposal -- <slug>` (encrypt → upload to Firebase Storage →
   register). **Live instantly, no route file, no site rebuild.**
5. **`create-html-proposal/WRITING-GUIDE.md`** — how to format each section as
   HTML so it isn't a wall of text.
6. **`create-html-proposal/COMPOSITION.md`** — the handoff details + the
   §(Google Doc) → #(portal section) mapping.
7. **`create-html-proposal/COMMON-MISTAKES.md`** — gotchas. Especially **#16**
   (never copy the gate / make a route), **#26** (Storage CORS), **#27** (ADC
   for publish-proposal), **#28** (editing a legacy route-based proposal).
8. **`create-html-proposal/templates/`** — `proposal-skeleton.html` (start here)
   + `about-globalbit.html` (paste-in block).

---

## Stage 3 — Reference examples & facts (Globalbit website repo)

9. **`content/klapton-proposal.html`** — canonical **English** content example
   (structure, section IDs, classes).
10. **`content/kablan-chacham-proposal.html`** — canonical **Hebrew / RTL**
    example. Copy its top inline `<style>` block for any Hebrew proposal — the
    gate auto-detects RTL and switches its own UI (mode toggle, comments, etc.)
    to Hebrew via `GATE_STRINGS.he`.
11. **`docs/SALES_MARKETING_KB.md`** — Globalbit facts, clients, stats, awards,
    testimonials — source of truth for the About / credibility content.

---

## Minimal fast path

`SKILL.md` → matching **playbook** → `create-html-proposal/SKILL.md` → the right
**content example** (klapton = EN, kablan-chacham = HE) →
`npm run publish-proposal -- <slug>`.

## Adjacent skills (only if the deliverable is NOT the portal)

- **`globalbit-document`** — produce a styled Google Doc instead of the portal.
- **`copywriting`** — conversion copy for headlines/CTAs.

# Section Writing Guides

> **Usage**: When composing a proposal section-by-section, use the guide for the current section. Each guide defines what inputs are needed, the expected structure, rules, and a quality gate.

---

## Section 1: Executive Summary

> ⚠️ **Write this section LAST** — after all other sections are complete.

### Inputs

- All completed sections (2–16)

### Structure

- 1 page maximum
- **Paragraph 1**: Client context + challenge + what Globalbit proposes (2-3 sentences)
- **Paragraph 2**: Solution philosophy — what makes this more than a technical project ("Revenue Engine", "Growth Platform", etc.) + key capability highlights (2-3 sentences)
- **Paragraph 3**: 3-4 takeaway bullets (●) summarizing: (1) what we build, (2) key capability, (3) methodology/timeline, (4) strategic outcome
- **Closing sentence**: Vision — long-term value and stability ("a digital infrastructure that will serve the organization for years to come")

> ⚠️ **NO TABLE** in the executive summary. Budget and timeline appear as inline text within bullets or the closing paragraph. Hours do NOT appear at all.

### Rules

- Written for the **Decision Maker** — strategic, ROI-focused, concise
- Budget/timeline: inline text ("~3 months", "269,200 ₪"), never a table
- End with a confidence/vision statement, not numbers
- Use only power phrases from the tone guide
- Every claim must be backed by content from subsequent sections

### Quality Gate

- [ ] Fits on 1 page
- [ ] Mentions client by name
- [ ] States the problem clearly
- [ ] Ends with 3-4 takeaway bullets
- [ ] Budget/timeline as inline text (NO table)
- [ ] Ends with vision/confidence sentence
- [ ] Uses zero weak phrases

---

## Section 2: Background & Context

### Inputs

- Client name, industry, project description
- Internet research (validated with user)
- Meeting notes, RFPs, or briefs (if available)

### Writing Process

#### Step 2a: Client Research

1. Search the internet for the client company — website, LinkedIn, Crunchbase, recent news
2. **IMPORTANT**: The same company name may belong to different entities. Present your findings to the user and ask: *"Is this the correct company?"* Do NOT proceed until confirmed.
3. Capture: company size, industry, market position, tech stack, funding, key people, recent news

#### Step 2b: Problem / Need

- What is the client's current situation?
- What challenges or pain points do they face?
- Why is the status quo no longer acceptable?

#### Step 2c: Anticipated Results

- What results does the client expect from this project?
- What measurable improvements will this deliver?
- What is the risk of inaction?

### Structure

```
{{Client business description — who they are, market position, industry context}}

{{Current situation — what exists today, what challenges they face}}

{{Anticipated results — what success looks like, what this project will unlock}}
```

### Rules

- Show deep understanding of the client's world — use their terminology
- Reference specific challenges from research/meetings
- Position the project as strategically important, not just a task
- Never guess about the client — validate with user

### Quality Gate

- [ ] Client research validated with user
- [ ] Client described in their own industry language
- [ ] Problem is concrete, not generic
- [ ] Anticipated results are specific and measurable
- [ ] Strategic importance is clear

---

## Section 3: Business Goals

### Inputs

- Background section (completed)
- Client meetings, RFP, project brief

### Purpose

Articulate what the **business** achieves as a result of this project. These are outcomes at the organizational level — revenue, efficiency, market position, compliance — not technical deliverables.

### Structure

Present as 3–6 numbered goals, each with a brief explanation:

```
1. **{{Goal Name}}** — {{1-2 sentence explanation of how this project achieves this goal}}
2. **{{Goal Name}}** — {{explanation}}
...
```

### Rules

- Think from the CEO's perspective: "What does this mean for our business?"
- Each goal should connect to a measurable business metric where possible
- Use the value translation rule: technical → business outcome
- Goals should be distinct — no overlap

### Examples

- "Reduce operational costs by automating manual reporting workflows"
- "Achieve regulatory compliance (SOC 2, ISO 27001) to unlock enterprise sales"
- "Increase customer retention through improved digital experience"
- "Enable data-driven decision making with real-time analytics"

### Quality Gate

- [ ] 3–6 distinct goals
- [ ] Each goal is a business outcome, not a technical task
- [ ] Goals connect to measurable metrics
- [ ] No overlap between goals

---

## Section 4: Project Goals

### Inputs

- Background section + Business Goals section (completed)
- Project description, service type

### Purpose

Define what the **project itself** aims to achieve — these are the goals of the engagement, not the product. Think: "What does this project deliver? What are its success criteria?"

### Structure

Present as 3–6 numbered goals:

```
1. **{{Goal Name}}** — {{1-2 sentence description}}
2. **{{Goal Name}}** — {{description}}
...
```

### Rules

- These are about the project (engagement), not the product
- Think: scope, quality, process, handover, knowledge transfer
- Each goal should be verifiable — you can check if it was achieved
- Align with the methodology (Agile, sprints, iterative delivery)

### Examples

- "Deliver a production-ready platform within 16 weeks"
- "Establish a CI/CD pipeline enabling weekly releases by Sprint 3"
- "Complete full knowledge transfer to the client's internal team"
- "Achieve 90%+ automated test coverage across critical user journeys"
- "Provide SOC 2-aligned security documentation"

### Quality Gate

- [ ] 3–6 distinct goals
- [ ] Goals are about the project/engagement, not the product
- [ ] Each goal is verifiable
- [ ] Goals are realistic and time-bound where applicable

---

## Section 5: Proposed Solution

### Inputs

- Background, Business Goals, Project Goals (completed)
- Service playbook (`playbooks/{{SERVICE_TYPE}}.md`)
- Project description, technical requirements

### Structure

```
### Our Approach — {{Strategic Framing}}
{{1-2 paragraphs explaining Globalbit's philosophy for this project.
  E.g., "Revenue Engine", "Growth Platform", "AI-First Architecture".
  Why this is more than a technical project — what business value the approach unlocks.}}

### Key Components

1. {{Component Name}}
{{Narrative paragraph: what it is, why it matters, how it works.
  End with: "The business impact: {{one sentence}}"}}

2. {{Component Name}}
{{Narrative paragraph ending with business impact}}

...
```

> ⚠️ **NO What/Why/Deliverable bullet format.** Components are narrative paragraphs. Deliverables go in the Deliverables table (Section 7 or Section 8).

### Rules

- **Open with "Our Approach" / "הגישה שלנו"** — strategic framing before any components
- Each component is a **narrative paragraph** (not bullet lists)
- Every component ends with **"The business impact:" / "המשמעות העסקית:"** — one sentence
- Use business language, not technical jargon ("channel the visitor arrived from" not "UTM Parameters")
- Use exec-level vocabulary: "Revenue Engine", "Revenue Operations", "Agentic AI"
- Technology choices embedded naturally in the narrative, justified with business reasoning
- Include QA as a component ("Quality Assurance & Testing") with the 4-layer approach
- Number of components depends on project complexity (typically 4–8)

### Quality Gate

- [ ] Opens with "Our Approach" strategic sub-section
- [ ] Each component is a narrative paragraph (not bullet lists)
- [ ] Each component ends with a business impact statement
- [ ] No technical jargon without business translation
- [ ] QA included as a solution component
- [ ] Components cover the full solution without gaps

---

## Section 6: About Globalbit

### Inputs

- `resources/company-profile.md`
- Client context (industry, type) from Background
- Stakeholder analysis (Decision Maker + Recipient) from SKILL.md
- Adaptation rules from SKILL.md

### Structure

```
### Who We Are
{{Adapted company profile — 1-2 paragraphs based on client context}}

### Why Globalbit for This Project
{{5-7 project-specific bullets, including:
  - 2+ bullets for the Decision Maker (industry experience, CTO oversight, track record)
  - 2+ bullets for the Recipient (understands their domain, easy collaboration, self-service)
  - 1 bullet on E2E responsibility
  - 1 bullet on long-term partnership}}

### Clients & Recognition (optional)
{{Logos, awards, social proof — if high-impact}}
```

### Context Adaptation

| Context | Lead With |
|---------|-----------|
| B2C / Consumer | "200M+ users", app store awards, UX excellence |
| Enterprise | Enterprise clients, system complexity, regulatory experience |
| Fintech | Financial clients, compliance, security-first |
| Healthcare | Healthcare clients, compliance, accessibility |
| Startup | "0 to scale" experience, Agile, speed to market |
| Defense / Government | Government clients, essential facility, security DNA |

### Rules

- Always include: "Over 200 million people worldwide use digital products built by Globalbit"
- **"Why Globalbit for THIS project"** — must be specific to this engagement, not generic
- Include at least 2 bullets that speak to the **Recipient** (e.g., "partner who understands marketing, not just development", "comfortable and efficient collaboration for your team")
- Include at least 2 bullets for the **Decision Maker** (e.g., "industry experience", "CTO oversight")
- Highlight relevant client portfolio from the same industry
- Mention AI-First positioning if relevant
- Keep to approximately 1 page

### Competitive Positioning (Implicit — Never Name Competitors)

> The Israeli enterprise buyer is mentally comparing Globalbit against Matrix, Ness, Malam-Team, Aman, Comm-IT, Tikal, Naya, and others — even if no one says it out loud. The "Why Globalbit" bullets must **preempt that comparison** without naming names. Every bullet implicitly defeats one type of competitor.

Use the Implicit Positioning Lever Table to choose 3-4 levers per proposal (the ones that matter most to this client's persona):

| Competitor archetype the buyer is mentally comparing | Implicit lever that defeats it (use as a "Why Globalbit" bullet) |
|---|---|
| Big body-shops (hundreds of consultants, layered account managers) | "**Senior-only team with no junior dilution**" — every developer assigned has 5+ years in the discipline; no "training on your account" |
| Big body-shops with offshore delivery | "**100% Israel-based delivery**" — every developer works from Israel, in your timezone, in Hebrew when needed |
| Big body-shops with account-management layer | "**Direct CEO/CTO involvement**" — Sasha Feldman is personally accountable. No "I'll have to check with the team" |
| Slow-moving consultancies (3-month spec phases, no working code) | "**Working software in weeks, not months**" — sprint demos every 2 weeks, you see real progress from week 2 |
| Boutique freelancer collectives | "**Full E2E ownership**" — one contract, one accountable party, one continuous team from spec through maintenance |
| Cheap commodity providers | "**Premium quality, measured outcomes**" — products serving 200M+ users, not a CV factory |
| AI-curious general dev shops | "**AI-First with production track record**" — RAG systems, AI agents, and Generative AI deployed in regulated environments — not "we can also do AI" |
| Vendors with vague exit terms | "**No vendor lock-in, ever**" — full source code ownership, documented exit plan, knowledge transfer included |
| Foreign vendors / non-Israeli houses | "**Native Israeli regulatory fluency**" — we know 357, נב"ת, רשות שוק ההון, חוק הגנת הפרטיות 2024, accessibility standards — without ramp-up |

**Implementation rule:** Pick 3-4 levers most relevant to the client's archetype. Phrase each as a confident bullet under "Why Globalbit for This Project". Never name a competitor. Never write "unlike X, we...". The buyer fills in the blank.

### Quality Gate

- [ ] Profile is adapted to client context (not generic)
- [ ] "200M+ users" fact included
- [ ] "Why Globalbit for THIS project" is project-specific (not boilerplate)
- [ ] At least 2 Recipient-facing bullets in "Why Us"
- [ ] At least 2 Decision-Maker-facing bullets in "Why Us"
- [ ] Relevant industry clients highlighted

---

## Section 7: Project Scope & Deliverables

### Inputs

- Proposed Solution section (completed)
- Playbook typical deliverables

### Structure

```
### In Scope
{{Numbered list of what is included}}

### Out of Scope (if relevant)
{{What is explicitly excluded}}

### Deliverables
| # | Deliverable | Description |
|---|------------|-------------|
| 1 | {{NAME}} | {{DESCRIPTION}} |
```

### Rules

- In Scope items should map back to solution components
- Out of Scope should preempt common assumptions
- Deliverables must be tangible — apply deliverable language rules from tone guide
- Number deliverables — makes it easy to reference in conversations

### Quality Gate

- [ ] Every solution component has matching scope items
- [ ] Out of Scope addresses likely assumptions
- [ ] Deliverables are specific, not vague
- [ ] Deliverables table is complete

---

## Section 8: Project Phases & Methodology

### Inputs

- Service playbook methodology section
- Proposed Solution components
- Project type

### Structure

```
### Project Phases

| Phase | Duration | Key Activities |
|-------|----------|---------------|
| Phase 0: Discovery | X weeks | ... |
| Phase 1: Design | X weeks | ... |
| Phase 2: Development | X weeks (N sprints) | ... |
| Phase 3: Launch | X weeks | ... |

{{1-2 sentences per phase describing what happens, what the client sees, and what they approve.}}

### Quality Assurance

Globalbit applies a multi-layered QA process:
- **Continuous testing** — developers run unit and integration tests as part of daily work
- **Sprint testing** — dedicated QA cycle at the end of each sprint
- **Regression testing** — full regression before every release
- **User acceptance testing (UAT)** — client verification before production deployment
```

> ⚠️ **NO Agile ceremony names.** Do not list Sprint Planning, Daily Standups, Sprint Retrospectives, or Definition of Done. The client is not managing a dev team. Mention "2-week sprints" and "live demo at the end of each sprint" once, then describe phases by activities and deliverables.

### Rules

- Describe phases by **activities and client touchpoints**, not Agile ceremonies
- Mention "2-week sprints with a live demo" once in the overview — that's sufficient
- QA = detailed 4-layer sub-section (signals professionalism)
- Include "up to 2 review rounds" in the launch phase to set client expectations
- Phase approach must align with Proposed Solution components

### Quality Gate

- [ ] Zero Agile ceremony names (no Sprint Planning, DoD, etc.)
- [ ] Phases described by activities and deliverables
- [ ] QA has 4 layers explicitly listed
- [ ] "2-week sprints" mentioned exactly once
- [ ] Client review rounds specified in launch phase

---

## Section 9: Team Structure

### Inputs

- `resources/hourly-rates.md` — team compositions by service type
- Proposed Solution — what skills are needed
- Project scope
- Named Team availability (ask the user for actual senior names if deal > 200K)

### Structure (Default — Anonymous Roles)

```
| Role | Responsibility |
|------|---------------|
| {{ROLE}} | {{RESPONSIBILITY}} |
```

### Structure (Enhanced — Named Team, for deals > 200K NIS)

For mid-large enterprise deals, replace the anonymous role table with a named team table:

```
| Role | Name | Allocation | Background |
|------|------|------------|-----------|
| Tech Lead | מאיר כהן (Meir Cohen) | Dedicated 80% | 12 yrs full-stack, ex-IBI lead, LinkedIn: ... |
| Senior Engineer | ... | Dedicated 100% | ... |
| CTO Oversight | סשה פלדמן (Sasha Feldman) | 4-6 hrs/week | CEO/CTO of Globalbit |
```

Add the following commitment paragraph beneath the table:

**Hebrew:**
> "אנשי הצוות הליבתיים המופיעים לעיל מוקצים לפרויקט זה ישירות. גלובלביט לא תחליף איש צוות ליבתי במהלך הפרויקט ללא אישור מראש מהלקוח. במקרה של עזיבת עובד או היעדרות ממושכת, גלובלביט תספק החלפה ברמה שווה או גבוהה יותר תוך 5 ימי עבודה."

**English:**
> "The core team members listed above are directly assigned to this project. Globalbit will not replace a core team member without prior client approval. In case of departure or extended absence, an equal or higher caliber replacement will be provided within 5 business days."

### Rules

- Include only roles relevant to this project
- Responsibilities should be project-specific, not generic
- Use team compositions from hourly-rates.md as a starting point
- **For deals > 200K NIS**: ask the user for actual names (Tech Lead minimum) and use the Named Team structure. Anonymous "Senior Developer" reads as a body shop. Named team with allocation % reads as a partnership.
- LinkedIn references are powerful but only include them if the team member has consented (default: ask the user)
- Do NOT name junior roles — only senior, lead, and oversight roles get names
- The "no-swap without approval" commitment must accompany any named team

### Quality Gate

- [ ] All required skills for the solution are covered
- [ ] Responsibilities are specific to this project
- [ ] Rates exist for all roles in hourly-rates.md
- [ ] For deals > 200K: at least the Tech Lead is named, with allocation % shown
- [ ] Named team is accompanied by the no-swap commitment paragraph

---

## Section 10: Timeline & Milestones

### Inputs

- Proposed Solution, Scope, Team Structure (completed)
- Playbook phase structure

### Structure

```
### Phase Overview
| Phase | Duration | Key Activities |
|-------|----------|---------------|
| {{PHASE}} | {{WEEKS}} | {{ACTIVITIES}} |

### Effort Estimation
| Activity | Estimated Hours |
|----------|:-:|
| {{ACTIVITY}} | {{HOURS}} |
| **Total** | **{{TOTAL}}** |
```

### Rules

- Phases should align with the Proposed Solution components
- Include Project Management hours (typically 15–20% of total)
- Always include the commercial disclaimer from hourly-rates.md
- Hours must be defensible — tie back to scope items

### Quality Gate

- [ ] Phases match solution components
- [ ] Effort total is realistic
- [ ] PM hours included
- [ ] Commercial disclaimer included

---

## Section 11: Risk Management

### Inputs

- `resources/boilerplate-sections-{en|he}.md` — risk template
- Playbook-specific risks
- Project context

### Structure

Use the boilerplate risk assessment template (Severity × Probability matrix) but fill with project-specific risks.

### Rules

- Present proactively — risk management is a STRENGTH
- Use severity × probability matrix (1-5 scale)
- Every risk must have a mitigation plan
- Include 5–8 project-specific risks
- Include scales and risk level formula from boilerplate

### Quality Gate

- [ ] 5–8 project-specific risks
- [ ] Every risk has a mitigation
- [ ] Severity/probability scales included
- [ ] Risks are relevant to this specific project

---

## Section 12: Added Value

### Inputs

- `resources/company-profile.md` → Standard Value Propositions
- Client context
- Stakeholder analysis (Decision Maker + Recipient)

### Structure

5–7 items in **headline + mini-explanation** format:

```
● **{{Bold Headline}}** —
{{1-2 sentence explanation}}

● **{{Bold Headline}}** —
{{1-2 sentence explanation}}
```

> The CEO reads only the headlines. If the headlines alone communicate the value, the section works.

### Rules

- **Headline must stand alone** — if the CEO reads only bold headlines, he gets the full picture
- Mini-explanation = 1-2 sentences max, not a long bullet
- Select from standard value propositions, adapt to project context
- Include "Strategic project" designation for high-value deals (>500K NIS)
- Include AI-First if the project involves AI
- At least 1 item must reference the **Revenue Engine / Growth** angle (if applicable)
- Every item should answer: "Why should the client choose Globalbit over alternatives?"

### Quality Gate

- [ ] 5–7 distinct value items
- [ ] Each item: bold headline + 1-2 sentence explanation (not long bullets)
- [ ] Headlines stand alone — CEO reads only these and understands
- [ ] Adapted to project context (not copy-paste)
- [ ] Strategic project designation if applicable
- [ ] Every item answers "why Globalbit?"

---

## Section 13: Commercial Terms

### Inputs

- `resources/hourly-rates.md`
- Timeline & Milestones (effort hours)
- Team Structure (roles and rates)

### Structure

```
### Engagement Model
{{T&M / Fixed Price / Retainer — description}}

### Project Estimate
**Total estimate**: {{AMOUNT}} ₪
**Estimated timeframe**: {{TIMEFRAME}}
**Estimated hours**: ~{{HOURS}} hours

### Hourly Rates
| Role | Hourly Rate (ILS) |
|------|:-:|
| {{ROLE}} | {{RATE}} ₪ |

### Payment Terms
{{From boilerplate — matching the engagement model}}

### Assumptions
{{Key assumptions that affect the estimate}}
```

### Rules

- Default to T&M unless project clearly fits fixed price
- Include only roles used in this project's team structure
- Always add "All prices exclude VAT"
- Always include commercial disclaimer
- Always include assumptions — these protect both parties
- Never present rates apologetically

### Quality Gate

- [ ] Model matches project type
- [ ] Rates match hourly-rates.md
- [ ] Total estimate aligns with effort hours × rates
- [ ] Payment terms included
- [ ] Assumptions are specific and complete
- [ ] Commercial disclaimer included

---

## Sections 14–16: Boilerplate (Auto-Insert)

### Section 14: Next Steps

- Source: `resources/boilerplate-sections-{en|he}.md` → Next Steps
- Replace `{{CLIENT_NAME}}` with actual client name
- No other modifications

### Section 15: Client Commitment

- Source: `resources/boilerplate-sections-{en|he}.md` → Client Commitment
- Insert **verbatim** — no modifications

### Section 16: General Terms

- Source: `resources/boilerplate-sections-{en|he}.md` → General Terms
- Insert **verbatim** — no modifications

---

## Optional Sections (Insert When Triggered)

### Performance Commitments & SLA

- Source: `resources/boilerplate-sections-{en|he}.md` → Performance Commitments & SLA
- **Trigger**: Deal value > NIS 200K, mid-large enterprise client, or any explicit client question about SLA / continuity / IP
- Insert immediately before Commercial Terms (Section 13) or as a sub-section within Commercial Terms

### Appendix A: Security & Compliance

- Source: `resources/security-compliance-annex.md` (HE or EN per language)
- **Trigger**: ANY enterprise client (banking, insurance, healthcare, government, regulated industries) OR any deal > NIS 200K
- Insert as the LAST appendix, after General Terms, before signatures
- Title in HE: "נספח א׳ - אבטחת מידע ותאימות רגולטורית"
- Title in EN: "Appendix A - Information Security & Regulatory Compliance"
- Customize the regulatory bullet list to the client's specific sector — remove non-applicable rows

---

## One-Page Executive Brief (Companion Document)

> For deals > NIS 500K, generate a separate one-page brief alongside the full proposal.

### When to produce

- Deal value > NIS 500K
- Multi-stakeholder buying committee (CEO + CFO + CIO involved)
- Recipient asks for "something to forward to the CEO"

### Structure (single page only)

```
HEADER: Project name + one-sentence goal
"AI Knowledge Hub for Menora Mivtachim Investment Division - replacing scattered file storage with a queryable knowledge platform that reduces analyst search time by 60-80%."

COMMERCIAL SNAPSHOT (3 lines):
- Total: NIS XXX,XXX (T&M, Net + 45)
- Timeline: X weeks
- Effort: ~XXX hours

KEY MILESTONES (3-4 bullets):
- Week 1: Discovery + Azure infrastructure
- Weeks 2-3: Core development (RAG + chat UI)
- Week 4: QA, security hardening, go-live

WHY GLOBALBIT (3 bullets, the strongest from the full proposal):
- Bullet 1
- Bullet 2
- Bullet 3

NEXT STEP: Single-line CTA
"We propose a 30-minute alignment call to confirm scope. Available [day]/[day] this week."
```

### Output format

- Same Globalbit-branded Google Doc template
- Title: "[Project Name] - Executive Brief"
- File ID format: `GB-2026-XXXX-001-BRIEF`
- Stays as a single page, even if it requires tighter language

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

> ⚠️ **NO What/Why/Deliverable bullet format.** Components are narrative paragraphs. Deliverables go in the Deliverables table (§7 or §8).

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

### Structure

```
| Role | Responsibility |
|------|---------------|
| {{ROLE}} | {{RESPONSIBILITY}} |
```

### Rules

- Include only roles relevant to this project
- Responsibilities should be project-specific, not generic
- Use team compositions from hourly-rates.md as a starting point
- Name team members only if assigned

### Quality Gate

- [ ] All required skills for the solution are covered
- [ ] Responsibilities are specific to this project
- [ ] Rates exist for all roles in hourly-rates.md

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

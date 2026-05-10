---
name: product-planner
description: >
  End-to-end product planning — from discovery interview through PRD authoring to phased
  implementation plans. Replaces prd, write-a-prd, breakdown-feature-prd, and prd-to-plan
  with a single, mode-aware skill. Supports full lifecycle, standalone PRD, epic breakdown,
  and plan-only workflows.
---

# Product Planner

Create production-grade Product Requirements Documents and implementation plans through
structured discovery, codebase exploration, and iterative user review.

---

## Modes

Detect the mode from the user's request. If ambiguous, default to `full`.

| Mode | Triggers | Output |
|------|----------|--------|
| **full** | "write a PRD", "plan a feature", "product requirements" | PRD + Implementation Plan |
| **prd-only** | "just the PRD", "document requirements", "spec this out" | PRD only |
| **breakdown** | "break down this epic", "feature PRD from epic" | Feature PRD from parent Epic |
| **plan** | "implementation plan", "tracer bullets", "break this PRD into phases" | Phased plan from existing PRD |

---

## Process

### Phase 1 — Discovery (all modes except `plan`)

> **Rule: never skip discovery.** Ask at least 3 clarifying questions before writing.

1. **Understand the problem.** Ask the user for a detailed description of:
   - The core pain point — why build this now?
   - Who it's for (end users, buyers, internal teams)
   - Any existing solutions or workarounds

2. **Interview relentlessly.** Walk down each branch of the design tree.
   Resolve dependencies between decisions one by one. Cover:
   - Success metrics — how do we know it worked? (quantifiable KPIs)
   - Constraints — budget, timeline, tech stack, regulatory
   - Non-goals — what are we explicitly NOT building?

3. **Explore the codebase** (if one exists). Verify the user's assertions.
   Understand current architecture, patterns, and integration points.
   - Identify reusable modules and patterns
   - Spot technical constraints the user may not have mentioned
   - Note existing test patterns

4. **Identify deep modules.** Sketch the major modules needed. A deep module
   encapsulates significant functionality behind a simple, stable interface.
   Prefer deep modules over shallow ones. Check with the user that these
   match expectations.

> In `breakdown` mode, the parent Epic replaces the interview. Read the Epic,
> ask clarifying questions about the specific feature, then proceed.

### Phase 2 — Draft the PRD

Write the PRD using the schema below. Present it section-by-section for review.

### Phase 3 — Implementation Plan (modes: `full` and `plan`)

1. **Identify durable architectural decisions** that won't change across phases:
   - Route structures / URL patterns
   - Database schema shape and key models
   - Authentication / authorization approach
   - Third-party service boundaries

2. **Draft vertical slices (tracer bullets).** Each phase is a thin slice that
   cuts through ALL layers end-to-end — not a horizontal slice of one layer.
   - Each slice delivers a narrow but COMPLETE path (schema → API → UI → tests)
   - A completed slice is demoable or verifiable on its own
   - Prefer many thin slices over few thick ones
   - Include durable decisions (routes, schema shapes, model names)
   - Do NOT include specific file names or implementation details likely to change

3. **Quiz the user.** Present the breakdown as a numbered list showing title
   and covered user stories. Ask:
   - Does the granularity feel right? Too coarse or too fine?
   - Should any phases be merged or split?
   - Iterate until approved.

### Phase 4 — Output

Save the PRD and plan as Markdown files:

- **PRD:** `./docs/prd/{feature-name}.md`
- **Plan:** `./plans/{feature-name}.md`

If the user prefers a different location or format (GitHub Issue, Google Doc),
adapt accordingly.

---

## PRD Schema

Use this exact structure. Omit sections marked "if applicable" when not relevant.

```markdown
# PRD: {Feature Name}

**Version:** 1.0
**Date:** {date}
**Author:** {author}
**Status:** Draft — Pending Review

---

## 1. Executive Summary

### Problem Statement
1–3 sentences on the core pain point, from the user's perspective.

### Proposed Solution
1–3 sentences on what we're building and how it solves the problem.

### Success Criteria
| KPI | Target | Measurement |
|-----|--------|-------------|
| ... | ...    | ...         |

---

## 2. User Experience

### User Personas

#### Primary: {Name} ("{Role}")
- **Who:** ...
- **Behavior:** ...
- **Goal:** ...
- **Tech comfort:** ...

#### Secondary: {Name} ("{Role}")
- ...

### User Stories

An extensive numbered list. Each story follows:
`As a {persona}, I want to {action} so that {benefit}.`

Cover primary paths AND edge cases. Group by feature area.

### Acceptance Criteria

For each major user story, provide criteria in Given/When/Then format:
- **Given** {precondition}
- **When** {action}
- **Then** {expected result}

### Non-Goals / Out of Scope

Explicit list of what we are NOT building. Protects the timeline.

---

## 3. Requirements

### Functional Requirements
Detailed bulleted list of what the system must do. Be specific
and unambiguous. Use concrete values, not "fast" or "intuitive".

```diff
# BAD — vague
- The search should be fast and return relevant results

# GOOD — concrete
+ The search must return results within 200ms for a 10k record dataset
+ The search must achieve >= 85% Precision@10 in benchmark evaluations
```

### Non-Functional Requirements
Bulleted list of constraints and quality attributes:
- Performance targets (response times, throughput)
- Security requirements (encryption, auth, compliance)
- Accessibility standards (WCAG level)
- Scalability expectations
- Browser / device support matrix

### AI/ML Requirements (if applicable)
- Model selection and rationale
- Tool / API requirements
- Evaluation strategy — how to measure output quality
- Fallback behavior when AI produces low-confidence results
- Cost constraints per request / per month

---

## 4. Technical Design

### Architecture Overview
High-level data flow and component interaction.
Include a diagram if helpful (Mermaid or ASCII).

### Module Design
List major modules with their responsibilities and interfaces.
Identify deep modules — those that encapsulate significant
complexity behind a simple, stable API.

### Implementation Decisions
- Architectural decisions made during discovery
- Schema changes required
- API contracts
- Key interactions between modules

> Do NOT include specific file paths or code snippets that
> may become outdated quickly.

### Integration Points
- External APIs and services
- Databases and data stores
- Authentication providers
- Third-party dependencies

---

## 5. Quality & Testing

### Testing Strategy
- What makes a good test for this feature (test external
  behavior, not implementation details)
- Which modules need tests
- Test types: unit, integration, E2E
- Prior art — reference similar tests in the codebase

### Security & Privacy
- Data handling requirements
- PII considerations
- Compliance requirements (GDPR, SOC2, etc.)
- Threat model (if relevant)

---

## 6. Risks & Roadmap

### Technical Risks
| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| ...  | ...      | ...        | ...        |

### Phased Rollout
High-level phases (detailed plan in separate document):
- **Phase 1 (MVP):** ...
- **Phase 2:** ...
- **Phase 3:** ...
```

---

## Implementation Plan Schema

Use this structure for the plan output (modes: `full` and `plan`):

```markdown
# Plan: {Feature Name}

> Source PRD: {link or file path}

## Architectural Decisions

Durable decisions that apply across all phases:

- **Routes:** ...
- **Schema:** ...
- **Key models:** ...
- **Auth approach:** ...
- (add/remove as appropriate)

---

## Phase 1: {Title}

**User stories:** {list from PRD}

### What to build
Concise description of this vertical slice. Describe end-to-end
behavior, not layer-by-layer implementation.

### Acceptance criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

---

## Phase 2: {Title}

**User stories:** {list from PRD}

### What to build
...

### Acceptance criteria
- [ ] ...

<!-- Repeat for each phase -->
```

---

## Quality Standards

### Requirements Quality

Use concrete, measurable criteria. Never use vague terms.

| ❌ Vague | ✅ Concrete |
|----------|------------|
| "fast" | "responds within 200ms at p95" |
| "easy to use" | "task completion in ≤ 3 clicks" |
| "secure" | "AES-256 encryption at rest, TLS 1.3 in transit" |
| "scalable" | "handles 10k concurrent users with < 500ms p99 latency" |

### Process Rules

1. **Never skip discovery.** Ask at least 3 questions before writing.
2. **Never hallucinate constraints.** If the user didn't specify something, ask or mark as `TBD`.
3. **Iterate.** Present drafts and ask for feedback on specific sections.
4. **Vertical slices only.** Implementation phases must cut through all layers, never horizontal.
5. **No premature file paths.** Don't include specific file names in plans — they'll change.
6. **Deep modules over shallow.** When designing module boundaries, prefer modules that hide complexity behind simple interfaces.

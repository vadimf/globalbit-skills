# Proposal Learnings

> This file is the skill's memory. It accumulates lessons from every proposal created.
> Read this file **before** starting a new proposal. Update it **during and after** each proposal.

---

## How to Use This File

### Before a proposal
- Read all sections below to absorb past learnings
- Pay special attention to the **Patterns** and **Don'ts** sections

### During a proposal
- When user corrects or revises a section, immediately add a learning entry
- Tag it with `[CORRECTION]` and the section number

### After a proposal
- Add a retrospective entry under **Proposal Log**
- Promote recurring patterns to the **Patterns** section

---

## Patterns

> Proven approaches that worked across multiple proposals. These override default behavior.

- **Executive Summary: paragraphs + 3-4 takeaway bullets, not tables** — end the executive summary with 3-4 bullet points summarizing the key value. Never put a table with hours/budget/methodology in the executive summary. Budget and timeline appear as inline text, not a table. Tables feel like "a deal"; bullets feel like "value". (learned from Neemanim post-analysis, 2026-03-16)
- **Budget/timeline as inline text** — write "~3 months" and "269,200 ₪" in a sentence, not as a table row. Hours should NOT appear in the executive summary at all. (learned from Neemanim post-analysis, 2026-03-16)
- **Background = 3 paragraphs max** — enough to show understanding, not a lecture. Personas/use-cases belong in the discovery phase, not in the proposal body. (learned from Neemanim post-analysis, 2026-03-16)
- **"The Need" as a separate section** — write in pain language ("currently does not provide…") not solution language ("we will build…"). Each need gets a concrete example from the client's world. (learned from Neemanim post-analysis, 2026-03-16)
- **Narrative format for solution components** — instead of What/Why/Deliverable bullet format, write each component as a short narrative paragraph that ends with the business impact: "המשמעות העסקית:" / "The business impact:". Deliverables go in a separate table. (learned from Neemanim post-analysis, 2026-03-16)
- **Open the Solution section with strategy first** — add a "הגישה שלנו" / "Our Approach" sub-section before any technical components. Explain the philosophy (e.g., "Revenue Engine", "Growth Platform"), then descend into components. (learned from Neemanim post-analysis, 2026-03-16)
- **Revenue Engine / Revenue Operations language** — use exec-level growth vocabulary: "Revenue Engine", "Revenue Operations", "Growth Platform", "Agentic AI". Avoid developer jargon. (learned from Neemanim post-analysis, 2026-03-16)
- **Stakeholder-specific bullets** — include at least 2 bullets in Business Goals AND 2 in "Why Globalbit" that speak directly to the Recipient's daily work. E.g., for marketing: "גמישות תפעולית לצוות השיווק", "Speed to Campaign". (learned from Neemanim post-analysis, 2026-03-16)
- **"Why Globalbit for THIS project"** — the About section's "why us" must be project-specific, not generic. Include Recipient-facing bullets ("partner who understands marketing, not just development") alongside Decision-Maker bullets ("CTO oversight", "industry experience"). (learned from Neemanim post-analysis, 2026-03-16)
- **QA as a detailed sub-section** — list QA layers (continuous → sprint → regression → UAT) instead of using Agile ceremony names. This signals professionalism better than "Definition of Done". (learned from Neemanim post-analysis, 2026-03-16)
- **Added Value: headline + mini-explanation** — each value item has a bold headline that stands alone (CEO reads only headlines) followed by a 1-2 sentence explanation. Don't write long bullets. (learned from Neemanim post-analysis, 2026-03-16)
- **AI Disclaimer in assumptions** — when the proposal includes AI/ML, add: "The solution uses AI models... which are statistical by nature and may occasionally produce imperfect results; human judgment remains necessary." Protects legally. (learned from Neemanim post-analysis, 2026-03-16)

---

## Don'ts

> Things that were explicitly corrected. Never repeat these.

- **Don't assume personal areas / authenticated sections** — unless explicitly confirmed, website projects are public-facing only. Don't include "login to personal area" or "view my policies" in proposals. Ask first. (learned from Neemanim)
- **Don't default to "lead generation" as the website's business goal** — always ask about the client's actual sales model. (learned from Neemanim)
- **Don't upload proposals as raw HTML to Google Docs** — always duplicate the Globalbit template first so headers, footers, fonts, and cover page are preserved. (learned from Neemanim)
- **Don't insert content after the NEXT_PAGE section break** — content in Section 1 has no header/footer. Always insert in Section 0 (before the break). (learned from Neemanim)
- **Don't try to manipulate headers/footers programmatically** — rely on the template's built-in header/footer. `updateSectionStyle` cannot change `defaultHeaderId`. (learned from Neemanim)
- **Don't create new section breaks in programmatic output** — this changes header/footer behavior. Work within the template's existing section structure. (learned from Neemanim)
- **Don't use Agile ceremony jargon in proposals** — Sprint Planning, Daily Standups, Sprint Retrospectives, Definition of Done do NOT belong in client-facing proposals. The client is not managing a dev team. Say: "ספרינטים של שבועיים, דמו חי בסוף כל ספרינט" and move on. (learned from Neemanim post-analysis, 2026-03-16)
- **Don't put a numbers table in the Executive Summary** — no table with hours/budget/timeline/methodology. It makes the summary feel transactional, not strategic. (learned from Neemanim post-analysis, 2026-03-16)
- **Don't include detailed personas/use-case tables in the proposal** — those belong in the discovery phase deliverable. In the proposal, mention audience types in narrative form with 1-2 examples. (learned from Neemanim post-analysis, 2026-03-16)
- **Don't write "UTM Parameters" or technical parameter names** — translate to business language: "ערוץ שממנו הגיע המבקר" / "the channel the visitor arrived from". (learned from Neemanim post-analysis, 2026-03-16)
- **Don't combine Scope and Deliverables into one section** — "Deliverables" is its own section. "In Scope / Out of Scope" moves to Commercial Terms or is its own section. (learned from Neemanim post-analysis, 2026-03-16)

---

## Section-Specific Learnings

> Refinements for specific sections, organized by section number.

### §1 Executive Summary
- **[PATTERN] Structure: paragraphs → bullets → confidence close** — 2-3 narrative paragraphs + 3-4 takeaway bullets (●) at the end. No table. Budget/timeline as inline text. End with a vision sentence about long-term value, not data. (learned from Neemanim post-analysis, 2026-03-16)
- **[PATTERN] Takeaway bullets** — the CEO will read only these 4 bullets and decide. They must summarize: (1) what we build, (2) key capability, (3) methodology/timeline, (4) strategic outcome. (learned from Neemanim post-analysis, 2026-03-16)

### §2 Background & Context
- **[CORRECTION] Always identify personas and use cases per brand/product** — when a project involves multiple brands with different audiences, map each brand's business model (B2B, B2C, B2B2C) and specific personas with their use cases. Don't describe brands generically. (learned from Neemanim, 2026-03-09)
- **[CORRECTION] Don't assume personal area / authenticated sections** — unless explicitly confirmed, website projects are public-facing only. Don't include "login to personal area" or "view my policies" in personas. Ask first. (learned from Neemanim, 2026-03-09)
- **[PATTERN] UTM-based personalization** — for B2C / lead-gen sites, consider personalization based on traffic source (ad campaign, email, organic). Show relevant content immediately based on where the visitor came from. Example: car insurance ad → car insurance content front and center with relevant offers. This is a strong differentiator in proposals. (learned from Neemanim, 2026-03-09)
- **[PATTERN] 3 paragraphs max** — (1) what the project is, (2) why it matters now (strategic context), (3) what the challenge is. Personas and use-cases do NOT go here — they belong in the discovery phase. (learned from Neemanim post-analysis, 2026-03-16)

### §3 Business Goals
- **[CORRECTION] Don't default to "lead generation" as the website's business goal** — always ask about the client's actual sales model before writing business goals. Websites serve different purposes for different businesses: lead gen, validation/credibility, retention, e-commerce, self-service, etc. Ask: "How do your customers find you and buy from you?" (learned from Neemanim, 2026-03-09)
- **[PATTERN] Add Recipient-specific goals** — when the Recipient is a marketing team, add: "גמישות תפעולית לצוות השיווק" (operational flexibility) and "Speed to Campaign" (ability to launch campaigns independently). For IT: add "reduced vendor dependency" and "maintainability". These goals make the Recipient feel the proposal is for them. (learned from Neemanim post-analysis, 2026-03-16)

### §4 Project Goals
- **[PATTERN] Consider merging into Business Goals** — in the final proposal, Project Goals were absorbed into Business Goals. This reduces redundancy and makes the document more concise. If the project is complex, keep them separate. If straightforward, merge. Decision should be per-project. (learned from Neemanim post-analysis, 2026-03-16)

### §5 Proposed Solution
- **[CRITICAL] Narrative format, not What/Why/Deliverable** — each component is a narrative paragraph that flows naturally and ends with "המשמעות העסקית:" / "The business impact:". Deliverables go in a separate table (§8 Deliverables). (learned from Neemanim post-analysis, 2026-03-16)
- **[PATTERN] Open with "הגישה שלנו" / "Our Approach"** — before any components, add a strategic sub-section explaining Globalbit's philosophy for this project (e.g., "Revenue Engine", "Growth Platform"). This frames the technical components in business context. (learned from Neemanim post-analysis, 2026-03-16)
- **[PATTERN] Include QA in the solution** — QA is a component of the solution ("בדיקות ואבטחת איכות"), not a separate methodology section. List the 4 QA layers: continuous → sprint → regression → UAT. (learned from Neemanim post-analysis, 2026-03-16)

### §6 About Globalbit
- **[CRITICAL] "Why Globalbit for THIS project"** — replace the generic "Why Globalbit" with project-specific reasons (5-7 bullets). Must include at least 2 bullets for the Recipient ("understands marketing, not just development") and 2 for the Decision Maker ("industry experience", "CTO oversight"). (learned from Neemanim post-analysis, 2026-03-16)

### §7 Deliverables (was "Scope & Deliverables")
- **[PATTERN] Separate from Scope** — Deliverables is its own section. Scope (In/Out) moves to Assumptions or is listed in Commercial Terms. (learned from Neemanim post-analysis, 2026-03-16)

### §8 Methodology → Project Phases
- **[CRITICAL] No Agile ceremony names** — do NOT list Sprint Planning, Daily Standups, Retrospectives, Definition of Done. Clients don't manage dev teams. Describe phases by activities and deliverables. Mention "ספרינטים של שבועיים" once. (learned from Neemanim post-analysis, 2026-03-16)
- **[PATTERN] Place "up to 2 review rounds" in the launch phase** — this gives the client a sense of control and sets expectations. (learned from Neemanim post-analysis, 2026-03-16)

### §9 Team Structure
- **[PATTERN] Consider removing as a standalone section** — Team info can be a single paragraph or sentence in About Globalbit ("senior dedicated team, CTO oversight"). A full table of roles/responsibilities is more internal-facing than client-facing. If included, keep it minimal. (learned from Neemanim post-analysis, 2026-03-16)

### §10 Timeline & Milestones
- **[PATTERN] Ask for commercial parameters before write** — hours, timeline, and budget are commercial decisions that need CEO input. Never default-estimate without asking. (learned from Neemanim post-analysis, 2026-03-16)
- **[PATTERN] Merge UX and UI into one timeline row** — "עיצוב UX/UI" instead of two separate lines. Reduces visual inflation. (learned from Neemanim post-analysis, 2026-03-16)

### §11 Risk Management
- **[PATTERN] Optional section** — in mid-size projects (<500K), risk management can be omitted. It's the "driest" section. If included, keep to 5-7 rows. If omitted, mention risk mitigation briefly in Methodology. (learned from Neemanim post-analysis, 2026-03-16)

### §12 Added Value
- **[PATTERN] Headline + mini-explanation format** — each bullet: bold headline that stands alone → 1-sentence explanation. The CEO reads only headlines. If he understands the value from headlines alone, the section works. (learned from Neemanim post-analysis, 2026-03-16)

### §13 Commercial Terms
- **[PATTERN] AI Disclaimer** — when AI is included, add to assumptions: "הפתרון כולל שימוש במנגנוני בינה מלאכותית... מערכות אלו מבוססות על מודלים סטטיסטיים ועשויות לעיתים להפיק תוצאות שאינן מדויקות, ולכן נדרש שיקול דעת אנושי." (learned from Neemanim post-analysis, 2026-03-16)
- **[PATTERN] Include only active roles** — don't list roles that won't be used (e.g., Junior Developer if none assigned). (learned from Neemanim post-analysis, 2026-03-16)

### §14–16 Boilerplate
- **[CORRECTION] Add "ונכסים גרפיים נוספים" to Client Commitment** — after "לוגואים" in the content responsibility clause. (learned from Neemanim post-analysis, 2026-03-16)
- **[CORRECTION] Add "שירותי AI" to third-party services list** — in General Terms. (learned from Neemanim post-analysis, 2026-03-16)

---

## Industry-Specific Learnings

> What works well for specific industries.

### Finance & Insurance
- **Tender-based B2B2C model** — corporate insurance companies (like Neemanim) often sell via tenders, not direct leads. The website's role is trust/credibility for tender evaluation and retention of existing clients' employees — NOT lead generation. Always ask about the sales model first. (learned from Neemanim, 2026-03-09)
- **Dual-brand architecture** — insurance groups often have separate B2B2C and B2C brands with completely different website goals. Design proposals as unified projects with shared infrastructure but distinct personas and KPIs per brand. (learned from Neemanim, 2026-03-09)

<!-- Example format:
### Healthcare
- Compliance section must reference MOH regulations specifically
-->

---

## Client Preferences

> Recurring client-specific preferences. Use when working with a returning client.

_(Nothing here yet.)_

<!-- Example format:
### DSR Rada
- Prefers concise executive summaries (under half a page)
- Technical audience — less business fluff, more architecture detail
-->

---

## Tone & Style Learnings

> Refinements to the tone guide based on user feedback.

_(Nothing here yet.)_

<!-- Example format:
- User prefers "we will deliver" over "we ensure delivery of" — more direct
- Hebrew proposals: avoid overly formal legal-sounding language in methodology section
-->

---

## Google Docs Workflow Learnings

> Lessons about pushing proposals to Google Docs format.

### Template Architecture (Critical)

- **The template uses a two-section structure** — Section 0 (CONTINUOUS) contains the cover page AND the body content. The NEXT_PAGE section break at the end creates Section 1 which is empty. (learned from Neemanim, 2026-03-10)
- **Header/footer only appears in Section 0** — `useFirstPageHeaderFooter: True` hides header/footer on page 1 (cover). Pages 2+ in Section 0 get the default header/footer (Globalbit logo bar). Section 1 has its own **empty** header/footer overrides. (learned from Neemanim, 2026-03-10)
- **NEVER insert content after the NEXT_PAGE section break** — content in Section 1 will have NO header/footer. This was the root cause of 3 failed iterations. (learned from Neemanim, 2026-03-10)
- **Find the insertion point**: the last paragraph's `startIndex` before the NEXT_PAGE break. Insert all proposal content at this index (within Section 0). (learned from Neemanim, 2026-03-10)

### Template Operations

- **Always duplicate the template** — never create a blank doc or upload raw HTML. The template has Globalbit branding (header, footer, fonts, cover page). Template ID: `1P2BhWQGGxeWdCYhdFP8uaUd7BqilgwKAYXnvEzfX57U`. (learned from Neemanim, 2026-03-09)
- **Use `replaceAllText` for cover page** — template has placeholders (`כותרת ראשית`, `כותרת משנית 1/2/3`) that should be replaced with the actual title, client name, date, and doc number. (learned from Neemanim, 2026-03-09)

### Deletion Rules

- **`deleteContentRange` cannot cross section breaks or tables** — delete within element boundaries only. (learned from Neemanim, 2026-03-09)
- **Delete in reverse order** — always delete from highest index first to preserve lower indices. (learned from Neemanim, 2026-03-10)
- **Cannot delete the last paragraph before a section break** — Google Docs requires at least one paragraph per section. Leave it as an empty line. (learned from Neemanim, 2026-03-10)
- **Delete tables separately** — a table element has its own `[startIndex, endIndex]` range and must be deleted as a single unit. (learned from Neemanim, 2026-03-10)

### Content Insertion (Three-Pass Approach)

- **Pass 1: Text insertion** — insert all text (headings, paragraphs, bullets, numbered lists) with `insertText`. Use `__TBL1__`, `__TBL2__` placeholders for tables. (learned from Neemanim, 2026-03-10)
- **Pass 2: Style application** — apply paragraph styles (`HEADING_1`, `HEADING_2`, `HEADING_3`), bullets, spacing, and bold formatting. (learned from Neemanim, 2026-03-10)
- **Pass 3: Table insertion** — for each table placeholder (in reverse order): delete placeholder → `insertTable` → re-read doc → insert cell text → style table. This requires re-reading the document between each table to get correct indices. (learned from Neemanim, 2026-03-10)
- **Chunk batchUpdate requests** — max ~60 requests per batch call (not 100, which can cause issues). (learned from Neemanim, 2026-03-10)

### Table Styling Standard

- **Header row**: Navy blue background (`rgb: 0.11, 0.09, 0.25`), white bold text, 9pt font
- **Body rows**: 9pt font, 2pt spacing above/below, 115% line spacing
- **Use `updateTableCellStyle`** with `tableRange` for cell backgrounds (not `updateParagraphStyle`)
- **Use `updateTextStyle`** for font color, size, and bold (learned from Neemanim, 2026-03-10)

### List Spacing Standard

- **CRITICAL**: Google Docs default `spacingMode` is `COLLAPSE_LISTS` — this **ignores** `spaceBelow`/`spaceAbove` between consecutive list items. You MUST set `spacingMode: "NEVER_COLLAPSE"` on list paragraphs for spacing to render. (learned from Neemanim, 2026-03-10)
- **Bullet and numbered list items**: 8pt `spaceBelow`, 115% `lineSpacing`, `spacingMode: "NEVER_COLLAPSE"` — include `spacingMode` in the `fields` mask
- **Paragraphs**: 8pt `spaceBelow` + 115% `lineSpacing`
- **Headings**: 14pt `spaceAbove`, 6pt `spaceBelow`
- **Table header pinning**: Use `pinTableHeaderRows` request (NOT `updateTableRowStyle.tableHeader`) with `tableStartLocation.index` and `pinnedHeaderRowsCount: 1` to repeat headers on each page

### Token Management

- **`gws-auth.sh` can hang** — for reliability, refresh the token directly via OAuth2 API using `curl`. The refresh token is in `~/.config/gws/credentials.json` under `tokens.refresh_token`, and client credentials are in `~/.config/gws/client_secret.json` under `installed`. (learned from Neemanim, 2026-03-10)
- **Token path**: `~/.config/gws/cached_token.json` has the access token. There is NO `~/.config/gws/config.json` — that was a wrong assumption. (learned from Neemanim, 2026-03-10)

### Don'ts (Google Docs Specific)

- **Don't try to manipulate headers/footers programmatically** — `updateSectionStyle` does not allow changing `defaultHeaderId`. Inserting images into headers/footers can result in misplaced content. Always rely on the template's built-in header/footer. (learned from Neemanim, 2026-03-10)
- **Don't create new section breaks** — adding section breaks changes the header/footer behavior. Work entirely within the template's existing sections. (learned from Neemanim, 2026-03-10)
- **Don't insert all text + all tables in a single batchUpdate** — table insertion shifts indices, making subsequent operations fail. Use the three-pass approach. (learned from Neemanim, 2026-03-10)

---

## Proposal Log

> One entry per proposal. Brief retrospective.

### 2026-03-09/10 — Ayalon Neemanim & Nechonim — Website Design & Development
- **Service type**: UX/UI Design + Development
- **Language**: Hebrew
- **Client brief**: Downloaded from email attachment (`brief.docx`)
- **What went well**: Solution architecture, commercial terms, and full 16-section structure produced in a single session. All 9 tables formatted with navy blue headers. Cover page placeholders replaced automatically.
- **What was revised**: 
  - Business goals initially defaulted to lead-gen — corrected to tender-based model for Neemanim
  - Personas initially included personal area/login — corrected to public-facing only
  - UTM personalization added as a differentiator per user request
- **Google Docs output**: 
  - Template duplicated 3 times before getting section structure right
  - Root cause of header/footer failure: content was inserted after the NEXT_PAGE section break (Section 1), which has empty header/footer overrides
  - Fix: insert all content before the NEXT_PAGE break (in Section 0)
  - Three-pass approach for tables (placeholder → insert → style) worked reliably
  - Final working script: `/tmp/populate_v4.py`
- **Key learnings**: 
  - Always ask about the client's sales model before writing business goals
  - Don't assume personal/authenticated areas
  - Always use the Globalbit template (never raw HTML upload)
  - **Critical: insert content in Section 0 (before NEXT_PAGE break), never in Section 1**
  - Token refresh: use direct OAuth2 API, not `gws-auth.sh` (which can hang)

### Google Docs Formatting Rules (Global)

- **Never center-align text** — center alignment is only for images. All text must be left-aligned (or right-aligned for RTL Hebrew). This includes headings, paragraphs, and list items.
- **Always add spacing after bullet/numbered list items** — set `spaceBelow` (e.g., 8pt) on every list item paragraph to ensure visual separation between items.
- **Always rewrite the existing document** — never duplicate/create new documents. Work on a single doc and overwrite content as needed (delete old content → insert new content).
- **Always use Google Docs native styles** — use `namedStyleType` for all content: `TITLE`, `HEADING_1`, `HEADING_2`, `HEADING_3`, `NORMAL_TEXT`. Never apply manual font sizes or styles that bypass the doc's style definitions.


---
name: create-new-page
description: |
  Full protocol for creating a new service or landing page on the Globalbit website.
  
  Use when: creating any new page (service, industry, use-case), even if you have prior context.
  This skill defines the mandatory research, story, copy, component, testing, and verification steps.
  
  Triggers: "create a new page", "add a [service] page", "build a page for [topic]"
user-invocable: true
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Browser", "WebSearch"]
---

# How to Create a New Globalbit Website Page

**Company**: Globalbit — a software and product development company based in Israel.
**Website framework**: Next.js (App Router), TypeScript, Tailwind CSS.
**Page directory**: `app/[route]/page.tsx`
**Dev server**: `npm run dev` (runs on localhost:3000)

This skill must be followed in full, in order, every time you create a new page. Do not skip steps.

---

## Table of Contents

1. [Project Context: What You Need to Know](#1-project-context-what-you-need-to-know)
2. [Step 1 — Research: Gather Real Data](#step-1--research-gather-real-data)
3. [Step 2 — Decide What the Page Must Accomplish](#step-2--decide-what-the-page-must-accomplish)
4. [Step 3 — Build the Story Arc](#step-3--build-the-story-arc)
5. [Step 4 — Map the Story to Shared Components](#step-4--map-the-story-to-shared-components)
6. [Step 5 — Write the Implementation Plan](#step-5--write-the-implementation-plan)
7. [Step 6 — Write the Page Code](#step-6--write-the-page-code)
8. [Step 7 — Refine the Copy](#step-7--refine-the-copy)
9. [Step 8 — Verify: npm run build](#step-8--verify-npm-run-build)
10. [Step 9 — Verify: Visual Test in Browser](#step-9--verify-visual-test-in-browser)
11. [Step 10 — Report to the User](#step-10--report-to-the-user)

---

## 1. Project Context: What You Need to Know

Before starting any research, read and internalize the following facts about this codebase.

### Project structure

```
app/                        ← Next.js App Router pages
  [service]/page.tsx        ← e.g. app/mobile-development/page.tsx
components/
  layout/                   ← Header, Footer, Contact, PageHero, PageLogos
  shared/                   ← Reusable section components (CasesSection, TimelineWorkflow, etc.)
  ui/                       ← Primitive UI components (Button, TextReveal, Card, Stat)
  [page-specific]/          ← Components used only on one page (avoid creating these)
docs/
  knowledge/COMPONENT_LIBRARY.md  ← Authoritative list of all shared components
  DESIGN_GUIDELINES.md            ← Typography, spacing, color rules
```

### Absolute rules (never break these)

1. **English only.** All copy on all pages is in English.
2. **Shared components only.** Do not create page-specific components unless there is no shared component that can do the job. Before creating anything new, check `COMPONENT_LIBRARY.md`.
3. **No changes to colors, font sizes, or spacing values unless explicitly asked.** Every component has correct styling already. Just pass the right props.
4. **Standard section spacing**: `py-10 lg:py-12`. Never use `py-16`, `py-20`, or `py-24` for sections.
5. **Data arrays at the top of the file.** Define all text content as `const` arrays at the top of `page.tsx`, above the page component.
6. **`"use client"` only when necessary.** If the page uses `useState`, `framer-motion`, or event handlers, add `"use client"` at the top. Otherwise omit it.
7. **Image paths**: All case images are in `/public/images/cases/`. Use `/images/cases/filename.png` (no `/public` prefix in `src`).

### Available case images

Use these real images from `/public/images/cases/`:

- `/images/cases/moovit small.png` — Moovit, urban mobility app
- `/images/cases/espresso small.png` — Espresso Club, e-commerce
- `/images/cases/IBI Small.png` — IBI Smart, fintech
- `/images/cases/igds small.png` — Israel Government Design System
- `/images/cases/covid small.png` — COVID response dashboard
- `/images/cases/pfizer small.png` — Pfizer digital health

---

## Step 1 — Research: Gather Real Data

**Why**: You cannot write converting copy using generic phrases. You need real business outcomes, real client names, and real numbers. Generic copy ("we build great apps") does not convert.

### 1a. Read the Globalbit company website

Use `read_url_content` on `https://globalbit.co.il` (and any linked pages) to extract:

- **Real clients**: names of companies Globalbit has worked with
- **Real numbers**: user counts (e.g. "1.7 billion Moovit users"), years of experience, team size, number of projects
- **Awards and recognition**: app store rankings, industry awards, certifications
- **Real services**: what Globalbit actually does (not what you assume)
- **Case studies**: specific project descriptions with outcomes

**Store everything you find.** You will use it in the copy.

Known facts from previous research you can use directly:

- Moovit: 1.7 billion users worldwide, built from MVP, #1 transit app globally, Google Play App of the Year
- Espresso Club: digital transformation, #2 coffee brand in Israel
- IBI Smart: #1 trading app in Israel, 600,000+ users
- Israel Government Design System: national UX standards
- Pfizer: "top innovative project" recognition
- Team: 50+ developers, designers, and analysts
- 15+ years of experience
- 150+ projects delivered globally
- 200,000,000+ users across all products

### 1b. Research the target visitor

Ask yourself: **What does a visitor searching for this service actually want?**

Use `search_web` with queries like:

- `"[service] development company Israel"`
- `"how to find [service] agency"`
- `"what to look for in [service] company"`
- `"[service] development mistakes"`

From the search results, extract:

- **Pain points**: what do they fear? (wasted budget, poor quality, missed deadlines)
- **Desired outcomes**: what do they actually want to achieve? (working product, growth, profitability)
- **Objections**: why would they NOT hire a company? (trust, cost, communication)
- **Search intent**: are they comparison shopping, or ready to buy?

### 1c. Research 2–3 competitors

Use `read_url_content` on 2–3 top competitor pages for the same service. Look for:

- What do they lead with? (their strongest claim)
- What proof do they offer? (logos, case studies, numbers)
- What do they lack? (Globalbit's opportunity to differentiate)

Good competitor pages to check for software companies:

- surf.ru (Russian market leader — good structure reference)
- miquido.com
- cleveroad.com
- netguru.com

Do NOT copy competitor copy. Extract the structure and proof approach only.

---

## Step 2 — Decide What the Page Must Accomplish

A good landing page has one job: **move the visitor to book a discovery call**.

Before writing any copy, answer these four questions clearly:

**Q1: Who is this visitor?**
Be specific. "A CTO at a 100-person retail company who needs a mobile app built in 4 months and is worried about budget overruns" is a valid answer. "Businesses" is not.

**Q2: What is their #1 pain right now?**
Not a feature they want — a business problem they are stressed about. Example: "They tried to build a mobile app with a local agency, got burned, and now need a trustworthy partner."

**Q3: What is the ONE thing Globalbit can say that makes this visitor trust us?**
Must be specific and provable. Example: "We built Moovit from MVP to 1.7 billion users." Not: "We are a trusted technology partner."

**Q4: What do we want them to do after reading the page?**
Answer: Submit the contact form. Everything on the page leads to this.

---

## Step 3 — Build the Story Arc

Humans make emotional decisions and justify them rationally. The page must tell a story that moves from "I have this problem" → "these people can solve it" → "I trust them" → "I should contact them now."

Use this proven structure for service pages:

```
Section 1 — HOOK (PageHero)
  The visitor has a problem. Name it. Make the biggest promise.
  Headline: outcome-first. What will they achieve?
  Example: "Mobile Apps That Scale to 1.7 Billion Users"
  NOT: "Mobile Application Development Services"
  
Section 2 — TRUST SIGNAL (PageLogos)
  Show familiar client logos. This says "real companies trust us."
  Place this HIGH on the page — before the visitor has scrolled away.
  
Section 3 — THE PROBLEM + OUR SOLUTION (ApproachSection or TextSection)
  Articulate the visitor's pain, then position Globalbit as the solution.
  Use two text columns: left = the challenge, right = how we handle it.
  
Section 4 — WHY US (FeatureSteps)
  4–6 concrete differentiators. NOT "we care about quality."
  Each differentiator needs a specific, verifiable claim.
  Wrong: "Experienced team"
  Right: "15 years. 150+ projects. 200M+ users."
  
Section 5 — INDUSTRIES / WHO WE SERVE (IndustryTable or FeatureSteps)
  Help the visitor confirm "yes, they work with companies like mine."
  Name specific industries with real project examples.
  
Section 6 — PROOF: PROJECTS (CasesSection)
  Show 2–4 real case studies with outcomes, not just project names.
  Each case: company + what we built + measurable result.
  
Section 7 — HOW IT WORKS (TimelineWorkflow)
  4 steps from "first contact" to "launched product."
  Remove the fear of the unknown. Make hiring us feel safe and clear.
  
Section 8 — MID-PAGE CTA (MidPageCTA)
  A compelling push to take action. Strong verb + specific benefit.
  Example: "Speak with a Product Expert. Get a scope and estimate in 48 hours."
  
Section 9 — MORE TRUST (WhyTrustUs)
  Awards, recognition, certifications.
  
Section 10 — TESTIMONIALS (Testimonials)
  Real quotes from real clients. Names + roles + company.
  Use the actual testimonials harvested from Globalbit's website.
  
Section 11 — FAQ (FAQ)
  Remove the last 5 objections standing between the visitor and contacting us.
  Answer: timeline, cost, technology stack, support, industry expertise.
  
Section 12 — CONTACT (Contact)
  The form. Already built. Just place it at the bottom.
```

**You do not need all 12 sections on every page.** Choose the sections that are most important for this specific visitor type. But always have: Hook → Proof → Process → CTA.

### Section Belief Mapping (MANDATORY before writing copy)

> [!CAUTION]
> **Before writing ANY section copy**, complete this belief map for EVERY section you include on the page. If you skip this, sections will repeat the same argument in different words and CTAs will feel disconnected.

For **every section** on the page, answer:

1. **What should the TA believe after reading this section?** — One specific belief. Each section must create a DIFFERENT belief than every other section.
2. **Why does this section exist?** — What unique argument does it advance?
3. **How does this section move the reader toward conversion?** — Map the psychological progression: curiosity → identification → trust in method → proof of execution → decision trigger.

**Anti-patterns to catch:**

- Multiple sections saying "we're experienced" in different words → cut one
- CTAs that don't match the section's emotional moment (e.g., ambition-themed section with a transactional "Get a Free Estimate" CTA — should be "Tell Us What You're Building" instead)
- Facts listed without a belief goal → every number must serve a specific belief

**Include the belief map in your implementation plan as a table:**

| # | Section | TA Belief | Why It Exists |
|---|---------|-----------|---------------|
| 1 | Hero | "Wait — they did THAT?" | Break assumptions, force curiosity |
| 2 | Metrics | "These numbers are real" | Quantify before skepticism kicks in |
| 3 | Story | "This is a pattern, not luck" | Show repeated verified impact |
| ... | ... | ... | ... |

---

## Step 4 — Map the Story to Shared Components

Read `docs/knowledge/COMPONENT_LIBRARY.md` fully before mapping.

Here is how each story beat maps to a component:

| Story Beat | Component | Import path |
|---|---|---|
| Hero / Hook | `PageHero` | `@/components/layout/PageHero` |
| Client logos | `PageLogos` | `@/components/layout/PageLogos` |
| Text + two columns | `ApproachSection` | `@/components/shared/ApproachSection` |
| Text + bullet list | `TextSection` | `@/components/shared/TextSection` |
| 4–8 feature cards | `FeatureSteps` | `@/components/shared/FeatureSteps` |
| Industry table | `IndustryTable` | `@/components/shared/IndustryTable` |
| Project cards | `CasesSection` | `@/components/shared/CasesSection` |
| Process timeline | `TimelineWorkflow` | `@/components/shared/TimelineWorkflow` |
| Mid-page push | `MidPageCTA` | `@/components/shared/MidPageCTA` |
| Awards / trust | `WhyTrustUs` | `@/components/uiux-design/WhyTrustUs` |
| Client quotes | `Testimonials` | `@/components/shared/Testimonials` |
| Q&A objections | `FAQ` | `@/components/shared/FAQ` |
| Contact form | `Contact` | `@/components/layout/Contact` |

**Before mapping**, view the actual component file to confirm what props it accepts. Never guess props. Example:

```
view_file: components/shared/CasesSection.tsx
```

**If no existing component fits**, do not create a new one. Use the closest existing component and pass it what it needs.

---

## Step 5 — Write the Implementation Plan

Before writing any code, create `implementation_plan.md` in the artifacts directory. The plan must include:

### Story narrative (2–3 sentences)

Describe who the visitor is, what they want, and how the page moves them to action.

### Section mapping table

List every section in order:

| # | Section | Component | Headline (draft) | Key proof/claim |
|---|---|---|---|---|
| 1 | Hero | `PageHero` | "Mobile Apps That Scale to Billions" | Moovit 1.7B users |
| 2 | Logos | `PageLogos` | — | Moovit, IBI, Pfizer, Espresso |
| ... | ... | ... | ... | ... |

### Automatic test plan

Exact commands to run after building:

```bash
npm run build     # must exit 0
```

If TypeScript errors or missing module errors appear, they will be logged here.

### Manual test plan

Step-by-step browser verification:

1. Open `localhost:3000/[route]`
2. Verify: navigation header is visible and not overlapping hero
3. Verify: hero text is readable, no overflow
4. Scroll through all sections — confirm no broken images
5. Submit the contact form — confirm it renders without error
6. Resize to mobile (375px) — confirm layout stacks correctly

**After writing the plan → call `notify_user` and wait for user approval before writing any code.**

---

## Step 6 — Write the Page Code

Once the plan is approved, create `app/[route]/page.tsx`.

### File structure template

```tsx
"use client"; // only add if using useState or framer-motion directly

import React from "react";
// import only the components you actually use
import { PageHero } from "@/components/layout/PageHero";
import { PageLogos } from "@/components/layout/PageLogos";
import { CasesSection } from "@/components/shared/CasesSection";
import { TimelineWorkflow } from "@/components/shared/TimelineWorkflow";
import { MidPageCTA } from "@/components/shared/MidPageCTA";
import { Testimonials } from "@/components/shared/Testimonials";
import { FAQ } from "@/components/shared/FAQ";
import { Contact } from "@/components/layout/Contact";

// ── Data ─────────────────────────────────────
// All content as constants. Never inline strings in JSX.

const CASES_DATA = [
  {
    title: "Moovit",
    description: "From MVP to 1.7 billion users. The world's #1 transit app.",
    image: "/images/cases/moovit small.png",
  },
  // ...
];

const PROCESS_STEPS = [
  {
    id: "01",
    title: "Discovery & Analysis",
    description: "...",
  },
  // ...
];

const TESTIMONIALS_DATA = [
  {
    text: "...",
    author: "Nir Erez",
    role: "CEO, Moovit",
    logo: "/images/clients/Moovit_Logo-primary.png",
  },
];

const FAQ_DATA = [
  {
    question: "How long does development take?",
    answer: "...",
  },
];

// ── Page ─────────────────────────────────────

export default function ServiceNamePage() {
  return (
    <main className="min-h-screen">
      <PageHero
        title="Your Outcome-Focused Headline"
        description="Supporting line that names the visitor's goal."
        useTextReveal
      />

      <PageLogos />

      <CasesSection
        title="Our Projects"
        subtitle="Real outcomes. Not just deliverables."
        cases={CASES_DATA}
        columns={2}
      />

      <TimelineWorkflow
        tag="PROCESS"
        title="From First Call to Launched Product"
        items={PROCESS_STEPS}
      />

      <MidPageCTA
        title="Speak with a Product Expert"
        description="Get a scope and budget estimate within 48 hours."
        buttonText="Contact us"
        bgDesktop="/images/services/bg-desktop.webp"
        bgMobile="/images/services/bg-mobile.webp"
      />

      <Testimonials items={TESTIMONIALS_DATA} />

      <FAQ items={FAQ_DATA} />

      <Contact />
    </main>
  );
}
```

### Critical implementation rules

**Never inline content.** Every string visible to the visitor must be in a `const` at the top. This makes it easy for the user to update text without touching JSX.

**Images**: Always use `next/image` or pass the path string to components that use it internally (like `CasesSection`). Never use `<img>` tags.

**MidPageCTA images**: The standard background images are:

- Desktop: `/images/services/bg-desktop.webp`
- Mobile: `/images/services/bg-mobile.webp`

**PageLogos**: This component needs no props. It renders the standard set of client logos. Just include `<PageLogos />`.

**Contact**: This component needs no props. Just include `<Contact />` at the bottom.

---

## Step 7 — Refine the Copy

After the page renders without errors, go back and re-read every piece of text on the page. Apply these rules:

### Headline rules

- **Lead with outcome, not capability.** "Apps That Reach 1.7 Billion Users" not "Mobile App Development"
- **Be specific.** "Used by 200M+ users in 15 countries" not "used by many users worldwide"
- **Use strong verbs.** Built, Shipped, Scaled, Drove, Generated — not Made, Created, Did
- **One strong idea per headline.** Do not cram two concepts into one headline.

### Description/body copy rules

- **Cut corporate speak.** Delete: "robust", "cutting-edge", "synergy", "leverage", "holistic", "end-to-end solution"
- **Name the customer's pain.** "Most agencies build what you asked for. We build what your users need."
- **Use social proof as evidence.** Don't say "we are experienced" — say "we built Moovit from 0 to 1.7 billion users."
- **Answer "so what?"** After writing any claim, ask "so what does that mean for the visitor?" and add that to the copy.

### FAQ copy rules

- Write questions as the visitor would actually ask them, in their own words.
- Answers must be informative, not evasive. Give real numbers (timeline, cost range, team structure).
- End every FAQ answer with a confidence statement that reduces fear.

### CTA copy rules

- Buttons must describe the action AND the benefit.
  - ✅ "Get a Free Estimate"
  - ✅ "Speak with an Expert"
  - ❌ "Submit"
  - ❌ "Learn More"
- The supporting line under the CTA headline must remove the last objection: "No commitment. 48-hour response."

---

## Step 8 — Verify: npm run build

Run this exact command and wait for it to complete:

```bash
npm run build
```

The build must exit with code 0. If it does not:

1. Read the error output carefully.
2. Fix all TypeScript errors — these are usually wrong prop types or missing imports.
3. Fix all "module not found" errors — wrong import paths.
4. Re-run `npm run build` until it exits 0.

**Do not report the page as done if the build fails.**

Common errors and how to fix them:

| Error | Fix |
|---|---|
| `Module not found: @/components/shared/X` | Wrong import path — check the actual file name and path |
| `Type error: Property 'X' does not exist on type 'Y'` | You passed a prop the component doesn't accept. Read the component's TypeScript interface. |
| `Image with src "/images/X" is not defined in next.config.js` | The image path is wrong. Check `/public/images/` for the actual filename. |
| `'X' is defined but never used` | Remove the import. |

---

## Step 9 — Verify: Visual Test in Browser

Open a `browser_subagent` and navigate to `http://localhost:3000/[route]`.

Check the following in order:

1. **Navigation**: The site header (with logo and menu) must be visible at the top. If it is missing, the header is probably being overridden by the hero section.

2. **Hero section**: The main headline must be legible. No text overflow. The background or color is correct.

3. **All images load**: Scroll slowly through the entire page. Note any image that shows a broken icon or grey placeholder. If images are broken, fix the `src` path.

4. **Section spacing**: There should be consistent vertical spacing between all sections. No sections should be touching or have excessive gaps.

5. **Cards and grids**: All cards should be the same height in their row. Columns should align correctly.

6. **Contact form**: Scroll to the bottom. The contact form should render with all its fields visible.

7. **Mobile layout (optional but recommended)**: Resize the browser viewport to 375px width. All sections should stack vertically. Navigation should collapse to a hamburger menu.

Take screenshots and note any issues. Fix them before reporting done.

---

## Step 10 — Report to the User

After build passes and visual test is clean, call `notify_user` with a concise report:

```
✅ [Page Name] page is live at localhost:3000/[route]

Structure:
- Hero: [headline]
- [N] sections: [list]
- Contact form at bottom

Build: passed (0 errors)
Visual test: all sections render correctly

Placeholder items to update:
- [list anything the user needs to supply: real testimonials, real case images, etc.]
```

---

## Appendix: Quick Reference — Real Data to Use in Copy

### Client names (safe to use)

Moovit, Espresso Club, IBI Smart, Israeli Government (IGDS), Pfizer, Afikim, Egged, Mekorot, Intel, Maariv, Daka90, Menora, Clalbit, Isracard, Alliance, WeShoes, Teva, Johnson & Johnson

### Real numbers (safe to use)

- 1.7 billion Moovit users
- 200,000,000+ total users across all Globalbit products
- 150+ projects delivered
- 15+ years of experience
- 50+ engineers, designers, and analysts
- 14 apps reached #1 in their App Store category
- Google Play App of the Year (Moovit)

### Real awards (safe to use)

- Google Play App of the Year
- Apple App Store Editor's Choice
- Multiple industry awards for Moovit and IBI Smart

### MidPageCTA background images

- `/images/services/bg-desktop.webp`
- `/images/services/bg-mobile.webp`

### Client logo images

Check `/public/images/clients/` for available logos before referencing.

### Case images (confirmed to exist)

```
/images/cases/moovit small.png
/images/cases/espresso small.png
/images/cases/IBI Small.png
/images/cases/igds small.png
/images/cases/covid small.png
/images/cases/pfizer small.png
/images/cases/moovit-cover.webp
/images/cases/ibi-smart-cover.webp
/images/cases/espresso-club-cover.webp
/images/cases/israel-gov-design.webp
```

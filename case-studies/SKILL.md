---
name: case-studies
description: |
  Create, rewrite, and strategically improve case study pages on the Globalbit website.
  Covers strategic narrative, Globalbit voice, section structure, component mapping,
  image creation, copy rules, AI pattern removal, SEO/AIO validation, and conversion optimization.

  Use when: creating a new case study page, rewriting existing case study copy,
  improving conversion on a case study, or auditing case study quality.

  Triggers: "rewrite case study", "improve case study", "case study copy",
  "write case study", "audit case study", "case study strategy", "create case study"
---

# Case Study Creation & Rewriting

This skill defines how to create and rewrite case study pages on the Globalbit website.
Every case study tells the story of what Globalbit built, how we built it, and why it matters.

**Before starting, also read:**

- `.agents/skills/copywriting/SKILL.md` — general copy principles
- `.agents/skills/humanizer/SKILL.md` — AI pattern removal checklist

> [!CAUTION]
> **MANDATORY WORKFLOW**: Research → Strategic Narrative → Implementation Plan → **USER APPROVAL** → Execution → Verification.
> Never skip the implementation plan. Never write code before the user approves the plan.

---

## Step 1 — Strategic Narrative (Do This First)

Before touching any code, answer these six questions. Write them in the implementation plan.

### 1. What is the story?

One sentence. This drives everything.

- Pfizer: "Globalbit turned a daily injection battle into a space adventure that kids asked to play"
- WeShoes: "Globalbit rebuilt Israel's biggest shoe chain's entire digital shopping experience"
- Moovit: "Globalbit built the first versions of the app that Intel paid $1B for"

### 2. What should the reader believe after this page?

2–3 beliefs. These drive every copy decision.

- "Globalbit can take an idea from zero to category-defining product"
- "If they built the app Intel paid $1B for, they can build mine"

### 3. Who is the target reader?

Be specific: CTOs, VPs of Product, startup founders, enterprise innovation leads, procurement teams.

### 4. What is the conversion mechanism?

The psychological trigger that makes the reader want to contact Globalbit.

- "If Globalbit built Pfizer's Most Innovative Project, they can handle my regulated product"
- "If they handle 350,000 monthly users for Espresso Club, they can handle my e-commerce"

### 5. What is the philosophy?

The working style you want to communicate.

- "Move fast and refactor" (Moovit)
- "Game design meets clinical precision" (Pfizer)

### 6. What did we do that another agency wouldn't?

This is the most important question. It forces the Globalbit-specific angle.

- Pfizer: "We spent two weeks in clinics watching actual injections before writing a line of code"
- WeShoes: "We killed the product grid and rebuilt navigation from user research — most agencies would've just added better filters"
- IBI: "We built a trading app that handles real-time market data for 500K users — one crash and people lose money"

---

## Step 2 — Research

### Required research before writing

1. **Read the current page** (if rewriting) — `app/cases/[slug]/page.tsx`
2. **Read the Hebrew reference** — `https://globalbit.co.il/projects/[slug]/`
3. **Web search** — find real data: founding year, metrics, acquisitions, awards
4. **Check existing images** — `public/images/case-studies/[slug]/` and `public/images/cases/`
5. **Check `/projects` page** — does the client have an entry? What's the current href?
6. **Check other case studies** — for pattern consistency and to plan `RELATED_CASES`

### Data to collect

- Company name, industry, founding story
- What Globalbit actually built (Hebrew reference is the source of truth)
- Hard numbers: users, revenue, acquisition, timeline
- Awards or recognitions
- Client testimonial (if available)
- Available images and screenshots

---

## Step 3 — Implementation Plan (MANDATORY GATE)

> [!IMPORTANT]
> **STOP HERE.** Write an implementation plan and get user approval before writing any code.

Create an `implementation_plan.md` artifact with:

- The 6 answers from Step 1
- Key data from research
- Proposed section structure with actual headlines
- Hero headline options (propose 2-3)
- Challenge framing
- WHY GLOBALBIT items
- Image plan (what exists, what to generate)
- MidPageCTA copy

**After writing the plan, use `notify_user` with `BlockedOnUser: true` to request approval.**

---

## Step 4 — Section Structure

Every case study page follows this section order. All sections use shared components.

```
1.  PageHero          — Stop the scroll. Biggest proof point in one line.
2.  MetricsSection    — Three numbers that make the reader recalculate.
3.  Intro H2 + <p>    — Converting intro paragraph below metrics.
4.  [Inline Image]    — Product screenshot with text beside it.
5.  TextSection       — THE CHALLENGE. Frame as business risk.
6.  ApproachSection   — HOW Globalbit works. The philosophy.
7.  FeatureSteps      — WHAT WE BUILT. Each item = a decision, not a feature.
8.  [Inline Images]   — More screenshots or product views.
9.  MidPageCTA        — Conversion point. Placed AFTER features.
10. TimelineWorkflow  — PROCESS. Show methodology with real timelines.
11. FeatureCards      — TECH ARCHITECTURE. With background image.
12. FeatureSteps      — WHY GLOBALBIT. Translate story into "hire us."
13. [Testimonials]    — Client quote if available. Use Testimonials component.
14. FeatureCards      — RESULTS. Use darkMode + custom background.
15. CasesSection      — RELATED CASES. 2 cases with tags.
16. Contact           — Final CTA.
```

### Section Value Mapping (MANDATORY before writing copy)

> [!CAUTION]
> **Before writing ANY section**, answer these three questions. If you can't answer them distinctly for each section, your copy will be repetitive.

For **every section** on the page, define:

1. **What belief does this section create?** — Each section must establish ONE specific belief about Globalbit that no other section on this page covers. Examples:
   - Challenge → "This was a hard problem worth solving"
   - Approach → "Globalbit's methodology is unique and proven"
   - What We Built → "Globalbit made specific technical decisions others wouldn't"
   - Results → "The outcomes were measurable and significant"

2. **Have I already said this elsewhere?** — If the same point (even in different words) appears in another section, cut it. Every section must earn its place with a *new* dimension of credibility.

3. **How does this section move the reader toward conversion?** — Map the psychological progression:
   - Hero/Metrics → "I need to keep reading" (curiosity)
   - Challenge → "This is relevant to my problem" (identification)
   - Approach → "These people think differently" (trust in methodology)
   - What We Built → "They made smart, specific calls" (trust in execution)
   - Results → "It worked, at scale" (proof)
   - Why Globalbit → "They're the right partner for me" (decision trigger)

**Anti-pattern to avoid**: Multiple sections all saying "Globalbit is experienced and capable" using different vocabulary. Each section should advance a DIFFERENT argument. If Challenge says "the stakes were high," Approach should NOT also say "the stakes were high" — it should say HOW Globalbit's method addressed those stakes differently than anyone else would.

### Section-by-section copy strategy

#### Hero (`PageHero`)

- Title: outcome-first, specific. The headline IS the case study summary.
- Always include client tag badge.
- CTA: "Get a Free Consultation"

```tsx
<PageHero
    title="We Turned a Needle Into a Space Mission"
    titleClassName="max-w-[900px] text-white"
    useTextReveal={true}
    imageSrc="/images/cases/[slug].webp"
    ctaText="Get a Free Consultation"
    ctaHref="#contact"
>
    <div className="absolute top-[120px] left-4 md:left-6 z-20">
        <span className="inline-block rounded-full bg-white/80 backdrop-blur-sm px-4 py-1.5 text-xs font-bold uppercase tracking-widest text-black/70">
            Client Name
        </span>
    </div>
</PageHero>
```

#### Metrics (`MetricsSection`)

- Exactly 3 metrics. Short labels.
- Best metrics: user count, delivery timeline, business outcome (acquisition/recognition).

#### Intro (Raw HTML)

- Converting H2 + paragraph below metrics. This replaced the old hero description.
- The H2 should be benefit-oriented. The paragraph gives the full story in 3-4 sentences.

```tsx
<div className="w-full max-w-[1440px] mx-auto px-4 md:px-6 py-10 md:py-14">
    <h2 className="text-2xl md:text-4xl font-bold text-neutral-900 mb-4 max-w-[850px]">
        A Mobile Game That Made Children Want Their Injection
    </h2>
    <p className="text-lg md:text-xl leading-relaxed text-neutral-700 max-w-[850px]">
        The story in 3-4 sentences. What Globalbit built, for whom, and why it matters.
    </p>
</div>
```

#### Inline Image + Text

- Product screenshots with context text. Shows the product is real.
- Image on one side, explanation on the other.

```tsx
<div className="w-full max-w-[1440px] mx-auto py-10 md:py-14">
    <div className="flex flex-col md:flex-row items-center gap-4 md:gap-8">
        <div className="w-full md:w-2/3 flex justify-left px-6">
            <img
                src="/images/case-studies/[slug]/screenshot.jpg"
                alt="[Descriptive alt text mentioning the product]"
                className="w-full max-w-[800px] h-auto shadow-lg rounded-3xl"
            />
        </div>
        <div className="w-full md:w-1/2">
            <h3 className="text-xl md:text-2xl font-bold text-neutral-900 mb-4">
                What we built and why it matters
            </h3>
            <p className="text-lg leading-relaxed text-neutral-700">
                Context about this specific feature or screen.
            </p>
        </div>
    </div>
</div>
```

#### Challenge (`TextSection`)

- Title: business language, not technical.
- 3–4 items. Each is a **business risk**, not a feature request.
- closingText: must be project-specific, not generic agency language.

> [!WARNING]
> **Bad closing**: "That meant defining a completely new platform — not patching the old one."
> **Good closing**: "Online, you could look at shoes — you just couldn't shop for them. We needed to build that same browsing energy into a screen."

#### What We Built (`FeatureSteps`)

- Tag: "WHAT WE BUILT" (not "WHAT WE DELIVERED")
- **Every item needs a decision or tradeoff** — not a feature list.
- Show the insight, the argument, or the thing another team wouldn't have done.

> [!IMPORTANT]
> **The test**: if any agency in the world could write this item about their own work, it's too generic. Rewrite it.

| Generic (bad) | Globalbit-specific (good) |
|---|---|
| "Mobile that works one-handed" | "Mobile-first wasn't a buzzword here — our CEO wrote the book on apps people actually use" |
| "Product pages that answer 'Will it fit?'" | "We solved the 'will it fit?' problem — and argued for supplier data to make it work" |
| "One design system for 20+ brands" | "We mapped 20+ brands without losing any of them — Crocs looks like Crocs inside the WeShoes frame" |

#### MidPageCTA (`MidPageCTA`)

- Place AFTER features, not at the bottom.
- Title: question format. Industry-specific.
- Button: "Get a Free Project Estimate"

#### Process (`TimelineWorkflow`)

- Tag: "PROCESS"
- 4 steps with real durations.
- Describe the work, the decisions, the breakthroughs.
- **Never use "Output:"** — that's a template pattern. Describe what happened.

#### Why Globalbit (`FeatureSteps`)

- Tag: "WHY GLOBALBIT"
- Title: "Why [Client] Chose Globalbit for [specific thing]"
- 3–4 items: each backed by evidence from this specific project.

#### Testimonials (`Testimonials`, optional)

- Include when a real client quote exists.
- Place after Why Globalbit, before Results.

```tsx
const TESTIMONIALS_DATA = [
    {
        text: "The actual quote",
        author: "Person Name",
        role: "Title, Company",
        logo: "/images/clients/company-logo.webp",
        photo: "/images/clients/testimonials/Person Name.webp",
    },
];

<Testimonials items={TESTIMONIALS_DATA} title="[Person]'s Take on Working with Globalbit" />
```

#### Results (`FeatureCards`)

- Tag: "RESULTS"
- Use `darkMode` prop and a project-specific background image when available.
- 3–4 items: measurable outcomes, awards, client quotes.

#### Related Cases (`CasesSection`)

- Always 2 cases from the same or adjacent industry.
- Always include `tags` array.

```tsx
const RELATED_CASES = [
    {
        title: "Project Name",
        description: "One-line description",
        image: "/images/cases/slug.webp",
        link: "/cases/slug",
        tags: ["Industry", "Type", "Platform"],
    },
];
```

#### Contact

```tsx
<div className="px-4 md:px-6 pb-12">
    <div className="mx-auto max-w-[1440px]">
        <Contact />
    </div>
</div>
```

---

## Step 5 — Globalbit Voice Rules

This is the difference between a generic agency case study and a Globalbit one.

### Rule 1: "We" > "The app"

Every feature should describe what **we built**, not what the product does.

| Bad | Good |
|-----|------|
| "The app tracks injection sites" | "We built a rotation algorithm that tracks every injection site" |
| "The dashboard shows growth charts" | "The dashboard we built for doctors shows growth charts" |

### Rule 2: Decisions, not features

Each item shows the insight, the tradeoff, or the thing another team wouldn't have done.

| Bad | Good |
|-----|------|
| "We restructured navigation" | "We killed the product grid — most agencies would've just added filters" |
| "We designed for mobile" | "Mobile-first wasn't a buzzword. Our CEO wrote the book on it" |

### Rule 3: Team references

Mention specific roles when it adds credibility: "our game designers", "our backend team", "our UX researchers". Don't overdo it — once or twice per page.

### Rule 4: Honesty markers

Phrases that signal real experience, not marketing:

- "surprised even us"
- "worth the fight"
- "we argued for this internally"
- "tested until kids asked to play again"
- "it took weeks of user research to figure out"

### Rule 5: Specific process details

- "two weeks in clinics watching actual injections"
- "prototyping character concepts until kids said 'can I play again?'"
- "weeks of user research to find the right hierarchy"

### Rule 6: Plain language over consultant-speak

Write like you're explaining the project to a smart friend, not presenting to a board.

| Consultant-speak (bad) | Plain language (good) |
|---|---|
| "Disparate legacy verticals" | "Five different businesses" |
| "Support deflection mandate" | "It had to replace the phone call" |
| "Cohesive frontend paradigm" | "A single product" |
| "Deterministic wireframes" | "Specs developers could build from" |
| "Systematizing enterprise transformation" | "From research to ready-to-build specs" |
| "Dense regulatory environments" | "Complex business rules" |
| "Actionable frontend component structures" | "Detailed blueprints" |

**Test:** Read it out loud. If you'd never say it in a conversation, rewrite it.

---

## Step 6 — Image Creation for Conversion

Images aren't decoration — they're conversion tools. Every image should make the reader believe the project was real, significant, and well-executed.

### Image types (by priority)

| Type | Purpose | When to create | Placement |
|---|---|---|---|
| **Product screenshots** | Proof the thing exists | Always — check `images/case-studies/[slug]/` first | Inline sections |
| **Hero/cover** | Set emotional tone | When no client-supplied hero exists | `PageHero` background |
| **Atmospheric scene** | Show human impact | When no real photos exist | Between sections |
| **Data visualization** | Make results tangible | When metrics drive conversion | Results or inline |
| **Team/process** | Reinforce "we built this" | For trust-building on complex projects | Near Approach/Process |

### Prompt rules (for `generate_image` tool)

1. **Photorealistic for hero/atmospheric** — "cinematic photograph", "shallow depth of field"
2. **No text in generated images** — use HTML overlays instead
3. **Show people using the product** — a child playing a game > a screenshot of a game
4. **Industry-specific lighting** — healthcare = warm, fintech = clean, retail = vibrant
5. **No stock clichés** — no handshakes, no pointing at screens
6. **Context details** — "on a couch with their parent" > "using a tablet"

### Prompt templates

```
Hero (emotional):
"A [cinematic/warm] photograph of [specific person] [doing what] in [setting].
[Lighting]. Photorealistic, high quality. No text overlays."

Atmospheric:
"A [style] showing [real-world scenario the product serves].
[Specific visual details]. [Photography style]. No text."

Product showcase:
"A clean mockup showing [app/dashboard] on [device].
[Setting]. Modern, minimal. No text overlays."
```

### Sizing

- **Phone screenshots**: `max-w-[300px]` with `rounded-[24px] shadow-2xl`
- **Landscape/desktop**: `max-w-[800px]` with `shadow-lg rounded-3xl`
- **Full-width**: `aspect-[16/9]` container with `rounded-[20px] overflow-hidden`
- Always write descriptive alt text mentioning the product name and purpose

### What NOT to generate

- Generic office/team photos
- Abstract illustrations (blog post energy, not case study)
- Images that duplicate text content

---

## Step 7 — Copy Rules

### Voice and tone

- Direct. Confident. Not promotional.
- Write like a senior engineer explaining work to a CTO.
- First person plural ("We built") for Globalbit's work.
- Third person ("WeShoes needed") for the client.

### Sentence structure

- Vary length. Short for impact. Longer for explanation.
- No "By" + gerund openings ("By implementing X, we achieved Y").
- No triple-adjective lists ("fast, reliable, and scalable").

### Specificity

- Every claim needs a number, name, or concrete detail.
- Bad: "significantly improved" → Good: "reduced load from 4s to 800ms"
- Bad: "large user base" → Good: "500,000 active users"

### CTAs

- Hero: "Get a Free Consultation"
- MidPage: "Get a Free Project Estimate" or "Discuss Your Project"
- Never: "Let's Talk", "Contact Us", "Learn More"

---

## Step 8 — AI Pattern Removal Checklist

Run this on every case study. Fix every instance.

### General AI patterns

| Pattern | Example | Fix |
|---------|---------|-----|
| Em dash overuse | "speed — quality — scale" | Use periods or commas |
| Rule of three | "fast, reliable, and scalable" | Vary grouping size |
| Triple negative | "No X, no Y, no Z" | Break rhythm: "There was no X, no Y. Nothing that..." |
| "Seamless/seamlessly" | "seamless integration" | Delete or name the specific mechanism |
| "Cutting-edge/state-of-the-art" | "cutting-edge technology" | Name the actual technology |
| "Dramatically/significantly" | "dramatically improved" | Use a number |
| Negative parallelism | "We didn't just X — we Y" | Flatten: "We Y" |
| "Powerhouse/game-changer" | "digital powerhouse" | Remove or be specific |
| "Testament to" | "a testament to expertise" | Remove entirely |
| "Leveraging/harnessing" | "leveraging AI" | "Using AI" |
| "Innovative/groundbreaking" | "innovative solution" | Describe what makes it innovative |
| "Robust/comprehensive" | "robust platform" | Describe what it does |
| "Ensuring" | "ensuring quality" | Remove or restructure |
| "Output: [deliverable]" | Process step endings | Describe what happened instead |

### Enterprise/consulting jargon (especially common in case studies)

| Jargon | Plain alternative |
|--------|-------------------|
| disparate systems/verticals | separate / different |
| paradigm | approach / model / system |
| encapsulated | handled / covered |
| fault-tolerant | reliable |
| scaffolding | structure / foundation |
| actionable [anything] | [just say what the thing does] |
| deterministic | predictable / clear |
| cohesive | unified / single |
| ecosystem complexity | how many moving parts there are |
| digital transformation | moving [process] online |
| enterprise-scale | large / nationwide |
| multi-vertical / cross-vertical | across [N] business types |
| operational efficiency | fewer people doing the same work |
| aggressive timeline | tight deadline / [N] months |
| dense regulatory environments | complex rules |
| legacy backend systems | old systems |
| human operators | staff / agents / handlers |

---

## Step 9 — Required Code Patterns

### CaseStudyJsonLd (required on every page)

```tsx
import { CaseStudyJsonLd } from "@/components/shared/CaseStudyJsonLd";

<CaseStudyJsonLd
    title="[Client] Case Study — Globalbit"
    url="https://globalbit.co.il/cases/[slug]"
    description="One-line summary of what Globalbit built."
    image="https://globalbit.co.il/images/cases/[slug].webp"
    clientName="[Client]"
    industry="[Industry]"
    keyFacts="Key facts: [metric 1], [metric 2], [metric 3]."
/>
```

### Dynamic Contact import

```tsx
import dynamic from "next/dynamic";
const Contact = dynamic(
    () => import("@/components/layout/Contact").then((mod) => mod.Contact),
    { ssr: true }
);
```

### RELATED_CASES with tags

```tsx
const RELATED_CASES = [
    {
        title: "Project — Subtitle",
        description: "One-line description.",
        image: "/images/cases/slug.webp",
        link: "/cases/slug",
        tags: ["Industry", "Type"],
    },
];
```

---

## Step 10 — Post-Creation Checklist

- [ ] Update `/projects` page entry (href from `/contact` to `/cases/[slug]`, title, description)
- [ ] Add new case to `RELATED_CASES` in 2-3 related case study pages
- [ ] Verify `CaseStudyJsonLd` renders correctly
- [ ] Run humanizer skill on all copy — check for AI patterns
- [ ] Run SEO/AIO validation — meta tags, structured data, heading hierarchy
- [ ] `npx next build` — must pass with zero errors
- [ ] Visual check at `localhost:3000/cases/[slug]`
- [ ] Check mobile rendering (text overflow, image sizing)
- [ ] Confirm MidPageCTA is positioned after features, not at bottom

---

## Quick Reference: Section → Component Mapping

| Section | Component | Tag | Key Props |
|---------|-----------|-----|-----------|
| Hero | `PageHero` | — | `title`, `imageSrc`, `ctaText="Get a Free Consultation"` |
| Metrics | `MetricsSection` | — | `metrics` (3 items) |
| Intro | Raw `<div>` | — | H2 + paragraph |
| Inline Image | Raw `<div>` | — | Image + text side by side |
| Challenge | `TextSection` | THE CHALLENGE | `items`, `closingText` |
| Approach | `ApproachSection` | — | `title`, `text1`, `text2` |
| What We Built | `FeatureSteps` | WHAT WE BUILT | `items`, `gridClassName` |
| CTA | `MidPageCTA` | — | `title`, `buttonText="Get a Free Project Estimate"` |
| Process | `TimelineWorkflow` | PROCESS | `items` (4 steps with durations) |
| Architecture | `FeatureCards` | TECH ARCHITECTURE | `items`, `backgroundImage` |
| Why Globalbit | `FeatureSteps` | WHY GLOBALBIT | `items` |
| Testimonials | `Testimonials` | — | `items`, `title` |
| Results | `FeatureCards` | RESULTS | `items`, `darkMode`, `backgroundImage` |
| Related | `CasesSection` | — | `cases` (2 items with `tags`) |
| Contact | `Contact` | — | Wrapped in padding div |

---
name: blog-articles
description: |
  Write, optimize, and publish blog articles for the Globalbit website in English or Hebrew.
  Covers topic research, SEO structure, copy quality, humanization, image generation,
  data file integration, and build verification.

  Use when: writing new blog posts, rewriting existing articles, creating Hebrew versions,
  or doing bulk article creation.

  Triggers: "write a blog post", "create articles", "add blog content", "write Hebrew articles",
  "blog about [topic]", "new article", "create blog posts"
user-invocable: true
---

# Blog Articles: Writing & Publishing Protocol

**Company**: Globalbit — AI, digital, mobile, and web development company based in Israel.
**Target audience**: CTOs, VPs Engineering, product leaders at mid-to-large enterprises.
**Website**: Next.js (App Router), TypeScript, Tailwind CSS, static export.

This skill covers the full lifecycle of creating blog articles: research → write → optimize → integrate → verify.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Step 1 — Topic Research](#step-1--topic-research)
3. [Step 2 — Article Structure](#step-2--article-structure)
4. [Step 3 — Write the Article](#step-3--write-the-article)
5. [Step 4 — Apply the Humanizer](#step-4--apply-the-humanizer)
6. [Step 5 — SEO Optimization](#step-5--seo-optimization)
7. [Step 6 — Generate the Hero Image](#step-6--generate-the-hero-image)
8. [Step 7 — Add to Data Files](#step-7--add-to-data-files)
9. [Step 8 — Build Verification](#step-8--build-verification)
10. [Step 9 — Report to User](#step-9--report-to-user)

---

## 1. Architecture Overview

### File structure

```
data/
  blog-posts.ts          ← English articles + exports (BlogPost interface)
  blog-posts-he.ts       ← Hebrew articles (hebrewPosts array)

app/blog/
  page.tsx               ← Blog listing page (shows all articles)
  [slug]/
    layout.tsx            ← EN metadata + generateStaticParams (filters out he/ slugs)
    page.tsx              ← EN article renderer (LTR)
  he/[slug]/
    layout.tsx            ← HE metadata + generateStaticParams (he/ slugs only)
    page.tsx              ← HE article renderer (RTL-native)

public/images/blog/       ← Article hero images
```

### BlogPost interface

```typescript
export interface BlogPost {
    slug: string;          // URL slug. EN: "topic-name", HE: "he/topic-name"
    title: string;
    description: string;   // Meta description (150-160 chars)
    date: string;          // ISO 8601 (YYYY-MM-DD)
    dateModified?: string; // Last update date
    lang: "en" | "he";
    oldPath?: string;      // For redirect mapping from old site
    image?: string;        // Hero image path: "/images/blog/slug-name.png"
    content: string;       // Markdown content (escaped in template literal)
    author?: string;       // Author name
    tags?: string[];       // Category tags
}
```

### Routing rules

| Language | Slug format | URL | Data file |
|----------|-----------|-----|-----------|
| English | `topic-name` | `/blog/topic-name` | `data/blog-posts.ts` → `enPosts` array |
| Hebrew | `he/topic-name` | `/blog/he/topic-name` | `data/blog-posts-he.ts` → `hebrewPosts` array |

### Content format

Articles use **simplified markdown** rendered by the page component:

- `## Heading` → H2
- `### Subheading` → H3
- `**bold text**` → bold
- `*italic text*` → italic
- `[text](url)` → link
- `- item` → unordered list
- `1. item` → ordered list
- Double newline (`\n\n`) → paragraph break

No HTML, no code blocks, no images inside content. Keep it simple.

---

## Step 1 — Topic Research

### 1a. Understand the target reader

Every article targets one of these personas:

- **CTO / VP Engineering** at a 100-500 person company considering outsourcing
- **Product leader** evaluating technology partners
- **Technical decision-maker** researching a specific technology or approach

Before writing, answer:

- **Who is reading this?** Be specific about role, company size, and situation.
- **What problem are they Googling?** This determines the title and H2 structure.
- **What should they do after reading?** Usually: contact Globalbit.

### 1b. Research the topic

Use `search_web` to find:

- Current industry data and statistics (cite real numbers)
- Common misconceptions or outdated advice
- What competitors write about this topic (to differentiate)
- Real-world examples Globalbit can reference

### 1c. Check existing articles

Before writing, check `data/blog-posts.ts` and `data/blog-posts-he.ts` to avoid duplicating topics.

---

## Step 2 — Article Structure

### Section Belief Mapping (before writing)

Before writing, define what the reader should believe after each major section:

1. **Opening** — What problem belief? ("This is relevant to my situation")
2. **Core section 1** — What expertise belief? ("These people understand this deeply")
3. **Core section 2** — What action belief? ("I know what to do now")
4. **FAQ** — What trust belief? ("They answered my exact objection")
5. **CTA** — What next-step belief? ("Contacting them is the logical next step")

Each section must advance a DIFFERENT argument. If two sections say the same thing in different words, cut one.

### Article skeleton

Every article follows this skeleton:

```
## [Opening section — name the problem or opportunity]
First 2-3 paragraphs: hook the reader. State the problem clearly.
Connect it to their business reality.

## [Core section 1 — the substance]
The main argument, analysis, or framework.
Use H3 subheadings to break into digestible parts.

### [Subsection]
Concrete details. Real examples. Numbers.

### [Subsection]
More substance.

## [Core section 2 — practical application]
How this applies to the reader's situation.
What they should actually do.

## [Optional: section 3 — deeper analysis or comparison]

## שאלות נפוצות (Hebrew) / Frequently Asked Questions (English)
3-5 Q&A pairs. Answer real objections.
End the last answer with a CTA link.
```

### Structure rules

1. **1,200-2,500 words.** Long enough to be substantive, short enough to finish.
2. **No H1.** The page component renders the `title` field as H1. Start content with H2.
3. **H2 for major sections, H3 for subsections.** Never skip levels.
4. **FAQ section at the end.** Use bold for questions: `**Question text?**` followed by the answer.
5. **CTA in the last FAQ answer.** Link to `/contact` or a relevant service page.
6. **No fluff introductions.** Start with the problem or a striking fact. No "In today's landscape..."

---

## Step 3 — Write the Article

### Before reading this section

Read these skills first (they contain the detailed rules you must follow):

1. **Copywriting skill** (`/.agents/skills/copywriting/SKILL.md`) — for headline rules, CTA copy, voice/tone
2. **Humanizer skill** (`/.agents/skills/humanizer/SKILL.md`) — for detecting and removing AI writing patterns

### English articles

- Write in clear, direct English. No corporate jargon.
- Use active voice. Short sentences. Concrete examples.
- Reference Globalbit's real projects: Moovit (1.7B users), IBI Smart (#1 trading app), Psika.ai (legal AI), Espresso Club, government projects.
- Author names: use real team members — "Vadim Feinstein" (CEO), "Sasha Feldman" (CTO/technical).

### Hebrew articles

> [!IMPORTANT]
> Hebrew articles are **original content written in Hebrew**, NOT translations of English articles.
> Write in natural, idiomatic Israeli Hebrew. Think Haaretz op-ed, not Google Translate.

- Write directly in Hebrew from scratch.
- Use Israeli tech slang naturally (פרודקשן, דיבאג, דיפלוימנט).
- Keep English terms where Hebrew alternatives sound forced (AI, API, DevOps, CRM, ROI).
- Slug format: `he/topic-name` (the `he/` prefix is mandatory).
- Author names in Hebrew: "ודים פיינשטיין", "סשה פלדמן".
- CTA links use the same English paths (`/contact`, `/ai-consulting`).

### Content quality checklist

Before moving to the next step, verify:

- [ ] Opens with a concrete problem or striking statistic
- [ ] Contains at least 2 real Globalbit project references
- [ ] Every claim has a number or specific example behind it
- [ ] FAQ section has 3-5 questions
- [ ] Last FAQ answer includes a CTA link
- [ ] No placeholder text or TODO markers
- [ ] Word count is 1,200-2,500

---

## Step 4 — Apply the Humanizer

After writing, run the content through the humanizer checklist from `/.agents/skills/humanizer/SKILL.md`.

### Quick humanizer check (minimum)

Scan and fix these AI writing patterns:

1. **Rule of three** — Delete lists that always group exactly three items
2. **Em dashes** — Replace with commas, periods, or parentheses
3. **AI vocabulary** — Remove: "delve", "crucial", "landscape", "robust", "leverage", "tapestry", "multifaceted", "pivotal", "holistic", "cutting-edge", "game-changer", "at its core"
4. **Promotional language** — Cut superlatives without evidence
5. **Negative parallelisms** — "not just X, but Y" → rewrite directly
6. **Conjunctive phrases** — Reduce "Furthermore", "Moreover", "Additionally"
7. **Symmetrical structures** — Vary sentence length and structure
8. **Vague attributions** — "Experts say..." → name the source or delete

### Hebrew-specific humanizer rules

- No literal Hebrew translations of English idioms
- Vary sentence openings (don't start 3 paragraphs with the same word)
- Use conversational connectors naturally (אז, כלומר, בקיצור) but don't overuse
- Avoid the robotic ה-definite-article stacking common in machine translation

---

## Step 5 — SEO Optimization

Apply these SEO rules (derived from `/.agents/skills/seo-audit/SKILL.md`):

### Title and meta description

- **Title**: 50-60 characters. Include primary keyword. Outcome-focused.
- **Description**: 150-160 characters. Summarize the article's value proposition. Include a reason to click.

### Heading structure

- One clear topic per H2 section
- Target keywords in at least 2 H2 headings (naturally, not stuffed)
- H3 for subsections — helps featured snippets

### Content SEO

- Primary keyword in the first 100 words of content
- Related keywords spread naturally throughout
- Internal links to Globalbit service pages where relevant
- FAQ section targets "People Also Ask" queries

### Technical SEO (handled by layout.tsx)

The layout files automatically handle:

- `og:type: article`
- `og:locale` (en_US or he_IL)
- `hreflang` alternates between EN and HE versions
- `canonical` URL
- JSON-LD `BlogPosting` schema (in page.tsx)

---

## Step 6 — Generate the Hero Image

Every article needs a hero image.

```
Path: /public/images/blog/{slug-without-he-prefix}.png
```

Use the `generate_image` tool to create the image:

- Style: modern, abstract, professional
- No text in the image (the title overlays it)
- Relevant to the article topic
- Landscape aspect ratio (roughly 21:9)
- Dark or muted tones work best (text overlays in white/light)

After generating, copy the image to `public/images/blog/`:

```bash
cp /path/to/generated/image.png public/images/blog/slug-name.png
```

Set the `image` field in the BlogPost data to `/images/blog/slug-name.png`.

---

## Step 7 — Add to Data Files

### English articles

Add to the `enPosts` array in `data/blog-posts.ts`:

```typescript
{
    slug: "your-article-slug",
    title: "Your Article Title",
    description: "150-160 char meta description.",
    date: "2025-06-15",       // Publication date
    dateModified: "2026-01-10", // If updating an older article
    lang: "en",
    author: "Vadim Feinstein",
    tags: ["AI", "Enterprise"],
    image: "/images/blog/your-article-slug.png",
    content: `## Your first H2 heading

Your content here using simplified markdown.

## FAQ

**Question one?**
Answer one.

**Question two?**
Answer two with a [CTA link](/contact).`,
},
```

### Hebrew articles

Add to the `hebrewPosts` array in `data/blog-posts-he.ts`:

```typescript
{
    slug: "he/your-article-slug",     // he/ prefix is mandatory
    title: "כותרת המאמר שלכם",
    description: "תיאור מטא של 150-160 תווים.",
    date: "2025-06-15",
    lang: "he",                        // must be "he"
    author: "ודים פיינשטיין",
    tags: ["AI", "Enterprise"],
    image: "/images/blog/your-article-slug.png",  // same image as EN version if applicable
    content: `## הכותרת הראשונה שלכם

תוכן המאמר כאן.

## שאלות נפוצות

**שאלה ראשונה?**
תשובה ראשונה.

**שאלה שנייה?**
תשובה שנייה עם [קישור ליצירת קשר](/contact).`,
},
```

### Escaping rules for content template literals

- Use backtick-delimited template literals (`` `content` ``)
- Escape any backticks inside content with `\``
- Escape `${` sequences with `\${`
- No need to escape quotes, apostrophes, or other characters

---

## Step 8 — Build Verification

Run this command and wait for it to complete:

```bash
npx next build 2>&1 | tail -40
```

The build must exit with code 0. Check that your new article slug appears in the output under the generated paths.

### Common errors

| Error | Fix |
|---|---|
| `Template literal syntax error` | You have an unescaped backtick or `${` in the content string |
| `Module not found` | Wrong import path |
| `Type error on BlogPost` | Missing required field (slug, title, description, date, lang, content) |
| Build hangs | Content string is malformed — check for unclosed template literals |

---

## Step 9 — Report to User

After the build passes, notify the user:

```
✅ [N] articles published

| # | Title | Slug | Lang |
|---|-------|------|------|
| 1 | ... | ... | EN/HE |

Build: passed (exit 0)
All article routes generated successfully.
```

---

## Appendix A: Quick Reference — Real Data for Articles

### Client references (safe to use)

- Moovit: 1.7 billion users, #1 transit app globally, Google Play App of the Year
- IBI Smart: #1 trading app in Israel, 600,000+ users
- Espresso Club: digital transformation, #2 coffee brand in Israel
- Psika.ai: legal AI, 40% reduction in research time per case
- Israeli Government Design System: national UX standards
- Pfizer: "top innovative project" recognition

### Company numbers

- 50+ engineers, designers, analysts
- 15+ years of experience
- 150+ projects delivered
- 200,000,000+ users across all products
- 14 apps reached #1 in their category

### Author names

| English | Hebrew | Role |
|---------|--------|------|
| Vadim Feinstein | ודים פיינשטיין | CEO |
| Sasha Feldman | סשה פלדמן | CTO / Technical |

### Service page links for CTAs

- `/contact` — general contact
- `/ai-consulting` — AI consulting
- `/product-development` — product development
- `/mobile-development` — mobile apps
- `/web-development` — web development
- `/legacy-systems-modernization` — legacy modernization

---

## Appendix B: Batch Article Creation

When creating multiple articles at once:

1. **Plan all topics first.** List titles, target keywords, and personas.
2. **Write in batches of 3-5.** This allows quality control between batches.
3. **Alternate authors.** Don't attribute all articles to one person.
4. **Vary publication dates.** Spread dates across weeks/months for a natural publishing cadence.
5. **Cross-link articles.** Reference other Globalbit blog posts where relevant.
6. **One build at the end.** Don't rebuild after each article — add all to data files, then build once.

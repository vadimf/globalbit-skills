# Pfizer Case Study — Annotated Reference

This file documents the Pfizer/Genotropin case study as the reference implementation
for the skill. Comments explain **why** each section works.

---

## Strategic Answers (Step 1)

| Question | Answer |
|---|---|
| **Story** | Globalbit turned a daily injection battle into a space adventure kids asked to play |
| **Belief** | "If Globalbit built Pfizer's Most Innovative Project, they can handle my regulated product" |
| **Reader** | Pharma innovation leads, digital health product owners |
| **Conversion** | The Pfizer 2015 award creates instant credibility |
| **Philosophy** | Game design meets clinical precision |
| **What we did differently** | Spent two weeks in clinics before writing code. Game designers + child psychologists working together |

---

## Section Breakdown

### 1. Hero

```
Title: "We Turned a Needle Into a Space Mission"
```

**Why it works**: Emotional, specific, tells the story in 8 words. The contrast (needle → space mission) creates curiosity.

### 2. Metrics

```
"Pfizer 2015" — Most Innovative Project
"Daily Game" — children initiated treatment through play
"Real Data" — first-ever injection compliance tracking
```

**Why it works**: The Pfizer award leads. "Daily Game" is unexpected for a medical product. "Real Data" speaks to the CTO reader.

### 3. Intro

```
H2: "A Mobile Game That Made Children Want Their Injection"
```

**Why it works**: States the impossible-sounding result. Two paragraphs give the full story:

- Paragraph 1: How we started (clinic visits, team assembly) — **Globalbit voice**
- Paragraph 2: What we built (I Grow, the mechanics) — **product description**

### 4. Inline Image + Text

```
Image: pfizer_1.jpg (superhero characters in space)
H3: "We built a universe kids would come back to"
```

**Why it works**: The H3 says "we built" (not "the app features"). The text mentions
"our game designers" and "child development principles" — team references that
build credibility.

### 5. Challenge

```
Tag: THE CHALLENGE
Title: "Daily Injections, Nightly Battles, Zero Data"
```

Items are framed as human problems, not technical ones:

- "Kids fight the needle" — parents relate
- "Injections cluster in the same spots" — medical consequence
- "Doctors are flying blind" — the data gap

**closingText** is a parent quote: "Parents told us the hardest part wasn't the medical side..."
This is project-specific. It couldn't appear on any other case study.

### 6. Approach

```
Title: "What If the Child Actually Wanted the Injection?"
```

**Why it works**: Questions make better titles than statements for approach sections.
text1 explains the insight (reminders weren't the problem, dread was).
text2 explains the game loop mechanics.

### 7. What We Built

```
Tag: WHAT WE BUILT
Title: "A Game That Tracks, Rotates, and Reports"
Description: "We built I Grow as three systems in one..."
```

5 items. Each starts with what it IS, then explains the clever mechanics:

- "A game kids actually want to play" — not "gamification module"
- "The hero needs the injection to fly" — the design insight
- "Body mapping with built-in rotation" — the technical innovation
- "Real clinical data, securely delivered" — the backend
- "Doctor dashboard with growth tracking" — the physician layer

### 8. Inline Images (Clinical Data)

Two phone screenshots side by side showing growth charts.
H3: "The dashboard we built for doctors" — "we built" again.
Text mentions "our backend team" — team reference.

### 9. MidPageCTA

```
Title: "Building a healthcare product that patients actually use?"
Description: "We've designed compliance solutions for Pfizer, Johnson & Johnson, and Teva."
```

**Why it works**: Name-drops 3 pharma clients. Industry-specific question.

### 10. Process

4 steps with real durations. Note: descriptions explain the work, not "Output: [deliverable]".

- "Clinical research and pediatric UX — 6 weeks"
- "Game design and character development — 8 weeks"

### 11. Tech Architecture

Background image used for visual weight. 4 pillars:

- Medical-Grade Data Security
- Injection Site Algorithm (proprietary)
- Gamification Engine
- Physician Analytics Platform

### 12. Why Globalbit

```
Title: "Why Pfizer Chose Globalbit for a Pediatric Health Product"
Description: "Pharma companies don't hand patient-facing products to agencies that haven't worked in regulated healthcare before."
```

4 items. Each backed by THIS project's evidence:

- "We've built for pharma before" — names 3 companies
- "We design products that children use" — two-user challenge
- "Game design meets clinical precision" — the core differentiator
- "We delivered a product, not a prototype" — shipped in 6 months

### 13. Results

```
Title: "The Nightly Battle Became a Nightly Ritual"
```

darkMode + background image. 4 items including an actual App Store review quote.
The quote is real social proof — stronger than any metric we could write.

### 14. Related Cases

Healthcare-adjacent: Savyon Diagnostics + TokiDoc. Both have `tags` arrays.

---

## Key Patterns to Replicate

1. **"We" appears 15+ times** in copywriting — not "the app" or "the system"
2. **Team references**: "our game designers", "our backend team", "our CEO"
3. **Process details**: "first two weeks in clinics", "tested with real families"
4. **Project-specific closing quotes** — no generic agency lines
5. **Inline images**: product screenshots with explanatory text, not just decoration
6. **Questions as approach titles**: "What If the Child Actually Wanted the Injection?"

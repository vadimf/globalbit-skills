# Typography and Punctuation Reference

Exact characters Globalbit uses in Hebrew documents. Most rendering bugs in client-facing copy come from the wrong character (a hyphen where an em-dash is expected, an ASCII apostrophe where a geresh is expected). This file is the source of truth.

## Special characters — the locked five

| Name | Glyph | Unicode | Use |
|---|---|---|---|
| Em-dash | `—` | U+2014 | Sentence-level separator: feature — value, fact — meaning, name — definition. Always with spaces: ` — ` |
| Geresh | `׳` | U+05F3 | Foreign-origin Hebraicised words: `צ׳אט`, `פיצ׳ר`, `ג׳קט`, `צ׳קליסט` |
| Gershayim | `״` | U+05F4 | Hebrew acronyms: `מע״מ`, `לו״ז`, `ש״ח`, `קק״ל`, `דו״ח`, `דו״ח שעות`, `דב״ש` |
| Hebrew comma | `,` | U+002C | Standard Western comma, same as English |
| Maqaf-like hyphen | `-` | U+002D | Used as glue between numbers and units: `30 יום`, `2-3 שבועות`, `200 מיליון` |

Do not use:

- `'` ASCII apostrophe (U+0027) instead of geresh — wrong
- `"` ASCII quote (U+0022) instead of gershayim — wrong (only acceptable inside English-language quotes)
- `–` en-dash (U+2013) — never; em-dash or hyphen only
- `−` minus sign (U+2212) — never in body copy
- `…` ellipsis (U+2026) — avoid; usually a sign of unfinished thought

## When to use the em-dash vs. hyphen

| Situation | Use | Example |
|---|---|---|
| Defining or explaining a term | em-dash with spaces | `AI Knowledge Hub — פלטפורמת AI ארגונית מאובטחת` |
| Connecting feature to business value | em-dash with spaces | `המערכת תזהה דפוסי עניין — מודיעין שיווקי ומכירתי מדויק.` |
| Positioning (affirmative) | em-dash with spaces | `הפורטל הוא שכבת השירות הדיגיטלית של Focus מול לקוחותיה.` |
| Numeric range | hyphen, no spaces | `5-7 שבועות`, `130,000-160,000 ₪` |
| Compound with number unit | hyphen, no spaces | `30-יום`, `RTL-First`, `2.5-חודשים` (only when modifying a noun) |
| Compound with English term | hyphen | `AI-First`, `Cloud-Native`, `End-to-End` |
| Phase label | hyphen | `MS-0`, `MS-1` |

The em-dash carries the Globalbit voice. It is the most common piece of punctuation after the period. Get this character right.

## Quotation marks

Globalbit documents use two patterns; pick one per document and stay consistent.

**Pattern A — Straight ASCII double quotes (most common):**

> ההגדרה של "ליד חם" שונה בכל ארגון.

**Pattern B — Hebrew gershayim quotes (more formal):**

> ההגדרה של ״ליד חם״ שונה בכל ארגון.

Single quotes are rare. When quoting English inside Hebrew, use ASCII straight double quotes and keep the English untouched:

> Microsoft's "Azure OpenAI" service runs inside the tenant.

## Numbers and units

### Thousands separator

Western comma every three digits. No alternative.

- ✓ `1,600`, `28,000`, `200,000,000`
- ✗ `1.600`, `1 600`, `1600`

### Decimal point

Western period.

- ✓ `2.5 חודשים`, `1.5 שעות`
- ✗ `2,5 חודשים`

### Numbers in flowing text vs. tables

- Flowing text up to ten: spell out optional, but digits are equally accepted when paired with a unit. `3 שבועות` is preferred over `שלושה שבועות` in business writing.
- Tables, headlines, scope items, prices, dates, hours, percentages: always digits.

### Percentages

`60%`, no space, no spelling.

- ✓ `קיצור זמני פיתוח בעד כ-60%`
- ✗ `60 %`, `60 אחוז`

### Currency

| Currency | Form | Example |
|---|---|---|
| Shekel symbol | `₪` after digits, with a space | `28,000 ₪` |
| Shekel word | `ש״ח` after digits, with a space, gershayim mandatory | `28,000 ש״ח` |
| Dollar | `$` before digits | `$400` |
| Dollar word | `דולר` after digits, with a space | `400 דולר` |
| VAT note | `כל המחירים אינם כוללים מע״מ` — always in a separate line at the bottom of the commercial block | (boilerplate) |
| Range | hyphen, no spaces | `130,000-160,000 ₪` or `130,000 – 160,000 ש״ח` (formal long form) |

When pairing two currencies (e.g. cloud spend in dollars inside a Hebrew document), keep both forms:

> עלות התשתית החודשית המשוערת צפויה לנוע בטווח של **400–600 דולר לחודש**.

### Time and dates

| Form | Example | Notes |
|---|---|---|
| Working day | `2 ימי עבודה` | Always pair with `ימי עבודה`, not `ימים`, when meaning business days. |
| Calendar day | `30 יום קלנדריים` | Specify `קלנדריים` only if the contrast with working days matters. |
| Weeks | `5-7 שבועות` | Range with hyphen. |
| Months | `2.5 חודשים`, `כ-4 חודשים` | Decimal months acceptable. |
| Year | `שנת 2026` | Always digits. |
| Hours | `12 שעות עבודה בפועל` | Use `בפועל` when the cap is on actual recorded hours. |

Hedging time estimates: `כ-`, `כ‐`, `מוערך בכ-`, `בטווח של`, `צפוי`. All preceded by a hyphen-glue to the number: `כ-280 שעות`, `כ-3 שבועות`.

## Hebrew acronyms — the gershayim rules

The `״` character sits between the second-to-last and last letter of a Hebrew acronym. ASCII `"` will look wrong on every rendered surface.

| Word | Wrong | Right |
|---|---|---|
| Value-added tax | `מע"מ`, `מע'מ` | `מע״מ` |
| Schedule | `לו"ז`, `לוז` | `לו״ז` |
| Shekel | `ש"ח` | `ש״ח` |
| KKL | `קק"ל` | `קק״ל` |
| Report | `דו"ח` | `דו״ח` |
| MAYUEHL | `מנכ"ל` | `מנכ״ל` |
| Israel | `יש'ראל` | (no acronym — write `ישראל`) |

When inserting these in markdown, paste the actual gershayim character. Don't rely on the text input to convert.

## Geresh on Hebraicised foreign words

The `׳` character (apostrophe-shaped) is required on these common Globalbit terms:

| Word | Required form | Notes |
|---|---|---|
| Chat | `צ׳אט` | Never `צאט`, never `צ'אט` (ASCII apostrophe). |
| Feature | `פיצ׳ר` / `פיצ׳רים` | Only acceptable for "feature" in non-engineering contexts; engineers prefer English. |
| Cheque | `צ׳ק` | Rare in Globalbit documents. |
| George | `ג׳ורג׳` | Names. |
| Chip | `צ׳יפ` | Rare. |
| Gel | `ג׳ל` | Rare. |

When in doubt, leave the term in English: `chat` is fine; `צ׳אט` is required when the term is in a Hebrew clause where the English form would jar.

## Bold and emphasis

Markdown bold `**text**` is the only emphasis Globalbit uses.

- No italics (renders inconsistently in Hebrew).
- No underline.
- No ALL CAPS in Hebrew (impossible in Hebrew anyway, but the rule extends to inline English: don't write `THIS IS IMPORTANT`).
- No coloured text inside the body. Colour belongs to the visual layer, not the copy.

Where to use bold:

- Section subtitles: `## **שלב 1 — הקמה והפעלה**`
- Bullet leads (Shape A): `- **שיפור חוויית השירות** — ...`
- Inline emphasis on a single key noun phrase: `הפלטפורמה מהווה **תשתית אסטרטגית**, לא פתרון נקודתי.`
- Numbers in tables: bold only when they're the row's main fact.

Do not bold whole sentences or paragraphs. Bold loses meaning when overused.

## Bullets and lists

Two acceptable bullet markers:

- `-` (hyphen + space) — preferred for most lists
- `•` (Unicode bullet) — acceptable in some published Hebrew layouts, but inside source documents prefer the hyphen for portability

Inside a bullet:

- Sentence case (no Title Case in Hebrew, since Hebrew has no case).
- No terminal punctuation if the bullet is a noun phrase.
- Period only if the bullet is a full sentence and other bullets in the same list are also full sentences. Consistency wins.
- No semicolons between bullets.

Nested lists: indent two spaces. Two levels max in body; three levels is a sign the list should become prose or a table.

## Headers

Hebrew headers use markdown `#` with bold inside, in the proposal-document style:

```
# **תקציר מנהלים**
## **1. רקע והקשר עסקי**
### **רכיב 1 — מנוע פרוטוקולים גרפי**
```

For section numbers, the markdown-escaped form `# 1\. כותרת` is the historical pattern (it disables markdown's numbered-list rendering inside a heading). Either is acceptable; pick one per document.

## Tables

Globalbit's Hebrew tables follow markdown's pipe-separator syntax. Three locked patterns:

**Pricing block:**

```
| **תפקיד** | **תעריף שעתי (₪)** |
| :-: | :-: |
| מנכ״ל / מנהל טכני | 380 ₪ |
| מנהל פרויקט | 322 ₪ |
```

**Risk register:**

```
| **סיכון** | **חומרה** | **הסתברות** | **רמת סיכון** | **גידור** |
| :-: | :-: | :-: | :-: | :-: |
| עיכוב באספקת נתונים | 4 | 3 | בינוני | Template ב-Discovery, לוח זמנים ברור |
```

**Milestones:**

```
| **אבן דרך** | **שבוע** | **תוצר** | **תנאי סיום** |
| :-: | :-: | :-: | :-: |
| MS-0 — Kickoff | 0 | התנעת פרויקט | פגישת פתיחה |
```

Header cells are bolded. Cells are centred (`:-:`) by default in Globalbit's published proposals.

## Linebreaks inside cells

When a cell needs a soft break, use markdown's two-space-and-newline pattern, or HTML `<br/>`. Both are acceptable; pick one per document. In source files, the two-space pattern is more portable.

## Common rendering bugs to scan for

Before delivering Hebrew copy, ctrl-F for these:

| Pattern | Likely bug | Fix |
|---|---|---|
| `'` | ASCII apostrophe — usually a missing geresh in `צ'אט` or missing gershayim in `מע'מ` | Replace with `׳` or `״` |
| `"` (around Hebrew acronym) | Missing gershayim | Replace with `״` |
| ` - ` (hyphen with spaces) | Usually meant to be em-dash | Replace with ` — ` |
| `–` | En-dash never appears in Globalbit Hebrew | Replace with `-` or `—` based on use |
| `5 %` | Stray space before percent | Remove the space |
| `₪28,000` | Currency symbol before digits | Flip to `28,000 ₪` |
| double `מאוד` or `ביותר` | Forbidden intensifier | Rewrite with a stronger noun/verb |
| `!` | Forbidden punctuation | Rewrite into a calm statement |
| `?` (rhetorical) | Forbidden in body | Convert to a statement |

A clean scan on these eight patterns catches >90% of typography drift.

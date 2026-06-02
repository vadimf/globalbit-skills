---
name: globalbit-hebrew
description: Globalbit's Hebrew writing standard — the exact register, lexicon, syntax, and typography used in Globalbit's client-facing proposals and documents. Use whenever writing or rewriting Hebrew copy for Globalbit (proposals, PRDs, architecture documents, clarifying-question lists, executive summaries, scope sections, commercial terms, client emails). Trigger phrases: "כתוב בעברית של גלובלביט", "תרגם להצעה של גלובלביט", "make this sound like a Globalbit proposal", "Hebrew copy for Globalbit", "rewrite in Globalbit Hebrew", "סגנון גלובלביט". This skill defines the LANGUAGE standard (tone, words, sentences, punctuation) — not the document structure, which is owned by `create-proposal`.
---

# Globalbit Hebrew Writing Standard

This skill captures how Globalbit writes Hebrew — the choices that make a paragraph "sound like Globalbit" regardless of which section it sits in.

Defer document structure, section ordering, and commercial templates to the `create-proposal` skill. This skill answers only: **given that I need to write this sentence in Hebrew, how does it have to read?**

---

## 1. Register (the most important rule)

Globalbit Hebrew is **professional business Hebrew** (`עברית עסקית-מקצועית`) — the register of a senior consultant briefing an executive committee. It is:

- **Formal but not legal.** Avoid courtroom Hebrew (`הואיל ו...`, `מכוח האמור`). Avoid colloquial Hebrew (`סבבה`, `אחי`, `וואלה`, `יאללה`, `בקטנה`). Slang is forbidden, even softened.
- **Measured.** Confidence comes from precise nouns and verbs, not adjectives. Drop `מאוד`, `ביותר`, `הכי`, `סופר-`, `אדיר`. Prefer `משמעותי`, `מהותי`, `מהותית`, `ברמה הגבוהה ביותר`, `מובהק`.
- **Third-person institutional + inclusive first-person plural.** The company refers to itself in the third person ("גלובלביט מציעה", "גלובלביט תבצע") AND in inclusive "we" ("אנו מציעים", "אנו מאמינים"). Both modes coexist in the same document. Use third-person when stating commitments or scope; switch to `אנו` / `אנחנו` when describing values, method, or relationship.
- **Calm.** No exclamation marks. No rhetorical questions. No emoji. No bold-uppercase shouting.
- **Hedged in estimates, decisive in commitments.** Numbers, scopes, timelines: hedge with `כ-`, `מוערך`, `צפוי`, `בטווח של`. Commitments and obligations: state flatly (`גלובלביט מתחייבת`, `הלקוח ימנה`).

If a sentence could appear in a WhatsApp message between friends, it's too informal. If it could appear in a court summons, it's too legal.

---

## 2. Voice and grammatical person

| Use | When | Example |
|---|---|---|
| `גלובלביט` (3rd person, feminine singular) | Stating company commitments, scope, methodology | `גלובלביט תספק תיעוד מלא` |
| `אנו` / `אנחנו` (1st person plural) | Values, beliefs, approach, relationship framing | `אנו רואים בפרויקט זה...` |
| `[Client name]` then later `החברה` / `הארגון` | Referring to the client; rotate to avoid repetition | First mention: `מהדרין`. Later: `החברה` / `הארגון` |
| Passive (`יבוצע`, `יוקם`, `יסופק`) | When the actor is obvious or institutional | `בדיקות הקבלה יבוצעו על-ידי הלקוח` |
| Future tense (`ת/יפתח`, `תכלול`) | Default tense for everything that will happen post-signing | `המערכת תכלול שלושה מודולים` |

**Address the reader.** Never use `אתה` / `אתם` to address the reader. The client is named by company name, then by `החברה`, `הארגון`, or implied through the verb. Never `you`.

---

## 3. Lexicon — canonical word choices

These choices are non-negotiable. Use the left column; never the right.

| Use | Avoid |
|---|---|
| מערכת / פלטפורמה / פתרון | אפליקציה (unless specifically a mobile app), תוכנה |
| תשתית | מערך, סביבה (when meaning infrastructure) |
| מקצה לקצה | "אנד טו אנד", "מההתחלה ועד הסוף" |
| ערך עסקי / משמעות עסקית | "תועלת", "יתרון" (when stating ROI to the business) |
| לאורך זמן | "לטווח רחוק", "לעתיד הרחוק" |
| לאורך הפרויקט | "לכל אורך הפרויקט" |
| כבר מהיום הראשון | "מהתחלה", "מההתחלה ממש" |
| מבוסס AI / מבוסס נתונים | "AI-based" inline (use Hebrew with English term in caps) |
| ברמת Enterprise / ארגונית | "ברמה גבוהה" (when meaning enterprise-grade) |
| מוקשח / מאובטח | "סופר-מאובטח", "חזק" |
| סקלאבילי / ניתן להרחבה | "סקייל", "מתרחב" (use Hebrew where natural) |
| ייעודי | "ספציפי", "ייחודי" (when meaning purpose-built) |
| ממוקד | "פוקוס", "ממוקד מטרה" |
| מקצועי | "פרופסיונלי" |
| בלוח זמנים קצר וממוקד | "מהר", "במהירות" alone |
| צוות מנוסה / צוות בכיר | "צוות חזק", "צוות מקצועי" (overused) |
| תוצר | "פלט", "deliverable" inline |
| היקף / תכולה | "סקופ" |
| אישור | "סיין-אוף", "approval" inline |
| הטמעה | "אינטגרציה" when meaning rollout/adoption |
| אינטגרציה | when meaning system-to-system connection |

See `references/glossary.md` for the full canonical mapping including AI/SaaS/security/finance term lists.

---

## 4. Sentence shape

### 4.1 The "value-then-meaning" two-beat

The dominant rhetorical move in Globalbit Hebrew is the **two-beat sentence**:

> **Beat 1:** state what the system / approach does (technical or factual).
> **Beat 2:** state what it means for the client (business impact).

Connect the beats with `—` (em-dash), `כך ש-`, `המאפשר`, `על מנת ש-`, `במטרה ל-`. Weave the business value into the sentence itself — never break it out into a separate labelled line.

Example:

> מנגנון ה-Audit מתעד כל פעולה במערכת באופן בלתי ניתן לשינוי — כך שלכל החלטה ניתן לחזור, להסביר ולבקר.

### 4.2 Sentence length

- **Opening paragraphs (תקציר מנהלים, רקע):** long periodic sentences — 25–40 words each, with embedded clauses. They build authority.
- **Capability bullets:** short — 8–15 words. Each bullet states one thing.
- **Commercial / legal sections:** medium, structured. Each obligation gets its own sentence.

Vary within a paragraph: two long sentences, then one short for punch. Never write five short sentences in a row — it reads like marketing copy, not consulting.

### 4.3 Connectors

Prefer these connectors; they carry the register:

- `תוך כדי`, `תוך שמירה על`, `תוך שילוב`, `תוך הקפדה על`
- `במקביל`, `בנוסף`, `יחד עם זאת`, `לצד`
- `כך ש-`, `על מנת ש-`, `במטרה ל-`, `מתוך מטרה ל-`
- `בהתאם ל-`, `בכפוף ל-`, `בהסתמך על`
- `המאפשר ל-`, `המהווה`, `המספק`, `שעליו ניתן ל-` (affirmative expansion)

Avoid: `וגם`, `אז`, `אבל` at sentence start, `כי` (use `שכן`, `מאחר ש-`, `היות ש-`), `בגלל ש-` (use `מאחר ש-`). Also avoid the contrast connectors `במקום X — Y` and `לא רק X — אלא Y` — Globalbit copy positions affirmatively (see §4.4), never by what the offer is not.

### 4.4 Affirmative positioning

State what the product **is** — directly and with conviction. Never define the offer by contrast with what it is not. Name the category you want the client to place it in, then substantiate it.

> הפתרון הוא מנוע החלטה קליני מובנה, הנשען על פרוטוקולים מאומתים שנכתבים יחד עם הצוות הקליני.

> הפרויקט מהווה קפיצת מדרגה תפעולית ותשתית אסטרטגית לשנים קדימה.

> המערכת היא תשתית AI ארגונית אסטרטגית, שעליה ניתן להרחיב יכולות נוספות לאורך זמן.

Whenever the client's mental model risks underestimating the offer, raise the framing by naming a bigger, more accurate category — `תשתית אסטרטגית`, `מנוע החלטה`, `קפיצת מדרגה`, `שכבת ידע ארגונית` — and back it with substance. Never reach for `אינו X אלא Y`, `לא רק X — אלא Y`, `במקום X`, or `ולא Y`. There is no "what it isn't" in Globalbit copy — only what it is.

---

## 5. Code-switching with English

Hebrew and English coexist in every Globalbit document. The rules:

**Keep in English (inline, no transliteration):**
- Product / company names: Azure, AWS, GCP, Next.js, PostgreSQL, Slack, Klafton
- Technical acronyms: API, RAG, RBAC, SSO, MFA, SLA, KPI, PII, OCR, OTP, CI/CD, ERP, BI, CRM, LMS, MVP, UAT, QA, T&M, B2B, SaaS, OWASP, ISO, SOC2
- Architecture terms: Embeddings, Vector Store, Pipeline, Microservices, Auth, Session, Cache, Webhook, Stream, Schema, Endpoint
- Methodology terms: Discovery, Kickoff, Go-Live, Sprint, Backlog, Roadmap, Foundation, Stack
- Business model terms: Time & Materials, Recurring Revenue, Multi-Tenant, Self-Service, Open Source, Cloud-Native
- Phase / artefact labels in tables: MS-0, MS-1, Sprint 1, Phase 0

**Translate (or pair) into Hebrew:**
- General concepts that have a clean Hebrew word: `אבטחת מידע` (not "security"), `הרשאות` (not "permissions"), `הצפנה` (not "encryption"), `בדיקות` (not "testing"), `תיעוד` (not "documentation").
- When in doubt, write the Hebrew term first and put the English in parentheses: `ניתוח פערים (Gap Analysis)`, `עקיבות (Traceability)`, `סוכני פיתוח (Development Agents)`. This is the pattern for any term that the client might recognise faster in English.

**Mixed inline is acceptable and frequent:** `פיתוח Pipeline אינדוקס`, `הקמת תשתית Azure`, `אינטגרציה מלאה עם Azure AD`. Don't try to translate the English term — the mixed phrase is the standard.

**Don't transliterate:**
- Bad: `אפ.איי.`, `קליינט-סייד`, `סקופ`, `דליוורבל`
- Good: `API`, `Client-side`, `היקף`, `תוצר`

See `references/glossary.md` for the full code-switching list by domain.

---

## 6. Typography and punctuation

These are tight rules. Follow them exactly.

| Element | Use | Don't use |
|---|---|---|
| Dash for emphasis / definition | `—` (em-dash, U+2014) with spaces on both sides | `-` (hyphen), `–` (en-dash) |
| Geresh on Hebraicised foreign words | `׳` (U+05F3): `צ׳אט`, `פיצ׳ר`, `ג׳ירפה` | `'` ASCII apostrophe |
| Gershayim on Hebrew acronyms | `״` (U+05F4): `מע״מ`, `לו״ז`, `ש״ח`, `קק״ל`, `דו״ח` | `"` straight quote |
| Quotation marks | `"..."` straight double quotes or `״...״` are both acceptable; be consistent inside one document | "smart quotes" mixed |
| Number-noun hyphen | hyphen, no space: `2-3 שבועות`, `30 יום`, `200,000,000 משתמשים` | space, en-dash |
| Range | hyphen: `5-7 שבועות`, `130,000-160,000 ₪` | `–` en-dash |
| Currency | digits + space + `₪` (or `ש״ח`). `28,000 ₪` | `28000₪`, `₪28,000` |
| Thousands separator | Western comma: `1,600`, `200,000,000` | space, dot |
| Percentages | `60%` no space | `60 %` |
| Plus operator (payment terms) | `שוטף + 30`, `שוטף + 5` | `שוטף +30` |
| Ordinals on phases | letter, dot, space: `1.`, `2.` — or `# 1\. כותרת` markdown | `1)`, `(1)` |
| Headers | `# **כותרת**` with bold inside | plain text headers |
| Bold for emphasis | `**טקסט**` (markdown bold) | underline, italic, ALL CAPS |
| Bullets | hyphen + space `- ` | `•` (unicode bullet) inside flowing copy |
| Sentence end | `.` and a newline | no period before bullet break |

See `references/typography.md` for the complete character table and worked examples.

---

## 7. Numbers, time, money

- **Always Western digits**, never Hebrew letters. `5 שבועות`, not `ה' שבועות`.
- **Hebrew ordinal words for phases:** `שלב ראשון`, `שלב שני` — but in tables and headings, use digits: `שלב 1`, `שלב 2`.
- **Hedged ranges for estimates:** `כ-280 שעות`, `בטווח של 130,000-160,000 ₪`, `מוערך בכ-`.
- **Decisive numbers for obligations:** `תוך 2 ימי עבודה`, `30 יום`, `שוטף + 5`.
- **Currency:** `₪` for shekels, `$` for dollars. State `+ מע״מ` or `כולל מע״מ` exactly once per pricing block; always also include the boilerplate line `כל המחירים אינם כוללים מע״מ` at the end of the commercial section.
- **Time windows:** always pair the unit. `2 ימי עבודה` not `2 ימים`. `30 יום קלנדריים` when distinguishing from working days.

---

## 8. Recurring signature phrases

These phrases appear across Globalbit's Hebrew documents and define the voice. Use them verbatim; do not paraphrase.

**Capability framing (value folded into the sentence):**
- `התוצאה היא`
- `כך ש-`
- `המאפשר ל-`
- `על מנת ש-`

**Positioning (affirmative only):**
- `מהווה תשתית אסטרטגית`
- `מבסיס עבודה מתקדם`
- `Production-ready מהיום הראשון`
- `שכבת ידע ארגונית`

**Method:**
- `בגישת ספרינטים של שבועיים`
- `עם דמו חי בסוף כל ספרינט`
- `שקיפות מלאה`
- `בליווי צמוד של מנכ״ל החברה`
- `פרויקט אסטרטגי בגלובלביט`
- `במודל Time & Materials`
- `קיצור משמעותי של זמני העלייה ל-Production`

**Credibility:**
- `יותר מ-200 מיליון אנשים ברחבי העולם משתמשים במערכות תוכנה שיצרנו`
- `ניסיון של 30 שנה`
- `בית תוכנה ישראלי עטור פרסים`
- `סוכני פיתוח ייעודיים (Development Agents)`
- `קיצור זמני פיתוח בעד כ-60%`
- `Total Customer Experience (TCE)`

**Closing:**
- `אנו מצפים לשיתוף פעולה`
- `Globalbit ערוכה להתחיל את הפרויקט`
- `בכפוף לזמינות משאבים`

Full verbatim library (with the canonical legal/commercial boilerplate sections — מחויבות הלקוח, תנאים כלליים, השלבים הבאים, הצהרת AI) lives in `references/boilerplate.md`.

---

## 9. Listicle and bullet conventions

Inside bullets, each item follows one of three shapes — pick one and stay consistent within a list:

**Shape A — Bold lead + explanation:**
> - **שיפור חוויית השירות ללקוחות** — לקוחות יוכלו לצפות בדוחות הביטוח שלהם בכל זמן ומכל מכשיר.

**Shape B — Pure noun phrase + dash + sentence:**
> - מערכת מודרנית — תשתית סקלאבילית הניתנת להרחבה ללא תלות טכנולוגית.

**Shape C — Verb-led action:**
> - הפחתת תלות בידע אישי באמצעות ניהול מרכזי של כלל המידע.

Do not mix shapes inside one list. Do not end bullets with semicolons; end with a period only if the bullet is a full sentence, otherwise no terminal punctuation.

When a feature deserves a "what it means" framing, fold the business value into the bullet itself with `—` or `כך ש-`. Never add a separate bolded `המשמעות העסקית:` line.

---

## 10. AI / risk / commercial disclosure (Hebrew)

When the offer includes AI or LLM components, include this exact-style disclosure inside the assumptions or general terms block (paraphrase only if length forces it):

> המערכת כוללת שימוש במנגנוני בינה מלאכותית. מערכות אלו מבוססות על מודלים סטטיסטיים ועשויות לעיתים להפיק תוצאות שאינן מדויקות באופן מלא — לכן נדרש שיקול דעת אנושי על תוצרי המערכת.

For risk tables, the canonical column set in Hebrew is:

| סיכון | חומרה | הסתברות | רמת סיכון | גידור |

Severity and probability are integers 1–5; risk level is either the product (numeric) or a tier (`נמוך`, `בינוני`, `גבוה`).

---

## 11. Things to never do

- Never write `אתה` or `אתם` when addressing the reader.
- Never use exclamation marks, emoji, or rhetorical questions.
- Never use Hebrew slang or English internet slang. No `יאללה`, no `LOL`, no `super-`.
- Never transliterate an English technical term that has a clean Hebrew equivalent (`סקופ` → `היקף`).
- Never repeat the client's name three times in one paragraph — rotate with `החברה`, `הארגון`, or pronominal verb.
- Never make superlative claims without a number or a citation (`הכי טוב בשוק` is forbidden; `מערכות שלנו משמשות מעל 200 מיליון משתמשים` is fine).
- Never end a section with a CTA in marketing language (`בואו נתחיל!`). End with `אנו מצפים לשיתוף פעולה עם [client] סביב הפרויקט.` or equivalent neutral closing.
- **Never define the offer by what it is NOT.** Forbidden: `אינו X אלא Y`, `לא רק X — אלא Y`, `במקום X — Y`, `זה לא ...`, `ולא Y`. State only what the product IS, in affirmative form. Name the right category up front and substantiate it.
- **Never use a bolded `המשמעות העסקית:` (or `ערך עסקי:` / `המשמעות:`) callout line.** Fold the business value into the sentence with `—` or `כך ש-`.
- Never machine-translate from English. The English source's sentence rhythm collapses Hebrew register. Rewrite from the idea.

---

## 12. Self-check before delivering Hebrew copy

Run this checklist on every paragraph:

1. Could a friend send this in a WhatsApp message? If yes — too informal. Fix.
2. Could it appear in a court ruling? If yes — too legal. Fix.
3. Are there exclamation marks, emoji, or `מאוד`/`ביותר`? Remove.
4. Are technical English terms inline (uppercase, untransliterated)? Good.
5. Are em-dashes `—` (not hyphens) used for emphasis and definition? Fix if wrong.
6. Is `מע״מ` written with `״` (gershayim), not `"`? Fix.
7. Does every meaningful capability state its business value inside the sentence (via `—` or `כך ש-`), with no bolded `המשמעות העסקית:` label line? Fix if a callout slipped in.
8. Did I address the reader as `אתה`/`אתם` anywhere? Replace with company name or third person.
9. Is every estimate hedged (`כ-`, `מוערך`, `בטווח של`) and every commitment flat?
10. Did I avoid every "not X — but Y" construction (`אינו`, `לא רק ... אלא`, `במקום X`, `ולא Y`) and state only what the offer IS?

If all ten pass, the paragraph is in voice.

---

## Reference files

Read these on demand:

- **`references/glossary.md`** — full Hebrew↔English term mapping by domain (AI, security, finance, methodology, commercial). Consult before choosing any noun that has both a Hebrew and English form.
- **`references/typography.md`** — exhaustive punctuation, character, and number-formatting rules with copy-paste examples.
- **`references/boilerplate.md`** — verbatim recurring sections: `מחויבות הלקוח`, `תנאים כלליים`, `הצהרת AI`, `השלבים הבאים`, and standard closing lines.
- **`references/examples.md`** — exemplar paragraphs from real Globalbit proposals, organised by rhetorical move (executive summary opener, capability bullet with business impact, risk row, commitment statement, closing line). Use as imitation models.
- **`references/anti-patterns.md`** — concrete bad sentences observed in early drafts and the corrected Globalbit-voice rewrites. The fastest way to internalise the register.

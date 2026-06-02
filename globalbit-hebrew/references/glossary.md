# Glossary — Canonical Hebrew↔English Mapping

The "use" column is what Globalbit writes. The "avoid" column lists wordings observed in less-polished drafts. The "context" column tells you when a term is locked vs. when the English form is also acceptable inline.

## Methodology and project management

| Use | Avoid | Context |
|---|---|---|
| הצעה | פרופוזל | Always Hebrew. |
| תקציר מנהלים | רזומה, סיכום | Locked. |
| רקע והקשר עסקי | אינטרו, מבוא | Locked. |
| יעדים עסקיים | אובייקטיבס, מטרות גבוהות | Locked for the section title; `מטרות` is fine in body. |
| היקף הפרויקט / תכולה | סקופ | Locked. English `Scope` only inside parentheses if disambiguating. |
| מחוץ להיקף | "אאוט אוף סקופ" | Locked. |
| תוצרים | פלטים, deliverables | Locked. |
| אבני דרך | מיילסטונים | Locked. Inline `MS-0`, `MS-1` numbers are fine in tables. |
| לוח זמנים | שדיול, "טיים פריים" | Locked. |
| ניהול סיכונים | "ריסק מנג'מנט" | Locked. |
| גידור (סיכון) | מיטיגציה | Locked. |
| חומרה / הסתברות / רמת סיכון | severity / probability inline | Locked in table headers. |
| ספרינט / ספרינטים | "מחזור עבודה" | Use ספרינט (transliterated, accepted). |
| Discovery | אפיון, גילוי | Keep English `Discovery` as a phase label. In body, `שלב Discovery` or `שלב גילוי` both work. |
| Kickoff | "פגישת פתיחה" | Keep English in headers; `פגישת התנעה` is the Hebrew body equivalent. |
| Go-Live / עלייה לאוויר | "השקה" alone | Either acceptable. Prefer `עלייה לאוויר` in flowing text. |
| MVP | "מוצר מינימלי" | Keep English. |
| UAT / בדיקות קבלה | פילוט קבלה | Both `UAT` (in parens) and `בדיקות קבלה` are used. |
| QA / בקרת איכות / בדיקות | טסט | Both acceptable. |
| מסירה מדורגת | "מסירה רציפה" | Locked. |
| Backlog | "רשימת משימות" | Keep English. |
| Sprint Backlog | "תכולת ספרינט" | Either. |
| תוכנית עבודה | "וורק פלאן" | Locked. |
| בקשת שינוי / Change Request / CR | "שינוי תכולה" | Use both; pair on first mention: `בקשת שינוי (Change Request)`. |
| מודל Time & Materials / T&M | "תמורת שעות" | Keep English. |
| חבילת שעות / בנק שעות | "מאגר שעות" | Both used interchangeably. |
| תעריף שעתי | "מחיר לשעה" | Locked. |
| תנאי תשלום | "תנאי שילום" | Locked. |
| שוטף + N | "נטו N", "EOM + N" | Locked Hebrew form. |
| משולש הזהב | "טריאנגל" | Locked. |
| Agile | אג'יל | Either. `Agile` (capitalised, English) is more common. |
| CI/CD | "מערכת בנייה" | Keep English. |
| DevOps | "דב-אופס" | Keep English. |

## Technology — Stack and infrastructure

| Use | Avoid | Context |
|---|---|---|
| ארכיטקטורה | "מבנה" | Locked when meaning system architecture. |
| תשתית | "אינפראסטרוקטורה" | Locked. |
| שכבה / שכבת X | "ליין", "שכבת" with English suffix | Locked. |
| Pipeline | "צינור" | Keep English. |
| API / APIs | "ממשק תכנותי" | Keep English. |
| Endpoint | "נקודת קצה" | Keep English. |
| Service / Microservice | "שירות" | Both acceptable. Prefer `שירות` in flowing Hebrew, `Microservice` in architecture diagrams. |
| Frontend / Backend | "צד לקוח / צד שרת" | Keep English in technical sections. |
| Authentication / אימות | "לוגין" | `אימות` in body; `Authentication` (or `Auth`) capitalised in lists. |
| Authorization / הרשאות | "הרשאות גישה" alone | Locked: `הרשאות`. |
| RBAC | "הרשאות מבוססות תפקיד" | Keep English; pair on first mention. |
| SSO | "התחברות אחודה" | Keep English. |
| MFA / OTP | "אימות דו-שלבי" | Keep English; the Hebrew is acceptable on first mention with the English in parens. |
| Session / Sessions | "סשן" | Keep English. |
| Cache | "מטמון" | Keep English in technical sections; `מטמון` acceptable elsewhere. |
| Encryption at Rest / In Transit | "הצפנה במנוחה / בתעבורה" | Either. Pair on first mention if mixed audience. |
| Audit / Audit Log | "תיעוד" alone | Keep English: `Audit Log`. `תיעוד פעולות` is acceptable in body. |
| Monitoring / ניטור | "מוניטורינג" | `ניטור` for body, `Monitoring` for table headers. |
| Observability | "תצפיתיות" | Keep English. |
| Load Balancer | "מאזן עומסים" | Keep English. |
| Vector Store / Embeddings | "מאגר וקטורי / שיכון" | Keep English. |
| RAG | "אחזור-וייצור" | Keep English. |
| LLM | "מודל שפה גדול" | Keep English; pair on first mention. |
| Prompt / Prompts | "פרומפט" | Keep English. |
| Fine-tuning | "כיוון עדין" | Keep English. |
| Inference | "היסק" | Keep English. |
| Hallucination | "הזיה" | Both acceptable; `הזיות (Hallucinations)` is the canonical pair. |
| AI Agent / Agentic | "סוכן AI / סוכנים" | `סוכן AI` in Hebrew flow; `Agent` in titles. |

## Security and compliance

| Use | Avoid | Context |
|---|---|---|
| אבטחת מידע | "סקיוריטי" | Locked. |
| הצפנה | "אנקריפשן" | Locked. |
| פגיעות / Vulnerability | "חולשה" alone | Either; `פגיעות` in Hebrew, `Vulnerability` in technical lists. |
| חדירה / Penetration Test | "פנטסט", "מבחן חדירה" | Hebrew + English-in-parens canonical. |
| Zero-Trust | "אפס אמון" | Keep English. |
| Audit Trail | "מעקב פעולות" | Keep English. |
| DLP | "מניעת דליפת מידע" | Keep English; pair on first mention. |
| Secure SDLC | "תהליך פיתוח מאובטח" | Keep English. |
| OWASP | (Hebrew translation) | Keep English. |
| ISO 27001 / SOC2 | (Hebrew) | Keep English. |
| מפעל חיוני | "תשתית קריטית" | Locked Hebrew when describing Globalbit's classification. |
| חוק הגנת הפרטיות | (English) | Locked Hebrew. Include year: `חוק הגנת הפרטיות התשפ״ד-2024`. |
| תקנות הגנת הפרטיות (אבטחת מידע) | (English) | Locked. Include year: `התשע״ז-2017`. |

## Data, analytics, BI

| Use | Avoid | Context |
|---|---|---|
| בסיס נתונים | "דאטה בייס" | Locked. |
| מבנה נתונים / סכמה | "Schema" alone | Pair. |
| מיגרציית נתונים | "העברת נתונים" | Locked: `מיגרציה`. |
| ייבוא / ייצוא | "אימפורט / אקספורט" | Locked Hebrew. |
| דוח / דוחות | "ריפורט" | Locked. |
| דשבורד | "לוח בקרה" | `דשבורד` is the canonical Hebrew form. |
| אנליטיקה | "אנליטיקס" | Locked: `אנליטיקה`. |
| מטריקה / מטריקות | "KPI" alone in body | Use `מטריקה`; reserve `KPI` for explicit performance indicators. |
| תובנות | "אינסייטים" | Locked. |
| נתונים גולמיים | "raw data" | Locked Hebrew; English acceptable inline. |

## Business model and commercial

| Use | Avoid | Context |
|---|---|---|
| לקוח | "קליינט", "יוזר" (when meaning customer) | Locked. |
| משתמש / משתמשי קצה | "אנד יוזר" | Locked. |
| מנוי / Subscription | "סבסקריפשן" | Locked Hebrew. |
| הכנסות חוזרות / Recurring Revenue | "הכנסות שוטפות" | Pair canonical: `הכנסות חוזרות (Recurring Revenue)`. |
| בעלי עניין | "סטייקהולדרס" | Locked. |
| שותפות | "פרטנרשיפ" | Locked. |
| הסכם | "קונטרקט", "חוזה" | `הסכם` in proposals; `חוזה` only for executed contracts. |
| הזמנה / הזמנת רכש | "פיו-או", "פרצ'ייס אורדר" | Locked Hebrew. |
| חתימה / אישור | "סיין-אוף" | Locked Hebrew. |
| פגישת יישור | "אליינמנט" | Locked Hebrew. |
| מע״מ | "VAT" inline | Locked Hebrew with gershayim. |
| ש״ח / ₪ | "שקל" | `₪` for prices, `ש״ח` in flowing text. |

## Mode of speech — Globalbit-isms

These compound noun phrases recur across proposals and are part of the brand voice:

- `שותפת טכנולוגיה ותיקה` / `שותפים טכנולוגיים`
- `בית תוכנה ישראלי עטור פרסים`
- `סטנדרטים מחמירים של אבטחת מידע`
- `מדיניות גישה מבוקרת`
- `שכבת ידע ארגונית`
- `Knowledge as Infrastructure`
- `AI-First` (capitalised, hyphenated)
- `Foundation` (capitalised when used as a product element)
- `תשתית AI אסטרטגית`
- `מנוע החלטה דטרמיניסטי`
- `קפיצת מדרגה תפעולית`
- `נקודת מפנה אסטרטגית`
- `מחויבות של ההנהלה הבכירה להצלחה`
- `הפחתת סיכון משמעותית`
- `קיצור דרמטי של זמני העלייה ל-Production`
- `מבסיס פתיחה מתקדם`
- `Production-ready`
- `Mission Critical`
- `כל אחד מבעלי העניין` (rotating-stakeholder framing)
- `חוויית שירות דיגיטלית`
- `קצב אימוץ גבוה`
- `מצמצם תלות במערכות צד שלישי`

## Verbs — preferred forms

| Use | Avoid |
|---|---|
| לספק | לתת |
| להעניק | "להגיש" (unless physically) |
| לבצע | לעשות |
| להוביל | "לרוץ עם" |
| להטמיע | "להכניס", "להתקין" |
| להאיץ | "לזרז" |
| לייעל | "לעשות יעיל יותר" |
| לצמצם | "להקטין" |
| לאמת | "לבדוק שזה נכון" |
| לשלב | "לחבר ביחד" |
| לתאם | "לתזמן" (unless meaning scheduling) |
| לחדד | "לעדכן את הדרישות" |
| לכייל | "לכוונן" |
| לתפעל | "להפעיל" |
| לנטר | "לעקוב" (when meaning system monitoring) |
| לזהות | "לראות מי" |
| לאפשר | "לתת אפשרות ל-" |

## Adjectives — preferred forms

| Use | Avoid |
|---|---|
| מהותי / משמעותי | "ענקי", "אדיר", "מטורף" |
| ברור / מובחן | "ברור לעין" |
| מובחן / מובהק | "ברור מאוד" |
| מדויק | "טוב מאוד" |
| איכותי | "טוב" |
| יציב | "stabili", "סטבילי" |
| חזק | "סופר-חזק" |
| מתקדם | "מתקדם מאוד", "ממש מתקדם" |
| עקבי | "consistent" inline |
| גמיש / סקלאבילי | "סקיילבילי" |
| מודרני | "חדיש" |
| ייעודי | "ספציפי" (when meaning purpose-built) |
| מהיר | "סופר-מהיר", "מהיר מאוד" |

When the temptation is to add an intensifier (`מאוד`, `ביותר`), instead pick a stronger noun or verb. The Globalbit register is built on precision, not amplification.

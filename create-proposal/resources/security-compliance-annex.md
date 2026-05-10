# Security & Compliance Annex

> **When to include**: ALL proposals to enterprise clients (banks, insurance, healthcare, government, regulated industries) AND any proposal where the deal value > 200K NIS. The CISO is often a veto holder — without a clear security story, the proposal stalls regardless of how good the technical solution is.
>
> **Where to include**: As the LAST appendix, after General Terms but before signatures. Title in Hebrew: "נספח א׳ - אבטחת מידע ותאימות רגולטורית". In English: "Appendix A - Information Security & Regulatory Compliance".
>
> **Length target**: 1.5 - 2 pages. Long enough to satisfy CISO due diligence, short enough not to bury the proposal.

---

## Hebrew Boilerplate (Default for Israeli Clients)

### נספח א׳ - אבטחת מידע ותאימות רגולטורית

#### תקני אבטחה ותהליכי עבודה

גלובלביט מקפידה על תהליכי אבטחת מידע מהדורים בכל מחזור החיים של הפרויקט - מהאפיון, דרך הפיתוח, הבדיקות ועד התחזוקה השוטפת. החברה מסווגת כמפעל חיוני בשל פעילותה במערכות ממשלתיות וביטחוניות, ומיישמת בפועל את הסטנדרטים הבאים:

- **Secure SDLC** - תהליכי פיתוח מאובטחים מבוססי OWASP, סקירות קוד אבטחתיות לפני כל release, ובדיקות SAST/DAST אוטומטיות בצנרת ה-CI/CD.
- **Zero-Trust Architecture** - הנחת מוצא של חוסר אמון בכל רכיב, אכיפת הרשאות מינימליות (Least Privilege), MFA חובה לכל גישה, ובידוד רשתי בין סביבות.
- **Encryption at Rest & In Transit** - הצפנת AES-256 על כלל הנתונים במנוחה, TLS 1.3 לכלל התעבורה, ניהול מפתחות ב-Key Vault עם Key Rotation תקופתי.
- **Data Loss Prevention (DLP)** - מנגנוני סניטיזציה ובקרה על נתונים יוצאים, חסימת הזלגת PII / מידע רגיש.
- **Audit Logging** - תיעוד בלתי ניתן לשינוי של כל פעולה רגישה (כניסה, גישה לנתונים, שינוי הרשאות), שמירה ל-365 יום לפחות.
- **Penetration Testing** - בדיקות חדירות תקופתיות (לפחות פעם בשנה ולפני כל release מרכזי) על-ידי גורם חיצוני בלתי תלוי.
- **Vulnerability Management** - סריקה רציפה לפגיעויות (Snyk / Dependabot / OWASP Dependency-Check), טיפול ב-CVE קריטיות תוך 7 ימים.

#### תאימות רגולטורית

הפתרון יבוצע בהתאם לדרישות הרגולציה הישראלית הרלוונטיות לסקטור הלקוח:

- **חוק הגנת הפרטיות התשפ"ד-2024** - יישום מנגנוני בקרה על מידע אישי, הסכמה מפורשת, זכות עיון ומחיקה, מינוי DPO ככל שנדרש.
- **תקנות הגנת הפרטיות (אבטחת מידע) התשע"ז-2017** - קלסיפיקציה של מאגרי מידע, הקשחת בקרות גישה, תוכנית התמודדות עם אירועי אבטחה.
- **בנקים ומוסדות פיננסיים**: הוראת בנק ישראל ניהול בנקאי תקין 357 (ניהול סייבר), הוראה 361 (מיקור חוץ של פעילויות), הוראה 362 (סיכוני סייבר).
- **חברות ביטוח וגופים מוסדיים**: הוראת רשות שוק ההון, הביטוח והחיסכון בנושא ניהול סיכוני סייבר, הוראות סיכוני מיקור חוץ.
- **מערכות בריאות**: הוראות נב"ת של משרד הבריאות, ת"י 5470 (ניהול תיק רפואי דיגיטלי), חוק זכויות החולה.
- **מגזר ממשלתי**: תקנות עמ"ת (עיבוד מידע ממשלתי), חוק חתימה אלקטרונית, הנחיות מערך הסייבר הלאומי.
- **תקנים בינלאומיים**: גלובלביט פועלת בהתאם לעקרונות ISO 27001 ו-SOC 2 Type II. הסטטוס הפורמלי של הסמכה נמסר ללקוח לפי בקשה במסגרת תהליך ה-Due Diligence.

#### Data Residency

כל הנתונים של הלקוח יישמרו אך ורק במרכזי נתונים בישראל או באזור EU (לפי בחירת הלקוח), בענן הציבורי של מנורה / הלקוח. אין העברת נתונים מחוץ לאזור מבלי לאישור מפורש בכתב מטעם הלקוח. אנשי גלובלביט מתחייבים לעבוד מתוך ישראל ולא לבצע גישה למידע ממקומות אחרים בעולם.

#### ניהול אירועי אבטחה

- **תוכנית תגובה לאירועי אבטחה (IR)** - נוהל מתועד עם זמני תגובה: P0 (פריצה פעילה) - שעה אחת; P1 (פגיעות קריטית) - 4 שעות; P2 (חשד) - 24 שעות.
- **דיווח ללקוח** - על כל אירוע אבטחה רלוונטי, הלקוח יקבל הודעה תוך 24 שעות, יחד עם תיעוד ראשוני, וניתוח גורם שורש מלא תוך 7 ימים.
- **שימור ראיות** - שימור Audit Logs ו-System Snapshots למשך 90 יום לפחות לצורך חקירה.

#### תהליך Due Diligence

לקוחות תאגידיים זכאים לקבל לפי בקשה (תחת NDA הדדי):

- מסמך SOC 2 Type II Report מלא
- מסמכי מדיניות אבטחת מידע פנים-ארגונית
- תוצאות בדיקות חדירות אחרונות (סיכום מנהלים)
- אישור ביטוח אחריות מקצועית בסכום של 5,000,000 ש"ח לפחות
- רשימת תת-ספקים ושותפי טכנולוגיה (SaaS, ענן, כלי DevOps) - ברירת מחדל: Microsoft Azure, GitHub, Atlassian
- ראיון אבטחה (Security Interview) עם ה-CTO וה-CISO של גלובלביט מול ה-CISO של הלקוח

---

## English Boilerplate

### Appendix A - Information Security & Regulatory Compliance

#### Security Standards & Practices

Globalbit implements rigorous information security processes throughout the entire project lifecycle - from specification through development, testing, and ongoing maintenance. The company is classified as an Essential Facility (מפעל חיוני) due to its work on government and defense systems, and applies the following standards:

- **Secure SDLC** - OWASP-based secure development processes, mandatory security code reviews before each release, automated SAST/DAST in CI/CD.
- **Zero-Trust Architecture** - assume-breach posture, Least Privilege enforcement, mandatory MFA, network isolation between environments.
- **Encryption at Rest & In Transit** - AES-256 for data at rest, TLS 1.3 for all traffic, key management via Key Vault with periodic Key Rotation.
- **Data Loss Prevention (DLP)** - sanitization and outbound data controls, PII / sensitive data leak prevention.
- **Audit Logging** - immutable logging of all sensitive operations (login, data access, permission changes), retained for at least 365 days.
- **Penetration Testing** - periodic third-party penetration tests (at least annually and before every major release).
- **Vulnerability Management** - continuous scanning (Snyk / Dependabot / OWASP Dependency-Check), critical CVE remediation within 7 days.

#### Regulatory Compliance

The solution will be delivered in compliance with all relevant Israeli regulations applicable to the client's sector:

- **Israeli Privacy Protection Law (5784-2024)** - personal data controls, explicit consent, access and deletion rights, DPO appointment where required.
- **Privacy Protection Regulations (Information Security) 5777-2017** - database classification, access control hardening, incident response plan.
- **Banking & Financial Institutions**: Bank of Israel Proper Banking Conduct Directive 357 (cyber management), Directive 361 (outsourcing), Directive 362 (cyber risk).
- **Insurance & Institutional Bodies**: Capital Markets Authority directives on cyber risk management.
- **Healthcare**: Ministry of Health digital directives, IS 5470 (digital medical records), Patient Rights Law.
- **Government**: Government Information Processing Regulations, Electronic Signature Law, National Cyber Directorate guidelines.
- **International Standards**: Globalbit operates per ISO 27001 and SOC 2 Type II principles. Formal certification status disclosed under NDA during Due Diligence.

#### Data Residency

All client data is stored exclusively in Israeli or EU data centers (client's choice), within the client's or Globalbit's Azure tenant. No cross-region data transfer without explicit written client approval. Globalbit personnel work from Israel and do not access client data from other geographies.

#### Security Incident Management

- **Incident Response Plan** - documented procedure with response times: P0 (active breach) - 1 hour; P1 (critical vulnerability) - 4 hours; P2 (suspected) - 24 hours.
- **Client notification** - any relevant security incident reported within 24 hours, with initial documentation and full root-cause analysis within 7 days.
- **Evidence retention** - audit logs and system snapshots retained for at least 90 days for investigation.

#### Due Diligence Materials

Enterprise clients are entitled, under mutual NDA, to receive on request:

- Full SOC 2 Type II Report
- Internal information security policies
- Recent penetration test results (executive summary)
- Professional liability insurance certificate (minimum NIS 5,000,000)
- List of sub-processors and tech partners (default: Microsoft Azure, GitHub, Atlassian)
- Security interview between Globalbit's CTO and CISO and the client's CISO

# Service Playbook: Performance Analysis & Code Audit

> **When to use**: Client needs performance profiling, code quality audit, architecture review, or optimization roadmap for an existing system.
> **Reference proposals**: IsraelPharm (Proposal 5)

---

## Overview

Performance Analysis is a **diagnostic engagement** — short, focused, and high-value. Position it as the **smart, data-driven approach** before committing to larger investments like rewrites or migrations.

### Key Selling Points

- Data-driven decisions instead of assumptions
- Identifies quick wins that deliver immediate value
- Prevents wasting budget on unnecessary rewrites
- Comprehensive: covers infrastructure, backend, frontend, and delivery layers
- Clear, prioritized roadmap: Quick wins → Medium-term → Long-term improvements

---

## Typical Phases

### Phase 1: Initial System Review (1–2 days)

- Architecture overview and documentation review
- Technology stack assessment
- Codebase structure walkthrough
- Identify areas of concern
- Deliverable: **Initial Assessment Briefing**

### Phase 2: Environment Assessment (1–2 days)

- Hosting infrastructure review (servers, PHP/runtime version, web server, database engine)
- Caching layers evaluation
- Server resources audit (CPU, RAM, I/O, storage)
- Cloud configuration review
- Deliverable: **Infrastructure Audit Report**

### Phase 3: Baseline Measurements (2–3 days)

- Core Web Vitals and TTFB benchmarking
- Lighthouse, GTmetrix, WebPageTest audits on key pages
- Server response profiling (Query Monitor, NewRelic, or equivalent)
- Mobile vs desktop performance comparison
- Deliverable: **Performance Baseline Report**

### Phase 4: Backend Profiling & Database Analysis (3–5 days)

- Slow query identification and optimization recommendations
- Database indexing analysis
- Background tasks and cron job review
- Plugin/module load time analysis
- API endpoint response time profiling
- Deliverable: **Backend & Database Profiling Report**

### Phase 5: Frontend Optimization Analysis (2–3 days)

- Render-blocking resource identification
- Asset size analysis (JS, CSS, images)
- Third-party script impact
- Template rendering efficiency
- Responsive performance analysis
- Deliverable: **Frontend Optimization Report**

### Phase 6: Caching & Delivery Review (2–3 days)

- Page and object caching effectiveness
- CDN configuration and coverage
- Compression audit (GZIP/Brotli)
- Cache miss analysis
- Deliverable: **Caching & CDN Assessment**

### Phase 7: Reporting & Recommendations (1–2 days)

- Consolidated findings report
- Prioritized action plan
- Executive summary for leadership
- Deliverable: **Final Performance Analysis Report & Roadmap**

---

## Prioritized Roadmap Template

All findings are categorized into three tracks:

### Quick Wins (1–2 days each)

- Items that can be resolved immediately with high impact
- Typically: caching improvements, image optimization, render-blocking resource fixes
- Low risk, high reward

### Medium-Term Fixes (3–5 days each)

- Require more planning but deliver significant improvement
- Typically: database query optimization, plugin restructuring, infrastructure upgrades
- Moderate risk, high reward

### Long-Term Improvements

- Structural or architectural changes
- Typically: frontend framework migration, microservice decomposition, database redesign
- High investment, transformative impact

---

## Typical Deliverables

- [ ] Infrastructure audit report
- [ ] Performance baseline report (key pages, Core Web Vitals)
- [ ] Backend profiling & database analysis report
- [ ] Frontend optimization report
- [ ] Caching & CDN assessment
- [ ] Consolidated Performance Analysis Report
- [ ] Prioritized Improvement Roadmap (Quick Wins / Medium / Long-Term)

---

## Typical Effort Estimates

| Phase | Hours |
|-------|:-:|
| Initial System Review | 4–8 |
| Environment Assessment | 4–8 |
| Baseline Measurements | 8–12 |
| Backend Profiling & DB Analysis | 12–20 |
| Frontend Optimization Analysis | 8–12 |
| Caching & Delivery Review | 8–12 |
| Reporting & Recommendations | 4–8 |
| Project Management | 10–15 |
| **Total** | **60–100** |

---

## Value Framing

- **Save before you spend**: "Before investing in a full rewrite, invest {{X}} ₪ to understand where the real bottlenecks are. In many cases, targeted optimizations achieve 80% of the desired improvement at 20% of the cost."
- **Data-driven decisions**: "Every recommendation is backed by measurable data, not assumptions."
- **Business impact**: "For IsraelPharm, a 1-second improvement in page load time can increase conversion rates by 7%."
- **Risk reduction**: "A performance audit prevents investing in the wrong solution."

---

## Risks Specific to This Service

| Risk | Severity | Probability | Mitigation |
|------|:-:|:-:|-----------|
| Limited access to production environment | 3 | 3 | Request staging with production-like data; use monitoring tools |
| Missing documentation for existing system | 2 | 4 | Factor in extra discovery time; code walkthrough sessions |
| Performance issues caused by third-party dependencies | 3 | 3 | Identify third-party bottlenecks; recommend alternatives |
| Client expectations for immediate fix (not analysis) | 3 | 3 | Clear scoping in proposal; separate optimization engagement |

---

## Commercial Notes

- Typically a **Fixed Price** or **short T&M** engagement (2–3 weeks)
- Often leads to follow-on development / optimization work
- Position the analysis as **Phase 1** of a larger improvement program
- Total investment is typically 15,000–30,000 ₪

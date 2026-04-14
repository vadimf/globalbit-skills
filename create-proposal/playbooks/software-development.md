# Service Playbook: Custom Software Development

> **When to use**: Client needs to build a new application, platform, or system (web, mobile, or both).
> **Reference proposals**: Crypto-C (Proposal 3), LIT Development (Proposal 6)

---

## Overview

Custom software development is Globalbit's **core service**. Position it as a partnership — not a contractor relationship. Emphasize Agile methodology, iterative delivery, and business-outcome focus.

### Key Selling Points

- Full-stack delivery: architecture → development → testing → deployment → support
- Products serving **200M+ users** demonstrate ability to build at scale
- AI-First approach: integrating AI into both the product and the development process
- Reusable component library reduces development time and cost
- Code agent management reduces delivery time by **4x**

---

## Typical Project Structure

### Phase 0: Discovery & Architecture (2–4 weeks)

- Technical architecture design
- Technology stack selection (with business justification)
- Infrastructure planning (cloud, CI/CD, environments)
- Sprint planning and backlog creation
- Deliverable: **Architecture Document** + **Sprint Backlog**

### Phase 1–N: Development Sprints (2-week sprints)

Each sprint delivers:

- Working, tested features
- Sprint review / demo to client
- Sprint retrospective for continuous improvement
- Updated backlog and priorities

### Final Phase: Launch & Stabilization (2–4 weeks)

- Performance optimization
- Security audit
- Production deployment
- Monitoring setup
- Knowledge transfer
- Deliverable: **Production System** + **Handover Documentation**

---

## Technology Stack Guidance

Present tech choices with **business justifications**, not just technical preferences:

| Technology Area | Typical Choices | Business Justification |
|----------------|----------------|----------------------|
| Frontend (Web) | React, Next.js, Angular | Large talent pool, component reuse, SEO capability |
| Frontend (Mobile) | React Native, Flutter | Single codebase = faster delivery, lower maintenance |
| Backend | Node.js, .NET, Python | Proven at scale, extensive ecosystem, rapid development |
| Database | PostgreSQL, MongoDB, Redis | Reliability, scalability, industry standard |
| Cloud | AWS, Azure, GCP | Enterprise-grade, global availability, compliance |
| CI/CD | GitHub Actions, Jenkins, Azure DevOps | Automated quality, faster releases |

---

## Scope Table Template

Use this format to break down project scope:

| Module | Feature | Complexity | Estimated Hours |
|--------|---------|:-:|:-:|
| User Management | Registration, login, profile management | Medium | 80 |
| {{MODULE}} | {{FEATURE}} | {{LOW/MEDIUM/HIGH}} | {{HOURS}} |
| Admin Panel | Back-office management, reporting | Medium-High | 120 |
| Infrastructure | CI/CD, environments, monitoring | Medium | 60 |
| QA & Testing | Test strategy, automation, regression | Medium | 15% of dev hours |

---

## Typical Deliverables

- [ ] Architecture document
- [ ] Working application (web / mobile / both)
- [ ] Admin panel / back-office
- [ ] API documentation
- [ ] Automated test suite
- [ ] CI/CD pipeline
- [ ] Deployment documentation
- [ ] Source code (in client's repository)
- [ ] Knowledge transfer sessions

---

## Methodology Section Content

> Globalbit employs an Agile Scrum methodology with 2-week sprints, ensuring continuous delivery and client visibility throughout the project:
>
> - **Sprint Planning** — Prioritize user stories based on business value
> - **Daily Standups** — Team alignment on progress and blockers
> - **Sprint Reviews** — Bi-weekly demos of working features to stakeholders
> - **Sprint Retrospectives** — Continuous process improvement
> - **Definition of Done** — Code reviewed, tested, documented, and deployable
>
> Key principles:
>
> - Working software over comprehensive documentation
> - Client collaboration over contract negotiation
> - Responding to change over following a plan
> - Continuous integration and continuous deployment (CI/CD)

---

## Risks Specific to This Service

| Risk | Severity | Probability | Mitigation |
|------|:-:|:-:|-----------|
| Scope expansion beyond initial requirements | 4 | 4 | Strict change control process; document all scope changes |
| Third-party API instability or changes | 3 | 3 | Abstraction layers; fallback mechanisms; SLA monitoring |
| Data migration complexity underestimated | 4 | 3 | Early data audit; migration dry runs in staging |
| Performance degradation under load | 4 | 2 | Load testing from Sprint 3; performance budgets |
| Key team member turnover | 3 | 2 | Knowledge sharing practices; documentation culture |
| Security vulnerabilities | 5 | 2 | OWASP compliance; regular security reviews; penetration testing |
| Client-side delays in feedback/approvals | 3 | 3 | SLA for feedback (2/5/7 days); escalation process |

---

## Commercial Notes

- **Default model**: Time & Materials (T&M) — best for evolving scope
- **Sprint-based billing**: Invoice per sprint based on actual hours
- **Include buffer**: Add 10–15% buffer in estimates for unforeseen complexity
- **Maintenance transition**: Propose maintenance contract for post-launch (see `maintenance-support.md`)

---

## AI/GenAI Projects — Special Considerations

When the development project involves AI capabilities, include these additional sections:

### AI-Specific Scope Items

- Model selection and evaluation
- Training data preparation and validation
- Model training / fine-tuning / prompt engineering
- Integration testing with AI components
- Performance monitoring and model drift detection
- Compute resource planning (GPU, API costs)

### AI Value Framing

- Quantify the business impact: "AI-powered recommendations increase conversion by X%"
- Address data quality: "Garbage in, garbage out — we ensure data quality before model training"
- Set realistic expectations: "AI augments human decision-making, it doesn't replace it"
- Include monitoring costs in ongoing estimates

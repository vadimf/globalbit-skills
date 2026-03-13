# Globalbit Skills

A collection of AI coding agent skills for web development, SEO, content creation, and deployment. These skills extend AI assistants (like Gemini, Claude, etc.) with specialized capabilities for building and maintaining production websites.

## 🚀 What Are Skills?

Skills are structured instruction sets that give AI coding agents domain-specific expertise. Each skill contains a `SKILL.md` file with detailed instructions, and may include helper scripts, examples, and resources.

## 📦 Available Skills

### Web Development
| Skill | Description |
|-------|-------------|
| **[nextjs](./nextjs)** | Build Next.js 16 apps with App Router, Server Components/Actions, Cache Components ("use cache"), and async route params |
| **[create-new-page](./create-new-page)** | Full protocol for creating new service or landing pages — research, story, copy, components, testing |
| **[tailwind-patterns](./tailwind-patterns)** | Production-ready Tailwind CSS patterns for responsive layouts, cards, navigation, forms, and buttons |
| **[clone-website](./clone-website)** | Clone/replicate websites into production-ready Next.js 16 code |
| **[web-design-guidelines](./web-design-guidelines)** | Review UI code against Web Interface Guidelines for best practices |

### Performance & Accessibility
| Skill | Description |
|-------|-------------|
| **[core-web-vitals](./core-web-vitals)** | Optimize Core Web Vitals (LCP, INP, CLS) for better page experience and search ranking |
| **[core-web-vitals-tuner](./core-web-vitals-tuner)** | Systematically improve LCP, INP, and CLS with prioritized fixes and verification |
| **[core-web-vitals-next-firebase-auto](./core-web-vitals-next-firebase-auto)** | Auto-discover URLs, run lab audits, collect field vitals, and produce a prioritized fix plan |
| **[accessibility](./accessibility)** | Build WCAG 2.1 AA compliant websites with semantic HTML, ARIA, focus management, and screen reader support |
| **[accessibility-compliance](./accessibility-compliance)** | WCAG 2.2 compliance, mobile accessibility, inclusive design patterns, and assistive technology support |

### SEO & Analytics
| Skill | Description |
|-------|-------------|
| **[seo-audit](./seo-audit)** | Audit, review, and diagnose technical SEO issues — meta tags, structured data, crawlability |
| **[google-search-console](./google-search-console)** | Analyze Google Search Console data, search performance, indexing, and Core Web Vitals |

### Content & Copy
| Skill | Description |
|-------|-------------|
| **[copywriting](./copywriting)** | Expert conversion copywriting — headlines, CTAs, page structure, voice/tone |
| **[blog-articles](./blog-articles)** | Write, optimize, and publish blog articles in English or Hebrew |
| **[case-studies](./case-studies)** | Create, rewrite, and strategically improve case study pages |
| **[humanizer](./humanizer)** | Remove signs of AI-generated writing to make text sound natural and human-written |


## 🛠️ Usage

### With Gemini Code Assist / Antigravity

Place skills in your project's `.agents/skills/` directory:

```
your-project/
├── .agents/
│   └── skills/
│       ├── nextjs/
│       │   └── SKILL.md
│       ├── seo-audit/
│       │   └── SKILL.md
│       └── ...
```

The AI agent will automatically discover and use relevant skills based on your requests.

### With Other AI Agents

Each skill's `SKILL.md` can be used as a system prompt or context file for any AI coding assistant. Simply provide the content of the relevant `SKILL.md` as context when working on related tasks.

## 📄 License

MIT — see [LICENSE](./LICENSE) for details.

## 🤝 Contributing

Contributions welcome! Each skill should follow this structure:

```
skill-name/
├── SKILL.md          # Required: Main instruction file with YAML frontmatter
├── scripts/          # Optional: Helper scripts and utilities
├── examples/         # Optional: Reference implementations
└── resources/        # Optional: Templates, assets, additional files
```

The `SKILL.md` should include YAML frontmatter with `name` and `description` fields.

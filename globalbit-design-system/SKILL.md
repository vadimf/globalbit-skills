---
name: globalbit-design-system
description: >
  The canonical Globalbit design system — the single source of truth for brand
  tokens (color, typography, spacing, radius, shadow, icons) and component
  patterns that every agent should apply when designing or building any
  Globalbit UI. Use when generating mockups, landing pages, app screens, or
  components; when running Claude Design / the `design` skill; or when keeping a
  Claude Design design-system project in sync via `/design-sync`. Triggers:
  "design a page", "build a component", "make it on-brand", "apply our design
  system", "create a mockup", "Globalbit design", "sync the design system".
---

# Globalbit Design System

This skill is the **authoritative, machine-readable design system for Globalbit**.
Any agent — a subagent, a desktop session, a Claude Design canvas, or Claude Code
on the web — should read this before producing visual output so everything ships
on-brand and consistent, without a human re-specifying the brand each time.

> **How to use this skill**
> 1. Load these tokens as hard constraints before writing any UI, mockup, or component.
> 2. Prefer the component patterns below over inventing new ones.
> 3. When output is a *design canvas*, pair this with the `design` skill.
> 4. To publish or update the shared Claude Design design-system project, use
>    the **"Publish to Claude Design"** workflow at the bottom (via `/design-sync`).

The full portable spec lives in [`DESIGN.md`](./DESIGN.md) (hand that file to
Claude Design or any external agent). Ready-to-sync component previews live in
[`components/`](./components).

---

## Two surfaces, one brand

Globalbit ships two UI contexts. They share the same brand foundation; only the
token *delivery* differs.

| Surface | Palette delivery | Dark mode | Reference |
|---------|------------------|-----------|-----------|
| **Product / CRM app** | Literal Tailwind classes (`bg-gray-50`, `text-gray-900`) | No | `crm-design-guidelines` |
| **Marketing website** | Semantic tokens (`bg-background`, `text-foreground`, `bg-primary`) | Yes | `tailwind-patterns` |

**Rule of thumb:** building inside the app → use literal classes below. Building
a website/landing page → use semantic tokens that map to the same brand values.
Never mix the two systems in one component.

---

## Brand Foundation

| Token | Value |
|-------|-------|
| Primary typeface | **Inter** (Google Fonts, `--font-inter`) |
| Primary action | `gray-900` (`#111827`) on white text |
| Brand mark background | `black` |
| Accent | **Indigo 500** `#6366f1` (data viz, highlights — used sparingly) |
| Neutral scale | Tailwind `gray-*` for all structural UI |
| Icon library | **Lucide** only (never Heroicons / FontAwesome) |

### Color — product/app (literal classes)

| Use | Class |
|-----|-------|
| Page background | `bg-gray-50` |
| Card / panel | `bg-white` |
| Card border | `border-gray-200` |
| Primary text | `text-gray-900` |
| Secondary text | `text-gray-500` |
| Muted text | `text-gray-400` |
| Default icon | `text-gray-600` |
| Hover background | `hover:bg-gray-50` |
| Active nav item | `bg-gray-100 text-gray-900` |
| Primary button | `bg-gray-900 text-white hover:bg-gray-800` |

### Status pattern (deals, activities, badges)

Always pair a **`-100` background with a `-700` text**. Never deviate.

`New` blue · `Keep in touch` sky · `Contacted` purple · `Qualified` amber ·
`Proposal Sent` orange · `Negotiation` pink · `Commit` violet · `Won` emerald ·
`Lost` gray-500 · `Archived` slate-500.

### Typography scale

| Use | Classes |
|-----|---------|
| Page title (h1) | `text-2xl font-semibold text-gray-900` |
| Section title (h2) | `text-lg font-semibold text-gray-900` |
| KPI value | `text-3xl font-semibold text-gray-900` |
| Label / subtitle | `text-sm font-medium text-gray-500` |
| Body | `text-sm text-gray-600` |
| Help / timestamp | `text-xs text-gray-400` |
| Badge | `text-xs font-medium` |

Headings are `font-semibold`; interactive labels are `font-medium`.
**`font-bold` is reserved for the logo mark only.**

### Spacing · Radius · Elevation

- **Sections:** `space-y-8`. **Grid cards:** `gap-4`. **Card padding:** `p-5` (KPI) / `p-6` (section).
- **Radius ladder (small → large):** badges `rounded-md`/`rounded-full` → buttons `rounded-lg` → interactive rows/inputs `rounded-xl` → cards/panels `rounded-2xl`. Never bare `rounded`.
- **Elevation:** every card has **both** `border border-gray-200` **and** `shadow-sm`. Hover → `shadow-md`. Elevated (drag/dropdown) → `shadow-lg`. No border without shadow, no shadow without border.

### Icons (Lucide)

`h-5 w-5` nav/KPI · `h-4 w-4` buttons/feed · `h-3 w-3` inline metadata.
Default `text-gray-600`, or match the semantic color inside a status badge.
Always add `shrink-0` next to truncatable text.

---

## Non-negotiable rules

**Do**
- Use Lucide icons exclusively.
- Use the `-100 / -700` pattern for every status indicator.
- `truncate` any text that can overflow; `tabular-nums` for aligned numbers.
- Match loading skeletons to the shape and radius of real content (`animate-pulse`).
- Use `transition-colors` on interactive elements.

**Don't**
- Raw hex in JSX (exception: Recharts `stroke`/`fill` props).
- `font-bold` outside the logo.
- Bare `rounded` (always a size suffix).
- `shadow-md` as a default card state (use `shadow-sm`).
- `transition-all` (be specific).
- New CSS classes — Tailwind utilities only.

---

## Canonical components

Copy-paste patterns (KPI card, section card, page header, primary/secondary
button, status badge, activity-feed item, dropdown, skeleton, empty state) are
documented in full in `crm-design-guidelines/SKILL.md`. Standalone, renderable
previews of the core set live in [`components/`](./components) — these double as
the Claude Design card library (see below).

---

## Publish to Claude Design (agents "rule" the design system)

Claude Design has **no public API/MCP**, but Claude Code can read and write your
`claude.ai/design` design-system projects through the first-party **`DesignSync`**
tool, driven by the **`/design-sync`** skill. This is how an agent keeps the
shared Claude Design design system in lockstep with this repo.

**Workflow (user starts it):**
1. Run `/design-sync` in Claude Code (sign in / `/design-login` if prompted for design scope).
2. The skill lists your writable design-system projects (`list_projects`) — pick one or create a new one.
3. It builds a structural diff between `components/` here and the remote project.
4. Review the plan; on approval it pushes **one component at a time** (never a wholesale replace).
5. Each preview's first line carries a `<!-- @dsCard group="…" -->` marker, so it shows up as a card in the Claude Design **Design System** pane automatically.

After publishing, every new Claude Design project in the org inherits these
Globalbit components and tokens — so prompt-to-prototype output is on-brand by
default, and the reverse hand-off (**Export → Send to Claude Code**) lands back
here for implementation.

---

## Source of truth & drift

- Tokens here are distilled from `crm-design-guidelines` (app) and `tailwind-patterns` (web).
- If those change, update `DESIGN.md` and `components/` here, then re-run `/design-sync`.
- When auditing existing UI for compliance, pair with the `web-design-guidelines` and `accessibility` skills.
</content>
</invoke>

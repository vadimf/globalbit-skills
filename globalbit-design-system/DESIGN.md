# Globalbit — DESIGN.md

Portable design-system spec. Drop this into Claude Design, a new repo, or hand it
to any AI agent to make output on-brand. Canonical source: `globalbit-skills`.

## Brand

- **Typeface:** Inter (400/500/600). Headings 600, labels 500. **Never 700 except the logo.**
- **Primary action color:** `#111827` (gray-900), white text, hover `#1f2937` (gray-800).
- **Brand mark:** black square, white glyph, `rounded-lg`.
- **Accent:** `#6366f1` (indigo-500) — data viz and highlights only, used sparingly.
- **Neutrals:** gray scale for all structural UI. No raw hex in markup (exception: chart libs).

## Color roles

| Role | Product/app (Tailwind) | Hex |
|------|------------------------|-----|
| Page background | `bg-gray-50` | `#f9fafb` |
| Surface / card | `bg-white` | `#ffffff` |
| Border | `border-gray-200` | `#e5e7eb` |
| Text primary | `text-gray-900` | `#111827` |
| Text secondary | `text-gray-500` | `#6b7280` |
| Text muted | `text-gray-400` | `#9ca3af` |
| Icon default | `text-gray-600` | `#4b5563` |
| Primary button | `bg-gray-900` | `#111827` |
| Accent | `#6366f1` | `#6366f1` |

Website variant uses semantic tokens (`bg-background`, `text-foreground`,
`bg-primary`, `text-muted-foreground`, `border-border`) mapped to the values
above, with dark-mode equivalents.

## Status colors — `-100` bg / `-700` text

new=blue · keep-in-touch=sky · contacted=purple · qualified=amber ·
proposal-sent=orange · negotiation=pink · commit=violet · won=emerald ·
lost=gray-500 · archived=slate-500.

## Type scale

| Token | Class |
|-------|-------|
| h1 / page title | `text-2xl font-semibold` |
| h2 / section | `text-lg font-semibold` |
| kpi value | `text-3xl font-semibold` |
| label | `text-sm font-medium text-gray-500` |
| body | `text-sm text-gray-600` |
| caption | `text-xs text-gray-400` |

## Spacing

Sections `space-y-8` · grid `gap-4` · KPI card `p-5` · section card `p-6` ·
icon↔text `gap-2`/`gap-3`. Scale increments of 4 (4, 6, 8, 12, 16, 24).

## Radius ladder

badge `rounded-md`/`rounded-full` → button `rounded-lg` → input/row `rounded-xl`
→ card/panel `rounded-2xl`. Progressively rounder from small to large. Never bare `rounded`.

## Elevation

Card = `border border-gray-200` **and** `shadow-sm` (both, always).
Hover `shadow-md`. Dropdown/drag `shadow-lg`.

## Icons

Lucide only. `h-5 w-5` (nav/KPI), `h-4 w-4` (buttons/feed), `h-3 w-3` (inline).
`shrink-0` beside truncatable text.

## Motion

`transition-colors` on interactive elements; `transition-shadow` for drag.
Tailwind default duration (150ms). Never `transition-all`.

## Charts (Recharts)

Grid `strokeDasharray="3 3" stroke="#f0f0f0"` · primary data `#111827` ·
secondary `#6366f1` · area fill opacity 0.1/0.05 · bar radius `[4,4,0,0]` ·
tooltip 12px radius, `1px solid #e5e7eb`.

## Rules digest

Lucide only · `-100/-700` status · `truncate` overflow · `tabular-nums` columns ·
skeletons match shape + `animate-pulse` · no raw hex (except charts) · no
`font-bold` (except logo) · no bare `rounded` · `shadow-sm` default · no
`transition-all` · Tailwind utilities only.
</content>

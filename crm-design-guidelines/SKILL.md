---
name: crm-design-guidelines
description: >
  Design guidelines for the Globalbit CRM. Covers layout, colors, typography,
  components, spacing, and patterns. Follow these rules when building or
  modifying any CRM UI to keep the interface consistent.
---

# Globalbit CRM — Design Guidelines

These guidelines describe every visual convention used in the CRM.
Follow them exactly when creating or editing any component or page.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 16 (App Router, `"use client"` pages) |
| Styling | Tailwind CSS 4 (`@import "tailwindcss"`) |
| Font | Inter (Google Fonts, `--font-inter`) |
| Icons | Lucide React — **only** use Lucide icons |
| Charts | Recharts (`AreaChart`, `BarChart`, `ResponsiveContainer`) |
| Rich Text | Tiptap (`@tiptap/react`, `@tiptap/starter-kit`) |
| Drag & Drop | `@hello-pangea/dnd` |
| Dates | `date-fns` |
| Backend | Firebase (Firestore, Auth, Functions) |

---

## Layout

```
┌──────────────────────────────────────────────┐
│  Sidebar (w-64, fixed, hidden on mobile)     │
│  ┌────────────────────────────────────────┐  │
│  │ Logo bar  h-16  border-b              │  │
│  │ Nav items  space-y-1  p-4             │  │
│  │ User section  border-t  p-4           │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  Main content  (ml-64 on lg)                 │
│  ┌────────────────────────────────────────┐  │
│  │ max-w-7xl  px-4 py-6  sm:px-6 lg:px-8│  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

| Element | Classes |
|---------|---------|
| Page background | `bg-gray-50` |
| Sidebar background | `bg-white` |
| Sidebar border | `border-r border-gray-200` |
| Main content | `lg:ml-64`, `mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8` |
| Mobile header | Visible `lg:hidden`, same border/bg as sidebar |

**Rules:**
- Every authenticated page wraps content in `<AppShell>`.
- Sidebar is hidden below `lg` breakpoint; `<MobileHeader>` shows instead.
- Page content spacing: `space-y-8` between major sections.

---

## Color System

### Base Palette

The CRM uses a **neutral gray** palette for all structural UI.
Never use raw color values — always use Tailwind classes.

| Use | Class |
|-----|-------|
| Page background | `bg-gray-50` |
| Card / panel background | `bg-white` |
| Card border | `border-gray-200` |
| Primary text | `text-gray-900` |
| Secondary text | `text-gray-500` |
| Tertiary / muted text | `text-gray-400` |
| Icon default | `text-gray-600` |
| Icon muted | `text-gray-400` |
| Hover background | `hover:bg-gray-50` |
| Active nav item | `bg-gray-100 text-gray-900` |
| Inactive nav item | `text-gray-600 hover:bg-gray-50 hover:text-gray-900` |

### Primary Action (Dark)

| Use | Class |
|-----|-------|
| Primary button | `bg-gray-900 text-white` |
| Primary button hover | `hover:bg-gray-800` |
| Logo square | `rounded-lg bg-black text-white` |

### Accent — Indigo

Used sparingly for data visualization and highlights.

| Use | Value |
|-----|-------|
| Chart fill / stroke | `#6366f1` (indigo-500) |
| Drag-over highlight | `bg-blue-50/50` |
| Drag active border | `border-blue-300` |

### Semantic Status Colors

Used for deal stages, activity types, and status badges.
Always pair a `-100` background with a `-700` (or `-600`) text.

| Stage | Background | Text |
|-------|-----------|------|
| New | `bg-blue-100` | `text-blue-700` |
| Keep in touch | `bg-sky-100` | `text-sky-700` |
| Contacted | `bg-purple-100` | `text-purple-700` |
| Qualified | `bg-amber-100` | `text-amber-700` |
| Proposal Sent | `bg-orange-100` | `text-orange-700` |
| Negotiation | `bg-pink-100` | `text-pink-700` |
| Commit | `bg-violet-100` | `text-violet-700` |
| Won | `bg-emerald-100` | `text-emerald-700` |
| Lost | `bg-gray-100` | `text-gray-500` |
| Archived | `bg-slate-100` | `text-slate-500` |

Activity types follow the same `-100 / -700` pattern:

| Activity | Background | Text |
|----------|-----------|------|
| New Lead | `bg-green-100` | `text-green-700` |
| Email Sent | `bg-blue-100` | `text-blue-700` |
| Email Clicked | `bg-purple-100` | `text-purple-700` |
| Call Made | `bg-amber-100` | `text-amber-700` |
| Note Added | `bg-gray-100` | `text-gray-700` |
| Stage Changed | `bg-indigo-100` | `text-indigo-700` |
| Revisited | `bg-teal-100` | `text-teal-700` |

**Color rules:**
- Never use raw hex colors in components — use Tailwind classes only.
- Status badges: always `bg-{color}-100 text-{color}-700` pattern.
- Charts may use hex values for `stroke`, `fill` props (Recharts requirement).

---

## Typography

| Use | Classes |
|-----|---------|
| Page title (h1) | `text-2xl font-semibold text-gray-900` |
| Section title (h2) | `text-lg font-semibold text-gray-900` |
| Card label / subtitle | `text-sm font-medium text-gray-500` |
| KPI value | `text-3xl font-semibold text-gray-900` |
| Body text | `text-sm text-gray-600` |
| Help text / timestamp | `text-xs text-gray-400` |
| Metadata / detail | `text-xs text-gray-500` |
| Sidebar title | `text-lg font-semibold text-gray-900` |
| Nav item | `text-sm font-medium` |
| Button text | `text-sm font-medium` |
| Badge / tag | `text-xs font-medium` |

**Rules:**
- Use `font-semibold` for headings, `font-medium` for labels and interactive elements.
- Never use `font-bold` except inside the logo mark.
- Use `truncate` on any text that could overflow (names, emails, messages).
- Use `line-clamp-2` for preview text (e.g., lead messages).
- Numbers that align in columns should use `tabular-nums`.

---

## Spacing

| Context | Approach |
|---------|----------|
| Between page sections | `space-y-8` |
| Grid cards | `gap-4` |
| Inside cards | `p-5` (KPI cards), `p-6` (chart / section cards) |
| Kanban column items | `space-y-2`, card padding `p-3` |
| Activity feed items | `space-y-1`, item padding `px-3 py-2.5` |
| Between icon + text | `gap-2` or `gap-3` |
| Between small icon + text | `gap-1.5` |
| Sidebar nav items | `space-y-1`, item padding `px-3 py-2.5` |

---

## Border Radius

| Element | Radius |
|---------|--------|
| Cards, panels, chart containers | `rounded-2xl` |
| Interactive elements (nav, activity rows, inputs) | `rounded-xl` |
| Buttons, dropdowns | `rounded-lg` |
| Badges, tags, status pills | `rounded-md` or `rounded-full` |
| Icon containers (large, 10×10) | `rounded-xl` |
| Icon containers (small, 8×8) | `rounded-lg` |
| Avatars | `rounded-full` |
| Logo mark | `rounded-lg` |

**Rule:** Components should get progressively rounder from small (badges) to large (cards). Never use `rounded` alone — always use a size suffix.

---

## Shadows & Borders

| Element | Classes |
|---------|---------|
| Default card | `border border-gray-200 shadow-sm` |
| Card on hover | `hover:shadow-md` |
| Dragging card | `border-blue-300 shadow-lg` |
| Dropdown menu | `border border-gray-200 shadow-lg` |
| Chart tooltip | `border: 1px solid #e5e7eb`, `box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05)` |

**Rules:**
- Every card must have both `border border-gray-200` AND `shadow-sm`.
- Elevated items (drag, dropdown) use `shadow-lg`.
- No shadows without borders and no borders without shadows on cards.

---

## Components Reference

### KPI Card

```tsx
<div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
  <div className="flex items-center gap-3">
    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gray-100">
      <Icon className="h-5 w-5 text-gray-600" />
    </div>
    <p className="text-sm font-medium text-gray-500">{label}</p>
  </div>
  <p className="mt-3 text-3xl font-semibold text-gray-900">{value}</p>
</div>
```

### Section Card (Charts, Activity Feed, Tables)

```tsx
<div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
  <h2 className="mb-4 text-lg font-semibold text-gray-900">{title}</h2>
  {/* content */}
</div>
```

### Page Header

```tsx
<div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
  <div>
    <h1 className="text-2xl font-semibold text-gray-900">{title}</h1>
    <p className="text-sm text-gray-500">{subtitle}</p>
  </div>
  <div className="flex gap-2">
    {/* Action buttons */}
  </div>
</div>
```

### Button — Primary

```tsx
<button className="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 transition-colors">
  {label}
</button>
```

### Button — Secondary (Toggle / Period Selector)

```tsx
// Active
<button className="rounded-lg px-3 py-1.5 text-sm font-medium bg-gray-900 text-white">
  {label}
</button>
// Inactive
<button className="rounded-lg px-3 py-1.5 text-sm font-medium bg-white text-gray-600 border border-gray-200 hover:bg-gray-50">
  {label}
</button>
```

### Status Badge

```tsx
<span className="rounded-md px-2.5 py-0.5 text-xs font-medium bg-blue-100 text-blue-700">
  {stage}
</span>
```

### Counter Badge

```tsx
<span className="text-xs font-medium text-gray-400 bg-gray-50 px-2.5 py-1 rounded-full">
  {count} items
</span>
```

### Activity Feed Item

```tsx
<Link
  href={detailUrl}
  className="flex items-center gap-3 rounded-xl px-3 py-2.5 hover:bg-gray-50 transition-colors"
>
  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-green-100 text-green-700">
    <Icon className="h-4 w-4" />
  </div>
  <div className="flex-1 min-w-0">
    <div className="flex items-center gap-2">
      <span className="text-sm font-medium text-gray-900 truncate">{name}</span>
      <span className="text-xs text-gray-400 shrink-0">{typeLabel}</span>
    </div>
    <p className="text-xs text-gray-500 truncate">{description}</p>
  </div>
  <span className="text-xs text-gray-400 shrink-0 tabular-nums">{time}</span>
</Link>
```

### Loading Skeleton

```tsx
// Card skeleton
<div className="h-28 animate-pulse rounded-2xl bg-gray-200" />

// Row skeleton
<div className="h-12 animate-pulse rounded-xl bg-gray-100" />

// Chart skeleton
<div className="h-64 animate-pulse rounded-xl bg-gray-100" />
```

**Skeleton rules:**
- Match the shape and `rounded-*` of the real component.
- Use `bg-gray-200` for prominent skeletons (cards), `bg-gray-100` for content areas.
- Always use `animate-pulse`.

### Dropdown Menu

```tsx
<div className="absolute left-0 top-full z-50 mt-1 w-40 rounded-lg border border-gray-200 bg-white shadow-lg py-1">
  <button className="flex w-full items-center gap-2 px-3 py-1.5 text-left text-xs hover:bg-gray-50">
    {option}
  </button>
</div>
```

### Empty State

```tsx
<p className="text-sm text-gray-400 text-center py-8">
  No items yet
</p>
```

---

## Icons

- **Library:** Lucide React — `import { IconName } from "lucide-react"`
- **Standard size:** `h-5 w-5` (nav, KPI cards)
- **Small size:** `h-4 w-4` (buttons, activity feed, metadata)
- **Tiny size:** `h-3 w-3` (inline metadata, secondary info)
- **Large size:** `h-2.5 w-2.5` inside small indicator circles
- **Color:** `text-gray-600` default, or match semantic color when inside status badges
- **Flex shrink:** Always add `flex-shrink-0` (or `shrink-0`) on icons next to truncatable text

---

## Charts (Recharts)

| Property | Value |
|----------|-------|
| Container | `<ResponsiveContainer width="100%" height="100%">` inside `h-64` div |
| Grid | `strokeDasharray="3 3" stroke="#f0f0f0"` |
| Axis ticks | `fontSize: 12` |
| Tooltip border radius | `12px` |
| Tooltip border | `1px solid #e5e7eb` |
| Tooltip shadow | `0 4px 6px -1px rgb(0 0 0 / 0.05)` |
| Primary data color | `#111827` (gray-900) |
| Secondary data color | `#6366f1` (indigo-500) |
| Area fill opacity | `0.1` (primary), `0.05` (secondary) |
| Bar radius | `[4, 4, 0, 0]` (rounded top corners) |
| Axis labels | `fontSize: 11`, appropriate fill color |

---

## Responsive Breakpoints

| Breakpoint | Use |
|-----------|-----|
| Default (mobile) | Single column, mobile header visible, sidebar hidden |
| `sm` (640px) | 2-column grids, side-by-side header layout |
| `lg` (1024px) | Sidebar visible, 3-column KPI grid, desktop padding |

Grid patterns:
- KPI cards: `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3`
- Kanban: horizontal scroll, `w-72` per column, `flex-shrink-0`
- Tables: full-width with horizontal scroll on mobile

---

## Transitions

- All interactive elements: `transition-colors`
- Drag states: `transition-shadow`
- Duration: use Tailwind defaults (150ms)
- Never use `transition-all` — be specific

---

## Do's and Don'ts

### Do

- Use `"use client"` directive on interactive pages
- Wrap authenticated pages in `<AppShell>`
- Use Lucide icons exclusively
- Use the `-100 / -700` color pattern for all status indicators
- Add `truncate` to any potentially overflowing text
- Include loading skeletons that match the shape of real content
- Use `transition-colors` on interactive elements

### Don't

- Use raw hex colors in JSX (except Recharts props)
- Use `font-bold` (use `font-semibold` instead)
- Mix icon libraries (no Heroicons, no FontAwesome)
- Use `rounded` without a size suffix
- Use `shadow-md` for default card state (use `shadow-sm`)
- Put logic in `layout.tsx` — keep it minimal (metadata + providers)
- Create new CSS classes — use Tailwind utilities only

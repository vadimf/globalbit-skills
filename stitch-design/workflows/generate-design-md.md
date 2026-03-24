---
description: Extract a DESIGN.md design system from a Stitch project's anchor screen.
---

# Workflow: Generate DESIGN.md

Extract the visual source of truth from a Stitch-generated screen and synthesize it into a `.stitch/DESIGN.md` file.

## When to Use

- After the first screen (anchor screen) is approved
- To create a shared design language for all subsequent pages
- When onboarding new pages that need visual consistency

## Steps

### 1. Generate the Anchor Screen
Follow the [text-to-design](text-to-design.md) workflow to generate and approve the first screen.

### 2. Get the Generation Output
The `generate` command returns a `designSystem` object with:
- Design system name
- Heading and body fonts
- Accent color
- Full `designMd` content (Stitch auto-generates this)

### 3. Download the Screen
```bash
STITCH_API_KEY="$KEY" node .agents/skills/stitch-design/scripts/stitch-cli.mjs download <projectId> <screenId> web/.stitch/designs/
```

### 4. Inspect the HTML
Open the downloaded `.html` file and extract:
- Color palette (inspect CSS custom properties)
- Typography stack (font-family declarations)
- Spacing scale
- Border radius values
- Shadow definitions
- Button styles

### 5. Synthesize DESIGN.md
Create `web/.stitch/DESIGN.md` with these sections:

```markdown
# [Project Name] Design System

## Color Palette
| Role | Name | Hex | Usage |
|------|------|-----|-------|
| Primary | Electric Lime | #A3FF00 | CTAs, highlights |
| Background | White | #FFFFFF | Main sections |

## Typography
- **Headings**: Space Grotesk (bold)
- **Body**: Manrope (regular, 16px base)
- **Captions**: Manrope (medium, 14px)

## Spacing & Layout
- Section padding: 80px vertical
- Card border-radius: 16px
- Button border-radius: 12px

## Component Patterns
[Describe reusable patterns observed in the anchor screen]
```

### 6. Use for All Subsequent Pages
Include DESIGN.md tokens in every future prompt to maintain visual consistency.

## Tips
- **Stitch auto-DESIGN.md**: Check `designSystem.designMd` in the generate output — Stitch often produces a full design system document automatically.
- **Don't over-specify**: Capture the essential tokens, not every CSS detail.
- **Living document**: Update DESIGN.md as the design evolves across pages.

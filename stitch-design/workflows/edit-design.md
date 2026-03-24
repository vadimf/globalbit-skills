---
description: Edit existing Stitch screens with targeted text prompts via CLI.
---

# Workflow: Edit Design

Make targeted adjustments to an existing Stitch screen without regenerating from scratch.

## When to Use

- Fine-tuning colors, spacing, or typography
- Changing specific copy or CTAs
- Adding/removing a section
- Adjusting responsive layout

## Steps

### 1. Identify the Screen
Get the `projectId` and `screenId` from:
- Previous generation output
- `.stitch/designs/*.meta.json` files
- Running `list-screens`:
```bash
STITCH_API_KEY="$KEY" node .agents/skills/stitch-design/scripts/stitch-cli.mjs list-screens <projectId>
```

### 2. Write Edit Prompt
Write a focused edit prompt to a file. Be specific about what to change:
```markdown
# web/.stitch/prompts/hero-edit.md

Change the hero background from white to near-black (#0A0A0A).
Make the headline text white (#FFFFFF).
Increase the CTA button size by 20%.
Keep everything else the same.
```

### 3. Apply the Edit
```bash
STITCH_API_KEY="$KEY" node .agents/skills/stitch-design/scripts/stitch-cli.mjs edit <projectId> <screenId> web/.stitch/prompts/hero-edit.md
```

### 4. Download Updated Assets
```bash
STITCH_API_KEY="$KEY" node .agents/skills/stitch-design/scripts/stitch-cli.mjs download <projectId> <screenId> web/.stitch/designs/
```

### 5. Present Changes
Show the user the updated screenshot. Compare with the previous version if available.

## Tips
- **Be surgical**: Only describe what should change, not the entire page.
- **Reference elements**: Use terms like "the hero section", "the pricing card", "the navigation bar".
- **Preserve consistency**: If editing colors, mention the design system palette to maintain harmony.

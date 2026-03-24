---
description: Generate new screens from a text prompt using the Stitch CLI.
---

# Workflow: Text-to-Design

Transform a text description into a high-fidelity design screen.

## Steps

### 1. Enhance the User Prompt
Before generating, apply the [Prompt Enhancement Pipeline](../SKILL.md#-prompt-enhancement-pipeline).
- Identify the platform (Web/Mobile) and page type.
- Incorporate any existing project design system from `.stitch/DESIGN.md`.
- Use specific [Design Mappings](../references/design-mappings.md) and [Prompting Keywords](../references/prompt-keywords.md).

### 2. Write Prompt to File
Save the enhanced prompt to a `.md` file in your prompts directory:
```bash
# Example: web/.stitch/prompts/homepage.md
```

### 3. Identify the Project
Use `list-projects` to find the correct project ID if it is not already known:
```bash
STITCH_API_KEY="$KEY" node .agents/skills/stitch-design/scripts/stitch-cli.mjs list-projects
```
Or create a new one:
```bash
STITCH_API_KEY="$KEY" node .agents/skills/stitch-design/scripts/stitch-cli.mjs create-project "My App"
```

### 4. Generate the Screen
```bash
STITCH_API_KEY="$KEY" node .agents/skills/stitch-design/scripts/stitch-cli.mjs generate <projectId> web/.stitch/prompts/homepage.md --device DESKTOP
```

> [!IMPORTANT]
> This can take **2–5 minutes**. Do NOT retry. If it times out, use `list-screens` to check.

### 5. Present AI Feedback
Parse the JSON output and show the user:
- `text` — Stitch's description of what it generated
- `suggestions` — Follow-up ideas (e.g., "Add a mobile version")
- `screens[0].screenId` — Needed for download/edit

### 6. Download Design Assets
```bash
STITCH_API_KEY="$KEY" node .agents/skills/stitch-design/scripts/stitch-cli.mjs download <projectId> <screenId> web/.stitch/designs/
```

### 7. Review and Refine
- If the result needs tweaks, use the [edit-design](edit-design.md) workflow.
- Do NOT re-generate from scratch unless the fundamental layout is wrong.

## Tips
- **Be structural**: Break the page down into header, hero, features, and footer.
- **Specify colors**: Use hex codes for precision.
- **Set the tone**: Explicitly mention if the design should be minimal, professional, or vibrant.

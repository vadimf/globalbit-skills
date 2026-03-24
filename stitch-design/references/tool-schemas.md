# Stitch CLI — Command Reference

All commands are run via:
```bash
STITCH_API_KEY="<key>" node .agents/skills/stitch-design/scripts/stitch-cli.mjs <command> [args...]
```

---

## 🏗️ Project Management

### `create-project`
Creates a new Stitch project. Returns project metadata with ID.
```bash
node stitch-cli.mjs create-project "Zetra Website"
```
Output:
```json
{
  "name": "projects/15425236754889579409",
  "title": "Zetra Website",
  "visibility": "PRIVATE"
}
```

### `list-projects`
Lists all Stitch projects accessible to the authenticated user.
```bash
node stitch-cli.mjs list-projects
```

---

## 🎨 Design Generation

### `generate`
Generates a new screen from a text prompt file. Prompt file can be `.txt`, `.md`, or `.json`.
```bash
node stitch-cli.mjs generate 15425236754889579409 prompts/homepage.md --device DESKTOP
```
Output:
```json
{
  "projectId": "15425236754889579409",
  "sessionId": "10603445688400819722",
  "screens": [
    { "name": "projects/.../screens/ce1a602774f8...", "screenId": "ce1a602774f8...", "title": "Homepage" }
  ],
  "designSystem": { "name": "Zetra Kinetic", "font": "SPACE_GROTESK", "accent": "#A3FF00" },
  "suggestions": ["Add a mobile version", "Design the pricing page"],
  "text": "I've created a premium homepage..."
}
```

> [!IMPORTANT]
> Generation can take **2–5 minutes**. Do NOT retry — check `list-screens` if the command times out.

### `edit`
Edits an existing screen with a text prompt.
```bash
node stitch-cli.mjs edit 15425236754889579409 ce1a602774f8... prompts/hero-edit.md
```

---

## 🖼️ Screen Management

### `list-screens`
Lists all screens in a project.
```bash
node stitch-cli.mjs list-screens 15425236754889579409
```

### `get-screen`
Retrieves metadata (title, dimensions, download URLs) for a specific screen.
```bash
node stitch-cli.mjs get-screen 15425236754889579409 ce1a602774f8...
```

### `download`
Downloads the HTML code and screenshot PNG to a local directory. Also saves a `.meta.json` file.
```bash
node stitch-cli.mjs download 15425236754889579409 ce1a602774f8... web/.stitch/designs/
```
This creates:
```
web/.stitch/designs/
├── homepage-concept.html      # Full HTML with inline CSS/JS
├── homepage-concept.png       # Screenshot image
└── homepage-concept.meta.json # Metadata (dimensions, device, IDs)
```

---

## 📝 Prompt File Formats

### Plain text (`.txt` / `.md`)
The entire file content becomes the prompt:
```markdown
A modern pricing page with 3 tiers. Dark background. Neon green accent (#A3FF00).
Monthly: $9.99. Yearly: $49.99 (highlighted). Weekly: $4.99.
```

### JSON (`.json`)
Must contain a `"prompt"` key:
```json
{
  "prompt": "A modern pricing page with 3 tiers..."
}
```
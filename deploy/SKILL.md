---
name: deploy
description: |
  Deploy the Globalbit website to Firebase Hosting (static pages) and/or Firebase Functions.
  
  Use when: "deploy", "push to production", "deploy functions", "deploy hosting", 
  "build and deploy", "push changes live".

user-invocable: true
allowed-tools: ["Bash"]
---

# Globalbit Deploy Skill

> **RULE: Always deploy after making changes. Never tell the user to deploy — just do it yourself.**
> The user expects all deployments to happen automatically as part of any workflow.

This project has **two independent deployable targets**:

| Target | Directory | Command |
|--------|-----------|---------|
| **Static site** (Next.js → Firebase Hosting) | `/` (root) | `firebase deploy --only hosting` |
| **Firebase Functions** (CRM backend) | `crm/functions/` | `firebase deploy --only functions` |

They are always deployed independently. Never run `firebase deploy` without `--only` to avoid accidentally deploying both.

---

## 0. Pre-Deploy: Image Optimization Check

**MANDATORY before every hosting deploy.** Ensures all images are WebP and properly sized.

### Step 0a: Find non-WebP image references in code

```bash
grep -rn '\.png\|\.jpg\|\.jpeg' app/ components/ data/ --include="*.tsx" --include="*.ts" \
  | grep -v 'node_modules' \
  | grep -v 'og-default' \
  | grep -v 'email-header' \
  | grep -v 'signature/' \
  | grep -v '//' \
  | grep -E 'src=|image[=:]|Image|background|logo'
```

If output is empty → skip to Step 1. If matches found → fix them:

### Step 0b: Convert any new PNG/JPG images to WebP

For each PNG/JPG file in `public/images/` that doesn't have a `.webp` version:

```bash
find public/images -not -path "*/signature/*" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) \
  ! -name "og-default.png" ! -name "email-header.png" -print0 | \
  while IFS= read -r -d '' f; do
    base="${f%.*}"
    if [ ! -f "${base}.webp" ]; then
      ext="${f##*.}"
      q=95; [ "$ext" = "jpg" ] || [ "$ext" = "jpeg" ] && q=90
      cwebp -q $q "$f" -o "${base}.webp" 2>/dev/null && echo "Converted: $f" || echo "FAIL: $f"
    fi
  done
```

> [!CAUTION]
> **Image quality is crucial.** Use high quality settings to prevent visible degradation:
>
> - Quality **95** for PNGs (graphics/screenshots/illustrations)
> - Quality **90** for JPGs (photos)
>
> Do NOT reduce quality below these thresholds. Smaller file sizes are not worth visible artifacts.

> [!IMPORTANT]
> **Never convert** these files (email clients and social platforms need PNG):
>
> - `og-default.png` — OG meta tags
> - `email-header.png` — used in CRM lead emails
> - `images/signature/*` — email signature images (must stay PNG for email client compatibility)
>
> For small images (cards, logos), add `-resize WIDTH 0` to resize during conversion:
>
> - Card thumbnails: `-resize 640 0`
> - Hero/full-width: `-resize 1440 0`
> - Logos: `-resize 240 0`
> - Mobile images: `-resize 750 0`

### Step 0c: Update code references

Change all `.png`/`.jpg`/`.jpeg` paths in source files to `.webp`. Use the multi_replace_file_content tool
or search-and-replace. Then re-run the grep from Step 0a to confirm zero matches.

### Step 0d: Delete old source files (optional)

```bash
find public/images -not -path "*/signature/*" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) \
  ! -name "og-default.png" ! -name "email-header.png" -print0 | \
  while IFS= read -r -d '' f; do
    base="${f%.*}"
    if [ -f "${base}.webp" ]; then
      rm "$f" && echo "Deleted: $f"
    fi
  done
```

> [!CAUTION]
> **Never delete** `og-default.png` or `email-header.png` — these must remain as PNG.

---

## 1. Deploy Static Site (Hosting)

This is the most common deploy. Run from the **root** of the project.

### Steps

// turbo

```bash
# Step 1: Kill any running dev server on port 3000
lsof -ti:3000 | xargs kill -9 2>/dev/null; true
```

// turbo

```bash
# Step 2: Clean build
rm -rf .next out
```

// turbo

```bash
# Step 3: Build (Next.js 16 with Turbopack)
npm run build
```

```bash
# Step 4: Verify build succeeded (exit code 0) and check output
# The build output should list all routes with ○ (Static) or ● (SSG)
```

```bash
# Step 5: Deploy to Firebase Hosting
firebase deploy --only hosting
```

// turbo

```bash
# Step 6: Purge Cloudflare edge cache (ensures visitors see latest version)
source .env.local
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/purge_cache" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}' | python3 -c "import sys,json;r=json.load(sys.stdin);print('✅ CF cache purged' if r.get('success') else '❌ CF purge failed:', r.get('errors',''))"
```

### Expected Output

- Build: `Exit code: 0` with all pages listed
- Deploy: `✔  Deploy complete!` with hosting URL
- Cache purge: `✅ CF cache purged`

### Live URLs

- **Primary**: <https://2026.globalbit.co.il>
- **Firebase**: <https://globalbit-website-2026.web.app>

---

## 2. Deploy Firebase Functions (CRM backend)

Functions live in `crm/functions/`. Deploy separately from the main site.

### Steps

```bash
# Step 1: Navigate to functions directory
cd crm/functions

# Step 2: Install dependencies if needed
npm install

# Step 3: Build TypeScript
npm run build

# Step 4: Return to root and deploy
cd ../..
firebase deploy --only functions
```

> [!WARNING]
> Always build functions before deploying. Deploying unbuilt JS will fail or deploy stale code.

---

## 3. Deploy Both (Full Deploy)

Only do this when you've changed both the site AND functions in the same session.

```bash
# Build site
rm -rf .next out && npm run build

# Build functions
cd crm/functions && npm run build && cd ../..

# Deploy both
firebase deploy --only hosting,functions

# Purge CF cache
source .env.local
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/purge_cache" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}' | python3 -c "import sys,json;r=json.load(sys.stdin);print('✅ CF cache purged' if r.get('success') else '❌ CF purge failed:', r.get('errors',''))"
```

---

## 4. Troubleshooting

### Build fails with Turbopack errors

```bash
# Fallback: build with Webpack
npx next build --webpack
```

### `Cannot find module` errors in functions

```bash
cd crm/functions && npm install && npm run build
```

### Port 3000 still in use

```bash
lsof -ti:3000 | xargs kill -9
```

### Rollback hosting to previous version

Go to [Firebase Console → Hosting](https://console.firebase.google.com/project/globalbit-website-2026/hosting) and click "Rollback" on the previous version.

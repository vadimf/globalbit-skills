---
description: Test and improve speed and Core Web Vitals for a Next.js (React) website deployed on Firebase Hosting by automatically discovering all site URLs, running repeatable lab audits, collecting field vitals instrumentation, and producing a prioritized fix plan mapped to code locations.
---

# Core Web Vitals (Next.js & Firebase) Auto-Auditor

## 1. Purpose

Test and improve speed and Core Web Vitals for a Next.js (React) website deployed on Firebase Hosting by automatically discovering all site URLs, running repeatable lab audits, collecting field vitals instrumentation, and producing a prioritized fix plan mapped to code locations.

## 2. Inputs

### Required

- **`base_url`**: Production base URL, for example `https://example.com`

### Optional

- **`max_urls`**: Maximum URLs to audit, default `60`
- **`crawl_depth`**: Default `5`
- **`exclude_patterns`**: Default:
  - `^/api`
  - `^/_next`
  - `^/static`
  - `^/assets`
  - `^/favicon`
  - `^/robots.txt`
  - `^/sitemap.xml`
  - `^/auth`
  - `\?`
  - `#`
- **`runs`**: Lighthouse runs per URL per strategy, default `3` (use `5` for smaller sites)
- **`strategies`**: `mobile`, `desktop`
- **`auth`**: Optional login support:
  - If the site has gated routes, the agent should run an authenticated crawl with Playwright storage state if credentials are available

## 3. URL discovery

The agent must discover URLs in this order, deduplicate, then filter:

1. **`base_url/sitemap.xml`**
   - If present, parse it and collect all `<loc>` URLs.
2. **Crawl internal links**
   - Use a crawler (Playwright or a lightweight link crawler) starting at `/`.
   - Only include same-origin URLs.
   - Respect `crawl_depth` and `max_urls`.
3. **Repo route discovery** (if repo access exists)
   - Enumerate Next.js routes from:
     - `app/**/page.*`
     - `pages/**/*.*` excluding `_app`, `_document`, `_error`, API routes
   - Convert dynamic routes to a testable set:
     - Use sitemap or crawl results to find concrete instances
     - If none exist, skip dynamic templates and report them as “unresolved”
4. **Filtering rules**
   - Remove duplicates and trailing slash variants consistently.
   - Exclude anything matching `exclude_patterns`.
   - Prefer canonical URLs.

## 4. Lab testing plan

For each discovered URL:

1. **Run Lighthouse performance audits:**
   - Mobile and desktop
   - `runs` repeated runs
   - Save JSON and HTML reports
   - Compute medians for: LCP, CLS, TBT, FCP, Speed Index, performance score
   - Extract:
     - LCP element selector and resource
     - Top opportunities and diagnostics (top 10)
2. **Handle URL limits:**
   - If the URL count exceeds `max_urls`, the agent must select a representative subset:
     - Always include: `/` (root)
     - Top N pages by internal link frequency
     - One page per major route group
   - Report which URLs were skipped and why.

## 5. Field measurement plan

Add real user Core Web Vitals collection:

1. Integrate `web-vitals` in Next.js
2. Capture: LCP, INP, CLS
3. Include route pathname and a stable page identifier
4. Send to:
   - Firebase Analytics if already enabled, otherwise
   - A lightweight endpoint (Cloud Function or Cloud Run) that logs events to BigQuery or Firestore
5. Deliverables:
   - Code changes with file paths
   - Event schema
   - A query example to view p75 by route

## 6. Firebase Hosting checks

Inspect `firebase.json`:

1. Confirm caching headers for fingerprinted assets:
   - `/_next/static/*` should be long cache and immutable
2. Confirm HTML caching strategy aligns with deployment mode
3. Confirm compression is enabled in practice (gzip or brotli where supported)
4. If SSR via rewrites:
   - Measure TTFB for SSR routes
   - Recommend mitigations: caching, edge behavior, cold start reduction

## 7. Output format

**A) URL inventory**

- Total discovered
- Included in audits
- Excluded and why

**B) Results tables**

- One table per URL with mobile and desktop medians

**C) Prioritized fix list**
Grouped into:

- Quick wins
- Medium effort
- Larger refactors

Each item must include:

- Which metric it improves (LCP, INP, CLS, TBT)
- Evidence from reports
- Exact files or components involved
- Concrete suggested change
- Expected impact and risk

**D) Regression guardrails**

- Lighthouse CI config and a CI workflow that fails on regressions.

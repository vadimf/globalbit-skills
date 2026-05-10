---
name: globalbit-document
description: Work with Google Docs using the Globalbit template — create, populate, and style professional documents via the Docs API
---

# Globalbit Document Skill

Skill for creating and editing Google Docs the Globalbit way. Handles authentication, template duplication, content insertion, styling, and all the hard-won patterns from real proposal production.

---

## When to Use This Skill

- Creating a new Globalbit-branded document from the template
- Updating/rewriting content in an existing Google Doc
- Pushing markdown-structured content to Google Docs with proper styles
- Fixing formatting or styling issues in a Google Doc

---

## Golden Rules

> These rules are absolute. Never violate them.

1. **Never center-align text** — center alignment is only for images. All text is left-aligned (or right-aligned for RTL Hebrew).
2. **Always add spacing after bullet/numbered list items** — set `spaceBelow` (8pt) + `spacingMode: "NEVER_COLLAPSE"` on every list item.
3. **Always rewrite the existing document** — never duplicate to create new versions. Work on one doc: delete old content → insert new content.
4. **Always use Google Docs native styles** — `TITLE`, `HEADING_1`, `HEADING_2`, `HEADING_3`, `NORMAL_TEXT` via `namedStyleType`. Never apply manual font sizes that bypass the doc's style definitions.
5. **Always insert content in Section 0** — BEFORE the `NEXT_PAGE` section break. Content after the break has no header/footer.
6. **Never create new section breaks** — this breaks the template's header/footer behavior.
7. **Never manipulate headers/footers programmatically** — rely on the template's built-in header/footer. The API does not reliably support header changes.
8. **Never insert blank lines before or after headings** — headings already have built-in `spaceAbove` / `spaceBelow` from the named style. Adding empty paragraphs around them creates double spacing and breaks the visual rhythm. When inserting content, place a heading directly after the previous paragraph and the next paragraph directly after the heading - no `"\n"`-only items between them.
9. **Never use em dash (`—`) or en dash (`–`)** - always use a regular hyphen (`-`) instead. Em dashes are a strong AI-writing tell and look out of place in Hebrew RTL text. Apply this in body copy, tables, and lists. When parsing markdown input that contains `—` or `–`, normalize them to `-` before insertion.
10. **List font and size must match body text** - bullet and numbered list items must use the same `weightedFontFamily` and `fontSize` as `NORMAL_TEXT` paragraphs (**Rubik 11pt** in the Globalbit template). After `createParagraphBullets`, always re-assert the text style on the list item's range. Lists in a different font or size from surrounding paragraphs look broken. Best practice: probe the doc's `NORMAL_TEXT` style for the actual font/size at runtime (in case the template changes) instead of hard-coding.

---

## IDs and Paths

| Resource | Value |
|----------|-------|
| Template Document ID | `1P2BhWQGGxeWdCYhdFP8uaUd7BqilgwKAYXnvEzfX57U` |
| Shared Drive ID | `0AIoPXOi3tfaaUk9PVA` |
| Proposals Folder ID | `14t2WcrT_bhRO6eu_YX8dcaY9ys5iXQbc` |
| **OAuth credentials (.env)** | `GWS_CLIENT_ID`, `GWS_CLIENT_SECRET` — loaded from `.env` in project root |
| OAuth refresh token | `~/.config/gws/credentials.json` → `tokens.refresh_token` |
| Client secret (fallback) | `~/.config/gws/client_secret.json` → `installed.client_id`, `installed.client_secret` |
| Cached access token | `~/.config/gws/cached_token.json` → `access_token` |
| Auth wrapper script | `scripts/gws-auth.sh` (loads `.env` automatically) |

---

## Template Architecture

The Globalbit template has a **two-section structure**:

```
Section 0 (CONTINUOUS):
  ├── Cover page (TITLE + HEADING placeholders)
  ├── Template placeholder body (DELETE this)
  └── ALL your content goes HERE ← insertion point
Section break (NEXT_PAGE) ← DO NOT cross this
Section 1 (after NEXT_PAGE):
  └── Empty paragraph (just a doc ending)
```

### How Header/Footer Works

- `useFirstPageHeaderFooter: True` → page 1 (cover) has NO header/footer
- Pages 2+ **in Section 0** → default header/footer (Globalbit logo bar)
- Section 1 → has its own **empty** header/footer overrides
- **If you insert after the NEXT_PAGE break → pages have NO header/footer**

### Cover Page Placeholders

Replace these with `replaceAllText`:

| Placeholder | Content |
|-------------|---------|
| `כותרת ראשית` | Proposal title (e.g., "הצעה לפיתוח אפליקציה") |
| `כותרת משנית 1` | Client name (e.g., "עבור: מגוריט ישראל") |
| `כותרת משנית 2` | Date (e.g., "מרץ 2026") |
| `כותרת משנית 3` | Document ID (e.g., "GB-2026-MGRT-001") |

---

## Authentication

### Python Token Refresh (Recommended)

Always use direct OAuth2 API refresh. The `gws-auth.sh` script can hang.

```python
import json, os, ssl, certifi
import urllib.request, urllib.parse

ctx = ssl.create_default_context(cafile=certifi.where())

def refresh_token():
    cache = os.path.expanduser('~/.config/gws/cached_token.json')
    cs = os.path.expanduser('~/.config/gws/client_secret.json')
    cred = os.path.expanduser('~/.config/gws/credentials.json')
    
    with open(cache) as f: data = json.load(f)
    with open(cs) as f: client = json.load(f)['installed']
    with open(cred) as f: refresh_tok = json.load(f)['tokens']['refresh_token']
    
    body = urllib.parse.urlencode({
        'client_id': client['client_id'],
        'client_secret': client['client_secret'],
        'refresh_token': refresh_tok,
        'grant_type': 'refresh_token'
    }).encode()
    
    req = urllib.request.Request('https://oauth2.googleapis.com/token',
                                 data=body, method='POST')
    with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
        result = json.loads(resp.read())
    
    data['access_token'] = result['access_token']
    with open(cache, 'w') as f: json.dump(data, f)
    return result['access_token']
```

### SSL Note (macOS)

Python 3.11+ on macOS needs `certifi` for SSL. Always use:
```python
ctx = ssl.create_default_context(cafile=certifi.where())
```
Pass `context=ctx` to all `urllib.request.urlopen` calls.

### MCP Server (google-docs-mcp)

The `google-docs-mcp` MCP server can read documents but has limitations for heavy batch operations. For reading doc content, use:
```
mcp_google-docs_google_docs_read_document(documentId)
```

For all write operations, use Python scripts with direct API calls instead.

---

## API Helper Functions

Standard boilerplate for every Google Docs script:

```python
def api(method, url, token, body=None):
    """Make an authenticated Google API request."""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()[:1000]
        print(f"API Error {e.code}: {err}")
        raise

def read_doc(doc_id, token):
    return api('GET', f"https://docs.googleapis.com/v1/documents/{doc_id}", token)

def batch_update(doc_id, token, requests):
    return api('POST',
        f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate",
        token, {'requests': requests})
```

---

## Workflow: New Document from Template

### Step 1 — Duplicate the Template

```python
TEMPLATE_ID = "1P2BhWQGGxeWdCYhdFP8uaUd7BqilgwKAYXnvEzfX57U"
FOLDER_ID = "14t2WcrT_bhRO6eu_YX8dcaY9ys5iXQbc"

resp = api('POST',
    f'https://www.googleapis.com/drive/v3/files/{TEMPLATE_ID}/copy?supportsAllDrives=true',
    token, {"name": "Proposal Title", "parents": [FOLDER_ID]})
doc_id = resp['id']
```

### Step 2 — Replace Cover Page Placeholders

```python
batch_update(doc_id, token, [
    {'replaceAllText': {
        'containsText': {'text': 'כותרת ראשית', 'matchCase': True},
        'replaceText': 'הצעה לפיתוח אפליקציה'}},
    {'replaceAllText': {
        'containsText': {'text': 'כותרת משנית 1', 'matchCase': True},
        'replaceText': 'עבור: מגוריט ישראל'}},
    {'replaceAllText': {
        'containsText': {'text': 'כותרת משנית 2', 'matchCase': True},
        'replaceText': 'מרץ 2026'}},
    {'replaceAllText': {
        'containsText': {'text': 'כותרת משנית 3', 'matchCase': True},
        'replaceText': 'GB-2026-MGRT-001'}},
])
```

### Step 3 — Delete Template Placeholder Content

Read the doc, find elements between the cover page and the `NEXT_PAGE` break, delete in reverse order.

```python
doc = read_doc(doc_id, token)
body = doc['body']['content']

# Find the NEXT_PAGE section break index
next_page_idx = None
for elem in body:
    if 'sectionBreak' in elem:
        stype = elem['sectionBreak'].get('sectionStyle', {}).get('sectionType', '')
        if stype == 'NEXT_PAGE':
            next_page_idx = elem.get('startIndex', 0)
            break

# Find where cover/TOC ends and body begins
body_start = None
for elem in body:
    if 'paragraph' in elem:
        style = elem['paragraph'].get('paragraphStyle', {}).get('namedStyleType', '')
        if style == 'HEADING_1' and body_start is None:
            body_start = elem.get('startIndex', 0)
            break

# Delete body content (keep at least one empty paragraph before section break)
if body_start and next_page_idx and next_page_idx > body_start + 1:
    batch_update(doc_id, token, [{
        'deleteContentRange': {
            'range': {'startIndex': body_start, 'endIndex': next_page_idx - 1}
        }
    }])
```

**Important:**
- `deleteContentRange` **cannot cross section breaks or tables**
- Delete in **reverse order** (highest index first)
- The last paragraph before a section break **cannot be deleted**
- Delete tables separately — each table has its own `[startIndex, endIndex]`

### Step 4 — Find Insertion Point

After deletion, re-read the doc and find the insertion point:

```python
doc = read_doc(doc_id, token)
body = doc['body']['content']

insert_idx = None
for elem in body:
    if 'sectionBreak' in elem:
        stype = elem['sectionBreak'].get('sectionStyle', {}).get('sectionType', '')
        if stype == 'NEXT_PAGE':
            break
    if 'paragraph' in elem:
        insert_idx = elem.get('startIndex', 0)
```

If the doc has NO `NEXT_PAGE` break (e.g., some existing docs use only `CONTINUOUS` breaks), find the first `HEADING_1` as the body start and the last `CONTINUOUS` break (with startIndex > 100) as the body end.

---

## Workflow: Update Existing Document

When updating content in an existing document (not a fresh template):

1. **Read doc** and analyze the structure
2. **Identify body boundaries** — find where the cover/TOC ends and where the closing section break is
3. **Delete body content** using `deleteContentRange` within the boundaries
4. **Re-read doc** after deletion to get updated indices
5. **Insert new content** at the correct index
6. **Apply styles** after all text is inserted

> **RULE**: Always rewrite the existing doc. Never create a new copy.

---

## Content Insertion (Three-Pass Approach)

### Pass 1 — Text Insertion

Build content as a list of `(text, style)` tuples, then insert in **reverse order** at the same index:

```python
items = [
    ("1. תקציר מנהלים", "H1"),
    ("", "BLANK"),
    ("גלובלביט מציעה...", "NORMAL"),
    ("מטרה ראשונה — תיאור...", "NUMBERED"),
    ("מטרה שנייה — תיאור...", "NUMBERED"),
    ("הגישה שלנו", "H2"),
    ("הגישה מבוססת על...", "NORMAL"),
    ("ניתוח שוק", "BULLET"),
    ("ראיונות", "BULLET"),
]

# Insert ALL text in reverse order at the same index
insert_requests = []
for text, style in reversed(items):
    insert_requests.append({
        'insertText': {
            'location': {'index': insert_idx},
            'text': text + '\n'
        }
    })

# Execute in chunks of max 50
for i in range(0, len(insert_requests), 50):
    batch_update(doc_id, token, insert_requests[i:i+50])
```

### Pass 2 — Style Application

After inserting text, re-read the doc and apply styles:

```python
doc = read_doc(doc_id, token)
body = doc['body']['content']

style_requests = []
item_idx = 0

for elem in body:
    if item_idx >= len(items):
        break
    if 'paragraph' not in elem:
        continue
    
    start = elem.get('startIndex', 0)
    end = elem.get('endIndex', 0)
    
    if start < insert_idx:
        continue
    
    text = ''
    for e in elem['paragraph'].get('elements', []):
        if 'textRun' in e:
            text += e['textRun'].get('content', '')
    text = text.strip()
    
    expected_text, expected_style = items[item_idx]
    
    if not text and expected_style == 'BLANK':
        item_idx += 1
        continue
    if not text:
        continue
    
    if expected_text and expected_text[:20] in text[:30]:
        if expected_style == 'H1':
            style_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {'namedStyleType': 'HEADING_1'},
                    'fields': 'namedStyleType'
                }
            })
        elif expected_style == 'H2':
            style_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {'namedStyleType': 'HEADING_2'},
                    'fields': 'namedStyleType'
                }
            })
        elif expected_style == 'NORMAL':
            style_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'namedStyleType': 'NORMAL_TEXT',
                        'lineSpacing': 115,
                        'spaceBelow': {'magnitude': 8, 'unit': 'PT'},
                    },
                    'fields': 'namedStyleType,lineSpacing,spaceBelow'
                }
            })
        elif expected_style == 'NUMBERED':
            style_requests.append({
                'createParagraphBullets': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'bulletPreset': 'NUMBERED_DECIMAL_NESTED'
                }
            })
            # Add spacing for list items
            style_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'lineSpacing': 115,
                        'spaceBelow': {'magnitude': 8, 'unit': 'PT'},
                        'spacingMode': 'NEVER_COLLAPSE',
                    },
                    'fields': 'lineSpacing,spaceBelow,spacingMode'
                }
            })
            # MANDATORY: re-assert font/size to match body text
            style_requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'weightedFontFamily': {'fontFamily': 'Rubik'},
                        'fontSize': {'magnitude': 11, 'unit': 'PT'},
                    },
                    'fields': 'weightedFontFamily,fontSize'
                }
            })
        elif expected_style == 'BULLET':
            style_requests.append({
                'createParagraphBullets': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
                }
            })
            # Add spacing for list items
            style_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'lineSpacing': 115,
                        'spaceBelow': {'magnitude': 8, 'unit': 'PT'},
                        'spacingMode': 'NEVER_COLLAPSE',
                    },
                    'fields': 'lineSpacing,spaceBelow,spacingMode'
                }
            })
            # MANDATORY: re-assert font/size to match body text
            style_requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'weightedFontFamily': {'fontFamily': 'Rubik'},
                        'fontSize': {'magnitude': 11, 'unit': 'PT'},
                    },
                    'fields': 'weightedFontFamily,fontSize'
                }
            })
        
        item_idx += 1
    else:
        item_idx += 1

# Execute in chunks
for i in range(0, len(style_requests), 50):
    batch_update(doc_id, token, style_requests[i:i+50])
```

### Pass 3 — Table Insertion (when needed)

For each table placeholder (process in **reverse** order):

1. Find the `__TBL1__` placeholder text in the doc
2. Delete the placeholder paragraph
3. `insertTable` at the same index
4. **Re-read doc** to get cell indices
5. `insertText` into each cell (reverse order)
6. Style the table

---

## Table Styling Standard

> **MANDATORY for ALL tables, no exceptions:**
> - **Font:** Arial 10pt for both header and body cells (set `weightedFontFamily.fontFamily: "Arial"` and `fontSize: 10pt`).
> - **Header row:** navy blue background (`rgb 0.11, 0.09, 0.25`), text in **bold** and **white** (`rgb 1.0, 1.0, 1.0`).
> - **Body rows:** default text color, 115% line spacing, 2pt above/below.
> - **First row pinned** as repeating header on multi-page tables (`pinTableHeaderRows`).

```python
# Header row - navy blue bg, white bold text
header_bg = {
    'updateTableCellStyle': {
        'tableCellStyle': {
            'backgroundColor': {
                'color': {'rgbColor': {'red': 0.11, 'green': 0.09, 'blue': 0.25}}
            }
        },
        'tableRange': {
            'tableCellLocation': {
                'tableStartLocation': {'index': table_start_idx},
                'rowIndex': 0, 'columnIndex': 0
            },
            'rowSpan': 1,
            'columnSpan': num_columns
        },
        'fields': 'backgroundColor'
    }
}

# Header text - Arial 10, white, bold (MANDATORY for ALL tables)
header_text = {
    'updateTextStyle': {
        'range': {'startIndex': header_start, 'endIndex': header_end},
        'textStyle': {
            'bold': True,
            'weightedFontFamily': {'fontFamily': 'Arial'},
            'fontSize': {'magnitude': 10, 'unit': 'PT'},
            'foregroundColor': {
                'color': {'rgbColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0}}
            }
        },
        'fields': 'bold,weightedFontFamily,fontSize,foregroundColor'
    }
}

# Body rows - Arial 10, compact spacing (MANDATORY for ALL tables)
body_text_style = {
    'updateTextStyle': {
        'range': {'startIndex': body_start, 'endIndex': body_end},
        'textStyle': {
            'weightedFontFamily': {'fontFamily': 'Arial'},
            'fontSize': {'magnitude': 10, 'unit': 'PT'},
        },
        'fields': 'weightedFontFamily,fontSize'
    }
}
body_style = {
    'updateParagraphStyle': {
        'range': {'startIndex': body_start, 'endIndex': body_end},
        'paragraphStyle': {
            'lineSpacing': 115,
            'spaceAbove': {'magnitude': 2, 'unit': 'PT'},
            'spaceBelow': {'magnitude': 2, 'unit': 'PT'},
        },
        'fields': 'lineSpacing,spaceAbove,spaceBelow'
    }
}

# Pin header row for multi-page tables
pin_header = {
    'pinTableHeaderRows': {
        'tableStartLocation': {'index': table_start_idx},
        'pinnedHeaderRowsCount': 1
    }
}
```

---

## List Spacing (CRITICAL)

Google Docs has a quirk: `spacingMode` defaults to `COLLAPSE_LISTS`, which **ignores** `spaceBelow`/`spaceAbove` between consecutive list items.

**Always set all three properties on list items:**

```python
{
    'updateParagraphStyle': {
        'range': {'startIndex': start, 'endIndex': end},
        'paragraphStyle': {
            'lineSpacing': 115,
            'spaceBelow': {'magnitude': 8, 'unit': 'PT'},
            'spacingMode': 'NEVER_COLLAPSE',
        },
        'fields': 'lineSpacing,spaceBelow,spacingMode'
    }
}
```

Without `spacingMode: NEVER_COLLAPSE`, bullet and numbered items will be crammed together.

## List Font Consistency (CRITICAL)

> **MANDATORY**: bullet and numbered list items must use the **same font family and size as body text** (the `NORMAL_TEXT` named style of the document — typically Arial 11pt for the Globalbit template). Lists that inherit a different font/size from the bullet preset look visually broken next to surrounding paragraphs.

After applying `createParagraphBullets`, the preset can override the run's font. Always re-assert the text style explicitly on the list item's range:

```python
# Apply this to EVERY bullet and numbered list item, after createParagraphBullets
# Globalbit template uses Rubik 11pt for body text - lists must match
{
    'updateTextStyle': {
        'range': {'startIndex': start, 'endIndex': end},
        'textStyle': {
            'weightedFontFamily': {'fontFamily': 'Rubik'},
            'fontSize': {'magnitude': 11, 'unit': 'PT'},
        },
        'fields': 'weightedFontFamily,fontSize'
    }
}
```

**Best practice: probe `NORMAL_TEXT` at runtime** rather than hard-coding the font. The template currently uses Rubik 11pt, but probing makes the script resilient to future template changes:

```python
def detect_body_font(doc):
    """Find the actual font/size used in NORMAL_TEXT paragraphs."""
    font, size = 'Rubik', 11  # fallback defaults
    for el in doc['body']['content']:
        if 'paragraph' not in el:
            continue
        if el['paragraph'].get('paragraphStyle', {}).get('namedStyleType') != 'NORMAL_TEXT':
            continue
        for e in el['paragraph'].get('elements', []):
            ts = e.get('textRun', {}).get('textStyle', {})
            if 'weightedFontFamily' in ts:
                font = ts['weightedFontFamily'].get('fontFamily', font)
            if 'fontSize' in ts:
                size = ts['fontSize'].get('magnitude', size)
        return font, size  # use the first NORMAL_TEXT we find
    return font, size
```

If the body text changes (e.g. another template uses 10pt), list items follow automatically.

---

## Text Alignment

- **All text**: left-aligned for English, right-aligned for Hebrew (RTL). NEVER center.
- **Images**: center alignment OK.
- **Headings**: follow the document direction (no center).

---

## Heading Spacing Standard

> **CRITICAL**: Do NOT insert empty paragraphs (`"\n"`-only items) before or after headings. The `spaceAbove` / `spaceBelow` values below already create the correct visual gap. Adding a blank line on top stacks two whitespace blocks and the heading floats too far from its content. When parsing markdown, skip blank lines that surround `#`/`##`/`###` lines.

```python
# HEADING_1 — large spacing above, smaller below
{'updateParagraphStyle': {
    'range': {'startIndex': start, 'endIndex': end},
    'paragraphStyle': {
        'namedStyleType': 'HEADING_1',
        'spaceAbove': {'magnitude': 14, 'unit': 'PT'},
        'spaceBelow': {'magnitude': 6, 'unit': 'PT'},
    },
    'fields': 'namedStyleType,spaceAbove,spaceBelow'
}}

# HEADING_2 — medium spacing
{'updateParagraphStyle': {
    'range': {'startIndex': start, 'endIndex': end},
    'paragraphStyle': {
        'namedStyleType': 'HEADING_2',
        'spaceAbove': {'magnitude': 12, 'unit': 'PT'},
        'spaceBelow': {'magnitude': 4, 'unit': 'PT'},
    },
    'fields': 'namedStyleType,spaceAbove,spaceBelow'
}}
```

---

## Batch Size Limit

Max **~50 requests** per `batchUpdate` call. Chunk larger lists:

```python
for i in range(0, len(requests), 50):
    batch_update(doc_id, token, requests[i:i+50])
```

---

## Debugging Tips

### Print Doc Structure

Use this to diagnose document issues:

```python
doc = read_doc(doc_id, token)
body = doc['body']['content']
print(f"Total elements: {len(body)}")

for i, elem in enumerate(body[:20]):
    start = elem.get('startIndex', 0)
    end = elem.get('endIndex', 0)
    
    if 'sectionBreak' in elem:
        stype = elem['sectionBreak'].get('sectionStyle', {}).get('sectionType', '')
        print(f"  [{i}] SECTION_BREAK({stype}) @ {start}-{end}")
    elif 'paragraph' in elem:
        style = elem['paragraph'].get('paragraphStyle', {}).get('namedStyleType', '?')
        text = ''
        for e in elem['paragraph'].get('elements', []):
            if 'textRun' in e:
                text += e['textRun'].get('content', '')
        text = text.strip()[:60]
        print(f"  [{i}] PARA({style}) @ {start}-{end}: '{text}'")
    elif 'table' in elem:
        rows = elem['table'].get('rows', 0)
        cols = elem['table'].get('columns', 0)
        print(f"  [{i}] TABLE({rows}x{cols}) @ {start}-{end}")
```

### Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| No header/footer on pages | Content inserted in Section 1 | Insert before NEXT_PAGE break |
| List items crammed together | Missing `spacingMode` | Add `NEVER_COLLAPSE` to list styling |
| SSL error on macOS | Python 3.11+ cert issue | Use `certifi` + `ssl.create_default_context` |
| `gws-auth.sh` hangs | Shell script waiting for input | Use Python OAuth2 refresh directly |
| Index out of range | Indices shifted after insert/delete | Re-read doc between operations |
| `deleteContentRange` fails | Range crosses table or section break | Delete each element individually, reverse order |
| Center-aligned text | Wrong alignment applied | Always use `START` alignment (never `CENTER` for text) |

---

## File Reference

| Resource | Path |
|----------|------|
| This skill | `.agents/skills/globalbit-document/SKILL.md` |
| Auth wrapper | `.agents/skills/globalbit-document/scripts/gws-auth.sh` |
| MCP docs | `.agents/docs/google-docs-mcp.md` |
| OAuth credentials | `~/.config/gws/credentials.json` |
| Client secret | `~/.config/gws/client_secret.json` |
| Cached token | `~/.config/gws/cached_token.json` |

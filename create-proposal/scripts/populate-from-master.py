#!/usr/bin/env python3
"""Populate a new Globalbit proposal from a master Google Docs template.

This is the PRIMARY proposal generation script. It works by:

1. Reading templates-google-docs.yaml to pick a master template by
   (service-type, language).
2. Duplicating the master template into the Proposals folder.
3. Replacing every placeholder in the template with project-specific content:
   - {{PROPOSAL_TITLE}}            -> the proposal title
   - {{SECTION_X}} (CUSTOM)        -> markdown content rendered to Docs styles
   - {{SECTION_X_APPEND}} (APPEND) -> markdown content rendered to Docs styles
                                      (same mechanism, but the placeholder lives
                                       at the END of a static section so the
                                       generated content appends rather than
                                       replacing the static base)
   - {{PROJECT_COST}}, etc.        -> single-value text replacement
4. Optionally adapting two canonical sentences in the static About section
   to match the prospect's industry.

The script NEVER touches static sections (About Globalbit with images, the
Agile methodology block, payment terms, the static portion of client
commitments / general terms, etc.). They are inherited byte-identical from
the master.

USAGE
=====

    python3 populate-from-master.py \\
        --service-type default \\
        --language he \\
        --client-name "המרכז הרפואי שניידר לילדים" \\
        --proposal-title "הצעה לפיתוח מערכת תומכת החלטה קלינית" \\
        --content-dir /path/to/sections/ \\
        --commercial-json /path/to/commercial.json \\
        --output-name "Schneider DSS - Proposal"

The --content-dir contains one markdown file per CUSTOM/APPEND placeholder:
    section-exec-summary.md
    section-background.md
    section-business-value.md
    section-project-goals.md
    section-solution.md
    section-scope.md
    section-project-phases.md
    section-team.md
    section-timeline-hours.md
    section-risks.md
    section-added-value.md
    assumptions-append.md
    client-commitments-append.md
    general-terms-append.md
    next-steps-append.md

The --commercial-json contains:
    {"project_cost": "230,000 ₪", "project_timeframe": "14 שבועות", ...}

DEPENDENCIES
============

    - Google OAuth credentials at ~/.config/gws/{cached_token,client_secret,credentials}.json
    - Python 3.11+ with stdlib + certifi
    - PyYAML (only for reading the manifest)
"""

import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import certifi
except ImportError:
    print("ERROR: certifi is required. Install with: pip3 install certifi")
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip3 install pyyaml")
    sys.exit(1)


# ============================================================================
# CONFIG
# ============================================================================

ctx = ssl.create_default_context(cafile=certifi.where())

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent  # create-proposal/
MANIFEST_PATH = SKILL_ROOT / "templates-google-docs.yaml"

PROPOSALS_FOLDER_ID = "14t2WcrT_bhRO6eu_YX8dcaY9ys5iXQbc"

# Map placeholder names (without braces) to source markdown filenames in --content-dir
PLACEHOLDER_TO_FILE = {
    # CUSTOM
    "SECTION_EXEC_SUMMARY": "section-exec-summary.md",
    "SECTION_BACKGROUND": "section-background.md",
    "SECTION_BUSINESS_VALUE": "section-business-value.md",
    "SECTION_PROJECT_GOALS": "section-project-goals.md",
    "SECTION_SOLUTION": "section-solution.md",
    "SECTION_SCOPE": "section-scope.md",
    "SECTION_PROJECT_PHASES": "section-project-phases.md",
    "SECTION_TEAM": "section-team.md",
    "SECTION_TIMELINE_HOURS": "section-timeline-hours.md",
    "SECTION_RISKS": "section-risks.md",
    "SECTION_ADDED_VALUE": "section-added-value.md",
    # APPEND
    "ASSUMPTIONS_APPEND": "assumptions-append.md",
    "CLIENT_COMMITMENTS_APPEND": "client-commitments-append.md",
    "GENERAL_TERMS_APPEND": "general-terms-append.md",
    "NEXT_STEPS_APPEND": "next-steps-append.md",
}

INLINE_FIELDS = ["PROJECT_COST", "PROJECT_TIMEFRAME", "ESTIMATED_HOURS"]


# ============================================================================
# AUTHENTICATION
# ============================================================================

def refresh_token() -> str:
    """Refresh the Google OAuth access token via the refresh-token grant."""
    cache = Path.home() / ".config/gws/cached_token.json"
    cs_path = Path.home() / ".config/gws/client_secret.json"
    cred_path = Path.home() / ".config/gws/credentials.json"

    with cache.open() as f:
        data = json.load(f)
    with cs_path.open() as f:
        client = json.load(f)["installed"]
    with cred_path.open() as f:
        refresh_tok = json.load(f)["tokens"]["refresh_token"]

    body = urllib.parse.urlencode({
        "client_id": client["client_id"],
        "client_secret": client["client_secret"],
        "refresh_token": refresh_tok,
        "grant_type": "refresh_token",
    }).encode()

    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=body, method="POST")
    with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
        result = json.loads(resp.read())

    data["access_token"] = result["access_token"]
    with cache.open("w") as f:
        json.dump(data, f)
    return result["access_token"]


def api(method: str, url: str, token: str, body=None, retries: int = 3):
    """Make an authenticated Google API request with light retry on 429."""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = json.dumps(body).encode() if body else None
    last_err = None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()[:1500]
            last_err = e
            if e.code == 429 and attempt < retries - 1:
                wait = 30 * (attempt + 1)
                print(f"  Rate limit hit, sleeping {wait}s (attempt {attempt+1}/{retries})")
                time.sleep(wait)
                continue
            print(f"API Error {e.code}: {err_body}")
            raise
    raise last_err  # type: ignore


def read_doc(doc_id: str, token: str):
    return api("GET", f"https://docs.googleapis.com/v1/documents/{doc_id}", token)


def batch_update(doc_id: str, token: str, requests):
    if not requests:
        return None
    return api("POST",
               f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate",
               token, {"requests": requests})


def throttled_batch(doc_id: str, token: str, requests, chunk_size: int = 18, sleep_between: float = 12.0):
    """Stay safely under Google's 60-writes-per-minute quota."""
    for i in range(0, len(requests), chunk_size):
        chunk = requests[i:i + chunk_size]
        batch_update(doc_id, token, chunk)
        if i + chunk_size < len(requests):
            time.sleep(sleep_between)


# ============================================================================
# MARKDOWN PARSING (lightweight)
# ============================================================================

def normalize_dashes(s: str) -> str:
    """Em/en-dashes are AI-tells in Hebrew; replace with hyphens."""
    return s.replace("—", "-").replace("–", "-").replace("•", "●")


def parse_markdown_to_items(md_text: str):
    """Parse markdown into a list of (text, style) tuples + tables.

    Returns:
        items: list of (text, style) where style is one of:
            H1, H2, H3, NORMAL, BULLET, NUMBERED, QUOTE, TABLE_PLACEHOLDER
        tables: list of [[row1], [row2], ...]
    """
    md_text = normalize_dashes(md_text)
    lines = md_text.split("\n")

    items = []
    tables = []
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        # Table detection
        if line.strip().startswith("|") and line.strip().endswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if i + 1 < len(lines) and re.match(r"^\s*\|[-:|\s]+\|\s*$", lines[i + 1]):
                table = [cells]
                i += 2
                while i < len(lines) and lines[i].strip().startswith("|"):
                    row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                    table.append(row)
                    i += 1
                tbl_idx = len(tables)
                tables.append(table)
                items.append((f"__TBL_{tbl_idx}__", "TABLE_PLACEHOLDER"))
                continue

        if line.startswith("### "):
            items.append((line[4:].strip(), "H3"))
        elif line.startswith("## "):
            items.append((line[3:].strip(), "H2"))
        elif line.startswith("# "):
            # Embedded H1s become H2 inside a section to avoid colliding with
            # the master template's existing H1 hierarchy.
            items.append((line[2:].strip(), "H2"))
        elif re.match(r"^---+\s*$", line):
            pass  # skip horizontal rules
        elif re.match(r"^\s*[●•]\s+", line):
            items.append((re.sub(r"^\s*[●•]\s+", "", line).strip(), "BULLET"))
        elif re.match(r"^\s*-\s+", line):
            items.append((re.sub(r"^\s*-\s+", "", line).strip(), "BULLET"))
        elif re.match(r"^\s*\d+\.\s+", line):
            items.append((re.sub(r"^\s*\d+\.\s+", "", line).strip(), "NUMBERED"))
        elif line.startswith("> "):
            items.append((line[2:].strip(), "QUOTE"))
        elif line.strip() == "":
            pass
        else:
            if line.strip():
                items.append((line.strip(), "NORMAL"))

        i += 1

    return items, tables


# ============================================================================
# DOC OPERATIONS
# ============================================================================

def find_placeholder_paragraph(doc, placeholder_marker: str):
    """Find a paragraph that contains exactly the placeholder text.

    Returns the paragraph element (with startIndex/endIndex), or None.
    """
    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        text = ""
        for ee in elem["paragraph"].get("elements", []):
            if "textRun" in ee:
                text += ee["textRun"].get("content", "")
        if placeholder_marker in text:
            return elem
    return None


def replace_placeholder_with_content(doc_id: str, token: str, placeholder_marker: str,
                                     items, tables) -> bool:
    """Replace a single placeholder paragraph with rendered markdown content.

    Returns True if the placeholder was found and replaced, False otherwise.
    """
    doc = read_doc(doc_id, token)
    target = find_placeholder_paragraph(doc, placeholder_marker)
    if not target:
        return False

    ts = target.get("startIndex", 0)
    te = target.get("endIndex", 0)

    # Delete the placeholder paragraph's text but keep one trailing newline
    # (the paragraph itself stays, its content gets cleared then we insert into it)
    text_len = te - ts - 1  # exclude trailing newline that terminates the paragraph
    if text_len > 0:
        batch_update(doc_id, token, [{
            "deleteContentRange": {"range": {"startIndex": ts, "endIndex": ts + text_len}}
        }])

    # The paragraph at ts is now empty. Insert all items at ts (in reverse order
    # so the indices don't shift between insertions).
    insert_requests = []
    for text, style in reversed(items):
        insert_requests.append({
            "insertText": {
                "location": {"index": ts},
                "text": (text or "") + "\n",
            }
        })
    throttled_batch(doc_id, token, insert_requests)

    # We over-inserted one trailing newline relative to the original paragraph.
    # That's fine - it just means the section now has its own paragraphs ending
    # in newlines, which is the natural Docs structure.

    # Apply paragraph styles
    apply_paragraph_styles(doc_id, token, ts, items)

    # Insert tables (replace __TBL_N__ placeholders) in reverse order
    for tbl_idx in reversed(range(len(tables))):
        insert_table_at_placeholder(doc_id, token, f"__TBL_{tbl_idx}__", tables[tbl_idx])

    # Apply bold for **markers** patterns
    apply_bold_markers(doc_id, token, after_index=ts)

    return True


def apply_paragraph_styles(doc_id: str, token: str, after_index: int, items):
    """Walk paragraphs after `after_index` and apply styles based on the items list."""
    doc = read_doc(doc_id, token)
    style_requests = []
    item_idx = 0

    for elem in doc["body"]["content"]:
        if item_idx >= len(items):
            break
        if "paragraph" not in elem:
            continue
        s = elem.get("startIndex", 0)
        e = elem.get("endIndex", 0)
        if s < after_index:
            continue

        text = ""
        for ee in elem["paragraph"].get("elements", []):
            if "textRun" in ee:
                text += ee["textRun"].get("content", "")
        text_stripped = text.strip()

        expected_text, expected_style = items[item_idx]
        if not text_stripped:
            continue
        # Loose matching - inserted text might have minor differences
        if not (expected_text and (expected_text[:25] in text or text_stripped[:25] in expected_text)):
            item_idx += 1
            continue

        style_requests.extend(_style_requests_for(s, e, expected_style))
        item_idx += 1

    throttled_batch(doc_id, token, style_requests)


def _style_requests_for(start: int, end: int, style: str):
    """Return the Docs API requests needed to apply a single paragraph style."""
    if style == "H1":
        return [{
            "updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": {
                    "namedStyleType": "HEADING_1",
                    "spaceAbove": {"magnitude": 14, "unit": "PT"},
                    "spaceBelow": {"magnitude": 6, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow",
            }
        }]
    if style == "H2":
        return [{
            "updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": {
                    "namedStyleType": "HEADING_2",
                    "spaceAbove": {"magnitude": 12, "unit": "PT"},
                    "spaceBelow": {"magnitude": 4, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow",
            }
        }]
    if style == "H3":
        return [{
            "updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": {
                    "namedStyleType": "HEADING_3",
                    "spaceAbove": {"magnitude": 10, "unit": "PT"},
                    "spaceBelow": {"magnitude": 3, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow",
            }
        }]
    if style == "NORMAL":
        return [{
            "updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "lineSpacing": 115,
                    "spaceBelow": {"magnitude": 8, "unit": "PT"},
                },
                "fields": "namedStyleType,lineSpacing,spaceBelow",
            }
        }]
    if style in ("BULLET", "NUMBERED"):
        bullet_preset = "BULLET_DISC_CIRCLE_SQUARE" if style == "BULLET" else "NUMBERED_DECIMAL_NESTED"
        return [
            {"createParagraphBullets": {
                "range": {"startIndex": start, "endIndex": end},
                "bulletPreset": bullet_preset,
            }},
            {"updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": {
                    "lineSpacing": 115,
                    "spaceBelow": {"magnitude": 8, "unit": "PT"},
                    "spacingMode": "NEVER_COLLAPSE",
                },
                "fields": "lineSpacing,spaceBelow,spacingMode",
            }},
            {"updateTextStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "textStyle": {
                    "weightedFontFamily": {"fontFamily": "Rubik"},
                    "fontSize": {"magnitude": 11, "unit": "PT"},
                },
                "fields": "weightedFontFamily,fontSize",
            }},
        ]
    if style == "QUOTE":
        return [
            {"updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "indentStart": {"magnitude": 18, "unit": "PT"},
                    "indentEnd": {"magnitude": 18, "unit": "PT"},
                    "spaceBelow": {"magnitude": 8, "unit": "PT"},
                },
                "fields": "namedStyleType,indentStart,indentEnd,spaceBelow",
            }},
            {"updateTextStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "textStyle": {
                    "italic": True,
                    "foregroundColor": {"color": {"rgbColor": {"red": 0.4, "green": 0.4, "blue": 0.4}}},
                },
                "fields": "italic,foregroundColor",
            }},
        ]
    return []


def insert_table_at_placeholder(doc_id: str, token: str, placeholder: str, table):
    """Replace a __TBL_N__ placeholder paragraph with a styled table.

    Header row gets navy bg + white bold; body rows get Arial 10pt + compact spacing.
    """
    doc = read_doc(doc_id, token)
    target = find_placeholder_paragraph(doc, placeholder)
    if not target:
        return

    ts = target.get("startIndex", 0)
    te = target.get("endIndex", 0)
    text_len = te - ts - 1
    if text_len > 0:
        batch_update(doc_id, token, [{
            "deleteContentRange": {"range": {"startIndex": ts, "endIndex": ts + text_len}}
        }])

    rows = len(table)
    cols = len(table[0])
    batch_update(doc_id, token, [{
        "insertTable": {"rows": rows, "columns": cols, "location": {"index": ts}}
    }])

    # Find inserted table, fill cells, style
    doc = read_doc(doc_id, token)
    target_table = None
    for elem in doc["body"]["content"]:
        if "table" in elem and elem.get("startIndex", 0) >= ts - 5:
            target_table = elem
            break
    if not target_table:
        return

    table_start = target_table.get("startIndex", 0)
    cell_inserts = []
    for r_idx, row_elem in enumerate(target_table["table"]["tableRows"]):
        for c_idx, cell_elem in enumerate(row_elem["tableCells"]):
            cell_paras = cell_elem.get("content", [])
            if cell_paras:
                cell_start = cell_paras[0].get("startIndex", 0)
                cell_text = re.sub(r"\*\*([^*]+)\*\*", r"\1", table[r_idx][c_idx])
                cell_inserts.append((cell_start, cell_text))

    cell_inserts.sort(key=lambda x: x[0], reverse=True)
    cell_text_requests = [
        {"insertText": {"location": {"index": cs}, "text": ct}}
        for cs, ct in cell_inserts if ct
    ]
    throttled_batch(doc_id, token, cell_text_requests)

    # Style header row
    doc = read_doc(doc_id, token)
    target_table = None
    for elem in doc["body"]["content"]:
        if "table" in elem and elem.get("startIndex", 0) >= ts - 5:
            target_table = elem
            break
    if not target_table:
        return

    style_reqs = [{
        "updateTableCellStyle": {
            "tableCellStyle": {
                "backgroundColor": {"color": {"rgbColor": {"red": 0.11, "green": 0.09, "blue": 0.25}}}
            },
            "tableRange": {
                "tableCellLocation": {
                    "tableStartLocation": {"index": table_start},
                    "rowIndex": 0, "columnIndex": 0,
                },
                "rowSpan": 1, "columnSpan": cols,
            },
            "fields": "backgroundColor",
        }
    }]

    header_row = target_table["table"]["tableRows"][0]
    for cell_elem in header_row["tableCells"]:
        for cp in cell_elem.get("content", []):
            if "paragraph" not in cp:
                continue
            cs = cp.get("startIndex", 0)
            ce = cp.get("endIndex", 0)
            if ce - cs > 1:
                style_reqs.append({
                    "updateTextStyle": {
                        "range": {"startIndex": cs, "endIndex": ce - 1},
                        "textStyle": {
                            "bold": True,
                            "weightedFontFamily": {"fontFamily": "Arial"},
                            "fontSize": {"magnitude": 10, "unit": "PT"},
                            "foregroundColor": {"color": {"rgbColor": {"red": 1.0, "green": 1.0, "blue": 1.0}}},
                        },
                        "fields": "bold,weightedFontFamily,fontSize,foregroundColor",
                    }
                })

    for r_idx in range(1, len(target_table["table"]["tableRows"])):
        for cell_elem in target_table["table"]["tableRows"][r_idx]["tableCells"]:
            for cp in cell_elem.get("content", []):
                if "paragraph" not in cp:
                    continue
                cs = cp.get("startIndex", 0)
                ce = cp.get("endIndex", 0)
                if ce - cs > 1:
                    style_reqs.append({
                        "updateTextStyle": {
                            "range": {"startIndex": cs, "endIndex": ce - 1},
                            "textStyle": {
                                "weightedFontFamily": {"fontFamily": "Arial"},
                                "fontSize": {"magnitude": 10, "unit": "PT"},
                            },
                            "fields": "weightedFontFamily,fontSize",
                        }
                    })
                    style_reqs.append({
                        "updateParagraphStyle": {
                            "range": {"startIndex": cs, "endIndex": ce - 1},
                            "paragraphStyle": {
                                "lineSpacing": 115,
                                "spaceAbove": {"magnitude": 2, "unit": "PT"},
                                "spaceBelow": {"magnitude": 2, "unit": "PT"},
                            },
                            "fields": "lineSpacing,spaceAbove,spaceBelow",
                        }
                    })

    style_reqs.append({
        "pinTableHeaderRows": {
            "tableStartLocation": {"index": table_start},
            "pinnedHeaderRowsCount": 1,
        }
    })

    throttled_batch(doc_id, token, style_reqs)


def apply_bold_markers(doc_id: str, token: str, after_index: int = 0):
    """Find **text** patterns, bold the inner text, then strip the asterisks."""
    doc = read_doc(doc_id, token)
    bold_requests = []

    def walk(content):
        for elem in content:
            if "paragraph" in elem:
                s = elem.get("startIndex", 0)
                if s < after_index:
                    continue
                text = ""
                for ee in elem["paragraph"].get("elements", []):
                    if "textRun" in ee:
                        text += ee["textRun"].get("content", "")
                for m in re.finditer(r"\*\*([^*]+)\*\*", text):
                    inner_start = s + m.start() + 2
                    inner_end = s + m.end() - 2
                    if inner_end > inner_start:
                        bold_requests.append({
                            "updateTextStyle": {
                                "range": {"startIndex": inner_start, "endIndex": inner_end},
                                "textStyle": {"bold": True},
                                "fields": "bold",
                            }
                        })
            elif "table" in elem:
                for row in elem["table"]["tableRows"]:
                    for cell in row["tableCells"]:
                        walk(cell.get("content", []))

    walk(doc["body"]["content"])
    throttled_batch(doc_id, token, bold_requests)

    # Strip the ** markers
    doc = read_doc(doc_id, token)
    strip_ranges = []

    def collect_strips(content):
        for elem in content:
            if "paragraph" in elem:
                s = elem.get("startIndex", 0)
                if s < after_index:
                    continue
                text = ""
                for ee in elem["paragraph"].get("elements", []):
                    if "textRun" in ee:
                        text += ee["textRun"].get("content", "")
                for m in re.finditer(r"\*\*", text):
                    strip_ranges.append((s + m.start(), s + m.start() + 2))
            elif "table" in elem:
                for row in elem["table"]["tableRows"]:
                    for cell in row["tableCells"]:
                        collect_strips(cell.get("content", []))

    collect_strips(doc["body"]["content"])
    strip_ranges.sort(key=lambda x: x[0], reverse=True)
    strip_requests = [
        {"deleteContentRange": {"range": {"startIndex": a, "endIndex": b}}}
        for a, b in strip_ranges
    ]
    throttled_batch(doc_id, token, strip_requests)


# ============================================================================
# MAIN
# ============================================================================

def load_manifest():
    with MANIFEST_PATH.open() as f:
        return yaml.safe_load(f)


def get_template_doc_id(manifest, service_type: str, language: str) -> str:
    try:
        return manifest["templates"][service_type][language]["doc_id"]
    except KeyError:
        raise SystemExit(f"No template registered for service-type={service_type!r} language={language!r}")


def replace_title(doc_id: str, token: str, new_title: str):
    """Replace {{PROPOSAL_TITLE}} (or the literal Hebrew title text) in the cover."""
    batch_update(doc_id, token, [{
        "replaceAllText": {
            "containsText": {"text": "{{PROPOSAL_TITLE}}", "matchCase": True},
            "replaceText": new_title,
        }
    }])


def replace_inline_field(doc_id: str, token: str, placeholder_name: str, value: str):
    """Replace {{PLACEHOLDER_NAME}} with value via replaceAllText."""
    batch_update(doc_id, token, [{
        "replaceAllText": {
            "containsText": {"text": "{{" + placeholder_name + "}}", "matchCase": True},
            "replaceText": value,
        }
    }])


def replace_adaptable_sentence(doc_id: str, token: str, canonical: str, adapted: str):
    """Replace a canonical About-section sentence with an industry-adapted one."""
    if not adapted or canonical == adapted:
        return
    batch_update(doc_id, token, [{
        "replaceAllText": {
            "containsText": {"text": canonical, "matchCase": True},
            "replaceText": adapted,
        }
    }])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--service-type", default="default")
    p.add_argument("--language", default="he")
    p.add_argument("--client-name", required=True, help='e.g. "המרכז הרפואי שניידר לילדים"')
    p.add_argument("--proposal-title", required=True, help="Full title for the cover page")
    p.add_argument("--content-dir", required=True, help="Directory with section markdown files")
    p.add_argument("--commercial-json", required=True, help="JSON with project_cost, project_timeframe, estimated_hours")
    p.add_argument("--output-name", required=True, help='New doc name in Drive')
    p.add_argument("--industry", default=None, help="Industry key for adaptable sentences (healthcare, finance, etc.)")
    p.add_argument("--dry-run", action="store_true", help="Print plan without making API calls")
    args = p.parse_args()

    content_dir = Path(args.content_dir)
    if not content_dir.is_dir():
        raise SystemExit(f"--content-dir {content_dir} does not exist or is not a directory")

    with open(args.commercial_json) as f:
        commercial = json.load(f)
    for k in INLINE_FIELDS:
        key = k.lower()
        if key not in commercial:
            raise SystemExit(f"--commercial-json missing key {key!r}")

    manifest = load_manifest()
    template_id = get_template_doc_id(manifest, args.service_type, args.language)
    print(f"Using master template: {template_id}")

    if args.dry_run:
        print("(dry-run — would now duplicate template, replace placeholders, etc.)")
        return

    token = refresh_token()

    # 1. Duplicate
    print(f"Duplicating master into Proposals folder as {args.output_name!r}...")
    resp = api("POST",
               f"https://www.googleapis.com/drive/v3/files/{template_id}/copy?supportsAllDrives=true",
               token, {"name": args.output_name, "parents": [PROPOSALS_FOLDER_ID]})
    doc_id = resp["id"]
    print(f"Created: https://docs.google.com/document/d/{doc_id}/edit")

    # 2. Title
    print("Replacing title...")
    replace_title(doc_id, token, args.proposal_title)

    # 3. Inline commercial fields
    print("Replacing commercial fields...")
    for field in INLINE_FIELDS:
        replace_inline_field(doc_id, token, field, str(commercial[field.lower()]))

    # 4. Adaptable sentences (if industry specified)
    if args.industry:
        print(f"Adapting About sentences for industry={args.industry}...")
        adaptables = manifest.get("adaptable_sentences", {})
        for key, spec in adaptables.items():
            canonical = spec.get("canonical")
            adapted = (spec.get("adaptation_rules") or {}).get(args.industry)
            if canonical and adapted:
                replace_adaptable_sentence(doc_id, token, canonical, adapted)

    # 5. CUSTOM and APPEND placeholders -> markdown content
    for placeholder, filename in PLACEHOLDER_TO_FILE.items():
        path = content_dir / filename
        if not path.is_file():
            print(f"  SKIP {placeholder!r}: file not found ({filename})")
            continue
        print(f"Replacing {{{placeholder}}}...")
        md_text = path.read_text()
        items, tables = parse_markdown_to_items(md_text)
        if not items:
            print(f"  SKIP {placeholder!r}: parsed 0 items from {filename}")
            continue
        marker = "{{" + placeholder + "}}"
        ok = replace_placeholder_with_content(doc_id, token, marker, items, tables)
        if not ok:
            print(f"  WARNING: placeholder {marker} not found in doc")

    # 6. Final integrity check - fail loudly if any {{...}} placeholders remain
    print("\nVerifying no placeholders remain...")
    doc = read_doc(doc_id, token)
    leftover = []
    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        text = ""
        for ee in elem["paragraph"].get("elements", []):
            if "textRun" in ee:
                text += ee["textRun"].get("content", "")
        for m in re.finditer(r"\{\{([A-Z_]+)\}\}", text):
            leftover.append(m.group(0))
    if leftover:
        print(f"WARNING: {len(leftover)} unresolved placeholders: {set(leftover)}")
    else:
        print("OK - no placeholders left.")

    print(f"\nDone! https://docs.google.com/document/d/{doc_id}/edit")


if __name__ == "__main__":
    main()

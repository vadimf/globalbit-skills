#!/usr/bin/env python3
"""Duplicate the Globalbit master proposal template and inject placeholders."""

import json, os, ssl, certifi, time, re
import urllib.request, urllib.parse, urllib.error

ctx = ssl.create_default_context(cafile=certifi.where())

SOURCE_DOC_ID = "1_dZHdcikoq9OWNjli3GPxlNxGWWKPWPYGEzU57edFyI"
FOLDER_ID = "14t2WcrT_bhRO6eu_YX8dcaY9ys5iXQbc"  # Proposals folder
NEW_NAME = "Globalbit Proposal Template - Master (with placeholders)"


# Map of CUSTOM H1 sections (by Hebrew text) → placeholder.
# These get their content (between this H1 and the next H1) replaced with one placeholder paragraph.
# Note: "שלבי הפרויקט" appears TWICE. The first is methodology (STATIC). The SECOND is the project-specific plan (CUSTOM).
# We track by occurrence index.
CUSTOM_SECTIONS_FIRST_OCCURRENCE = {
    "תקציר מנהלים": "{{SECTION_EXEC_SUMMARY}}",
    "רקע והקשר": "{{SECTION_BACKGROUND}}",
    "ערך עסקי ותוצאות אסטרטגיות צפויות": "{{SECTION_BUSINESS_VALUE}}",
    "מטרות הפרויקט": "{{SECTION_PROJECT_GOALS}}",
    "הפתרון המוצע": "{{SECTION_SOLUTION}}",
    "היקף הפרויקט ותוצרים": "{{SECTION_SCOPE}}",
    "צוות הפרויקט": "{{SECTION_TEAM}}",
    "לוח זמנים והיקף שעות": "{{SECTION_TIMELINE_HOURS}}",
    "ניהול סיכונים": "{{SECTION_RISKS}}",
    "ערכים מוספים ויתרונות גלובלביט": "{{SECTION_ADDED_VALUE}}",
}

# שלבי הפרויקט by occurrence (1-indexed). Second occurrence is CUSTOM (project-specific plan).
PROJECT_PHASES_OCCURRENCE = 2
PROJECT_PHASES_PLACEHOLDER = "{{SECTION_PROJECT_PHASES}}"
PROJECT_PHASES_HEADING = "שלבי הפרויקט"

# STATIC sections that need inline field placeholders inside them.
# We do NOT replace their content - we inject specific placeholders surgically via replaceAllText.
INLINE_REPLACEMENTS = [
    # In תמורה section, the project cost/time/hours fields
    # We expect the doc has placeholder lines like "הערכת עלות הפרויקט:" but no values yet.
    # The replacements are done at runtime per-proposal; the master keeps the labels with placeholders.
    # We add explicit {{...}} markers next to the labels.
]

# About-Globalbit adaptable sentences - documented in manifest, not changed in master.
# They stay as canonical strings; runtime can replaceAllText them to client-adapted versions.
ABOUT_CANONICAL_SENTENCES = {
    "industry_framing": "גלובלביט הוא בית תוכנה ישראלי עטור פרסים, המתמחה בפיתוח מוצרי דיגיטל למשרדי ממשלה ותאגידים ישראליים ובינלאומיים.",
    "client_list": "לחברה ניסיון עשיר בתכנון, יישום ותחזוקת מערכות ארגוניות עבור מוסדות פיננסיים, שנצבר בעבודה עם ארגונים רבים כגון: הפניקס, כלל ביטוח, IBI, ישרכארט ועוד.",
}


# ---------- AUTH ----------

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
    req = urllib.request.Request('https://oauth2.googleapis.com/token', data=body, method='POST')
    with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
        result = json.loads(resp.read())
    data['access_token'] = result['access_token']
    with open(cache, 'w') as f: json.dump(data, f)
    return result['access_token']


def api(method, url, token, body=None):
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()[:1500]
        print(f"API Error {e.code}: {err}")
        raise


def read_doc(doc_id, token):
    return api('GET', f"https://docs.googleapis.com/v1/documents/{doc_id}", token)


def batch_update(doc_id, token, requests):
    if not requests:
        return None
    return api('POST',
        f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate",
        token, {'requests': requests})


def throttled_batch(doc_id, token, requests, chunk_size=20, sleep_between=8):
    for i in range(0, len(requests), chunk_size):
        batch_update(doc_id, token, requests[i:i+chunk_size])
        if i + chunk_size < len(requests):
            time.sleep(sleep_between)


# ---------- ANALYZE ----------

def find_h1_segments(body):
    """Return list of (heading_text, heading_start, heading_end, content_start, content_end, occurrence) for each H1."""
    h1s = []
    name_count = {}
    for i, elem in enumerate(body):
        if 'paragraph' not in elem:
            continue
        style = elem['paragraph'].get('paragraphStyle', {}).get('namedStyleType', '')
        if style != 'HEADING_1':
            continue
        text = ''
        for ee in elem['paragraph'].get('elements', []):
            if 'textRun' in ee:
                text += ee['textRun'].get('content', '')
        text = text.strip()
        if not text:
            continue
        occ = name_count.get(text, 0) + 1
        name_count[text] = occ
        h1s.append({
            'name': text,
            'heading_start': elem.get('startIndex', 0),
            'heading_end': elem.get('endIndex', 0),
            'occurrence': occ,
            'index_in_body': i,
        })

    # Compute content_start/end for each (between this H1's end and next H1's start)
    for idx, h in enumerate(h1s):
        h['content_start'] = h['heading_end']
        if idx + 1 < len(h1s):
            h['content_end'] = h1s[idx + 1]['heading_start']
        else:
            # Last H1 - content goes until end of body or NEXT_PAGE break
            h['content_end'] = None
            for elem in body:
                if 'sectionBreak' in elem and elem.get('startIndex', 0) > h['heading_end']:
                    stype = elem['sectionBreak'].get('sectionStyle', {}).get('sectionType', '')
                    if stype == 'NEXT_PAGE':
                        h['content_end'] = elem.get('startIndex', 0)
                        break
            if h['content_end'] is None:
                # Use last paragraph endIndex
                h['content_end'] = body[-1].get('endIndex', body[-1].get('startIndex', 0) + 1)

    return h1s


# ---------- MAIN ----------

def main():
    print("Auth...")
    token = refresh_token()

    # Step 1: Duplicate
    print(f"Duplicating source doc {SOURCE_DOC_ID}...")
    resp = api('POST',
        f'https://www.googleapis.com/drive/v3/files/{SOURCE_DOC_ID}/copy?supportsAllDrives=true',
        token, {"name": NEW_NAME, "parents": [FOLDER_ID]})
    doc_id = resp['id']
    print(f"Created: {doc_id}")
    print(f"URL: https://docs.google.com/document/d/{doc_id}/edit")

    # Step 2: Read structure
    doc = read_doc(doc_id, token)
    h1s = find_h1_segments(doc['body']['content'])

    print(f"\nFound {len(h1s)} H1 sections:")
    for h in h1s:
        print(f"  {h['name']!r} (occ {h['occurrence']}) "
              f"heading@{h['heading_start']}-{h['heading_end']} "
              f"content@{h['content_start']}-{h['content_end']}")

    # Step 3: Determine which sections need their content replaced with a placeholder
    # Process in REVERSE order (highest content_start first) so indices don't shift.
    print(f"\nPlanning content replacements...")
    replacements = []  # (content_start, content_end, placeholder_text)

    for h in h1s:
        target_placeholder = None

        # Check first-occurrence custom sections
        if h['name'] in CUSTOM_SECTIONS_FIRST_OCCURRENCE and h['occurrence'] == 1:
            target_placeholder = CUSTOM_SECTIONS_FIRST_OCCURRENCE[h['name']]

        # Check duplicated section (שלבי הפרויקט second occurrence)
        elif h['name'] == PROJECT_PHASES_HEADING and h['occurrence'] == PROJECT_PHASES_OCCURRENCE:
            target_placeholder = PROJECT_PHASES_PLACEHOLDER

        if target_placeholder:
            replacements.append({
                'name': h['name'],
                'occurrence': h['occurrence'],
                'content_start': h['content_start'],
                'content_end': h['content_end'],
                'placeholder': target_placeholder,
            })

    print(f"\nWill replace content of {len(replacements)} sections:")
    for r in replacements:
        print(f"  {r['name']} (occ {r['occurrence']}) → {r['placeholder']}")

    # Step 4: Apply replacements in reverse order (so indices don't shift)
    # For each section we want to replace:
    #   1. Delete any existing content (between heading and next heading)
    #   2. Insert a single placeholder paragraph right after the heading
    replacements.sort(key=lambda r: r['content_start'], reverse=True)

    for r in replacements:
        cs = r['content_start']
        ce = r['content_end']

        # Re-read doc each time so indices are fresh
        doc = read_doc(doc_id, token)
        body = doc['body']['content']

        # Find elements that fall WHOLLY within (cs, ce) range
        elements_in_range = []
        for elem in body:
            es = elem.get('startIndex', -1)
            ee = elem.get('endIndex', -1)
            if es >= cs and ee <= ce and 'sectionBreak' not in elem:
                elements_in_range.append((es, ee, 'table' in elem))

        # Delete in reverse (highest first)
        elements_in_range.sort(key=lambda x: x[0], reverse=True)
        if elements_in_range:
            print(f"  {r['name']}: deleting {len(elements_in_range)} elements in {cs}-{ce}")
            for es, ee, is_table in elements_in_range:
                try:
                    batch_update(doc_id, token, [{
                        'deleteContentRange': {'range': {'startIndex': es, 'endIndex': ee}}
                    }])
                    time.sleep(0.5)
                except Exception as ex:
                    print(f"    delete failed for {es}-{ee}: {ex}")
        else:
            print(f"  {r['name']}: empty section, only inserting placeholder")

        # Re-read to find the H1 fresh and insert placeholder right after it
        doc = read_doc(doc_id, token)
        body = doc['body']['content']

        target_h1 = None
        seen_count = 0
        for elem in body:
            if 'paragraph' not in elem:
                continue
            if elem['paragraph'].get('paragraphStyle', {}).get('namedStyleType', '') != 'HEADING_1':
                continue
            text = ''
            for ee in elem['paragraph'].get('elements', []):
                if 'textRun' in ee:
                    text += ee['textRun'].get('content', '')
            text = text.strip()
            if text == r['name']:
                seen_count += 1
                if seen_count == r['occurrence']:
                    target_h1 = elem
                    break

        if not target_h1:
            print(f"    can't relocate heading {r['name']!r} - skipping insert")
            continue

        insert_at = target_h1.get('endIndex', 0)
        placeholder_text = r['placeholder'] + '\n'

        batch_update(doc_id, token, [{
            'insertText': {'location': {'index': insert_at}, 'text': placeholder_text}
        }])

        batch_update(doc_id, token, [{
            'updateParagraphStyle': {
                'range': {'startIndex': insert_at, 'endIndex': insert_at + len(placeholder_text)},
                'paragraphStyle': {'namedStyleType': 'NORMAL_TEXT'},
                'fields': 'namedStyleType'
            }
        }])

        time.sleep(1.5)

    # Step 5: Inject placeholders into תמורה section (cost, timeframe, hours)
    print("\nInjecting commercial placeholders in תמורה...")
    # We'll add 3 lines RIGHT after the תמורה H1 with formatted placeholders.
    doc = read_doc(doc_id, token)
    body = doc['body']['content']

    temura_h1 = None
    for elem in body:
        if 'paragraph' not in elem:
            continue
        if elem['paragraph'].get('paragraphStyle', {}).get('namedStyleType', '') != 'HEADING_1':
            continue
        text = ''
        for ee in elem['paragraph'].get('elements', []):
            if 'textRun' in ee:
                text += ee['textRun'].get('content', '')
        if text.strip() == "תמורה":
            temura_h1 = elem
            break

    if temura_h1:
        insert_at = temura_h1.get('endIndex', 0)
        # Insert 3 labelled paragraphs with placeholders
        commercial_lines = (
            "הערכת עלות הפרויקט: {{PROJECT_COST}}\n"
            "זמן השלמת הפרויקט: {{PROJECT_TIMEFRAME}}\n"
            "הערכת היקף שעות: {{ESTIMATED_HOURS}}\n"
        )
        batch_update(doc_id, token, [{
            'insertText': {'location': {'index': insert_at}, 'text': commercial_lines}
        }])
        # Style as NORMAL_TEXT bold labels
        batch_update(doc_id, token, [{
            'updateParagraphStyle': {
                'range': {'startIndex': insert_at, 'endIndex': insert_at + len(commercial_lines)},
                'paragraphStyle': {'namedStyleType': 'NORMAL_TEXT'},
                'fields': 'namedStyleType'
            }
        }])
        print(f"  Injected commercial fields at {insert_at}")
    else:
        print("  WARNING: תמורה heading not found")

    # Step 6: Replace title text with placeholder
    print("\nReplacing title with placeholder...")
    batch_update(doc_id, token, [{
        'replaceAllText': {
            'containsText': {'text': 'הצעה למתן שירותי פיתוח……..', 'matchCase': True},
            'replaceText': '{{PROPOSAL_TITLE}}'
        }
    }])

    print(f"\nDone!")
    print(f"Master template URL: https://docs.google.com/document/d/{doc_id}/edit")
    print(f"\nDoc ID for manifest: {doc_id}")


if __name__ == '__main__':
    main()

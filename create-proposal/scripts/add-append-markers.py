#!/usr/bin/env python3
"""Add {{APPEND}} placeholders at the end of static-with-append sections."""

import json, os, ssl, certifi, time
import urllib.request, urllib.error

ctx = ssl.create_default_context(cafile=certifi.where())
DOC_ID = "1CRStai4W3U_ZW0Cc4Tvs0EcVQc19wPezRbuwTomQMOM"

# Mapping: section heading text -> append placeholder
APPEND_SECTIONS = {
    "הנחות יסוד": "{{ASSUMPTIONS_APPEND}}",
    "מחויבות הלקוח": "{{CLIENT_COMMITMENTS_APPEND}}",
    "תנאים כלליים": "{{GENERAL_TERMS_APPEND}}",
    "שלבים הבאים": "{{NEXT_STEPS_APPEND}}",
}


def refresh_token():
    cache = os.path.expanduser('~/.config/gws/cached_token.json')
    cs = os.path.expanduser('~/.config/gws/client_secret.json')
    cred = os.path.expanduser('~/.config/gws/credentials.json')
    with open(cache) as f: data = json.load(f)
    with open(cs) as f: client = json.load(f)['installed']
    with open(cred) as f: refresh_tok = json.load(f)['tokens']['refresh_token']
    import urllib.parse
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
    with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
        return json.loads(resp.read())


def main():
    token = refresh_token()
    doc = api('GET', f"https://docs.googleapis.com/v1/documents/{DOC_ID}", token)
    body = doc['body']['content']

    # Find each section's end position (start of next H1, or end of body)
    h1_positions = []
    for i, elem in enumerate(body):
        if 'paragraph' not in elem:
            continue
        if elem['paragraph'].get('paragraphStyle', {}).get('namedStyleType', '') != 'HEADING_1':
            continue
        text = ''
        for ee in elem['paragraph'].get('elements', []):
            if 'textRun' in ee:
                text += ee['textRun'].get('content', '')
        text = text.strip()
        if text:
            h1_positions.append({
                'name': text,
                'heading_start': elem.get('startIndex', 0),
                'heading_end': elem.get('endIndex', 0),
                'index_in_body': i,
            })

    # For each H1 in APPEND_SECTIONS, find its content_end (= next H1 start, or NEXT_PAGE break)
    # Then determine WHERE to inject: right before content_end (so it's the last paragraph of the section)
    # If content is empty (heading_end == content_end), inject right after heading
    for h_idx, h in enumerate(h1_positions):
        if h['name'] not in APPEND_SECTIONS:
            continue
        placeholder = APPEND_SECTIONS[h['name']]

        # Compute content_end
        if h_idx + 1 < len(h1_positions):
            content_end = h1_positions[h_idx + 1]['heading_start']
        else:
            # Last H1 - find NEXT_PAGE break
            content_end = None
            for elem in body:
                if 'sectionBreak' in elem and elem.get('startIndex', 0) > h['heading_end']:
                    if elem['sectionBreak'].get('sectionStyle', {}).get('sectionType', '') == 'NEXT_PAGE':
                        content_end = elem.get('startIndex', 0)
                        break
            if content_end is None:
                content_end = body[-1].get('endIndex', 0)

        # Where to insert: at content_end (the position of the next H1's start, or section break)
        # That's where we add a new paragraph BEFORE that boundary.
        # Use insertText at content_end — the placeholder paragraph becomes part of the current section.
        h['content_end'] = content_end
        h['placeholder'] = placeholder

    # Process in REVERSE order to preserve indices
    targets = [h for h in h1_positions if 'placeholder' in h]
    targets.sort(key=lambda x: x['content_end'], reverse=True)

    for t in targets:
        ce = t['content_end']
        placeholder_text = t['placeholder'] + '\n'
        print(f"  Inserting {t['placeholder']!r} at index {ce} (end of section {t['name']!r})")

        try:
            api('POST', f"https://docs.googleapis.com/v1/documents/{DOC_ID}:batchUpdate", token, {
                'requests': [
                    {'insertText': {'location': {'index': ce}, 'text': placeholder_text}},
                    {'updateParagraphStyle': {
                        'range': {'startIndex': ce, 'endIndex': ce + len(placeholder_text)},
                        'paragraphStyle': {'namedStyleType': 'NORMAL_TEXT'},
                        'fields': 'namedStyleType'
                    }}
                ]
            })
        except urllib.error.HTTPError as e:
            print(f"    Error: {e.read().decode()[:200]}")
        time.sleep(1.5)

    print("\nDone!")
    print(f"https://docs.google.com/document/d/{DOC_ID}/edit")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Deep comparison: extract all paragraphs from English and check presence in Chinese."""

import urllib.request
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_meaningful_paragraphs_adoc(text):
    """Extract meaningful paragraphs from AsciiDoc, skipping metadata/headers/tables."""
    paragraphs = []
    lines = text.split('\n')
    current_para = []
    in_table = False
    in_code = False
    skip_next = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Track table state
        if '|===' in stripped:
            in_table = not in_table
            continue

        # Track code block state
        if stripped == '----':
            in_code = not in_code
            if not in_code and current_para:
                # Save code block as a paragraph
                paragraphs.append(('code', '\n'.join(current_para)))
                current_para = []
            continue

        if in_table or in_code:
            if in_code:
                current_para.append(stripped)
            continue

        # Skip empty lines - flush current paragraph
        if not stripped:
            if current_para:
                paragraphs.append(('text', '\n'.join(current_para)))
                current_para = []
            continue

        # Skip metadata, headings, includes
        if stripped.startswith('---') or stripped.startswith('include::'):
            continue
        if re.match(r'^={1,4}\s', stripped):
            if current_para:
                paragraphs.append(('text', '\n'.join(current_para)))
                current_para = []
            continue
        if stripped.startswith('[[') and stripped.endswith(']]'):
            continue

        # Skip table header rows
        if stripped.startswith('|Advisory') or stripped.startswith('|Errata') or stripped.startswith('|Date'):
            continue

        # Skip [.note], [.important], [.programlisting] markers
        if re.match(r'^\[\.(note|important|programlisting|contrib)\]', stripped):
            if current_para:
                paragraphs.append(('text', '\n'.join(current_para)))
                current_para = []
            continue

        # Skip *Note* and *Important* lines
        if stripped.startswith('*Note*') or stripped.startswith('*Important*'):
            continue

        # Collect the line
        current_para.append(stripped)

    if current_para:
        paragraphs.append(('text', '\n'.join(current_para)))

    return paragraphs

def check_paragraph_in_chinese(en_para, cn_text):
    """Check if an English paragraph has a corresponding Chinese translation."""
    # Extract key identifiers from the English paragraph
    # 1. Revision references
    revs = re.findall(r'r\d{5,6}', en_para)
    if revs:
        for rev in revs:
            if rev in cn_text:
                return True
        return False

    # 2. Man page references
    man_refs = re.findall(r'query=(\w[\w.-]*)&sektion=(\d)', en_para)
    if man_refs:
        for name, sect in man_refs:
            if f'{name}({sect})' in cn_text or f'{name}({sect})' in cn_text:
                return True

    # 3. Specific technical terms
    # Extract significant words (skip common words)
    significant_terms = []
    for term in re.findall(r'\b[A-Z][a-zA-Z]{3,}\b', en_para):
        if term not in ['This', 'That', 'These', 'Those', 'The', 'FreeBSD', 'Linux', 'Intel',
                        'OpenSSL', 'OpenSSH', 'Microsoft', 'Solaris', 'Apple', 'NetBSD',
                        'FreeBSDorg', 'January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December']:
            significant_terms.append(term)

    if significant_terms:
        found = 0
        for term in significant_terms:
            if term in cn_text:
                found += 1
        # If at least half the significant terms are found, consider it present
        if found >= len(significant_terms) * 0.5:
            return True

    return None  # Uncertain

# Compare 10.0
print("="*60)
print("Deep comparison: FreeBSD 10.0")
print("="*60)

en_text = fetch("https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/10.0R/relnotes.adoc")
cn_text = read_file(r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\10.0.md")

en_paras = extract_meaningful_paragraphs_adoc(en_text)
print(f"English paragraphs: {len(en_paras)}")

missing = []
uncertain = []

for ptype, para in en_paras:
    if ptype == 'code':
        continue  # Code blocks checked separately

    result = check_paragraph_in_chinese(para, cn_text)
    if result is False:
        # Extract a short description
        short = para[:150].replace('\n', ' ')
        missing.append(short)
    elif result is None:
        short = para[:150].replace('\n', ' ')
        uncertain.append(short)

print(f"\nMissing paragraphs ({len(missing)}):")
for m in missing:
    print(f"  - {m}...")

print(f"\nUncertain paragraphs ({len(uncertain)}):")
for u in uncertain:
    print(f"  ? {u}...")

# Now do the same for 10.1, 10.2, 10.3, 10.4
for version in ['10.1', '10.2', '10.3', '10.4']:
    print(f"\n{'='*60}")
    print(f"Deep comparison: FreeBSD {version}")
    print(f"{'='*60}")

    en_text = fetch(f"https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/{version}R/relnotes.adoc")
    cn_text = read_file(fr"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\{version}.md")

    en_paras = extract_meaningful_paragraphs_adoc(en_text)
    print(f"English paragraphs: {len(en_paras)}")

    missing = []
    uncertain = []

    for ptype, para in en_paras:
        if ptype == 'code':
            continue

        result = check_paragraph_in_chinese(para, cn_text)
        if result is False:
            short = para[:150].replace('\n', ' ')
            missing.append(short)
        elif result is None:
            short = para[:150].replace('\n', ' ')
            uncertain.append(short)

    print(f"\nMissing paragraphs ({len(missing)}):")
    for m in missing:
        print(f"  - {m}...")

    print(f"\nUncertain paragraphs ({len(uncertain)}):")
    for u in uncertain:
        print(f"  ? {u}...")

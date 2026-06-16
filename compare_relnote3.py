#!/usr/bin/env python3
"""
Final comprehensive comparison - check each English paragraph against Chinese
by extracting revision numbers and verifying they exist in the Chinese text.
Also check for missing note/important blocks, tables, and specific content.
"""

import re
import urllib.request
import ssl

EN_URLS = {
    "11.0": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/11.0R/relnotes.adoc",
    "11.1": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/11.1R/relnotes.adoc",
    "11.2": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/11.2R/relnotes.adoc",
    "11.3": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/11.3R/relnotes.adoc",
}

CN_FILES = {
    "11.0": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\11.0.md",
    "11.1": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\11.1.md",
    "11.2": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\11.2.md",
    "11.3": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\11.3.md",
}

def fetch_url(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx) as resp:
        return resp.read().decode('utf-8')

def extract_adoc_paragraphs(text):
    """Extract individual paragraphs from asciidoc, each with its revision numbers."""
    paragraphs = []
    current_para = []
    in_table = False
    table_lines = []

    for line in text.split('\n'):
        stripped = line.strip()

        # Skip front matter, includes, TOC, anchors
        if stripped == '---' or stripped.startswith('include::') or stripped.startswith('* <<') or (stripped.startswith('[[') and stripped.endswith(']]')):
            continue

        # Table handling
        if stripped == '|===':
            if in_table:
                in_table = False
                if table_lines:
                    table_text = '\n'.join(table_lines)
                    revs = re.findall(r'r(\d{5,7})', table_text)
                    paragraphs.append({
                        'type': 'table',
                        'text': table_text[:300],
                        'revs': revs,
                    })
                table_lines = []
            else:
                in_table = True
                table_lines = []
            continue

        if in_table:
            table_lines.append(stripped)
            continue

        # Note/Important blocks
        if stripped == '[.note]' or stripped == '[.important]':
            # Save current paragraph
            if current_para:
                text_content = ' '.join(current_para)
                revs = re.findall(r'r(\d{5,7})', text_content)
                if text_content.strip():
                    paragraphs.append({
                        'type': 'paragraph',
                        'text': text_content[:300],
                        'revs': revs,
                    })
                current_para = []
            # The note content will be on the next lines
            continue

        # Section headers
        if re.match(r'^={2,4}\s+', stripped):
            if current_para:
                text_content = ' '.join(current_para)
                revs = re.findall(r'r(\d{5,7})', text_content)
                if text_content.strip():
                    paragraphs.append({
                        'type': 'paragraph',
                        'text': text_content[:300],
                        'revs': revs,
                    })
                current_para = []
            continue

        # Empty line = paragraph break
        if not stripped:
            if current_para:
                text_content = ' '.join(current_para)
                revs = re.findall(r'r(\d{5,7})', text_content)
                if text_content.strip():
                    paragraphs.append({
                        'type': 'paragraph',
                        'text': text_content[:300],
                        'revs': revs,
                    })
                current_para = []
            continue

        # Content line
        if stripped and not stripped.startswith('[.'):
            current_para.append(stripped)

    # Flush
    if current_para:
        text_content = ' '.join(current_para)
        revs = re.findall(r'r(\d{5,7})', text_content)
        if text_content.strip():
            paragraphs.append({
                'type': 'paragraph',
                'text': text_content[:300],
                'revs': revs,
            })

    return paragraphs

def extract_md_paragraphs(text):
    """Extract individual paragraphs from markdown, each with its revision numbers."""
    paragraphs = []
    current_para = []
    in_table = False
    table_lines = []

    for line in text.split('\n'):
        stripped = line.strip()

        # Skip title and meta lines
        if stripped.startswith('# ') and not paragraphs:
            continue
        if stripped.startswith('- 原文'):
            continue

        # Table detection
        if stripped.startswith('|') and ':---' in stripped:
            if current_para:
                text_content = ' '.join(current_para)
                revs = re.findall(r'r(\d{5,7})', text_content)
                if text_content.strip():
                    paragraphs.append({
                        'type': 'paragraph',
                        'text': text_content[:300],
                        'revs': revs,
                    })
                current_para = []
            in_table = True
            table_lines = []
            continue

        if in_table and stripped.startswith('|'):
            table_lines.append(stripped)
            continue

        if in_table and not stripped.startswith('|'):
            in_table = False
            if table_lines:
                table_text = '\n'.join(table_lines)
                revs = re.findall(r'r(\d{5,7})', table_text)
                paragraphs.append({
                    'type': 'table',
                    'text': table_text[:300],
                    'revs': revs,
                })
            table_lines = []

        # Section headers
        if re.match(r'^#{2,5}\s+', stripped):
            if current_para:
                text_content = ' '.join(current_para)
                revs = re.findall(r'r(\d{5,7})', text_content)
                if text_content.strip():
                    paragraphs.append({
                        'type': 'paragraph',
                        'text': text_content[:300],
                        'revs': revs,
                    })
                current_para = []
            continue

        # Empty line = paragraph break
        if not stripped:
            if current_para:
                text_content = ' '.join(current_para)
                revs = re.findall(r'r(\d{5,7})', text_content)
                if text_content.strip():
                    paragraphs.append({
                        'type': 'paragraph',
                        'text': text_content[:300],
                        'revs': revs,
                    })
                current_para = []
            continue

        # Content line
        if stripped:
            current_para.append(stripped)

    # Flush
    if current_para:
        text_content = ' '.join(current_para)
        revs = re.findall(r'r(\d{5,7})', text_content)
        if text_content.strip():
            paragraphs.append({
                'type': 'paragraph',
                'text': text_content[:300],
                'revs': revs,
            })

    return paragraphs

def check_note_blocks(en_text, cn_text):
    """Check for missing note/important blocks."""
    issues = []

    # Extract English note blocks with their content
    en_notes = []
    lines = en_text.split('\n')
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped == '[.note]' or stripped == '[.important]':
            note_type = 'Note' if 'note' in stripped else 'Important'
            i += 1
            content_lines = []
            while i < len(lines):
                s = lines[i].strip()
                if not s or s.startswith('[.') or re.match(r'^={2,4}\s+', s) or s == '|===':
                    break
                content_lines.append(s)
                i += 1
            content = ' '.join(content_lines)
            # Extract key identifiers
            revs = set(re.findall(r'r(\d{5,7})', content))
            # Extract man page references
            man_refs = set(re.findall(r'(\w+)\(\d+\)', content))
            en_notes.append({
                'type': note_type,
                'content': content[:300],
                'revs': revs,
                'man_refs': man_refs,
            })
        else:
            i += 1

    # Extract Chinese note blocks
    cn_notes = []
    lines = cn_text.split('\n')
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if (stripped.startswith('>') and ('注意' in stripped or '重要' in stripped)
            and not stripped.startswith('> ') == False):
            note_type = 'Note' if '注意' in stripped else 'Important'
            i += 1
            content_lines = []
            while i < len(lines):
                s = lines[i].strip()
                if not s.startswith('>') and s != '':
                    break
                if s.startswith('>'):
                    s = s[1:].strip()
                if s:
                    content_lines.append(s)
                i += 1
            content = ' '.join(content_lines)
            revs = set(re.findall(r'r(\d{5,7})', content))
            man_refs = set(re.findall(r'(\w+)\(\d+\)', content))
            cn_notes.append({
                'type': note_type,
                'content': content[:300],
                'revs': revs,
                'man_refs': man_refs,
            })
        else:
            i += 1

    # Also check for inline notes (like **注意**：)
    for line in cn_text.split('\n'):
        m = re.search(r'\*\*注意\*\*[：:](.+)', line)
        if m:
            content = m.group(1).strip()
            revs = set(re.findall(r'r(\d{5,7})', content))
            cn_notes.append({
                'type': 'Note',
                'content': content[:300],
                'revs': revs,
                'man_refs': set(),
            })

    # Compare
    for en_note in en_notes:
        found = False
        for cn_note in cn_notes:
            # Match by revision numbers
            if en_note['revs'] and cn_note['revs'] and en_note['revs'] & cn_note['revs']:
                found = True
                break
            # Match by man page references
            if en_note['man_refs'] and cn_note['man_refs'] and en_note['man_refs'] & cn_note['man_refs']:
                found = True
                break
            # Match by type and partial content overlap
            if en_note['type'] == cn_note['type']:
                # Check for key term overlap
                en_terms = set(re.findall(r'\b[a-z]{4,}\b', en_note['content'].lower()))
                cn_terms = set(re.findall(r'\b[a-z]{4,}\b', cn_note['content'].lower()))
                overlap = en_terms & cn_terms
                if len(overlap) >= 3:
                    found = True
                    break

        if not found:
            # Clean up the content for display
            clean = re.sub(r'http://www\.FreeBSD\.org/cgi/man\.cgi\?[^[]+\[([^\]]+)\]', r'\1', en_note['content'])
            clean = re.sub(r'http[s]?://svn\.freebsd\.org/\S+', '', clean)
            clean = clean.strip()[:200]
            issues.append(f"Missing {en_note['type']} block: {clean}")

    return issues

def compare_version_detailed(version):
    print(f"\n{'='*70}")
    print(f"COMPREHENSIVE CHECK: FreeBSD {version}")
    print(f"{'='*70}")

    en_text = fetch_url(EN_URLS[version])
    with open(CN_FILES[version], 'r', encoding='utf-8') as f:
        cn_text = f.read()

    issues = []

    # 1. Check revision numbers
    en_revs = set(re.findall(r'r(\d{5,7})', en_text))
    cn_revs = set(re.findall(r'r(\d{5,7})', cn_text))
    missing_revs = en_revs - cn_revs
    if missing_revs:
        for rev in sorted(missing_revs, key=int):
            issues.append(f"Missing revision r{rev}")
    else:
        print("  ✓ All revision numbers present")

    # 2. Check SA/EN entries
    en_sa = set(re.findall(r'FreeBSD-SA-\d{2}:\d+\.\w+', en_text))
    cn_sa = set(re.findall(r'FreeBSD-SA-\d{2}:\d+\.\w+', cn_text))
    missing_sa = en_sa - cn_sa
    if missing_sa:
        for sa in sorted(missing_sa):
            issues.append(f"Missing security advisory: {sa}")
    else:
        print(f"  ✓ All {len(en_sa)} security advisories present")

    en_en = set(re.findall(r'FreeBSD-EN-\d{2}:\d+\.\w+', en_text))
    cn_en = set(re.findall(r'FreeBSD-EN-\d{2}:\d+\.\w+', cn_text))
    missing_en = en_en - cn_en
    if missing_en:
        for en in sorted(missing_en):
            issues.append(f"Missing errata notice: {en}")
    else:
        print(f"  ✓ All {len(en_en)} errata notices present")

    # 3. Check note/important blocks
    note_issues = check_note_blocks(en_text, cn_text)
    if note_issues:
        for issue in note_issues:
            issues.append(issue)
    else:
        print("  ✓ All note/important blocks present")

    # 4. Check platform tags
    en_platforms = re.findall(r'\[(amd64|arm|arm64|i386|powerpc|sparc64)\]', en_text)
    cn_platforms = re.findall(r'\[(amd64|arm|arm64|i386|powerpc|sparc64)\]', cn_text)
    from collections import Counter
    en_pc = Counter(en_platforms)
    cn_pc = Counter(cn_platforms)
    for tag in en_pc:
        diff = en_pc[tag] - cn_pc.get(tag, 0)
        if diff > 0:
            issues.append(f"Missing [{tag}] platform tag: {diff} occurrences")
    if not any('platform tag' in i for i in issues):
        print("  ✓ All platform tags present")

    # 5. Check for specific content patterns
    # Check for inline code references like `command`
    en_code = re.findall(r'`([^`]+)`', en_text)
    cn_code = re.findall(r'`([^`]+)`', cn_text)
    # Check for specific important code references
    en_code_set = Counter(en_code)
    cn_code_set = Counter(cn_code)
    # Focus on command/option names that should be preserved
    missing_code = []
    for code, count in en_code_set.items():
        if count > cn_code_set.get(code, 0) and len(code) > 3 and not code.startswith('http'):
            diff = count - cn_code_set.get(code, 0)
            if diff >= 2:  # Only report if multiple occurrences missing
                missing_code.append((code, diff))
    if missing_code:
        for code, diff in sorted(missing_code, key=lambda x: -x[1])[:10]:
            issues.append(f"Inline code `{code}` appears {diff} fewer times in Chinese")

    # 6. Check for list items (bullet points)
    en_list_items = len(re.findall(r'^\* ', en_text, re.MULTILINE))
    cn_list_items = len(re.findall(r'^\* ', cn_text, re.MULTILINE))
    if en_list_items > cn_list_items:
        diff = en_list_items - cn_list_items
        if diff > 2:
            issues.append(f"Missing bullet list items: English has {en_list_items}, Chinese has {cn_list_items}")

    # Print issues
    if issues:
        print(f"\n  ISSUES FOUND ({len(issues)}):")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print("\n  ✓ No issues found - translation appears complete")

    return issues

def main():
    all_issues = {}
    for version in ["11.0", "11.1", "11.2", "11.3"]:
        all_issues[version] = compare_version_detailed(version)

    print(f"\n\n{'='*70}")
    print("FINAL SUMMARY")
    print(f"{'='*70}")
    total = 0
    for version in ["11.0", "11.1", "11.2", "11.3"]:
        count = len(all_issues[version])
        total += count
        if count > 0:
            print(f"\n  {version}.md - {count} issues:")
            for issue in all_issues[version]:
                print(f"    - {issue}")
        else:
            print(f"\n  {version}.md - Complete, no issues found")
    print(f"\n  Total issues: {total}")

if __name__ == '__main__':
    main()

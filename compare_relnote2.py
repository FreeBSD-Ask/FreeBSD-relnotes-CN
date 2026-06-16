#!/usr/bin/env python3
"""
Detailed comparison of Chinese translations vs English originals.
Focuses on finding missing sections, notes, important blocks, and paragraphs.
"""

import re
import urllib.request
import ssl
import json

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

def parse_adoc_sections(text):
    """Parse asciidoc into a structured list of sections with their content."""
    result = []
    lines = text.split('\n')
    current_section = None
    current_content = []
    in_table = False
    table_content = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip front matter
        if stripped == '---':
            i += 1
            continue

        # Skip includes and TOC
        if stripped.startswith('include::') or stripped.startswith('* <<'):
            i += 1
            continue

        # Table handling
        if stripped == '|===':
            if in_table:
                in_table = False
                if current_section is not None:
                    current_content.append(('table', '\n'.join(table_content)))
                table_content = []
            else:
                in_table = True
                table_content = []
            i += 1
            continue

        if in_table:
            table_content.append(stripped)
            i += 1
            continue

        # Section headers (== or === or ====)
        m = re.match(r'^(={2,4})\s+(.+)$', stripped)
        if m:
            # Save previous section
            if current_section is not None:
                result.append((current_section, current_content))
            level = len(m.group(1))
            title = m.group(2).strip()
            # Clean asciidoc anchors
            title = re.sub(r'\[\[.*?\]\]\s*', '', title)
            title = re.sub(r'`([^`]+)`', r'\1', title)
            current_section = (level, title)
            current_content = []
            i += 1
            continue

        # Skip anchor lines
        if stripped.startswith('[[') and stripped.endswith(']]'):
            i += 1
            continue

        # Note/Important blocks
        if stripped.startswith('[.note]') or stripped.startswith('[.important]'):
            i += 1
            continue

        # Content lines
        if stripped:
            current_content.append(('line', stripped))

        i += 1

    # Save last section
    if current_section is not None:
        result.append((current_section, current_content))

    return result

def parse_md_sections(text):
    """Parse markdown into a structured list of sections with their content."""
    result = []
    lines = text.split('\n')
    current_section = None
    current_content = []
    in_table = False
    table_content = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip title line and meta
        if i < 5 and (stripped.startswith('# ') or stripped.startswith('- 原文') or stripped == ''):
            i += 1
            continue

        # Table detection
        if stripped.startswith('|') and ':---' in stripped:
            in_table = True
            i += 1
            continue

        if in_table and stripped.startswith('|'):
            table_content.append(stripped)
            i += 1
            continue

        if in_table and not stripped.startswith('|'):
            in_table = False
            if current_section is not None:
                current_content.append(('table', '\n'.join(table_content)))
            table_content = []

        # Section headers
        m = re.match(r'^(#{2,5})\s+(.+)$', stripped)
        if m:
            if current_section is not None:
                result.append((current_section, current_content))
            level = len(m.group(1))
            title = m.group(2).strip()
            # Clean markdown
            title = re.sub(r'`([^`]+)`', r'\1', title)
            title = re.sub(r'\*\*([^*]+)\*\*', r'\1', title)
            current_section = (level, title)
            current_content = []
            i += 1
            continue

        # Content lines
        if stripped:
            current_content.append(('line', stripped))

        i += 1

    # Save last section
    if current_section is not None:
        result.append((current_section, current_content))

    return result

def extract_en_note_blocks(text):
    """Extract note and important blocks from asciidoc."""
    notes = []
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped == '[.note]' or stripped == '[.important]':
            note_type = 'Note' if 'note' in stripped else 'Important'
            # Collect the content
            i += 1
            content_lines = []
            while i < len(lines):
                s = lines[i].strip()
                if not s or s.startswith('[.') or re.match(r'^={2,4}\s+', s):
                    break
                content_lines.append(s)
                i += 1
            content = ' '.join(content_lines)
            # Clean asciidoc
            content = re.sub(r'http://www\.FreeBSD\.org/cgi/man\.cgi\?[^[]+\[([^\]]+)\]', r'\1', content)
            content = re.sub(r'http[s]?://\S+', '', content)
            content = content.strip()
            if content:
                notes.append((note_type, content[:200]))
        else:
            i += 1
    return notes

def extract_cn_note_blocks(text):
    """Extract note and important blocks from markdown."""
    notes = []
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped == '>**注意**' or stripped == '>**重要**' or stripped == '> **注意**' or stripped == '> **重要**':
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
            content = content.strip()
            if content:
                notes.append((note_type, content[:200]))
        else:
            i += 1
    return notes

def compare_version(version):
    """Detailed comparison for a specific version."""
    print(f"\n{'='*70}")
    print(f"DETAILED COMPARISON: FreeBSD {version}")
    print(f"{'='*70}")

    en_text = fetch_url(EN_URLS[version])
    with open(CN_FILES[version], 'r', encoding='utf-8') as f:
        cn_text = f.read()

    # 1. Compare notes/important blocks
    en_notes = extract_en_note_blocks(en_text)
    cn_notes = extract_cn_note_blocks(cn_text)

    print(f"\n--- Note/Important Blocks ---")
    print(f"  English: {len(en_notes)} blocks")
    print(f"  Chinese: {len(cn_notes)} blocks")

    if len(en_notes) > len(cn_notes):
        print(f"  MISSING: {len(en_notes) - len(cn_notes)} note/important blocks")
        # Try to identify which ones are missing
        cn_contents = [c for _, c in cn_notes]
        for ntype, content in en_notes:
            # Simple matching - check if any Chinese note contains similar content
            found = False
            for cn_c in cn_contents:
                # Check for overlap in key terms
                # Extract revision numbers as a more reliable match
                en_revs = set(re.findall(r'r(\d{5,7})', content))
                cn_revs_in_note = set(re.findall(r'r(\d{5,7})', cn_c))
                if en_revs and cn_revs_in_note and en_revs & cn_revs_in_note:
                    found = True
                    break
            if not found:
                # Try matching by key words
                print(f"    Possibly missing {ntype}: {content[:150]}")

    # 2. Compare sections in detail
    en_sections = parse_adoc_sections(en_text)
    cn_sections = parse_md_sections(cn_text)

    print(f"\n--- Section-by-Section Comparison ---")
    print(f"  English sections: {len(en_sections)}")
    print(f"  Chinese sections: {len(cn_sections)}")

    # Map sections by position
    en_idx = 0
    cn_idx = 0
    missing_sections = []

    for en_sec, en_content in en_sections:
        en_level, en_title = en_sec
        # Skip Table of Contents
        if 'Table of Contents' in en_title:
            continue

        # Try to find matching Chinese section
        found = False
        for cn_sec, cn_content in cn_sections:
            cn_level, cn_title = cn_sec
            # Compare by level (allowing for level offset due to markdown vs asciidoc)
            if cn_level == en_level or cn_level == en_level + 1 or cn_level == en_level - 1:
                # Check if titles could be translations
                # This is a rough check
                found = True
                break

        # Compare content items count
        en_content_items = len([c for c in en_content if c[0] == 'line'])
        cn_content_items = len([c for c in cn_content if c[0] == 'line'])
        en_tables = len([c for c in en_content if c[0] == 'table'])
        cn_tables = len([c for c in cn_content if c[0] == 'table'])

        if en_content_items > 0 or en_tables > 0:
            diff = en_content_items - cn_content_items
            if diff > 2:  # Allow some tolerance
                print(f"  Section '{en_title}': EN has {en_content_items} items, CN has {cn_content_items} items (diff: {diff})")

    # 3. Check for missing paragraphs by comparing revision numbers in context
    print(f"\n--- Paragraph-Level Missing Content Check ---")

    # Extract all paragraphs with their revision numbers from English
    en_paragraphs = []
    current_para = []
    for line in en_text.split('\n'):
        stripped = line.strip()
        if stripped.startswith('---') or stripped.startswith('include::') or stripped.startswith('* <<') or stripped.startswith('[['):
            continue
        if not stripped or re.match(r'^={2,4}\s+', stripped) or stripped == '|===':
            if current_para:
                text = ' '.join(current_para)
                revs = re.findall(r'r(\d{5,7})', text)
                if revs:
                    en_paragraphs.append((revs, text[:200]))
                current_para = []
        else:
            current_para.append(stripped)
    if current_para:
        text = ' '.join(current_para)
        revs = re.findall(r'r(\d{5,7})', text)
        if revs:
            en_paragraphs.append((revs, text[:200]))

    # Same for Chinese
    cn_paragraphs = []
    current_para = []
    for line in cn_text.split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            if current_para:
                text = ' '.join(current_para)
                revs = re.findall(r'r(\d{5,7})', text)
                if revs:
                    cn_paragraphs.append((revs, text[:200]))
                current_para = []
        else:
            current_para.append(stripped)
    if current_para:
        text = ' '.join(current_para)
        revs = re.findall(r'r(\d{5,7})', text)
        if revs:
            cn_paragraphs.append((revs, text[:200]))

    # Check each English paragraph's revision numbers against Chinese
    cn_all_revs = set()
    for revs, _ in cn_paragraphs:
        cn_all_revs.update(revs)

    missing_paragraphs = []
    for revs, preview in en_paragraphs:
        # If any revision from this paragraph is missing in Chinese
        missing_revs_in_para = [r for r in revs if r not in cn_all_revs]
        if missing_revs_in_para:
            missing_paragraphs.append((missing_revs_in_para, preview))

    if missing_paragraphs:
        print(f"  Found {len(missing_paragraphs)} paragraphs with missing revision references:")
        for revs, preview in missing_paragraphs:
            print(f"    r{', r'.join(revs)}: {preview[:150]}")
    else:
        print(f"  All paragraphs accounted for by revision number check.")

    # 4. Check for missing content by counting items per section
    print(f"\n--- Item Count per Section ---")

    # Group by section
    en_section_data = {}
    current_sec_name = None
    for sec, content in en_sections:
        level, title = sec
        if 'Table of Contents' in title:
            continue
        current_sec_name = title
        en_section_data[current_sec_name] = {
            'lines': len([c for c in content if c[0] == 'line']),
            'tables': len([c for c in content if c[0] == 'table']),
        }

    cn_section_data = {}
    for sec, content in cn_sections:
        level, title = sec
        cn_section_data[title] = {
            'lines': len([c for c in content if c[0] == 'line']),
            'tables': len([c for c in content if c[0] == 'table']),
        }

    # Print sections with significant differences
    for sec_name, data in en_section_data.items():
        if data['lines'] > 3:  # Only check sections with content
            # Find corresponding Chinese section
            # This is approximate
            pass

    # 5. Specific check for FreeBSD-SA and FreeBSD-EN entries
    print(f"\n--- Security Advisory / Errata Table Entries ---")
    en_sa_entries = re.findall(r'FreeBSD-SA-\d{2}:\d+\.\w+', en_text)
    cn_sa_entries = re.findall(r'FreeBSD-SA-\d{2}:\d+\.\w+', cn_text)
    en_en_entries = re.findall(r'FreeBSD-EN-\d{2}:\d+\.\w+', en_text)
    cn_en_entries = re.findall(r'FreeBSD-EN-\d{2}:\d+\.\w+', cn_text)

    print(f"  English SA entries: {len(en_sa_entries)}")
    print(f"  Chinese SA entries: {len(cn_sa_entries)}")
    missing_sa = set(en_sa_entries) - set(cn_sa_entries)
    if missing_sa:
        print(f"  MISSING SA entries: {', '.join(sorted(missing_sa))}")

    print(f"  English EN entries: {len(en_en_entries)}")
    print(f"  Chinese EN entries: {len(cn_en_entries)}")
    missing_en = set(en_en_entries) - set(cn_en_entries)
    if missing_en:
        print(f"  MISSING EN entries: {', '.join(sorted(missing_en))}")

    # 6. Check for specific note content that might be missing
    print(f"\n--- Detailed Note Comparison ---")
    for i, (ntype, content) in enumerate(en_notes):
        # Extract revision numbers from the note
        en_note_revs = set(re.findall(r'r(\d{5,7})', content))
        # Check if this note exists in Chinese
        found = False
        for cn_ntype, cn_content in cn_notes:
            cn_note_revs = set(re.findall(r'r(\d{5,7})', cn_content))
            if en_note_revs and cn_note_revs and en_note_revs & cn_note_revs:
                found = True
                break
            # Also check for keyword overlap
            en_keywords = set(re.findall(r'\b\w{4,}\b', content.lower()))
            cn_keywords = set(re.findall(r'\b\w{4,}\b', cn_content.lower()))
            if en_keywords & cn_keywords and len(en_keywords & cn_keywords) > 3:
                found = True
                break

        if not found:
            print(f"  Possibly missing {ntype} block #{i+1}:")
            print(f"    {content[:200]}")

    return {
        'missing_sa': missing_sa,
        'missing_en': missing_en,
        'missing_notes': len(en_notes) - len(cn_notes),
    }

def main():
    results = {}
    for version in ["11.0", "11.1", "11.2", "11.3"]:
        results[version] = compare_version(version)

    print(f"\n\n{'='*70}")
    print("FINAL SUMMARY")
    print(f"{'='*70}")
    for version in ["11.0", "11.1", "11.2", "11.3"]:
        r = results[version]
        issues = []
        if r['missing_sa']:
            issues.append(f"Missing SA: {', '.join(sorted(r['missing_sa']))}")
        if r['missing_en']:
            issues.append(f"Missing EN: {', '.join(sorted(r['missing_en']))}")
        if r['missing_notes'] > 0:
            issues.append(f"Missing {r['missing_notes']} note/important blocks")
        if issues:
            print(f"  {version}: {'; '.join(issues)}")
        else:
            print(f"  {version}: No major issues found")

if __name__ == '__main__':
    main()

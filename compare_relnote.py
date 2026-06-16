#!/usr/bin/env python3
"""
Compare Chinese translation files with original English sources from FreeBSD
to check for missing paragraphs, sentences, code blocks, or inline code.
"""

import re
import urllib.request
import ssl
import sys

# URLs for the English sources
EN_URLS = {
    "11.0": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/11.0R/relnotes.adoc",
    "11.1": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/11.1R/relnotes.adoc",
    "11.2": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/11.2R/relnotes.adoc",
    "11.3": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/11.3R/relnotes.adoc",
}

# Chinese translation files
CN_FILES = {
    "11.0": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\11.0.md",
    "11.1": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\11.1.md",
    "11.2": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\11.2.md",
    "11.3": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\11.3.md",
}

def fetch_url(url):
    """Fetch content from URL."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx) as resp:
        return resp.read().decode('utf-8')

def extract_revision_numbers(text):
    """Extract all revision numbers like r123456 from text."""
    return set(re.findall(r'r(\d{5,7})', text))

def extract_sections_adoc(text):
    """Extract section headings from asciidoc text."""
    sections = []
    for line in text.split('\n'):
        line = line.strip()
        # Match == Section Title or === Subsection Title
        m = re.match(r'^(={2,4})\s+(.+)$', line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            # Skip document title (single =) and TOC
            if level >= 2:
                # Clean up asciidoc markup
                title = re.sub(r'\[\[.*?\]\]', '', title)
                title = re.sub(r'<<.*?>>', '', title)
                title = title.strip()
                if title:
                    sections.append((level, title))
    return sections

def extract_sections_md(text):
    """Extract section headings from markdown text."""
    sections = []
    for line in text.split('\n'):
        line = line.strip()
        m = re.match(r'^(#{2,5})\s+(.+)$', line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            if title:
                sections.append((level, title))
    return sections

def extract_adoc_content_blocks(text):
    """Extract meaningful content blocks from asciidoc (paragraphs, list items, tables, notes)."""
    blocks = []
    lines = text.split('\n')
    i = 0
    current_block = []
    in_table = False
    in_note = False

    while i < len(lines):
        line = lines[i].strip()

        # Skip front matter, includes, TOC entries
        if line.startswith('---') or line.startswith('include::') or line.startswith('* <<'):
            i += 1
            continue

        # Table start/end
        if line == '|===':
            if in_table:
                in_table = False
                if current_block:
                    blocks.append(('table', '\n'.join(current_block)))
                    current_block = []
            else:
                in_table = True
                current_block = []
            i += 1
            continue

        if in_table:
            if line and not line.startswith('|'):
                pass  # skip non-table lines inside table
            current_block.append(line)
            i += 1
            continue

        # Note/Important blocks
        if line.startswith('[.note]') or line.startswith('[.important]'):
            in_note = True
            i += 1
            continue

        if in_note and line.startswith('*Note*') or line.startswith('*Important*'):
            current_block.append(line)
            i += 1
            continue

        # Section headers
        if re.match(r'^={2,4}\s+', line):
            if current_block:
                content = '\n'.join(current_block).strip()
                if content:
                    blocks.append(('paragraph', content))
                current_block = []
            i += 1
            continue

        # Empty line = paragraph break
        if not line:
            if current_block:
                content = '\n'.join(current_block).strip()
                if content:
                    blocks.append(('paragraph', content))
                current_block = []
            i += 1
            continue

        # Content line
        if line and not line.startswith('[['):
            current_block.append(line)

        i += 1

    # Flush remaining
    if current_block:
        content = '\n'.join(current_block).strip()
        if content:
            blocks.append(('paragraph', content))

    return blocks

def find_missing_revisions(en_text, cn_text):
    """Find revision numbers present in English but missing from Chinese."""
    en_revs = extract_revision_numbers(en_text)
    cn_revs = extract_revision_numbers(cn_text)
    missing = en_revs - cn_revs
    return sorted(missing, key=lambda x: int(x))

def find_missing_sections(en_sections, cn_sections):
    """Compare section structures between English and Chinese."""
    missing = []

    # Extract just the section titles for comparison
    en_titles = []
    for level, title in en_sections:
        # Clean up for comparison
        clean = re.sub(r'http[s]?://\S+', '', title)
        clean = re.sub(r'`[^`]+`', '', clean)
        clean = clean.strip()
        if clean:
            en_titles.append((level, clean))

    cn_titles = []
    for level, title in cn_sections:
        clean = re.sub(r'http[s]?://\S+', '', title)
        clean = re.sub(r'`[^`]+`', '', clean)
        clean = clean.strip()
        if clean:
            cn_titles.append((level, clean))

    # Check if Chinese has the same number of sections
    if len(cn_titles) < len(en_titles):
        missing.append(f"  English has {len(en_titles)} sections, Chinese has {len(cn_titles)} sections")

    return missing

def extract_paragraphs_with_revs(text):
    """Extract paragraphs that contain revision references, along with their revision numbers."""
    paragraphs = []
    # Split by double newline or section headers
    blocks = re.split(r'\n\n+|\n(?==)', text)
    for block in blocks:
        block = block.strip()
        revs = re.findall(r'r(\d{5,7})', block)
        if revs:
            # Get first 100 chars as preview
            preview = block[:150].replace('\n', ' ')
            paragraphs.append((revs, preview))
    return paragraphs

def compare_file(version):
    """Compare a single version's English source with Chinese translation."""
    print(f"\n{'='*70}")
    print(f"Comparing FreeBSD {version} Release Notes")
    print(f"{'='*70}")

    # Fetch English source
    print(f"Fetching English source for {version}...")
    en_text = fetch_url(EN_URLS[version])

    # Read Chinese translation
    print(f"Reading Chinese translation for {version}...")
    with open(CN_FILES[version], 'r', encoding='utf-8') as f:
        cn_text = f.read()

    # 1. Compare revision numbers
    missing_revs = find_missing_revisions(en_text, cn_text)
    if missing_revs:
        print(f"\n--- Missing Revision Numbers ({len(missing)}) ---")
        for rev in missing_revs:
            # Find the context of this revision in the English text
            pattern = re.compile(r'r' + rev + r'[^\n]*', re.IGNORECASE)
            matches = pattern.findall(en_text)
            context = matches[0][:120] if matches else "unknown context"
            print(f"  r{rev}: {context}")
    else:
        print("\n  All revision numbers are present.")

    # 2. Compare section structure
    en_sections = extract_sections_adoc(en_text)
    cn_sections = extract_sections_md(cn_text)

    print(f"\n--- Section Structure ---")
    print(f"  English sections: {len(en_sections)}")
    print(f"  Chinese sections: {len(cn_sections)}")

    # Map English section titles to Chinese equivalents
    # We check by position and level
    en_flat = [(l, t) for l, t in en_sections if not t.startswith('Table of Contents')]
    cn_flat = cn_sections

    if len(cn_flat) < len(en_flat):
        print(f"  WARNING: Chinese has {len(en_flat) - len(cn_flat)} fewer sections than English")

    # 3. Check for specific content markers
    # Check for platform tags like [powerpc], [sparc64], [arm], [amd64]
    en_platform_tags = re.findall(r'\[(amd64|arm|arm64|i386|powerpc|sparc64)\]', en_text)
    cn_platform_tags = re.findall(r'\[(amd64|arm|arm64|i386|powerpc|sparc64)\]', cn_text)

    print(f"\n--- Platform Tags ---")
    print(f"  English platform tags: {len(en_platform_tags)}")
    print(f"  Chinese platform tags: {len(cn_platform_tags)}")
    if len(cn_platform_tags) < len(en_platform_tags):
        print(f"  WARNING: {len(en_platform_tags) - len(cn_platform_tags)} platform tags missing in Chinese")
        # Find which specific tags are missing
        from collections import Counter
        en_counter = Counter(en_platform_tags)
        cn_counter = Counter(cn_platform_tags)
        for tag in en_counter:
            diff = en_counter[tag] - cn_counter.get(tag, 0)
            if diff > 0:
                print(f"    Missing [{tag}]: {diff} occurrences")

    # 4. Check for code blocks
    en_code_blocks = re.findall(r'`[^`\n]+`', en_text)
    cn_code_blocks = re.findall(r'`[^`\n]+`', cn_text)
    print(f"\n--- Inline Code ---")
    print(f"  English inline code: {len(en_code_blocks)}")
    print(f"  Chinese inline code: {len(cn_code_blocks)}")

    # 5. Check for tables
    en_tables = en_text.count('|===')
    cn_tables = cn_text.count('| :---') + cn_text.count('|:---')
    print(f"\n--- Tables ---")
    print(f"  English table markers (|===): {en_tables // 2}")
    print(f"  Chinese table markers: {cn_tables // 2}")

    # 6. Check for note/important blocks
    en_notes = len(re.findall(r'\[\.note\]|\[\.important\]', en_text))
    cn_notes = len(re.findall(r'>\*\*注意\*\*|>\*\*重要\*\*', cn_text))
    print(f"\n--- Note/Important Blocks ---")
    print(f"  English note/important blocks: {en_notes}")
    print(f"  Chinese note/important blocks: {cn_notes}")

    # 7. Check for specific missing paragraphs by looking at revision numbers
    # and their surrounding context
    if missing_revs:
        print(f"\n--- Detailed Missing Content (by revision) ---")
        for rev in missing_revs:
            # Find the paragraph containing this revision
            lines = en_text.split('\n')
            for i, line in enumerate(lines):
                if f'r{rev}' in line or f'revision={rev}' in line:
                    # Get surrounding context
                    start = max(0, i-2)
                    end = min(len(lines), i+3)
                    context_lines = lines[start:end]
                    context = ' '.join(l.strip() for l in context_lines if l.strip())
                    # Clean up asciidoc links
                    context = re.sub(r'http://www\.FreeBSD\.org/cgi/man\.cgi\?[^[]+\[([^\]]+)\]', r'\1', context)
                    context = re.sub(r'http[s]?://\S+', '', context)
                    context = context[:200]
                    print(f"  r{rev}: {context}")
                    break

    return missing_revs

def main():
    all_missing = {}
    for version in ["11.0", "11.1", "11.2", "11.3"]:
        missing = compare_file(version)
        all_missing[version] = missing

    # Summary
    print(f"\n\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    for version in ["11.0", "11.1", "11.2", "11.3"]:
        count = len(all_missing[version])
        if count > 0:
            print(f"  {version}: {count} missing revision references")
        else:
            print(f"  {version}: Complete - no missing content detected by revision check")

if __name__ == '__main__':
    main()

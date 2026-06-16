#!/usr/bin/env python3
"""
Compare Chinese translation files with English originals from FreeBSD release notes.
Check for missing paragraphs, sentences, code blocks, inline code, and table entries.
"""

import re
import urllib.request
import ssl
import sys
import os

# Disable SSL verification for fetching
ssl._create_default_https_context = ssl._create_unverified_context

FILES = [
    {
        "cn": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\10.0.md",
        "en_url": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/10.0R/relnotes.adoc",
        "version": "10.0"
    },
    {
        "cn": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\10.1.md",
        "en_url": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/10.1R/relnotes.adoc",
        "version": "10.1"
    },
    {
        "cn": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\10.2.md",
        "en_url": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/10.2R/relnotes.adoc",
        "version": "10.2"
    },
    {
        "cn": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\10.3.md",
        "en_url": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/10.3R/relnotes.adoc",
        "version": "10.3"
    },
    {
        "cn": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\10.4.md",
        "en_url": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/10.4R/relnotes.adoc",
        "version": "10.4"
    },
]


def fetch_url(url):
    """Fetch content from URL."""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')


def read_file(path):
    """Read file content."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_sections_adoc(text):
    """Extract sections from AsciiDoc English source."""
    sections = []
    # Match == Section Title or === Subsection Title
    pattern = re.compile(r'^(={2,4})\s+(.+)$', re.MULTILINE)
    for m in pattern.finditer(text):
        level = len(m.group(1))
        title = m.group(2).strip()
        # Clean up asciidoc markup from title
        title = re.sub(r'\[\[.*?\]\]', '', title)
        title = re.sub(r'<<.*?>>', '', title)
        title = title.strip()
        sections.append((level, title, m.start()))
    return sections


def extract_sections_md(text):
    """Extract sections from Markdown Chinese translation."""
    sections = []
    pattern = re.compile(r'^(#{1,4})\s+(.+)$', re.MULTILINE)
    for m in pattern.finditer(text):
        level = len(m.group(1))
        title = m.group(2).strip()
        sections.append((level, title, m.start()))
    return sections


def extract_code_blocks(text):
    """Extract code blocks from text."""
    # AsciiDoc code blocks: [source,...] or [.programlisting] followed by ----
    adoc_blocks = re.findall(r'\[\.programlisting\]\n----\n(.*?)\n----', text, re.DOTALL)
    # Also match [source,...] style
    adoc_blocks += re.findall(r'\[source[^\]]*\]\n----\n(.*?)\n----', text, re.DOTALL)
    
    # Markdown code blocks: ```...```
    md_blocks = re.findall(r'```\w*\n(.*?)\n```', text, re.DOTALL)
    
    return adoc_blocks, md_blocks


def extract_table_entries_adoc(text):
    """Extract table entries from AsciiDoc source."""
    entries = []
    # Find all table rows (lines starting with |)
    # First find table sections
    in_table = False
    for line in text.split('\n'):
        if '|===' in line:
            in_table = not in_table
            continue
        if in_table and line.startswith('|'):
            # This is a table row
            cells = [c.strip() for c in line.split('|')[1:]]
            if cells and cells[0] and not cells[0].startswith('Advisory') and not cells[0].startswith('Errata') and not cells[0].startswith('Date'):
                entries.append(cells)
    return entries


def extract_table_entries_md(text):
    """Extract table entries from Markdown source."""
    entries = []
    in_table = False
    for line in text.split('\n'):
        if '|' in line and not line.strip().startswith('|:'):
            cells = [c.strip() for c in line.split('|')]
            # Remove empty first/last from split
            cells = [c for c in cells if c]
            if cells:
                # Skip header rows
                first_cell = cells[0]
                if first_cell and 'SA-' not in first_cell and 'EN-' not in first_cell and '公告' not in first_cell and '勘误' not in first_cell and '日期' not in first_cell:
                    continue
                if 'SA-' in first_cell or 'EN-' in first_cell:
                    entries.append(cells)
    return entries


def extract_sa_entries_adoc(text):
    """Extract security advisory entries from AsciiDoc."""
    entries = []
    # Match SA-XX:XX.xxx patterns
    pattern = re.compile(r'SA-\d{2}:\d{2}\.\w+', re.IGNORECASE)
    return list(set(pattern.findall(text)))


def extract_sa_entries_md(text):
    """Extract security advisory entries from Markdown."""
    entries = []
    pattern = re.compile(r'SA-\d{2}:\d{2}\.\w+', re.IGNORECASE)
    return list(set(pattern.findall(text)))


def extract_en_entries_adoc(text):
    """Extract errata notice entries from AsciiDoc."""
    entries = []
    pattern = re.compile(r'EN-\d{2}:\d{2}\.\w+', re.IGNORECASE)
    return list(set(pattern.findall(text)))


def extract_en_entries_md(text):
    """Extract errata notice entries from Markdown."""
    entries = []
    pattern = re.compile(r'EN-\d{2}:\d{2}\.\w+', re.IGNORECASE)
    return list(set(pattern.findall(text)))


def extract_platform_markers_adoc(text):
    """Extract platform-specific entries from AsciiDoc."""
    # Match [amd64], [i386], [powerpc], [sparc64], [arm], [amd64,i386] etc.
    pattern = re.compile(r'\[(amd64|i386|powerpc|powerpc64|sparc64|arm|armv6|armv7)(?:,(amd64|i386|powerpc|powerpc64|sparc64|arm|armv6|armv7))*\]', re.IGNORECASE)
    return pattern.findall(text)


def extract_revision_refs(text):
    """Extract revision references like (rXXXXXX) or [(rXXXXXX)]."""
    pattern = re.compile(r'r\d{5,6}')
    return list(set(pattern.findall(text)))


def extract_inline_code_adoc(text):
    """Extract inline code references from AsciiDoc (backtick content)."""
    # Match `content` patterns
    pattern = re.compile(r'`([^`]+)`')
    return list(set(pattern.findall(text)))


def extract_man_page_refs_adoc(text):
    """Extract man page references like name(N) from AsciiDoc."""
    pattern = re.compile(r'(?:query=)?(\w[\w.-]*)&(?:amp;)?sektion=(\d)')
    refs = pattern.findall(text)
    return [f"{name}({section})" for name, section in refs]


def extract_man_page_refs_md(text):
    """Extract man page references from Markdown."""
    pattern = re.compile(r'(\w[\w.-]*)\((\d)\)')
    refs = pattern.findall(text)
    return [f"{name}({section})" for name, section in refs]


def extract_paragraphs_adoc(text):
    """Extract substantive paragraphs from AsciiDoc (non-empty, non-heading, non-table lines)."""
    paragraphs = []
    lines = text.split('\n')
    current_para = []
    in_table = False
    in_code = False
    
    for line in lines:
        stripped = line.strip()
        
        if '|===' in stripped:
            in_table = not in_table
            continue
        if stripped == '----':
            in_code = not in_code
            if not in_code and current_para:
                paragraphs.append('\n'.join(current_para))
                current_para = []
            continue
        if in_table or in_code:
            continue
        
        # Skip headings, empty lines, metadata
        if not stripped:
            if current_para:
                paragraphs.append('\n'.join(current_para))
                current_para = []
            continue
        if stripped.startswith('=') or stripped.startswith('[[') or stripped.startswith('include::'):
            if current_para:
                paragraphs.append('\n'.join(current_para))
                current_para = []
            continue
        if stripped.startswith('[') and not stripped.startswith('[amd64') and not stripped.startswith('[i386') and not stripped.startswith('[powerpc') and not stripped.startswith('[arm') and not stripped.startswith('[sparc64'):
            if current_para:
                paragraphs.append('\n'.join(current_para))
                current_para = []
            continue
        if stripped.startswith('*') or stripped.startswith('.'):
            paragraphs.append(stripped)
            continue
        
        current_para.append(stripped)
    
    if current_para:
        paragraphs.append('\n'.join(current_para))
    
    return paragraphs


def compare_file(file_info):
    """Compare a single Chinese translation with its English original."""
    version = file_info["version"]
    cn_path = file_info["cn"]
    en_url = file_info["en_url"]
    
    print(f"\n{'='*60}")
    print(f"Comparing FreeBSD {version}")
    print(f"{'='*60}")
    
    # Fetch and read files
    try:
        en_text = fetch_url(en_url)
    except Exception as e:
        print(f"  ERROR: Failed to fetch English source: {e}")
        return []
    
    try:
        cn_text = read_file(cn_path)
    except Exception as e:
        print(f"  ERROR: Failed to read Chinese translation: {e}")
        return []
    
    issues = []
    
    # 1. Compare sections
    print(f"\n--- Section Comparison ---")
    en_sections = extract_sections_adoc(en_text)
    cn_sections = extract_sections_md(cn_text)
    
    # Extract section titles for comparison
    en_titles = []
    for level, title, pos in en_sections:
        # Normalize title for comparison
        clean = re.sub(r'\[\[.*?\]\]', '', title)
        clean = clean.strip()
        en_titles.append(clean)
    
    cn_titles = []
    for level, title, pos in cn_sections:
        cn_titles.append(title)
    
    print(f"  English sections: {len(en_titles)}")
    print(f"  Chinese sections: {len(cn_titles)}")
    
    if len(en_titles) > len(cn_titles):
        print(f"  WARNING: English has {len(en_titles) - len(cn_titles)} more sections than Chinese")
    
    # 2. Compare Security Advisory entries
    print(f"\n--- Security Advisory Comparison ---")
    en_sa = extract_sa_entries_adoc(en_text)
    cn_sa = extract_sa_entries_md(cn_text)
    
    # Normalize for comparison
    en_sa_normalized = set(s.lower() for s in en_sa)
    cn_sa_normalized = set(s.lower() for s in cn_sa)
    
    missing_sa = en_sa_normalized - cn_sa_normalized
    if missing_sa:
        print(f"  MISSING Security Advisories in Chinese translation:")
        for sa in sorted(missing_sa):
            print(f"    - {sa}")
            issues.append(f"缺失安全公告: {sa}")
    else:
        print(f"  All {len(en_sa_normalized)} security advisories present")
    
    # 3. Compare Errata Notice entries
    print(f"\n--- Errata Notice Comparison ---")
    en_en = extract_en_entries_adoc(en_text)
    cn_en = extract_en_entries_md(cn_text)
    
    en_en_normalized = set(e.lower() for e in en_en)
    cn_en_normalized = set(e.lower() for e in cn_en)
    
    missing_en = en_en_normalized - cn_en_normalized
    if missing_en:
        print(f"  MISSING Errata Notices in Chinese translation:")
        for en in sorted(missing_en):
            print(f"    - {en}")
            issues.append(f"缺失勘误通知: {en}")
    else:
        print(f"  All {len(en_en_normalized)} errata notices present")
    
    # 4. Compare code blocks
    print(f"\n--- Code Block Comparison ---")
    en_code, cn_code = extract_code_blocks(en_text), extract_code_blocks(cn_text)
    # Actually need to call separately
    en_code_adoc, _ = extract_code_blocks(en_text)
    _, cn_code_md = extract_code_blocks(cn_text)
    
    print(f"  English code blocks: {len(en_code_adoc)}")
    print(f"  Chinese code blocks: {len(cn_code_md)}")
    
    if len(en_code_adoc) > len(cn_code_md):
        diff = len(en_code_adoc) - len(cn_code_md)
        print(f"  WARNING: {diff} code block(s) may be missing in Chinese translation")
        issues.append(f"可能缺失 {diff} 个代码块")
    
    # 5. Compare revision references
    print(f"\n--- Revision Reference Comparison ---")
    en_revs = extract_revision_refs(en_text)
    cn_revs = extract_revision_refs(cn_text)
    
    en_rev_set = set(en_revs)
    cn_rev_set = set(cn_revs)
    
    missing_revs = en_rev_set - cn_rev_set
    if missing_revs:
        print(f"  MISSING revision references ({len(missing_revs)}):")
        for rev in sorted(missing_revs):
            print(f"    - r{rev}")
        issues.append(f"缺失 {len(missing_revs)} 个修订引用: {', '.join(sorted('r'+r for r in missing_revs))}")
    else:
        print(f"  All {len(en_rev_set)} revision references present")
    
    # 6. Compare man page references
    print(f"\n--- Man Page Reference Comparison ---")
    en_man = set(extract_man_page_refs_adoc(en_text))
    cn_man = set(extract_man_page_refs_md(cn_text))
    
    missing_man = en_man - cn_man
    if missing_man:
        print(f"  MISSING man page references ({len(missing_man)}):")
        for ref in sorted(missing_man):
            print(f"    - {ref}")
        issues.append(f"缺失 {len(missing_man)} 个手册页引用: {', '.join(sorted(missing_man))}")
    else:
        print(f"  All {len(en_man)} man page references present")
    
    # 7. Check for platform-specific entries
    print(f"\n--- Platform-Specific Entry Check ---")
    # Look for [amd64], [i386], [powerpc], [arm] etc. in English
    platform_pattern = re.compile(r'\[(amd64|i386|powerpc(?:64)?|sparc64|arm(?:v[67])?)\]', re.IGNORECASE)
    en_platforms = platform_pattern.findall(en_text)
    cn_platforms = platform_pattern.findall(cn_text)
    
    print(f"  English platform markers: {len(en_platforms)}")
    print(f"  Chinese platform markers: {len(cn_platforms)}")
    
    if len(en_platforms) > len(cn_platforms):
        diff = len(en_platforms) - len(cn_platforms)
        print(f"  WARNING: {diff} platform-specific entries may be missing")
        issues.append(f"可能缺失 {diff} 个平台特定条目")
    
    # 8. Detailed paragraph-level comparison
    # Look for specific key terms that should appear in both
    print(f"\n--- Key Term Presence Check ---")
    # Check for specific important terms/technologies mentioned in English
    key_terms = [
        'bhyve', 'capsicum', 'zfs', 'netmap', 'carp', 'virtio', 'capsicum',
        'nvme', 'fuse', 'iscsi', 'unbound', 'clang', 'llvm', 'pkg',
        'geli', 'loader', 'vt', 'drm', 'radeon', 'hyper-v', 'xen',
        'jail', 'dtrace', 'pf', 'ipfw', 'sctp', 'autofs',
        'growfs', 'bsdinstall', 'freebsd-update',
    ]
    
    for term in key_terms:
        en_count = len(re.findall(re.escape(term), en_text, re.IGNORECASE))
        cn_count = len(re.findall(re.escape(term), cn_text, re.IGNORECASE))
        if en_count > 0 and cn_count == 0:
            print(f"  WARNING: Term '{term}' appears {en_count} times in English but 0 in Chinese")
            issues.append(f"术语 '{term}' 在英文中出现 {en_count} 次但中文中未出现")
    
    # 9. Check for specific paragraphs that might be missing
    # by looking for unique identifiers in English (revision numbers)
    print(f"\n--- Paragraph Completeness Check (via revision refs) ---")
    # Each revision reference in English should have a corresponding one in Chinese
    # We already checked this above, but let's be more specific
    
    # Find all paragraphs in English that contain revision references
    en_para_revs = {}
    for line in en_text.split('\n'):
        revs = re.findall(r'r(\d{5,6})', line)
        for rev in revs:
            # Get a short description of the line
            desc = line.strip()[:100]
            en_para_revs[rev] = desc
    
    cn_para_revs = set(re.findall(r'r(\d{5,6})', cn_text))
    
    missing_para_revs = set(en_para_revs.keys()) - cn_para_revs
    if missing_para_revs:
        print(f"  Paragraphs with these revision refs are missing:")
        for rev in sorted(missing_para_revs):
            desc = en_para_revs[rev]
            print(f"    - r{rev}: {desc[:80]}...")
            issues.append(f"缺失段落 (r{rev}): {desc[:80]}")
    
    return issues


def main():
    all_issues = {}
    
    for file_info in FILES:
        issues = compare_file(file_info)
        all_issues[file_info["version"]] = issues
    
    # Print summary
    print(f"\n\n{'='*60}")
    print(f"SUMMARY OF MISSING CONTENT")
    print(f"{'='*60}")
    
    for version, issues in all_issues.items():
        print(f"\n=== FreeBSD {version} ===")
        if issues:
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"  No missing content detected")
    
    # Write report to file
    report_path = os.path.join(os.path.dirname(FILES[0]["cn"]), "comparison_report.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("FreeBSD 发行说明中文翻译完整性对比报告\n")
        f.write("="*60 + "\n\n")
        for version, issues in all_issues.items():
            f.write(f"=== FreeBSD {version} ===\n")
            if issues:
                for issue in issues:
                    f.write(f"  - {issue}\n")
            else:
                f.write("  未检测到缺失内容\n")
            f.write("\n")
    
    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()

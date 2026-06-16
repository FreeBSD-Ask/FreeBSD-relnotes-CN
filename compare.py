#!/usr/bin/env python3
"""Compare Chinese translations with English originals for FreeBSD 6.x release notes."""

import urllib.request
import re
import os

files = [
    {
        "cn": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\6.0-amd64.md",
        "en_url": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/6.0R/relnotes-amd64.adoc",
        "version": "6.0",
    },
    {
        "cn": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\6.1-amd64.md",
        "en_url": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/6.1R/relnotes-amd64.adoc",
        "version": "6.1",
    },
    {
        "cn": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\6.2-amd64.md",
        "en_url": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/6.2R/relnotes-amd64.adoc",
        "version": "6.2",
    },
    {
        "cn": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\6.3-amd64.md",
        "en_url": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/6.3R/relnotes-amd64.adoc",
        "version": "6.3",
    },
    {
        "cn": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\6.4-amd64.md",
        "en_url": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/6.4R/relnotes-amd64.adoc",
        "version": "6.4",
    },
]


def extract_en_sections(html_text):
    """Extract sections and key content items from the English HTML source."""
    sections = {}
    current_section = "header"
    items = []

    # Remove HTML tags for text extraction but keep structure
    # Split by h2/h3 headers
    lines = html_text.split('\n')

    # Extract all h2 and h3 section headers and their content
    # The HTML uses <h2>, <h3> etc.
    h2_pattern = re.compile(r'<h2[^>]*>(.*?)</h2>', re.DOTALL)
    h3_pattern = re.compile(r'<h3[^>]*>(.*?)</h3>', re.DOTALL)
    h4_pattern = re.compile(r'<h4[^>]*>(.*?)</h4>', re.DOTALL)

    # Find all section headers with their positions
    all_headers = []
    for m in h2_pattern.finditer(html_text):
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        all_headers.append((m.start(), 2, title))
    for m in h3_pattern.finditer(html_text):
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        all_headers.append((m.start(), 3, title))
    for m in h4_pattern.finditer(html_text):
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        all_headers.append((m.start(), 4, title))

    all_headers.sort(key=lambda x: x[0])

    # Extract paragraphs (items between <p> tags)
    p_pattern = re.compile(r'<p>(.*?)</p>', re.DOTALL)
    paragraphs = []
    for m in p_pattern.finditer(html_text):
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if text:
            paragraphs.append((m.start(), text))

    # Extract list items
    li_pattern = re.compile(r'<li>(.*?)</li>', re.DOTALL)
    list_items = []
    for m in li_pattern.finditer(html_text):
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if text:
            list_items.append((m.start(), text))

    # Extract code blocks
    pre_pattern = re.compile(r'<pre[^>]*>(.*?)</pre>', re.DOTALL)
    code_blocks = []
    for m in pre_pattern.finditer(html_text):
        text = m.group(1).strip()
        if text:
            code_blocks.append((m.start(), text))

    # Extract table rows
    tr_pattern = re.compile(r'<tr[^>]*>(.*?)</tr>', re.DOTALL)
    tables = []
    for m in tr_pattern.finditer(html_text):
        text = re.sub(r'<[^>]+>', ' | ', m.group(1)).strip()
        if text and ' | ' in text:
            tables.append((m.start(), text))

    return {
        "headers": all_headers,
        "paragraphs": paragraphs,
        "list_items": list_items,
        "code_blocks": code_blocks,
        "tables": tables,
    }


def extract_cn_structure(md_text):
    """Extract structure from Chinese markdown."""
    headers = []
    code_blocks = []
    tables = []
    list_items = []

    for i, line in enumerate(md_text.split('\n')):
        line_stripped = line.strip()
        if line_stripped.startswith('#'):
            level = len(line_stripped.split(' ')[0])
            title = line_stripped.lstrip('#').strip()
            headers.append((i, level, title))
        elif line_stripped.startswith('```'):
            # Find end of code block
            pass
        elif line_stripped.startswith('|') and '|' in line_stripped[1:]:
            tables.append((i, line_stripped))
        elif line_stripped.startswith('- ') or re.match(r'^\d+\.', line_stripped):
            list_items.append((i, line_stripped))

    # Extract code blocks
    in_code = False
    code_start = 0
    code_content = []
    for i, line in enumerate(md_text.split('\n')):
        if line.strip().startswith('```'):
            if in_code:
                code_blocks.append((code_start, '\n'.join(code_content)))
                code_content = []
                in_code = False
            else:
                in_code = True
                code_start = i
                code_content = []

    return {
        "headers": headers,
        "code_blocks": code_blocks,
        "tables": tables,
        "list_items": list_items,
    }


def find_key_terms_in_en(en_text):
    """Find key technical terms, driver names, advisory IDs in English text."""
    # Security advisories
    advisories = re.findall(r'FreeBSD-SA-\d{2}:\d{2}\.\w+', en_text)
    # Errata notices
    errata = re.findall(r'FreeBSD-EN-\d{2}:\d{2}\.\w+', en_text)
    # Driver names like xxx(4)
    drivers = re.findall(r'\w+\(\d+\)', en_text)
    # Kernel options
    options = re.findall(r'options\s+\w+', en_text)
    # sysctl variables
    sysctls = re.findall(r'[a-z][a-z0-9._]+(?:_allowed|_enabled|_flags|_time|_cps|_thresh|_debug|_rate|_requests|_on_failure)', en_text)

    return {
        "advisories": sorted(set(advisories)),
        "errata": sorted(set(errata)),
        "drivers": sorted(set(drivers)),
    }


def find_key_terms_in_cn(cn_text):
    """Find key technical terms in Chinese text."""
    advisories = re.findall(r'FreeBSD-SA-\d{2}:\d{2}\.\w+', cn_text)
    errata = re.findall(r'FreeBSD-EN-\d{2}:\d{2}\.\w+', cn_text)
    drivers = re.findall(r'\w+\(\d+\)', cn_text)

    return {
        "advisories": sorted(set(advisories)),
        "errata": sorted(set(errata)),
        "drivers": sorted(set(drivers)),
    }


def compare_file(file_info):
    """Compare one Chinese translation with its English original."""
    version = file_info["version"]
    cn_path = file_info["cn"]
    en_url = file_info["en_url"]

    print(f"\n{'='*80}")
    print(f"Comparing FreeBSD {version}-RELEASE amd64")
    print(f"{'='*80}")

    # Fetch English
    try:
        req = urllib.request.Request(en_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            en_text = resp.read().decode('utf-8')
    except Exception as e:
        print(f"  ERROR fetching English source: {e}")
        return

    # Read Chinese
    try:
        with open(cn_path, 'r', encoding='utf-8') as f:
            cn_text = f.read()
    except Exception as e:
        print(f"  ERROR reading Chinese file: {e}")
        return

    # Extract key terms
    en_terms = find_key_terms_in_en(en_text)
    cn_terms = find_key_terms_in_cn(cn_text)

    # Compare security advisories
    en_adv = set(en_terms["advisories"])
    cn_adv = set(cn_terms["advisories"])
    missing_adv = en_adv - cn_adv
    extra_adv = cn_adv - en_adv

    if missing_adv:
        print(f"\n  [缺失安全公告] ({len(missing_adv)}):")
        for a in sorted(missing_adv):
            print(f"    - {a}")
    else:
        print(f"\n  [安全公告] 全部存在 ({len(en_adv)} 个)")

    if extra_adv:
        print(f"  [多余安全公告] ({len(extra_adv)}):")
        for a in sorted(extra_adv):
            print(f"    - {a}")

    # Compare errata notices
    en_err = set(en_terms["errata"])
    cn_err = set(cn_terms["errata"])
    missing_err = en_err - cn_err

    if missing_err:
        print(f"\n  [缺失勘误通知] ({len(missing_err)}):")
        for a in sorted(missing_err):
            print(f"    - {a}")
    elif en_err:
        print(f"\n  [勘误通知] 全部存在 ({len(en_err)} 个)")

    # Compare driver references
    en_drv = set(en_terms["drivers"])
    cn_drv = set(cn_terms["drivers"])
    missing_drv = en_drv - cn_drv

    if missing_drv:
        print(f"\n  [缺失驱动/手册页引用] ({len(missing_drv)}):")
        for d in sorted(missing_drv):
            print(f"    - {d}")

    # Extract English section headers
    en_headers = []
    for m in re.finditer(r'<h[234][^>]*>(.*?)</h[234]>', en_text, re.DOTALL):
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        level = int(re.search(r'<h(\d)', en_text[m.start():m.start()+4]).group(1))
        en_headers.append((level, title))

    # Extract Chinese section headers
    cn_headers = []
    for line in cn_text.split('\n'):
        line_s = line.strip()
        if line_s.startswith('#'):
            level = len(line_s.split(' ')[0])
            title = line_s.lstrip('#').strip()
            cn_headers.append((level, title))

    # Map English headers to expected Chinese headers
    # Section mapping (English -> Chinese patterns)
    header_map = {
        "Introduction": "引",
        "What's New": "新",
        "Security Advisories": "安全公告",
        "Kernel Changes": "内核变更",
        "Boot Loader Changes": "引导",
        "Hardware Support": "硬件支持",
        "Multimedia Support": "多媒体",
        "Network Interface Support": "网络接口",
        "Network Protocols": "网络协议",
        "Disks and Storage": "磁盘",
        "File Systems": "文件系统",
        "Third-Party Software": "第三方",
        "Userland Changes": "用户空间",
        "/etc/rc.d Scripts": "rc.d",
        "Ports and Packages": "Ports",
        "Release Engineering and Integration": "发行工程",
        "Documentation": "文档",
        "Upgrading from": "升级",
    }

    # Check for missing sections
    print(f"\n  [章节结构对比]")
    for level, title in en_headers:
        found = False
        for en_key, cn_key in header_map.items():
            if en_key.lower() in title.lower():
                # Check if Chinese has a matching header
                for cl, ct in cn_headers:
                    if cn_key in ct:
                        found = True
                        break
                break
        if not found and any(k.lower() in title.lower() for k in header_map):
            print(f"    可能缺失章节: H{level} - {title}")

    # Check for paragraphs by looking for distinctive content
    # Extract all <p> blocks from English
    en_paragraphs = []
    for m in re.finditer(r'<p>(.*?)</p>', en_text, re.DOTALL):
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if len(text) > 50:  # Only substantial paragraphs
            en_paragraphs.append(text)

    # Check for specific content items that should be in Chinese
    # Look for distinctive phrases/keywords from English paragraphs
    missing_content = []

    # Check for code blocks
    en_code_blocks = []
    for m in re.finditer(r'<pre[^>]*>(.*?)</pre>', en_text, re.DOTALL):
        text = m.group(1).strip()
        if text:
            en_code_blocks.append(text)

    cn_code_blocks = []
    in_code = False
    code_content = []
    for line in cn_text.split('\n'):
        if line.strip().startswith('```'):
            if in_code:
                cn_code_blocks.append('\n'.join(code_content))
                code_content = []
                in_code = False
            else:
                in_code = True
                code_content = []
        elif in_code:
            code_content.append(line)

    # Check if English code blocks exist in Chinese
    for i, en_code in enumerate(en_code_blocks):
        # Normalize whitespace for comparison
        en_normalized = re.sub(r'\s+', ' ', en_code).strip()
        found = False
        for cn_code in cn_code_blocks:
            cn_normalized = re.sub(r'\s+', ' ', cn_code).strip()
            if en_normalized in cn_normalized or cn_normalized in en_normalized:
                found = True
                break
            # Check if key lines match
            en_lines = set(l.strip() for l in en_code.split('\n') if l.strip())
            cn_lines = set(l.strip() for l in cn_code.split('\n') if l.strip())
            if en_lines and en_lines.issubset(cn_lines):
                found = True
                break
        if not found and en_normalized:
            # Check if the code block content appears anywhere in Chinese text
            first_line = en_code.strip().split('\n')[0].strip() if en_code.strip() else ""
            if first_line and first_line not in cn_text:
                missing_content.append(("code_block", first_line[:100]))

    if missing_content:
        print(f"\n  [可能缺失的代码块]:")
        for typ, content in missing_content:
            print(f"    - {content}")

    # Check for table entries (especially security advisory tables in 6.4)
    en_table_rows = []
    for m in re.finditer(r'<tr[^>]*>(.*?)</tr>', en_text, re.DOTALL):
        cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', m.group(1), re.DOTALL)
        if cells:
            row_text = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
            en_table_rows.append(row_text)

    # Check Chinese tables
    cn_table_rows = []
    for line in cn_text.split('\n'):
        if line.strip().startswith('|') and not line.strip().startswith('| :-') and not line.strip().startswith('|---'):
            cells = [c.strip() for c in line.strip().split('|')[1:-1]]
            if cells:
                cn_table_rows.append(cells)

    # Compare table row counts
    if en_table_rows:
        print(f"\n  [表格对比] 英文表格行数: {len(en_table_rows)}, 中文表格行数: {len(cn_table_rows)}")
        if len(en_table_rows) > len(cn_table_rows):
            print(f"    中文可能缺失 {len(en_table_rows) - len(cn_table_rows)} 行表格数据")
            # Find which rows are missing
            for en_row in en_table_rows:
                found = False
                for cn_row in cn_table_rows:
                    # Check if any cell content matches
                    for en_cell in en_row:
                        for cn_cell in cn_row:
                            if en_cell and cn_cell and (en_cell in cn_cell or cn_cell in en_cell):
                                found = True
                                break
                        if found:
                            break
                    if found:
                        break
                if not found and any(c for c in en_row if len(c) > 3):
                    print(f"    可能缺失行: {' | '.join(en_row)}")

    # Detailed paragraph-level comparison
    # Extract distinctive keywords from English paragraphs and check Chinese
    en_key_phrases = []
    for p in en_paragraphs:
        # Extract distinctive technical terms
        # Look for driver names, tool names, specific features
        drivers_in_p = re.findall(r'(\w+)\(\d+\)', p)
        for d in drivers_in_p:
            if d not in [x for x in en_key_phrases]:
                en_key_phrases.append(d)

    cn_text_lower = cn_text.lower()
    missing_drivers_in_text = []
    for d in en_key_phrases:
        if d.lower() not in cn_text_lower and len(d) > 2:
            missing_drivers_in_text.append(d)

    if missing_drivers_in_text:
        # Filter out common false positives
        real_missing = [d for d in missing_drivers_in_text
                       if d not in ['class', 'span', 'div', 'table', 'thead',
                                   'tbody', 'tr', 'td', 'th', 'href', 'http',
                                   'aen', 'p', 'ul', 'li', 'pre', 'code',
                                   'em', 'strong', 'br', 'hr', 'img']]
        if real_missing:
            print(f"\n  [正文中可能缺失的驱动/工具引用] ({len(real_missing)}):")
            for d in sorted(set(real_missing)):
                print(f"    - {d}")

    # Check for specific sections that exist in English but might be empty in Chinese
    # Look for empty sections in Chinese
    cn_lines = cn_text.split('\n')
    for i, line in enumerate(cn_lines):
        if line.strip().startswith('#'):
            # Check if next non-empty line is also a header
            j = i + 1
            while j < len(cn_lines) and cn_lines[j].strip() == '':
                j += 1
            if j < len(cn_lines) and cn_lines[j].strip().startswith('#'):
                print(f"  [空章节] 第 {i+1} 行: {line.strip()} (下一行是另一个标题，无内容)")

    return {
        "version": version,
        "missing_advisories": missing_adv if missing_adv else set(),
        "missing_errata": missing_err if missing_err else set(),
        "missing_drivers": missing_drv if missing_drv else set(),
    }


# Run comparisons
results = []
for f in files:
    try:
        result = compare_file(f)
        if result:
            results.append(result)
    except Exception as e:
        print(f"Error processing {f['version']}: {e}")

print(f"\n\n{'='*80}")
print("总结")
print(f"{'='*80}")
for r in results:
    print(f"\nFreeBSD {r['version']}-RELEASE:")
    if r['missing_advisories']:
        print(f"  缺失安全公告: {', '.join(sorted(r['missing_advisories']))}")
    else:
        print(f"  安全公告: 完整")
    if r['missing_errata']:
        print(f"  缺失勘误通知: {', '.join(sorted(r['missing_errata']))}")
    if r['missing_drivers']:
        print(f"  缺失驱动引用: {', '.join(sorted(r['missing_drivers']))}")

#!/usr/bin/env python3
"""Item-by-item comparison: match EN paragraphs to CN paragraphs by key identifiers."""
import re, os, html

BASE = r"C:\Users\ykla\Documents\FreeBSD-relnotes-CN"

def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def clean_html(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def extract_en_items(en_text):
    """Extract individual change items from English HTML."""
    parts = en_text.split('++++')
    html_part = parts[1] if len(parts) > 1 else en_text

    items = []
    # Extract <p> paragraphs
    paras = re.findall(r'<p[^>]*>(.*?)</p>', html_part, re.DOTALL)
    for p in paras:
        text = clean_html(p)
        if text and len(text) > 20:
            items.append(text)

    # Also extract <li> items
    lis = re.findall(r'<li[^>]*>\s*<p[^>]*>(.*?)</p>', html_part, re.DOTALL)
    for li in lis:
        text = clean_html(li)
        if text and len(text) > 20 and text not in items:
            items.append(text)

    return items

def extract_cn_items(cn_text):
    """Extract individual change items from Chinese Markdown."""
    items = []
    for line in cn_text.split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith('#') or stripped.startswith('|') or stripped.startswith('```') or stripped.startswith('---') or stripped.startswith('>'):
            continue
        if len(stripped) > 20:
            items.append(stripped)
    return items

def get_item_fingerprint(text):
    """Get a fingerprint of key identifiers from an item."""
    fp = set()

    # Man page references: foo(4)
    fp.update(re.findall(r'\b\w+\(\d+\)', text))

    # Driver names in man page links
    fp.update(re.findall(r'query=(\w+)&', text))

    # sysctl-like variables
    sysctls = re.findall(r'\b[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*){2,}', text)
    fp.update(s for s in sysctls if not any(x in s for x in ['.html', '.org', '.com', 'www.', 'http']))

    # Specific technical terms (version numbers, protocol names, etc.)
    fp.update(re.findall(r'\b\d+\.\d+\.\d+\b', text))  # Version numbers
    fp.update(re.findall(r'SA-\d{2}:\d{2}\.\w+', text))  # Security advisories
    fp.update(re.findall(r'\bRFC\s*\d+\b', text))  # RFC references

    # Specific driver/hardware names
    fp.update(re.findall(r'\b[A-Z][A-Z0-9]+\b', text))  # Acronyms

    # File paths
    fp.update(re.findall(r'/[a-zA-Z][a-zA-Z0-9_./-]+', text))

    return fp

def match_items(en_items, cn_items):
    """Match EN items to CN items and find missing ones."""
    missing = []
    matched = []

    for en_item in en_items:
        en_fp = get_item_fingerprint(en_item)

        if not en_fp:
            # No key identifiers, skip (likely generic text)
            continue

        best_match = None
        best_overlap = 0

        for cn_item in cn_items:
            cn_fp = get_item_fingerprint(cn_item)
            overlap = len(en_fp & cn_fp)

            if overlap > best_overlap:
                best_overlap = overlap
                best_match = cn_item

        # Require at least 2 matching identifiers or 40% overlap
        min_required = max(2, len(en_fp) * 0.3)

        if best_overlap >= min_required:
            matched.append((en_item, best_match, best_overlap))
        else:
            missing.append((en_item, en_fp, best_overlap))

    return matched, missing

def compare_file(ver, en_file, cn_file):
    en = read(en_file)
    cn = read(cn_file)

    print(f"\n{'='*60}")
    print(f"=== FreeBSD {ver}-RELEASE 逐项比对 ===")
    print(f"{'='*60}")

    en_items = extract_en_items(en)
    cn_items = extract_cn_items(cn)

    print(f"\n英文条目数: {len(en_items)}")
    print(f"中文条目数: {len(cn_items)}")

    matched, missing = match_items(en_items, cn_items)

    print(f"匹配条目数: {len(matched)}")
    print(f"可能缺失条目数: {len(missing)}")

    if missing:
        print(f"\n❌ 以下英文条目在中文翻译中可能缺失:\n")
        for i, (en_item, en_fp, overlap) in enumerate(missing):
            preview = en_item[:150] + "..." if len(en_item) > 150 else en_item
            print(f"  缺失 #{i+1}:")
            print(f"    内容: {preview}")
            print(f"    关键标识: {', '.join(sorted(en_fp)[:10])}")
            print()

    # Also check for specific items
    print(f"\n--- 特定项目检查 ---")

    # Microsoft trademark
    if 'Microsoft, IntelliMouse, MS-DOS' in en:
        if 'Microsoft' in cn or '微软' in cn:
            print(f"  ✅ Microsoft 商标声明存在")
        else:
            print(f"  ❌ Microsoft 商标声明缺失")

    # Check for 2.5/2.6/2.7 sections
    en_has_ports = 'Ports' in en or 'packages' in en.lower()
    cn_has_ports = 'Ports' in cn or '软件包' in cn or '端口' in cn
    if en_has_ports:
        if cn_has_ports:
            print(f"  ✅ Ports/软件包相关内容存在")
        else:
            print(f"  ❌ Ports/软件包相关内容可能缺失")

    # Check for release engineering section
    en_has_re = 'Release Engineering' in en or 'release engineering' in en.lower()
    cn_has_re = '发布工程' in cn or '版本工程' in cn
    if en_has_re:
        if cn_has_re:
            print(f"  ✅ 发布工程章节存在")
        else:
            print(f"  ❌ 发布工程章节可能缺失")

    # Check for documentation section
    en_has_doc = 'Documentation' in en and re.search(r'2\.\s*7\s+Documentation|2\.\s*5\s+Documentation', en)
    cn_has_doc = '文档' in cn
    if en_has_doc:
        if cn_has_doc:
            print(f"  ✅ 文档章节存在")
        else:
            print(f"  ❌ 文档章节可能缺失")

# Run comparisons
compare_file('7.0', os.path.join(BASE, 'en_7.0.txt'), os.path.join(BASE, '7.0.md'))
compare_file('7.1', os.path.join(BASE, 'en_7.1.txt'), os.path.join(BASE, '7.1.md'))
compare_file('7.2', os.path.join(BASE, 'en_7.2_detailed.txt'), os.path.join(BASE, '7.2.md'))
compare_file('7.4', os.path.join(BASE, 'en_7.4.txt'), os.path.join(BASE, '7.4.md'))

print("\n\n" + "="*60)
print("比对完成")

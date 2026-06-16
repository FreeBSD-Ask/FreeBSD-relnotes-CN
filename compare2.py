#!/usr/bin/env python3
"""Detailed paragraph-level comparison of Chinese translations vs English originals."""
import re, os, html

BASE = r"C:\Users\ykla\Documents\FreeBSD-relnotes-CN"

def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def clean_html(s):
    """Remove HTML tags and decode entities."""
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def extract_en_paragraphs(html_content):
    """Extract paragraphs from English HTML, preserving structure."""
    # Get content between ++++ markers (the HTML part)
    parts = html_content.split('++++')
    if len(parts) > 1:
        html_part = parts[1] if len(parts) == 2 else parts[-2]
    else:
        html_part = html_content

    paragraphs = []
    # Extract <p> tags
    raw_paras = re.findall(r'<p[^>]*>(.*?)</p>', html_part, re.DOTALL)
    for p in raw_paras:
        text = clean_html(p)
        if text and len(text) > 15:
            paragraphs.append(text)

    # Also extract <li> items
    raw_lis = re.findall(r'<li[^>]*>(.*?)</li>', html_part, re.DOTALL)
    for li in raw_lis:
        text = clean_html(li)
        if text and len(text) > 15:
            paragraphs.append(text)

    return paragraphs

def extract_key_identifiers(text):
    """Extract key technical identifiers from text that should appear in translation."""
    ids = set()

    # Man page references like foo(4)
    ids.update(re.findall(r'\b\w+\(\d+\)', text))

    # sysctl-like variables (at least 2 dots)
    sysctls = re.findall(r'\b[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*){2,}', text)
    ids.update(s for s in sysctls if not any(x in s for x in ['.html', '.org', '.com', 'www.', 'http']))

    # Security advisory IDs
    ids.update(re.findall(r'SA-\d{2}:\d{2}\.\w+', text))

    # Kernel options (all caps with underscores, min 4 chars)
    kopts = re.findall(r'\b[A-Z][A-Z0-9_]{3,}\b', text)
    # Filter common English words
    common_words = {
        'THE', 'AND', 'FOR', 'NOT', 'THIS', 'THAT', 'WITH', 'FROM', 'HAVE', 'BEEN',
        'WHICH', 'WOULD', 'THEIR', 'THERE', 'WILL', 'EACH', 'LIKE', 'LONG', 'LOOK',
        'MANY', 'MORE', 'SOME', 'THAN', 'BEFORE', 'AFTER', 'BECAUSE', 'BETWEEN',
        'ABOUT', 'SINCE', 'INTO', 'ALSO', 'OVER', 'SUCH', 'FIRST', 'WHERE', 'THESE',
        'THOSE', 'OTHER', 'ONLY', 'THEN', 'WHEN', 'WHAT', 'YOUR', 'SHOULD', 'BELOW',
        'ABOVE', 'UNDER', 'NEED', 'BEING', 'NOTE', 'TRUE', 'FALSE', 'NULL', 'DEFAULT',
        'VALUE', 'KERNEL', 'SYSTEM', 'DRIVER', 'SUPPORT', 'ENABLED', 'DISABLED',
        'REMOVED', 'ADDED', 'CHANGED', 'UPDATED', 'FIXED', 'REPLACED', 'MERGED',
        'FREEBSD', 'RELEASE', 'STABLE', 'CURRENT', 'BRANCH', 'VERSION', 'UPDATE',
        'ALSO', 'NOTE', 'WHEN', 'WHERE', 'WHICH', 'THAN', 'THEN', 'THESE', 'THOSE',
        'BEEN', 'BEING', 'HAVE', 'WERE', 'WILL', 'WOULD', 'COULD', 'SHOULD', 'MUST',
        'MAY', 'MIGHT', 'SHALL', 'SOME', 'MOST', 'VERY', 'EVEN', 'JUST', 'ONLY',
        'ALREADY', 'STILL', 'YET', 'NEVER', 'ALWAYS', 'OFTEN', 'RARELY', 'USUALLY',
        'HOWEVER', 'THEREFORE', 'MOREOVER', 'FURTHERMORE', 'NEVERTHELESS', 'NONETHELESS',
        'MEANWHILE', 'OTHERWISE', 'INSTEAD', 'ACCORDINGLY', 'CONSEQUENTLY',
    }
    ids.update(k for k in kopts if k not in common_words and len(k) >= 5)

    # File paths like /etc/foo, /usr/bar
    ids.update(re.findall(r'/[a-zA-Z][a-zA-Z0-9_./-]+', text))

    # Version numbers like 9.4.2, 2.6.16
    ids.update(re.findall(r'\b\d+\.\d+\.\d+\b', text))

    return ids

def compare_file_detailed(ver, en_file, cn_file):
    """Do detailed paragraph-level comparison."""
    en = read(en_file)
    cn = read(cn_file)

    print(f"\n{'='*60}")
    print(f"=== FreeBSD {ver}-RELEASE 详细段落比对 ===")
    print(f"{'='*60}")

    # Extract paragraphs from English
    en_paras = extract_en_paragraphs(en)
    print(f"\n英文段落总数: {len(en_paras)}")

    # For each English paragraph, check if key identifiers appear in Chinese
    missing_items = []
    for i, para in enumerate(en_paras):
        ids = extract_key_identifiers(para)
        if not ids:
            continue

        # Check which identifiers are missing from Chinese
        missing_ids = []
        for id_val in ids:
            if id_val not in cn:
                missing_ids.append(id_val)

        if missing_ids:
            # Get a short preview of the paragraph
            preview = para[:120] + "..." if len(para) > 120 else para
            missing_items.append({
                'para_num': i,
                'preview': preview,
                'missing_ids': missing_ids,
                'all_ids': sorted(ids),
            })

    if missing_items:
        print(f"\n❌ 发现 {len(missing_items)} 个段落可能存在缺失内容:\n")
        for item in missing_items:
            print(f"  段落 #{item['para_num']}:")
            print(f"    预览: {item['preview']}")
            print(f"    缺失标识符: {', '.join(item['missing_ids'])}")
            print()
    else:
        print(f"\n✅ 所有关键内容均已翻译")

    # Also check for specific items that should be in the translation
    # Check Microsoft trademark (7.0 and 7.2 have it)
    if 'Microsoft' in en and 'Microsoft' not in cn and '微软' not in cn:
        print(f"  ⚠️  英文原文包含 Microsoft 商标声明，中文翻译中未找到")

    # Check for specific section counts
    # Count how many <p> paragraphs are in each section of EN
    en_section_paras = {}
    current_section = "header"
    for line in en.split('\n'):
        h2_match = re.search(r'<h2[^>]*>(.*?)</h2>', line)
        h3_match = re.search(r'<h3[^>]*>(.*?)</h3>', line)
        if h2_match:
            current_section = clean_html(h2_match.group(1))
        elif h3_match:
            current_section = clean_html(h3_match.group(1))

    # Count paragraphs per section in English
    parts = en.split('++++')
    html_part = parts[1] if len(parts) > 1 else en

    # Split by h2/h3 to count paragraphs per section
    section_splits = re.split(r'<h[23][^>]*>(.*?)</h[23]>', html_part)
    en_section_counts = {}
    current = "header"
    for i, part in enumerate(section_splits):
        if i % 2 == 1:  # This is a header
            current = clean_html(part)
        else:
            p_count = len(re.findall(r'<p[^>]*>', part))
            if p_count > 0:
                en_section_counts[current] = en_section_counts.get(current, 0) + p_count

    print(f"\n--- 英文各章节段落数 ---")
    for sec, count in en_section_counts.items():
        print(f"  {sec}: {count} 段")

# Run comparisons
# 7.0: en_7.0.txt is the detailed version
compare_file_detailed('7.0', os.path.join(BASE, 'en_7.0.txt'), os.path.join(BASE, '7.0.md'))

# 7.1: en_7.1.txt is the detailed version
compare_file_detailed('7.1', os.path.join(BASE, 'en_7.1.txt'), os.path.join(BASE, '7.1.md'))

# 7.2: Use the detailed version
compare_file_detailed('7.2', os.path.join(BASE, 'en_7.2_detailed.txt'), os.path.join(BASE, '7.2.md'))

# 7.4: en_7.4.txt is the detailed version
compare_file_detailed('7.4', os.path.join(BASE, 'en_7.4.txt'), os.path.join(BASE, '7.4.md'))

print("\n\n" + "="*60)
print("详细比对完成")

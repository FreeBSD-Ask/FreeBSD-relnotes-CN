#!/usr/bin/env python3
"""Focused comparison: paragraph counts per section, specific missing items."""
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

def analyze_en(en_text):
    """Analyze English HTML source - extract sections and paragraph counts."""
    parts = en_text.split('++++')
    html_part = parts[1] if len(parts) > 1 else en_text

    sections = []
    current_section = "Header"
    current_paras = []

    # Split by h2/h3/h4 tags
    tokens = re.split(r'(<h[234][^>]*>.*?</h[234]>)', html_part)

    for token in tokens:
        h_match = re.match(r'<h([234])[^>]*>(.*?)</h[1234]>', token)
        if h_match:
            # Save previous section
            if current_paras:
                sections.append((current_section, current_paras))
            current_section = clean_html(h_match.group(2))
            current_paras = []
        else:
            # Extract paragraphs
            paras = re.findall(r'<p[^>]*>(.*?)</p>', token, re.DOTALL)
            for p in paras:
                text = clean_html(p)
                if text and len(text) > 10:
                    current_paras.append(text)
            # Also extract list items
            lis = re.findall(r'<li[^>]*>(.*?)</li>', token, re.DOTALL)
            for li in lis:
                text = clean_html(li)
                if text and len(text) > 10:
                    current_paras.append(text)

    if current_paras:
        sections.append((current_section, current_paras))

    return sections

def analyze_cn(cn_text):
    """Analyze Chinese Markdown source - extract sections and paragraph counts."""
    sections = []
    current_section = "Header"
    current_paras = []

    for line in cn_text.split('\n'):
        stripped = line.strip()
        # Check for heading
        h_match = re.match(r'^(#{1,5})\s+(.+)$', stripped)
        if h_match:
            if current_paras:
                sections.append((current_section, current_paras))
            current_section = stripped.lstrip('#').strip()
            current_paras = []
        elif stripped and not stripped.startswith('|') and not stripped.startswith('```') and not stripped.startswith('---') and not stripped.startswith('>'):
            # Regular paragraph or list item
            if stripped.startswith('- ') or stripped.startswith('* '):
                current_paras.append(stripped)
            elif len(stripped) > 10:
                current_paras.append(stripped)

    if current_paras:
        sections.append((current_section, current_paras))

    return sections

def check_specific_items(ver, en_text, cn_text):
    """Check for specific known items that might be missing."""
    issues = []

    # 1. Microsoft trademark notice
    if 'Microsoft, IntelliMouse, MS-DOS' in en_text:
        if 'Microsoft' not in cn_text and '微软' not in cn_text:
            issues.append("❌ 缺失 Microsoft 商标声明段落")
        else:
            issues.append("✅ Microsoft 商标声明存在")

    # 2. Check for errata notice
    if 'errata' in en_text.lower():
        if '勘误' in cn_text or '错误文档' in cn_text or 'errata' in cn_text.lower():
            issues.append("✅ 勘误/errata 相关内容存在")
        else:
            issues.append("❌ 可能缺失勘误/errata 相关内容")

    # 3. Check for "all users" warning
    if 'All users are encouraged' in en_text or 'all users' in en_text.lower():
        if '所有用户' in cn_text or '建议所有用户' in cn_text:
            issues.append("✅ '所有用户' 警告存在")
        else:
            issues.append("❌ 可能缺失 '所有用户' 警告")

    # 4. Check for upgrade section
    if 'Upgrading from previous' in en_text:
        if '升级' in cn_text:
            issues.append("✅ 升级章节存在")
        else:
            issues.append("❌ 可能缺失升级章节")

    # 5. Check for important/warning blocks
    en_importants = len(re.findall(r'<div class="IMPORTANT"', en_text))
    cn_importants = cn_text.count('重要')
    if en_importants > 0:
        if cn_importants >= en_importants:
            issues.append(f"✅ 重要提示块: 英文 {en_importants}, 中文 {cn_importants}")
        else:
            issues.append(f"❌ 重要提示块可能缺失: 英文 {en_importants}, 中文 {cn_importants}")

    # 6. Check for table entries (security advisories)
    en_table_rows = len(re.findall(r'<tr>', en_text))
    cn_table_rows = cn_text.count('| [SA-')
    if en_table_rows > 3:  # Header rows
        sa_rows = en_table_rows - 2  # Subtract header rows
        if cn_table_rows >= sa_rows - 1:
            issues.append(f"✅ 安全公告表行数: 英文 ~{sa_rows}, 中文 {cn_table_rows}")
        else:
            issues.append(f"❌ 安全公告表行数不匹配: 英文 ~{sa_rows}, 中文 {cn_table_rows}")

    # 7. Check code blocks in detail
    en_code_blocks = re.findall(r'<pre class="PROGRAMLISTING">(.*?)</pre>', en_text, re.DOTALL)
    cn_code_blocks = re.findall(r'```[\w]*\n(.*?)```', cn_text, re.DOTALL)

    if en_code_blocks:
        issues.append(f"英文代码块: {len(en_code_blocks)} 个, 中文代码块: {len(cn_code_blocks)} 个")
        for i, en_block in enumerate(en_code_blocks):
            en_clean = clean_html(en_block).strip()
            # Check if this code block content exists in Chinese
            # Extract key identifiers
            en_ids = set(re.findall(r'[a-zA-Z_]\w*', en_clean))
            found = False
            for cn_block in cn_code_blocks:
                cn_clean = cn_block.strip()
                cn_ids = set(re.findall(r'[a-zA-Z_]\w*', cn_clean))
                overlap = en_ids & cn_ids
                if len(overlap) > max(3, len(en_ids) * 0.4):
                    found = True
                    break
            if not found:
                issues.append(f"  ❌ 英文代码块 #{i+1} 可能缺失: {en_clean[:80]}...")
            else:
                issues.append(f"  ✅ 英文代码块 #{i+1} 已翻译")

    # 8. Check for specific driver entries that might be missing
    # Extract all driver names from English (foo(4) pattern in man page links)
    en_drivers = set(re.findall(r'query=(\w+)&', en_text))
    cn_drivers = set(re.findall(r'query=(\w+)&', cn_text))
    missing_drivers = en_drivers - cn_drivers
    if missing_drivers:
        issues.append(f"❌ 缺失驱动/工具手册页链接: {', '.join(sorted(missing_drivers))}")
    else:
        issues.append(f"✅ 所有驱动/工具手册页链接均存在")

    return issues

def compare_file(ver, en_file, cn_file):
    en = read(en_file)
    cn = read(cn_file)

    print(f"\n{'='*60}")
    print(f"=== FreeBSD {ver}-RELEASE 完整性比对 ===")
    print(f"{'='*60}")

    # Section-level comparison
    en_sections = analyze_en(en)
    cn_sections = analyze_cn(cn)

    print(f"\n--- 章节段落数对比 ---")
    print(f"{'英文章节':<50} {'EN':>4} {'CN':>4} {'状态':>6}")
    print("-" * 70)

    # Map EN section names to CN section names (approximate matching)
    for en_sec, en_paras in en_sections:
        en_count = len(en_paras)
        # Try to find matching CN section
        best_match = None
        best_count = 0
        for cn_sec, cn_paras in cn_sections:
            # Check if section names share key words
            en_words = set(re.findall(r'\w+', en_sec.lower()))
            cn_words = set(re.findall(r'[\w\u4e00-\u9fff]+', cn_sec.lower()))
            # Check for number match (like "2.1", "2.2")
            en_nums = re.findall(r'\d+\.\d+', en_sec)
            cn_nums = re.findall(r'\d+\.\d+', cn_sec)
            if en_nums and cn_nums and en_nums[0] == cn_nums[0]:
                best_match = cn_sec
                best_count = len(cn_paras)
                break
            # Check for keyword overlap
            en_key = set(w for w in en_words if len(w) > 3)
            if en_key & cn_words or (en_nums and str(en_nums[0]) in cn_sec):
                if len(cn_paras) > best_count:
                    best_match = cn_sec
                    best_count = len(cn_paras)

        if en_count > 0:  # Only show sections with content
            status = "✅" if best_count >= en_count * 0.8 else "⚠️" if best_count >= en_count * 0.5 else "❌"
            cn_name = best_match if best_match else "(未找到)"
            print(f"{en_sec:<50} {en_count:>4} {best_count:>4} {status:>6}")

    # Specific items check
    print(f"\n--- 具体项目检查 ---")
    issues = check_specific_items(ver, en, cn)
    for issue in issues:
        print(f"  {issue}")

# Run comparisons
compare_file('7.0', os.path.join(BASE, 'en_7.0.txt'), os.path.join(BASE, '7.0.md'))
compare_file('7.1', os.path.join(BASE, 'en_7.1.txt'), os.path.join(BASE, '7.1.md'))
compare_file('7.2', os.path.join(BASE, 'en_7.2_detailed.txt'), os.path.join(BASE, '7.2.md'))
compare_file('7.4', os.path.join(BASE, 'en_7.4.txt'), os.path.join(BASE, '7.4.md'))

print("\n\n" + "="*60)
print("比对完成")

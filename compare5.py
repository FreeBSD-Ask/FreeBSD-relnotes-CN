#!/usr/bin/env python3
"""Final precise comparison: extract each change item and match by primary identifier."""
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

def extract_en_change_items(en_text):
    """Extract individual change items from English HTML, with their primary identifier."""
    parts = en_text.split('++++')
    html_part = parts[1] if len(parts) > 1 else en_text

    items = []
    # Extract <p> paragraphs that describe changes
    paras = re.findall(r'<p[^>]*>(.*?)</p>', html_part, re.DOTALL)
    for p in paras:
        text = clean_html(p)
        if not text or len(text) < 20:
            continue

        # Skip header/footer paragraphs
        if any(skip in text for skip in [
            'Copyright', 'FreeBSD is a registered trademark',
            'IBM, AIX, EtherJet', 'IEEE, POSIX', 'Intel, Celeron',
            'Microsoft, IntelliMouse', 'Sparc, Sparc64',
            'Many of the designations', 'The release notes for FreeBSD',
            'This document contains the release notes',
            'This distribution of FreeBSD', 'This version of FreeBSD',
            'All users are encouraged', 'Typical release note items',
            'This section describes', 'Problems described in the following',
            'An up-to-date copy', 'More information on obtaining',
            'This file, and other', 'For questions about FreeBSD',
            'All users of FreeBSD', 'Questions about this document',
        ]):
            continue

        # Extract primary identifier
        primary_id = None

        # Check for man page reference (most common identifier)
        man_ref = re.search(r'(\w+)\((\d+)\)', text)
        if man_ref:
            primary_id = f"{man_ref.group(1)}({man_ref.group(2)})"

        # Check for SA advisory
        sa_ref = re.search(r'(SA-\d{2}:\d{2}\.\w+)', text)
        if sa_ref:
            primary_id = sa_ref.group(1)

        # Check for sysctl variable
        sysctl = re.search(r'([a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*){2,})', text)
        if sysctl and not primary_id:
            val = sysctl.group(1)
            if not any(x in val for x in ['.html', '.org', '.com', 'www.', 'http']):
                primary_id = val

        # Check for GEOM class
        geom = re.search(r'(GEOM_\w+)', text)
        if geom and not primary_id:
            primary_id = geom.group(1)

        # Check for platform tag
        plat = re.search(r'\[(amd64|i386|sparc64|powerpc|ia64|pc98|arm|sun4v)\]', text)
        if plat and not primary_id:
            primary_id = plat.group(0)

        # Check for specific software name
        sw_match = re.search(r'\b(BIND|GCC|OpenSSL|sendmail|OpenSSH|ncurses|less|bzip2|IPFilter|DRM|FICL|FILE|NTP|CVS|hostapd|PF|WPA|awk|gzip|netcat|tcsh|cpio|tzdata|libpcap|tcpdump|am-utils|libarchive|OpenPAM|GNOME|KDE|Xorg)\b', text)
        if sw_match and not primary_id:
            primary_id = sw_match.group(1)

        items.append({
            'text': text,
            'primary_id': primary_id,
            'all_man_refs': re.findall(r'(\w+)\((\d+)\)', text),
        })

    return items

def extract_cn_change_items(cn_text):
    """Extract individual change items from Chinese Markdown."""
    items = []
    for line in cn_text.split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith('#') or stripped.startswith('|') or stripped.startswith('```') or stripped.startswith('---') or stripped.startswith('>'):
            continue
        if len(stripped) < 20:
            continue

        # Skip header/footer paragraphs
        if any(skip in stripped for skip in [
            '版权', '注册商标', 'IBM', 'IEEE', 'Intel', 'Sparc',
            '商标', '发行说明包含', '本文档包含', '此版本', '此发行版',
            '建议所有用户', '典型的发行说明', '本节介绍', '以下安全',
            '勘误', '此文件', '有关 FreeBSD', '所有用户应订阅',
            '关于本文档',
        ]):
            continue

        # Extract primary identifier
        primary_id = None

        # Check for man page reference
        man_ref = re.search(r'(\w+)\((\d+)\)', stripped)
        if man_ref:
            primary_id = f"{man_ref.group(1)}({man_ref.group(2)})"

        # Check for SA advisory
        sa_ref = re.search(r'(SA-\d{2}:\d{2}\.\w+)', stripped)
        if sa_ref:
            primary_id = sa_ref.group(1)

        # Check for sysctl variable
        sysctl = re.search(r'([a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*){2,})', stripped)
        if sysctl and not primary_id:
            val = sysctl.group(1)
            if not any(x in val for x in ['.html', '.org', '.com', 'www.', 'http']):
                primary_id = val

        # Check for GEOM class
        geom = re.search(r'(GEOM_\w+)', stripped)
        if geom and not primary_id:
            primary_id = geom.group(1)

        # Check for platform tag
        plat = re.search(r'\[(amd64|i386|sparc64|powerpc|ia64|pc98|arm|sun4v)\]', stripped)
        if plat and not primary_id:
            primary_id = plat.group(0)

        # Check for specific software name
        sw_match = re.search(r'\b(BIND|GCC|OpenSSL|sendmail|OpenSSH|ncurses|less|bzip2|IPFilter|DRM|FICL|FILE|NTP|CVS|hostapd|PF|WPA|awk|gzip|netcat|tcsh|cpio|tzdata|libpcap|tcpdump|am-utils|libarchive|OpenPAM|GNOME|KDE|Xorg)\b', stripped)
        if sw_match and not primary_id:
            primary_id = sw_match.group(1)

        items.append({
            'text': stripped,
            'primary_id': primary_id,
            'all_man_refs': re.findall(r'(\w+)\((\d+)\)', stripped),
        })

    return items

def match_by_primary_id(en_items, cn_items):
    """Match EN items to CN items by primary identifier."""
    matched_en = set()
    matched_cn = set()
    missing = []

    for i, en_item in enumerate(en_items):
        pid = en_item['primary_id']
        if not pid:
            continue

        found = False
        for j, cn_item in enumerate(cn_items):
            if cn_item['primary_id'] == pid:
                found = True
                matched_en.add(i)
                matched_cn.add(j)
                break

        if not found:
            # Try matching by man page references
            for en_ref in en_item['all_man_refs']:
                for j, cn_item in enumerate(cn_items):
                    if en_ref in cn_item['all_man_refs']:
                        found = True
                        matched_en.add(i)
                        matched_cn.add(j)
                        break
                if found:
                    break

        if not found:
            missing.append(en_item)

    return missing, matched_en, matched_cn

def compare_file(ver, en_file, cn_file):
    en = read(en_file)
    cn = read(cn_file)

    print(f"\n{'='*60}")
    print(f"=== FreeBSD {ver}-RELEASE 精确比对 ===")
    print(f"{'='*60}")

    en_items = extract_en_change_items(en)
    cn_items = extract_cn_change_items(cn)

    print(f"\n英文变更条目数: {len(en_items)}")
    print(f"中文变更条目数: {len(cn_items)}")

    missing, matched_en, matched_cn = match_by_primary_id(en_items, cn_items)

    print(f"匹配条目数: {len(matched_en)}")
    print(f"可能缺失条目数: {len(missing)}")

    # Filter out items without primary_id (can't reliably match)
    missing_with_id = [m for m in missing if m['primary_id']]
    missing_no_id = [m for m in missing if not m['primary_id']]

    if missing_with_id:
        print(f"\n❌ 以下 {len(missing_with_id)} 个有明确标识符的条目在中文翻译中可能缺失:\n")
        for i, item in enumerate(missing_with_id):
            preview = item['text'][:120] + "..." if len(item['text']) > 120 else item['text']
            print(f"  缺失 #{i+1} [{item['primary_id']}]:")
            print(f"    {preview}")
            print()

    if missing_no_id:
        print(f"\n⚠️  另外 {len(missing_no_id)} 个无明确标识符的条目可能缺失（无法精确匹配）")

    # Check for specific structural items
    print(f"\n--- 结构完整性检查 ---")

    # Check sections present in EN but missing in CN
    en_h2s = [clean_html(h) for h in re.findall(r'<h2[^>]*>(.*?)</h2>', en)]
    cn_h2s = [re.sub(r'^#+\s+', '', h).strip() for h in re.findall(r'^##\s+.+$', cn, re.MULTILINE)]

    print(f"英文 H2 章节: {en_h2s}")
    print(f"中文 H2 章节: {cn_h2s}")

    # Check for code blocks
    en_code_blocks = re.findall(r'<pre class="PROGRAMLISTING">(.*?)</pre>', en, re.DOTALL)
    cn_code_blocks = re.findall(r'```[\w]*\n(.*?)```', cn, re.DOTALL)
    print(f"\n英文代码块: {len(en_code_blocks)}, 中文代码块: {len(cn_code_blocks)}")

    # Check for security advisory table
    en_sa = sorted(set(re.findall(r'SA-\d{2}:\d{2}\.\w+', en)))
    cn_sa = sorted(set(re.findall(r'SA-\d{2}:\d{2}\.\w+', cn)))
    missing_sa = [sa for sa in en_sa if sa not in cn_sa]
    print(f"\n安全公告: 英文 {len(en_sa)}, 中文 {len(cn_sa)}")
    if missing_sa:
        print(f"  ❌ 缺失: {missing_sa}")
    else:
        print(f"  ✅ 完整")

# Run comparisons
compare_file('7.0', os.path.join(BASE, 'en_7.0.txt'), os.path.join(BASE, '7.0.md'))
compare_file('7.1', os.path.join(BASE, 'en_7.1.txt'), os.path.join(BASE, '7.1.md'))
compare_file('7.2', os.path.join(BASE, 'en_7.2_detailed.txt'), os.path.join(BASE, '7.2.md'))
compare_file('7.4', os.path.join(BASE, 'en_7.4.txt'), os.path.join(BASE, '7.4.md'))

print("\n\n" + "="*60)
print("比对完成")

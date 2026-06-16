#!/usr/bin/env python3
"""Compare Chinese translations with English originals for completeness."""
import re, os

BASE = r"C:\Users\ykla\Documents\FreeBSD-relnotes-CN"

def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_sa(text):
    return sorted(set(re.findall(r'SA-\d{2}:\d{2}\.\w+', text)))

def extract_man_refs(text):
    return sorted(set(re.findall(r'(\w+)\((\d+)\)', text)))

def extract_platforms(text):
    return re.findall(r'\[(amd64|i386|sparc64|powerpc|ia64|pc98|arm|sun4v)\]', text)

def extract_sysctls(text):
    vars = set(re.findall(r'\b[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*){2,}', text))
    exclude = {s for s in vars if any(x in s for x in ['.html', '.org', '.com', 'www.', 'http', 'freebsd.org', 'mailto:', 'ftp.', 'cgi'])}
    return sorted(vars - exclude)

def extract_code_blocks_en(text):
    blocks = re.findall(r'<pre class="PROGRAMLISTING">(.*?)</pre>', text, re.DOTALL)
    return [b.strip() for b in blocks if b.strip()]

def extract_code_blocks_cn(text):
    blocks = re.findall(r'```[\w]*\n(.*?)```', text, re.DOTALL)
    return [b.strip() for b in blocks if b.strip()]

def extract_en_paragraphs_by_section(text):
    """Extract paragraphs grouped by section from English HTML."""
    sections = {}
    current_h2 = ""
    current_h3 = ""
    current_h4 = ""

    # Split by section headers
    parts = re.split(r'<h2 class="SECT\d*"[^>]*>(.*?)</h2>|<h3 class="SECT\d*"[^>]*>(.*?)</h3>|<h4 class="SECT\d*"[^>]*>(.*?)</h4>', text)

    for i, part in enumerate(parts):
        if part is None:
            continue
        # Check if this is a header match
        if i % 4 == 1 and part:  # h2
            current_h2 = re.sub(r'<[^>]+>', '', part).strip()
        elif i % 4 == 2 and part:  # h3
            current_h3 = re.sub(r'<[^>]+>', '', part).strip()
        elif i % 4 == 3 and part:  # h4
            current_h4 = re.sub(r'<[^>]+>', '', part).strip()

    return sections

def compare_file(ver):
    en_path = os.path.join(BASE, f'en_{ver}.txt')
    cn_path = os.path.join(BASE, f'{ver}.md')

    if not os.path.exists(en_path) or not os.path.exists(cn_path):
        print(f"\n=== {ver}: Missing files ===")
        return

    print(f"\n{'='*60}")
    print(f"=== FreeBSD {ver}-RELEASE 完整性比对 ===")
    print(f"{'='*60}")

    en = read(en_path)
    cn = read(cn_path)

    # 1. Security Advisories
    en_sa = extract_sa(en)
    cn_sa = extract_sa(cn)
    missing_sa = [sa for sa in en_sa if sa not in cn_sa]

    print(f"\n--- 安全公告 ---")
    print(f"  英文: {len(en_sa)} 条, 中文: {len(cn_sa)} 条")
    if missing_sa:
        print(f"  ❌ 缺失: {missing_sa}")
    else:
        print(f"  ✅ 完整")

    # 2. Man page references
    en_refs = extract_man_refs(en)
    cn_refs = extract_man_refs(cn)
    missing_refs = [r for r in en_refs if r not in cn_refs]

    print(f"\n--- 手册页引用 ---")
    print(f"  英文: {len(en_refs)} 个, 中文: {len(cn_refs)} 个")
    if missing_refs:
        by_sec = {}
        for name, sec in missing_refs:
            by_sec.setdefault(sec, []).append(name)
        print(f"  ❌ 缺失 ({len(missing_refs)} 个):")
        for sec in sorted(by_sec.keys()):
            print(f"    章节 {sec}: {', '.join(sorted(by_sec[sec]))}")
    else:
        print(f"  ✅ 完整")

    # 3. Platform tags
    en_plat = extract_platforms(en)
    cn_plat = extract_platforms(cn)
    en_pc = {}
    for p in en_plat: en_pc[p] = en_pc.get(p, 0) + 1
    cn_pc = {}
    for p in cn_plat: cn_pc[p] = cn_pc.get(p, 0) + 1

    print(f"\n--- 平台标记 ---")
    print(f"  英文: {len(en_plat)} 个, 中文: {len(cn_plat)} 个")
    for p in sorted(set(list(en_pc.keys()) + list(cn_pc.keys()))):
        ec = en_pc.get(p, 0)
        cc = cn_pc.get(p, 0)
        status = "✅" if cc >= ec else "❌"
        print(f"    [{p}]: 英文 {ec}, 中文 {cc} {status}")

    # 4. Code blocks
    en_code = extract_code_blocks_en(en)
    cn_code = extract_code_blocks_cn(cn)

    print(f"\n--- 代码块 ---")
    print(f"  英文: {len(en_code)} 个, 中文: {len(cn_code)} 个")

    missing_code = []
    for en_block in en_code:
        en_keys = set(re.findall(r'[a-zA-Z_]\w*', en_block))
        found = False
        for cn_block in cn_code:
            cn_keys = set(re.findall(r'[a-zA-Z_]\w*', cn_block))
            if en_keys and cn_keys and len(en_keys & cn_keys) > len(en_keys) * 0.5:
                found = True
                break
        if not found and en_block:
            missing_code.append(en_block[:100])

    if missing_code:
        print(f"  ❌ 可能缺失 ({len(missing_code)} 个):")
        for mc in missing_code:
            print(f"    - {mc}...")
    else:
        print(f"  ✅ 完整")

    # 5. sysctl variables
    en_sys = extract_sysctls(en)
    cn_sys = extract_sysctls(cn)
    missing_sys = [s for s in en_sys if s not in cn_sys]

    print(f"\n--- sysctl 变量 ---")
    print(f"  英文: {len(en_sys)} 个, 中文: {len(cn_sys)} 个")
    if missing_sys:
        print(f"  ❌ 缺失 ({len(missing_sys)} 个):")
        for s in missing_sys:
            print(f"    - {s}")
    else:
        print(f"  ✅ 完整")

    # 6. Check for key sections presence
    print(f"\n--- 章节结构 ---")

    # Extract section headings from EN (HTML)
    en_h2 = re.findall(r'<h2[^>]*>(.*?)</h2>', en)
    en_h3 = re.findall(r'<h3[^>]*>(.*?)</h3>', en)
    en_h4 = re.findall(r'<h4[^>]*>(.*?)</h4>', en)

    # Clean HTML from headings
    def clean_html(s):
        return re.sub(r'<[^>]+>', '', s).strip()

    en_sections = [clean_html(h) for h in en_h2 + en_h3 + en_h4 if clean_html(h)]

    # Extract section headings from CN (Markdown)
    cn_headings = re.findall(r'^#+\s+(.+)$', cn, re.MULTILINE)
    cn_sections = [h.strip() for h in cn_headings]

    # Check key sections
    key_sections = {
        '2.1': ['Security', '安全'],
        '2.2': ['Kernel', '内核'],
        '2.3': ['Userland', '用户'],
        '2.4': ['Contributed', 'Third', '第三方'],
        '2.5': ['Ports', 'Release Engineering', '发布工程'],
        '2.6': ['Release Engineering', 'Ports', '发布工程'],
    }

    for sec_id, keywords in key_sections.items():
        en_found = any(any(kw.lower() in s.lower() for kw in keywords) for s in en_sections)
        cn_found = any(any(kw.lower() in s.lower() for kw in keywords) for s in cn_sections)
        if en_found and not cn_found:
            print(f"  ❌ 章节 {sec_id} 可能在中文翻译中缺失")
        elif en_found and cn_found:
            print(f"  ✅ 章节 {sec_id} 存在")

    # 7. Check for Microsoft trademark notice (7.2 has it)
    if 'Microsoft' in en and 'Microsoft' not in cn:
        print(f"\n  ⚠️  英文原文包含 Microsoft 商标声明，但中文翻译中未找到")

    # 8. Check for errata notice
    if 'errata' in en.lower() and '勘误' not in cn and '错误' not in cn:
        print(f"  ⚠️  英文原文包含 errata 相关内容，中文翻译中可能缺失")

for ver in ['7.0', '7.1', '7.2', '7.4']:
    compare_file(ver)

print("\n\n" + "="*60)
print("比对完成")

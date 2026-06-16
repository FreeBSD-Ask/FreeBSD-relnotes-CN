#!/usr/bin/env python3
"""
Compare Chinese translation files with English originals from FreeBSD doc repo.
Check for missing paragraphs, sections, code blocks, and inline code.
"""

import re
import os
import urllib.request
import ssl

# File mapping: Chinese file -> English URL
FILES = {
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\5.0.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.0R/relnotes-i386.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\5.1.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.1R/relnotes-i386.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\5.2-amd64.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.2R/relnotes-amd64.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\5.2.1-amd64.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.2.1R/relnotes-amd64.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\5.3-amd64.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.3R/relnotes-amd64.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\5.4-amd64.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.4R/relnotes-amd64.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\5.5-amd64.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.5R/relnotes-amd64.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\4.0.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.0R/relnotes-i386.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\4.1.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.1R/relnotes-i386.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\4.1.1.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.1.1R/relnotes-i386.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\4.2.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.2R/relnotes-i386.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\4.3.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.3R/relnotes.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\4.4-i386.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.4R/relnotes-i386.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\4.5-i386.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.5R/relnotes-i386.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\4.6-i386.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.6R/relnotes-i386.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\4.6.2-i386.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.6.2R/relnotes-i386.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\4.7-i386.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.7R/relnotes-i386.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\4.8.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.8R/relnotes-i386.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\4.9.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.9R/relnotes-i386.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\4.10.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.10R/relnotes-i386.adoc",
    r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\4.11.md": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.11R/relnotes-i386.adoc",
}

def fetch_url(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        return resp.read().decode('utf-8', errors='replace')

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def clean_html(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&trade;', 'TM', text)
    text = re.sub(r'&reg;', '(R)', text)
    text = re.sub(r'&copy;', '(C)', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'``', '"', text)
    text = re.sub(r"''", '"', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_en_data(html_content):
    # Security advisories
    sa_pattern = re.compile(r'FreeBSD-SA-\d{2}:\d{2}')
    security_advisories = sorted(set(sa_pattern.findall(html_content)))

    # Headings
    heading_pattern = re.compile(r'<h[234][^>]*>(?:<a[^>]*>)?\s*(.*?)\s*(?:</a>)?</h[234]>', re.DOTALL)
    headings = [clean_html(m.group(1)) for m in heading_pattern.finditer(html_content)]

    # Paragraphs
    para_pattern = re.compile(r'<p[^>]*>(.*?)</p>', re.DOTALL)
    paragraphs = [clean_html(m.group(1)) for m in para_pattern.finditer(html_content) if len(clean_html(m.group(1))) > 30]

    # Code blocks
    code_pattern = re.compile(r'<pre[^>]*>(.*?)</pre>', re.DOTALL)
    code_blocks = [clean_html(m.group(1)) for m in code_pattern.finditer(html_content) if clean_html(m.group(1))]

    # Man page refs
    man_pattern = re.compile(r'man\.cgi\?query=(\w+)')
    man_refs = sorted(set(man_pattern.findall(html_content)))

    # Inline code (tt tags)
    tt_pattern = re.compile(r'<tt[^>]*>(.*?)</tt>', re.DOTALL)
    inline_code = sorted(set(clean_html(m.group(1)) for m in tt_pattern.finditer(html_content) if clean_html(m.group(1))))

    return {
        'headings': headings,
        'paragraphs': paragraphs,
        'code_blocks': code_blocks,
        'security_advisories': security_advisories,
        'man_refs': man_refs,
        'inline_code': inline_code,
    }

def extract_cn_data(md_content):
    # Security advisories
    sa_pattern = re.compile(r'FreeBSD-SA-\d{2}:\d{2}')
    security_advisories = sorted(set(sa_pattern.findall(md_content)))

    # Headings
    heading_pattern = re.compile(r'^(#{1,5})\s+(.+)$', re.MULTILINE)
    headings = [m.group(2).strip() for m in heading_pattern.finditer(md_content)]

    # Paragraphs - simplified
    lines = md_content.split('\n')
    paragraphs = []
    current_para = []
    in_code_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if stripped.startswith('#') or stripped.startswith('>') or stripped.startswith('- ') or stripped.startswith('* '):
            if current_para:
                para = ' '.join(current_para).strip()
                if len(para) > 30:
                    paragraphs.append(para)
                current_para = []
            continue
        if not stripped:
            if current_para:
                para = ' '.join(current_para).strip()
                if len(para) > 30:
                    paragraphs.append(para)
                current_para = []
            continue
        current_para.append(stripped)
    if current_para:
        para = ' '.join(current_para).strip()
        if len(para) > 30:
            paragraphs.append(para)

    # Code blocks
    code_pattern = re.compile(r'```[\w]*\n(.*?)```', re.DOTALL)
    code_blocks = [m.group(1).strip() for m in code_pattern.finditer(md_content) if m.group(1).strip()]

    # Man page refs
    man_pattern = re.compile(r'man\.cgi\?query=(\w+)')
    man_refs = sorted(set(man_pattern.findall(md_content)))

    # Inline code
    inline_pattern = re.compile(r'`([^`]+)`')
    inline_code = sorted(set(m.group(1) for m in inline_pattern.finditer(md_content) if m.group(1) and not m.group(1).startswith('http')))

    return {
        'headings': headings,
        'paragraphs': paragraphs,
        'code_blocks': code_blocks,
        'security_advisories': security_advisories,
        'man_refs': man_refs,
        'inline_code': inline_code,
    }

def compare_files(cn_path, en_url):
    basename = os.path.basename(cn_path)
    print(f"\n{'='*60}")
    print(f"对比: {basename}")
    print(f"{'='*60}")

    try:
        en_content = fetch_url(en_url)
    except Exception as e:
        print(f"  ERROR fetching English source: {e}")
        return None

    try:
        cn_content = read_file(cn_path)
    except Exception as e:
        print(f"  ERROR reading Chinese file: {e}")
        return None

    en = extract_en_data(en_content)
    cn = extract_cn_data(cn_content)

    issues = []

    # 1. Missing security advisories
    en_sa_set = set(en['security_advisories'])
    cn_sa_set = set(cn['security_advisories'])
    missing_sa = en_sa_set - cn_sa_set
    if missing_sa:
        issues.append(f"缺失安全公告: {', '.join(sorted(missing_sa))}")

    # 2. Paragraph ratio check
    en_para_count = len(en['paragraphs'])
    cn_para_count = len(cn['paragraphs'])
    ratio = cn_para_count / en_para_count if en_para_count > 0 else 1
    if ratio < 0.6:
        issues.append(f"段落比例偏低: 英文 {en_para_count} 段, 中文 {cn_para_count} 段 ({ratio:.0%})")

    # 3. Code block count
    en_code_count = len(en['code_blocks'])
    cn_code_count = len(cn['code_blocks'])
    if en_code_count > cn_code_count:
        issues.append(f"代码块数量不匹配: 英文 {en_code_count} 个, 中文 {cn_code_count} 个")

    # 4. Man page references
    en_man_count = len(en['man_refs'])
    cn_man_count = len(cn['man_refs'])
    if en_man_count > 0 and cn_man_count < en_man_count * 0.4:
        issues.append(f"man 引用数量偏少: 英文 {en_man_count} 个, 中文 {cn_man_count} 个")

    # 5. Important kernel options/keywords
    important_keywords = [
        'COMPAT_FREEBSD', 'NO_KERBEROS', 'MAKE_KERBEROS5',
        'SCHED_4BSD', 'SCHED_ULE',
        'NO_GEOM', 'NODEVFS',
        'FAST_IPSEC', 'RLIMIT_VMEM', 'MUTEX_PROFILING',
        'REGRESSION', 'DIRECTIO', 'LAZY_SWITCH',
        'CD9660_ICONV', 'MSDOSFS_ICONV', 'LIBICONV',
        'GEOM_BDE', 'CPU_ELAN', 'CPU_DISABLE_CMPXCHG',
        'DA_OLD_QUIRKS', 'IP_ONESBCAST',
        'PFIL_HOOKS', 'COMPAT_AOUT',
    ]
    missing_keywords = []
    for kw in important_keywords:
        if kw in en_content and kw not in cn_content:
            missing_keywords.append(kw)
    if missing_keywords:
        issues.append(f"缺失重要关键词/内核选项: {', '.join(missing_keywords)}")

    # 6. Heading count comparison
    en_heading_count = len(en['headings'])
    cn_heading_count = len(cn['headings'])
    if en_heading_count > 0 and cn_heading_count < en_heading_count * 0.6:
        issues.append(f"标题数量偏少: 英文 {en_heading_count} 个, 中文 {cn_heading_count} 个")

    # Print results
    if issues:
        print(f"  发现问题:")
        for issue in issues:
            print(f"    * {issue}")
    else:
        print(f"  未发现明显缺失")

    print(f"  统计: EN({en_heading_count}标题, {en_para_count}段, {en_code_count}代码块, {len(en_sa_set)}SA, {en_man_count}man)")
    print(f"        CN({cn_heading_count}标题, {cn_para_count}段, {cn_code_count}代码块, {len(cn_sa_set)}SA, {cn_man_count}man)")

    return {'basename': basename, 'issues': issues, 'en': en, 'cn': cn, 'en_content': en_content, 'cn_content': cn_content}

def main():
    all_results = {}
    for cn_path, en_url in FILES.items():
        result = compare_files(cn_path, en_url)
        if result:
            all_results[result['basename']] = result

    # Detailed report
    print("\n\n" + "="*80)
    print("详细缺失内容报告")
    print("="*80)

    for basename, result in sorted(all_results.items()):
        if not result['issues']:
            continue

        print(f"\n### {basename}")
        en = result['en']
        cn = result['cn']
        en_content = result['en_content']
        cn_content = result['cn_content']

        # Missing security advisories detail
        en_sa_set = set(en['security_advisories'])
        cn_sa_set = set(cn['security_advisories'])
        missing_sa = en_sa_set - cn_sa_set
        if missing_sa:
            print(f"  缺失安全公告:")
            for sa in sorted(missing_sa):
                # Find context in English
                sa_context = re.search(re.escape(sa) + r'[^\n]{0,200}', en_content)
                if sa_context:
                    ctx = clean_html(sa_context.group(0))[:200]
                    print(f"    - {sa}: {ctx}")

        # Missing keywords detail
        important_keywords = [
            'COMPAT_FREEBSD', 'NO_KERBEROS', 'MAKE_KERBEROS5',
            'SCHED_4BSD', 'SCHED_ULE', 'NO_GEOM', 'NODEVFS',
            'FAST_IPSEC', 'RLIMIT_VMEM', 'MUTEX_PROFILING',
            'REGRESSION', 'DIRECTIO', 'LAZY_SWITCH',
            'CD9660_ICONV', 'MSDOSFS_ICONV', 'LIBICONV',
            'GEOM_BDE', 'CPU_ELAN', 'CPU_DISABLE_CMPXCHG',
            'DA_OLD_QUIRKS', 'IP_ONESBCAST', 'PFIL_HOOKS', 'COMPAT_AOUT',
        ]
        missing_kw = [kw for kw in important_keywords if kw in en_content and kw not in cn_content]
        if missing_kw:
            print(f"  缺失内核选项/关键词:")
            for kw in missing_kw:
                # Find context
                kw_context = re.search(re.escape(kw) + r'[^\n]{0,150}', en_content)
                if kw_context:
                    ctx = clean_html(kw_context.group(0))[:200]
                    print(f"    - {kw}: {ctx}")

    # Summary
    print("\n\n" + "="*80)
    print("总结")
    print("="*80)
    files_with_issues = sum(1 for r in all_results.values() if r['issues'])
    print(f"共检查 {len(all_results)} 个文件, {files_with_issues} 个文件存在缺失内容问题")

    for basename, result in sorted(all_results.items()):
        if result['issues']:
            print(f"\n  {basename}:")
            for issue in result['issues']:
                print(f"    - {issue}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Compare Chinese translations with English originals for FreeBSD 4.x and 5.x release notes.
Focus on: missing paragraphs, sentences, code blocks, man page references, security advisories.
Filter out false positives from previous runs.
"""
import re, os, urllib.request, ssl, sys, json, time

sys.stdout.reconfigure(encoding='utf-8')
BASE = r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN"

FILES = [
    # 5.x
    ("5.0.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.0R/relnotes-i386.adoc"),
    ("5.1.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.1R/relnotes-i386.adoc"),
    ("5.2-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.2R/relnotes-amd64.adoc"),
    ("5.2.1-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.2.1R/relnotes-amd64.adoc"),
    ("5.3-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.3R/relnotes-amd64.adoc"),
    ("5.4-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.4R/relnotes-amd64.adoc"),
    ("5.5-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.5R/relnotes-amd64.adoc"),
    # 4.0-4.3 (plain text format)
    ("4.0.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.0R/notes.adoc"),
    ("4.1.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.1R/notes.adoc"),
    ("4.1.1.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.1.1R/notes.adoc"),
    ("4.2.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.2R/notes.adoc"),
    ("4.3.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.3R/notes.adoc"),
    # 4.4-4.7 (HTML in adoc)
    ("4.4-i386.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.4R/relnotes-i386.adoc"),
    ("4.5-i386.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.5R/relnotes-i386.adoc"),
    ("4.6-i386.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.6R/relnotes-i386.adoc"),
    ("4.6.2-i386.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.6.2R/relnotes-i386.adoc"),
    ("4.7-i386.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.7R/relnotes-i386.adoc"),
    # 4.8-4.11 (HTML in adoc)
    ("4.8.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.8R/relnotes-i386.adoc"),
    ("4.9.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.9R/relnotes-i386.adoc"),
    ("4.10.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.10R/relnotes-i386.adoc"),
    ("4.11.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.11R/relnotes-i386.adoc"),
]

def fetch(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        return resp.read().decode('utf-8', errors='replace')

def clean_html(t):
    """Remove HTML tags and decode entities."""
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'&lt;', '<', t)
    t = re.sub(r'&gt;', '>', t)
    t = re.sub(r'&amp;', '&', t)
    t = re.sub(r'&quot;', '"', t)
    t = re.sub(r'&\w+;', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

def extract_html_body(en):
    """Extract content between ++++ markers (HTML body in adoc files)."""
    parts = re.split(r'\+\+\+\+', en)
    html_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 1:  # odd indices are between ++++
            html_parts.append(part)
    return '\n'.join(html_parts)

def extract_sections_from_html(html):
    """Extract sections from HTML content based on <h2>, <h3> tags."""
    sections = []
    # Find all headings
    headings = list(re.finditer(r'<(h[1-6])[^>]*>(.*?)</\1>', html, re.DOTALL | re.IGNORECASE))
    for i, m in enumerate(headings):
        title = clean_html(m.group(2)).strip()
        start = m.end()
        end = headings[i+1].start() if i+1 < len(headings) else len(html)
        content = html[start:end]
        sections.append({'title': title, 'content': content})
    return sections

def extract_sections_from_plain(en):
    """Extract sections from plain text format (4.0-4.3)."""
    sections = []
    lines = en.split('\n')
    current_title = ""
    current_lines = []
    for line in lines:
        # Section headers in plain text: lines that look like "1. Title" or "1.1 Title"
        if re.match(r'^\d+\.\d*\s+\S', line.strip()):
            if current_title:
                sections.append({'title': current_title, 'content': '\n'.join(current_lines)})
            current_title = line.strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_title:
        sections.append({'title': current_title, 'content': '\n'.join(current_lines)})
    return sections

def extract_cn_sections(cn):
    """Extract sections from Chinese markdown."""
    sections = []
    lines = cn.split('\n')
    current_title = ""
    current_lines = []
    for line in lines:
        if re.match(r'^#+\s+', line):
            if current_title:
                sections.append({'title': current_title, 'content': '\n'.join(current_lines)})
            current_title = re.sub(r'^#+\s+', '', line).strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_title:
        sections.append({'title': current_title, 'content': '\n'.join(current_lines)})
    return sections

def get_man_page_refs(text):
    """Extract man page references from HTML or markdown text."""
    refs = set()
    # HTML format: man.cgi?query=xxx&sektion=N
    for m in re.finditer(r'man\.cgi\?query=(\w+)[&/]sektion=(\d+)', text):
        refs.add((m.group(1).lower(), m.group(2)))
    # Markdown format: [xxx(N)](http...man.cgi?query=xxx&sektion=N) or just xxx(N)
    for m in re.finditer(r'\[([\w.-]+)\((\d+)\)\]', text):
        refs.add((m.group(1).lower(), m.group(2)))
    # Also check for bare man.cgi links
    for m in re.finditer(r'man\.cgi\?query=([\w.-]+)', text):
        refs.add((m.group(1).lower(), None))
    return refs

def get_code_blocks_html(html):
    """Extract code blocks from HTML."""
    blocks = []
    for m in re.finditer(r'<pre[^>]*>(.*?)</pre>', html, re.DOTALL):
        content = clean_html(m.group(1)).strip()
        if content:
            blocks.append(content)
    return blocks

def get_code_blocks_md(md):
    """Extract code blocks from markdown."""
    blocks = []
    for m in re.finditer(r'```[\w]*\n(.*?)```', md, re.DOTALL):
        content = m.group(1).strip()
        if content:
            blocks.append(content)
    return blocks

def get_sa_refs(text):
    """Extract security advisory references."""
    return set(re.findall(r'FreeBSD-SA-\d{2}:\d{2}', text))

def get_en_refs(text):
    """Extract errata notice references."""
    return set(re.findall(r'FreeBSD-EN-\d{2}:\d{2}', text))

def compare_code_blocks(en_blocks, cn_blocks):
    """Compare code blocks and find missing ones."""
    missing = []
    for en_block in en_blocks:
        # Normalize for comparison
        en_normalized = re.sub(r'\s+', ' ', en_block.lower().strip())
        found = False
        for cn_block in cn_blocks:
            cn_normalized = re.sub(r'\s+', ' ', cn_block.lower().strip())
            # Check if the code block content is similar
            if en_normalized == cn_normalized:
                found = True
                break
            # Check if one is a substring of the other (partial match)
            if len(en_normalized) > 20 and (en_normalized[:50] in cn_normalized or cn_normalized[:50] in en_normalized):
                found = True
                break
        if not found and len(en_normalized) > 10:
            missing.append(en_block[:150])
    return missing

def detailed_compare(cn_name, en_url):
    cn_path = os.path.join(BASE, cn_name)
    print(f"\n{'='*60}")
    print(f"检查: {cn_name}")
    print(f"{'='*60}")

    try:
        en = fetch(en_url)
    except Exception as e:
        print(f"  错误: 无法获取英文原文 - {e}")
        return None

    try:
        with open(cn_path, 'r', encoding='utf-8') as f:
            cn = f.read()
    except Exception as e:
        print(f"  错误: 无法读取中文文件 - {e}")
        return None

    issues = []

    # Determine format
    is_plain_text = '++++' not in en and '<html' not in en.lower()
    is_html = '++++' in en

    # 1. Security advisories
    en_sa = get_sa_refs(en)
    cn_sa = get_sa_refs(cn)
    missing_sa = en_sa - cn_sa
    if missing_sa:
        issues.append({
            'type': '缺失安全公告',
            'detail': ', '.join(sorted(missing_sa)),
            'count': len(missing_sa)
        })

    # 2. Errata notices
    en_en = get_en_refs(en)
    cn_en = get_en_refs(cn)
    missing_en = en_en - cn_en
    if missing_en:
        issues.append({
            'type': '缺失勘误通知',
            'detail': ', '.join(sorted(missing_en)),
            'count': len(missing_en)
        })

    # 3. Man page references
    en_man = get_man_page_refs(en)
    cn_man = get_man_page_refs(cn)
    # Only compare by name (ignore section number differences)
    en_man_names = {name for name, sect in en_man}
    cn_man_names = {name for name, sect in cn_man}
    missing_man = en_man_names - cn_man_names
    # Filter out common false positives
    false_positives = {'contents', 'index', 'home', 'search', 'about', 'help', 'type', 'name', 'value', 'size', 'count', 'data', 'file', 'list', 'text', 'time', 'date', 'mode', 'flag', 'port', 'host', 'user', 'group', 'path', 'link', 'read', 'write', 'open', 'close', 'start', 'stop', 'test', 'load', 'boot', 'init', 'main', 'info', 'stat', 'set', 'get', 'put', 'add', 'del', 'run', 'log', 'key', 'map', 'dev', 'src', 'dst', 'src', 'old', 'new'}
    missing_man_filtered = {m for m in missing_man if m not in false_positives and len(m) > 2}
    if missing_man_filtered:
        # Verify each one - check if the name appears anywhere in the Chinese text
        truly_missing = []
        text_only_missing = []
        for name in sorted(missing_man_filtered):
            if name.lower() not in cn.lower():
                truly_missing.append(name)
            else:
                text_only_missing.append(name)
        if truly_missing:
            issues.append({
                'type': '完全缺失的手册页引用',
                'detail': ', '.join(sorted(truly_missing)),
                'count': len(truly_missing)
            })
        if text_only_missing:
            issues.append({
                'type': '有文本但缺少man.cgi链接的手册页',
                'detail': ', '.join(sorted(text_only_missing)),
                'count': len(text_only_missing)
            })

    # 4. Code blocks
    if is_html:
        html_body = extract_html_body(en)
        en_code = get_code_blocks_html(html_body)
    else:
        en_code = get_code_blocks_html(en)
    cn_code = get_code_blocks_md(cn)

    if en_code:
        missing_code = compare_code_blocks(en_code, cn_code)
        if missing_code:
            for mc in missing_code[:5]:  # Limit to first 5
                issues.append({
                    'type': '可能缺失的代码块',
                    'detail': mc[:200],
                    'count': 1
                })

    # 5. Section comparison
    if is_plain_text:
        en_sections = extract_sections_from_plain(en)
    elif is_html:
        html_body = extract_html_body(en)
        en_sections = extract_sections_from_html(html_body)
    else:
        en_sections = extract_sections_from_plain(en)

    cn_sections = extract_cn_sections(cn)

    # Compare section counts
    en_section_titles = [s['title'] for s in en_sections if s['title']]
    cn_section_count = len(cn_sections)
    en_section_count = len(en_sections)

    # 6. Paragraph-level comparison for HTML sources
    if is_html:
        html_body = extract_html_body(en)
        # Extract paragraphs from HTML
        en_paragraphs = re.findall(r'<p>(.*?)</p>', html_body, re.DOTALL)
        en_para_texts = [clean_html(p).strip() for p in en_paragraphs if clean_html(p).strip()]

        # Extract paragraphs from Chinese markdown (non-heading, non-code, non-table lines)
        cn_lines = cn.split('\n')
        cn_para_texts = []
        current_para = []
        in_code = False
        for line in cn_lines:
            if line.strip().startswith('```'):
                in_code = not in_code
                continue
            if in_code:
                continue
            if line.strip().startswith('#') or line.strip().startswith('|') or line.strip().startswith('---'):
                if current_para:
                    cn_para_texts.append(' '.join(current_para).strip())
                    current_para = []
                continue
            if line.strip() == '':
                if current_para:
                    cn_para_texts.append(' '.join(current_para).strip())
                    current_para = []
            else:
                current_para.append(line.strip())
        if current_para:
            cn_para_texts.append(' '.join(current_para).strip())

        # Check for significant paragraph count difference
        if len(en_para_texts) > 0 and len(cn_para_texts) > 0:
            ratio = len(cn_para_texts) / len(en_para_texts)
            if ratio < 0.5:
                issues.append({
                    'type': '段落数量差异较大',
                    'detail': f'英文段落数: {len(en_para_texts)}, 中文段落数: {len(cn_para_texts)}, 比率: {ratio:.2f}',
                    'count': 1
                })

    # Print results
    if issues:
        for issue in issues:
            print(f"  [{issue['type']}] {issue['detail']}")
    else:
        print(f"  通过 - 未发现明显缺失")

    return {'name': cn_name, 'issues': issues, 'en_len': len(en), 'cn_len': len(cn)}

# Run all comparisons
print("FreeBSD 4.x/5.x 发行说明中文翻译完整性检查")
print("=" * 60)

results = {}
for cn_name, en_url in FILES:
    r = detailed_compare(cn_name, en_url)
    if r:
        results[r['name']] = r
    time.sleep(0.5)  # Be nice to GitHub

# Final summary
print("\n\n" + "=" * 80)
print("最终汇总报告")
print("=" * 80)

ok_files = []
problem_files = {}
for name, r in sorted(results.items()):
    if r['issues']:
        problem_files[name] = r['issues']
    else:
        ok_files.append(name)

print(f"\n通过检查的文件 ({len(ok_files)}):")
for f in ok_files:
    print(f"  - {f}")

print(f"\n存在问题的文件 ({len(problem_files)}):")
for name, issues in sorted(problem_files.items()):
    print(f"\n  {name}:")
    for issue in issues:
        print(f"    [{issue['type']}] {issue['detail']}")

print(f"\n总计: {len(results)} 个文件检查, {len(ok_files)} 个通过, {len(problem_files)} 个存在问题")

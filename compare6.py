#!/usr/bin/env python3
"""Comprehensive structural comparison of EN vs CN files."""
import re, html

BASE = r"C:\Users\ykla\Documents\FreeBSD-relnotes-CN"

def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def clean_html(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def extract_en_sections(en_text):
    parts = en_text.split('++++')
    html_part = parts[1] if len(parts) > 1 else en_text
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html_part)
    h3s = re.findall(r'<h3[^>]*>(.*?)</h3>', html_part)
    h4s = re.findall(r'<h4[^>]*>(.*?)</h4>', html_part)
    return [clean_html(h) for h in h2s], [clean_html(h) for h in h3s], [clean_html(h) for h in h4s]

def extract_cn_sections(cn_text):
    h2s = [re.sub(r'^#+\s+', '', h).strip() for h in re.findall(r'^##\s+.+$', cn_text, re.MULTILINE)]
    h3s = [re.sub(r'^#+\s+', '', h).strip() for h in re.findall(r'^###\s+.+$', cn_text, re.MULTILINE)]
    h4s = [re.sub(r'^#+\s+', '', h).strip() for h in re.findall(r'^####\s+.+$', cn_text, re.MULTILINE)]
    return h2s, h3s, h4s

for ver, en_file, cn_file in [
    ('7.0', 'en_7.0.txt', '7.0.md'),
    ('7.1', 'en_7.1.txt', '7.1.md'),
    ('7.2', 'en_7.2_detailed.txt', '7.2.md'),
    ('7.4', 'en_7.4.txt', '7.4.md'),
]:
    en = read(f"{BASE}\\{en_file}")
    cn = read(f"{BASE}\\{cn_file}")
    en_h2, en_h3, en_h4 = extract_en_sections(en)
    cn_h2, cn_h3, cn_h4 = extract_cn_sections(cn)

    print(f'\n{"="*60}')
    print(f'=== FreeBSD {ver}-RELEASE 结构比对 ===')
    print(f'{"="*60}')

    print(f'\nEN H2({len(en_h2)}): {en_h2}')
    print(f'CN H2({len(cn_h2)}): {cn_h2}')
    print(f'EN H3({len(en_h3)}): {en_h3}')
    print(f'CN H3({len(cn_h3)}): {cn_h3}')
    print(f'EN H4({len(en_h4)}): {en_h4}')
    print(f'CN H4({len(cn_h4)}): {cn_h4}')

    # Count paragraphs per section in EN
    parts = en.split('++++')
    html_part = parts[1] if len(parts) > 1 else en
    en_paras = re.findall(r'<p[^>]*>(.*?)</p>', html_part, re.DOTALL)
    en_content_paras = [p for p in en_paras if len(clean_html(p)) > 20]

    # Count content lines in CN (non-heading, non-table, non-code, non-quote)
    cn_lines = []
    for l in cn.split('\n'):
        s = l.strip()
        if not s:
            continue
        if s.startswith('#'):
            continue
        if s.startswith('|'):
            continue
        if s.startswith('```'):
            continue
        if s.startswith('---'):
            continue
        if s.startswith('>'):
            continue
        if s.startswith('*') and len(s) < 30:
            continue
        if len(s) > 20:
            cn_lines.append(s)

    print(f'\nEN content paragraphs: {len(en_content_paras)}, CN content lines: {len(cn_lines)}')

    # Check for Microsoft trademark notice
    ms_in_en = 'Microsoft' in en and 'IntelliMouse' in en
    ms_in_cn = 'Microsoft' in cn and 'IntelliMouse' in cn
    print(f'Microsoft trademark notice: EN={ms_in_en}, CN={ms_in_cn}')

    # Check for code blocks
    en_code_blocks = re.findall(r'<pre class="PROGRAMLISTING">(.*?)</pre>', en, re.DOTALL)
    cn_code_blocks = re.findall(r'```[\w]*\n(.*?)```', cn, re.DOTALL)
    print(f'EN code blocks: {len(en_code_blocks)}, CN code blocks: {len(cn_code_blocks)}')

    # Check for security advisories
    en_sa = sorted(set(re.findall(r'SA-\d{2}:\d{2}\.\w+', en)))
    cn_sa = sorted(set(re.findall(r'SA-\d{2}:\d{2}\.\w+', cn)))
    missing_sa = [sa for sa in en_sa if sa not in cn_sa]
    print(f'Security advisories: EN={len(en_sa)}, CN={len(cn_sa)}, missing={missing_sa}')

    # Check for man page references
    en_man = sorted(set(re.findall(r'(\w+)\((\d+)\)', en)))
    cn_man = sorted(set(re.findall(r'(\w+)\((\d+)\)', cn)))
    missing_man = [m for m in en_man if m not in cn_man]
    print(f'Man page refs: EN={len(en_man)}, CN={len(cn_man)}, missing={len(missing_man)}')
    if missing_man:
        print(f'  Missing man refs: {missing_man[:20]}...' if len(missing_man) > 20 else f'  Missing man refs: {missing_man}')

    # Check for commit references
    en_commits = re.findall(r'r\d{6}', en)
    cn_commits = re.findall(r'r\d{6}', cn)
    print(f'Commit refs: EN={len(en_commits)}, CN={len(cn_commits)}')

    # Check for sponsored-by statements
    en_sponsored = len(re.findall(r'Sponsored by', en, re.IGNORECASE))
    cn_sponsored = len(re.findall(r'Sponsored by|赞助|由.*赞助', cn, re.IGNORECASE))
    print(f'Sponsored-by: EN={en_sponsored}, CN={cn_sponsored}')

print('\n\n比对完成')

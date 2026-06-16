#!/usr/bin/env python3
"""
Paragraph-level comparison for 4.6.2-i386.md.
"""
import re, os, urllib.request, ssl, sys

sys.stdout.reconfigure(encoding='utf-8')
BASE = r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN"

def fetch(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        return resp.read().decode('utf-8', errors='replace')

def clean_html(t):
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'&lt;', '<', t)
    t = re.sub(r'&gt;', '>', t)
    t = re.sub(r'&amp;', '&', t)
    t = re.sub(r'&quot;', '"', t)
    t = re.sub(r'&\w+;', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

def extract_html_body(en):
    parts = re.split(r'\+\+\+\+', en)
    html_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            html_parts.append(part)
    return '\n'.join(html_parts)

def extract_key_terms(text):
    terms = []
    versions = re.findall(r'\b\d+\.\d+\.\d+\b', text)
    terms.extend(versions)
    for m in re.finditer(r'\b([A-Z][A-Z_]{3,})\b', text):
        word = m.group(1)
        if word not in ('MERGED', 'NOTE', 'ALSO', 'THIS', 'THAT', 'WHEN', 'WHERE', 'WHICH', 'WITH', 'FROM', 'INTO', 'HAVE', 'BEEN', 'SOME', 'SUCH', 'OVER', 'THAN', 'MORE', 'MOST', 'ONLY', 'JUST', 'ALSO', 'VERY', 'EVEN', 'STILL', 'ALREADY', 'BEFORE', 'AFTER', 'BETWEEN', 'UNDER', 'ABOVE', 'BELOW', 'ABOUT', 'OTHER', 'THESE', 'THOSE', 'EACH', 'EVERY', 'BOTH', 'FEW', 'MANY', 'MUCH', 'ANY', 'ALL', 'NONE', 'SINCE', 'UNTIL', 'DURING', 'THROUGH', 'WITHOUT', 'WITHIN', 'ALONG', 'ACROSS', 'AGAINST', 'TOWARD', 'UPON', 'AMONG', 'THROUGHOUT', 'FREEBSD', 'RELEASE'):
            terms.append(word)
    terms.extend(re.findall(r'\b(\w+)\((\d+)\)', text))
    terms.extend(re.findall(r'(/\w+/\w+[\w/]*)', text))
    terms.extend(re.findall(r'\b(ALTQ|SMBFS|EXT2FS|MSDOSFS|IPFilter|IPsec|NFSv|KAME|OpenPAM|pf|gbde|pam_\w+)\b', text, re.IGNORECASE))
    terms.extend(re.findall(r'\b(\d{4,})\b', text))
    return list(set(terms))

en = fetch("https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.6.2R/relnotes-i386.adoc")
html = extract_html_body(en)

with open(os.path.join(BASE, "4.6.2-i386.md"), 'r', encoding='utf-8') as f:
    cn = f.read()

en_paras = []
for m in re.finditer(r'<p>(.*?)</p>', html, re.DOTALL):
    text = clean_html(m.group(1)).strip()
    if text and len(text) > 30:
        en_paras.append(text)

print(f"英文段落数: {len(en_paras)}")

missing_paras = []
for i, para in enumerate(en_paras):
    key_terms = extract_key_terms(para)
    if not key_terms:
        continue

    found = 0
    for term in key_terms:
        term_str = str(term).lower()
        if term_str in cn.lower():
            found += 1

    ratio = found / len(key_terms) if key_terms else 0

    if ratio < 0.4:
        missing_paras.append((i+1, para, ratio, key_terms))

print(f"\n可能缺失的段落 ({len(missing_paras)}):")
for idx, para, ratio, terms in missing_paras:
    print(f"\n  段落 {idx} (匹配率: {ratio:.0%}):")
    print(f"    {para[:250]}")
    print(f"    关键术语: {terms[:10]}")

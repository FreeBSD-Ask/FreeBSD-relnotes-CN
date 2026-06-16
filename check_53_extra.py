#!/usr/bin/env python3
"""
Check for additional missing paragraphs in 5.3-amd64.md.
"""
import re, urllib.request, ssl, sys

sys.stdout.reconfigure(encoding='utf-8')

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

def get_paragraphs_with_keyword(html, keyword):
    results = []
    for m in re.finditer(r'<p>(.*?)</p>', html, re.DOTALL):
        text = m.group(1)
        clean = clean_html(text)
        if keyword.lower() in clean.lower():
            results.append(clean)
    return results

en = fetch("https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.3R/relnotes-amd64.adoc")
html = extract_html_body(en)

# Check for EXT2FS
print("--- EXT2FS ---")
for p in get_paragraphs_with_keyword(html, 'EXT2FS'):
    print(f"  {p}")
    print()

# Check for MSDOSFS_LARGE
print("--- MSDOSFS_LARGE ---")
for p in get_paragraphs_with_keyword(html, 'MSDOSFS_LARGE'):
    print(f"  {p}")
    print()

# Check for LSI
print("--- LSI ---")
for p in get_paragraphs_with_keyword(html, 'LSI'):
    print(f"  {p}")
    print()

# Check for all paragraphs in the "Disks and Storage" section
# Find the section
sections = re.split(r'<h[1-6][^>]*>', html)
for s in sections:
    if 'Disks and Storage' in s or '磁盘' in s:
        # Get all paragraphs
        paras = re.findall(r'<p>(.*?)</p>', s, re.DOTALL)
        print(f"\n--- 磁盘与存储部分段落数: {len(paras)} ---")
        for i, p in enumerate(paras):
            clean = clean_html(p)
            print(f"  {i+1}. {clean[:150]}")
        break

# Also check the "File Systems" section
print("\n\n--- 文件系统部分 ---")
for s in sections:
    if 'Filesystems' in s or '文件系统' in s:
        paras = re.findall(r'<p>(.*?)</p>', s, re.DOTALL)
        print(f"  段落数: {len(paras)}")
        for i, p in enumerate(paras):
            clean = clean_html(p)
            print(f"  {i+1}. {clean[:150]}")
        break

# Count total paragraphs in English
all_paras = re.findall(r'<p>(.*?)</p>', html, re.DOTALL)
print(f"\n\n英文总段落数: {len(all_paras)}")

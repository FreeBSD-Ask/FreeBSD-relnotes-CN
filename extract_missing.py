#!/usr/bin/env python3
"""
Extract specific missing paragraphs from English sources for 5.3-amd64.md and 4.6.2-i386.md.
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
    """Get all <p> paragraphs containing a keyword."""
    results = []
    for m in re.finditer(r'<p>(.*?)</p>', html, re.DOTALL):
        text = m.group(1)
        clean = clean_html(text)
        if keyword.lower() in clean.lower():
            results.append(clean)
    return results

# ===== 5.3-amd64.md =====
print("=" * 70)
print("5.3-amd64.md 缺失段落详情")
print("=" * 70)

en = fetch("https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.3R/relnotes-amd64.adoc")
html = extract_html_body(en)

# ALTQ paragraph
print("\n--- ALTQ 框架段落 ---")
for p in get_paragraphs_with_keyword(html, 'ALTQ'):
    print(f"  {p}")
    print()

# SMBFS paragraph
print("\n--- SMBFS 客户端段落 ---")
for p in get_paragraphs_with_keyword(html, 'SMBFS'):
    print(f"  {p}")
    print()

# bfe driver paragraph
print("\n--- bfe 驱动段落 ---")
for p in get_paragraphs_with_keyword(html, 'bfe'):
    print(f"  {p}")
    print()

# lnc driver paragraph
print("\n--- lnc 驱动段落 ---")
for p in get_paragraphs_with_keyword(html, 'lnc'):
    print(f"  {p}")
    print()

# mount_smbfs paragraph
print("\n--- mount_smbfs 段落 ---")
for p in get_paragraphs_with_keyword(html, 'mount_smbfs'):
    print(f"  {p}")
    print()

# ===== 4.6.2-i386.md =====
print("\n" + "=" * 70)
print("4.6.2-i386.md 缺失段落详情")
print("=" * 70)

en = fetch("https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.6.2R/relnotes-i386.adoc")
html = extract_html_body(en)

# All missing man page refs
missing_items = ['m4', 'cpp', 'ngctl', 'patch', 'pam_opie', 'pam_opieaccess',
                 'pam_radius', 'pam_ssh', 'pam_tacplus', 'pam_unix', 'reboot',
                 'usbhidctl', 'watch', 'ssh-agent']

for item in missing_items:
    paras = get_paragraphs_with_keyword(html, item)
    if paras:
        print(f"\n--- {item} ---")
        for p in paras:
            print(f"  {p}")
            print()

# ===== 4.11.md =====
print("\n" + "=" * 70)
print("4.11.md 缺失段落详情")
print("=" * 70)

en = fetch("https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.11R/relnotes-i386.adoc")
html = extract_html_body(en)

paras = get_paragraphs_with_keyword(html, 'rarpd')
if paras:
    print(f"\n--- rarpd ---")
    for p in paras:
        print(f"  {p}")

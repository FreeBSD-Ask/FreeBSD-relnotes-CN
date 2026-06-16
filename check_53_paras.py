#!/usr/bin/env python3
"""
Comprehensive paragraph-level comparison for 5.3-amd64.md.
Extract all English paragraphs and check which ones are missing from Chinese.
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

def extract_key_phrases(text):
    """Extract key technical phrases from a paragraph for matching."""
    phrases = []
    # Version numbers
    phrases.extend(re.findall(r'\d+\.\d+[\.\d]*', text))
    # Technical terms (uppercase or mixed case)
    phrases.extend(re.findall(r'\b[A-Z][A-Z_]+\b', text))
    # Man page names
    phrases.extend(re.findall(r'\b\w+\(\d+\)', text))
    # File paths
    phrases.extend(re.findall(r'/\w+/\w+', text))
    # Specific technical words
    phrases.extend(re.findall(r'\b(?:GEOM|RAID|ALTQ|SMBFS|EXT2FS|MSDOSFS|NFS|IPsec|VLAN|SMP|ABI)\b', text, re.IGNORECASE))
    return [p for p in phrases if len(p) > 2]

# Fetch English source
en = fetch("https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.3R/relnotes-amd64.adoc")
html = extract_html_body(en)

# Read Chinese translation
with open(os.path.join(BASE, "5.3-amd64.md"), 'r', encoding='utf-8') as f:
    cn = f.read()

# Extract all English paragraphs
en_paras = []
for m in re.finditer(r'<p>(.*?)</p>', html, re.DOTALL):
    text = clean_html(m.group(1)).strip()
    if text and len(text) > 30:  # Skip very short paragraphs
        en_paras.append(text)

print(f"英文段落数: {len(en_paras)}")

# Check each English paragraph against Chinese
missing_paras = []
for i, para in enumerate(en_paras):
    key_phrases = extract_key_phrases(para)
    if not key_phrases:
        continue

    # Check how many key phrases appear in Chinese
    found = 0
    for phrase in key_phrases:
        if phrase.lower() in cn.lower():
            found += 1

    ratio = found / len(key_phrases) if key_phrases else 0

    if ratio < 0.3:  # Less than 30% of key phrases found
        missing_paras.append((i+1, para, ratio, key_phrases))

print(f"\n可能缺失的段落 ({len(missing_paras)}):")
for idx, para, ratio, phrases in missing_paras:
    print(f"\n  段落 {idx} (匹配率: {ratio:.0%}):")
    print(f"    {para[:200]}")
    print(f"    关键短语: {phrases[:10]}")

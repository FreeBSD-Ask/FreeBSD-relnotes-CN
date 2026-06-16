#!/usr/bin/env python3
"""Compare Chinese translations with English originals - focused on missing content."""
import re, os, urllib.request, ssl, sys

sys.stdout.reconfigure(encoding='utf-8')

BASE = r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN"

# Corrected file mapping with proper URLs
FILES = [
    ("5.0.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.0R/relnotes-i386.adoc"),
    ("5.1.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.1R/relnotes-i386.adoc"),
    ("5.2-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.2R/relnotes-amd64.adoc"),
    ("5.2.1-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.2.1R/relnotes-amd64.adoc"),
    ("5.3-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.3R/relnotes-amd64.adoc"),
    ("5.4-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.4R/relnotes-amd64.adoc"),
    ("5.5-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.5R/relnotes-amd64.adoc"),
    # 4.0-4.3 use notes.adoc
    ("4.0.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.0R/notes.adoc"),
    ("4.1.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.1R/notes.adoc"),
    ("4.1.1.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.1.1R/notes.adoc"),
    ("4.2.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.2R/notes.adoc"),
    ("4.3.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.3R/notes.adoc"),
    # 4.4+ use relnotes-i386.adoc
    ("4.4-i386.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.4R/relnotes-i386.adoc"),
    ("4.5-i386.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.5R/relnotes-i386.adoc"),
    ("4.6-i386.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.6R/relnotes-i386.adoc"),
    ("4.6.2-i386.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.6.2R/relnotes-i386.adoc"),
    ("4.7-i386.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.7R/relnotes-i386.adoc"),
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

def clean(t):
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'&lt;', '<', t)
    t = re.sub(r'&gt;', '>', t)
    t = re.sub(r'&amp;', '&', t)
    t = re.sub(r'&\w+;', ' ', t)
    t = re.sub(r'``', '"', t)
    t = re.sub(r"''", '"', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

def extract_en_sections(en):
    """Extract section headings from English source (both HTML and plain text formats)."""
    headings = []
    # HTML format headings (5.x and 4.4+)
    for m in re.finditer(r'<h[234][^>]*>(?:<a[^>]*>)?\s*(.*?)\s*(?:</a>)?</h[234]>', en, re.DOTALL):
        headings.append(clean(m.group(1)))
    # Plain text format headings (4.0-4.3)
    if not headings:
        for m in re.finditer(r'^(\d+(?:\.\d+)*)\.?\s+(.+)$', en, re.MULTILINE):
            num = m.group(1)
            title = m.group(2).strip()
            if len(title) > 3:
                headings.append(f"{num} {title}")
    return headings

def extract_en_paragraphs(en):
    """Extract meaningful paragraphs from English source."""
    paragraphs = []
    # HTML paragraphs
    for m in re.finditer(r'<p[^>]*>(.*?)</p>', en, re.DOTALL):
        text = clean(m.group(1))
        if len(text) > 30:
            paragraphs.append(text)
    # Plain text paragraphs (for 4.0-4.3 which use plain text format)
    if not paragraphs:
        for line in en.split('\n'):
            line = line.strip()
            if len(line) > 40 and not line.startswith('-') and not line.startswith('*'):
                paragraphs.append(line)
    return paragraphs

def compare(cn_name, en_url):
    cn_path = os.path.join(BASE, cn_name)
    print(f"\n{'='*60}")
    print(f"Comparing: {cn_name}")
    print(f"{'='*60}")

    try:
        en = fetch(en_url)
    except Exception as e:
        print(f"  ERROR fetching: {e}")
        return None

    try:
        with open(cn_path, 'r', encoding='utf-8') as f:
            cn = f.read()
    except Exception as e:
        print(f"  ERROR reading: {e}")
        return None

    issues = []

    # 1. Security advisories
    en_sa = set(re.findall(r'FreeBSD-SA-\d{2}:\d{2}', en))
    cn_sa = set(re.findall(r'FreeBSD-SA-\d{2}:\d{2}', cn))
    missing_sa = en_sa - cn_sa
    if missing_sa:
        issues.append(("missing_sa", sorted(missing_sa)))

    # 2. Important keywords
    keywords = [
        'COMPAT_FREEBSD', 'NO_KERBEROS', 'MAKE_KERBEROS5',
        'SCHED_4BSD', 'SCHED_ULE', 'NO_GEOM', 'NODEVFS',
        'FAST_IPSEC', 'RLIMIT_VMEM', 'MUTEX_PROFILING',
        'REGRESSION', 'DIRECTIO', 'LAZY_SWITCH',
        'CD9660_ICONV', 'MSDOSFS_ICONV', 'LIBICONV',
        'GEOM_BDE', 'CPU_ELAN', 'CPU_DISABLE_CMPXCHG',
        'DA_OLD_QUIRKS', 'IP_ONESBCAST', 'PFIL_HOOKS', 'COMPAT_AOUT',
        'IPSEC', 'P1003_1B', 'UCONSOLE', 'USER_LDT',
        'MAC', 'I386_CPU', 'GEOM_VOL',
        'ATA_ENABLE_TAGS', 'MAP_NOSYNC',
    ]
    missing_kw = [kw for kw in keywords if kw in en and kw not in cn]
    if missing_kw:
        issues.append(("missing_keywords", missing_kw))

    # 3. Section headings
    en_headings = extract_en_sections(en)
    cn_headings = re.findall(r'^#{1,5}\s+(.+)$', cn, re.MULTILINE)

    # 4. Paragraph count
    en_paras = extract_en_paragraphs(en)
    cn_para_count = 0
    cur = []
    in_cb = False
    for line in cn.split('\n'):
        s = line.strip()
        if s.startswith('```'):
            in_cb = not in_cb
            continue
        if in_cb: continue
        if s.startswith('#') or s.startswith('>') or s.startswith('- ') or s.startswith('* '):
            if cur:
                p = ' '.join(cur).strip()
                if len(p) > 30: cn_para_count += 1
                cur = []
            continue
        if not s:
            if cur:
                p = ' '.join(cur).strip()
                if len(p) > 30: cn_para_count += 1
                cur = []
            continue
        cur.append(s)
    if cur:
        p = ' '.join(cur).strip()
        if len(p) > 30: cn_para_count += 1

    en_para_count = len(en_paras)
    ratio = cn_para_count / en_para_count if en_para_count > 0 else 1
    if ratio < 0.5:
        issues.append(("low_para_ratio", f"EN={en_para_count}, CN={cn_para_count}, ratio={ratio:.0%}"))

    # 5. Code blocks
    en_code = len(re.findall(r'<pre[^>]*>', en))
    cn_code = len(re.findall(r'```', cn)) // 2
    if en_code > cn_code:
        issues.append(("code_block_mismatch", f"EN={en_code}, CN={cn_code}"))

    # 6. Man page refs
    en_man = set(re.findall(r'man\.cgi\?query=(\w+)', en))
    cn_man = set(re.findall(r'man\.cgi\?query=(\w+)', cn))
    missing_man = en_man - cn_man
    if len(missing_man) > 5:
        issues.append(("missing_man_refs", f"EN={len(en_man)}, CN={len(cn_man)}, missing={len(missing_man)}"))

    # 7. Check for major sections that exist in English but not Chinese
    # For HTML-format docs (5.x, 4.4+)
    en_section_ids = set(re.findall(r'<a id="(\w+)"', en))
    # For plain text docs (4.0-4.3), check section titles
    en_text_sections = re.findall(r'^\d+\.\s+\w', en, re.MULTILINE)

    if issues:
        print(f"  Issues found:")
        for itype, idata in issues:
            if itype == "missing_sa":
                print(f"    * Missing security advisories: {', '.join(idata)}")
            elif itype == "missing_keywords":
                print(f"    * Missing keywords/options: {', '.join(idata)}")
            elif itype == "low_para_ratio":
                print(f"    * Low paragraph ratio: {idata}")
            elif itype == "code_block_mismatch":
                print(f"    * Code block count mismatch: {idata}")
            elif itype == "missing_man_refs":
                print(f"    * Missing man page refs: {idata}")
    else:
        print(f"  No major issues found")

    print(f"  Stats: EN({len(en_headings)}h, {en_para_count}p, {en_code}cb, {len(en_sa)}sa, {len(en_man)}man)")
    print(f"         CN({len(cn_headings)}h, {cn_para_count}p, {cn_code}cb, {len(cn_sa)}sa, {len(cn_man)}man)")

    return {'name': cn_name, 'issues': issues, 'en': en, 'cn': cn}

# Run comparisons
results = {}
for cn_name, en_url in FILES:
    r = compare(cn_name, en_url)
    if r:
        results[r['name']] = r

# Detailed report
print("\n\n" + "="*80)
print("DETAILED MISSING CONTENT REPORT")
print("="*80)

for name, r in sorted(results.items()):
    if not r['issues']:
        continue

    print(f"\n### {name}")
    en = r['en']
    cn = r['cn']

    for itype, idata in r['issues']:
        if itype == "missing_sa":
            print(f"  Missing security advisories:")
            for sa in idata:
                ctx = re.search(re.escape(sa) + r'.{0,200}', en)
                if ctx:
                    print(f"    - {sa}: {clean(ctx.group(0))[:200]}")
        elif itype == "missing_keywords":
            print(f"  Missing keywords/options:")
            for kw in idata:
                ctx = re.search(re.escape(kw) + r'.{0,150}', en)
                if ctx:
                    print(f"    - {kw}: {clean(ctx.group(0))[:200]}")

# Summary
print("\n\n" + "="*80)
print("SUMMARY")
print("="*80)
with_issues = sum(1 for r in results.values() if r['issues'])
print(f"Checked {len(results)} files, {with_issues} have missing content issues")

for name, r in sorted(results.items()):
    if r['issues']:
        print(f"\n  {name}:")
        for itype, idata in r['issues']:
            if itype == "missing_sa":
                print(f"    - Missing SAs: {', '.join(idata)}")
            elif itype == "missing_keywords":
                print(f"    - Missing keywords: {', '.join(idata)}")
            elif itype == "low_para_ratio":
                print(f"    - Low paragraph ratio: {idata}")
            elif itype == "code_block_mismatch":
                print(f"    - Code blocks mismatch: {idata}")
            elif itype == "missing_man_refs":
                print(f"    - Missing man refs: {idata}")

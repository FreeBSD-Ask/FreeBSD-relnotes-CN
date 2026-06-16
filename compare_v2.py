#!/usr/bin/env python3
import re, os, urllib.request, ssl, sys

sys.stdout.reconfigure(encoding='utf-8')

FILES = [
    ("5.0.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.0R/relnotes-i386.adoc"),
    ("5.1.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.1R/relnotes-i386.adoc"),
    ("5.2-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.2R/relnotes-amd64.adoc"),
    ("5.2.1-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.2.1R/relnotes-amd64.adoc"),
    ("5.3-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.3R/relnotes-amd64.adoc"),
    ("5.4-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.4R/relnotes-amd64.adoc"),
    ("5.5-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.5R/relnotes-amd64.adoc"),
    ("4.0.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.0R/relnotes-i386.adoc"),
    ("4.1.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.1R/relnotes-i386.adoc"),
    ("4.1.1.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.1.1R/relnotes-i386.adoc"),
    ("4.2.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.2R/relnotes-i386.adoc"),
    ("4.3.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.3R/relnotes.adoc"),
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

BASE = r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN"

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
        'IPSEC', 'INET6', 'P1003_1B', 'UCONSOLE', 'USER_LDT',
        'MAC', 'I386_CPU', 'GEOM_VOL', 'ATARaid',
    ]
    missing_kw = [kw for kw in keywords if kw in en and kw not in cn]
    if missing_kw:
        issues.append(("missing_keywords", missing_kw))

    # 3. Paragraph count
    en_paras = [clean(m.group(1)) for m in re.finditer(r'<p[^>]*>(.*?)</p>', en, re.DOTALL) if len(clean(m.group(1))) > 30]
    cn_lines = cn.split('\n')
    cn_para_count = 0
    cur = []
    in_cb = False
    for line in cn_lines:
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
    if ratio < 0.6:
        issues.append(("low_para_ratio", f"EN={en_para_count}, CN={cn_para_count}, ratio={ratio:.0%}"))

    # 4. Code blocks
    en_code = len(re.findall(r'<pre[^>]*>', en))
    cn_code = len(re.findall(r'```', cn)) // 2
    if en_code > cn_code:
        issues.append(("code_block_mismatch", f"EN={en_code}, CN={cn_code}"))

    # 5. Man page refs
    en_man = set(re.findall(r'man\.cgi\?query=(\w+)', en))
    cn_man = set(re.findall(r'man\.cgi\?query=(\w+)', cn))
    if en_man and len(cn_man) < len(en_man) * 0.4:
        issues.append(("low_man_refs", f"EN={len(en_man)}, CN={len(cn_man)}"))

    # 6. Heading count
    en_h = len(re.findall(r'<h[234][^>]*>', en))
    cn_h = len(re.findall(r'^#{1,5}\s+', cn, re.MULTILINE))
    if en_h > 0 and cn_h < en_h * 0.6:
        issues.append(("low_heading_count", f"EN={en_h}, CN={cn_h}"))

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
            elif itype == "low_man_refs":
                print(f"    * Low man page refs: {idata}")
            elif itype == "low_heading_count":
                print(f"    * Low heading count: {idata}")
    else:
        print(f"  No major issues found")

    print(f"  Stats: EN({en_h}h, {en_para_count}p, {en_code}cb, {len(en_sa)}sa, {len(en_man)}man)")
    print(f"         CN({cn_h}h, {cn_para_count}p, {cn_code}cb, {len(cn_sa)}sa, {len(cn_man)}man)")

    return {'name': cn_name, 'issues': issues, 'en': en, 'cn': cn}

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
                ctx = re.search(re.escape(sa) + r'[^\n]{0,200}', en)
                if ctx:
                    print(f"    - {sa}: {clean(ctx.group(0))[:200]}")
        elif itype == "missing_keywords":
            print(f"  Missing keywords/options:")
            for kw in idata:
                ctx = re.search(re.escape(kw) + r'[^\n]{0,150}', en)
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
            elif itype == "low_man_refs":
                print(f"    - Low man refs: {idata}")
            elif itype == "low_heading_count":
                print(f"    - Low heading count: {idata}")

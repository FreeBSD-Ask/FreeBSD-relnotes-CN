#!/usr/bin/env python3
"""Detailed comparison - check specific content items."""
import re, os, urllib.request, ssl, sys

sys.stdout.reconfigure(encoding='utf-8')
BASE = r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN"

FILES = [
    ("5.0.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.0R/relnotes-i386.adoc"),
    ("5.1.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.1R/relnotes-i386.adoc"),
    ("5.2-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.2R/relnotes-amd64.adoc"),
    ("5.2.1-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.2.1R/relnotes-amd64.adoc"),
    ("5.3-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.3R/relnotes-amd64.adoc"),
    ("5.4-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.4R/relnotes-amd64.adoc"),
    ("5.5-amd64.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/5.5R/relnotes-amd64.adoc"),
    ("4.0.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.0R/notes.adoc"),
    ("4.1.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.1R/notes.adoc"),
    ("4.1.1.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.1.1R/notes.adoc"),
    ("4.2.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.2R/notes.adoc"),
    ("4.3.md", "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.3R/notes.adoc"),
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

def extract_driver_names(en):
    """Extract driver names like dc(4), ata(4), etc. from English source."""
    # HTML format: man.cgi?query=dc&sektion=4
    drivers = set(re.findall(r'man\.cgi\?query=(\w+)&sektion=(\d+)', en))
    # Plain text format: driver(4)
    drivers.update(re.findall(r'\b(\w+)\((\d+)\)', en))
    return drivers

def extract_software_versions(en):
    """Extract software version mentions like GCC 3.2.1, BIND 8.3.3, etc."""
    # HTML format: <b>GCC</b> and version numbers nearby
    versions = []
    # Find patterns like "GCC 3.2.1", "BIND 8.3.3", etc.
    for m in re.finditer(r'(?:GCC|BIND|OpenSSH|OpenSSL|sendmail|Perl|Python|Heimdal|IPFilter|ncurses|texinfo|groff|NTP|CVS|gdb|zlib|libpcap|tcpdump|less|tcsh|GNU\s+\w+)\s+[\d]+[\.\d]*', en, re.IGNORECASE):
        versions.append(clean(m.group(0)))
    # Also check <b> tagged software names
    for m in re.finditer(r'<b[^>]*>([\w\s.-]+)</b>\s+(?:has been|has|is now|was|updated|upgraded|imported|replaced|removed|added)', en, re.IGNORECASE):
        versions.append(clean(m.group(0)))
    return set(versions)

def detailed_compare(cn_name, en_url):
    cn_path = os.path.join(BASE, cn_name)
    print(f"\n### {cn_name}")

    try:
        en = fetch(en_url)
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

    try:
        with open(cn_path, 'r', encoding='utf-8') as f:
            cn = f.read()
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

    issues = []

    # 1. Security advisories
    en_sa = set(re.findall(r'FreeBSD-SA-\d{2}:\d{2}', en))
    cn_sa = set(re.findall(r'FreeBSD-SA-\d{2}:\d{2}', cn))
    missing_sa = en_sa - cn_sa
    if missing_sa:
        issues.append(f"Missing security advisories: {', '.join(sorted(missing_sa))}")

    # 2. Driver/man page references
    en_drivers = set(re.findall(r'man\.cgi\?query=(\w+)&sektion=(\d+)', en))
    cn_drivers = set(re.findall(r'man\.cgi\?query=(\w+)&sektion=(\d+)', cn))
    missing_drivers = en_drivers - cn_drivers
    if len(missing_drivers) > 3:
        missing_names = [f"{d[0]}({d[1]})" for d in sorted(missing_drivers)]
        issues.append(f"Missing man page refs ({len(missing_drivers)}): {', '.join(missing_names[:20])}")

    # 3. Code blocks (pre tags in HTML)
    en_code_blocks = re.findall(r'<pre[^>]*>(.*?)</pre>', en, re.DOTALL)
    cn_code_blocks = re.findall(r'```[\w]*\n(.*?)```', cn, re.DOTALL)
    if len(en_code_blocks) > len(cn_code_blocks):
        # Check what the code blocks contain
        for i, cb in enumerate(en_code_blocks):
            cb_text = clean(cb)
            if cb_text and not any(cb_text[:30] in c for c in [clean(c) for c in cn_code_blocks]):
                issues.append(f"Possible missing code block: {cb_text[:100]}")

    # 4. Important kernel options
    options = re.findall(r'options\s+(\w+)', en)
    missing_opts = [o for o in set(options) if o not in cn and len(o) > 3]
    if missing_opts:
        issues.append(f"Missing kernel options: {', '.join(sorted(set(missing_opts)))}")

    # 5. Device names mentioned in context
    device_names = re.findall(r'device\s+(\w+)', en)
    missing_devices = [d for d in set(device_names) if d not in cn and len(d) > 3]
    if missing_devices:
        issues.append(f"Missing device names: {', '.join(sorted(set(missing_devices)))}")

    # 6. sysctl variable names
    sysctl_names = re.findall(r'([\w.]+\.(?:enable|disable|mode|limit|count|size|rate|delay|timeout|flags|mask|type|level|debug|prof))', en)
    missing_sysctl = [s for s in set(sysctl_names) if s not in cn]
    if len(missing_sysctl) > 5:
        issues.append(f"Missing sysctl variables ({len(missing_sysctl)}): {', '.join(sorted(missing_sysctl)[:15])}")

    # 7. For plain text format (4.0-4.3), check section completeness
    # Count section headings in English
    en_sections = re.findall(r'^\d+\.\d*\.?\s+\w', en, re.MULTILINE)
    cn_sections = re.findall(r'^#+\s+\d+\.?\d*\.?\s+', cn, re.MULTILINE)
    # Also check for Chinese section headings
    cn_cn_sections = re.findall(r'^#+\s+', cn, re.MULTILINE)

    if issues:
        for issue in issues:
            print(f"  - {issue}")
    else:
        print(f"  OK")

    return {'name': cn_name, 'issues': issues, 'en': en, 'cn': cn}

# Run
results = {}
for cn_name, en_url in FILES:
    r = detailed_compare(cn_name, en_url)
    if r:
        results[r['name']] = r

# Final summary
print("\n\n" + "="*80)
print("FINAL SUMMARY")
print("="*80)
total_issues = 0
for name, r in sorted(results.items()):
    if r['issues']:
        total_issues += len(r['issues'])
        print(f"\n{name}:")
        for issue in r['issues']:
            print(f"  - {issue}")

print(f"\nTotal: {len(results)} files checked, {sum(1 for r in results.values() if r['issues'])} files with issues, {total_issues} total issues")

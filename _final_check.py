import re

with open(r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\_en_9.3.adoc', 'r', encoding='utf-8') as f:
    en = f.read()

with open(r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\9.3.md', 'r', encoding='utf-8') as f:
    cn = f.read()

# Check all revision-numbered paragraphs are present
en_revs = set(re.findall(r'r\d{5,6}', en))
cn_revs = set(re.findall(r'r\d{5,6}', cn))
missing_revs = en_revs - cn_revs
print(f'Total English revisions: {len(en_revs)}')
print(f'Total Chinese revisions: {len(cn_revs)}')
print(f'Missing revisions: {sorted(missing_revs) if missing_revs else "None"}')

# Check security advisories
en_sa = set(re.findall(r'FreeBSD-SA-\d+:\d+\.\w+', en))
cn_sa = set(re.findall(r'FreeBSD-SA-\d+:\d+\.\w+', cn))
missing_sa = en_sa - cn_sa
print(f'\nSecurity Advisories: EN={len(en_sa)}, CN={len(cn_sa)}, Missing={sorted(missing_sa) if missing_sa else "None"}')

# Check sponsor mentions
en_sponsors = re.findall(r'\(Sponsored by.*?\)', en)
cn_sponsors = re.findall(r'（由.*?赞助）', cn)
print(f'\nSponsor mentions: EN={len(en_sponsors)}, CN={len(cn_sponsors)}')

# Check contributed mentions
en_contrib = re.findall(r'\(Contributed.*?\)', en)
cn_contrib = re.findall(r'（由.*?提供/贡献）', cn)
print(f'Contributed mentions: EN={len(en_contrib)}, CN={len(cn_contrib)}')

# Check sections
en_sections = re.findall(r'^== (.+)', en, re.MULTILINE)
cn_sections = re.findall(r'^## (.+)', cn, re.MULTILINE)
print(f'\nEnglish sections ({len(en_sections)}):')
for s in en_sections:
    print(f'  - {s}')
print(f'Chinese sections ({len(cn_sections)}):')
for s in cn_sections:
    print(f'  - {s}')

# Check the specific 'latest' issue
print('\n=== Specific content issue: latest repository name ===')
en_lines = en.split('\n')
cn_lines = cn.split('\n')
for i, line in enumerate(en_lines):
    if 'KDE4' in line and 'latest' in line:
        print(f'EN: {line.strip()[:200]}')
for i, line in enumerate(cn_lines):
    if 'KDE4' in line:
        print(f'CN: {line.strip()[:200]}')

# Check for inline code formatting differences (paths using bold instead of code)
print('\n=== Inline code formatting differences ===')
en_code = set(re.findall(r'`([^`]+)`', en))
cn_code = set(re.findall(r'`([^`]+)`', cn))
missing_code = en_code - cn_code
# Filter out whitespace-only differences
real_missing = []
for c in sorted(missing_code):
    # Check if a version without extra spaces exists
    normalized = re.sub(r'\s+', ' ', c).strip()
    if normalized not in cn_code and c not in cn:
        # Check if it's present as bold text instead
        if f'**{c}**' in cn:
            real_missing.append((c, 'present as bold instead of code'))
        else:
            real_missing.append((c, 'NOT FOUND'))

if real_missing:
    for item, status in real_missing:
        print(f'  `{item}`: {status}')
else:
    print('  No real missing inline code (only formatting differences)')

print('\n=== DONE ===')

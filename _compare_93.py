import re

with open(r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\_en_9.3.adoc', 'r', encoding='utf-8') as f:
    en = f.read()

with open(r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\9.3.md', 'r', encoding='utf-8') as f:
    cn = f.read()

# Extract all inline code from English
en_code = sorted(set(re.findall(r'`([^`]+)`', en)))
cn_code = sorted(set(re.findall(r'`([^`]+)`', cn)))

print('=== Inline code comparison ===')
print(f'English unique inline code count: {len(en_code)}')
print(f'Chinese unique inline code count: {len(cn_code)}')

missing_code = set(en_code) - set(cn_code)
extra_code = set(cn_code) - set(en_code)

if missing_code:
    print(f'\nMissing inline code in Chinese ({len(missing_code)}):')
    for c in sorted(missing_code):
        print(f'  `{c}`')

if extra_code:
    print(f'\nExtra inline code in Chinese ({len(extra_code)}):')
    for c in sorted(extra_code):
        print(f'  `{c}`')

# Count occurrences of each inline code
print('\n=== Inline code occurrence comparison (mismatches only) ===')
for code in sorted(set(en_code) | set(cn_code)):
    en_count = en.count(f'`{code}`')
    cn_count = cn.count(f'`{code}`')
    if en_count != cn_count:
        print(f'  `{code}`: EN={en_count}, CN={cn_count}')

# Now do a detailed paragraph-level comparison for each section
print('\n' + '='*60)
print('DETAILED SECTION-BY-SECTION COMPARISON')
print('='*60)

en_lines = en.split('\n')
cn_lines = cn.split('\n')

# Map English sections to their content
def extract_sections(lines, header_prefix, skip_prefixes=None):
    sections = []
    current_section = None
    current_content = []
    for line in lines:
        if line.startswith(header_prefix) and not line.startswith(header_prefix + '='):
            if current_section is not None:
                sections.append((current_section, current_content))
            current_section = line.strip(header_prefix + ' ').strip()
            current_content = []
        elif line.strip() and skip_prefixes and any(line.strip().startswith(sp) for sp in skip_prefixes):
            continue
        elif line.strip():
            current_content.append(line.strip())
    if current_section is not None:
        sections.append((current_section, current_content))
    return sections

en_sections = extract_sections(en_lines, '==', ['---', '|===', '[[', 'include::', '[cols'])
cn_sections = extract_sections(cn_lines, '##', ['---', '| :---'])

# Compare section by section using revision numbers as anchors
print('\n--- Checking each revision number has corresponding content ---')
en_revs = re.findall(r'r\d{5,6}', en)
cn_revs = re.findall(r'r\d{5,6}', cn)

# For each English revision, find the paragraph and check if Chinese has it
en_paragraphs = {}
current_para = ''
for line in en_lines:
    if line.strip() == '':
        if current_para.strip():
            revs = re.findall(r'r\d{5,6}', current_para)
            for r in revs:
                en_paragraphs[r] = current_para.strip()
        current_para = ''
    else:
        current_para += ' ' + line.strip()

cn_paragraphs = {}
current_para = ''
for line in cn_lines:
    if line.strip() == '':
        if current_para.strip():
            revs = re.findall(r'r\d{5,6}', current_para)
            for r in revs:
                cn_paragraphs[r] = current_para.strip()
        current_para = ''
    else:
        current_para += ' ' + line.strip()

# Check for missing paragraphs by revision number
all_en_revs = set(re.findall(r'r\d{5,6}', en))
all_cn_revs = set(re.findall(r'r\d{5,6}', cn))

missing_revs = all_en_revs - all_cn_revs
if missing_revs:
    print(f'\nMISSING revisions in Chinese: {sorted(missing_revs)}')
else:
    print('\nAll revision numbers present in Chinese translation.')

# Check for "Note:" and "Important:" blocks in English
print('\n--- Checking for Note/Important blocks ---')
note_pattern = re.compile(r'(Note:|Important:|WARNING:|CAUTION:)', re.IGNORECASE)
for i, line in enumerate(en_lines):
    if note_pattern.search(line):
        print(f'  EN L{i+1}: {line.strip()[:120]}')

for i, line in enumerate(cn_lines):
    if '注意' in line or '重要' in line or '警告' in line:
        if line.startswith('#') or line.startswith('|'):
            continue
        print(f'  CN L{i+1}: {line.strip()[:120]}')

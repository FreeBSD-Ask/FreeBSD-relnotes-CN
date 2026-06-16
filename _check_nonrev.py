import re

with open(r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\_en_9.3.adoc', 'r', encoding='utf-8') as f:
    en = f.read()

with open(r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\9.3.md', 'r', encoding='utf-8') as f:
    cn = f.read()

en_lines = en.split('\n')

# Extract non-revision paragraphs from English
print('=== English non-revision content paragraphs ===')
for i, line in enumerate(en_lines):
    stripped = line.strip()
    if not stripped:
        continue
    if stripped.startswith('---') or stripped.startswith('|===') or stripped.startswith('[['):
        continue
    if stripped.startswith('include::') or stripped.startswith('[cols') or stripped.startswith('title:') or stripped.startswith('sidenav:'):
        continue
    if stripped.startswith('== ') or stripped == "'''''":
        continue
    if stripped.startswith('Table of Contents') or stripped.startswith('* ' + '<<'):
        continue
    if stripped.startswith('|') and not stripped.startswith('|==='):
        continue
    if stripped == '+':
        continue
    if re.findall(r'r\d{5,6}', stripped):
        continue
    print(f'  L{i+1}: {stripped[:200]}')

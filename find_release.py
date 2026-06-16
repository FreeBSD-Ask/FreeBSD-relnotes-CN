#!/usr/bin/env python3
"""查找"发布版"（不匹配"发布版本"）的实例"""
import re, os

base = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN'
for fname in sorted(os.listdir(base)):
    if not fname.endswith('.md') or fname in ('SUMMARY.md', 'README.md', 'CHANGELOG.md'):
        continue
    fpath = os.path.join(base, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('```'):
            continue
        for m in re.finditer(r'发布版(?!本)', line):
            ctx = stripped[:150]
            print(f'{fname}:{i}: {m.group()!r}')
            print(f'  -> {ctx}')
            print()
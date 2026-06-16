#!/usr/bin/env python3
"""
统一混合格式：**`text`** -> 根据内容类型决定格式
- 命令名/选项/驱动名 -> `text`（反引号）
- 路径/文件名/邮箱 -> **text**（加粗）
"""

import os
import re
import glob

BASE_DIR = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN'
EXCLUDE_FILES = {'README.md', 'SUMMARY.md', 'CHANGELOG.md', 'test_table.md', '15.1-en.md'}

# 应使用反引号的内容（命令名、选项、驱动名等）
BACKTICK_CONTENTS = {
    'send-pr', 'sendbug', 'brandelf', 'help',
    'ex', 'de', 'ed', 'async',
    'lsdev(8)',
}

def is_in_code_block(lines, line_idx):
    code_block_count = 0
    for i in range(line_idx):
        if lines[i].strip().startswith('```'):
            code_block_count += 1
    return code_block_count % 2 == 1


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    modified = False
    changes = []

    for i, line in enumerate(lines):
        if is_in_code_block(lines, i):
            continue

        original_line = line

        # 匹配 **`text`** 模式
        pattern = r'\*\*`([^`]+)`\*\*'
        matches = list(re.finditer(pattern, line))
        for m in reversed(matches):
            text = m.group(1)
            old = m.group(0)

            if text in BACKTICK_CONTENTS:
                # 命令名/选项/驱动名 -> 反引号
                new = f'`{text}`'
            elif text.startswith('/') or '.' in text.split('/')[-1]:
                # 路径或文件名 -> 加粗
                new = f'**{text}**'
            elif '@' in text:
                # 邮箱地址 -> 加粗
                new = f'**{text}**'
            else:
                # 默认：命令名/工具名 -> 反引号
                new = f'`{text}`'

            line = line[:m.start()] + new + line[m.end():]
            changes.append(f'  L{i+1}: {old} -> {new}')

        if line != original_line:
            lines[i] = line
            modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(lines))
        print(f'{os.path.basename(filepath)}: Modified')
        for c in changes:
            print(c)
    else:
        print(f'{os.path.basename(filepath)}: No changes')

    return modified


def main():
    md_files = glob.glob(os.path.join(BASE_DIR, '*.md'))
    total_modified = 0

    for filepath in sorted(md_files):
        if os.path.basename(filepath) in EXCLUDE_FILES:
            continue
        if filepath.startswith(os.path.join(BASE_DIR, '.github')):
            continue
        if process_file(filepath):
            total_modified += 1

    print(f'\nTotal files modified: {total_modified}')


if __name__ == '__main__':
    main()

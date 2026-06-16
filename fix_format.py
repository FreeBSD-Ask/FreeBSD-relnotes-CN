#!/usr/bin/env python3
"""
统一格式脚本：
- 路径（以 / 开头的）、文件名（.conf, .ko, .db, .html, .h, .c, .so 等）从反引号改为加粗
- 内核模块文件（.ko）从反引号改为加粗
- 不修改代码块内的内容
- 不修改混合格式（**`text`**）的情况
"""

import os
import re
import glob

BASE_DIR = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN'

# 排除的文件
EXCLUDE_FILES = {'README.md', 'SUMMARY.md', 'CHANGELOG.md', 'test_table.md', '15.1-en.md'}

# 文件扩展名模式（这些是文件名/路径，应使用加粗）
FILE_EXTENSIONS = r'\.(conf|ko|db|html|h|c|so|so\.\d+|py|sh|txt|xml|json|yaml|yml|md|log|pid|rc|efi|img|bin|sys|dat|cfg|sample|distinfo|pkg|desc|messages|mtree|pl|pm|t|pod|spec|ini|properties|toml|list|manifest|version|release|lock|cache|index|cert|key|pem|crt|csr|jks|p12|pfx|der|cer|crl|srl|stf|tbl|md5|sha256|sha512|sig|asc|sign|bz2|gz|xz|zst|tgz|txz|tbz|tbz2|zip|tar|cpio|rpm|deb|pkg|apk|msi|exe|dll|sys|drv|inf|cat|cab|iso|img|vmdk|vdi|qcow2|raw|vhd|vhdx)'

def is_in_code_block(lines, line_idx):
    """检查某行是否在代码块内"""
    code_block_count = 0
    for i in range(line_idx):
        if lines[i].strip().startswith('```'):
            code_block_count += 1
    return code_block_count % 2 == 1


def process_file(filepath):
    """处理单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    modified = False
    changes = []

    for i, line in enumerate(lines):
        if is_in_code_block(lines, i):
            continue

        original_line = line

        # 模式1: `/path/to/something` -> **/path/to/something**
        # 匹配反引号包裹的路径（以/开头）
        pattern1 = r'`(/[^`]+)`'
        matches1 = list(re.finditer(pattern1, line))
        for m in reversed(matches1):
            path_content = m.group(1)
            # 跳过 man page 链接中的路径（如 man.cgi?query=...）
            if 'man.cgi' in path_content:
                continue
            # 跳过 URL
            if path_content.startswith('//') or '://' in path_content:
                continue
            # 替换为加粗
            old = m.group(0)
            new = f'**{path_content}**'
            line = line[:m.start()] + new + line[m.end():]
            changes.append(f'  L{i+1}: {old} -> {new}')

        # 模式2: `filename.conf` 或 `filename.ko` 等（不以/开头的文件名）
        # 匹配反引号包裹的文件名（带扩展名）
        pattern2 = r'`([^`/\s]+\.(conf|ko|db|html|efi|so(\.\d+)?))`'
        matches2 = list(re.finditer(pattern2, line))
        for m in reversed(matches2):
            filename = m.group(1)
            old = m.group(0)
            new = f'**{filename}**'
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

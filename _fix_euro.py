# -*- coding: utf-8 -*-
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def fix_file(filepath, replacements):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return 0
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    count = 0
    for old, new in replacements:
        found = content.count(old)
        if found:
            content = content.replace(old, new)
            count += found
            print(f"  [{os.path.basename(filepath)}] {found}x: '{old[:60]}' -> '{new[:60]}'")
        else:
            print(f"  [{os.path.basename(filepath)}] NOT FOUND: '{old[:60]}'")
    if count > 0:
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
    return count

total = 0

# 14.1
total += fix_file(
    r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\freebsd-14.1-fa-hang-shuo-ming.md',
    [
        ('更多有关下载该（及其他）FreeBSD\u201cRELEASE\u201d版本的信息，请参阅',
         '下载该（及其他）FreeBSD\u201cRELEASE\u201d版本的信息，请参阅'),
    ]
)

# 14.2
total += fix_file(
    r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\freebsd-14.2.md',
    [
        ('有关获取此版本（及其他版本）FreeBSD的更多信息，请参阅',
         '获取此版本（及其他版本）FreeBSD的更多信息，请参阅'),
        ('有关该分支中预编译的二进制\u201cRELEASE\u201d发行版的信息，请参见',
         '该分支中预编译的二进制\u201cRELEASE\u201d发行版的信息，请参见'),
    ]
)

# 14.3
total += fix_file(
    r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\14.3.md',
    [
        ('有关特定版本升级的详细信息，请参阅',
         '特定版本升级的详细信息，请参阅'),
    ]
)

# 14.4
total += fix_file(
    r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\14.4.md',
    [
        ('有关获取此（或其他）FreeBSD\u201cRELEASE\u201d发行版的更多信息，请参见',
         '获取此（或其他）FreeBSD\u201cRELEASE\u201d发行版的更多信息，请参见'),
        ('有关该分支上预构建二进制\u201cRELEASE\u201d发行版的信息，请参见',
         '该分支上预构建二进制\u201cRELEASE\u201d发行版的信息，请参见'),
    ]
)

# 15.0
total += fix_file(
    r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\15.0.md',
    [
        ('有关更多细节，请参阅',
         '更多细节请参阅'),
        ('有关如何使用',
         '如何使用'),
        ('有关MAC的介绍，请参见',
         'MAC的介绍请参见'),
        ('详细信息请参见',
         '详见'),
    ]
)

# 15.1
total += fix_file(
    r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\15.1.md',
    [
    ]
)

print(f'\nTotal: {total} replacements')
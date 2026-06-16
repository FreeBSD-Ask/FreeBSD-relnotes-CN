import sys
filepath = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\6.0-amd64.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

modifications = [
    # 1. Line 95: 倒装句
    ('[memguard(9)](http://www.freebsd.org/cgi/man.cgi?query=memguard&sektion=9&manpath=FreeBSD+6.0-RELEASE)，一种旨在帮助检测\u201c释放后篡改\u201d场景的内核内存分配器，已添加。',
     '新增了[memguard(9)](http://www.freebsd.org/cgi/man.cgi?query=memguard&sektion=9&manpath=FreeBSD+6.0-RELEASE)，一种旨在帮助检测\u201c释放后篡改\u201d场景的内核内存分配器。'),
    # 2. Line 196: 倒装句 - remove trailing 已新增
    ('和 [ural(4)](http://www.freebsd.org/cgi/man.cgi?query=ural&sektion=4&manpath=FreeBSD+6.0-RELEASE)（适用于 Ralink Technology RT2500USB）驱动已新增。',
     '和 [ural(4)](http://www.freebsd.org/cgi/man.cgi?query=ural&sektion=4&manpath=FreeBSD+6.0-RELEASE)（适用于 Ralink Technology RT2500USB）驱动。'),
    # 3. Line 216: URL误译
    ('ftp://ftp.freebsd.org/pub/FreeBSD/\u52d8\u8bef/notices/FreeBSD-EN-05:02.sk.asc',
     'ftp://ftp.freebsd.org/pub/FreeBSD/ERRATA/notices/FreeBSD-EN-05:02.sk.asc'),
    # 4. Line 321: URL误译
    ('ftp://ftp.freebsd.org/pub/FreeBSD/\u52d8\u8bef/notices/FreeBSD-EN-05:01.nfs.asc',
     'ftp://ftp.freebsd.org/pub/FreeBSD/ERRATA/notices/FreeBSD-EN-05:01.nfs.asc'),
    # 5. Line 427: 倒装句
    ('程序 [powerd(8)](http://www.freebsd.org/cgi/man.cgi?query=powerd&sektion=8&manpath=FreeBSD+6.0-RELEASE) 用于管理电源消耗，已新增。',
     '新增了[powerd(8)](http://www.freebsd.org/cgi/man.cgi?query=powerd&sektion=8&manpath=FreeBSD+6.0-RELEASE)程序，用于管理电源消耗。'),
    # 6. Line 479: 倒装句
    ('命令 [tcpdrop(8)](http://www.freebsd.org/cgi/man.cgi?query=tcpdrop&sektion=8&manpath=FreeBSD+6.0-RELEASE) 用于关闭选定的 TCP 连接，已新增。',
     '新增了[tcpdrop(8)](http://www.freebsd.org/cgi/man.cgi?query=tcpdrop&sektion=8&manpath=FreeBSD+6.0-RELEASE)命令，用于关闭选定的 TCP 连接。'),
]

count = 0
for old, new in modifications:
    if old in content:
        content = content.replace(old, new, 1)
        count += 1
        print(f'OK: {old[:40]}... -> {new[:40]}...')
    else:
        print(f'SKIP (not found): {old[:40]}...')

with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)
print(f'\nTotal: {count}/{len(modifications)} modifications applied')

import sys

sys.stdout.reconfigure(encoding='utf-8')

# Fix 1: 10.1.md - Add missing [ia64] serial terminal paragraph
filepath = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\10.1.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old = '已从 FreeBSD-CURRENT 合并 [nfsd(8)](http://www.freebsd.org/cgi/man.cgi?query=nfsd&sektion=8) 服务器的更新，支持 RFC5661 的 4.1 版本。[(r269398)](http://svn.freebsd.org/viewvc/base?view=revision&revision=269398)\n\n[ping6(8)]'

new = '已从 FreeBSD-CURRENT 合并 [nfsd(8)](http://www.freebsd.org/cgi/man.cgi?query=nfsd&sektion=8) 服务器的更新，支持 RFC5661 的 4.1 版本。[(r269398)](http://svn.freebsd.org/viewvc/base?view=revision&revision=269398)\n\n[ia64] 串口终端 `ttyu0` 和 `ttyu1` 已在 [ttys(5)](http://www.freebsd.org/cgi/man.cgi?query=ttys&sektion=5) 中默认更新为 `onifconsole`，根据平台的不同，其中任一均可作为串口控制台。[(r269432)](http://svn.freebsd.org/viewvc/base?view=revision&revision=269432)\n\n[ping6(8)]'

if old in content:
    content = content.replace(old, new, 1)
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print('10.1.md: Successfully inserted [ia64] paragraph')
else:
    print('10.1.md: Pattern not found!')

# Fix 2: 10.3.md - Add missing [arm] imxwdt driver paragraph
filepath = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\10.3.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old = '### 设备驱动程序\n\n[puc(4)]'

new = '### 设备驱动程序\n\n[arm] 已修复 `imxwdt` 驱动程序，该驱动程序支持 Freescale i.MX 看门狗。 [(r287079)](http://svn.freebsd.org/viewvc/base?view=revision&revision=287079)\n\n[puc(4)]'

if old in content:
    content = content.replace(old, new, 1)
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print('10.3.md: Successfully inserted [arm] imxwdt paragraph')
else:
    print('10.3.md: Pattern not found!')

# Fix 3: 9.3.md - Fix KDE4 entry to include 'latest' repository name
filepath = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\9.3.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old = '默认的 `pkg(8)` 仓库中没有 KDE4 的软件包，但可以在 `new_xorg` 仓库中找到。'

new = '默认的（`latest`）[pkg(8)](https://man.freebsd.org/cgi/man.cgi?query=pkg&sektion=8&format=html) 仓库中没有 KDE4 的软件包，但可以在 `new_xorg` 仓库中找到。'

if old in content:
    content = content.replace(old, new, 1)
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print('9.3.md: Successfully fixed KDE4 entry')
else:
    print('9.3.md: Pattern not found!')

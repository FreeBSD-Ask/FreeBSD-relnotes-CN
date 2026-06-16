import sys
sys.stdout.reconfigure(encoding='utf-8')

count = 0

# 1. freebsd-13.3.md L152: "进行了诸多稳定性修复" -> restructure
filepath = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\freebsd-13.3.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
old = '对原生和基于 LinuxKPI 的无线驱动程序进行了诸多稳定性修复'
new = '修复了原生和基于 LinuxKPI 的无线驱动程序的诸多稳定性问题'
if old in content:
    content = content.replace(old, new, 1)
    count += 1
    print('freebsd-13.3.md: Fixed L152')
else:
    print('freebsd-13.3.md L152: Pattern not found')
with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

# 2. freebsd-14.0-fa-hang-shuo-ming.md L15: "有关此分支" -> "此分支"
filepath = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\freebsd-14.0-fa-hang-shuo-ming.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
old = '找到有关此分支上的预构建二进制发行版的信息'
new = '找到此分支上预构建二进制发行版的信息'
if old in content:
    content = content.replace(old, new)
    count += 1
    print('freebsd-14.0: Fixed L15/L17 (有关此分支)')
else:
    print('freebsd-14.0 L15: Pattern not found')

# 3. freebsd-14.0 L501: "进行了许多调整和清理" -> "做了许多调整和清理"
old2 = '对 [hier(7)](https://man.freebsd.org/cgi/man.cgi?query=hier&sektion=7&format=html) 页面进行了许多调整和清理'
new2 = '对 [hier(7)](https://man.freebsd.org/cgi/man.cgi?query=hier&sektion=7&format=html) 页面做了许多调整和清理'
if old2 in content:
    content = content.replace(old2, new2, 1)
    count += 1
    print('freebsd-14.0: Fixed L501 (进行了)')
else:
    print('freebsd-14.0 L501: Pattern not found')
with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

# 4. freebsd-14.1-fa-hang-shuo-ming.md L141: "已进行了许多稳定性改进" -> "经过许多稳定性改进"
filepath = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\freebsd-14.1-fa-hang-shuo-ming.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
old = '驱动程序已进行了许多稳定性改进'
new = '驱动程序经过许多稳定性改进'
if old in content:
    content = content.replace(old, new, 1)
    count += 1
    print('freebsd-14.1: Fixed L141')
else:
    print('freebsd-14.1 L141: Pattern not found')
with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

# 5. 13.4.md L13: "有关此分支" -> "此分支"
filepath = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\13.4.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
old = '有关此分支上预编译的二进制'
new = '此分支上预编译的二进制'
if old in content:
    content = content.replace(old, new, 1)
    count += 1
    print('13.4.md: Fixed L13 (有关此分支)')
else:
    print('13.4.md L13: Pattern not found')

# 6. 13.4.md L97: "进行了许多稳定性修复" -> restructure
old2 = '对原生及基于 LinuxKPI 的无线驱动程序进行了许多稳定性修复'
new2 = '修复了原生及基于 LinuxKPI 的无线驱动程序的许多稳定性问题'
if old2 in content:
    content = content.replace(old2, new2, 1)
    count += 1
    print('13.4.md: Fixed L97 (进行了)')
else:
    print('13.4.md L97: Pattern not found')
with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

# 7. 14.3.md L277: "已进行了修订" -> "已修订"
filepath = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\14.3.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
old = '已进行了修订'
new = '已修订'
if old in content:
    content = content.replace(old, new, 1)
    count += 1
    print('14.3.md: Fixed L277')
else:
    print('14.3.md L277: Pattern not found')
with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

# 8. 14.4.md L80: "还进行了若干内部正确性和稳健性改进" -> "还做了若干内部正确性和稳健性改进"
filepath = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\14.4.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
old = '还进行了若干内部正确性和稳健性改进'
new = '还做了若干内部正确性和稳健性改进'
if old in content:
    content = content.replace(old, new, 1)
    count += 1
    print('14.4.md: Fixed L80')
else:
    print('14.4.md L80: Pattern not found')
with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print(f'\nTotal fixes: {count}')

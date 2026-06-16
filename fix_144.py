import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\14.4.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old = '对虚拟机初始化器 [nuageinit(7)](https://man.freebsd.org/cgi/man.cgi?query=nuageinit&sektion=7&format=html) 进行了多项改进'
new = '对虚拟机初始化器 [nuageinit(7)](https://man.freebsd.org/cgi/man.cgi?query=nuageinit&sektion=7&format=html) 做了多项改进'

if old in content:
    content = content.replace(old, new, 1)
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print('14.4.md: Fixed L170')
else:
    print('14.4.md L170: Pattern not found')

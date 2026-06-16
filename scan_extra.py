import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN'
files = [
    'freebsd-13.1-fa-hang-shuo-ming.md',
    'freebsd-13.2-fa-hang-shuo-ming.md',
    'freebsd-13.3.md',
    'freebsd-14.0-fa-hang-shuo-ming.md',
    'freebsd-14.1-fa-hang-shuo-ming.md',
    'freebsd-14.2.md',
    '13.4.md',
    '13.5.md',
    '14.3.md',
    '14.4.md',
]

# Euro-Chinese and inverted sentence patterns
patterns = [
    (r'有关更多[信息细节]', '欧化汉语:有关更多'),
    (r'有关详细[信息细节]', '欧化汉语:有关详细'),
    (r'有关获取', '欧化汉语:有关获取'),
    (r'有关通过', '欧化汉语:有关通过'),
    (r'有关创建', '欧化汉语:有关创建'),
    (r'有关此', '欧化汉语:有关此'),
    (r'，已新增[。，]', '倒装句:已新增'),
    (r'驱动已新增', '倒装句:驱动已新增'),
    (r'新增了.*已新增', '冗余:新增了...已新增'),
    (r'新增了.*已添加', '冗余:新增了...已添加'),
    (r'新增.*已添加到', '冗余:新增...已添加到'),
    (r'进行了[一个]?[^\n]{1,20}[，。]', '欧化:进行了'),
    (r'被[^人].{0,20}[的了]', '被动句:被...'),
]

for fname in files:
    path = os.path.join(base, fname)
    if not os.path.exists(path):
        print(f'{fname}: FILE NOT FOUND')
        continue
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    issues = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('```') or stripped.startswith('|') or stripped.startswith('#'):
            continue
        for pat, label in patterns:
            if re.search(pat, line):
                match = re.search(pat, line).group()
                if 'http' in line[max(0,line.find(match)-30):line.find(match)+len(match)+30]:
                    continue
                issues.append(f'  L{i}: [{label}] {stripped[:120]}')
    if issues:
        print(f'{fname}: {len(issues)} issues')
        for issue in issues[:20]:
            print(issue)
        if len(issues) > 20:
            print(f'  ... and {len(issues)-20} more')
    else:
        print(f'{fname}: OK')

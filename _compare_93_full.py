import re

with open(r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\_en_9.3.adoc', 'r', encoding='utf-8') as f:
    en = f.read()

with open(r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\9.3.md', 'r', encoding='utf-8') as f:
    cn = f.read()

en_lines = en.split('\n')
cn_lines = cn.split('\n')

# Extract content paragraphs from English (skip metadata, headers, table markers, etc.)
en_paragraphs = []
for line in en_lines:
    stripped = line.strip()
    if not stripped:
        continue
    if stripped.startswith('---'):
        continue
    if stripped.startswith('|==='):
        continue
    if stripped.startswith('[['):
        continue
    if stripped.startswith('include::'):
        continue
    if stripped.startswith('[cols'):
        continue
    if stripped.startswith('== '):
        continue
    if stripped.startswith('title:') or stripped.startswith('sidenav:'):
        continue
    if stripped == "'''''":
        continue
    if stripped.startswith('Table of Contents'):
        continue
    if stripped.startswith('* <<'):
        continue
    en_paragraphs.append(stripped)

cn_paragraphs = []
for line in cn_lines:
    stripped = line.strip()
    if not stripped:
        continue
    if stripped.startswith('---'):
        continue
    if stripped.startswith('| :---'):
        continue
    if stripped.startswith('## '):
        continue
    if stripped.startswith('# '):
        continue
    cn_paragraphs.append(stripped)

print(f'English content paragraphs: {len(en_paragraphs)}')
print(f'Chinese content paragraphs: {len(cn_paragraphs)}')

# Check each English paragraph has a corresponding Chinese paragraph
# Use revision numbers as anchors
print('\n=== Checking each revision-numbered paragraph ===')
en_rev_paragraphs = {}
for p in en_paragraphs:
    revs = re.findall(r'r\d{5,6}', p)
    for r in revs:
        if r not in en_rev_paragraphs:
            en_rev_paragraphs[r] = p

cn_rev_paragraphs = {}
for p in cn_paragraphs:
    revs = re.findall(r'r\d{5,6}', p)
    for r in revs:
        if r not in cn_rev_paragraphs:
            cn_rev_paragraphs[r] = p

# Check for missing revisions
all_en_revs = set(en_rev_paragraphs.keys())
all_cn_revs = set(cn_rev_paragraphs.keys())
missing = all_en_revs - all_cn_revs
extra = all_cn_revs - all_en_revs

if missing:
    print(f'Missing revisions in Chinese: {sorted(missing)}')
else:
    print('All revision-numbered paragraphs present in Chinese.')

# Check for non-revision paragraphs that might be missing
print('\n=== Checking non-revision paragraphs ===')
en_non_rev = [p for p in en_paragraphs if not re.findall(r'r\d{5,6}', p)]
cn_non_rev = [p for p in cn_paragraphs if not re.findall(r'r\d{5,6}', p)]

print(f'English non-revision paragraphs: {len(en_non_rev)}')
print(f'Chinese non-revision paragraphs: {len(cn_non_rev)}')

# Check for specific content that should be present
print('\n=== Checking specific content presence ===')
checks = [
    ('Abstract/摘要', '9.3-STABLE'),
    ('Introduction/引言', 'release errata'),
    ('Security intro', 'security.FreeBSD.org'),
    ('Kernel - arcmsr', 'arcmsr'),
    ('Kernel - isci', 'isci'),
    ('Kernel - ixgbe sysctl', 'System-level'),
    ('Kernel - mfi Invader', 'MegaRAID Invader'),
    ('Kernel - zfs_root panic', 'zfs_root'),
    ('Kernel - debug.devfs_iosize_max_clamp', 'debug.devfs_iosize_max_clamp'),
    ('Kernel - kern.disallow_high_osrel', 'kern.disallow_high_osrel'),
    ('Kernel - vfs.zfs.arc_meta_limit', 'vfs.zfs.arc_meta_limit'),
    ('Kernel - mmap superpages', 'superpage'),
    ('Kernel - bge workaround', 'BCM5719'),
    ('Kernel - kern.supported_archs', 'kern.supported_archs'),
    ('Kernel - kern.panic_reboot_wait_time', 'kern.panic_reboot_wait_time'),
    ('Kernel - Hardware RNG', 'Hardware Random Number'),
    ('Kernel - netmap', 'netmap'),
    ('Kernel - ext4', 'ext4'),
    ('Kernel - TTM', 'TTM'),
    ('Kernel - linprocfs uuid', '/sys/kernel/random/uuid'),
    ('Kernel - zpool extensible_dataset', 'extensible_dataset'),
    ('Kernel - vt driver', 'vt[4]'),
    ('Kernel - mpr', 'mpr[4]'),
    ('Kernel - Intel Turbo Boost', 'Turbo Boost'),
    ('Kernel - xen XENHVM', 'XENHVM'),
    ('Hardware - MacBook trackpad', 'Trackpad'),
    ('Hardware - nve deprecated', 'nve[4]'),
    ('Hardware - mfi Fury', 'MegaRAID Fury'),
    ('Hardware - Radeon KMS', 'Radeon KMS'),
    ('Hardware - aacraid', 'aacraid'),
    ('Network - re RTL8106E', 'RTL8106E'),
    ('Network - re RTL8168G', 'RTL8168G'),
    ('Network - re RTL8168EP', 'RTL8168EP'),
    ('Network - oce', 'oce[4]'),
    ('Network - qlxgbe', 'qlxgbe'),
    ('Network - qlxge', 'qlxge'),
    ('Network - bge BCM5725', 'BCM5725'),
    ('Network - bge BCM57764', 'BCM57764'),
    ('Network - run RT5370', 'RT5370'),
    ('Network - usb radiotap', 'radiotap'),
    ('Network - run firmware 0.33', '0.33'),
    ('Network - bxe', 'bxe[4]'),
    ('Network - run RT3593', 'RT3593'),
    ('Network - run DWA-127', 'DWA-127'),
    ('Network - axge', 'axge'),
    ('Network - urndis', 'urndis'),
    ('FS - zfs bookmarks', 'bookmarks'),
    ('Userland - pgrep -c', 'pgrep'),
    ('Userland - ddb ioapic', 'ioapic'),
    ('Userland - nmbcluster', 'nmbcluster'),
    ('Userland - /var/cache 0755', '0755'),
    ('Userland - uname -U -K', 'uname'),
    ('Userland - fetch SNI', 'SNI'),
    ('Userland - gcc segfault', 'gcc'),
    ('Userland - gcc Google', 'Google'),
    ('Userland - Heimdal gss_pseudo_random', 'gss_pseudo_random'),
    ('Userland - hastctl', 'hastctl'),
    ('Userland - ps no truncate', 'ps[1]'),
    ('Userland - protect', 'protect'),
    ('Userland - gmirror', 'gmirror'),
    ('Userland - etcupdate', 'etcupdate'),
    ('Userland - find -lname', '-lname'),
    ('Userland - hw.uart.console', 'hw.uart.console'),
    ('Userland - kldload dmesg', 'dmesg'),
    ('Userland - KDE X infinite loop', 'infinite loop'),
    ('Userland - newsyslog', 'newsyslog'),
    ('Userland - zdb', 'zdb'),
    ('Userland - pciconf -V', 'pciconf'),
    ('Userland - zfs snapshot inconsistent', 'snapshot'),
    ('Userland - zfs recv -F', 'recv -F'),
    ('Userland - read-only .OBJDIR', '.OBJDIR'),
    ('Userland - /usr/lib/private', '/usr/lib/private'),
    ('Userland - libmap32.conf', 'libmap32'),
    ('Userland - libucl', 'libucl'),
    ('Userland - pkg bootstrap', 'bootstrap'),
    ('Userland - tzdata2014a', 'tzdata2014a'),
    ('Userland - bmake', 'bmake'),
    ('Userland - fetch UTC', 'UTC'),
    ('Userland - zfs aliases', 'list -t snap'),
    ('Userland - zfs -p', 'zfs[8]'),
    ('Userland - OpenPAM', 'OpenPAM'),
    ('Userland - sh export local readonly', 'export'),
    ('Userland - find -ignore_readdir_race', '-ignore_readdir_race'),
    ('Userland - ps -J', '-J'),
    ('Userland - top jail', 'top[1]'),
    ('Userland - Blowfish crypt $2b$', '$2b$'),
    ('Userland - newsyslog.conf.d', 'newsyslog.conf.d'),
    ('Userland - onifconsole', 'onifconsole'),
    ('Userland - arc4random', 'arc4random'),
    ('Userland - pmcstat -l', 'pmcstat'),
    ('Userland - GNATS to Bugzilla', 'Bugzilla'),
    ('Periodic - 800.loginfail', '800.loginfail'),
    ('RC - first boot', 'first boot'),
    ('RC - SIGALRM', 'SIGALRM'),
    ('Contrib - readline', 'readline'),
    ('Contrib - Sendmail 8.14.9', '8.14.9'),
    ('Contrib - BIND 9.9.5', '9.9.5'),
    ('Contrib - xz post-5.0.5', '5.0.5'),
    ('Contrib - OpenSSH 6.6p1', '6.6p1'),
    ('Contrib - OpenSSL 0.9.8za', '0.9.8za'),
    ('Ports - Xorg KMS', 'KMS'),
    ('Ports - vt(4) console', 'vt[4]'),
    ('Ports - KDE4 packages', 'KDE4'),
    ('Ports - WITHOUT_NEW_XORG', 'WITHOUT_NEW_XORG'),
    ('Releng - etcupdate bootstrap', 'etcupdate'),
    ('Releng - release.sh pkg', 'release.sh'),
    ('Releng - services.mkdb', 'services.mkdb'),
    ('Upgrade - amd64,i386 binary', 'amd64'),
    ('Upgrade - source-based', 'UPDATING'),
    ('Upgrade - backup', 'backing up'),
    ('Upgrade - incompatibilities', 'incompatibilit'),
]

for name, keyword in checks:
    en_found = keyword.lower() in en.lower()
    cn_found = keyword.lower() in cn.lower()
    if en_found and not cn_found:
        print(f'  MISSING: {name} (keyword: {keyword})')
    elif not en_found and cn_found:
        print(f'  EXTRA in CN: {name} (keyword: {keyword})')

print('\n=== Done ===')

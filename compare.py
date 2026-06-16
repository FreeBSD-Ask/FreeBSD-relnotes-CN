import re
import sys

# Read the English originals
with open(r'C:\Users\ykla\AppData\Local\Temp\trae\toolcall-output\18cbc00e-2f48-4b02-8e8f-7c9a90db80e6.txt', 'r', encoding='utf-8') as f:
    en_80 = f.read()
with open(r'C:\Users\ykla\AppData\Local\Temp\trae\toolcall-output\15e30770-6a3a-48f1-989f-0855a4830fd2.txt', 'r', encoding='utf-8') as f:
    en_81 = f.read()
with open(r'C:\Users\ykla\AppData\Local\Temp\trae\toolcall-output\b5fa71c2-54ef-489f-ad77-04117a404852.txt', 'r', encoding='utf-8') as f:
    en_82 = f.read()
with open(r'C:\Users\ykla\AppData\Local\Temp\trae\toolcall-output\c92d69f6-a437-4df2-8272-18144a936d5d.txt', 'r', encoding='utf-8') as f:
    en_83 = f.read()

# Read the Chinese translations
with open(r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\8.0.md', 'r', encoding='utf-8') as f:
    cn_80 = f.read()
with open(r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\8.1.md', 'r', encoding='utf-8') as f:
    cn_81 = f.read()
with open(r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\8.2.md', 'r', encoding='utf-8') as f:
    cn_82 = f.read()
with open(r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\8.3.md', 'r', encoding='utf-8') as f:
    cn_83 = f.read()

def extract_sa_entries(text):
    return re.findall(r'SA-\d{2}:\d{2,3}\.\w+', text)

def extract_code_blocks(text):
    return re.findall(r'```\w*\n(.*?)```', text, re.DOTALL)

def extract_platform_tags(text):
    return re.findall(r'\[(amd64|i386|powerpc|sparc64|arm|ia64|mips|pc98)\]', text, re.IGNORECASE)

def extract_adoc_paragraphs(text):
    # Extract text from <p> tags in adoc HTML
    paras = re.findall(r'<p>(.*?)</p>', text, re.DOTALL)
    result = []
    for p in paras:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        if clean and len(clean) > 20:
            result.append(clean)
    return result

def check_key_terms_in_cn(en_text, cn_text, terms):
    missing = []
    for term in terms:
        if term.lower() in en_text.lower() and term.lower() not in cn_text.lower():
            missing.append(term)
    return missing

# ===== 8.0.md CHECK =====
print('='*60)
print('8.0.md COMPLETENESS CHECK')
print('='*60)

en_sa = extract_sa_entries(en_80)
cn_sa = extract_sa_entries(cn_80)
missing_sa = set(en_sa) - set(cn_sa)
if missing_sa:
    print(f'Missing security advisories: {missing_sa}')
else:
    print(f'Security advisories: All {len(set(en_sa))} unique entries present')

en_code = extract_code_blocks(en_80)
cn_code = extract_code_blocks(cn_80)
print(f'English code blocks: {len(en_code)}')
print(f'Chinese code blocks: {len(cn_code)}')

en_platforms = extract_platform_tags(en_80)
cn_platforms = extract_platform_tags(cn_80)
print(f'English platform tags: {len(en_platforms)}')
print(f'Chinese platform tags: {len(cn_platforms)}')

# Check for SA-09:13
if 'SA-09:13' in en_80 and 'SA-09:13' not in cn_80:
    print('MISSING: SA-09:13.protosw security advisory entry')

# Check for specific content
key_items_80 = [
    'SA-09:13', 'SA-08:05', 'SA-08:06', 'SA-08:07', 'SA-08:08',
    'SA-08:09', 'SA-08:10', 'SA-08:11', 'SA-08:12', 'SA-08:13',
    'SA-09:01', 'SA-09:02', 'SA-09:03', 'SA-09:04', 'SA-09:05',
    'SA-09:06', 'SA-09:07', 'SA-09:08', 'SA-09:09', 'SA-09:10',
    'SA-09:11', 'SA-09:12', 'SA-09:14',
    'VIMAGE', 'DEADLKRES', 'epair', 'ksyms',
    'options    VIMAGE', 'device crypto', 'options IPSEC', 'options IPSEC_NAT_T',
    'options    ROUTETABLES=2', 'net.fibs=6',
    'device    ahci', 'device    siis',
    'options    NFSCL', 'options    NFSD',
    'setfib', 'hw.clflush_disable',
    'vm.pmap.pg_ps_enabled',
    'loader_conf_files',
    'hw.est.msr_info', 'hw.drm.msi',
    'kern.cam.cd.retry_count',
    'hw.re.prefer_iomap',
    'vfs.lookup_shared', 'LOOKUP_SHARED',
    'hw.snd.default_unit',
    'hw.ata.ata_dma_check_80pin',
    'hw.ciss.nop_message_heartbeat',
    'vm.pmap.pg_ps_enabled',
    'machdep.hyperthreading_enabled',
]

for item in key_items_80:
    if item in en_80 and item not in cn_80:
        print(f'  MISSING key term: {item}')

# Check for missing sections
print()
print('Checking section structure...')
en_h2 = re.findall(r'<h2[^>]*>(.*?)</h2>', en_80, re.DOTALL)
for h in en_h2:
    clean = re.sub(r'<[^>]+>', '', h).strip()
    if clean and clean not in cn_80:
        # Check if the Chinese version has a translated version
        pass  # Sections are translated, so we check by number

# Check for 2.2.1 Boot Loader Changes
if '2.2.1' in cn_80:
    print('  Section 2.2.1 (Boot Loader): Present')
else:
    print('  Section 2.2.1 (Boot Loader): Check manually')

# ===== 8.1.md CHECK =====
print()
print('='*60)
print('8.1.md COMPLETENESS CHECK')
print('='*60)

en_sa = extract_sa_entries(en_81)
cn_sa = extract_sa_entries(cn_81)
missing_sa = set(en_sa) - set(cn_sa)
if missing_sa:
    print(f'Missing security advisories: {missing_sa}')
else:
    print(f'Security advisories: All {len(set(en_sa))} unique entries present')

en_code = extract_code_blocks(en_81)
cn_code = extract_code_blocks(cn_81)
print(f'English code blocks: {len(en_code)}')
print(f'Chinese code blocks: {len(cn_code)}')

# Check for specific content in 8.1
key_items_81 = [
    'DEADLKRES', 'F_READAHEAD', 'F_RDAHEAD', 'vfs.read_max',
    'lindev', '/dev/full', 'INCLUDE_CONFIG_FILE',
    'pselect', 'ip4.saddrsel', 'ip6.saddrsel',
    'hw.acpi.install_interface', 'hw.acpi.remove_interface',
    'option ATA_CAM',
    'GEOM_SCHED', 'gsched_rr', 'HAST', 'hastd', 'hastctl',
    'mvs', 'kern.cam.boot_delay',
    'zfsloader', 'gptzfsboot', 'zfsboot',
    'vfs.root.mountfrom',
    'negnametimeo',
    'vfs.vlru_allow_cache_src',
    'vfs.zfs.txg.write_limit_override',
    'kstat.zfs.misc.zfetchstats',
    'service', 'rc.d/rtsold', 'rc.d/static_arp',
    'rc.d/ubthidhci',
    'firewall_coscripts',
    'vlans_IF',
    'ENOTCAPABLE',
    'receive -u',
]

for item in key_items_81:
    if item in en_81 and item not in cn_81:
        print(f'  MISSING key term: {item}')

# Check for missing devd.conf example
if 'intclass' in en_81 and 'intclass' not in cn_81:
    print('  MISSING: devd.conf example with intclass/intsubclass/intprotocol')

# ===== 8.2.md CHECK =====
print()
print('='*60)
print('8.2.md COMPLETENESS CHECK')
print('='*60)

en_sa = extract_sa_entries(en_82)
cn_sa = extract_sa_entries(cn_82)
missing_sa = set(en_sa) - set(cn_sa)
if missing_sa:
    print(f'Missing security advisories: {missing_sa}')
else:
    print(f'Security advisories: All {len(set(en_sa))} unique entries present')

en_code = extract_code_blocks(en_82)
cn_code = extract_code_blocks(cn_82)
print(f'English code blocks: {len(en_code)}')
print(f'Chinese code blocks: {len(cn_code)}')

# Check for specific content in 8.2
key_items_82 = [
    'r209326', 'r209765', 'r209767', 'r211593', 'r215938',
    'r215598', 'r214620', 'r214621', 'r215513',
    'r215006', 'r215521', 'r209788', 'r209783',
    'r209692', 'r212230', 'r214326',
    'KDB', 'KDB_TRACE',
    'vm.kmem_size', 'vm.kmem_size_max', 'vm.kmem_size_min',
    'debug.kdb.stop_cpus', 'debug.trace_on_panic', 'kern.sync_on_panic',
    'vm.kmem_map_size', 'vm.kmem_map_free',
    'vfs.ncsizefactor', 'vfs.ncnegfactor',
    'memguard', 'PT_LWPINFO', 'ptrace',
    'XTS-AES', 'IEEE Std. 1619-2007',
    'xen', 'qpi',
    'aesni', 'aibs', 'acpi_aiboost',
    'coretemp', 'Xeon 5500', 'Xeon 5600',
    'tpm', 'xhci', 'USB 3.0',
    'ehci', 'ohci', 'uhci',
    'ichwd', 'NM10',
    'video4linux',
    'uaudio', 'MIDI',
    'alc', 'AR8151', 'AR8152',
    'bge', 'BCM5718',
    'bwi', 'BCM430', 'BCM431',
    'if_bwi.ko',
    'cxgb', 'nfilters', 'pkt_timestamp', 'core_clock',
    'em', '7.1.9', 'igb', '2.0.7',
    'iwn', '6000', '9.221.4.1',
    'ixgbe', '2.3.8', '82599',
    'miibus', 'flow control',
    'mwlfw',
    'nfe', 'WoL',
    're', 'RTL8168', '64-bit DMA',
    'rl', 'RTL8139B', 'WoL',
    'dev.rl', 'prefer_iomap',
    'sk', 'Yukon',
    'sis', 'DP8315', 'DP83815', 'DP83816',
    'dev.sis', 'manual_pad',
    'ste', 'prefer_iomap',
    'xl', 'WoL',
    'carp', 'ipfw', 'one_pass',
    'net.link.ifqmaxlen',
    'ngtee',
    'IPsec', 'parallel',
    'IPv6', 'ping6', 'use_defaultzone',
    'lagg', 'failover_rx_all',
    'ng_eiface', 'ng_ether', 'vnet',
    'ng_patch',
    'pf', 'ICMP', 'TSO',
    'tcp', 'inflight', 'reass',
    'RFC 3390', 'RFC 5681',
    'siftr',
    'vnet', 'IPv4 multicast',
    'ahci', 'VT8251', 'NCQ',
    'arcmsr', '1.20.00.19',
    'kern.cam.ada.spindown_shutdown',
    'ata', 'ATA_CAM', 'pm_level',
    'gconcat', 'crash dump',
    'geli', 'overwrites', 'XTS-AES',
    'mpt', 'MAXPHYS',
    'twa', '3.80.06.003',
    'linprocfs', 'proc/$$/environment',
    'boot.nfsroot.nfshandlelen',
    'ZFS', 'version 15', 'metadata',
    'zfs scrub', 'periodic',
    'port checksum',
    'ACPI-CA', '20101013',
    'ee', '1.5.2',
    'BIND', '9.6-ESV-R3',
    'netcat', '4.8',
    'OpenSSL', '0.9.8q',
    'tzdata2010o',
    'xz', '5.0.0',
    'pkg_create', 'LZMA',
    'sysinstall', '1GB', '4GB',
    'GNOME', '2.32.1',
    'KDE', '4.5.5',
]

for item in key_items_82:
    if item in en_82 and item not in cn_82:
        print(f'  MISSING key term: {item}')

# ===== 8.3.md CHECK =====
print()
print('='*60)
print('8.3.md COMPLETENESS CHECK')
print('='*60)

en_sa = extract_sa_entries(en_83)
cn_sa = extract_sa_entries(cn_83)
missing_sa = set(en_sa) - set(cn_sa)
if missing_sa:
    print(f'Missing security advisories: {missing_sa}')
else:
    print(f'Security advisories: All {len(set(en_sa))} unique entries present')

en_code = extract_code_blocks(en_83)
cn_code = extract_code_blocks(cn_83)
print(f'English code blocks: {len(en_code)}')
print(f'Chinese code blocks: {len(cn_code)}')

# Check for specific content in 8.3
key_items_83 = [
    'r219107', 'systrace_linux32', 'systrace_freebsd32',
    'hhook', 'khelp', 'pfil',
    'hw.memtest.tests',
    'O_CLOEXEC', 'FD_CLOEXEC',
    'posix_fallocate', 'posix_fadvise',
    'usb', 'USB packet filter', 'usbdump', 'bpf',
    'cxgb', '7.11.0',
    'cxgbe', 'T4', 'Terminator',
    'dc', 'PAE',
    'em', '7.3.2',
    'igb', '2.3.1', 'I350',
    'ixgbe', '2.4.5',
    'iwn', '1000', '5000', '6000', '6500',
    'msk', 'Yukon EC', 'Yukon Ultra', 'Yukon FE', 'Yukon Ultra2', 'Yukon XL',
    'nfe', 'MTU',
    'rdcphy', 'R6040',
    're', 'RTL8168E', '8111E-VL', 'RTL8401E',
    'RTL8105E',
    'vte', 'R6040', 'Vortex86',
    'ipfw', 'call', 'return',
    'ipsec', 'HMAC-SHA-256', 'HMAC-SHA-384', 'HMAC-SHA-512',
    'RFC 4868',
    'IPV6_PKTINFO', 'IPV6_USE_MIN_MTU',
    'mod_cc', 'cc_chd', 'cc_cubic', 'cc_hd', 'cc_htcp', 'cc_newreno', 'cc_vegas',
    'net.inet.tcp.cc.algorithm', 'net.inet.tcp.cc.available',
    'h_ertt', 'ERTT',
    'TCP_CONGESTION',
    'ng_ipfw', 'IPv6',
    'ng_one2many', 'XMIT_FAILOVER',
    'ada', 'write_cache', 'kern.cam.ada.write_cache',
    'arcmsr', '1.20.00.22',
    'graid', 'ataraid',
    'mxge',
    'tws', '9750',
    'TRIM', 'newfs', 'tunefs',
    'fsck_ffs', '-E',
    'nocto', 'close-to-open',
    'vfs.typenumhash',
    'ZFS', 'SPA', 'version 28', 'dedup', 'raidz3',
    'zfs diff', 'zpool split', 'zpool import -F',
    'bsdtar', 'cpio', 'libarchive', '2.8.5',
    'cpuset', '-C', 'all',
    'fetch', 'STAT',
    'gpart', 'show', '-p',
    'hastd', 'hast', 'checksum', 'compression', 'source',
    'readline', 'libedit',
    'makefs', 'ISO 9660',
    'libmd', 'libcrypt', 'SHA-256', 'SHA-512',
    'netstat', 'KAME', 'scope',
    'newsyslog', 'xz', 'X',
    'poweroff', 'shutdown -p now',
    'ppp', 'iface name', 'iface description',
    'ps', 'usertime', 'systime',
    'rtadvd', 'noifprefix', 'RDNSS', 'DNSSL', 'RFC 6106', 'rtadvctl',
    'tftpd',
    'zpool', 'labelclear',
    'awk', '2011',
    'BIND', '9.6-ESV-R5-P1',
    'netcat', '4.9',
    'GCC', 'libstdc', '127959',
    'LESS', 'v444',
    'OpenSSH', '5.4p1',
    'sendmail', '8.14.5',
    'tzdata2011n',
    'unifdef', '2.5.6',
    'xz', '5.0.1',
    'KDE', '4.7.4',
]

for item in key_items_83:
    if item in en_83 and item not in cn_83:
        print(f'  MISSING key term: {item}')

# Additional detailed checks
print()
print('='*60)
print('DETAILED CONTENT COMPARISON')
print('='*60)

# Check 8.0 for the errata section - original has a link to errata
# Check if the "errata" mention is present
for version, en, cn in [('8.0', en_80, cn_80), ('8.1', en_81, cn_81), ('8.2', en_82, cn_82), ('8.3', en_83, cn_83)]:
    # Check for Table of Contents
    if 'Table of Contents' in en and '目录' not in cn and 'Table of Contents' not in cn:
        print(f'{version}: Table of Contents section might be missing (but this is OK for markdown format)')

# Check 8.2 for the specific section 2.3.1 /etc/periodic Scripts
# The English original has section "2.3.1 /etc/periodic Scripts" while 8.0 and 8.1 have "2.3.1 /etc/rc.d Scripts"
if '/etc/periodic' in en_82:
    if '/etc/periodic' in cn_82:
        print('8.2: /etc/periodic section present')
    else:
        print('8.2: MISSING /etc/periodic section reference')

# Check 8.2 for the stray text "以下是翻译：" which is a translation artifact
if '以下是翻译' in cn_82:
    print('8.2: WARNING - Contains stray text "以下是翻译：" (translation artifact) at line with em/igb drivers')

# Check 8.3 for missing section "2.5 Ports/Packages Collection Infrastructure"
# The English 8.3 has section 2.5 but the structure is different
if 'Ports/Packages' in en_83:
    if 'Ports' in cn_83 or '软件包' in cn_83:
        print('8.3: Ports/Packages section present')
    else:
        print('8.3: MISSING Ports/Packages section')

# Check for "Release Engineering" section in 8.3
# The English 8.3 does NOT have a "Release Engineering" section (unlike 8.0, 8.1, 8.2)
# But the Chinese 8.3 also doesn't have it - this is correct

# Check 8.2 for the GNOME section
if 'GNOME' in en_82 and 'GNOME' in cn_82:
    print('8.2: GNOME section present')
if 'KDE' in en_82 and 'KDE' in cn_82:
    print('8.2: KDE section present')

# Check 8.3 for KDE in section 2.5
if 'KDE' in en_83 and 'KDE' in cn_83:
    print('8.3: KDE section present')

print()
print('Done.')

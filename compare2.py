import re

# Read files
with open(r'C:\Users\ykla\AppData\Local\Temp\trae\toolcall-output\18cbc00e-2f48-4b02-8e8f-7c9a90db80e6.txt', 'r', encoding='utf-8') as f:
    en_80 = f.read()
with open(r'C:\Users\ykla\AppData\Local\Temp\trae\toolcall-output\15e30770-6a3a-48f1-989f-0855a4830fd2.txt', 'r', encoding='utf-8') as f:
    en_81 = f.read()
with open(r'C:\Users\ykla\AppData\Local\Temp\trae\toolcall-output\b5fa71c2-54ef-489f-ad77-04117a404852.txt', 'r', encoding='utf-8') as f:
    en_82 = f.read()
with open(r'C:\Users\ykla\AppData\Local\Temp\trae\toolcall-output\c92d69f6-a437-4df2-8272-18144a936d5d.txt', 'r', encoding='utf-8') as f:
    en_83 = f.read()

with open(r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\8.0.md', 'r', encoding='utf-8') as f:
    cn_80 = f.read()
with open(r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\8.1.md', 'r', encoding='utf-8') as f:
    cn_81 = f.read()
with open(r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\8.2.md', 'r', encoding='utf-8') as f:
    cn_82 = f.read()
with open(r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\8.3.md', 'r', encoding='utf-8') as f:
    cn_83 = f.read()

def extract_key_terms_from_adoc(text):
    """Extract key technical terms, driver names, function names, sysctl variables from adoc"""
    terms = []
    # Extract driver names like bwi(4), em(4), etc.
    terms.extend(re.findall(r'(\w+)\((\d)\)', text))
    # Extract sysctl/loader tunable names
    terms.extend(re.findall(r'([a-z][a-z0-9_.]+(?:\.[a-z0-9_.]+)+)', text))
    # Extract SA entries
    terms.extend(re.findall(r'(SA-\d{2}:\d{2,3}\.\w+)', text))
    return set(terms)

def check_specific_content(en_text, cn_text, version):
    """Do a thorough check of specific content items that should be present"""
    issues = []
    
    # Extract all <p> paragraphs from English
    en_paras = re.findall(r'<p>(.*?)</p>', en_text, re.DOTALL)
    
    # Key identifiers to check for presence
    # Driver names, function names, device names, etc.
    identifiers = re.findall(r'[a-z_][a-z0-9_]+\(\d\)', en_text.lower())
    unique_ids = set(identifiers)
    
    missing_ids = []
    for id_item in sorted(unique_ids):
        if id_item not in cn_text.lower():
            missing_ids.append(id_item)
    
    if missing_ids:
        issues.append(f'  Potentially missing man page references: {missing_ids[:20]}...' if len(missing_ids) > 20 else f'  Potentially missing man page references: {missing_ids}')
    
    return issues

# ===== Deep check for 8.0 =====
print('='*60)
print('8.0.md DEEP CONTENT CHECK')
print('='*60)

# Check for specific paragraphs that might be missing
# The English 8.0 has a section about SA-09:13.protosw
# Check if it's in the Chinese version
if 'SA-09:13' in en_80:
    if 'SA-09:13' in cn_80:
        print('SA-09:13.protosw: Present')
    else:
        print('SA-09:13.protosw: MISSING!')

# Check for the "errata" paragraph
if 'errata' in en_80.lower():
    if '勘误' in cn_80 or '错误说明' in cn_80 or 'errata' in cn_80.lower():
        print('Errata reference: Present')
    else:
        print('Errata reference: Check needed')

# Check for code blocks in English (they use <pre> tags in adoc)
en_pre_blocks = re.findall(r'<pre[^>]*>(.*?)</pre>', en_80, re.DOTALL)
print(f'English <pre> blocks: {len(en_pre_blocks)}')

# Check for specific items in 8.0
specific_checks_80 = [
    ('hw.clflush_disable', 'Loader tunable hw.clflush_disable'),
    ('map_invalidate_cache_range', 'Function map_invalidate_cache_range'),
    ('CPUID_SS', 'CPUID_SS'),
    ('options    VIMAGE', 'Kernel option VIMAGE'),
    ('options SCTP', 'SCTP incompatibility note'),
    ('jail -c vnet', 'vimage jail creation command'),
    ('epair0 create', 'epair creation example'),
    ('device crypto', 'IPsec NAT-T crypto device'),
    ('options IPSEC_NAT_T', 'IPsec NAT-T option'),
    ('options    ROUTETABLES=2', 'Multiple routing tables option'),
    ('net.fibs=6', 'FIB loader tunable'),
    ('setfib -3', 'setfib example'),
    ('device    ahci', 'AHCI device'),
    ('device    siis', 'SIIS device'),
    ('options    NFSCL', 'NFS client option'),
    ('options    NFSD', 'NFS server option'),
    ('hw.est.msr_info', 'cpufreq loader tunable'),
    ('kern.timecounter.invariant_tsc', 'Invariant TSC tunable'),
    ('hw.drm.msi', 'DRM MSI tunable'),
    ('kern.cam.cd.retry_count', 'CD retry count sysctl'),
    ('hw.re.prefer_iomap', 'Realtek I/O map tunable'),
    ('vfs.lookup_shared', 'VFS lookup_shared sysctl'),
    ('hw.snd.default_unit', 'Sound default unit sysctl'),
    ('hw.ata.ata_dma_check_80pin', 'ATA DMA check tunable'),
    ('hw.ciss.nop_message_heartbeat', 'CISS NOP heartbeat tunable'),
    ('machdep.hyperthreading_enabled', 'Hyperthreading tunable'),
    ('loader_conf_files', 'Loader config files variable'),
    ('net.inet.ip.dummynet.io_fast', 'Dummynet fast mode'),
    ('dev.msk.N.stats', 'MSK stats sysctl'),
    ('dev.txp.N.stats', 'TXP stats sysctl'),
    ('dev.txp.N.process_limit', 'TXP process limit sysctl'),
]

for term, desc in specific_checks_80:
    if term in en_80 and term not in cn_80:
        print(f'  MISSING: {desc} ({term})')

# ===== Deep check for 8.1 =====
print()
print('='*60)
print('8.1.md DEEP CONTENT CHECK')
print('='*60)

specific_checks_81 = [
    ('option DEADLKRES', 'Deadlock resolver option'),
    ('F_READAHEAD', 'Read-ahead fcntl command'),
    ('F_RDAHEAD', 'Darwin read-ahead command'),
    ('vfs.read_max', 'Read-ahead limit sysctl'),
    ('/dev/full', 'Linux /dev/full device'),
    ('INCLUDE_CONFIG_FILE', 'Kernel config file option'),
    ('ip4.saddrsel', 'VIMAGE source address selection'),
    ('ip6.saddrsel', 'VIME6 source address selection'),
    ('option ATA_CAM', 'ATA CAM option'),
    ('kern.cam.boot_delay', 'CAM boot delay tunable'),
    ('PUIS', 'Power-Up In Standby'),
    ('GEOM_SCHED', 'GEOM scheduler module'),
    ('gsched_rr', 'Round-robin scheduler'),
    ('HAST', 'Highly Available Storage'),
    ('hastd(8)', 'HAST daemon'),
    ('hastctl(8)', 'HAST control'),
    ('hast.conf(5)', 'HAST config'),
    ('mvs(4)', 'Marvell SATA driver'),
    ('zfsloader', 'ZFS loader'),
    ('gptzfsboot', 'GPT ZFS boot'),
    ('zfsboot', 'ZFS boot'),
    ('vfs.root.mountfrom', 'Root mount from variable'),
    ('negnametimeo', 'NFS negative name cache timeout'),
    ('vfs.vlru_allow_cache_src', 'VFS vnlru cache source'),
    ('vfs.zfs.txg.write_limit_override', 'ZFS write limit override'),
    ('kstat.zfs.misc.zfetchstats', 'ZFS prefetch stats'),
    ('service(8)', 'service command'),
    ('rc.d/rtsold', 'rtsold rc.d script'),
    ('rc.d/static_arp', 'static ARP rc.d script'),
    ('rc.d/ubthidhci', 'Bluetooth HCI rc.d script'),
    ('firewall_coscripts', 'Firewall co-scripts variable'),
    ('vlans_IF', 'VLAN interface variable'),
    ('ENOTCAPABLE', 'Capability error number'),
    ('receive -u', 'ZFS receive -u option'),
    ('intclass', 'USB devd intclass'),
    ('intsubclass', 'USB devd intsubclass'),
    ('intprotocol', 'USB devd intprotocol'),
    ('dev.mskc.0.int_holdoff', 'MSK interrupt holdoff'),
    ('dev.ste.0.int_rx_mod', 'STE RX interrupt moderation'),
    ('dev.vge.0.int_holdoff', 'VGE interrupt holdoff'),
    ('dev.vge.0.rx_coal_pkt', 'VGE RX coalesce packets'),
    ('dev.vge.0.tx_coal_pkt', 'VGE TX coalesce packets'),
    ('cxgbtool', 'cxgb tool'),
    ('NGM_BRIDGE_SET_PERSISTENT', 'Netgraph bridge persistent'),
    ('NGM_HUB_SET_PERSISTENT', 'Netgraph hub persistent'),
    ('IFCAP_VLAN_HWTSO', 'VLAN hardware TSO capability'),
    ('ipfw0', 'ipfw virtual interface'),
    ('net.inet.ip.fw.verbose', 'ipfw verbose sysctl'),
    ('lookup', 'ipfw lookup option'),
    ('sloppy', 'pf sloppy keyword'),
    ('newfs -E', 'TRIM newfs command'),
    ('kern.geom.label', 'GEOM label sysctl variables'),
]

for term, desc in specific_checks_81:
    if term in en_81 and term not in cn_81:
        print(f'  MISSING: {desc} ({term})')

# ===== Deep check for 8.2 =====
print()
print('='*60)
print('8.2.md DEEP CONTENT CHECK')
print('='*60)

specific_checks_82 = [
    ('r209326', 'ia64 DMA revision'),
    ('r209765', 'powerpc kern.hz revision'),
    ('r209767', 'powerpc SMP revision'),
    ('r211593', 'powerpc DMA bounce revision'),
    ('r215938', 'mips SMP revision'),
    ('r215598', 'sparc64 reservation revision'),
    ('r214620', 'amd64 KVA revision'),
    ('r214621', 'CPU topology revision'),
    ('r215513', 'ACPI suspend/resume revision'),
    ('r215006', 'ACPI reset register revision'),
    ('r215521', 'ACPI interface tunables revision'),
    ('r209788', 'ALQ improvement revision'),
    ('r209783', 'ALQ kernel module revision'),
    ('r209692', 'ddb delay revision'),
    ('r212230', 'ddb show cdev revision'),
    ('r214326', 'GENERIC KDB revision'),
    ('KDB_TRACE', 'KDB_TRACE option'),
    ('vm.kmem_size', 'kmem size tunable'),
    ('vm.kmem_size_max', 'kmem size max tunable'),
    ('vm.kmem_size_min', 'kmem size min tunable'),
    ('debug.kdb.stop_cpus', 'KDB stop CPUs tunable'),
    ('debug.trace_on_panic', 'Trace on panic tunable'),
    ('kern.sync_on_panic', 'Sync on panic tunable'),
    ('vm.kmem_map_size', 'kmem map size sysctl'),
    ('vm.kmem_map_free', 'kmem map free sysctl'),
    ('vfs.ncsizefactor', 'namecache size factor'),
    ('vfs.ncnegfactor', 'negative namecache factor'),
    ('memguard', 'memguard framework'),
    ('PT_LWPINFO', 'ptrace LWP info request'),
    ('XTS-AES', 'XTS-AES crypto mode'),
    ('IEEE Std. 1619-2007', 'IEEE 1619 standard'),
    ('xen', 'Xen HVM support'),
    ('qpi', 'QPI pseudo-bus'),
    ('aesni', 'AES-NI driver'),
    ('aibs', 'AIBS sensor driver'),
    ('acpi_aiboost', 'replaced AIBOost driver'),
    ('tpm', 'TPM driver'),
    ('xhci', 'xHCI USB 3.0 driver'),
    ('video4linux', 'Linux V4L API'),
    ('AR8151', 'AR8151 controller'),
    ('AR8152', 'AR8152 controller'),
    ('BCM5718', 'BCM5718 controller'),
    ('if_bwi.ko', 'BWI kernel module'),
    ('dev.rl', 'RL device sysctl'),
    ('dev.sis', 'SIS device sysctl'),
    ('manual_pad', 'SIS manual pad tunable'),
    ('dev.ste', 'STE device hint'),
    ('net.link.ifqmaxlen', 'Interface queue max length'),
    ('ngtee', 'ipfw ngtee action'),
    ('failover_rx_all', 'lagg failover RX sysctl'),
    ('ng_patch', 'Netgraph patch node'),
    ('siftr', 'SIFTR TCP module'),
    ('kern.cam.ada.spindown_shutdown', 'ADA spindown on shutdown'),
    ('geli', 'geli encryption'),
    ('kern.geom.eli.overwrites', 'geli overwrites sysctl'),
    ('gpart', 'gpart partition tool'),
    ('GPT_ENT_ATTR_BOOTME', 'GPT bootme attribute'),
    ('GPT_ENT_ATTR_BOOTONCE', 'GPT bootonce attribute'),
    ('GPT_ENT_ATTR_BOOTFAILED', 'GPT bootfailed attribute'),
    ('zfs scrub', 'ZFS scrub periodic script'),
    ('pkg_create', 'pkg_create LZMA support'),
]

for term, desc in specific_checks_82:
    if term in en_82 and term not in cn_82:
        print(f'  MISSING: {desc} ({term})')

# ===== Deep check for 8.3 =====
print()
print('='*60)
print('8.3.md DEEP CONTENT CHECK')
print('='*60)

specific_checks_83 = [
    ('systrace_linux32', 'Linux32 systrace module'),
    ('systrace_freebsd32', 'FreeBSD32 systrace module'),
    ('hhook', 'Helper Hook KPI'),
    ('khelp', 'Kernel Helpers KPI'),
    ('hw.memtest.tests', 'Memory test tunable'),
    ('O_CLOEXEC', 'O_CLOEXEC flag'),
    ('FD_CLOEXEC', 'FD_CLOEXEC flag'),
    ('posix_fallocate', 'posix_fallocate syscall'),
    ('posix_fadvise', 'posix_fadvise syscall'),
    ('usbdump', 'USB dump tool'),
    ('cxgbe', 'Chelsio T4 driver'),
    ('Terminator 4', 'T4 adapter name'),
    ('PAE', 'PAE option for dc driver'),
    ('I350', 'Intel I350 controller'),
    ('rdcphy', 'RDC PHY driver'),
    ('RTL8168E', 'RTL8168E controller'),
    ('8111E-VL', 'RTL8111E-VL controller'),
    ('RTL8401E', 'RTL8401E controller'),
    ('RTL8105E', 'RTL8105E controller'),
    ('vte', 'VTE RDC driver'),
    ('Vortex86', 'Vortex86 SoC'),
    ('call', 'ipfw call action'),
    ('return', 'ipfw return action'),
    ('HMAC-SHA-256', 'HMAC-SHA-256 for IPsec'),
    ('HMAC-SHA-384', 'HMAC-SHA-384 for IPsec'),
    ('HMAC-SHA-512', 'HMAC-SHA-512 for IPsec'),
    ('RFC 4868', 'RFC 4868 reference'),
    ('IPV6_PKTINFO', 'IPv6 packet info option'),
    ('IPV6_USE_MIN_MTU', 'IPv6 use min MTU'),
    ('mod_cc', 'Pluggable congestion control'),
    ('cc_chd', 'CAIA-Hamilton-Delay module'),
    ('cc_cubic', 'CUBIC module'),
    ('cc_hd', 'Hamilton-Delay module'),
    ('cc_htcp', 'H-TCP module'),
    ('cc_newreno', 'NewReno module'),
    ('cc_vegas', 'Vegas module'),
    ('net.inet.tcp.cc.algorithm', 'CC algorithm sysctl'),
    ('net.inet.tcp.cc.available', 'CC available sysctl'),
    ('h_ertt', 'Enhanced RTT module'),
    ('TCP_CONGESTION', 'TCP congestion socket option'),
    ('ng_ipfw', 'Netgraph IPFW node'),
    ('XMIT_FAILOVER', 'one2many failover algorithm'),
    ('kern.cam.ada.write_cache', 'ADA write cache sysctl'),
    ('graid', 'graid GEOM class'),
    ('ataraid', 'replaced ataraid'),
    ('tws', '3ware 9750 driver'),
    ('TRIM', 'TRIM for UFS'),
    ('newfs', 'newfs -t flag'),
    ('tunefs', 'tunefs -t flag'),
    ('fsck_ffs', 'fsck_ffs -E flag'),
    ('nocto', 'NFS no close-to-open'),
    ('vfs.typenumhash', 'VFS type num hash tunable'),
    ('version 28', 'ZFS SPA version 28'),
    ('dedup', 'ZFS dedup'),
    ('raidz3', 'ZFS raidz3'),
    ('zfs diff', 'ZFS diff command'),
    ('zpool split', 'ZFS pool split'),
    ('zpool import -F', 'ZFS pool import -F'),
    ('zpool labelclear', 'ZFS pool labelclear'),
    ('bsdtar', 'bsdtar tool'),
    ('libarchive', 'libarchive 2.8.5'),
    ('readline', 'readline API in libedit'),
    ('libedit', 'libedit library'),
    ('makefs', 'makefs ISO 9660'),
    ('libmd', 'libmd SHA support'),
    ('libcrypt', 'libcrypt SHA support'),
    ('KAME', 'KAME IPv6 scope'),
    ('poweroff', 'poweroff command'),
    ('shutdown -p now', 'shutdown -p now equivalent'),
    ('rtadvctl', 'rtadvctl control tool'),
    ('RDNSS', 'RDNSS option'),
    ('DNSSL', 'DNSSL option'),
    ('RFC 6106', 'RFC 6106 reference'),
    ('noifprefix', 'noifprefix keyword'),
    ('GCC', 'GCC update'),
    ('libstdc', 'libstdc++ update'),
    ('127959', 'GCC revision'),
    ('LESS', 'LESS update'),
    ('v444', 'LESS version'),
    ('unifdef', 'unifdef update'),
    ('2.5.6', 'unifdef version'),
    ('KDE', 'KDE desktop'),
    ('4.7.4', 'KDE version'),
]

for term, desc in specific_checks_83:
    if term in en_83 and term not in cn_83:
        print(f'  MISSING: {desc} ({term})')

print()
print('Done.')

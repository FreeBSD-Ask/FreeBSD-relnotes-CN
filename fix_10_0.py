#!/usr/bin/env python3
"""Fix 10.0.md by adding 7 missing paragraphs."""

import sys

filepath = r'c:\Users\ykla\Documents\FreeBSD-relnotes-CN\10.0.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Insert drm2(4) Radeon GPU driver after Capsicum paragraph
old1 = '已在内核中默认启用 Capsicum 功能，支持通过\u201c能力模式\u201d对多个程序进行沙箱化。\n\n未映射的 VMIO 缓冲区'
new1 = ('已在内核中默认启用 Capsicum 功能，支持通过\u201c能力模式\u201d对多个程序进行沙箱化。\n\n'
        '[amd64,i386] 新增了 [drm2(4)](http://www.freebsd.org/cgi/man.cgi?query=drm2&sektion=4) Radeon GPU 驱动程序，'
        '支持最高至 Radeon HD 6000 的 GPU，并部分支持 Radeon HD 7000 系列。'
        '该驱动程序从 Linux 3.8 移植而来。[(r254885)](http://svn.freebsd.org/viewvc/base?view=revision&revision=254885)\n\n'
        '未映射的 VMIO 缓冲区')
assert old1 in content, 'Pattern 1 not found'
content = content.replace(old1, new1, 1)
print('1. drm2(4) Radeon GPU driver - inserted')

# 2. Insert max kernel memory after VMIO buffer paragraph
old2 = ('并在 I/O 密集型工作负载下减少了系统时间高达 25-30%。'
        '[(r248508)](http://svn.freebsd.org/viewvc/base?view=revision&revision=248508)\n\n'
        '[ddb(4)](http://www.freebsd.org/cgi/man.cgi?query=ddb&sektion=4) 内核调试器现支持输出捕获功能')
new2 = ('并在 I/O 密集型工作负载下减少了系统时间高达 25-30%。'
        '[(r248508)](http://svn.freebsd.org/viewvc/base?view=revision&revision=248508)\n\n'
        '[amd64] FreeBSD 内核可寻址的最大内存量已从 1TB 增加至 4TB。'
        '[(r254466)](http://svn.freebsd.org/viewvc/base?view=revision&revision=254466)\n\n'
        '[ddb(4)](http://www.freebsd.org/cgi/man.cgi?query=ddb&sektion=4) 内核调试器现支持输出捕获功能')
assert old2 in content, 'Pattern 2 not found'
content = content.replace(old2, new2, 1)
print('2. Max kernel addressable memory 1TB->4TB - inserted')

# 3. Insert Intel Bull Mountain RNG after ddb scripting paragraph
old3 = ('更多信息请参见 [ddb(4)](http://www.freebsd.org/cgi/man.cgi?query=ddb&sektion=4) 手册页。\n\n'
        '## 虚拟化支持')
new3 = ('更多信息请参见 [ddb(4)](http://www.freebsd.org/cgi/man.cgi?query=ddb&sektion=4) 手册页。\n\n'
        '[amd64,i386] 新增了对 Intel 片上 Bull Mountain 随机数生成器的支持，'
        '该生成器见于 IvyBridge 及后续 CPU，可通过 RDRAND 指令访问。'
        '[(r240135)](http://svn.freebsd.org/viewvc/base?view=revision&revision=240135)\n\n'
        '## 虚拟化支持')
assert old3 in content, 'Pattern 3 not found'
content = content.replace(old3, new3, 1)
print('3. Intel Bull Mountain RNG - inserted')

# 4. Insert bhyve before virtio in virtualization section
old4 = '## 虚拟化支持\n\n新增了对 [virtio(4)]'
new4 = ('## 虚拟化支持\n\n'
        '[amd64] BSD Hypervisor [bhyve(8)](http://www.freebsd.org/cgi/man.cgi?query=bhyve&sektion=8) 已包含在 FreeBSD 中。'
        '[bhyve(8)](http://www.freebsd.org/cgi/man.cgi?query=bhyve&sektion=8) 需要支持 VT-x 和扩展页表 (EPT) 的 Intel CPU。'
        '这些特性存在于所有 Nehalem 及更新的型号上，但低端 Atom CPU 不支持。'
        '[(r245652)](http://svn.freebsd.org/viewvc/base?view=revision&revision=245652)\n\n'
        '新增了对 [virtio(4)]')
assert old4 in content, 'Pattern 4 not found'
content = content.replace(old4, new4, 1)
print('4. bhyve hypervisor - inserted')

# 5. Insert Hyper-V intro before the code block
old5 = '```sh\nhv_ata_pci_disengage_load="YES"'
new5 = ('[amd64,i386] 支持 Microsoft Hyper-V 的半虚拟化驱动程序已被导入并成为 amd64 GENERIC 内核的一部分。'
        '对于 i386，这些驱动程序不属于 GENERIC，因此必须在 /boot/loader.conf 中添加以下行以加载这些驱动程序：'
        '[(r255524)](http://svn.freebsd.org/viewvc/base?view=revision&revision=255524)\n\n'
        '```sh\nhv_ata_pci_disengage_load="YES"')
assert old5 in content, 'Pattern 5 not found'
content = content.replace(old5, new5, 1)
print('5. Hyper-V paravirtualized drivers intro - inserted')

# 6. Insert Xen PVHVM after vmx paragraph
old6 = ('新增驱动程序 [vmx(4)](http://www.freebsd.org/cgi/man.cgi?query=vmx&sektion=4) 。'
        '[vmx(4)](http://www.freebsd.org/cgi/man.cgi?query=vmx&sektion=4) 是一款从 OpenBSD 移植的 VMware VMXNET3 以太网驱动。'
        '[(r254738)](http://svn.freebsd.org/viewvc/base?view=revision&revision=254738)\n\n'
        '## ARM 支持')
new6 = ('新增驱动程序 [vmx(4)](http://www.freebsd.org/cgi/man.cgi?query=vmx&sektion=4) 。'
        '[vmx(4)](http://www.freebsd.org/cgi/man.cgi?query=vmx&sektion=4) 是一款从 OpenBSD 移植的 VMware VMXNET3 以太网驱动。'
        '[(r254738)](http://svn.freebsd.org/viewvc/base?view=revision&revision=254738)\n\n'
        '[amd64,i386] Xen PVHVM 虚拟化现已成为 GENERIC 内核的一部分。'
        '[(r255744)](http://svn.freebsd.org/viewvc/base?view=revision&revision=255744)\n\n'
        '## ARM 支持')
assert old6 in content, 'Pattern 6 not found'
content = content.replace(old6, new6, 1)
print('6. Xen PVHVM virtualization - inserted')

# 7. Insert rc.d/sendmail SSL certificate after the removed scripts table
old7 = '| `swap1` | 被 `swap` 和 `swaplate` 替代 |\n\n## 第三方软件'
new7 = ('| `swap1` | 被 `swap` 和 `swaplate` 替代 |\n\n'
        'rc.d/sendmail 现在在 sendmail_enable="YES" 时默认生成并使用 SSL 证书。'
        '这将允许远程 MTA 使用 STARTTLS 加密传入的电子邮件。'
        '该证书使用一个被丢弃的密钥签名，不能替代在需要使用 STARTTLS 认证时自行生成正式证书。'
        '控制证书生成的选项记录在 rc.d/sendmail 中。'
        '[(r256773)](http://svn.freebsd.org/viewvc/base?view=revision&revision=256773)\n\n'
        '## 第三方软件')
assert old7 in content, 'Pattern 7 not found'
content = content.replace(old7, new7, 1)
print('7. rc.d/sendmail SSL certificate - inserted')

with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print('\nAll 7 paragraphs inserted successfully!')

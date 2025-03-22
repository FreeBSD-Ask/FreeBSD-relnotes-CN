# FreeBSD 14.0-RELEASE 发行说明（2023 年 11 月 20 日）


- 原文链接：<https://www.freebsd.org/releases/14.0R/relnotes/>
- 作者：FreeBSD 项目
- 译者：ChatGPT & Natsufumij


## 摘要

FreeBSD 14.0-RELEASE 发行说明总结了在 14-STABLE 开发线上对 FreeBSD 基本系统所做的变更。本文列出了自上一个 RELEASE 版本以来发行的适用的安全公告，以及对 FreeBSD 内核和用户空间的重大变更。同时也提供了关于升级的简要说明。

## 介绍

本文档包含了 FreeBSD 14.0-RELEASE 的发行说明。它说明了 FreeBSD 中最近添加、变更或删除的功能。同时还提供了有关从以前版本升级的一些建议。

这份发行说明适用于 14-STABLE 开发分支创建以来的最新的 RELEASE 版本。可以在 [ https://www.FreeBSD.org/releases/ ](https://www.freebsd.org/releases/) 找到有关此分支上的预构建二进制发行版的信息。

这份发行说明适用于 14-STABLE 开发分支中的一个节点，位于 13.2-RELEASE 和后续的 14.1-RELEASE 之间。可以在 [ https://www.FreeBSD.org/releases/ ](https://www.freebsd.org/releases/) 找到有关此分支上的预构建二进制发行版的信息。

FreeBSD 14.0-RELEASE 的这个发行版本是一个正式的 RELEASE 版本。可以在 [ https://www.FreeBSD.org/releases/ ](https://www.freebsd.org/releases/) 或其镜像站点找到它。有关获取这个（或其他）FreeBSD 发行版本的更多信息，请参阅[ FreeBSD 手册](https://docs.freebsd.org/en/books/handbook/) 中的[获取 FreeBSD 附录](https://docs.freebsd.org/en/books/handbook/mirrors)。

在安装 FreeBSD 之前，建议所有用户查阅发行勘误。发行勘误文档会在发行周期结束后或发行后发现的“迟到”的信息进行更新。通常，它包含已知错误、安全公告和对文档的更正。可以在 FreeBSD 网站上找到 FreeBSD 14.0-RELEASE 的最新发行勘误副本。

本文档说明了自 13.2-RELEASE 以来 FreeBSD 中最为用户可见的新功能或变更。一般来说，这里所述的变更是独特于 14-STABLE 分支的，除非特别标记为 MERGED 功能。

一般的发行说明条目记录了自 13.2-RELEASE 后发行的安全公告、新的驱动程序或硬件支持、新的命令或参数、主要错误修复或第三方软件软件升级。它们还可能列出对主要 Ports/软件包或发行工程实践的变更。显然，发行说明不能列出在版本之间对 FreeBSD 进行的每一项变更；这份文档主要关注安全公告、用户可见的变更和主要的架构改进。

## 从 FreeBSD 旧版本升级

在 RELEASE 版本之间进行二进制升级（以及各种安全分支的快照）是受支持的，可以使用 [freebsd-update(8)](https://man.freebsd.org/cgi/man.cgi?query=freebsd-update&sektion=8&format=html) 工具。二进制升级过程将更新未修改的用户空间工具，以及作为官方 FreeBSD 发行的一部分的未修改的 GENERIC 内核。[ freebsd-update(8)  ](https://man.freebsd.org/cgi/man.cgi?query=freebsd-update&sektion=8&format=html) 工具要求正在升级的主机具有互联网连接。请注意，freebsd-update 不能用于在升级到新的主要版本后回滚到先前版本。

基于源代码的升级（基于重新编译 FreeBSD 基本系统的源代码）从以前的版本进行支持，具体步骤详见 **/usr/src/UPDATING** 中的说明。

对于通过 EFI 引导的系统，请注意：EFI 系统分区（ESP）上有一个或多个引导加载程序的副本，由固件用于引导内核。如果根文件系统是 ZFS，则引导加载程序必须能够支持从 ZFS 引导文件系统读取。在系统升级后，但在执行 `zpool upgrade` 之前，必须更新 ESP 上的引导加载程序，否则系统可能无法引导。虽然不是强制性的，但在使用 UFS 作为根文件系统时也应遵循此更新过程。可以使用命令 `efibootmgr -v` 来确定正在使用的引导加载程序的位置。`BootCurrent` 显示的值应该是用于引导系统的当前引导配置的编号。输出的相应条目应该以 `+` 号开头，例如

```
+Boot0000* FreeBSD HD(1,GPT,f859c46d-19ee-4e40-8975-3ad1ab00ac09,0x800,0x82000)/File(EFIfreebsdloader.efi) nda0p1:/EFI/freebsd/loader.efi (null)
```

ESP 可能已经挂载在 **/boot/efi** 上。如果没有，可以手动挂载分区，使用 `efibootmgr` 输出中列出的分区（在此情况下为 `nda0p1`）：`mount_msdosfs /dev/nda0p1 /boot/efi`。有关另一个示例，请参阅 [ loader.efi(8)  ](https://man.freebsd.org/cgi/man.cgi?query=loader.efi&sektion=8&format=html)。

在 `efibootmgr -v` 输出的 `File` 字段中的值，例如 `EFIfreebsdloader.efi`，是 ESP 上正在使用的引导加载程序的 MS-DOS 名称。如果挂载点是 **/boot/efi**，则此文件将转换为 `/boot/efi/efi/freebsd/loader.efi`。 （在 MS-DOSFS 文件系统上大小写不敏感；FreeBSD 使用小写。）`File` 的另一个常见值可能是 `EFIbootbootXXX.efi`，其中 `XXX` 是 amd64 的 `x64`、aarch64 的 `aa64` 或 riscv64 的 `riscv64`；如果未配置，则为默认引导加载程序。应该把 **/boot/loader.efi** 复制到 **/boot/efi** 中的正确路径来更新已配置和默认的引导加载程序。

> 仅在备份**所有**数据和配置文件后尝试升级 FreeBSD。

## 安全性和勘误

本节列出了自 13.2-RELEASE 以来的各种安全公告和勘误通知。

### 安全公告

| 公告    | 日期 | 主题 |
| ------- | ---- | ---- |
| 无公告 |      |      |

### 勘误通知

| 勘误   | 日期 | 主题 |
| ------ | ---- | ---- |
| 无勘误 |      |      |

## FreeBSD 14.0 中合并的重要变更

FreeBSD 14.0 包含了自 FreeBSD 13.0 发行以来两年半的开发工作。其中一些工作已被选入旧的开发分支，并包含在 FreeBSD 13 的次要版本中。

对于 64 位架构，基本系统默认启用了位置无关可执行文件（PIE）支持。可以使用 `WITHOUT_PIE` 参数禁用此功能。[ 9a227a2fd642 ](https://cgit.freebsd.org/src/commit/?id=9a227a2fd642)（由 Stormshield 赞助）

新增了服务脚本 `zfskeys`​[ rc(8)  ](https://man.freebsd.org/cgi/man.cgi?query=rc&sektion=8&format=html)，以允许在启动期间自动解密使用 ZFS 本地加密的 ZFS 数据集。`zfskeys` 启动脚本支持加载存储在 ZFS 上的密钥。有关更多信息，请参阅 [ rc.conf(5)  ](https://man.freebsd.org/cgi/man.cgi?query=rc.conf&sektion=5&format=html) 手册页。[ 33ff39796ffe ](https://cgit.freebsd.org/src/commit/?id=33ff39796ffe)，[ 8719e8a951b7 ](https://cgit.freebsd.org/src/commit/?id=8719e8a951b7)，[ 97aeda224356 ](https://cgit.freebsd.org/src/commit/?id=97aeda224356)（由 Modirum 和 Klara Inc. 赞助）

`chroot` 工具现在支持非特权操作，并且 [ chroot(8)](https://man.freebsd.org/cgi/man.cgi?query=chroot&sektion=8&format=html) 程序可使用 `-n` 参数启用该功能。[ a40cf4175c90 ](https://cgit.freebsd.org/src/commit/?id=a40cf4175c90)（由 EPSRC 赞助）

新增了 [ md5sum(1)  ](https://man.freebsd.org/cgi/man.cgi?query=md5sum&sektion=1&format=html) 和与 Linux 兼容的类似消息摘要程序，通过在程序名称以 `sum` 结尾时运行相应的 BSD 程序，并使用 `-r` 参数。[ 086feed850c3 ](https://cgit.freebsd.org/src/commit/?id=086feed850c3)（由奈飞赞助）

在 `ssh` 中启用了 FIDO/U2F 硬件验证器的支持，使用新的公钥类型 `ecdsa-sk` 和 `ed25519-sk`，以及相应的证书类型。FIDO/U2F 支持见 [ https://www.openssh.com/txt/release-8.2 ](https://www.openssh.com/txt/release-8.2)。[ e9a994639b2a ](https://cgit.freebsd.org/src/commit/?id=e9a994639b2a)（由 FreeBSD 基金会赞助）

新增了 Intel I225 以太网控制器的 [ igc(4)  ](https://man.freebsd.org/cgi/man.cgi?query=igc&sektion=4&format=html) 驱动程序，支持 2.5 Gbps 网卡。[ 517904de5cca ](https://cgit.freebsd.org/src/commit/?id=517904de5cca)（由 Rubicon Communications, LLC ("Netgate") 赞助）

新增了 [ mgb(4)  ](https://man.freebsd.org/cgi/man.cgi?query=mgb&sektion=4&format=html) 网卡驱动程序，支持 Microchip 设备 LAN7430 PCIe Gigabit Ethernet 控制器带 PHY、LAN7431 PCIe Gigabit Ethernet 控制器带 RGMII 接口。该驱动程序有一些注意事项和限制，但是是功能齐备的。[ e0262ffbc6ae ](https://cgit.freebsd.org/src/commit/?id=e0262ffbc6ae)（由 FreeBSD 基金会赞助）

两个新的守护进程，[ rpc.tlsclntd(8)  ](https://man.freebsd.org/cgi/man.cgi?query=rpc.tlsclntd&sektion=8&format=html) 和 [ rpc.tlsservd(8)  ](https://man.freebsd.org/cgi/man.cgi?query=rpc.tlsservd&sektion=8&format=html)，现在在 amd64 和 arm64 上默认构建。它们提供了对 NFS-over-TLS 的支持，如《Towards Remote Procedure Call Encryption By Default》中所述。这些守护进程在指定 `WITH_OPENSSL_KTLS` 时构建。它们使用 KTLS 对所有 NFS RPC 消息流量进行加密/解密，并通过 X.509 证书提供可选的机器身份验证。[ 2b9cbc85d727 ](https://cgit.freebsd.org/src/commit/?id=2b9cbc85d727)​[ 59f6f5e23c1a ](https://cgit.freebsd.org/src/commit/?id=59f6f5e23c1a)

针对 amd64 的 UEFI 固件引导兼容性得到改进。有关详细信息，请参阅 [ loader.efi(8)  ](https://man.freebsd.org/cgi/man.cgi?query=loader.efi&sektion=8&format=html)​`amd64 Nocopy` 部分。[ f75caed644a5 ](https://cgit.freebsd.org/src/commit/?id=f75caed644a5)（由 [FreeBSD 基金会](https://www.freebsdfoundation.org/)赞助）

对许多内核子系统进行了启动时间性能改进。（由 [ https://www.patreon.com/cperciva ](https://www.patreon.com/cperciva) 赞助）

[ nvme(4)  ](https://man.freebsd.org/cgi/man.cgi?query=nvme&sektion=4&format=html) 错误处理得到了显著改进。

IPv4（子）网的最小地址（主机 0）的处理方式已变更，以便在未设置为广播地址的情况下，不将数据包发送为广播。这使得最小地址可用于主机。可以使用 sysctl 参数  `net.inet.ip.broadcast_lowest` 恢复旧的行为。有关背景信息，请参阅 [https://datatracker.ietf.org/doc/draft-schoen-intarea-unicast-lowest-address/](https://datatracker.ietf.org/doc/draft-schoen-intarea-unicast-lowest-address/)。[ fd0765933c3c ](https://cgit.freebsd.org/src/commit/?id=fd0765933c3c)

启动脚本 [ growfs(7)  ](https://man.freebsd.org/cgi/man.cgi?query=growfs&sektion=7&format=html) 现在在扩展根文件系统的同时，如果可能，会添加一个交换分区（如果之前不存在）。这在在 SD 卡上使用 RAW 镜像安装时特别有用。新增了 [ rc.conf(5)  ](https://man.freebsd.org/cgi/man.cgi?query=rc.conf&sektion=5&format=html) 变量——`growfs_swap_size`，它可以控制必要时的添加。有关详细信息，请参阅 [ growfs(7)  ](https://man.freebsd.org/cgi/man.cgi?query=growfs&sektion=7&format=html)。

新增了名为 `zpoolreguid` 的 RC 脚本，它将为一个或多个 zpool 分配一个新的 GUID，在共享数据集的虚拟化环境中很有用。

如果没有 **/etc/hostid** 文件或来自硬件的有效 UUID，则 `hostid` 启动脚本现在将生成一个随机的（版本 4）UUID。此外，如果没有 **/etc/machine-id** 文件，`hostid_save` 脚本将在 **/etc/machine-id** 中存储主机的紧凑版本（没有连字符）。GLib 等库使用此文件。[ 62a149bf6219 ](https://cgit.freebsd.org/src/commit/?id=62a149bf6219)​[ 862aab6281a5 ](https://cgit.freebsd.org/src/commit/?id=862aab6281a5)​[ baf1e9713969 ](https://cgit.freebsd.org/src/commit/?id=baf1e9713969)​[ ecad3f5c4d92 ](https://cgit.freebsd.org/src/commit/?id=ecad3f5c4d92)​[ d6852eed98ed ](https://cgit.freebsd.org/src/commit/?id=d6852eed98ed)

现在可以使用 `defaultrouter_fibN` 和 `ipv6_defaultrouter_fibN`​[ rc.conf(5)  ](https://man.freebsd.org/cgi/man.cgi?query=rc.conf&sektion=5&format=html) 变量为非主要 FIB 添加默认路由，。[ 30659d1dcbcc ](https://cgit.freebsd.org/src/commit/?id=30659d1dcbcc)（由 ScaleEngine Inc. 赞助）

[ bhyve(8)  ](https://man.freebsd.org/cgi/man.cgi?query=bhyve&sektion=8&format=html) 工具增加了 virtio-input 设备仿真支持。这可用于将键盘/鼠标输入事件注入到虚拟机中。命令行语法为：`-s <slot>,virtio-input,/dev/input/eventX`。[ 054accac71e0 ](https://cgit.freebsd.org/src/commit/?id=054accac71e0)

[ kdump(1)  ](https://man.freebsd.org/cgi/man.cgi?query=kdump&sektion=1&format=html) 工具增加了对解码 Linux 系统调用的支持。

新增了 [ nproc(1)  ](https://man.freebsd.org/cgi/man.cgi?query=nproc&sektion=1&format=html) 工具，与同名的 Linux 程序兼容。

[ uuidgen(1)  ](https://man.freebsd.org/cgi/man.cgi?query=uuidgen&sektion=1&format=html) 工具有一个新参数 `-r`，用于生成一个随机的 UUID，版本 4。[ f176fe8e7f63 ](https://cgit.freebsd.org/src/commit/?id=f176fe8e7f63)

[ bhyve(8)  ](https://man.freebsd.org/cgi/man.cgi?query=bhyve&sektion=8&format=html) 虚拟机监视器和内核模块 [ vmm(4)  ](https://man.freebsd.org/cgi/man.cgi?query=vmm&sektion=4&format=html) 现在在虚拟机中支持超过 16 个虚拟 CPU。默认情况下，bhyve 允许每个虚拟机创建与主机上物理 CPU 数相同的虚拟 CPU。此限制可以通过 loader 可调参数 `hw.vmm.maxcpu` 进行调整。[ ee98f99d7a68 ](https://cgit.freebsd.org/src/commit/?id=ee98f99d7a68)

64 位可执行文件默认启用了地址空间布局随机化（ASLR）。如果应用程序出现意外失败，例如段错误，可以根据需要禁用它。要在单个调用中禁用，使用 [ proccontrol(1)  ](https://man.freebsd.org/cgi/man.cgi?query=proccontrol&sektion=1&format=html) 命令：`proccontrol -m aslr -s disable command`。要为二进制文件的所有调用禁用 ASLR，请使用 [ elfctl(1)  ](https://man.freebsd.org/cgi/man.cgi?query=elfctl&sektion=1&format=html) 命令：`elfctl -e +noaslr file`。BUG 应通过问题报告系统 [ https://bugs.freebsd.org ](https://bugs.freebsd.org/) 或在 `freebsd-stable@FreeBSD.org` 邮件列表上报告。[ b014e0f15bc7 ](https://cgit.freebsd.org/src/commit/?id=b014e0f15bc7)（由 Stormshield 赞助）

可以在 amd64 内核中使用 LLVM 的 AddressSanitizer。有关更多信息，请参阅手册页面[ kasan(9)  ](https://man.freebsd.org/cgi/man.cgi?query=kasan&sektion=9&format=html)。[ 38da497a4dfc ](https://cgit.freebsd.org/src/commit/?id=38da497a4dfc)（由 FreeBSD 基金会赞助）

对于英特尔 Alder Lake（第十二代）和 Raptor Lake（第十三代）混合 CPU 上的硬件页面失效问题，已经实施了一种解决方法。该问题可能导致 UFS 和 MSDOSFS 的文件系统损坏，以及可能发生其他内存损坏。通过这种解决方法，小核（E-cores）将自动使用一种更慢的页面失效方法。[ cde70e312c3f ](https://cgit.freebsd.org/src/commit/?id=cde70e312c3f)（由 FreeBSD 基金会赞助）

arm64 的[ linux(4)  ](https://man.freebsd.org/cgi/man.cgi?query=linux&sektion=4&format=html) ABI 状态已与 amd64 的[ linux(4)  ](https://man.freebsd.org/cgi/man.cgi?query=linux&sektion=4&format=html) ABI 保持一致。[ ccc510b46340 ](https://cgit.freebsd.org/src/commit/?id=ccc510b46340)、[ 9931033bbfbe ](https://cgit.freebsd.org/src/commit/?id=9931033bbfbe)

为了提高 `stable` 分支的 ABI 兼容性，CPU 亲和力系统调用现在更容忍比内核使用的 CPU 集小的 CPU 集。这将有助于增加内核集 `MAXCPU` 的大小。[ 47a57144af25 ](https://cgit.freebsd.org/src/commit/?id=47a57144af25)​[ f35093f8d6d8 ](https://cgit.freebsd.org/src/commit/?id=f35093f8d6d8)（由 Juniper Networks, Inc.赞助）

现在可以在运行时使用有日志的软更新的 UFS 文件系统上进行快照。因此，现在可以在使用有日志的软更新运行的活动文件系统上执行后台转储。通过使用 `dump(8)` 的 `-L` 参数请求后台转储。（在先前的版本中，UFS 快照与有日志的软更新不兼容。）[ 78f412987605 ](https://cgit.freebsd.org/src/commit/?id=78f412987605)（由 FreeBSD 基金会赞助）

已经重新集成内核的[ wg(4)  ](https://man.freebsd.org/cgi/man.cgi?query=wg&sektion=4&format=html) WireGuard 驱动程序；它提供了使用 WireGuard 协议的虚拟专用网络（VPN）接口。[ 744bfb213144 ](https://cgit.freebsd.org/src/commit/?id=744bfb213144)（由 Rubicon Communications, LLC ("Netgate") 和 FreeBSD 基金会赞助）

KTLS（内核 TLS 实现）已为 TLS 1.3 添加了接收卸载支持。现在支持 TLS 1.1 到 1.3 的接收卸载；对于 TLS 1.0 到 1.3，支持发送卸载。[ 05a1d0f5d7ac ](https://cgit.freebsd.org/src/commit/?id=05a1d0f5d7ac)（由奈飞赞助）

Radix 表和查找现在在[ ipfw(4)  ](https://man.freebsd.org/cgi/man.cgi?query=ipfw&sektion=4&format=html)中支持 MAC 地址。这允许构建和用于过滤的 MAC 地址表。[ 81cac3906eb9 ](https://cgit.freebsd.org/src/commit/?id=81cac3906eb9)

## 14.0-RELEASE 的新变化

## 用户空间

此部分包括了用户空间应用程序、第三方软件和系统工具的变化和新增内容。

### 用户空间配置变更

root 用户的默认 shell 现在是 [ sh(1)  ](https://man.freebsd.org/cgi/man.cgi?query=sh&sektion=1&format=html)，具有许多用于交互式使用的新功能。 [ d410b585b6f0 ](https://cgit.freebsd.org/src/commit/?id=d410b585b6f0)

默认的邮件传输代理（MTA）现在是 Dragonfly Mail Agent ([ dma(8)  ](https://man.freebsd.org/cgi/man.cgi?query=dma&sektion=8&format=html))，而不再是[ sendmail(8)  ](https://man.freebsd.org/cgi/man.cgi?query=sendmail&sektion=8&format=html)。MTA 的配置通过 [ mailer.conf(5)  ](https://man.freebsd.org/cgi/man.cgi?query=mailer.conf&sektion=5&format=html) 进行。 [ sendmail(8)  ](https://man.freebsd.org/cgi/man.cgi?query=sendmail&sektion=8&format=html)及其配置仍然可用。 [ a67b925ff3e5 ](https://cgit.freebsd.org/src/commit/?id=a67b925ff3e5)

[ rc.conf(5)  ](https://man.freebsd.org/cgi/man.cgi?query=rc.conf&sektion=5&format=html)中已经删除了配置变量 `mta_start_script`，以及启动脚本 `othermta`。 [ 616f32ea6da7 ](https://cgit.freebsd.org/src/commit/?id=616f32ea6da7)

[ jail(8)  ](https://man.freebsd.org/cgi/man.cgi?query=jail&sektion=8&format=html)现在在[ jail.conf(5)  ](https://man.freebsd.org/cgi/man.cgi?query=jail.conf&sektion=5&format=html)文件中支持 `.include` 指令，并支持文件名通配。 [ e82a62943529 ](https://cgit.freebsd.org/src/commit/?id=e82a62943529)

一次性密码设施 OPIE，[ opie(4)  ](https://man.freebsd.org/cgi/man.cgi?query=opie&sektion=4&format=html)，已从基本系统中移除。如果仍然希望使用它，请安装 Port [ security/opie ](https://cgit.freebsd.org/ports/tree/security/opie/)。否则，请确保从你的 PAM 策略中删除或注释掉对 `pam_opie` 和 `pam_opieaccess` 的任何提及。 [ etcupdate(8)  ](https://man.freebsd.org/cgi/man.cgi?query=etcupdate&sektion=8&format=html)通常会处理已存储的策略。 [ 0aa2700123e2 ](https://cgit.freebsd.org/src/commit/?id=0aa2700123e2)

已删除构建配置参数 `SHARED_TOOLCHAIN`。仍然可以使用通用的参数 `NO_SHARED` 构建静态链接的工具链。 [ 77f6be448408 ](https://cgit.freebsd.org/src/commit/?id=77f6be448408)（由 FreeBSD 基金会赞助）

区域设置升级到 CLDR 41.0 和 Unicode 14.0。 [ e87ec409fa9b ](https://cgit.freebsd.org/src/commit/?id=e87ec409fa9b)

为新的法国 bepo 键盘（版本 1.1rc2）（由法国国家标准化组织规范为“NF Z71‐300”）添加了布局配置。 [ abdcd967dc0c ](https://cgit.freebsd.org/src/commit/?id=abdcd967dc0c)

现在，`rc.d`脚本（参见[ rc(8)  ](https://man.freebsd.org/cgi/man.cgi?query=rc&sektion=8&format=html)）即使没有定义 `procname` 或没有 PID 文件，也可以允许具有 `status` 方法。 [ 2651609fcbd7 ](https://cgit.freebsd.org/src/commit/?id=2651609fcbd7)

## 用户空间应用程序变更

添加了工具 [ base64(1)  ](https://man.freebsd.org/cgi/man.cgi?query=base64&sektion=1&format=html) 。 [ 540a99289bb1 ](https://cgit.freebsd.org/src/commit/?id=540a99289bb1)

[ bhyve(8)  ](https://man.freebsd.org/cgi/man.cgi?query=bhyve&sektion=8&format=html) 虚拟化程序现在支持可选的 TPM（可信平台模块）直通支持。这不是直接访问，而是将来自虚拟机的命令转发到物理 TPM。 [ 67c26eb2a57c ](https://cgit.freebsd.org/src/commit/?id=67c26eb2a57c)

[ bhyve(8)  ](https://man.freebsd.org/cgi/man.cgi?query=bhyve&sektion=8&format=html) 中的 GPU 直通已经在 AMD 和 Intel GPU 上得到改进。这是一个正在进行中的工作；直通在所有情况下都不起作用，配置尚未记录。

工具 [ cpuset(1)  ](https://man.freebsd.org/cgi/man.cgi?query=cpuset&sektion=1&format=html) 已从 **/usr/bin** 移动到 **/bin**，以便在启动处理过程中始终可用。 **/usr/bin/cpuset** 现在是一个符号链接。 [ f05948d4e98d ](https://cgit.freebsd.org/src/commit/?id=f05948d4e98d)

[ date(1)  ](https://man.freebsd.org/cgi/man.cgi?query=date&sektion=1&format=html) 工具现在具有 `-z` 参数用于时区转换。 [ 31edf56b1571 ](https://cgit.freebsd.org/src/commit/?id=31edf56b1571)

[ diff(1)  ](https://man.freebsd.org/cgi/man.cgi?query=diff&sektion=1&format=html) 工具现在支持 `--color` 参数以获得彩色输出。 [ f38702e5a52e ](https://cgit.freebsd.org/src/commit/?id=f38702e5a52e)

弃用的 [ fmtree(8)  ](https://man.freebsd.org/cgi/man.cgi?query=fmtree&sektion=8&format=html) 工具已被删除。 [ e4d63c5d5ff8 ](https://cgit.freebsd.org/src/commit/?id=e4d63c5d5ff8)

[ freebsd-update(8)  ](https://man.freebsd.org/cgi/man.cgi?query=freebsd-update&sektion=8&format=html) 现在说明如果升级未在进行中且不需要回滚，则可以删除 **/var/db/freebsd-update** 下的文件。 [ 80b003e81684 ](https://cgit.freebsd.org/src/commit/?id=80b003e81684)（由 FreeBSD 基金会赞助）

新的 [ fwget(8)  ](https://man.freebsd.org/cgi/man.cgi?query=fwget&sektion=8&format=html) 工具会检查系统需要固件的外围设备，并为其安装适当的软件包。目前仅支持 PCI 子系统，已知仅支持 Intel 和 AMD GPU 的显卡固件。 [ d198b8774d2cd198b8774d2c ](https://cgit.freebsd.org/src/commit/?id=d198b8774d2c)（由 Beckhoff Automation GmbH & Co. KG 赞助）

通过一致支持 `-q` 和 `-h` 参数、允许带有 SI 后缀的数字以及去除 [ head(1)  ](https://man.freebsd.org/cgi/man.cgi?query=head&sektion=1&format=html) 中行数的 2^31 限制，提高了 [ head(1)  ](https://man.freebsd.org/cgi/man.cgi?query=head&sektion=1&format=html) 和 [ tail(1)  ](https://man.freebsd.org/cgi/man.cgi?query=tail&sektion=1&format=html) 的可用性。 [ 643ac419fafb ](https://cgit.freebsd.org/src/commit/?id=643ac419fafb)

[ makefs(8)  ](https://man.freebsd.org/cgi/man.cgi?query=makefs&sektion=8&format=html) 现在具有实验性的 ZFS 支持。它可以创建一个 ZFS 池，由单个磁盘 vdev 支持，包含从暂存目录中填充的一个或多个数据集。 [ 240afd8c1fcc ](https://cgit.freebsd.org/src/commit/?id=240afd8c1fcc)（由 FreeBSD 基金会赞助）

移除了 [ minigzip(1)  ](https://man.freebsd.org/cgi/man.cgi?query=minigzip&sektion=1&format=html) 工具。 [ 278d080bad9F ](https://cgit.freebsd.org/src/commit/?id=278d080bad9F)

[ mandoc(1)  ](https://man.freebsd.org/cgi/man.cgi?query=mandoc&sektion=1&format=html) 工具现在在列表 `-width` 处理中解决了宏处理的缺陷，从而获得了更准确的列表列宽。 [ bbb2d2ce4220 ](https://cgit.freebsd.org/src/commit/?id=bbb2d2ce4220)（由 Dell EMC Isilon 赞助）

[ mixer(8)  ](https://man.freebsd.org/cgi/man.cgi?query=mixer&sektion=8&format=html) 工具不再尝试猜测音量是绝对音量还是百分比。现在，它接受一个附加的 `%` 百分比，否则音量为绝对音量。 [ 4014365e4219 ](https://cgit.freebsd.org/src/commit/?id=4014365e4219)

`netcat` 工具 [ nc(1)  ](https://man.freebsd.org/cgi/man.cgi?query=nc&sektion=1&format=html) 现在可以是一个 `if_tun` ([ tun(4)  ](https://man.freebsd.org/cgi/man.cgi?query=tun&sektion=4&format=html)) 代理。 [ cef7ab70ff44 ](https://cgit.freebsd.org/src/commit/?id=cef7ab70ff44)（由 Zenarmor 赞助）（由 OPNsense 赞助）（由 Klara, Inc.赞助）

[ netstat(1)  ](https://man.freebsd.org/cgi/man.cgi?query=netstat&sektion=1&format=html) 工具现在在 `-i` 参数下可计算正确的列宽，使 `-w` 参数不再必需。 [ 372e3d561d82 ](https://cgit.freebsd.org/src/commit/?id=372e3d561d82)

移除了 [ portsnap(8)  ](https://man.freebsd.org/cgi/man.cgi?query=portsnap&sektion=8&format=html) 工具。建议用户使用 `pkg install git`，然后 `git clone https://git.FreeBSD.org/ports.git /usr/ports` 来获取 Ports。 [ df53ae0fdd98 ](https://cgit.freebsd.org/src/commit/?id=df53ae0fdd98)

[ pw(8)  ](https://man.freebsd.org/cgi/man.cgi?query=pw&sektion=8&format=html) 和 [ bsdinstall(8)  ](https://man.freebsd.org/cgi/man.cgi?query=bsdinstall&sektion=8&format=html) 程序现在默认在 **/home** 中为用户创建家目录，而非 **/usr/home**。不再创建 **/home** 的默认符号链接（即指向 **/usr/home**）。 [ bbb2d2ce4220 ](https://cgit.freebsd.org/src/commit/?id=bbb2d2ce4220)

[ sleep(1)  ](https://man.freebsd.org/cgi/man.cgi?query=sleep&sektion=1&format=html) 工具现在接受单位为秒以外的值，并接受多个将被求和的延迟值（例如，`1h 30m`）。 [ 34978f7edd15 ](https://cgit.freebsd.org/src/commit/?id=34978f7edd15)​[ be038c3afcae ](https://cgit.freebsd.org/src/commit/?id=be038c3afcae)

[ sockstat(1)  ](https://man.freebsd.org/cgi/man.cgi?query=sockstat&sektion=1&format=html) 工具现在在 capsicum 中运行。 [ 94dc57159532 ](https://cgit.freebsd.org/src/commit/?id=94dc57159532)​[ c5a2d8c5f517 ](https://cgit.freebsd.org/src/commit/?id=c5a2d8c5f517)

[ systat(1)  ](https://man.freebsd.org/cgi/man.cgi?query=systat&sektion=1&format=html) 工具有一个新命令 `iolat`，可报告由 CAM I/O 调度程序计算的 I/O 延迟。 [ 22054f88914b ](https://cgit.freebsd.org/src/commit/?id=22054f88914b)（由奈飞赞助）

一个新的工具，[ tcpsso(8)  ](https://man.freebsd.org/cgi/man.cgi?query=tcpsso&sektion=8&format=html)，能够将套接字参数应用于现有的 TCP 端点，例如变更拥塞控制模块或 TCP 栈。 [ 881631a2a371 ](https://cgit.freebsd.org/src/commit/?id=881631a2a371)（由奈飞赞助）

Telnet 守护程序，[ telnetd(8)  ](https://man.freebsd.org/cgi/man.cgi?query=telnetd&sektion=8&format=html)，已被移除。如果需要，可以使用 Port [ net/freebsd-telnetd ](https://cgit.freebsd.org/ports/tree/net/freebsd-telnetd/)。客户端不受影响。 [ 0eea46fb1f83 ](https://cgit.freebsd.org/src/commit/?id=0eea46fb1f83)

在默认情况下禁用了参数 `PROFILE`，因此不提供系统库的配置版本。更倾向于使用基于硬件的性能分析（例如 [ hwpmc(4)  ](https://man.freebsd.org/cgi/man.cgi?query=hwpmc&sektion=4&format=html)）。 [ fe52b7f60ef4 ](https://cgit.freebsd.org/src/commit/?id=fe52b7f60ef4)（由 FreeBSD 基金会赞助）

二进制文件中的调试部分在小端目标上默认启用。[ 47363e99d3d3 ](https://cgit.freebsd.org/src/commit/?id=47363e99d3d3)（由 FreeBSD 基金会赞助）

已添加配置以生成 armv7 发行文件，这对于在 arm64 上构建 jail 可能很有用。[ ac099daf6742 ](https://cgit.freebsd.org/src/commit/?id=ac099daf6742)

### 第三方软件更新

**One True Awk**（[ awk(1)  ](https://man.freebsd.org/cgi/man.cgi?query=awk&sektion=1&format=html)）已更新到 20210727，这是第 1 版。 （第 2 版将包含在 14.1-RELEASE 中。）现在除一个 FreeBSD 补丁外，所有的 FreeBSD 补丁都已被上游采纳或丢弃。值得注意的变化包括：不再使用地区（locale）进行范围选择；与 `gawk` 和 `mawk` 有更好的兼容性。请注意，十六进制字符串的解释与早期的 FreeBSD 版本一样被解释为数字。这将在 FreeBSD 15 中变更以符合上游和当前的 POSIX 标准。 [ f39dd6a97844 ](https://cgit.freebsd.org/src/commit/?id=f39dd6a97844)​[ 23f24377b1a9 ](https://cgit.freebsd.org/src/commit/?id=23f24377b1a9)​[ 628bd30ab5a4 ](https://cgit.freebsd.org/src/commit/?id=628bd30ab5a4)

[ bc(1)  ](https://man.freebsd.org/cgi/man.cgi?query=bc&sektion=1&format=html) 和 [ dc(1)  ](https://man.freebsd.org/cgi/man.cgi?query=dc&sektion=1&format=html) 命令已更新到版本 6.6.0，修复了与行编辑和包含多个 read() 命令的复杂脚本的问题，并在 `bc` 的（非标准）扩展数学库中添加了一些功能。

**libbsdxml**（`expat`，[ libbsdxml(3)  ](https://man.freebsd.org/cgi/man.cgi?query=libbsdxml&sektion=3&format=html)）已升级到版本 2.4.7。 [ 7ed8e142a00d ](https://cgit.freebsd.org/src/commit/?id=7ed8e142a00d)

**libfido2** 已升级到版本 1.13.0。 [ f540a43052c1 ](https://cgit.freebsd.org/src/commit/?id=f540a43052c1)​[ 3e696dfb7009 ](https://cgit.freebsd.org/src/commit/?id=3e696dfb7009)​[ 95321fff46ec ](https://cgit.freebsd.org/src/commit/?id=95321fff46ec)（由 FreeBSD 基金会赞助）

**[llvm-objdump(1)](https://man.freebsd.org/cgi/man.cgi?query=llvm-objdump&sektion=1&format=html)** 工具现在始终作为[ objdump(1)  ](https://man.freebsd.org/cgi/man.cgi?query=objdump&sektion=1&format=html)安装。 [ 86edb11e7491 ](https://cgit.freebsd.org/src/commit/?id=86edb11e7491)（由 FreeBSD 基金会赞助）

**OpenSSH** 已升级到版本 9.5p1。完整的发行说明请参阅 [ https://www.openssh.com/txt/release-9.5 ](https://www.openssh.com/txt/release-9.5)。 [ 676824f5cdf9 ](https://cgit.freebsd.org/src/commit/?id=676824f5cdf9)（由 FreeBSD 基金会赞助）

**[scp(1)](https://man.freebsd.org/cgi/man.cgi?query=scp&sektion=1&format=html)** 工具现在默认使用 SFTP 协议，而不是传统的 scp/rcp 协议。这消除了对通配符扩展字符的双引号引用的需要。 [ fb5aabcb990b ](https://cgit.freebsd.org/src/commit/?id=fb5aabcb990b)（由 FreeBSD 基金会赞助）

默认情况下，在[ ssh(1)  ](https://man.freebsd.org/cgi/man.cgi?query=ssh&sektion=1&format=html)中禁用了 RSA/SHA-1 签名。可以在用户的 **~/.ssh/config** 文件中按主机启用它们。 [ 8c22023ca5e1 ](https://cgit.freebsd.org/src/commit/?id=8c22023ca5e1)（由 FreeBSD 基金会赞助）

对于[ ssh(1)  ](https://man.freebsd.org/cgi/man.cgi?query=ssh&sektion=1&format=html)，`VerifyHostKeyDNS` 参数现在默认为 `no`，与 OpenSSH 默认发行一致。`X11Forwarding` 参数也默认为 `no`。 [ 41ff5ea22cb9 ](https://cgit.freebsd.org/src/commit/?id=41ff5ea22cb9)​[ 77934b7a1301 ](https://cgit.freebsd.org/src/commit/?id=77934b7a1301)（由 FreeBSD 基金会赞助）

从 OpenSSH 中删除了 HPN 参数处理。HPN 支持很久以前就已经弃用，但配置参数仍然被接受（并被忽略）以保持向后兼容性。 [ 348bea10b6f2 ](https://cgit.freebsd.org/src/commit/?id=348bea10b6f2)（由 FreeBSD 基金会赞助）

从[ ssh(1)  ](https://man.freebsd.org/cgi/man.cgi?query=ssh&sektion=1&format=html)客户端中删除了 `VersionAddendum` 参数。 [ bffe60ead024 ](https://cgit.freebsd.org/src/commit/?id=bffe60ead024)（由 FreeBSD 基金会赞助）

**OpenSSL** 已升级到版本 3.0.12。这是从版本 1.1.1 的重大升级，已经到达了其生命周期的终点。基本系统的许多组件使用向后兼容的 API，但稍后将进行迁移。 [ aa7957345732 ](https://cgit.freebsd.org/src/commit/?id=aa7957345732)​[ 930cec16d9ee ](https://cgit.freebsd.org/src/commit/?id=930cec16d9ee)​[ b077aed33b7b ](https://cgit.freebsd.org/src/commit/?id=b077aed33b7b)（由 FreeBSD 基金会赞助）

**tcpdump** 已升级到版本 4.99.4。 [ ee67461e5682 ](https://cgit.freebsd.org/src/commit/?id=ee67461e5682)​[ 171a7bbfc048 ](https://cgit.freebsd.org/src/commit/?id=171a7bbfc048)​[ 1ad8d2ee1f7d ](https://cgit.freebsd.org/src/commit/?id=1ad8d2ee1f7d)（由 FreeBSD 基金会赞助）

**libpcap** 已升级到版本 1.10.4。 [ 6f9cba8f8b5e ](https://cgit.freebsd.org/src/commit/?id=6f9cba8f8b5e)​[ dd744a896be3 ](https://cgit.freebsd.org/src/commit/?id=dd744a896be3)（由 FreeBSD 基金会赞助）

**xz** 已升级到版本 5.4.3。

**zlib** 已升级到版本 1.3。

**zstd** 已升级到版本 1.5.2。 （由 Klara，Inc 赞助）

### 废弃的工具

[ mergemaster(8)  ](https://man.freebsd.org/cgi/man.cgi?query=mergemaster&sektion=8&format=html) 已被废弃。其替代品是 [ etcupdate(8)  ](https://man.freebsd.org/cgi/man.cgi?query=etcupdate&sektion=8&format=html)。 [ 398b12691b4f ](https://cgit.freebsd.org/src/commit/?id=398b12691b4f)（由 FreeBSD 基金会赞助）

### 运行时库和 API

`libncursesw` 库（参见 [ ncurses(3X)  ](https://man.freebsd.org/cgi/man.cgi?query=ncurses&sektion=3X&format=html)）已拆分为 `libtinfow` 和 `libncursesw`。链接脚本应使其对使用者透明。现在安装了 [ pkg-config(8)  ](https://man.freebsd.org/cgi/man.cgi?query=pkg-config&sektion=8&format=html) 文件，以便使 Port 能够从基本系统检测 `ncurses` 的设置。 [ 396851c20aeb ](https://cgit.freebsd.org/src/commit/?id=396851c20aeb)

[ ncurses(3X)  ](https://man.freebsd.org/cgi/man.cgi?query=ncurses&sektion=3X&format=html)库现在能够使用 [ terminfo(5)  ](https://man.freebsd.org/cgi/man.cgi?query=terminfo&sektion=5&format=html) 以及 [ termcap(5)  ](https://man.freebsd.org/cgi/man.cgi?query=termcap&sektion=5&format=html)，并首选使用 terminfo。 [ 61f66a1f4403 ](https://cgit.freebsd.org/src/commit/?id=61f66a1f4403)

在 [ ncurses(3X)  ](https://man.freebsd.org/cgi/man.cgi?query=ncurses&sektion=3X&format=html) 中，用于 terminfo 数据库的默认搜索路径现在包括 **/usr/local/share/terminfo**，便于使用来自 Ports 或软件包的数据库。 [ b75fb12b6827 ](https://cgit.freebsd.org/src/commit/?id=b75fb12b6827)

[ qsort_r(3)  ](https://man.freebsd.org/cgi/man.cgi?query=qsort_r&sektion=3&format=html) 的原型已修改以匹配 POSIX，该标准采用了 glibc-based 接口。 [ af3c78886fd8 ](https://cgit.freebsd.org/src/commit/?id=af3c78886fd8)

对于 aarch64（arm64），已经实现了 `COMPAT_LIB32` 构建参数，并默认启用。这为 arm64 系统提供了与 armv7 32 位二进制文件构建和运行大多数 armv7 32 位库和头文件兼容的支持。 [ f1d5183124d3 ](https://cgit.freebsd.org/src/commit/?id=f1d5183124d3)​[ d5d97bed4ab6 ](https://cgit.freebsd.org/src/commit/?id=d5d97bed4ab6)​[ a1b675731301 ](https://cgit.freebsd.org/src/commit/?id=a1b675731301)

## 云支持

本节涉及对云环境的支持的变更。

FreeBSD 现在在 AWS 上提供实验性的 ZFS 根文件系统 EC2 AMI。 （由 [ https://www.patreon.com/cperciva ](https://www.patreon.com/cperciva) 赞助）

FreeBSD 现在在 AWS 上提供实验性的 cloud-init EC2 AMI。有关信息，请参阅 Port [ net/cloud-init ](https://cgit.freebsd.org/ports/tree/net/cloud-init/)。 （由 [ https://www.patreon.com/cperciva ](https://www.patreon.com/cperciva) 赞助）

FreeBSD 现在为 Azure 提供 arm64 和 amd64 镜像。提供了 UFS 和实验性的 ZFS 镜像。现在支持 Gen2 VMs。 （由 FreeBSD 基金会赞助）（由微软赞助）

Microsoft Azure Network Adapter（MANA）VF（虚拟功能）现在得到支持。 [ ce110ea12fce ](https://cgit.freebsd.org/src/commit/?id=ce110ea12fce)（由微软赞助）

Google Virtual NIC（[ gve(4)  ](https://man.freebsd.org/cgi/man.cgi?query=gve&sektion=4&format=html)）现在得到支持。 [ 54dfc97b0bd9 ](https://cgit.freebsd.org/src/commit/?id=54dfc97b0bd9)（由谷歌赞助）

### 内核

本节介绍了对内核配置、系统调优和系统控制参数的变更，这些变更没有被分类到其他地方。

### 通用内核变更

SMP 系统现在在 amd64 和 arm64 上支持最多 1024 个核心。现在可动态分配多内核 CPU，以避免占用过多内存。内核 cpuset ABI 已更新以支持更高的限制。 [ 76887e84be97 ](https://cgit.freebsd.org/src/commit/?id=76887e84be97)​[ d1639e43c589 ](https://cgit.freebsd.org/src/commit/?id=d1639e43c589)​[ 9051987e40c5 ](https://cgit.freebsd.org/src/commit/?id=9051987e40c5)​[ e0c6e8910898 ](https://cgit.freebsd.org/src/commit/?id=e0c6e8910898)（由 FreeBSD 基金会赞助）

ACPI 系统现在支持 `_CR3` 临界待机 (`S3`) 阈值。 [ b8a0dfb17e3b ](https://cgit.freebsd.org/src/commit/?id=b8a0dfb17e3b)

默认禁用 `acpi_timer_test`，强制使用 ACPI-fast 而不是 ACPI-safe，以加快启动过程。可以通过设置可调参数 `hw.acpi.timer_test_enabled=1` 重新启用破解 ACPI 计时器。如果观察到时间问题，请尝试在 [ loader.conf(8)  ](https://man.freebsd.org/cgi/man.cgi?query=loader.conf&sektion=8&format=html) 中使用 `hw.acpi.timer_test_enabled=1` 进行测试，看看是否解决了问题。 [ a8b89dff6ac0 ](https://cgit.freebsd.org/src/commit/?id=a8b89dff6ac0)

[ boottrace(4)  ](https://man.freebsd.org/cgi/man.cgi?query=boottrace&sektion=4&format=html) 是用于在系统启动和关闭期间捕获跟踪事件的新内核用户空间接口。事件注释存在于内核中的启动和关闭路径中；系统工具（[ init(8)  ](https://man.freebsd.org/cgi/man.cgi?query=init&sektion=8&format=html)、[ shutdown(8)  ](https://man.freebsd.org/cgi/man.cgi?query=shutdown&sektion=8&format=html)、[ reboot(8)  ](https://man.freebsd.org/cgi/man.cgi?query=reboot&sektion=8&format=html)）；以及 [ rc(8)  ](https://man.freebsd.org/cgi/man.cgi?query=rc&sektion=8&format=html) 脚本（通过 [ boottrace(8)  ](https://man.freebsd.org/cgi/man.cgi?query=boottrace&sektion=8&format=html)）。 [ boottrace(4)  ](https://man.freebsd.org/cgi/man.cgi?query=boottrace&sektion=4&format=html) 注重易用性，主要面向系统管理员。它在默认的 `GENERIC` 内核中可用，并且可以通过调整 [ sysctl(8)  ](https://man.freebsd.org/cgi/man.cgi?query=sysctl&sektion=8&format=html) 变量来启用。 [ da5b7e90e740 ](https://cgit.freebsd.org/src/commit/?id=da5b7e90e740)​[ 5a8fceb3bd9f ](https://cgit.freebsd.org/src/commit/?id=5a8fceb3bd9f)​[ 7b0a665d72c0 ](https://cgit.freebsd.org/src/commit/?id=7b0a665d72c0)​[ 13ec1e3155c7 ](https://cgit.freebsd.org/src/commit/?id=13ec1e3155c7)​[ 318d0db5fe8a ](https://cgit.freebsd.org/src/commit/?id=318d0db5fe8a)​[ 1ae2c59bcf21 ](https://cgit.freebsd.org/src/commit/?id=1ae2c59bcf21)（由 NetApp, Inc.赞助）（由 Klara, Inc 赞助）

内核加密现在支持 XChaCha20-Poly1035 AEAD 加密。 [ 8f35841f1f35 ](https://cgit.freebsd.org/src/commit/?id=8f35841f1f35)（由 FreeBSD 基金会赞助）

内核加密中添加了 curve25519 的 API。 [ 0c6274a819ff ](https://cgit.freebsd.org/src/commit/?id=0c6274a819ff)（由 FreeBSD 基金会赞助）

FreeBSD 现在可以在 Firecracker VMM 中运行，通过 amd64 `FIRECRACKER` 内核配置。 [ 469ad8603127 ](https://cgit.freebsd.org/src/commit/?id=469ad8603127)（由 [ https://www.patreon.com/cperciva ](https://www.patreon.com/cperciva) 赞助）

FreeBSD 现在重新启动更快。添加了 sysctl  `kern.reboot_wait_time` 以控制在在控制台打印所有内核消息后重新启动之前的延迟。默认为 0。将其设置为 1 会恢复先前的行为（1 秒延迟）。 [ 84ec7df0d796 ](https://cgit.freebsd.org/src/commit/?id=84ec7df0d796)（由 [ https://www.patreon.com/cperciva ](https://www.patreon.com/cperciva) 赞助）

添加了新的 DTrace provider `kinst`，参见 [ dtrace_kinst(4)  ](https://man.freebsd.org/cgi/man.cgi?query=dtrace_kinst&sektion=4&format=html)。该 provider 允许跟踪内核指令，类似于 FBT（函数边界跟踪）提供者，但可以探测所有指令而不仅仅是逻辑入口和返回指令。 [ f0bc4ed144fc ](https://cgit.freebsd.org/src/commit/?id=f0bc4ed144fc)（由 Google, Inc.通过谷歌编程之夏 2022 赞助）

`kinst` 已移植到 arm64 和 riscv。 [ 07864a8a2466 ](https://cgit.freebsd.org/src/commit/?id=07864a8a2466)​[ 2d7bb03adb43 ](https://cgit.freebsd.org/src/commit/?id=2d7bb03adb43)（由 FreeBSD 基金会赞助）

现在可以在 amd64 内核中使用 LLVM 的 MemorySanitizer。有关更多信息，请参见手册页 [ kmsan(9)  ](https://man.freebsd.org/cgi/man.cgi?query=kmsan&sektion=9&format=html) 。 [ a422084abbda ](https://cgit.freebsd.org/src/commit/?id=a422084abbda)（由 FreeBSD 基金会赞助）

现在可以在 arm64 内核以及 amd64 上使用 LLVM 的 AddressSanitizer。有关更多信息，请参见 [ kasan(9)  ](https://man.freebsd.org/cgi/man.cgi?query=kasan&sektion=9&format=html) 手册页。 [ 89c52f9d59fa ](https://cgit.freebsd.org/src/commit/?id=89c52f9d59fa)（由 Juniper Networks, Inc.赞助）（由 Klara, Inc.赞助）

已从内核开放加密框架（OCF）中删除了对非对称加密操作的支持，因为它们不被现代 OpenSSL 版本使用。 [ 76681661be28 ](https://cgit.freebsd.org/src/commit/?id=76681661be28)

添加了一个本机 [ timerfd(2)  ](https://man.freebsd.org/cgi/man.cgi?query=timerfd&sektion=2&format=html) 设施，以便轻松移植使用 timerfd 的 Linux 程序。以前，timerfd 仅在 Linux 仿真下可用。对于仅为 FreeBSD 编写的程序，首选使用 [ kqueue(2)  ](https://man.freebsd.org/cgi/man.cgi?query=kqueue&sektion=2&format=html) EVFILT_TIMER 过滤器来建立任意计时器。 [ af93fea71038 ](https://cgit.freebsd.org/src/commit/?id=af93fea71038)

由 `security.bsd.see_jail_proc`​[ sysctl(8)  ](https://man.freebsd.org/cgi/man.cgi?query=sysctl&sektion=8&format=html) 开关控制的进程可见性策略已经过加固，防止未经授权的用户尝试随机杀死、变更优先级或调试同一子 jail 中具有相同（实际）UID 的进程，即使这些进程对其不可见也会成功。它也可以被 MAC 策略覆盖，就像其他进程可见性策略一样。 [ 7e21c691f295 ](https://cgit.freebsd.org/src/commit/?id=7e21c691f295)​[ 63c01c18a8d3 ](https://cgit.freebsd.org/src/commit/?id=63c01c18a8d3)（由 Kumacom, SAS 赞助）（由 FreeBSD 基金会赞助）

由 `security.bsd.see_other_gids`​[ sysctl(8)  ](https://man.freebsd.org/cgi/man.cgi?query=sysctl&sektion=8&format=html) 开关控制的进程可见性策略已修复，以考虑进程的实际组而不是其有效组，以确定试图访问进程的用户是否是进程组的成员。其原理是，某些用户应该继续看到它们启动的进程，即使它们通过设置组 ID 位而获得更高的权限，而它们不应该看到由特权用户启动的临时进入用户的主组的进程。这种新行为与 `security.bsd.see_other_uids` 一直在为用户 ID 执行的操作相一致（即，考虑一些进程的实际用户 ID 而不是有效 ID）。 [ 26ff4836c888 ](https://cgit.freebsd.org/src/commit/?id=26ff4836c888)（由 Kumacom, SAS 赞助）（由 FreeBSD 基金会赞助）

现在已自动封堵影响 AMD Zen2 处理器的 Zenbleed 漏洞（通过 chicken bit），防止在受影响的机器上发生错误行为和数据泄漏。如果需要，可以通过 ​[ sysctl(8)  ](https://man.freebsd.org/cgi/man.cgi?query=sysctl&sektion=8&format=html)  `machdep.mitigations.zenbleed.enable` 开关手动控制应用这种缓解措施。有关更多信息，请参阅新的 [ mitigations(7)  ](https://man.freebsd.org/cgi/man.cgi?query=mitigations&sektion=7&format=html) 手册页。 [ aea76bab1416 ](https://cgit.freebsd.org/src/commit/?id=aea76bab1416)（由 FreeBSD 基金会赞助）

## 设备和驱动程序

本节包括了自 13.2-RELEASE 以来对设备和设备驱动程序的变更和添加。

### 设备驱动程序

串行通信在引导加载程序、内核和用户空间中的默认速度现在为 115200 bps。请注意，早期的 x86 BIOS 引导加载程序（即 `boot0sio`）不支持 9600 bps 以上的速率，并且没有变更。 `boot0sio` 用户可以设置 `BOOT_COMCONSOLE_SPEED=9600`，以便在所有引导组件中使用 9600，或者使用标准的 `boot0`，并且 `boot2` 阶段的串行端口速率为 115200。 [ 4722ceb7d53e ](https://cgit.freebsd.org/src/commit/?id=4722ceb7d53e)（由 FreeBSD 基金会赞助）

默认的响铃音频现在为 800Hz。可以使用 [ kbdcontrol(1)  ](https://man.freebsd.org/cgi/man.cgi?query=kbdcontrol&sektion=1&format=html) 进行设置。对于希望使用声卡进行蜂鸣的用户，与 [ devd(8)  ](https://man.freebsd.org/cgi/man.cgi?query=devd&sektion=8&format=html) 集成。 [ ba48d52ca6c8 ](https://cgit.freebsd.org/src/commit/?id=ba48d52ca6c8)​[ 4ac3d08a9693 ](https://cgit.freebsd.org/src/commit/?id=4ac3d08a9693)​[ 2533eca1c2b9 ](https://cgit.freebsd.org/src/commit/?id=2533eca1c2b9)（由奈飞赞助）

在使用默认的 [ vt(4)  ](https://man.freebsd.org/cgi/man.cgi?query=vt&sektion=4&format=html) 控制台时，默认情况下不再启用可听的响铃。可以使用以下命令启用它：`sysctl kern.vt.enable_bell=1` 和 `kbdcontrol -b normal`。 [ 225639e7db68 ](https://cgit.freebsd.org/src/commit/?id=225639e7db68)

在 DPAA2（第二代数据路径加速架构，出现在一些 NXP SoC 中的硬件级网络架构）中进行了改进。它运行由 NXP 提供的固件，该固件提供 DPAA2 对象作为抽象层，并提供 `dpni` 网络接口。DPAA2 通道之间的分离已经显着改进，以隔离对 DMA 资源和清理操作的访问，并在网络负载较重（1 Gbit/s 链接）时避免内核崩溃。其他改进包括 FDT / ACPI MDIO 支持，通过 DPAA2 进行网络启动以及单独的命令门户（DPMCP）支持。

已添加对 Arm Corelink DMC-620 内存控制器和 CMN-600 一致性网格网络控制器的支持，已添加到 [ hwpmc(4)  ](https://man.freebsd.org/cgi/man.cgi?query=hwpmc&sektion=4&format=html) 和 `libpmc`。请参阅 [ pmc.dmc-620(3)  ](https://man.freebsd.org/cgi/man.cgi?query=pmc.dmc-620&sektion=3&format=html) 和 [ pmc.cmn-600(3)  ](https://man.freebsd.org/cgi/man.cgi?query=pmc.cmn-600&sektion=3&format=html)。 [ 1459a22787ea ](https://cgit.freebsd.org/src/commit/?id=1459a22787ea)​[ 59191f3573f6 ](https://cgit.freebsd.org/src/commit/?id=59191f3573f6)（由 ARM 赞助）（由 Ampere Computing 赞助）

已实施了有关 i386 和 Book-E powerpc 上影响物理上高于 4 GB 的帧缓冲区地址的帧缓冲地址的修复。 [ a78bb831a17f ](https://cgit.freebsd.org/src/commit/?id=a78bb831a17f)

Intel 无线网卡的 [ iwlwifi(4)  ](https://man.freebsd.org/cgi/man.cgi?query=iwlwifi&sektion=4&format=html) 驱动程序已更新到最新版本，支持 WiFi 6E AX411/AX211/AX210 芯片组，并为即将推出的 BX 和 SC 芯片组做好准备。 (由 FreeBSD 基金会赞助)

Realtek 无线 PCI 接口的 [ rtw88(4)  ](https://man.freebsd.org/cgi/man.cgi?query=rtw88&sektion=4&format=html) 驱动程序已更新。

已添加 KVM 虚拟化时钟的 kvm_clock 驱动程序。 [ 6c69c6bb4c7f ](https://cgit.freebsd.org/src/commit/?id=6c69c6bb4c7f)（由 Juniper Networks, Inc.赞助）（由 Klara, Inc.赞助）

对 Linux 设备驱动程序的 KPI 进行了稳定性修复和增强，以及无线驱动程序的 net80211 层。 (由 FreeBSD 基金会赞助)

现在，默认情况下，NVMe 磁盘是 `nda` 设备，例如 `nda0`；参见 [ nda(4)  ](https://man.freebsd.org/cgi/man.cgi?query=nda&sektion=4&format=html)。在 **/dev** 中为先前的 [ nvd(4)  ](https://man.freebsd.org/cgi/man.cgi?query=nvd&sektion=4&format=html) 设备名称创建了符号链接。但是，配置（例如 [ fstab(5)  ](https://man.freebsd.org/cgi/man.cgi?query=fstab&sektion=5&format=html)）应更新为引用新的设备名称。控制使用 `nda` 设备和符号链接的参数在 [ nda(4)  ](https://man.freebsd.org/cgi/man.cgi?query=nda&sektion=4&format=html) 中有描述。 [ bdc81eeda05d ](https://cgit.freebsd.org/src/commit/?id=bdc81eeda05d)（由奈飞赞助）

先前的 [ qat(4)  ](https://man.freebsd.org/cgi/man.cgi?query=qat&sektion=4&format=html) 驱动程序已替换为 Intel 的 QAT 驱动程序。新版本提供了与芯片组的加密和压缩卸载功能的额外接口。对于大多数用户，这将没有可见的变更；但是，新驱动程序不支持 Atom C2000 芯片组。为了保留对这些芯片组的支持，旧的驱动程序已重命名为 `qat_c2xxx`。因此，在 C2000 硬件上使用 [ qat(4)  ](https://man.freebsd.org/cgi/man.cgi?query=qat&sektion=4&format=html) 的用户需要确保加载的是 [ qat_c2xxx(4)  ](https://man.freebsd.org/cgi/man.cgi?query=qat_c2xxx&sektion=4&format=html) 而不是 [ qat(4)  ](https://man.freebsd.org/cgi/man.cgi?query=qat&sektion=4&format=html)。 [ 78ee8d1c4cda ](https://cgit.freebsd.org/src/commit/?id=78ee8d1c4cda)​[ f4f56ff43dbd ](https://cgit.freebsd.org/src/commit/?id=f4f56ff43dbd)（由英特尔公司赞助）

### 弃用和删除的驱动程序

x86 `GENERIC` 内核配置中已删除 [ pms(4)  ](https://man.freebsd.org/cgi/man.cgi?query=pms&sektion=4&format=html) 驱动程序 `pmspcv`，因为它很大且使用不常见。可以通过在 [ loader.conf(5)  ](https://man.freebsd.org/cgi/man.cgi?query=loader.conf&sektion=5&format=html) 中放置 `pmspcv_load="YES"` 来将其加载为模块。 [ 95e4f5ef7cce ](https://cgit.freebsd.org/src/commit/?id=95e4f5ef7cce)（由 Rubicon Communications, LLC ("Netgate") 赞助）

x86 `GENERIC` 和 `MINIMAL` 内核配置中已删除了 VESA 参数。它仍然可用作内核模块。VESA 不被默认控制台 [ vt(4)  ](https://man.freebsd.org/cgi/man.cgi?query=vt&sektion=4&format=html) 使用。 [ 777526ed8382 ](https://cgit.freebsd.org/src/commit/?id=777526ed8382)​[ b8cf1c5c30a5 ](https://cgit.freebsd.org/src/commit/?id=b8cf1c5c30a5)（由 FreeBSD 基金会赞助）

已删除 ISA 声卡的驱动程序。 [ 92e6b4712b53 ](https://cgit.freebsd.org/src/commit/?id=92e6b4712b53)​[ df51e63eb5d7 ](https://cgit.freebsd.org/src/commit/?id=df51e63eb5d7)​[ aa83e9b189d6 ](https://cgit.freebsd.org/src/commit/?id=aa83e9b189d6)​[ 754decef384a ](https://cgit.freebsd.org/src/commit/?id=754decef384a)​[ 5126e5eeeb5e ](https://cgit.freebsd.org/src/commit/?id=5126e5eeeb5e)​[ 716924cb4832 ](https://cgit.freebsd.org/src/commit/?id=716924cb4832)​[ 9054e296819f ](https://cgit.freebsd.org/src/commit/?id=9054e296819f)（由 FreeBSD 基金会赞助）

从 [ ath(4)  ](https://man.freebsd.org/cgi/man.cgi?query=ath&sektion=4&format=html) 中删除了 AHB 总线前端，因为它仅被 MIPS 使用。 [ 37c8ee8847fa ](https://cgit.freebsd.org/src/commit/?id=37c8ee8847fa)

已删除了弃用的 [ amr(4)  ](https://man.freebsd.org/cgi/man.cgi?query=amr&sektion=4&format=html) 驱动程序。 [ 60de2867c9fc ](https://cgit.freebsd.org/src/commit/?id=60de2867c9fc)（由奈飞赞助）

已删除过时的 [ iscsi_initiator(4)  ](https://man.freebsd.org/cgi/man.cgi?query=iscsi_initiator&sektion=4&format=html)。它的替代品 [ iscsi(4)  ](https://man.freebsd.org/cgi/man.cgi?query=iscsi&sektion=4&format=html) 在几个主要版本之前引入。 [ 48cb3fee2586 ](https://cgit.freebsd.org/src/commit/?id=48cb3fee2586)（由 FreeBSD 基金会赞助）

已删除了弃用的 [ iir(4)  ](https://man.freebsd.org/cgi/man.cgi?query=iir&sektion=4&format=html) 驱动程序。 [ 399188a2c60c ](https://cgit.freebsd.org/src/commit/?id=399188a2c60c)（由奈飞赞助）

已删除了弃用的 [ mn(4)  ](https://man.freebsd.org/cgi/man.cgi?query=mn&sektion=4&format=html) 同步串行驱动程序。 [ 0cff00ae682a ](https://cgit.freebsd.org/src/commit/?id=0cff00ae682a)（由 FreeBSD 基金会赞助）

已删除了弃用的 [ mly(4)  ](https://man.freebsd.org/cgi/man.cgi?query=mly&sektion=4&format=html) 驱动程序。 [ a9620045a5b9 ](https://cgit.freebsd.org/src/commit/?id=a9620045a5b9)（由奈飞赞助）

已弃用的[ nlmrsa(4)  ](https://man.freebsd.org/cgi/man.cgi?query=nlmrsa&sektion=4&format=html)驱动程序已被移除。[ 6a06b00a0d1f ](https://cgit.freebsd.org/src/commit/?id=6a06b00a0d1f)（由 Chelsio Communications 赞助）

已弃用的[ twa(4)  ](https://man.freebsd.org/cgi/man.cgi?query=twa&sektion=4&format=html)驱动程序已被移除。[ 8722e05ae149 ](https://cgit.freebsd.org/src/commit/?id=8722e05ae149)（由奈飞赞助）

## 存储

本节包括了文件系统和其他存储子系统的变更和添加，包括本地和网络存储。

### 通用存储

[ gconcat(8)  ](https://man.freebsd.org/cgi/man.cgi?query=gconcat&sektion=8&format=html)及其内核支持现在具有将在创建 gconcat 设备时不存在的设备追加到连接设备的能力。[ d575e81fbcfa ](https://cgit.freebsd.org/src/commit/?id=d575e81fbcfa)

一个新的[ gunion(8)  ](https://man.freebsd.org/cgi/man.cgi?query=gunion&sektion=8&format=html)工具跟踪对可写磁盘上只读磁盘的变更。这对于对磁盘进行临时变更（如文件系统修复或软件升级）并随后提交或还原变更非常有用。[ c7996ddf8000 ](https://cgit.freebsd.org/src/commit/?id=c7996ddf8000)（由奈飞赞助）

在调试和解决通用文件系统代码中 vnode 回收问题的过程中，与 vnode 相关的统计信息的 sysctl 现在已经分组到 `vfs.vnode` 下，以提高可见性。[ d3e647891243 ](https://cgit.freebsd.org/src/commit/?id=d3e647891243)

### NFS 变更

NFS 现在支持在 VNET jail 中运行 NFS 服务器，包括[ nfsd(8)  ](https://man.freebsd.org/cgi/man.cgi?query=nfsd&sektion=8&format=html)，[ nfsuserd(8)  ](https://man.freebsd.org/cgi/man.cgi?query=nfsuserd&sektion=8&format=html)，[ mountd(8)  ](https://man.freebsd.org/cgi/man.cgi?query=mountd&sektion=8&format=html)，[ gssd(8)  ](https://man.freebsd.org/cgi/man.cgi?query=gssd&sektion=8&format=html)和[ rpc.tlsservd(8)  ](https://man.freebsd.org/cgi/man.cgi?query=rpc.tlsservd&sektion=8&format=html)。VNET jail 必须位于自己的文件系统上，必须设置 jail 参数 `allow.nfsd`，而 `enforce_statfs` 不能设置为 `0`。不允许使用 UDP 和 pNFS 服务器配置。[ 7344856e3a6d ](https://cgit.freebsd.org/src/commit/?id=7344856e3a6d)和其他许多

对于 NFSv4 挂载，NFS 客户端现在默认使用 NFS 服务器支持的 NFSv4 的最高小版本，而不是小版本 0。挂载参数 `minorversion` 可用于覆盖此默认值。[ a145cf3f73c7 ](https://cgit.freebsd.org/src/commit/?id=a145cf3f73c7)

FreeBSD NFS 客户端现在可以设置为使用 1M 字节的 I/O 大小，通过`tunablevfs.maxbcachebuf`；Linux NFS 客户端也可以进行 1M 字节的 I/O。需要增加`kern.ipc.maxsockbuf`的值。控制台消息将建议其设置。请注意，在[ nfsd(8)  ](https://man.freebsd.org/cgi/man.cgi?query=nfsd&sektion=8&format=html)未运行时，可以通过 sysctl `vfs.nfsd.srvmaxio`将 FreeBSD NFS 服务器的最大 I/O 大小增加到任何 2 的幂次方，最多为 1M 字节。[ ee29e6f31111 ](https://cgit.freebsd.org/src/commit/?id=ee29e6f31111)

如果会话中断，NFSv4.1/4.2 客户端和服务器现在将生成控制台消息，建议用户检查确保字符串 **/etc/hostid** 的值对所有 NFSv4.1/4.2 客户端都是唯一的。[ b875d4f5ddcb ](https://cgit.freebsd.org/src/commit/?id=b875d4f5ddcb)​[ 0685c73cfe88 ](https://cgit.freebsd.org/src/commit/?id=0685c73cfe88)

NFSv4.1/4.2 挂载使用挂载参数 `intr` 现在基本可用，尽管不是 100％正确，但也使用了挂载参数 `nolockd`。有关详细信息，请参见手册页 [ mount_nfs(8)  ](https://man.freebsd.org/cgi/man.cgi?query=mount_nfs&sektion=8&format=html)。[ 981ef32230b2 ](https://cgit.freebsd.org/src/commit/?id=981ef32230b2)​[ 33721eb991d8 ](https://cgit.freebsd.org/src/commit/?id=33721eb991d8)

对于 Kerberized NFSv4.1/4.2 挂载，现在可以使用新的挂载参数 `syskrb5`。NFSv4.1/4.2 的一个特性用于提供 `AUTH_SYS` 身份验证，因此在挂载时不需要 Kerberos 凭证。请参见[ mount_nfs(8)  ](https://man.freebsd.org/cgi/man.cgi?query=mount_nfs&sektion=8&format=html)。[ 896516e54a8c ](https://cgit.freebsd.org/src/commit/?id=896516e54a8c)

在 NFS 服务器中，NFS 挂载协议中已添加对 `SP4_MACH_CRED` 的支持。该功能由 Linux NFSv4.1/4.2 客户端用于 Kerberized 挂载。以前通过回退处理，但现在直接支持。[ 330aa8acdec7 ](https://cgit.freebsd.org/src/commit/?id=330aa8acdec7)​[ ff2f1f691cdb ](https://cgit.freebsd.org/src/commit/?id=ff2f1f691cdb)

### UFS 变更

现在可以使用在运行启用了日志软更新的 UFS 文件系统上的快照执行后台文件系统检查。 （由 FreeBSD 基金会赞助）

已向超级块、柱组映射和 inode 添加了校验散列，以检测错误。对于超级块（120）和柱组（20），进行的检查远比以前进行的魔数检查要广泛得多。（由 FreeBSD 基金会赞助）

[ libufs(3)  ](https://man.freebsd.org/cgi/man.cgi?query=libufs&sektion=3&format=html)库已更新以包含这些检查，以便所有文件系统工具现在都会执行这些检查。检查在一个内核文件中实现，该文件也被 libufs 包含。对 libufs 的另一个变更是，查找备用超级块的代码已从[ fsck_ffs(8)  ](https://man.freebsd.org/cgi/man.cgi?query=fsck_ffs&sektion=8&format=html)移到了共享文件中，因此它现在可以在内核加载器中使用，以及所有文件系统工具。 （由 FreeBSD 基金会赞助）

### ZFS 变更

OpenZFS 已升级到 2.2 版。新功能包括：

- 块克隆，允许文件副本中块的浅复制。这是可选的，默认情况下禁用；可以使用 `sysctl vfs.zfs.bclone_enabled=1` 启用。
- scrub 错误日志（`zpool scrub -e`）
- BLAKE3 校验和，速度快，现在是推荐的安全校验和
- 修正的 `zfs receive` 可以修复损坏的数据
- vdev 和 zpool 用户属性，类似于数据集用户属性。

性能改进包括：

- 完全自适应 ARC，一个统一的 ARC，最小化手动调整的需求
- zstd 早期中止，提高对不可压缩数据的效率
- I/O 预取改进
- 一般优化。

已在 32 位 powerpc/powerpcspe 上启用 ZFS。[ 63715498ac6b ](https://cgit.freebsd.org/src/commit/?id=63715498ac6b)

### 其他存储变更

现在，[ msdosfs(5)  ](https://man.freebsd.org/cgi/man.cgi?query=msdosfs&sektion=5&format=html)文件系统在 FAT12 和 FAT16 文件系统的根目录中记录可用目录项（例如 EFI 引导分区），并将其报告为 inode。[ c33db74b5323 ](https://cgit.freebsd.org/src/commit/?id=c33db74b5323)

现在，[ msdosfs(5)  ](https://man.freebsd.org/cgi/man.cgi?query=msdosfs&sektion=5&format=html)文件系统正确计算 FAT12 和 FAT16 文件系统的可用块和已用块，并且不再拒绝挂载使用有效但不常见参数创建的文件系统。[ 0728695c63e ](https://cgit.freebsd.org/src/commit/?id=0728695c63e)

合成文件系统（[ devfs(5)  ](https://man.freebsd.org/cgi/man.cgi?query=devfs&sektion=5&format=html)，[ procfs(5)  ](https://man.freebsd.org/cgi/man.cgi?query=procfs&sektion=5&format=html)等）现在报告已使用 0 块，以便它们不被报告为 100％ 使用率。[ 88a795e80c03 ](https://cgit.freebsd.org/src/commit/?id=88a795e80c03f)

添加了一个名为[ tarfs(5)  ](https://man.freebsd.org/cgi/man.cgi?query=tarfs&sektion=5&format=html)的文件系统，其支持由 POSIX tar 档案支持，可选择使用[ zstd(1)  ](https://man.freebsd.org/cgi/man.cgi?query=zstd&sektion=1&format=html)进行压缩。[ 69d94f4c7608 ](https://cgit.freebsd.org/src/commit/?id=69d94f4c7608)（由 Juniper Networks，Inc.赞助）（由 Klara，Inc.赞助）

## 引导变更

本节包括了引导加载程序、引导菜单和其他与引导相关的变更。

### 引导加载程序变更

lua 风格的[ loader(8)  ](https://man.freebsd.org/cgi/man.cgi?query=loader&sektion=8&format=html)现在将解释在 `loader_conf_files` 中出现的 **.lua** 文件为 lua，并在沙盒中执行它们。现有的加载器环境变量在沙盒中作为全局变量可用，成功执行配置文件后，任何设置的全局变量，如果不是表值，都将反映在加载器环境中。具有不是有效 lua 名称的名称的环境变量可以作为 `_ENV` 的索引访问；例如，`_ENV[ 'net.fibs']`。[ 3cb2f5f369ec ](https://cgit.freebsd.org/src/commit/?id=3cb2f5f369ec)

EC2 实例现在在可用的情况下使用 UEFI 引导，大大加速了引导过程。[ b43d7aa09b3c ](https://cgit.freebsd.org/src/commit/?id=b43d7aa09b3c)​[ bcf9147144f3 ](https://cgit.freebsd.org/src/commit/?id=bcf9147144f3)（由[ https://www.patreon.com/cperciva ](https://www.patreon.com/cperciva)赞助）

## 网络

本节说明了影响 FreeBSD 网络的变更。

### 通用网络

[ carp(4)  ](https://man.freebsd.org/cgi/man.cgi?query=carp&sektion=4&format=html)现在支持配置 carp 消息发送到的地址，允许使用单播地址。这在某些虚拟配置中很有用。请参见[ carp(4)  ](https://man.freebsd.org/cgi/man.cgi?query=carp&sektion=4&format=html)和[ ifconfig(8)  ](https://man.freebsd.org/cgi/man.cgi?query=ifconfig&sektion=8&format=html)。[ 137818006de5 ](https://cgit.freebsd.org/src/commit/?id=137818006de5)

在[ if_bridge(4)  ](https://man.freebsd.org/cgi/man.cgi?query=if_bridge&sektion=4&format=html)上的第 3 层过滤将执行一些不安全的操作，因此 `net.link.bridge.pfil_member` 和 `net.link.bridge.pfil_bridge` 现在默认为 0。[ 22893e584032 ](https://cgit.freebsd.org/src/commit/?id=22893e584032)

[ netlink(4)  ](https://man.freebsd.org/cgi/man.cgi?query=netlink&sektion=4&format=html)是 RFC 3549 中定义的用户/内核通信协议，主要用于网络配置。它已经得到扩展、改进并启用了默认。已将许多网络配置工具转换为使用 netlink。[ 3091d980f581 ](https://cgit.freebsd.org/src/commit/?id=3091d980f581)

已删除不推荐使用的 `NgATM`（netgraph ATM 支持）和残余的 ATM 支持。

[ pf(4)  ](https://man.freebsd.org/cgi/man.cgi?query=pf&sektion=4&format=html)包过滤器现在支持使用 OpenBSD 语法和行为进行清理。如果没有 FreeBSD 清理规则，则全局参数 `set reassemble yes | no [ no-df]` 确定是否进行分组重组。清理，例如设置 tos、ttl 等，可以在匹配和传递规则中完成，这也使其具有状态。与 OpenBSD 一样，现在完全支持匹配规则，不仅适用于[ dummynet(4)  ](https://man.freebsd.org/cgi/man.cgi?query=dummynet&sektion=4&format=html)队列。[ 39282ef356db ](https://cgit.freebsd.org/src/commit/?id=39282ef356db)（由 InnoGames GmbH 赞助）

现在可以使用 IPv6 传输 [ pfsync(4)  ](https://man.freebsd.org/cgi/man.cgi?query=pfsync&sektion=4&format=html)。[ 6fc7fc2dbb2b ](https://cgit.freebsd.org/src/commit/?id=6fc7fc2dbb2b)（由 InnoGames GmbH 赞助）（由 FreeBSD 基金会赞助）

已扩展[ pfsync(4)  ](https://man.freebsd.org/cgi/man.cgi?query=pfsync&sektion=4&format=html)数据包格式以改进对排队、清理和路由规则的支持。此格式与旧版本不兼容。可以使用 `ifconfig pfsync0 version 1301` 选择旧格式。如果 pfsync 集群的成员没有同时升级，则这一点尤为重要。

已将 WiFi 6 支持添加到 wpa（[ wpa_supplicant(8)  ](https://man.freebsd.org/cgi/man.cgi?query=wpa_supplicant&sektion=8&format=html)和[ hostapd(8)  ](https://man.freebsd.org/cgi/man.cgi?query=hostapd&sektion=8&format=html)）。[ c1d255d3ffdb ](https://cgit.freebsd.org/src/commit/?id=c1d255d3ffdb)​[ 3968b47cd974 ](https://cgit.freebsd.org/src/commit/?id=3968b47cd974)​[ bd452dcbede6 ](https://cgit.freebsd.org/src/commit/?id=bd452dcbede6)

### 互联网网络

IPv6 over IPv4 的 `6to4` 接口，[ if_stf(4)  ](https://man.freebsd.org/cgi/man.cgi?query=if_stf&sektion=4&format=html)，现在支持 IPv6 Rapid Deployment（6rd，IPv6 快速部署）（RFC5969）。[ 19dc64451179 ](https://cgit.freebsd.org/src/commit/?id=19dc64451179)（由 Rubicon Communications, LLC（"Netgate"）赞助）

[ rtsol(8)  ](https://man.freebsd.org/cgi/man.cgi?query=rtsol&sektion=8&format=html)和[ rtsold(8)  ](https://man.freebsd.org/cgi/man.cgi?query=rtsold&sektion=8&format=html)程序现在具有`-i`参数，可禁用默认情况下使用的最多一秒的随机延迟。这些程序在[ rc.conf(5)  ](https://man.freebsd.org/cgi/man.cgi?query=rc.conf&sektion=5&format=html)中的默认参数包括 `-i`。[ 231bac4ccc43 ](https://cgit.freebsd.org/src/commit/?id=231bac4ccc43)​[ e29711da2352 ](https://cgit.freebsd.org/src/commit/?id=e29711da2352)（由[ https://www.patreon.com/cperciva ](https://www.patreon.com/cperciva)赞助）

IPv6 `nodeinfo`（RFC 4620）的处理现已默认禁用。[ b73183d1a243 ](https://cgit.freebsd.org/src/commit/?id=b73183d1a243)（由 FreeBSD 基金会赞助）

[ sysctl(8)  ](https://man.freebsd.org/cgi/man.cgi?query=sysctl&sektion=8&format=html)参数 `net.inet.tcp.nolocaltimewait` 现在默认启用。这样可以防止为本地终止的 TCP 连接创建 timewait 条目。[ 92b3e07229ba ](https://cgit.freebsd.org/src/commit/?id=92b3e07229ba)

TCP 的默认拥塞控制机制现在是 CUBIC。对于长时间的数据传输，CUBIC 在与 NewReno 竞争时得到了稍微更高的可用带宽的成绩。[ bb1d472d79f7 ](https://cgit.freebsd.org/src/commit/?id=bb1d472d79f7)（由 NetApp, Inc.赞助）

IPv4 已变更为不广播子网上的最小地址（主机 0），除非它配置为广播地址。这允许子网上的最小地址用于主机。[ fd0765933c3c ](https://cgit.freebsd.org/src/commit/?id=fd0765933c3c)

### 硬件支持

该部分包括了对物理机器、虚拟机监视器和虚拟化环境的一般硬件支持，以及不适用于本文其他部分的硬件变更和更新。

请查看[ 14.0-RELEASE 支持的硬件列表 ](https://www.freebsd.org/releases/14.0R/hardware)，以及[ 平台页面 ](https://www.freebsd.org/platforms/)以获取支持的完整 CPU 架构列表。

### 硬件体系结构支持

本项目不再提供带有 14.0-RELEASE 的 armv6 架构支持。

已删除对 MIPS 架构及相关硬件的支持。MIPS 将在其生命周期内继续在 13-STABLE 分支上得到支持。

已淘汰对 RISC-V 架构的软件浮点变体 riscv64sf 的支持。所有可用的硬件都受到常规 riscv64 架构的支持。

### 虚拟化支持

## 文档

该部分包括了随基本系统一起提供的手册页面（[ man(1)  ](https://man.freebsd.org/cgi/man.cgi?query=man&sektion=1&format=html)）和其他文档的变更。

### Man 页面

对[ hier(7)  ](https://man.freebsd.org/cgi/man.cgi?query=hier&sektion=7&format=html)页面进行了许多调整和清理，以提高准确性。

已审查并更新了第 9 节，内核文档中的许多页面，以确保准确性。

内核文档手册页的介绍，[ intro(9)  ](https://man.freebsd.org/cgi/man.cgi?query=intro&sektion=9&format=html) 已完全重写。[ 84f9f2c5cf78 ](https://cgit.freebsd.org/src/commit/?id=84f9f2c5cf78)（由 FreeBSD 基金会赞助）

已重新编写和改进了[ mi_switch(9)  ](https://man.freebsd.org/cgi/man.cgi?query=mi_switch&sektion=9&format=html)页面。[ 175db7b58270 ](https://cgit.freebsd.org/src/commit/?id=175db7b58270)（由 FreeBSD 基金会赞助）

添加了新的[ kern_yield(9)  ](https://man.freebsd.org/cgi/man.cgi?query=kern_yield&sektion=9&format=html)页面。[ 30cd6fd75d46 ](https://cgit.freebsd.org/src/commit/?id=30cd6fd75d463)（由 FreeBSD 基金会赞助）

删除了第 9 节中一些已过时的页面。[ d1c7405ef68a ](https://cgit.freebsd.org/src/commit/?id=d1c7405ef68a)​[ 52f9a2823c64 ](https://cgit.freebsd.org/src/commit/?id=52f9a2823c64)​[ b54391a1f831 ](https://cgit.freebsd.org/src/commit/?id=b54391a1f831)（由 FreeBSD 基金会赞助）

## Ports 和软件包基础设施

该部分包括了 FreeBSD Ports、软件包基础设施以及软件包维护和安装程序的变更。

### 安装程序变更

## 有关后续  FreeBSD 版本的一般说明

FreeBSD 15.0 预计将不包括对 armv7 以外的 32 位平台的支持。armv6、i386 和 powerpc 平台已被淘汰，并将被移除。64 位系统仍将能够运行较旧的 32 位二进制文件。

我们预计在 FreeBSD 15.0 中支持 armv7 作为 2 级架构，并可能在 FreeBSD 16.0 中删除 armv7。关于 armv7 在 15.x 和 16.x 的支持状态，我们将在 15.0 发行时提供更新。

通过参数 `COMPAT_FREEBSD32` 在 64 位平台上执行 32 位二进制文件的支持将继续至少在 stable/15 和 stable/16 分支上。通过 `cc -m32` 编译个别 32 位应用程序的支持也将至少在 stable/15 分支上继续，其中包括在 **/usr/include** 中的适当头文件和在 **/usr/lib32** 中的库。

Ports 将不包括对 FreeBSD 15.0 和以后版本的淘汰 32 位平台的支持。这些未来版本将不包括适用于淘汰的 32 位平台的二进制包或从 ports 构建软件包的支持。

FreeBSD stable/14 和更早版本的分支将保留现有的 32 位内核和系统支持。在 ports 系统支持的情况下，Ports 将保留对在 stable/14 和更早版本分支上为 32 位系统构建 ports 和软件包的支持。但是，所有 32 位平台都是 2 级 或 3 级，应预期随着上游淘汰 32 位平台，对个别 Port 的支持将降级。

按照当前的支持计划，stable/14 将在 FreeBSD 14.0-RELEASE 发行后的 5 年后达到生命周期结束（EOL）。stable/14 的 EOL 将参数着对淘汰的 32 位平台的支持结束，包括源代码发行、预构建软件包和从 Ports 构建应用程序的支持。随着 2023 年 11 月发行 FreeBSD 14.0-RELEASE，对淘汰的 32 位平台的支持将于 2028 年 11 月结束。

本项目可能会选择在 FreeBSD 15.0 发行时通过在 15.0 或以后扩展对一个或多个淘汰平台的某种程度的支持来变更此方法。任何变更将由社区反馈和支持这些平台的承诺驱动。使用 FreeBSD 14.0-RELEASE 和随后的版本，或者 stable/14 分支，以迁移至 32 位平台。

---

**最后修改于：** 2023 年 11 月 20 日，由[ Mike Karels ](https://cgit.freebsd.org/doc/commit/?id=37f329d574)进行。

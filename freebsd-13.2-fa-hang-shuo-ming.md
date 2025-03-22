# FreeBSD 13.2-RELEASE 发行说明（2023 年 4 月 11 日）

- 原文链接 [FreeBSD 13.2-RELEASE Release Notes](https://www.freebsd.org/releases/13.2R/relnotes/)

## 摘要

FreeBSD 13.2-RELEASE 的发布说明包含了自 13-STABLE 开发线以来对 FreeBSD 基本系统所做变更的摘要。本文件列出了自上次发布以来发布的相关安全通告，以及对 FreeBSD 内核和用户态的重大变更。此外，还提供了有关升级的一些简要说明。

## 介绍

本文档包含 FreeBSD 13.2-RELEASE 的发布说明。它介绍了最近添加、变更或删除的 FreeBSD 特性，并提供了一些关于从之前版本升级的说明。

这些发布说明适用于自 13-STABLE 创建以来，13-STABLE 开发分支上的最新版本。有关该分支上的预构建二进制发行版的信息，请访问 [https://www.FreeBSD.org/releases/](https://www.freebsd.org/releases/)。

这些发布说明适用于位于 13-STABLE 开发分支上的一个版本点，该版本位于 13.1-RELEASE 和未来的 13.3-RELEASE 之间。有关该分支上的预构建二进制发行版的信息，请访问 [https://www.FreeBSD.org/releases/](https://www.freebsd.org/releases/)。

该 FreeBSD 13.2-RELEASE 的分发版是一个正式的 RELEASE 版本。可以在 [https://www.FreeBSD.org/releases/](https://www.freebsd.org/releases/) 和镜像站点找到。有关获取此版本（及其他）FreeBSD 发行版的更多信息，请参见 [FreeBSD 手册](https://docs.freebsd.org/en/books/handbook/)中的[获取 FreeBSD 附录](https://docs.freebsd.org/en/books/handbook//mirrors)。

所有用户在安装 FreeBSD 之前都应查阅发布错误文档。错误文档会更新一些在发布周期末期或发布后发现的“突发”信息。通常，它包含已知的漏洞、安全通告以及文档的修正。FreeBSD 13.2-RELEASE 的最新错误文档可以在 FreeBSD 网站上找到。

本文档介绍了自 13.1-RELEASE 以来 FreeBSD 中最具用户可见性的新增或变更功能。一般来说，本文所述的变更是 13-STABLE 分支的特有变更，除非特别标记为已合并特性。

典型的发布说明项包括发布后的安全通告、新的驱动程序或硬件支持、新命令或选项、重大错误修复或第三方软件升级。它们也可能列出对主要 Port/软件包或发布工程实践的变更。显然，发布说明无法列出两个版本之间对 FreeBSD 所做的每个变更；本文件主要关注安全通告、用户可见的变更以及重大架构改进。

## 从先前版本升级 FreeBSD

使用 [freebsd-update(8)](https://man.freebsd.org/cgi/man.cgi?query=freebsd-update&sektion=8&format=html) 工具支持在 RELEASE 版本之间（以及各种安全分支的快照）进行二进制升级。 [二进制升级程序](https://docs.freebsd.org/en/books/handbook/cutting-edge/#freebsdupdate-upgrade) 会更新未修改的用户态工具以及作为官方 FreeBSD 发行版一部分分发的未修改的 GENERIC 内核。 [freebsd-update(8)](https://man.freebsd.org/cgi/man.cgi?query=freebsd-update&sektion=8&format=html) 工具要求被升级的主机必须具备互联网连接。

支持基于源代码的升级（即从源代码重新编译 FreeBSD 基本系统）到先前版本，具体按 `/usr/src/UPDATING` 中的说明进行操作。

所有 PowerPC 架构的用户，在成功安装内核和世界之后，必须手动运行 `kldxref /boot/kernel`。

>升级 FreeBSD 之前应备份 **所有** 数据和配置文件。


>安装新用户态软件后，正在运行的守护进程仍来自先前版本。在通过第二次调用 `freebsd-update` 安装用户级组件，或通过使用 `installworld` 从源代码进行升级后，系统应重新启动以启动新软件。例如，旧版本的 `sshd` 在安装新版本的 `/usr/sbin/sshd` 后无法正确处理传入连接；重启后，新的 `sshd` 和其他守护进程将启动。

## 用户态

本节涉及对用户态应用程序、第三方软件和系统工具的变更和新增内容。

### 用户态配置变更

[growfs(7)](https://man.freebsd.org/cgi/man.cgi?query=growfs&sektion=7&format=html) 启动脚本现在将在扩展根文件系统时添加交换分区（如果可能），且如果之前未存在交换分区。这在使用原始映像安装到 SD 卡时尤其有用。新增了 [rc.conf(5)](https://man.freebsd.org/cgi/man.cgi?query=rc.conf&sektion=5&format=html) 变量 `growfs_swap_size`，可以根据需要控制交换分区的添加。详细信息请参见 [growfs(7)](https://man.freebsd.org/cgi/man.cgi?query=growfs&sektion=7&format=html)。

`zfskeys` 启动脚本支持自动加载存储在 ZFS 上的密钥。[2411090f6940](https://cgit.freebsd.org/src/commit/?id=2411090f6940)（由 Klara Inc. 赞助）

新增了 RC 脚本 `zpoolreguid`，用于为一个或多个 zpool 分配新的 GUID，在虚拟化环境中共享数据集时非常有用。

`hostid` 启动脚本现在将在没有 `/etc/hostid` 文件且硬件没有有效 UUID 时生成一个随机（版本 4）UUID。此外，如果没有 `/etc/machine-id` 文件，`hostid_save` 脚本将把一个压缩版的 hostid（没有连字符的版本）存储在 `/etc/machine-id` 中。此文件由 GLib 等库使用。[17333d92643d](https://cgit.freebsd.org/src/commit/?id=17333d92643d) [a379d5c5efb2](https://cgit.freebsd.org/src/commit/?id=a379d5c5efb2) [71d88613d129](https://cgit.freebsd.org/src/commit/?id=71d88613d129)

现在可以通过使用变量 `defaultrouter_fibN` 和 `ipv6_defaultrouter_fibN` [rc.conf(5)](https://man.freebsd.org/cgi/man.cgi?query=rc.conf&sektion=5&format=html) ，为除主路由表外的其他 FIB 添加默认路由。[c6ec1b441ad3](https://cgit.freebsd.org/src/commit/?id=c6ec1b441ad3)（由 ScaleEngine Inc. 赞助）

### 用户态应用程序变更

工具 [bhyve(8)](https://man.freebsd.org/cgi/man.cgi?query=bhyve&sektion=8&format=html) 新增了 virtio-input 设备仿真支持。这将用于将键盘/鼠标输入事件注入到客户机中。命令行语法为：`-s <slot>,virtio-input,/dev/input/eventX`。[6192776124c5](https://cgit.freebsd.org/src/commit/?id=6192776124c5)

工具 [kdump(1)](https://man.freebsd.org/cgi/man.cgi?query=kdump&sektion=1&format=html) 新增了对 Linux 系统调用的解码支持。

工具 [killall(1)](https://man.freebsd.org/cgi/man.cgi?query=killall&sektion=1&format=html) 现在允许通过语法 `-t pts/N` 向具有其控制终端的进程发送信号，[pts(4)](https://man.freebsd.org/cgi/man.cgi?query=pts&sektion=4&format=html) 中使用。[a76fa7bb6cb7](https://cgit.freebsd.org/src/commit/?id=a76fa7bb6cb7)

新增工具 [nproc(1)](https://man.freebsd.org/cgi/man.cgi?query=nproc&sektion=1&format=html) ，与同名的 Linux 程序兼容。

工具 [timeout(1)](https://man.freebsd.org/cgi/man.cgi?query=timeout&sektion=1&format=html) 已从 `/usr/bin` 移动到 `/bin`。

工具 [pciconf(8)](https://man.freebsd.org/cgi/man.cgi?query=pciconf&sektion=8&format=html) 新增了对解码 ACS 扩展能力的支持。[dde4103a465b](https://cgit.freebsd.org/src/commit/?id=dde4103a465b)（由 Chelsio Communications 赞助）

工具 [procstat(1)](https://man.freebsd.org/cgi/man.cgi?query=procstat&sektion=1&format=html) 现在可以通过新增的 `advlock` 命令打印关于文件的建议锁的信息。[f9daaf452a8a](https://cgit.freebsd.org/src/commit/?id=f9daaf452a8a)

工具 [pwd_mkdb(8)](https://man.freebsd.org/cgi/man.cgi?query=pwd_mkdb&sektion=8&format=html) 工具不再将 `/etc/master.passwd` 中的注释复制到 `/etc/passwd` 中。[3e955733117d](https://cgit.freebsd.org/src/commit/?id=3e955733117d)

MSS clamping 在 [ppp(8)](https://man.freebsd.org/cgi/man.cgi?query=ppp&sektion=8&format=html) 中得到了改进。[301bff9bdd62](https://cgit.freebsd.org/src/commit/?id=301bff9bdd62)

在 [prometheus_sysctl_exporter(8)](https://man.freebsd.org/cgi/man.cgi?query=prometheus_sysctl_exporter&sektion=8&format=html) 中变更了指标别名，以避免由于冲突的指标名称而混淆 Prometheus 服务器。UMA 区域 `tcp_log_bucket` 已重命名为 `tcp_log_id_bucket`，`tcp_log_node` 被重命名为 `tcp_log_id_node` 以保持一致性。不再导出描述中带有 `(LEGACY)` 的 sysctl 变量，这些变量是由  sysctl ZFS 替换的，许多已别名为相同的 Prometheus 指标名称（如 `vfs.zfs.arc_max` 和 `vfs.zfs.arc.max`）。[e4f508d5a211](https://cgit.freebsd.org/src/commit/?id=e4f508d5a211)（由 Axcient 赞助）

[uuidgen(1)](https://man.freebsd.org/cgi/man.cgi?query=uuidgen&sektion=1&format=html) 工具新增了 `-r` 选项，用于生成随机 UUID，版本 4。[8fd1953b7eb2](https://cgit.freebsd.org/src/commit/?id=8fd1953b7eb2)

当由 [inetd(8)](https://man.freebsd.org/cgi/man.cgi?query=inetd&sektion=8&format=html) 调用时，`ctlstat -P` 现在将生成适合 Prometheus 导入的输出；详见 [ctlstat(8)](https://man.freebsd.org/cgi/man.cgi?query=ctlstat&sektion=8&format=html)。[f7896015fcde](https://cgit.freebsd.org/src/commit/?id=f7896015fcde)（由 Axcient 赞助）

### 第三方软件

Gavin Howard 的 `bc` 已升级到版本 6.2.4。

`expat`（`libbsdxml`）已升级到版本 2.5.0。

`file` 已升级到版本 5.43。

`less` 已升级到版本 608。

`libarchive` 已升级到版本 3.6.2，修复了许多可靠性问题。发布说明可查看 [https://github.com/libarchive/libarchive/releases](https://github.com/libarchive/libarchive/releases)。

`libedit` 已升级到版本 2022-04-11。

`LLVM` 和 `clang` 编译器已升级到版本 14.0.5。

现已在 `powerpc64` 及其变体上启用支持的 `LLVM` sanitizers。

`mandoc` 已升级到版本 1.14.6。

`OpenSSH` 已升级到版本 9.3p1。

`OpenSSL` 已升级到版本 1.1.1t。

`sendmail` 已升级到版本 8.17.1。[68e86d5265bc](https://cgit.freebsd.org/src/commit/?id=68e86d5265bc)

`sqlite3` 已升级到版本 3.40.1。

`tzcode` 已升级到版本 2022g，改进了时区变化检测并修复了可靠性问题。

`tzdata` 已升级到版本 2023c。

`unbound` 已升级到版本 1.17.1。

`xz` 已升级到版本 5.4.1。

`xz-embedded` 已升级到版本 3f438e15109229bb14ab45f285f4bff5412a9542。

`zlib` 已升级到版本 1.2.13。

### 运行时库和 API

`libmd` 增加了对 SHA-512/224 的支持。[e04ee7d95ef6](https://cgit.freebsd.org/src/commit/?id=e04ee7d95ef6)（由 Klara, Inc. 赞助）

现已支持 Linux 风格的系统调用跟踪，通过 [sysdecode(3)](https://man.freebsd.org/cgi/man.cgi?query=sysdecode&sektion=3&format=html) 和 [kdump(1)](https://man.freebsd.org/cgi/man.cgi?query=kdump&sektion=1&format=html)。

本地 pthread 库函数现在可以支持 Linux 语义。

## 内核

本节涉及内核配置、系统调优以及未分类的系统控制参数的变更。


### 一般内核变更

[bhyve(8)](https://man.freebsd.org/cgi/man.cgi?query=bhyve&sektion=8&format=html) 虚拟机监控器和内核模块 [vmm(4)](https://man.freebsd.org/cgi/man.cgi?query=vmm&sektion=4&format=html) 现在支持在虚拟机中使用超过 16 个 vCPU。默认情况下，bhyve 允许每个虚拟机创建与主机物理 CPU 数量相同的 vCPU。此限制可以通过加载器调节选项 `hw.vmm.maxcpu` 来调整。[3e02f8809aec](https://cgit.freebsd.org/src/commit/?id=3e02f8809aec)

默认启用了 64 位可执行文件的地址空间布局随机化（ASLR）。如果应用程序出现意外故障（例如，段错误），可以根据需要禁用 ASLR。要禁用单次调用，可以使用 [proccontrol(1)](https://man.freebsd.org/cgi/man.cgi?query=proccontrol&sektion=1&format=html) 命令：`proccontrol -m aslr -s disable command`。要禁用所有二进制文件的 ASLR 调用，可以使用 [elfctl(1)](https://man.freebsd.org/cgi/man.cgi?query=elfctl&sektion=1&format=html) 命令：`elfctl -e +noaslr file`。问题应通过问题报告系统 [https://bugs.freebsd.org](https://bugs.freebsd.org/) 提交，或通过 `freebsd-stable@FreeBSD.org` 邮件列表报告。[10192e77cfac](https://cgit.freebsd.org/src/commit/?id=10192e77cfac)（由 Stormshield 赞助）

已实现针对 Intel Alder Lake（第十二代）和 Raptor Lake（第十三代）混合 CPU 的硬件页面失效问题的解决方法。该漏洞可能导致 UFS 和 MSDOSFS 文件系统损坏，并可能导致其他内存损坏。通过此解决方法，小核（E 核心）会自动使用较慢的页面失效方法。[567cc4e6bfd9](https://cgit.freebsd.org/src/commit/?id=567cc4e6bfd9)（由 FreeBSD 基金会赞助）

新增内核配置选项 `SPLIT_KERNEL_DEBUG`，用于控制将内核和模块的调试数据分割成独立的文件。该选项与选项 `WITHOUT_KERNEL_SYMBOLS` 相互作用，后者的操作方式与 13.0-RELEASE 和 13.1-RELEASE 中不同，但与早期版本相似；它现在仅控制调试数据的安装。默认情况下为 `WITH_KERNEL_SYMBOLS` 和 `WITH_SPLIT_KERNEL_DEBUG`，允许将不含调试数据的内核和模块安装在 /boot 中，将独立的调试文件安装在 `/usr/lib/debug` 中，这与 13.0-RELEASE 之前的版本相同。使用 `WITHOUT_KERNEL_SYMBOLS` 和 `WITH_SPLIT_KERNEL_DEBUG` 时，生成独立的调试文件，但不安装，类似于早期版本中使用 `WITHOUT_KERNEL_SYMBOLS` 的情况。最后，使用 `WITHOUT_KERNEL_SYMBOLS` 和 `WITHOUT_SPLIT_KERNEL_DEBUG` 时，将内核和模块与内置调试信息一起安装到 `/boot` 中，这与 13.1-RELEASE 中使用 `WITHOUT_KERNEL_SYMBOLS` 的情况相同。[0c4d13c521aa](https://cgit.freebsd.org/src/commit/?id=0c4d13c521aa)（由 FreeBSD 基金会赞助）

在 PowerPC 上，支持 pseries 的 ISA 3.0 中的 radix pmap。这应使得 pseries 在 POWER9 实例上显著加速，因为现在管理 pmap 所需的超调用更少。[c74c77531248](https://cgit.freebsd.org/src/commit/?id=c74c77531248)

现已在 arm64 上为 Linux 进程提供 [ptrace(2)](https://man.freebsd.org/cgi/man.cgi?query=ptrace&sektion=2&format=html) 支持。[99950e8beb72](https://cgit.freebsd.org/src/commit/?id=99950e8beb72)

为了提高 `stable` 分支的 ABI 兼容性，CPU 亲和性系统调用现在可以更宽容地处理比内核使用的 CPU 集合小的 CPU 集合。这将促进 `MAXCPU`（内核 CPU 集合的大小）增加。[72bc1e6806cc](https://cgit.freebsd.org/src/commit/?id=72bc1e6806cc)

为保存 CPU 浮动点状态跨信号传递，64 位 [linux(4)](https://man.freebsd.org/cgi/man.cgi?query=linux&sektion=4&format=html) ABI 增加了支持。[0b82c544de58](https://cgit.freebsd.org/src/commit/?id=0b82c544de58)，[20d601714206](https://cgit.freebsd.org/src/commit/?id=20d601714206)

[linux(4)](https://man.freebsd.org/cgi/man.cgi?query=linux&sektion=4&format=html) ABI 中的 vDSO（虚拟动态共享对象）支持已基本完成。[a340b5b4bd48](https://cgit.freebsd.org/src/commit/?id=a340b5b4bd48)

arm64 上的 [linux(4)](https://man.freebsd.org/cgi/man.cgi?query=linux&sektion=4&format=html) ABI 已与 amd64 上的 [linux(4)](https://man.freebsd.org/cgi/man.cgi?query=linux&sektion=4&format=html) ABI 达到一致。[0b82c544de58](https://cgit.freebsd.org/src/commit/?id=0b82c544de58)，[a340b5b4bd48](https://cgit.freebsd.org/src/commit/?id=a340b5b4bd48)

## 设备和驱动程序

本节介绍了自 13.1-RELEASE 以来，设备和设备驱动程序的变更和新增内容。

### 设备驱动程序

[em(4)](https://man.freebsd.org/cgi/man.cgi?query=em&sektion=4&format=html) 驱动程序现在可以正确支持新款芯片 82580 和 i350 上的完整接收缓冲区大小范围。[3f8306cf8e2d](https://cgit.freebsd.org/src/commit/?id=3f8306cf8e2d)

[ena(4)](https://man.freebsd.org/cgi/man.cgi?query=ena&sektion=4&format=html) 驱动程序已升级到 2.6.2 版本。（由亚马逊赞助）

已为 [hwpmc(4)](https://man.freebsd.org/cgi/man.cgi?query=hwpmc&sektion=4&format=html) 实现了对 Intel Alder Lake CPU 的基本支持。[b8ef2ca9eae9](https://cgit.freebsd.org/src/commit/?id=b8ef2ca9eae9)

[ice(4)](https://man.freebsd.org/cgi/man.cgi?query=ice&sektion=4&format=html) 驱动程序已更新至 1.37.7-k 版本。

[irdma(4)](https://man.freebsd.org/cgi/man.cgi?query=irdma&sektion=4&format=html) RDMA 驱动程序已为 Intel E810 以太网控制器引入，支持 RoCEv2 和 iWARP 协议，以每个 PF 方式运行，默认使用 RoCEv2，并已升级至 1.1.5-k 版本。[42bad04a2156](https://cgit.freebsd.org/src/commit/?id=42bad04a2156)（由英特尔公司赞助）

现在已提供对 DPAA2（第二代数据路径加速架构，一种在某些 NXP SoC 中找到的硬件级网络架构）的初步支持。它运行 NXP 提供的固件，作为抽象层提供 DPAA2 对象，并提供一个 `dpni` 网络接口。[d5a64a935bc9](https://cgit.freebsd.org/src/commit/?id=d5a64a935bc9)（由 Bare Enthusiasm :) 和 Traverse Technologies 赞助）

[iwlwifi(4)](https://man.freebsd.org/cgi/man.cgi?query=iwlwifi&sektion=4&format=html) 驱动程序已更新，用于支持 Intel 无线接口。（由 FreeBSD 基金会赞助）

[rtw88(4)](https://man.freebsd.org/cgi/man.cgi?query=rtw88&sektion=4&format=html) 驱动程序已添加，用于支持多个 Realtek 无线 PCI 接口。目前仅限于 802.11 a/b/g 操作。更多信息请参见 [https://wiki.freebsd.org/WiFi/Rtw88](https://wiki.freebsd.org/WiFi/Rtw88)。

已为支持 Linux 设备驱动程序的 KPI 添加了许多新功能和改进。（由 FreeBSD 基金会赞助）

## 存储

本节介绍了文件系统和其他存储子系统（本地和网络存储）的变更和新增内容。

### NFS 变更

已修复导致 NFS 服务器挂起的问题；该问题是由 TCP 中 SACK 处理的 bug 引起的。

### UFS 变更

现在可以在运行启用了日志软更新的 UFS 文件系统上进行快照。因此，现在可以在运行日志软更新的在线文件系统上执行后台转储。通过使用 `-L` 参数来请求后台转储：[dump(8)](https://man.freebsd.org/cgi/man.cgi?query=dump&sektion=8&format=html)。在以前的版本中，UFS 快照与日志软更新不兼容。[3f908eed27b4](https://cgit.freebsd.org/src/commit/?id=3f908eed27b4)（由 FreeBSD 基金会赞助）

## 启动加载器变更

本节介绍了启动加载器、启动菜单和其他启动相关的变更。

### 启动加载器变更

变量 `teken.fg_color` 和 `teken.bg_color` [loader.conf(5)](https://man.freebsd.org/cgi/man.cgi?query=loader.conf&sektion=5&format=html) 现在接受 `bright` 或 `light` 前缀（以及颜色号 8 到 15）来选择亮色。[1dcb6002c500](https://cgit.freebsd.org/src/commit/?id=1dcb6002c500)（由 FreeBSD 基金会赞助）。另见 [233ab015c0d7](https://cgit.freebsd.org/src/commit/?id=233ab015c0d7)

修复了多个导致视频控制台输出消失的 bug。问题通常是在启动加载器启动内核后出现挂起。（由奈飞赞助）

## 网络

本节介绍了影响 FreeBSD 网络功能的变更。

### 一般网络

内核的 [wg(4)](https://man.freebsd.org/cgi/man.cgi?query=wg&sektion=4&format=html) WireGuard 驱动程序已重新集成；它通过 WireGuard 协议提供虚拟私人网络（VPN）接口。[5ae69e2f10da](https://cgit.freebsd.org/src/commit/?id=5ae69e2f10da)（由 Rubicon Communications, LLC（"Netgate"）和 FreeBSD 基金会赞助）

KTLS（内核 TLS 实现）已为 TLS 1.3 添加接收卸载支持。现在支持 TLS 1.1 至 1.3 的接收卸载；TLS 1.0 至 1.3 的发送卸载也得到了支持。[1462dc95f796](https://cgit.freebsd.org/src/commit/?id=1462dc95f796)（由奈飞赞助）

现在提供 [netlink(4)](https://man.freebsd.org/cgi/man.cgi?query=netlink&sektion=4&format=html) 网络配置协议。它是 RFC 3549 中定义的通信协议，使用原始套接字在用户空间和内核之间交换配置数据。第三方路由程序和 [linux(4)](https://man.freebsd.org/cgi/man.cgi?query=linux&sektion=4&format=html) ABI 使用该协议。[6058f6cc48f5](https://cgit.freebsd.org/src/commit/?id=6058f6cc48f5)（不包括在 13.2-RELEASE 的 GENERIC 配置中，但作为内核模块提供）

现在支持在 [ipfw(4)](https://man.freebsd.org/cgi/man.cgi?query=ipfw&sektion=4&format=html) 中使用 Radix 表和查找来处理 MAC 地址。这使得可以构建和使用 MAC 地址表来进行过滤。[c31f8b7bd895](https://cgit.freebsd.org/src/commit/?id=c31f8b7bd895)

内核模块 dpdk_lpm4 和 dpdk_lpm6 现在可用，可以通过 [loader.conf(5)](https://man.freebsd.org/cgi/man.cgi?query=loader.conf&sektion=5&format=html) 加载。它们为具有大量路由表的主机提供优化的路由功能。可以通过 [route(8)](https://man.freebsd.org/cgi/man.cgi?query=route&sektion=8&format=html) 配置，并且是模块化 FIB 查找机制的一部分。[0ca122044369](https://cgit.freebsd.org/src/commit/?id=0ca122044369)

TCP 和 SCTP 中有多个 bug 修复。

## 关于后续 FreeBSD 版本的一般说明

已弃用 `OPIE`，并将在 FreeBSD 14.0 中移除。

已弃用同步串行驱动程序 [ce(4)](https://man.freebsd.org/cgi/man.cgi?query=ce&sektion=4&format=html) 和 [cp(4)](https://man.freebsd.org/cgi/man.cgi?query=cp&sektion=4&format=html) ，并将在 FreeBSD 14.0 中移除。

ISA 声卡的驱动程序已弃用，并将在 FreeBSD 14.0 中移除。[d7620b6ec941](https://cgit.freebsd.org/src/commit/?id=d7620b6ec941)（由 FreeBSD 基金会赞助）

已弃用工具 [mergemaster(8)](https://man.freebsd.org/cgi/man.cgi?query=mergemaster&sektion=8&format=html)，并将在 FreeBSD 14.0 中移除。它的替代工具是 [etcupdate(8)](https://man.freebsd.org/cgi/man.cgi?query=etcupdate&sektion=8&format=html)。[5fa16e3c50c5](https://cgit.freebsd.org/src/commit/?id=5fa16e3c50c5)（由 FreeBSD 基金会赞助）

已弃用工具 [minigzip(1)](https://man.freebsd.org/cgi/man.cgi?query=minigzip&sektion=1&format=html) ，并将在 FreeBSD 14.0 中移除。[84d3fc26e3a2](https://cgit.freebsd.org/src/commit/?id=84d3fc26e3a2)

在 netgraph 中，ATM 的剩余组件（NgATM）已弃用，并将在 FreeBSD 14.0 中移除。已移除对 ATM NIC 的支持。

已弃用 Telnet 守护进程 [telnetd(8)](https://man.freebsd.org/cgi/man.cgi?query=telnetd&sektion=8&format=html) ，并将在 FreeBSD 14.0 中移除。Telnet 客户端不受影响。

已弃用 [geom(8)](https://man.freebsd.org/cgi/man.cgi?query=geom&sektion=8&format=html) 中的 VINUM 类，并将在后续版本中移除。

### 默认 `CPUTYPE` 变更

从 FreeBSD-13.0 开始，i386 架构的默认 `CPUTYPE` 将从 `486` 变更为 `686`。

这意味着，默认情况下，生成的二进制文件将要求 686 类 CPU，包括但不限于 FreeBSD 发布工程团队提供的二进制文件。FreeBSD 13.x 仍将继续支持旧的 CPU，但需要此功能的用户将需要为官方支持自行构建发行版。

由于 i486 和 i586 CPU 主要用于嵌入式市场，因此预计对普通用户的影响将是最小的，因为这些 CPU 类型的新硬件早已不再使用，而部署的这类系统的基础大部分接近退休年龄，统计上来看。

做出这一变更时考虑了多个因素。例如，i486 没有 64 位原子操作，虽然可以在内核中模拟，但无法在用户空间中模拟。此外，32 位 amd64 库从一开始就是 i686。

由于大多数 32 位测试是由开发人员使用内核选项 `COMPAT_FREEBSD32`，在 64 位硬件上使用 lib32 库进行的，这一变更确保了更好的覆盖率和用户体验。这也符合大多数 Linux® 发行版长期以来的做法。

预计这将是 i386 默认 `CPUTYPE` 的最后一次升级。

>此变更不会影响 FreeBSD 12.x 系列的版本。

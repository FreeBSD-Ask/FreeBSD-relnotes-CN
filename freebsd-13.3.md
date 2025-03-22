# FreeBSD 13.3-RELEASE 发行说明（2024 年 5 月 5 日）

- 原文地址：[FreeBSD 13.3-RELEASE Release Notes](https://www.freebsd.org/releases/13.3R/relnotes/)

## 摘要

FreeBSD 13.3-RELEASE 的发布说明包含了对 13-STABLE 开发主线中的 FreeBSD 基本系统所做变更的总结。本文列出了自上次发布以来发布的相关安全通告，并介绍了 FreeBSD 内核和用户空间的重大变更。还简要说明了从先前版本升级的相关事项。

## 简介

本文档包含了 FreeBSD 13.3-RELEASE 的发布说明。它简述了 FreeBSD 最近添加、改变和删除的功能，还提供了一些从旧版本升级的注意事项。

本次发布的分行版代表了自 13-STABLE 创建以来，13-STABLE 开发分支的最新位置。有关该分支上预构建二进制发行版的信息，请参见 [https://www.FreeBSD.org/releases/](https://www.freebsd.org/releases/)。

本文档所适用的 RELEASE 版本代表了 13-STABLE 开发分支中的一个节点，位于 13.2-RELEASE 和后续的 13.4-RELEASE 之间。有关该分支上预构建二进制发行版的信息，请参见 [https://www.FreeBSD.org/releases/](https://www.freebsd.org/releases/)。

此 FreeBSD 13.3-RELEASE 版本是 RELEASE 分行版。它可以在 [https://www.FreeBSD.org/releases/](https://www.freebsd.org/releases/) 和任何镜像站点找到。有关获取此版本或其他版本的更多信息，请参见 [FreeBSD 手册](https://docs.freebsd.org/en/books/handbook//) 中的附录 [获取 FreeBSD](https://docs.freebsd.org/en/books/handbook//mirrors)。

在安装 FreeBSD 之前，建议所有用户都先查阅下发行勘误文档。勘误文档会根据发布周期结束和发布后发现的“最后时刻”信息进行更新，通常包含已知的 bug、安全通告以及文档的更正。可以在 FreeBSD 网站上找到最新的 FreeBSD 13.3-RELEASE 勘误文档。

本文档介绍了 FreeBSD 13-STABLE 中自 13.2-RELEASE 以来最为用户可见的新特性或变更。请注意，本文中描述的某些变更也可以在 FreeBSD 14.0-RELEASE 中找到。

典型的发布说明项目记录了自 13.2-RELEASE 以来发布的安全通告、新的驱动程序和硬件支持、新的命令和参数、主要的 bug 修复，及第三方的软件升级。它们还可能列出主要 Port/包的变更和发布工程实践。显然，发布说明无法列出 FreeBSD 在两个版本之间做出的每一个变更；本文档主要关注安全通告、用户可见的变更以及主要的架构改进。

## 从以前的 FreeBSD 版本升级

使用工具 [freebsd-update(8)](https://man.freebsd.org/cgi/man.cgi?query=freebsd-update&sektion=8&format=html) 能在 RELEASE 版本之间（以及各种安全分支的快照）进行二进制升级。有关升级的详细信息，请参阅发布特定的升级程序：[FreeBSD 13.3-RELEASE 升级信息](https://www.freebsd.org/releases/13.3R/installation/#upgrade-binary)，以及 FreeBSD 手册中的 [二进制升级程序](https://docs.freebsd.org/en/books/handbook/cutting-edge/#freebsdupdate-upgrade)。这将更新未修改的用户空间工具以及作为官方 FreeBSD 发行版一部分的未修改的 GENERIC 内核。 [freebsd-update(8)](https://man.freebsd.org/cgi/man.cgi?query=freebsd-update&sektion=8&format=html) 工具要求升级的主机必须具备互联网连接。

从旧版本进行基于源代码的升级（即通过重新编译 FreeBSD 基本系统）也是支持的，请按照 `/usr/src/UPDATING` 中的说明进行。

>在升级 FreeBSD 前，请确保备份了 **所有** 数据和配置文件。

>在安装新的用户空间软件后，正在运行的守护进程仍然来自先前的版本。在第二次调用 `freebsd-update` 安装用户级组件，或通过源代码升级，再使用 `installworld` 命令安装后，应重启系统来启动所有新的软件。例如，较旧版本的 `sshd` 在安装新的 `/usr/sbin/sshd` 后无法正确处理传入连接；重启后将启动新的 `sshd` 和其他守护进程。


## 用户空间

本节涉及对用户空间应用程序、第三方软件和系统实用程序的变更和新增功能。

### 用户空间配置变更

[libtacplus(3)](https://man.freebsd.org/cgi/man.cgi?query=libtacplus&sektion=3&format=html) 库已改进，现 [tacplus.conf(5)](https://man.freebsd.org/cgi/man.cgi?query=tacplus.conf&sektion=5&format=html) 遵循 POSIX shell 语法规则。如果共享密钥包含单引号、双引号或反斜杠字符，且未正确引用和转义，可能会导致 `TACACS+` 认证失败。该库现在允许配置最多 255 个附加 AV 配对。[5761f8a7de9f](https://cgit.freebsd.org/src/commit/?id=5761f8a7de9f)（由 Klara, Inc. 赞助）

像 [login(1)](https://man.freebsd.org/cgi/man.cgi?query=login&sektion=1&format=html) 这样的程序，使用 [setusercontext(3)](https://man.freebsd.org/cgi/man.cgi?query=setusercontext&sektion=3&format=html)，现在能根据凭据从 `~/.login_conf` 文件中设置进程优先级。此外，可以在 [login.conf(5)](https://man.freebsd.org/cgi/man.cgi?query=login.conf&sektion=5&format=html) 中，将优先级指定为 `inherit`，表示进程优先级将继承自父进程。同样，现在也可以将 `umask` 值指定为 `inherit`。[8b359002747a](https://cgit.freebsd.org/src/commit/?id=8b359002747a) [e074746fec21](https://cgit.freebsd.org/src/commit/?id=e074746fec21) [16e02df98ad6](https://cgit.freebsd.org/src/commit/?id=16e02df98ad6)（由 Kumacom SAS 赞助）

通过 [periodic(8)](https://man.freebsd.org/cgi/man.cgi?query=periodic&sektion=8&format=html) 生成的配置文件和安全输出报告（发送给系统管理员）现在使用了简化的上下文，以减少无关内容。生成每日输出时，传给 [diff(1)](https://man.freebsd.org/cgi/man.cgi?query=diff&sektion=1&format=html) 的参数，可以通过 [rc.conf(5)](https://man.freebsd.org/cgi/man.cgi?query=rc.conf&sektion=5&format=html) 中的变量 `daily_diff_flags` 进行控制；安全脚本所用的 [diff(1)](https://man.freebsd.org/cgi/man.cgi?query=diff&sektion=1&format=html) 参数由 `security_status_diff_flags` 控制。[4c14a3a6aebe](https://cgit.freebsd.org/src/commit/?id=4c14a3a6aebe) [6d9195b5f763](https://cgit.freebsd.org/src/commit/?id=6d9195b5f763)

用于下载闰秒信息的默认链接已更新为使用标准源，因为旧链接已经失效。[d19b59cfe594](https://cgit.freebsd.org/src/commit/?id=d19b59cfe594)

在使用 arm64 `RPI` 系统的树莓派设备上，默认启用了守护进程 [powerd(8)](https://man.freebsd.org/cgi/man.cgi?query=powerd&sektion=8&format=html)，这样系统可以在需要时全速运行。非默认睿频设置的用户也许需要禁用之。[e889b5a892b6](https://cgit.freebsd.org/src/commit/?id=e889b5a892b6)

现在，可以通过 [rc.conf(5)](https://man.freebsd.org/cgi/man.cgi?query=rc.conf&sektion=5&format=html) 中的变量 `<服务>_umask` 为某个服务指定 `umask`，其中 `<服务>` 是服务名称。[2d6a03dd43c7](https://cgit.freebsd.org/src/commit/?id=2d6a03dd43c7)

### 用户空间应用程序变更

[head(1)](https://man.freebsd.org/cgi/man.cgi?query=head&sektion=1&format=html) 和 [tail(1)](https://man.freebsd.org/cgi/man.cgi?query=tail&sektion=1&format=html) 程序现在一致地支持参数 `-q`（安静）和 `-v`（详细）。数字参数现在可以使用 [expand_number(3)](https://man.freebsd.org/cgi/man.cgi?query=expand_number&sektion=3&format=html) 支持的 SI 后缀。[585762c3733f](https://cgit.freebsd.org/src/commit/?id=585762c3733f)

现在可以使用 LLVM 提供的工具 [objdump(1)](https://man.freebsd.org/cgi/man.cgi?query=objdump&sektion=1&format=html) 。某些 LLVM objdump 参数的输出格式与 GNU objdump 不同；可以使用 [readelf(1)](https://man.freebsd.org/cgi/man.cgi?query=readelf&sektion=1&format=html) 检查 ELF 文件，并且可以通过 Port devel/binutils 和二进制包安装 GNU objdump。

[tftpd(8)](https://man.freebsd.org/cgi/man.cgi?query=tftpd&sektion=8&format=html) 服务器现在可以配置为允许在 chroot 环境中写入非世界可写的文件，使用新的 `-S` 参数。[b71dde1aeba2](https://cgit.freebsd.org/src/commit/?id=b71dde1aeba2)



### 第三方软件

`expat` 已升级至 2.6.0 版本。

已应用若干 Heimdal 安全修复，以缓解 Kerberos 密钥分发中心中的漏洞。

`libfido2` 认证令牌库已更新至 1.13.0 版本。[b27bad1e0373](https://cgit.freebsd.org/src/commit/?id=b27bad1e0373) [079a1c2059e7](https://cgit.freebsd.org/src/commit/?id=079a1c2059e7) [d79e0d1735e3](https://cgit.freebsd.org/src/commit/?id=d79e0d1735e3)（由 FreeBSD 基金会赞助）

`LLVM` 和 `clang` 编译器已升级至 17.0.6 版本。

`nvi`（[vi(1)](https://man.freebsd.org/cgi/man.cgi?query=vi&sektion=1&format=html)）已升级至 2.2.1 版本。

`sendmail` 已升级至 8.18.1 版本。此版本默认执行更严格的 RFC 合规性，特别是在行尾方面。这可能会导致接收来自不合规邮件传输代理（MTA）的消息时出现问题；有关缓解措施，请参阅 [https://ftp.sendmail.org/RELEASE_NOTES](https://ftp.sendmail.org/RELEASE_NOTES) 中的 8.18.1 发布说明。[b36ddb27b3b9](https://cgit.freebsd.org/src/commit/?id=b36ddb27b3b9)

`OpenSSH` 已更新至 9.6p1 版本，包括若干安全修复。最重要的修复是针对 SSH 传输协议中新发现的漏洞。现在 [ssh-keygen(1)](https://man.freebsd.org/cgi/man.cgi?query=ssh-keygen&sektion=1&format=html) 默认生成 Ed25519 密钥。[sshd(8)](https://man.freebsd.org/cgi/man.cgi?query=sshd&sektion=8&format=html) 现在能够准确保留子系统命令和参数的引号。[f26eafdfafb0](https://cgit.freebsd.org/src/commit/?id=f26eafdfafb0) [221a6bc397ad](https://cgit.freebsd.org/src/commit/?id=221a6bc397ad) [2cd20d9bc807](https://cgit.freebsd.org/src/commit/?id=2cd20d9bc807)（由 FreeBSD 基金会赞助）

`tzdata` 已升级至 2024a 版本。

`unbound` 已升级至 1.19.1 版本，包括安全修复。[c6edb21e3763](https://cgit.freebsd.org/src/commit/?id=c6edb21e3763)

`xz` 已升级至 5.4.5 版本。

[zlib(3)](https://man.freebsd.org/cgi/man.cgi?query=zlib&sektion=3&format=html) 库已更新至 1.3.1 版本。[f2de7ba78a49](https://cgit.freebsd.org/src/commit/?id=f2de7ba78a49) [05e3998add1c](https://cgit.freebsd.org/src/commit/?id=05e3998add1c)

## 内核

本节涉及内核配置、系统调优以及未分类的系统控制参数的变更。

### 一般内核变更

[intro(9)](https://man.freebsd.org/cgi/man.cgi?query=intro&sektion=9&format=html) 核心编程接口介绍已完全重写。[5a0c410787b8](https://cgit.freebsd.org/src/commit/?id=5a0c410787b8)（由 FreeBSD 基金会赞助）

## 设备和驱动

本节涉及自 13.2-RELEASE 以降设备和设备驱动的变更与新增。

### 设备驱动

现在，x86 系统可支持多个 PCI MCFG 区域，使得支持访问非 0 域（段）的 PCI 配置成为可能。[0fb0306a89ad](https://cgit.freebsd.org/src/commit/?id=0fb0306a89ad)

已修复 `graid` 实现中的一个问题，该问题在使用 4 个及更多磁盘创建 Promise RAID1 时出现。该阵列仅在重启前正常工作。[394ceefc2f2f](https://cgit.freebsd.org/src/commit/?id=394ceefc2f2f)

[Intel 无线接口的 iwlwifi(4) 驱动](https://man.freebsd.org/cgi/man.cgi?query=iwlwifi&sektion=4&format=html) 已更新，支持 BE200 及更高版本的芯片组。（由 FreeBSD 基金会赞助）（由 minipci.biz 赞助）

[Realtek 无线 PCI 接口的 rtw88(4) 驱动](https://man.freebsd.org/cgi/man.cgi?query=rtw88&sektion=4&format=html) 已更新。

对原生和基于 LinuxKPI 的无线驱动程序进行了诸多稳定性修复。（由 FreeBSD 基金会赞助）

USB 以太网适配器驱动 [smsc(4)](https://man.freebsd.org/cgi/man.cgi?query=smsc&sektion=4&format=html) 现在将在树莓派设备中从 `bootargs` 获取 MAC 地址，如果没有提供，则回退到使用 [ether_gen_addr(9)](https://man.freebsd.org/cgi/man.cgi?query=ether_gen_addr&sektion=9&format=html) 生成固定的 MAC 地址。[3d96ee7c7dcc](https://cgit.freebsd.org/src/commit/?id=3d96ee7c7dcc)

## 存储

本节涉及文件系统和其他存储子系统的变更与新增，包括本地存储和网络存储。

### 一般存储

在调试和解决通用文件系统代码中与 vnode 回收相关的问题过程中，vnode 相关统计信息的 `sysctl` 已被分组到 `vfs.vnode` 下，以提高可见性。[77a8bd148796](https://cgit.freebsd.org/src/commit/?id=77a8bd148796)

### NFS 变更

NFS 服务器（[nfsd(8)](https://man.freebsd.org/cgi/man.cgi?query=nfsd&sektion=8&format=html)、[nfsuserd(8)](https://man.freebsd.org/cgi/man.cgi?query=nfsuserd&sektion=8&format=html)、[mountd(8)](https://man.freebsd.org/cgi/man.cgi?query=mountd&sektion=8&format=html)、[gssd(8)](https://man.freebsd.org/cgi/man.cgi?query=gssd&sektion=8&format=html)、和 [rpc.tlsservd(8)](https://man.freebsd.org/cgi/man.cgi?query=rpc.tlsservd&sektion=8&format=html)) 现在可以在适当配置的 vnet jail 中运行。vnet jail 必须位于独立的文件系统上，设置了 jail 参数 `allow.nfsd`，并且 `enforce_statfs` 不能设置为 `0`。不允许使用 UDP 和 pNFS 服务器配置。请参见 [jail(8)](https://man.freebsd.org/cgi/man.cgi?query=jail&sektion=8&format=html)、[nfsd(8)](https://man.freebsd.org/cgi/man.cgi?query=nfsd&sektion=8&format=html) 和 [mountd(8)](https://man.freebsd.org/cgi/man.cgi?query=mountd&sektion=8&format=html)。[b4805d577787](https://cgit.freebsd.org/src/commit/?id=b4805d577787)

现在有了一个新的挂载参数 `syskrb5`。能在没有 Kerberos 凭据（TGT 或 keytab）的情况下进行 Kerberized NFSv4.1/4.2 挂载。请参见 [mount_nfs(8)](https://man.freebsd.org/cgi/man.cgi?query=mount_nfs&sektion=8&format=html)。[0644746d5091](https://cgit.freebsd.org/src/commit/?id=0644746d5091)

### ZFS 变更

`OpenZFS` 已升级到 2.1.14 版本。[7005cd440405](https://cgit.freebsd.org/src/commit/?id=7005cd440405) [e6c1e181ba7f](https://cgit.freebsd.org/src/commit/?id=e6c1e181ba7f) [d9a61490b098](https://cgit.freebsd.org/src/commit/?id=d9a61490b098) [f5eac6541278](https://cgit.freebsd.org/src/commit/?id=f5eac6541278)

守护进程 [zfsd(8)](https://man.freebsd.org/cgi/man.cgi?query=zfsd&sektion=8&format=html) 现在将故障掉生成过多 I/O 延迟事件的磁盘。[e2ce586899ff](https://cgit.freebsd.org/src/commit/?id=e2ce586899ff)（由 Axcient 赞助）


## 网络

本节简述了影响 FreeBSD 网络的变更。

### 普通网络

现在可以使用 sysctl `kern.ipc.sooverprio` 设置因套接字监听队列溢出而导致的 syslog 消息的日志优先级。默认值为 `7`，表示 `LOG_DEBUG`。值为 `-1` 时将抑制日志记录。请参见 [listen(2)](https://man.freebsd.org/cgi/man.cgi?query=listen&sektion=2&format=html)。[773c91ccc892](https://cgit.freebsd.org/src/commit/?id=773c91ccc892)

netgraph 的 [ng_ipfw(4)](https://man.freebsd.org/cgi/man.cgi?query=ng_ipfw&sektion=4&format=html) 模块不再将 cookie 截断为 16 位，现在可使用完整的 32 位。[0b9242dea68c](https://cgit.freebsd.org/src/commit/?id=0b9242dea68c)

在默认情况下，现在禁用了对 IPv6 RFC 4620 nodeinfo 的支持。[5c4e8a631097](https://cgit.freebsd.org/src/commit/?id=5c4e8a631097)（由 FreeBSD 基金会赞助）

可以选择启用 pf 过滤规则，以便本地交付的包启用 pf rdr 规则，用于从主机发起的连接。这可能会改变匹配本地交付到 `lo0` 的包的规则行为。要启用此功能，请使用命令 `sysctl net.pf.filter_local=1; service pf restart`。启用时，最好确保本地交付的包不被过滤，例如通过添加 `set skip on lo` 规则。[6dfb2c2dce0f](https://cgit.freebsd.org/src/commit/?id=6dfb2c2dce0f)

## 硬件支持

本节涉及物理机器、虚拟化环境和超管理程序的通用硬件支持，以及不适合其他部分的硬件变更和更新。

### 硬件架构支持

BeagleBone Black（armv7）不再受支持；它与当前的启动文件（DTB）不兼容。

### 虚拟化支持

现在可支持谷歌虚拟网卡（[gve(4)](https://man.freebsd.org/cgi/man.cgi?query=gve&sektion=4&format=html)）。[4e846759f0a3](https://cgit.freebsd.org/src/commit/?id=4e846759f0a3)（由谷歌赞助）


## 关于后续 FreeBSD 版本的一般说明

预计 FreeBSD 15.0 不会再支持除 armv7 以外的 32 位平台。armv6、i386 和 powerpc 平台已弃用，并会在以后移除。64 位系统仍然能够运行较旧的 32 位二进制文件。

我们预计在 FreeBSD 15.0 和 stable/15 版本中，armv7 将作为二级架构继续得到支持。然而，我们也预见到 armv7 可能会在 FreeBSD 16.0 中被移除。我们将在 15.0 版本发布时，提供有关 armv7 在 15.x 和 16.x 中状态的更新。

通过参数 `COMPAT_FREEBSD32` 在 64 位平台上执行 32 位二进制文件的支持将至少在 stable/15 和 stable/16 分支中持续。通过 `cc -m32` 编译单个 32 位应用程序的支持也将至少在 stable/15 分支中继续，该分支包括适当的头文件（`/usr/include`）和库文件（`/usr/lib32`）。

对于 FreeBSD 15.0 及后续版本，Ports 将不再支持已弃用的 32 位平台。这些后续版本将不包含二进制包，也不再支持为已弃用的 32 位平台从 port 构建包。

FreeBSD stable/14 及以前的分支将继续保留对现有的 32 位内核和世界环境的支持。只要这些分支得到 Ports 系统的支持，Ports 将继续支持为 32 位系统构建 port 和包。然而，所有 32 位平台将被视为二级/三级平台，随着上游对 32 位平台的弃用，单个 Port 的支持可能会逐渐下降。

根据当前的支持计划，stable/14 将在 FreeBSD 14.0-RELEASE 发布后的 5 年内达到生命周期结束（EOL）。stable/14 的 EOL 将参数着对已弃用 32 位平台的支持结束，包括源代码发布、预构建包以及从 port 构建应用程序的支持。随着 14.0-RELEASE 于 2023 年 11 月发布，对已弃用 32 位平台的支持将在 2028 年 11 月结束。

该项目可能会选择在 FreeBSD 15.0 发布时调整此策略，通过在 15.0 及更高版本中对一个或多个已弃用平台提供某种级别的支持。任何调整都将根据社区反馈和为支持这些平台而作出的努力来决定。建议使用 FreeBSD 14.0-RELEASE 及其后续的次要版本，或 stable/14 分支，来迁移出 32 位平台。

---

**最后修改时间**：2024 年 3 月 4 日，作者 [Mike Karels](https://cgit.freebsd.org/doc/commit/?id=3f7e829604)

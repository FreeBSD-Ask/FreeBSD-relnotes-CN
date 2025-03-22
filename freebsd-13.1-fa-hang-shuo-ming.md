# FreeBSD 13.1-RELEASE 发行说明（2022 年 5 月 16 日）

- 原文链接 [FreeBSD 13.1-RELEASE Release Notes](https://www.freebsd.org/releases/13.1R/relnotes/)

## 摘要

FreeBSD 13.1-RELEASE 的发行说明总结了在 13-STABLE 开发分支中对 FreeBSD 基本系统所作的变更。本文件列出了自上次发行以来发布的适用安全公告，以及对 FreeBSD 内核和用户空间的重大变更。此外，还简要介绍了升级相关的注意事项。

## 引言

本文件包含 FreeBSD 13.1-RELEASE 的发行说明，介绍了最近添加、变更或删除的功能，同时提供了从 FreeBSD 早期版本升级的相关说明。

本发行说明适用于 FreeBSD 13-STABLE 开发分支中自创建以来的最新节点。有关此分支上预构建的二进制发行版的信息，请访问 [https://www.FreeBSD.org/releases/](https://www.freebsd.org/releases/)。

本发行说明所涉的发行版，位于 13-STABLE 开发分支中 13.0-RELEASE 和未来 13.2-RELEASE 之间的某一节点。有关此分支上预构建的二进制发行版的信息，请访问 [https://www.FreeBSD.org/releases/](https://www.freebsd.org/releases/)。

FreeBSD 13.1-RELEASE 是个 RELEASE 发行版，可以从 [https://www.FreeBSD.org/releases/](https://www.freebsd.org/releases/) 或其任一镜像站下载。关于获取此版本（或其他版本）发行版的更多信息，请参阅 [FreeBSD 手册](https://docs.freebsd.org/en/books/handbook//mirrors) 中的 [获取 FreeBSD 附录](https://docs.freebsd.org/en/books/handbook//mirrors)。

建议所有用户在安装 FreeBSD 之前，查阅发行版的勘误表。勘误表包含在发行周期后期或发行后发现的“最新信息”，通常包括已知错误、安全公告以及文档修订的相关内容。可在 FreeBSD 网站上找到 FreeBSD 13.1-RELEASE 的最新勘误表副本。

本文件介绍了自 13.0-RELEASE 以来，FreeBSD 中对用户最显著的新功能或变更。一般而言，本文中提到的变更是 13-STABLE 分支所独有的，除非明确标记为已合并功能。

发行说明通常记录自 13.0-RELEASE 以来发布的安全公告、新驱动程序或硬件支持、新命令或选项、重大错误修复或第三方软件升级。此外，还可能列出主要的 Port/软件包变更或发行工程实践的更新。显然，发行说明无法列出两个版本之间 FreeBSD 的每一处变更；本文件主要关注安全公告、用户可见的变更以及主要的架构改进。

## 从旧版 FreeBSD 升级

通过 [freebsd-update(8)](https://man.freebsd.org/cgi/man.cgi?query=freebsd-update&sektion=8&format=html) 工具，可以在不同 RELEASE 版本之间（包括各安全分支的快照版本）进行二进制升级。该工具将更新未修改的用户空间工具，以及官方 FreeBSD 发行版中包含的未修改的 GENERIC 内核。使用 [freebsd-update(8)](https://man.freebsd.org/cgi/man.cgi?query=freebsd-update&sektion=8&format=html) 工具要求待升级的主机具备互联网连接。

基于源代码的升级（通过重新编译 FreeBSD 基本系统的源代码进行升级）也受到支持，具体请按照 `/usr/src/UPDATING` 中的说明操作。

对于所有 powerpc 架构的用户，在成功安装内核和世界后，需要手动运行 `kldxref /boot/kernel`。

> 在尝试升级 FreeBSD 之前，务必备份 **所有** 数据和配置文件。

>升级后，sshd（来自 OpenSSH 8.8p1）在重新启动之前不会接受新的连接。在安装新用户空间后，要么按照源代码升级程序的要求重启系统，要么执行 `service sshd restart` 来重启 `sshd` 服务。

## 用户空间

本节涉及对用户空间应用程序、第三方软件以及系统实用工具的变更和新增内容。

### 用户空间配置变更

参数 `-i` 现在默认添加了到 `/etc/defaults/rc.conf` 中的 [rtsol(8)](https://man.freebsd.org/cgi/man.cgi?query=rtsol&sektion=8&format=html) 和 [rtsold(8)](https://man.freebsd.org/cgi/man.cgi?query=rtsold&sektion=8&format=html)。变更详情见 [a0fc5094bf4c](https://cgit.freebsd.org/src/commit/?id=a0fc5094bf4c)（由 [https://www.patreon.com/cperciva](https://www.patreon.com/cperciva) 赞助）。

### 用户空间应用程序变更

在 [rtsol(8)](https://man.freebsd.org/cgi/man.cgi?query=rtsol&sektion=8&format=html) 和 [rtsold(8)](https://man.freebsd.org/cgi/man.cgi?query=rtsold&sektion=8&format=html) 中添加了 `-i` 选项，用于禁用 0 到 1 秒的随机延迟，从而加快启动过程。[8056b73ea163](https://cgit.freebsd.org/src/commit/?id=8056b73ea163)（由 [https://www.patreon.com/cperciva](https://www.patreon.com/cperciva) 赞助）

对于 64 位架构，基本系统现在默认启用位置无关可执行文件（PIE）支持。可以通过开关 `WITHOUT_PIE` 禁用该功能，需要进行完全重新编译。[396e9f259d96](https://cgit.freebsd.org/src/commit/?id=396e9f259d96)

新增了 `zfskeys` [rc(8)](https://man.freebsd.org/cgi/man.cgi?query=rc&sektion=8&format=html) 服务脚本，允许在启动过程中自动解密使用 ZFS 原生加密的 ZFS 数据集。更多信息请参考 [rc.conf(5)](https://man.freebsd.org/cgi/man.cgi?query=rc.conf&sektion=5&format=html) 手册。[33ff39796ffe](https://cgit.freebsd.org/src/commit/?id=33ff39796ffe)、[8719e8a951b7](https://cgit.freebsd.org/src/commit/?id=8719e8a951b7)（由 Modirum 和 Klara Inc. 赞助）

[bhyve(8)](https://man.freebsd.org/cgi/man.cgi?query=bhyve&sektion=8&format=html) 的 NVMe 仿真已升级至 NVMe 规范的 1.4 版本。[b7a2cf0d9102](https://cgit.freebsd.org/src/commit/?id=b7a2cf0d9102) [eae02d959363](https://cgit.freebsd.org/src/commit/?id=eae02d959363)

修复了 [bhyve(8)](https://man.freebsd.org/cgi/man.cgi?query=bhyve&sektion=8&format=html) 中构建大 IO 的 NVMe iovec 的问题，该问题由 Rocky Linux 8.4 附带的 UEFI 驱动暴露出来。[a7761d19dacd](https://cgit.freebsd.org/src/commit/?id=a7761d19dacd)

为巴西葡萄牙语 ABNT2 键盘添加了额外的 Alt Gr 映射。[310623908c20](https://cgit.freebsd.org/src/commit/?id=310623908c20)

`chroot` 现在支持非特权操作，[chroot(8)](https://man.freebsd.org/cgi/man.cgi?query=chroot&sektion=8&format=html) 程序增加了 `-n` 选项以启用该功能。[460b4b550dc9](https://cgit.freebsd.org/src/commit/?id=460b4b550dc9)（由 EPSRC 赞助）

修改了 CAM 库以在解析设备名称之前使用 [realpath(3)](https://man.freebsd.org/cgi/man.cgi?query=realpath&sektion=3&format=html)，从而允许诸如 [camcontrol(8)](https://man.freebsd.org/cgi/man.cgi?query=camcontrol&sektion=8&format=html) 和 [smartctl(8)](https://man.freebsd.org/cgi/man.cgi?query=smartctl&sektion=8&format=html) 之类的工具在使用符号链接时更加友好。[e32acf95ea25](https://cgit.freebsd.org/src/commit/?id=e32acf95ea25)

通过在程序名称以 `sum` 结尾时让相应的 BSD 程序运行 `-r` 选项，添加了兼容 Linux 的 [md5sum(1)](https://man.freebsd.org/cgi/man.cgi?query=md5sum&sektion=1&format=html) 和类似的消息摘要程序。[c0d5665be0dc](https://cgit.freebsd.org/src/commit/?id=c0d5665be0dc)（由奈飞赞助）

[svnlite(1)](https://man.freebsd.org/cgi/man.cgi?query=svnlite&sektion=1&format=html) 默认在构建中禁用。[a4f99b3c2384](https://cgit.freebsd.org/src/commit/?id=a4f99b3c2384)

[mpsutil(8)](https://man.freebsd.org/cgi/man.cgi?query=mpsutil&sektion=8&format=html) 扩展以显示适配器信息并控制 NCQ。[395bc3598b47](https://cgit.freebsd.org/src/commit/?id=395bc3598b47)

修复了使用 [camcontrol(8)](https://man.freebsd.org/cgi/man.cgi?query=camcontrol&sektion=8&format=html) 下载固件后设备出现的问题，方法是在下载固件后强制重新扫描 LUN。[327da43602cc](https://cgit.freebsd.org/src/commit/?id=327da43602cc)（由奈飞赞助）

### 第三方软件

在所有 PowerPC 架构上已启用 LLDB 的构建支持。[cb1bee9bd34](https://cgit.freebsd.org/src/commit/?id=cb1bee9bd34)

- One True Awk 已更新为上游的最新版本（20210215）。除了一个补丁外，FreeBSD 的所有补丁已被上游接纳或移除。主要变更包括：
  - 范围不再使用区域设置。
  - 修复了各种错误。
  - 提高了与 `gawk` 和 `mawk` 的兼容性。
  剩下的一个 FreeBSD 修改可能会在 FreeBSD 14 中移除，目前依然允许将以 `0x` 为前缀的十六进制数解析并解释为十六进制数，而其他 awk 实现（现在包括 One True Awk）将其解释为 `0`，符合 awk 的历史行为。

- `zlib` 升级到版本 1.2.12。

- `libarchive` 升级到版本 3.6.0，并包含即将发布的修补程序版本中的额外错误和安全修复。发布说明可在 [https://github.com/libarchive/libarchive/releases](https://github.com/libarchive/libarchive/releases) 查看。

- `ssh` 包已更新为 OpenSSH v8.8p1，包含安全更新和错误修复。其他更新包括以下变更：
  - [ssh(1)](https://man.freebsd.org/cgi/man.cgi?query=ssh&sektion=1&format=html)：在提示是否记录新主机密钥时，接受该密钥的指纹作为“yes”的同义词。
  - [ssh-keygen(1)](https://man.freebsd.org/cgi/man.cgi?query=ssh-keygen&sektion=1&format=html)：作为 CA 并使用 RSA 密钥签署证书时，默认使用 `rsa-sha2-512` 签名算法。
  - [ssh(1)](https://man.freebsd.org/cgi/man.cgi?query=ssh&sektion=1&format=html)：默认启用 `UpdateHostkeys`，但受到一些保守条件的限制。
  - [scp(1)](https://man.freebsd.org/cgi/man.cgi?query=scp&sektion=1&format=html)：远程到远程复制（如 `scp host-a:/path host-b:`）的行为已变更，默认通过本地主机传输。
  - [scp(1)](https://man.freebsd.org/cgi/man.cgi?query=scp&sektion=1&format=html)：实验性支持使用 SFTP 协议进行传输，以替代传统的 SCP/RCP 协议。

在 `ssh` 中启用了对 FIDO/U2F 硬件认证器的支持，新增了 `ecdsa-sk` 和 `ed25519-sk` 公钥类型以及相应的证书类型。有关 FIDO/U2F 支持的描述请参考 [https://www.openssh.com/txt/release-8.2](https://www.openssh.com/txt/release-8.2)。[a613d68fff9a](https://cgit.freebsd.org/src/commit/?id=a613d68fff9a)（由 FreeBSD 基金会赞助）

[bsdinstall(8)](https://man.freebsd.org/cgi/man.cgi?query=bsdinstall&sektion=8&format=html) 的脚本分区编辑器新增了一种新模式，用于支持变体磁盘名称。如果 `DEFAULT` 被设置为磁盘参数，或者在 `PARTITIONS` 参数中未指定设备名称，安装程序将遵循自动分区模式的逻辑。如果存在多个磁盘，将提供选择对话框；如果只有一个磁盘，则会自动选择。这简化了为硬件或虚拟机创建全自动安装介质的过程。[5ec4eb443e81](https://cgit.freebsd.org/src/commit/?id=5ec4eb443e81)

### 运行时库与 API

为 powerpc、powerpc64 和 powerpc64le 添加了 OpenSSL 的汇编优化代码。[ce35a3bc852](https://cgit.freebsd.org/src/commit/?id=ce35a3bc852)

修复了对 ARMv7 和 ARM64 加速加密操作的 CPU 特性检测，大幅提升了 `aes-256-gcm` 和 `sha256` 的性能。[32a2fed6e71f](https://cgit.freebsd.org/src/commit/?id=32a2fed6e71f)（由 Ampere Computing LLC 和 Klara Inc. 赞助）

启用了 riscv64 和 riscv64sf 平台上的 ASAN 和 UBSAN 库的构建支持。[8c56b338da7](https://cgit.freebsd.org/src/commit/?id=8c56b338da7)

在 riscv64 和 riscv64sf 平台上构建了 OFED 库。[2b978245733](https://cgit.freebsd.org/src/commit/?id=2b978245733)

在 riscv64 和 riscv64sf 平台上构建了 OPENMP 库。[aaf56e35569](https://cgit.freebsd.org/src/commit/?id=aaf56e35569)



## 内核

本部分涉及内核配置、系统调优以及未分类的系统控制参数的变更。

### 通用内核变更

修复了 powerpc64 平台上串行控制台的输出损坏问题。[dca829138ca](https://cgit.freebsd.org/src/commit/?id=dca829138ca)

CAS 已变更为支持 Radix MMU。[cc8e726c85b](https://cgit.freebsd.org/src/commit/?id=cc8e726c85b)

修复了在 QEMU 的 TCG 模式下运行启用了 HPT 超页的 FreeBSD 于 powerpc64(le) 平台的问题。[f05174ed354](https://cgit.freebsd.org/src/commit/?id=f05174ed354)

在 powerpc64(le) 平台上的 `pmap_mincore` 添加了对超页的支持。[32b50b8520d](https://cgit.freebsd.org/src/commit/?id=32b50b8520d)

在 arm64 平台上为 32 位 ARM 二进制文件添加了 HWCAP/HWCAP2 辅助参数支持。这修复了在 `COMPAT32` 仿真下构建/运行 Golang 的问题。[28e22482279f](https://cgit.freebsd.org/src/commit/?id=28e22482279f)（由 Rubicon Communications, LLC ("Netgate") 赞助）

## 设备与驱动

本部分介绍了自 13.0-RELEASE 以来，设备和设备驱动的变更和新增内容。

### 设备驱动

引入了 [igc(4)](https://man.freebsd.org/cgi/man.cgi?query=igc&sektion=4&format=html) 驱动程序，用于支持 Intel I225 以太网控制器。该控制器支持 2.5G/1G/100Mb/10Mb 速度，并支持 tx/rx 校验和卸载、TSO、LRO 和多队列操作。[d7388d33b4dd](https://cgit.freebsd.org/src/commit/?id=d7388d33b4dd)（由 Rubicon Communications, LLC ("Netgate") 赞助）

修复了 powerpc64(le) 平台在启动过程中使用 AST2500 时，VGA/HDMI 控制台的问题。[c41d129485e](https://cgit.freebsd.org/src/commit/?id=c41d129485e)

修复了 [virtio(4)](https://man.freebsd.org/cgi/man.cgi?query=virtio&sektion=4&format=html) 驱动中大端目标设备的 PCI 通用读写功能。[7e583075a41](https://cgit.freebsd.org/src/commit/?id=7e583075a41), [8d589845881](https://cgit.freebsd.org/src/commit/?id=8d589845881)

为驱动 [mpr(4)](https://man.freebsd.org/cgi/man.cgi?query=mpr&sektion=4&format=html) 添加了大端支持。[7d45bf699dc](https://cgit.freebsd.org/src/commit/?id=7d45bf699dc), [2954aedb8e5](https://cgit.freebsd.org/src/commit/?id=2954aedb8e5), [c80a1c1072d](https://cgit.freebsd.org/src/commit/?id=c80a1c1072d)

降低了驱动 [aacraid(4)](https://man.freebsd.org/cgi/man.cgi?query=aacraid&sektion=4&format=html) 的最大 I/O 大小以避免 DMA 问题。[572e3575dba](https://cgit.freebsd.org/src/commit/?id=572e3575dba)

修复了驱动 [virtio_random(8)](https://man.freebsd.org/cgi/man.cgi?query=virtio_random&sektion=8&format=html) 阻止虚拟机客户机关机或重启的问题。[fa67c45842bb](https://cgit.freebsd.org/src/commit/?id=fa67c45842bb)

更新了驱动 [ice(4)](https://man.freebsd.org/cgi/man.cgi?query=ice&sektion=4&format=html) 至 1.34.2-k，增加了固件日志记录功能和初步的 DCB 支持。[a0cdf45ea1d1](https://cgit.freebsd.org/src/commit/?id=a0cdf45ea1d1)（由英特尔公司赞助）

添加了网络接口驱动程序 [mgb(4)](https://man.freebsd.org/cgi/man.cgi?query=mgb&sektion=4&format=html) ，支持 Microchip 的 LAN7430 PCIe 千兆以太网控制器（带 PHY）和 LAN7431 PCIe 千兆以太网控制器（带 RGMII 接口）。尽管该驱动仍存在一些限制，但功能已可用。[e0262ffbc6ae](https://cgit.freebsd.org/src/commit/?id=e0262ffbc6ae)（由 FreeBSD 基金会赞助）

为 [cdce(4)](https://man.freebsd.org/cgi/man.cgi?query=cdce&sektion=4&format=html) 设备添加了链路状态、媒体类型和 VLAN MTU 的支持。[973fb85188ea](https://cgit.freebsd.org/src/commit/?id=973fb85188ea)

添加了 [iwlwifi(4)](https://man.freebsd.org/cgi/man.cgi?query=iwlwifi&sektion=4&format=html) 驱动和一个 LinuxKPI 802.11 兼容层，用于支持较新的 Intel 无线芯片组，以补充 [iwm(4)](https://man.freebsd.org/cgi/man.cgi?query=iwm&sektion=4&format=html) 驱动。（由 FreeBSD 基金会赞助）

当内核使用选项 `MMCCAM` 配置时，现在可以使用 `dwmmc` 控制器将内核崩溃转储保存到 SD 卡和 eMMC 模块。[79c3478e76c3](https://cgit.freebsd.org/src/commit/?id=79c3478e76c3)

当内核使用选项 `MMCCAM` 配置时，现在可以使用 `sdhci` 控制器将内核崩溃转储保存到 SD 卡。[8934d3e7b9b9](https://cgit.freebsd.org/src/commit/?id=8934d3e7b9b9)

### 支持的平台

新增对 HiFive Unmatched RISC-V 开发板的支持。

## 存储

本部分涉及文件系统及其他存储子系统（包括本地和网络存储）的变更与新增内容。

### 通用存储

暂无具体变更说明。

### ZFS 变更

ZFS 已升级至 OpenZFS 2.1.4 版本。OpenZFS 的发行说明可参阅 [https://github.com/openzfs/zfs/releases](https://github.com/openzfs/zfs/releases)。

### NFS 变更

- 默认在 **amd64** 和 **arm64** 架构上构建了两个新的守护程序 [rpc.tlsclntd(8)](https://man.freebsd.org/cgi/man.cgi?query=rpc.tlsclntd&sektion=8&format=html) 和 [rpc.tlsservd(8)](https://man.freebsd.org/cgi/man.cgi?query=rpc.tlsservd&sektion=8&format=html)。它们提供了对基于 TLS 的 NFS 加密支持，该功能描述于《Towards Remote Procedure Call Encryption By Default》草案中。这些守护程序在指定 `WITH_OPENSSL_KTLS` 时构建，使用 KTLS 加密/解密所有 NFS RPC 消息流量，并可选择通过 X.509 证书验证设备身份。[2c76eebca71b](https://cgit.freebsd.org/src/commit/?id=2c76eebca71b) [59f6f5e23c1a](https://cgit.freebsd.org/src/commit/?id=59f6f5e23c1a)

- 默认的 NFSv4 挂载次版本号已变更为 NFSv4 服务器所支持的最高次版本号。用户可通过挂载选项 `minorversion` 手动覆盖此默认值。[8a04edfdcbd2](https://cgit.freebsd.org/src/commit/?id=8a04edfdcbd2)

- 新增了 NFSv4.1/4.2 的挂载选项 `nconnect`，用于指定挂载所使用的 TCP 连接数量（最多 16 个）。默认的第一个 TCP 连接将用于所有小型 RPC 消息，而可能包含大型 RPC 消息的操作（如 Read、Readdir、ReaddirPlus、Write）将在额外的 TCP 连接上以轮询方式发送。如果 NFS 客户端或服务器具有多个聚合的网络接口或支持多队列的网络接口，则此功能可以提高 NFS 的性能。[9ec7dbf46b0a](https://cgit.freebsd.org/src/commit/?id=9ec7dbf46b0a)

- 添加了 sysctl 配置项 `vfs.nfsd.srvmaxio`，用于将 NFS 服务器的最大 I/O 大小从 128KB 增加到任意 2 的幂值（最高 1MB）。该选项只能在 nfsd 线程未运行时设置，且通常需要将 `kern.ipc.maxsockbuf` 增加至控制台日志中建议的值。[9fb6e613373c](https://cgit.freebsd.org/src/commit/?id=9fb6e613373c)

### UFS 变更

修复了 [fsck_ffs(8)](https://man.freebsd.org/cgi/man.cgi?query=fsck_ffs&sektion=8&format=html) 工具在预检模式下处理启用软更新（但未启用软更新日志）的 UFS 时无法正常运行的问题。[fb2feceac34c](https://cgit.freebsd.org/src/commit/?id=fb2feceac34c)

## 引导加载程序的变更

本部分涉及引导加载程序、引导菜单和其他引导相关的变更内容。

### 引导加载程序的变更

- **UEFI 引导改进（amd64）**：  
  针对 amd64 架构改进了 UEFI 引导。加载器会检测所加载的内核是否支持原位暂存区（非复制模式）。默认设置为 `copy_staging auto`。用户可以通过手动覆盖自动检测，例如：设置 `copy_staging enable` 时，加载器会无条件将暂存区复制到 2M 地址，无论内核是否支持。此外，扩展暂存区的代码更为稳健，用户无需手动调整和重新编译加载器即可完成扩展。（由 [FreeBSD 基金会](https://www.freebsdfoundation.org/) 赞助）

- **修复 `boot1` 和 `loader` 在 powerpc64le 架构上的问题**：[8a62b07bce7](https://cgit.freebsd.org/src/commit/?id=8a62b07bce7)

### 其他引导变更

- **性能改进**：对 [loader(8)](https://man.freebsd.org/cgi/man.cgi?query=loader&sektion=8&format=html)、[nvme(4)](https://man.freebsd.org/cgi/man.cgi?query=nvme&sektion=4&format=html)、[random(4)](https://man.freebsd.org/cgi/man.cgi?query=random&sektion=4&format=html)、[rtsold(8)](https://man.freebsd.org/cgi/man.cgi?query=rtsold&sektion=8&format=html) 和 x86 时钟校准的性能进行了优化，这显著缩短了系统引导时间。此外，EC2 平台的配置变更进一步提高了性能，使得 13.1-RELEASE 的引导速度比 13.0-RELEASE 快了两倍以上。（由 [https://www.patreon.com/cperciva](https://www.patreon.com/cperciva) 赞助）

- **EC2 镜像默认使用 UEFI 引导**：  
  EC2 镜像现在默认使用 UEFI 引导而非传统的 BIOS 引导。不过，基于 Xen 的 EC2 实例或 `bare metal` EC2 实例仍不支持 UEFI。[65f22ccf8247](https://cgit.freebsd.org/src/commit/?id=65f22ccf8247)（由 [https://www.patreon.com/cperciva](https://www.patreon.com/cperciva) 赞助）

- **支持在 AWS Systems Manager 参数存储中记录 EC2 AMI ID**：  
  FreeBSD 在 AWS Systems Manager 参数存储中使用公共前缀 `/aws/service/freebsd`，生成类似 `/aws/service/freebsd/amd64/base/ufs/13.1/RELEASE` 的参数名称。[242d1c32e42c](https://cgit.freebsd.org/src/commit/?id=242d1c32e42c)（由 [https://www.patreon.com/cperciva](https://www.patreon.com/cperciva) 赞助）

## 网络

本部分介绍了 FreeBSD 中影响网络功能的变更。

### 通用网络

- **IPv4 子网最低地址的处理变更**：  
  IPv4（子）网的最低地址（主机 0）的处理方式发生了变化，只有在该地址被设置为广播地址时，才会将数据包作为广播发送。这一变更使最低地址可用于主机。如果需要恢复旧行为，可以通过 sysctl 选项 `net.inet.ip.broadcast_lowest` 完成。背景信息参见 [https://datatracker.ietf.org/doc/draft-schoen-intarea-unicast-lowest-address/](https://datatracker.ietf.org/doc/draft-schoen-intarea-unicast-lowest-address/)。[3ee882bf21af](https://cgit.freebsd.org/src/commit/?id=3ee882bf21af)

## 关于后续  FreeBSD 版本的说明

暂无具体变更内容。

### 默认 `CPUTYPE` 变更

从 FreeBSD-13.0 开始，i386 架构的默认 `CPUTYPE` 将从 `486` 变更为 `686`。

这意味着默认生成的二进制文件将需要支持 686 级别的 CPU，包括但不限于由 FreeBSD 发布工程团队提供的二进制文件。尽管 FreeBSD 13.0 仍将支持较旧的 CPU，但需要此功能的用户需自行构建其专属版本以获得官方支持。

由于 i486 和 i586 CPU 的主要应用通常在嵌入式市场，普通终端用户受此变更的影响预计会非常有限。新硬件中这些类型的 CPU 早已不常见，而大部分现有系统的硬件也接近使用寿命的尾声。

作出这一变更考虑了多个因素。例如，i486 不支持 64 位原子操作（atomics），虽然内核可以模拟这些操作，但在用户态（userland）中无法实现。此外，32 位 amd64 库自开始以来便已采用 i686。

大多数 32 位测试由开发者通过在 64 位硬件上使用内核中的选项 `COMPAT_FREEBSD32` 和 lib32 库完成。此变更可提供更好的覆盖范围和用户体验，同时符合大多数 Linux® 发行版的长期做法。

这预计将是 i386 架构中默认 `CPUTYPE` 的最后一次升级。

>此变更不影响 FreeBSD 12.x 系列版本。

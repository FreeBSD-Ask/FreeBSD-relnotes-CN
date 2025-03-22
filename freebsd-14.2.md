# FreeBSD 14.2-RELEASE 发行说明（2024 年 12 月 3 日）

- 原文地址：[FreeBSD 14.2-RELEASE Release Notes](https://www.freebsd.org/releases/14.2R/relnotes/)
- 最后修改：[Dave Cottlehuber](https://cgit.freebsd.org/doc/commit/?id=f232709d21) 于 2024 年 12 月 4 日

## 概述

FreeBSD 14.2-RELEASE 发行说明总结了在 14-STABLE 开发分支上 FreeBSD 基本系统发生的变更。本文档列出了自上次发布以来 RELEASE 适用的安全公告，以及对 FreeBSD 内核和用户空间的重大变更。同时还附带了有关更新的简要说明。

## 引言

本文档为 FreeBSD 14.2-RELEASE 的发行说明，概述了 FreeBSD 最近新增、修改和删除的功能，并附带了有关从旧版本更新的说明。

本发行说明适用于自 14-STABLE 开发分支创建以来的最新版本信息。有关该分支中预编译的二进制“RELEASE”发行版的信息，请参见 [https://www.FreeBSD.org/releases/](https://www.freebsd.org/releases/)。

FreeBSD 14.2-RELEASE 是个“RELEASE”发行版。可以通过 [https://www.FreeBSD.org/releases/](https://www.freebsd.org/releases/) 和其有关镜像下载。有关获取此版本（及其他版本）FreeBSD 的更多信息，请参阅 [FreeBSD Handbook](https://docs.freebsd.org/en/books/handbook//) 的 [FreeBSD 附录](https://docs.freebsd.org/en/books/handbook//mirrors)。

建议在安装 FreeBSD 之前，用户先查阅下发行勘误文档。该文档包含在发行周期后期及发行后发现的“最新”信息，通常涉及已知错误、安全公告以及文档修正。可在 FreeBSD 网站上找到最新的 FreeBSD 14.2-RELEASE 勘误文档。

本文档总结了自 14.1-RELEASE 以来 FreeBSD 中对用户最为可见的新增和变更功能。一般来说，这些变更是 14-STABLE 分支的独有内容，除非特别标记为 MERGED 功能。

一般的发行说明内容包括自 14.1-RELEASE 之后发布的安全公告、新增的驱动程序/硬件支持、新命令/参数、主要的错误修复/外部软件更新。还可能列出主要 Ports/软件包和发行工程实践的变更。显然，发行说明无法详尽列出两个 FreeBSD 版本之间所做的每项变更；本文档主要聚焦于安全公告、用户可见的变更和重大架构改进。


### 从旧版 FreeBSD 更新

使用工具 **freebsd-update(8)** 能在 RELEASE 版本（及各安全分支快照）间进行二进制更新。请参阅特定版本的更新程序，例如 FreeBSD 14.2-RELEASE 的更新信息，并在 FreeBSD 手册中查阅关于二进制更新的详细说明。此工具会更新未经修改的用户空间工具，以及在官方 FreeBSD RELEASE 分发的未经修改的 GENERIC 内核。工具 **freebsd-update(8)** 要求更新的主机能够连接互联网。

可以按照 **/usr/src/UPDATING** 中的说明从以前的版本进行基于源代码的更新（通过重新编译 FreeBSD 基本系统进行更新）。

在更新 FreeBSD 之前，应先备份所有数据和配置文件。


### 安全与勘误

本节列出了自 14.1-RELEASE 以来发布的安全公告和勘误通知。

#### 安全公告

| 公告编号                    | 日期           | 主题                                                                 |
|:---:|:---:|:---|
| **FreeBSD-SA-24:04.openssh** | 2024 年 7 月 1 日  | OpenSSH 预认证远程代码执行                                           |
| **FreeBSD-SA-24:05.pf**      | 2024 年 8 月 7 日  | pf 在状态表中错误匹配不同的 ICMPv6 状态                             |
| **FreeBSD-SA-24:06.ktrace**  | 2024 年 8 月 7 日  | [ktrace(2)](https://man.freebsd.org/cgi/man.cgi?query=ktrace&sektion=2&format=html) 在执行 setuid 二进制文件时未正确分离                      |
| **FreeBSD-SA-24:07.nfsclient** | 2024 年 8 月 7 日  | NFS 客户端接受包含路径分隔符的文件名                                 |
| **FreeBSD-SA-24:08.openssh** | 2024 年 8 月 7 日  | OpenSSH 预认证异步信号安全问题                                      |
| **FreeBSD-SA-24:09.libnv**   | 2024 年 9 月 4 日  | libnv 中的多个漏洞                                                  |
| **FreeBSD-SA-24:10.bhyve**   | 2024 年 9 月 4 日  | [bhyve(8)](https://man.freebsd.org/cgi/man.cgi?query=bhyve&sektion=8&format=html) 通过 TPM 设备直通导致的特权用户逃逸                        |
| **FreeBSD-SA-24:11.ctl**     | 2024 年 9 月 4 日  | [ctl(4)](https://man.freebsd.org/cgi/man.cgi?query=ctl&sektion=4&format=html) CAM 目标层的多个问题                                         |
| **FreeBSD-SA-24:12.bhyve**   | 2024 年 9 月 4 日  | [bhyve(8)](https://man.freebsd.org/cgi/man.cgi?query=bhyve&sektion=8&format=html) 通过 USB 控制器直通导致的特权用户逃逸                      |
| **FreeBSD-SA-24:13.openssl** | 2024 年 9 月 4 日  | OpenSSL 中 X.509 名称检查可能导致的 DoS                             |
| **FreeBSD-SA-24:14.umtx**    | 2024 年 9 月 4 日  | umtx 内核崩溃或使用后释放                                           |
| **FreeBSD-SA-24:15.bhyve**   | 2024 年 9 月 19 日 | [bhyve(8)](https://man.freebsd.org/cgi/man.cgi?query=bhyve&sektion=8&format=html) XHCI 仿真中越界读取访问                                   |
| **FreeBSD-SA-24:16.libnv**   | 2024 年 9 月 19 日 | libnv 中的整数溢出                                                  |
| **FreeBSD-SA-24:17.bhyve**   | 2024 年 10 月 29 日 | bhyve 管理程序中的多个问题                                          |
| **FreeBSD-SA-24:18.ctl**     | 2024 年 10 月 29 日 | [ctl(4)](https://man.freebsd.org/cgi/man.cgi?query=ctl&sektion=4&format=html) CAM 目标层中的不受限制分配                                   |
| **FreeBSD-SA-24:19.fetch**   | 2024 年 10 月 29 日 | [fetch(1)](https://man.freebsd.org/cgi/man.cgi?query=fetch&sektion=1&format=html) 参数的证书吊销列表功能失效                                 |


#### 勘误通知

| 勘误编号                   | 日期           | 主题                                                                 |
|:---:|:---:|:---|
| **FreeBSD-EN-24:10.zfs**   | 2024 年 6 月 19 日 | ZFS 内核内存泄漏                                                   |
| **FreeBSD-EN-24:11.ldns**  | 2024 年 6 月 19 日 | LDNS 使用了 **resolv.conf** 中注释掉的 nameserver                   |
| **FreeBSD-EN-24:12.killpg** | 2024 年 6 月 19 日 | killpg 中的锁顺序反转（Lock order reversal，LOR）导致的活锁                                   |
| **FreeBSD-EN-24:13.libc++** | 2024 年 6 月 19 日 |传递给堆分配的 `std::string` 删除操作的大小不正确                         |
| **FreeBSD-EN-24:14.ifconfig** | 2024 年 8 月 7 日  | ifconfig 掩码分配错误                                               |
| **FreeBSD-EN-24:15.calendar** | 2024 年 9 月 4 日  | [cron(8)](https://man.freebsd.org/cgi/man.cgi?query=cron&sektion=8&format=html)/[periodic(8)](https://man.freebsd.org/cgi/man.cgi?query=periodic&sektion=8&format=html) 会话登录                                        |
| **FreeBSD-EN-24:16.pf**     | 2024 年 9 月 19 日 | pf 中的 ICMPv6 状态处理错误                                         |
| **FreeBSD-EN-24:17.pam_xdg** | 2024 年 10 月 29 日 | 登录时 XDG 运行目录的文件描述符泄漏                                 |


## 用户空间

本节介绍用户空间应用程序、第三方软件和系统工具的变更与新增内容。

### 用户空间应用程序的变更

[env(1)](https://man.freebsd.org/cgi/man.cgi?query=env&sektion=1&format=html) 增加了一个用于变更目录的参数。此功能类似于 GNU 版 `env` 的功能，但不支持长选项（**译者注：即 `--` 此类参数**）。[08e8554c4a39](https://cgit.freebsd.org/src/commit/?id=08e8554c4a39)（由 Klara, Inc. 赞助）



### 第三方应用程序

- `bc` 已更新至 7.0.2。[90ea553a0d30](https://cgit.freebsd.org/src/commit/?id=90ea553a0d30)  
- `libarchive` 已更新至 3.7.7。[2ae238160f20](https://cgit.freebsd.org/src/commit/?id=2ae238160f20)
- `libcbor` 已更新至 0.11.0。[1755b9daa693](https://cgit.freebsd.org/src/commit/?id=1755b9daa693)（由 FreeBSD 基金会赞助）
- `libcxxrt` 已更新至供应商快照 6f2fdfebcd62。[d0dcee46d971](https://cgit.freebsd.org/src/commit/?id=d0dcee46d971)
- `libfido2` 已更新至 1.14.0。[128bace5102e](https://cgit.freebsd.org/src/commit/?id=128bace5102e)（由 FreeBSD 基金会赞助）
- `libpcap` 已更新至 1.10.5。[26f21a6494b4](https://cgit.freebsd.org/src/commit/?id=26f21a6494b4)（由 FreeBSD 基金会赞助）
- `llvm` 已更新至 18.1.6。[f1e3279983d6](https://cgit.freebsd.org/src/commit/?id=f1e3279983d6)
- `openssl` 已更新至 3.0.15。[cc43f991ab3e](https://cgit.freebsd.org/src/commit/?id=cc43f991ab3e)
- `tcpdump` 已更新至 4.99.5。[ec3da16d8bc1](https://cgit.freebsd.org/src/commit/?id=ec3da16d8bc1)（由 FreeBSD 基金会赞助）  
- `unbound` 已更新至 1.22.0。[0a096a7b3ae8](https://cgit.freebsd.org/src/commit/?id=0a096a7b3ae8)  


### 已弃用应用程序

[gpart(8)](https://man.freebsd.org/cgi/man.cgi?query=gpart&sektion=8&format=html) 已经取代 [fdisk(8)](https://man.freebsd.org/cgi/man.cgi?query=fdisk&sektion=8&format=html) 很久了，但后者未被删除。运行此应用程序时，将显示迁移到 [gpart(8)](https://man.freebsd.org/cgi/man.cgi?query=gpart&sektion=8&format=html) 的警告。[3958be5c29da](https://cgit.freebsd.org/src/commit/?id=3958be5c29da)（由 FreeBSD 基金会赞助）

[asinf(3)](https://man.freebsd.org/cgi/man.cgi?query=asinf&sektion=3&format=html) 和 [acosf(3)](https://man.freebsd.org/cgi/man.cgi?query=acosf&sektion=3&format=html) 的精度得到提高。[33c82f11c267](https://cgit.freebsd.org/src/commit/?id=33c82f11c267)

### 运行时库和 API

[fma(3)](https://man.freebsd.org/cgi/man.cgi?query=fma&sektion=3&format=html) 现在在处理某些较小输入时（如在 Python 测试套件中观察到的情况），能够正确返回符号为零的结果。[dc39004bc670](https://cgit.freebsd.org/src/commit/?id=dc39004bc670)（由 FreeBSD 基金会赞助）

新增函数 `cap_rights_is_empty`，用于判断 `cap_rights_t` 是否未设置任何权限。[e77813f7e4a3](https://cgit.freebsd.org/src/commit/?id=e77813f7e4a3)（由 FreeBSD 基金会赞助）

## 云端支持

本节介绍云环境支持方面的变化。

- `nuageinit` 启动脚本现在支持 OpenStack 网络配置。[ea310d18b222](https://cgit.freebsd.org/src/commit/?id=ea310d18b222)（由 OVHCloud 赞助）  
- FreeBSD 项目现在可发布符合 OCI 标准的容器镜像。[8a688fcc242e](https://cgit.freebsd.org/src/commit/?id=8a688fcc242e)
- FreeBSD 项目现已发布 Oracle Cloud Infrastructure 镜像。更多信息请参见 [Oracle Cloud Infrastructure FreeBSD 列表](https://cloudmarketplace.oracle.com/marketplace/app/freebsd-release)。[77b296a2582b](https://cgit.freebsd.org/src/commit/?id=77b296a2582b)
- Amazon EC2 云环境中的 `shutdown` 和 `reboot` API 现在可支持 arm64 实例。更新至 FreeBSD 14.2-RELEASE 的旧实例需要在 `/boot/loader.conf` 中设置 `debug.acpi.quirks="8"`。[28b881840df7](https://cgit.freebsd.org/src/commit/?id=28b881840df7)（由亚马逊赞助）  
- FreeBSD 项目现在发布了“精简版（small）”的 EC2 镜像。精简版镜像在“基础版（base）”中移除了调试符号、测试、32 位库、LLDB 调试器、Amazon SSM Agent 和 AWS CLI。[953142d6baf3](https://cgit.freebsd.org/src/commit/?id=953142d6baf3)（由亚马逊赞助）

## 设备与驱动程序

本节介绍自 FreeBSD 14.1-RELEASE 以来设备和驱动程序的变更与新增内容。


### 设备驱动程序

- `ena` 驱动已更新至 2.8.0。[6bf02434bd9a](https://cgit.freebsd.org/src/commit/?id=6bf02434bd9a)（由亚马逊赞助）  
- `ice` 驱动已更新至 1.43.2-k。[38a1655adcb3](https://cgit.freebsd.org/src/commit/?id=38a1655adcb3)（由英特尔赞助）  
- `ice_ddp` 已更新至 1.3.41.0。[a9d78bb714e3](https://cgit.freebsd.org/src/commit/?id=a9d78bb714e3)（由英特尔赞助）
- 驱动程序 [hda(4)](https://man.freebsd.org/cgi/man.cgi?query=hda&sektion=4&format=html)（**译者注：man 页面没有 hda(4)，可能指 [snd_hda(4)](https://man.freebsd.org/cgi/man.cgi?snd_hda(4))**）新增了对 Tiger Lake-H 的支持。[dbb6f488df6e](https://cgit.freebsd.org/src/commit/?id=dbb6f488df6e)
- 驱动程序 [ichsmb(4)](https://man.freebsd.org/cgi/man.cgi?query=ichsmb&sektion=4&format=html) 新增了对 Meteor Lake 的支持。[14c22e28e4ee](https://cgit.freebsd.org/src/commit/?id=14c22e28e4ee)（由 Framework Computer Inc 和 FreeBSD 基金会赞助）
- 驱动 [ig4(4)](https://man.freebsd.org/cgi/man.cgi?query=ig4&sektion=4&format=html) 新增了对 Meteor Lake 的支持。[56f0fc0011c2](https://cgit.freebsd.org/src/commit/?id=56f0fc0011c2)
- 一款支持部分 Realtek 芯片组的新无线驱动已可用：[rtw89(4)](https://man.freebsd.org/cgi/man.cgi?query=rtw89&sektion=4&format=html)。[a2d1e07f6451](https://cgit.freebsd.org/src/commit/?id=a2d1e07f6451)（由 FreeBSD 基金会赞助）
- 对 Realtek 8156/8156B 的支持已从 [cdce(4)](https://man.freebsd.org/cgi/man.cgi?query=cdce&sektion=4&format=html) 迁移至 [ure(4)](https://man.freebsd.org/cgi/man.cgi?query=ure&sektion=4&format=html)，以提升性能和可靠性。[630077a84186](https://cgit.freebsd.org/src/commit/?id=630077a84186)（由 FreeBSD 基金会赞助）
- 增加了对 ACPI GPIO _AEI 对象的支持。[1db6ffb2a482](https://cgit.freebsd.org/src/commit/?id=1db6ffb2a482)（由亚马逊赞助）
- 已在所有架构上启用 [nvme(4)](https://man.freebsd.org/cgi/man.cgi?query=nvme&sektion=4&format=html) 和 [nvmecontrol(8)](https://man.freebsd.org/cgi/man.cgi?query=nvmecontrol&sektion=8&format=html)。[24687a65dd7f](https://cgit.freebsd.org/src/commit/?id=24687a65dd7f)，[aba2d7f89dcf](https://cgit.freebsd.org/src/commit/?id=aba2d7f89dcf)（由 Chelsio Communications 和奈飞赞助）  


### 弃用和删除的驱动程序

- 计划在 FreeBSD 15.0 中删除 [agp(4)](https://man.freebsd.org/cgi/man.cgi?query=agp&sektion=4&format=html) ，手册页已标注为弃用。[92af7c97e197](https://cgit.freebsd.org/src/commit/?id=92af7c97e197)  
- 计划在后续版本中删除 [syscons(4)](https://man.freebsd.org/cgi/man.cgi?query=syscons&sektion=4&format=html) ，手册页已标注为弃用，建议用户迁移至 [vt(4)](https://man.freebsd.org/cgi/man.cgi?query=vt&sektion=4&format=html)。[2bc5b1d60512](https://cgit.freebsd.org/src/commit/?id=2bc5b1d60512)（由 FreeBSD 基金会赞助）  


## 存储

本节介绍文件系统及其他本地和网络存储子系统的变更与新增内容。


### ZFS

OpenZFS 已更新至版本 2.2.6。[755e773877e9](https://cgit.freebsd.org/src/commit/?id=755e773877e9)  



## 启动加载程序的变更

本节介绍启动加载程序、启动菜单及其他与启动相关的变更。



### 启动加载程序的变更

BIOS 引导加载程序重新添加了对 gzip 和 bzip2 的支持，但默认情况下移除了图形模式的支持，以解决大小问题。（EFI 引导加载程序未受影响，仍支持上述所有功能。）[4d3b05a8530e](https://cgit.freebsd.org/src/commit/?id=4d3b05a8530e)（由奈飞赞助）


## 网络

本节介绍 FreeBSD 网络功能的变更。



### 网络协议

对网络栈进行了大量改进，涉及性能提升以及对 [sctp(4)](https://man.freebsd.org/cgi/man.cgi?query=sctp&sektion=4&format=html) 栈的错误修复。


通过 [sctp_peeloff(2)](https://man.freebsd.org/cgi/man.cgi?query=sctp_peeloff&sektion=2&format=html) 返回的描述符现在会继承父套接字的权限。[ae3d7e27abc9](https://cgit.freebsd.org/src/commit/?id=ae3d7e27abc9)（由 FreeBSD 基金会赞助）

### 一般网络

- 为驱动 [igc(4)](https://man.freebsd.org/cgi/man.cgi?query=igc&sektion=4&format=html) 新增了 AIM（Adaptive Interrupt Moderation，自适应中断调节/中断裁决）支持。[472a0ccf847a](https://cgit.freebsd.org/src/commit/?id=472a0ccf847a)（由 Rubicon Communications, LLC ("Netgate") 和 BBOX.io 赞助）  
- 此功能也已添加到了驱动程序 [lem(4)](https://man.freebsd.org/cgi/man.cgi?query=lem&sektion=4&format=html)、[em(4)](https://man.freebsd.org/cgi/man.cgi?query=em&sektion=4&format=html) 和 [igb(4)](https://man.freebsd.org/cgi/man.cgi?query=igb&sektion=4&format=html) 中。FreeBSD 12.0 中引入的 UDP 性能严重下降问题（包括基于 UDP 的 NFS）预计已通过此变更得到修复。。[49f12d5b38f6](https://cgit.freebsd.org/src/commit/?id=49f12d5b38f6)（由 Rubicon Communications, LLC ("Netgate") 和 BBOX.io 赞助）

### 无线网络

LinuxKPI（尤其是针对 802.11）的功能已增强（如 [iwlwifi(4)](https://man.freebsd.org/cgi/man.cgi?query=iwlwifi&sektion=4&format=html)），提高了无线驱动程序的稳定性。（由 FreeBSD 基金会赞助）

## 硬件支持

本节介绍了对物理设备、虚拟化环境和硬件的一般支持，以及不属于其他章节的硬件更新。

请查看 [14.2-RELEASE 硬件支持列表](https://www.freebsd.org/releases/14.2R/hardware)以及[平台页面](https://www.freebsd.org/platforms/)以了解完整的支持 CPU 架构列表。


### 处理器支持

IOAPIC ID 最大值已增加至 255，修复了某些高核心数 AMD CPU 启动失败的问题。[18119e711f1c](https://cgit.freebsd.org/src/commit/?id=18119e711f1c)（由 FreeBSD 基金会赞助）

新增对 POWER10 和 POWER11 的初步支持。[f9f006df1535](https://cgit.freebsd.org/src/commit/?id=f9f006df1535)  

### 虚拟化支持

- 现在可识别 NVMM 虚拟机管理程序。[34f40baca641](https://cgit.freebsd.org/src/commit/?id=34f40baca641)  
- 在 [bhyve(8)](https://man.freebsd.org/cgi/man.cgi?query=bhyve&sektion=8&format=html) 的 VNC 服务器中使用 [www/novnc](https://cgit.freebsd.org/ports/tree/www/novnc/) 客户端时，色彩显示已修复。[f9e09dc5b1d5](https://cgit.freebsd.org/src/commit/?id=f9e09dc5b1d5)
- 在 Hyper-V 环境下，现在通过超调用（hypercalls）（而非 IPI）执行 TLB 刷新，这使 TLB 性能有了至高 40% 的提升。[7ece5993b787](https://cgit.freebsd.org/src/commit/?id=7ece5993b787)（由微软赞助）

### Linux 二进制兼容层

现在，Linux 二进制兼容层所有的 `stat()` 及其衍生都将忽略参数 `AT_NO_AUTOMOUNT`——因为该参数指定的行为已经与 FreeBSD 的行为一致，这提高了 Linux 应用程序的兼容性。[99d3ce80ba07](https://cgit.freebsd.org/src/commit/?id=99d3ce80ba07)（由 FreeBSD 基金会赞助）

### 多媒体

对音频堆栈进行了许多改进，包括支持 [mixer(8)](https://man.freebsd.org/cgi/man.cgi?query=mixer&sektion=8&format=html) 中的热插拔功能，以及新增了工具 [mididump(1)](https://man.freebsd.org/cgi/man.cgi?query=mididump&sektion=1&format=html)。[cf9d2fb18433](https://cgit.freebsd.org/src/commit/?id=cf9d2fb18433)（由 FreeBSD 基金会赞助） [7224e9f2d4af](https://cgit.freebsd.org/src/commit/?id=7224e9f2d4af)（由 FreeBSD 基金会赞助）

## Ports 与软件包基础设施

本节介绍 FreeBSD Ports、软件包基础设施以及软件包管理和安装工具的变更。



### 安装程序

FreeBSD 安装程序 [bsdinstall(8)](https://man.freebsd.org/cgi/man.cgi?query=bsdinstall&sektion=8&format=html) 现在能在 FreeBSD 基本系统安装完成后下载和安装固件包。[03c07bdc8b31](https://cgit.freebsd.org/src/commit/?id=03c07bdc8b31)（由 FreeBSD 基金会赞助）  



### 软件包变更

已将软件包 [net/wifi-firmware-kmod@release](https://cgit.freebsd.org/ports/tree/net/wifi-firmware-kmod/) 添加到 DVD 软件包中，以提供 WiFi 驱动所需固件。[8c6df7ead19c](https://cgit.freebsd.org/src/commit/?id=8c6df7ead19c)（由 FreeBSD 基金会赞助）  


## 关于后续 FreeBSD 版本的一般说明

预计 FreeBSD 15.0 将不再支持除 armv7 以外的 32 位平台。armv6、i386 和 powerpc 平台已弃用并将被删除。但 64 位系统仍可运行旧的 32 位二进制文件。

FreeBSD 项目计划在 FreeBSD 15.0 和 stable/15 中将 armv7 作为二级（Tier 2）架构继续支持。然而，项目方预计 armv7 可能会在 FreeBSD 16.0 中被删除。FreeBSD 项目将会在 15.0 发布时更新在 15.x 和 16.x RELEASE 中 armv7 的支持状态。

通过选项 `COMPAT_FREEBSD32` 在 64 位平台上运行 32 位二进制文件的支持将至少延续到分支 stable/15 和 stable/16。此外，通过 `cc -m32` 编译单个 32 位应用程序的支持也将至少延续到分支 stable/15，该分支中将包含适当的头文件（`/usr/include`）和库（`/usr/lib32`）。

自 FreeBSD 15.0 起，Ports 系统将不再支持被弃用的 32 位平台。Ports 后续版本将不再提供用于弃用的 32 位平台的二进制软件包，也不支持使用 Ports 构建这些平台的软件包。

FreeBSD stable/14 及更早分支将保留现有的 32 位内核和系统支持。在这些分支的支持期间，Ports 系统仍将支持为 32 位系统构建 Ports 和软件包。然而，所有 32 位平台均为二级、三级（Tier-2、Tier-3），因此随着上游停止对 32 位平台的支持，个别 Port 的支持可能会逐步下降。

按照当前的支持计划，stable/14 的生命周期将在 FreeBSD 14.0-RELEASE 发布后约 5 年结束。stable/14 的生命周期结束（EOL）将参数着被弃用的 32 位平台支持的终结，包括源代码发布、预构建软件包和通过 Ports 构建应用程序的支持。随着 14.0-RELEASE 于 2023 年 11 月发布，对被弃用的 32 位平台的支持将于 2028 年 11 月结束。

当 FreeBSD 15.0 发布时，FreeBSD 项目可能选择通过延续某些弃用平台的支持，调整这一计划。所有变更将根据社区反馈以及持续支持平台的努力来决定。

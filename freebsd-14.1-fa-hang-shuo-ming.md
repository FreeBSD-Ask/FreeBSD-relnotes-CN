# FreeBSD 14.1-RELEASE 发行说明

## 摘要

FreeBSD 14.1-RELEASE 的发行说明是对由 14-STABLE 开发线衍生的 FreeBSD 基本系统所做更改的摘要。本文件列出了自上次发布以来发布的适用安全公告，以及对 FreeBSD 内核和用户空间的重大变更。还概述了部分升级备注事宜。

## 介绍

本文档涉及 FreeBSD 14.1-RELEASE 的发布说明。它说明了最近增加、更改、删除的 FreeBSD 特性。还提供了从旧版本升级的一些相关注意事项。

这些发布说明适用于“RELEASE”分行版，代表了自 14-STABLE 分支创建以来的最新状态。有关基于此分支的预构建二进制“RELEASE”的分发信息，请访问 <https://www.FreeBSD.org/releases/>。

这些发布说明适用于“RELEASE”分发版本，代表的节点位于 14.0-RELEASE 与后续 14.2-RELEASE 之间的 14-STABLE 开发分支。有关基于此分支的预构建二进制“RELEASE”的分发信息，请访问 <https://www.FreeBSD.org/releases/>。

该 FreeBSD 14.1-RELEASE 版本是个“RELEASE”版本。可以在 <https://www.FreeBSD.org/releases/> 和其镜像站中找到它。有关下载该（及其他）FreeBSD“RELEASE”版本的更多信息，请参阅 FreeBSD 手册的附录《获取 FreeBSD》。

建议所有用户在安装 FreeBSD 之前查阅发行错误。错误文档会在发布周期后期，随发布后发现的“最新”信息进行更新。通常涉及已知错误、安全公告和文档更正的相关信息。可在 FreeBSD 网站上找到 FreeBSD 14.1-RELEASE 的最新错误信息。

本文档说明了自 14.0-RELEASE 以降，在 FreeBSD 中最具用户可见性的新特性和更改。一般来说，除非其明确标记为 MERGED 特性，否则此处所述的更改独立于 14-STABLE 分支。

标准的发布说明项目记录了在 14.0-RELEASE 之后发布的最新安全公告，新的驱动程序和硬件支持，新的命令（选项），重大错误修复（含第三方）的软件升级。可能还列出了对主要软件（包）和发行工程实践的更改。显然，发布说明无法枚举在不同版本之间对 FreeBSD 所做的所有更改；该文档主要关注安全公告，用户可见的更改及重大架构改进。

## 从旧版 FreeBSD 升级

RELEASE 版本（以及各种安全分支的快照）间使用工具 freebsd-update(8) 进行二进制升级。请参阅特定于版本的升级过程，FreeBSD 14.1-RELEASE 升级信息，在 FreeBSD 手册的二进制升级过程中有更多详情。可更新未修改的用户空间工具，以及随官方 FreeBSD 发行版分发的未修改的 GENERIC 内核。freebsd-update(8) 工具要求要升级的主机拥有互联网连接。

据 /usr/src/UPDATING 所述，还可通过源代码来升级：重新编译 FreeBSD 基本系统的源代码。

|  | 仅在备份所有数据和配置文件后，才能进行 FreeBSD 升级。 |
| -- | ---------------------------------------------------- |

## 安全和勘误

此部分列出了自 14.0-RELEASE 以降的所有安全公告和勘误通知。

### 安全公告

| 公告       | 日期 | 主题 |
| ------------ | ------ | ------ |
| 无公告。 |      |      |

### 勘误通知

| 勘误     | 日期 | 主题 |
| ---------- | ------ | ------ |
| 无通知。 |      |      |

## 用户空间

此部分涉及了对用户空间工具、第三方软件和系统工具的更改和增补。

### 用户空间配置更改

现在，有一个新的变量 kdc_restart，能用来管理daemon(8)下的 kdc(8)（krb5kdc）。在 rc.conf(5)中，设置 kdc_restart="YES"：能自动重启 kdc，来解决其异常停止问题。kdc_restart_delay="N" 设定了重启 kdc 前的延迟（秒）。abc4b3088941

在默认情況下，电子邮件中由周期性(8)工具显示变更，为了减少输出大小，通过 daily 脚本比以前输出的上下文要少。此行为由 periodic.conf(5)中的变量 daily_diff_flags 控制。同样地，安全脚本显示的更改比以前少，由 periodic.conf(5) 中的变量 security_status_diff_flags 控制。538994626b9f, 37dc394170a5, 128e78ffb084

### 用户空间工具的变更

由 bsdinstall(8) 调用的工具 adduser(8)，现在将为位于 ZFS 数据集上父目录，新用户的家目录创建一个 ZFS 数据集。命令行参数可禁用此独立数据集。ZFS 加密 also 可用。516009ce8d38

工具 date(1) 已支持纳秒。如： date -Ins 打印为 "2024-04-22T12:20:28,763742224+02:00"， date +%N 打印为 "415050400"。eeb04a736cb9

工具 dtrace(1) 已支持使用 libxo(3) 生成机器可读的输出格式：JSON、XML 和 HTML。aef4504139a4 (由 Innovate UK 赞助)

工具 lastcomm(1) 已支持精度到秒的显示时间戳。692c0a2e80c1 (由 DSS Gmbh 赞助)

工具 ldconfig(8) 已支持字节序为任一字节序的提示文件。默认格式为主机的本地字节序。fa7b31166ddb

OpenSSH 已升级至版本 9.7p1。完整的发布说明请参见 https://www.openssh.com/txt/release-9.7 和 https://www.openssh.com/txt/release-9.6 。a25789646d71, 464fa66f639b（由 FreeBSD 基金会赞助）

工具 usbconfig(8) 已支持：在可用时，从 /usr/share/misc/usb_vendors 读取 usb 供应商和产品的描述，类似于 pciconf(8) 的行为。7b9a772f9f64

### 第三方软件

One True Awk（awk(1)）已更新至第二版，新增了 -csv 和 UTF-8 支持。daf917daba9c

Clang/LLVM 已升级至版本 18.1.5。90a5e985e5f4

libarchive(3) 库已升级至版本 3.7.4。8774c92e32b2

套件 sendmail(8) 已升级至版本 8.18.1，修复了漏洞 CVE-2023-51765。58ae50f31e95

unbound(8) 解析器已升级至版本 1.20.0，并修复了 “DNSBomb” 漏洞（CVE-2024-33655）。dcde37c4170b

### 运行时库和 API

libutil 中的 setusercontext(3) 例程可依据一定的条件从家目录下的 .login.conf 文件以及系统 login.conf(5)设置进程优先级（nice）。优先级可以具有值 inherit ，意味着优先级会保持与父进程相同。umask 亦可以具有值 inherit 。6f6186e19fe5, a8c273b3c97f, d2d66fedc418（由 Kumacom SAS 赞助）

在 amd64 系统上可用时，C 库中的许多字符串和内存操作，都能用 SIMD（单指令多数据）进行扩展以提高性能；请参阅 simd(7)。（由 FreeBSD 基金会赞助）

在受支持的平台上, math(3) 库中的 128 位 tgammal 函数实现有了更好的实现。8df6c930c151

## 云端

本节涉及了对云端的更改。

14.1-RELEASE 支持 cloudinit，涉及 nuageinit 启动脚本和对 config-drive 分区的支持。它可兼容 OpenStack 和许多托管设施。请参阅 cloud-init 网站和提交信息，16a6da44e28d 227e7a205edf。（由 OVHCloud 赞助）

## 内核

本节涉及了对内核配置、系统调优和系统控制参数的更改，这些更改未分类。

### 通用内核更改

已为 powerpc 实现了例程 fpu_kern_enter 和 fpu_kern_leave，能在使用浮点和矢量寄存器的内核中使用加密函数 ossl(4) 了。91e53779b4fc

## 设备和驱动程序

本节内容涉及自 14.0-RELEASE 以降的设备和设备驱动程序的更改和增加。

### 设备驱动程序

Intel E800 系列（ice(4) 以太网网络控制器）已有驱动程序，可支持 100 Gb/s 速率。该驱动程序已升级至版本 1.39.13-k. 71d104536b51 f6de0a7c94e9（由英特尔公司赞助）。

英特尔 WiFi 设备的 iwlwifi(4) 驱动程序已进行了许多稳定性改进。(由 FreeBSD 基金会赞助)

现在在 amd64 和 i386 上支持多个 PCI MCFG 区域，允许对除 0 之外的域（段）进行 PCI 配置空间访问。4b5f64408804

以太网驱动程序 smsc(4) 可获取某些树莓派型号传递的 smsc95xx.macaddr 值，并将其用于 MAC 地址。即使在 EEPROM 中没有地址，它也将始终使用固定的 MAC 地址。028e4c6548e4

声音子系统中已移除 snd_clone 框架（及相关 sysctl）。简化了系统：不再创建单个通道节点（/dev/dspX.Y），仅创建主设备（/dev/dspX）。e6c51f6db8d7（由 FreeBSD 基金会赞助）

音频已支持异步设备分离。这极大地简化了诸如 USB 耳机之类的热插拔行为，且在需要操作系统休眠和唤醒（休眠和恢复）时，使用 PulseAudio 会更轻松。d692c314d29a（由 FreeBSD 基金会赞助）

## 存储

此部分涉及了对文件系统和其他存储子系统（包括本地和网络存储）的更改和增补。

### NFS

mountd(8) 服务器已修改为使用 strunvis(3) 解码文件 exports(5) 中的目录名称。故现可在目录名中使用特殊字符（如空格）。可使用 vis -M 对此类目录名进行编码；请参阅 vis(1)。2c83f1ada435

新添加的 sysctl（8）变量为 kern.rpc.unenc 和 kern.rpc.tls，能让 NFS 服务器管理员获取 NFS-over-TLS 运行时的使用数据。大量的失败握手可能意味着 NFS 配置有问题。b8e137d8d32d

### UFS

在使用 newfs（8）创建 UFS 文件系统时，已默认启用软更新。6b2af2d88ffd

### ZFS

OpenZFS 已升级至版本 2.2.4. 78c9d8f1ce65

## 引导加载程序更改

本节涉及了引导加载程序、引导菜单和其他与引导相关的更改。

### 引导加载程序更改

现在 loader(8) 会在其他配置文件之后，读取列在变量 local_loader_conf_files 中的本地配置文件， 默认为 /boot/loader.conf.local。a25531db0fc2

loader(8) 已可根据来自 SMBIOS 的平面制造商、平面产品、系统产品和 uboot m_product 变量读取特定配置文件进行配置。目前，最佳文档是 git 的提交信息，3eb3a802a31b。

对于 EFI 设备，loader(8) 中的控制台检测得到了改进。如果没有 ConOut 变量，会检查 ConIn。如果找到多个设备，则首选串行。20a6f4779ac6（由 Netflix 赞助）

loader(8) 中的帧缓冲区现在支持使用仅文本的视频驱动程序，从而节省空间。57ca2848c0aa（由 Netflix 赞助）

在 arm64 设备上的 loader.efi(8)，会更早地完成 ACPI 检测。对于基于 ACPI 的 arm64 设备，应更新 EFI 分区上的 loader.efi 文件。05cf4dda599a 16c09de80135

加载程序 LinuxBoot 可用于从 Linux 引导 FreeBSD。（aarch64、amd64），46010641267（由 Netflix 赞助）

## 网络

本节概述了影响 FreeBSD 网络的变更。

### 通用网络

ARP（arp（4））已恢复对 802 标准网络的支持；它曾在 FDDI 支持中被意外移除（以太网标准封装不同。）d776dd5fbd48

支持构建仅 IPv6 支持（INET6），无 IPv4 支持（INET）的内核。6df9fa1c6b83 和其他

netgraph ng_ipfw(4) 模块不再将 cookie 截断为 16 位，可使用完整的 32 位。dadf64c5586e

## 硬件支持

本节涉及了物理机、虚拟化环境的一般硬件支持，以及不兼容于本文档其他部分的硬件更改和更新。

请查看 14.1-RELEASE 支持的硬件列表，以及受支持的 CPU 架构完整列表页。

## 文档

本节涉及了与基本系统一起提供的手册（man(1)）页和其他文档的更改。

### 手册页面

新的网络(7)手册页包含了连接系统到网络（包括 Wi-Fi）的快速入门指南，并链接到了其他手册页面和手册。39f92a4c4c49

## 后续 FreeBSD 版本发布的一般注意事项

FreeBSD 15.0 预计不会支持除 armv7 以外的 32 位平台。 armv6、i386 和 powerpc 平台已被弃用并将被移除。 64 位系统仍可运行旧款 32 位二进制文件。

我们预计将在 FreeBSD 15.0 及 stable/15 中，把 armv7 作为第二级架构。然而，我们也预计可能会在 FreeBSD 16.0 中移除 armv7。我们将在发布 15.0 时提供armv7 在 15.x 和 16.x 中状态的相关更新。

对于在 64 位平台上执行 32 位二进制文件的支持（参数 COMPAT_FREEBSD32）将至少在稳定/15 和稳定/16 分支上延续。至少在稳定/15 分支上，还将继续支持使用 cc -m32 编译单个 32 位应用程序，其中包括 /usr/include 中的相应头文件和/usr/lib32 中的库。

对于 FreeBSD 15.0 及后续版本，Ports 将不再支持已废弃的 32 位平台。这些后续版本将不再支持已废弃的 32 位平台上的二进制软件包、ports 构建软件包。

FreeBSD 稳定/14 和更早版本分支将保留对现有的 32 位内核和系统支持。只要这些分支仍受 ports 系统支持，Ports 将保留对在稳定/14 和早期版本分支上构建ports和软件包的支持。但是，所有 32 位平台都是二级、三级，应该预期：个别的ports支持将随着上游废弃 32 位平台而降级。

根据当前的生命周期，stable/14 将在 FreeBSD 14.0-RELEASE 发布后的 5 年结束生命周期（EOL）。stable/14 的生命周期终点标志着对包括源代码发布、预构建软件包以及从ports构建应用程序的弃用 32 位平台的支持结束。随着 2023 年 11 月 14.0-RELEASE 的发布，对已弃用的 32 位平台支持将在 2028 年 11 月结束。

当 FreeBSD 15.0 发布后，FreeBSD 项目可能选择在 15.0（或后续）版本中延长对一个（多个）已弃用平台的某支持程度来改变这种方法。所有变更均由社区反馈和致力于支持这些平台的努力驱动。使用 FreeBSD 14.0-RELEASE 和随后的小版本发布，或者 stable/14 分支，可迁走 32 位平台。

---

最后修改于：2024 年 6 月 4 日，作者 Alexander Ziaee
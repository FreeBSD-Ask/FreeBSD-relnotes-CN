# FreeBSD 中文版发行说明

>**技巧**
>
>那些关注实时开发状态或使用 CURRENT 的用户应该关注 [freebsd-src/UPDATING](https://github.com/freebsd/freebsd-src/blob/main/UPDATING) 及 [freebsd-src/RELNOTES](https://github.com/freebsd/freebsd-src/blob/main/RELNOTES)。
>
>否则仅建议你使用在生命周期内最新的 RELEASE 版本。

>**警告**
>
>除已校对部分外，本项目目前翻译错漏百出，不适合用于生产。但译者已经尽力修正。
>
>本项目目前处于低维护状态，主要维护者因精力所限仅处理 PR。欢迎社区通过 PR 贡献力量。

镜像实时构建状态：

- <https://ci.freebsd.org/tinderbox/>

---

- 发行说明原文：<https://www.freebsd.org/releases/>
- 版本发布计划：<https://www.freebsd.org/releng/>

---


| 日期           | 事件        | 信息 |
| :---------------- | :--------------: | :-------------: |
| 2025 年 12 月  | FreeBSD 15.0 |     [参见此处](https://www.freebsd.org/releases/15.0R/schedule/)         |
| 2026 年 3 月     | FreeBSD 14.4 |    [参见此处](https://www.freebsd.org/releases/14.4R/schedule/)        |
| 2026 年 6 月      | FreeBSD 15.1 |             |
| 2026 年 9 月 | FreeBSD 14.5 |             |
| 2026 年 12 月  | FreeBSD 15.2 |             |
| 2027 年 3 月     | FreeBSD 14.6 |             |
| 2027 年 6 月      | FreeBSD 15.3 |             |
| 2027 年 12 月  | FreeBSD 16.0 |             |

——[发布工程信息](https://www.freebsd.org/releng/)

## 安全支持与生命周期

| 分支          | 版本        | 发布日期             |  EoL 预期（生命周期结束） |
| :-------------: | :----------: | :--------------------: | :--------------------: |
| stable/14   | 不适用     | 不适用            | 2028 年 11 月 30 日  |
| releng/14.3 | 14.3-RELEASE | 2025 年 6 月 10 日    | 2026 年 6 月 30 日  |
| releng/14.2 | 14.2-RELEASE | 2024 年 12 月 3 日   | 2025 年 9 月 30 日  |
| stable/13   | 不适用        | 不适用                | 2026 年 4 月 30 日  |
| releng/13.5 | 13.5-RELEASE | 2025 年 3 月 11 日   | 2026 年 4 月 30 日  |

——[FreeBSD 安全信息](https://www.freebsd.org/security/#sup)

## 平台支持


| 平台名称                 | 目标架构                                                  | 13.x [支持等级](https://docs.freebsd.org/en/articles/committers-guide/#archs) | 14.x [支持等级](https://docs.freebsd.org/en/articles/committers-guide/#archs) | 15.x [支持等级](https://docs.freebsd.org/en/articles/committers-guide/#archs) | 预计 16.x [支持等级](https://docs.freebsd.org/en/articles/committers-guide/#archs) |
| :--------------------: | :--------------------------------------------------------------: | :-------------------------------------------------------------------------: | :-------------------------------------------------------------------------: | :-------------------------------------------------------------------------: | :----------------------------------------------------------------------------: |
| 64 位 x86             | [amd64](https://www.freebsd.org/platforms/amd64)               | 一级                                                                        | 一级                                                                        | 一级                                                                        | 一级                                                                           |
| 32 位 x86             | [i386](https://www.freebsd.org/platforms/i386)                 | 二级                                                                        | 二级                                                                        | 不支持                                                                       | 不支持                                                                          |
| 64 位 ARMv8           | [aarch64](https://www.freebsd.org/platforms/arm)               | 一级                                                                        | 一级                                                                        | 一级                                                                        | 一级                                                                           |
| 32 位 ARMv6           | [armv6](https://www.freebsd.org/platforms/arm)                 | 二级                                                                        | 三级                                                                        | 不支持                                                                       | 不支持                                                                          |
| 32 位 ARMv7           | [armv7](https://www.freebsd.org/platforms/arm)                 | 二级                                                                        | 二级                                                                        | 二级                                                                        | 二级                                                                           |
| 32 位 MIPS 软浮点        | [mips, mipsel](https://www.freebsd.org/platforms/mips)         | 二级                                                                        | 不支持                                                                       | 不支持                                                                       | 不支持                                                                          |
| 32 位 MIPS 硬浮点        | [mipshf, mipselhf](https://www.freebsd.org/platforms/mips)     | 二级                                                                        | 不支持                                                                       | 不支持                                                                       | 不支持                                                                          |
| 32 位 MIPS n32        | [mipsn32](https://www.freebsd.org/platforms/mips)              | 二级                                                                        | 不支持                                                                       | 不支持                                                                       | 不支持                                                                          |
| 64 位 MIPS 软浮点        | [mips64, mips64el](https://www.freebsd.org/platforms/mips)     | 二级                                                                        | 不支持                                                                       | 不支持                                                                       | 不支持                                                                          |
| 64 位 MIPS 硬浮点        | [mips64hf, mips64elhf](https://www.freebsd.org/platforms/mips) | 二级                                                                        | 不支持                                                                       | 不支持                                                                       | 不支持                                                                          |
| 32 位 PowerPC         | [powerpc](https://www.freebsd.org/platforms/ppc)               | 二级                                                                        | 二级                                                                        | 不支持                                                                       | 不支持                                                                          |
| 带 SPE 的 32 位 PowerPC | [powerpcspe](https://www.freebsd.org/platforms/ppc)            | 二级                                                                        | 二级                                                                        | 不支持                                                                       | 不支持                                                                          |
| 64 位 PowerPC 大端序     | [powerpc64](https://www.freebsd.org/platforms/ppc)             | 二级                                                                        | 二级                                                                        | 二级                                                                        | 二级                                                                           |
| 64 位 PowerPC 小端序     | [powerpc64le](https://www.freebsd.org/platforms/ppc)           | 二级                                                                        | 二级                                                                        | 二级                                                                        | 二级                                                                           |
| 64 位 RISC-V          | [riscv64](https://wiki.freebsd.org/riscv)                      | 二级                                                                        | 二级                                                                        | 二级                                                                        | 二级                                                                           |
| 64 位 RISC-V 软浮点      | [riscv64sf](https://wiki.freebsd.org/riscv)                    | 二级                                                                        | 不支持                                                                       | 不支持                                                                       | 不支持                                                                          |



| 平台名称             | 目标架构 | 最后支持的 RELEASE 版本                                         |
| :----------------: | :------------: | :-------------------------------------------------: |
| Alpha            | alpha        | [6.4](https://www.freebsd.org/releases/#rel6-4)   |
| 32 位小端 ARM v4/v5 | arm          | [12.4](https://www.freebsd.org/releases/#rel12-4) |
| 32 位大端 ARM       | armeb        | [11.4](https://www.freebsd.org/releases/#rel11-4) |
| Intel IA-64      | ia64         | [10.4](https://www.freebsd.org/releases/#rel10-4) |
| PC98             | pc98         | [11.4](https://www.freebsd.org/releases/#rel11-4) |
| 64 位 SPARCv9     | sparc64      | [12.4](https://www.freebsd.org/releases/#rel12-4) |


——[Supported Platforms](https://www.freebsd.org/platforms/)

### 21. 多架构支持

——[提交者指南](https://docs.freebsd.org/en/articles/committers-guide/#archs)

FreeBSD 是一款高度可移植的操作系统，旨在于多种不同类型的硬件架构上运行。保持机器相关 (MD) 与机器无关 (MI) 代码的清晰分离，以及尽量减少机器相关代码，是我们在硬件趋势方面保持灵活性的关键策略之一。每增加一项 FreeBSD 所支持的新硬件架构，都会显著增加代码维护、工具链支持和版本工程的成本。同时，它也会极大地增加对内核变更进行有效测试的成本。因此，我们有充分的理由在保持对少数几项关键架构（被视为 FreeBSD 的“目标受众”）重点支持的同时，对不同架构的支持类别进行区分。

#### 21.1. 总体意向声明

FreeBSD 项目的目标是“生产级的商用现成品/技术（Commercial Off-The-Shelf，COTS）工作站、服务器以及高端嵌入式系统”。通过将关注点保持在这些环境中的少数架构上，FreeBSD 项目能够维持高水平的质量、稳定性和性能，同时尽量减轻项目中各支持团队（如 Ports 团队、文档团队、安全官以及版本工程团队）的负担。硬件支持的多样性为 FreeBSD 用户提供了更多的选择，带来了新特性和新的使用机会，但这些收益必须始终结合额外平台支持在现实中的维护成本进行慎重权衡。

FreeBSD 项目将平台目标分为四个层级。每个层级都包含用户可以依赖的保证列表，以及项目和开发者履行这些保证的义务。这些列表定义了各层级的最低保证。项目和开发者可能会在某一层级的最低保证之外提供额外支持，但这些额外支持并无保证。每个平台目标在每个稳定分支上都会被分配到一个特定层级。因此，在不同的并行稳定分支中某个平台目标可能会被分配到不同的层级。

#### 21.2. 平台目标

对一个硬件平台的支持包含两个组成部分：内核支持和用户空间应用二进制接口 (ABI)。内核平台支持包括运行 FreeBSD 内核在某一硬件平台所需的内容，例如机器相关的虚拟内存管理和设备驱动。用户空间 ABI 指定了用户进程与 FreeBSD 内核及基本系统库交互的接口。用户空间 ABI 包括系统调用接口、公共数据结构的布局与语义，以及传递给子程序的参数的布局与语义。ABI 的某些组件可能由规范定义，例如 C++ 异常对象的布局，或 C 函数的调用约定。

FreeBSD 内核本身也使用一种 ABI（有时称为内核二进制接口：Kernel Binary Interfac，KBI），它包括公共数据结构的语义和布局，以及传递给内核内部公共函数的参数的布局和语义。

单个 FreeBSD 内核可能支持多个用户空间 ABI。例如，FreeBSD 的 amd64 内核支持 FreeBSD amd64 与 i386 用户空间 ABI，同时也支持 Linux x86\_64 和 i386 用户空间 ABI。FreeBSD 内核应支持一个“原生” ABI 作为默认 ABI。原生 ABI 通常与内核 ABI 共享某些特性，例如 C 调用约定、基本类型的大小等。

层级同时针对内核和用户空间 ABI 定义。在常见情况下，一个平台的内核和 FreeBSD ABI 会被分配到相同的层级。

##### 21.2.1. 一级（Tier 1）：完全支持的架构

一级平台是 FreeBSD 最成熟的平台。它们受到安全官、版本工程以及 Ports 管理团队的支持。一级架构在 FreeBSD 操作系统的各个方面（包括安装和开发环境）都应达到生产级质量。

FreeBSD 项目向一级平台的用户提供以下保证：

- 版本工程团队将提供官方的 FreeBSD 发行镜像。
- 对受支持的发行版，将提供安全公告和勘误通知的二进制更新与源代码补丁。
- 对受支持的分支，将提供安全公告的源代码补丁。
- 针对跨平台的安全公告，通常会在公告发布时同时提供二进制更新和源代码补丁。
- 对用户空间 ABI 的更改通常会包含兼容性填充层，以确保在任何稳定分支上编译的二进制文件在该平台作为一级时能正常运行。这些填充层可能不会在默认安装中启用。若某次 ABI 变更未提供兼容性填充层，该情况将在发行说明中明确记录。
- 对内核 ABI 某些部分的更改会包含兼容性填充层，以确保针对该分支上最早受支持的版本编译的内核模块能正常运行。注意，并非内核 ABI 的所有部分都受保护。
- Ports 团队将提供第三方软件的官方二进制包。对于嵌入式架构，这些包可能是从其他架构交叉构建的。
- 绝大多数相关的 ports 具有可构建性，或具备适当的过滤机制以避免不合适的 ports 被构建。
- 新特性若非平台特定，应在所有一级架构上完全可用。
- 针对旧稳定分支编译的二进制所使用的特性和兼容性填充层可能会在新的主版本中移除。将在发行说明中明确记录此类移除。
- 一级平台应有完整文档。将在 FreeBSD 手册中记录基本操作。
- 一级平台将被包含在源代码树中。
- 一级平台应能自举构建（self-hosting），无论是通过源内工具链还是外部工具链。如果需要外部工具链，将提供该工具链的官方二进制包。

为保持一级平台的成熟度，FreeBSD 项目将维持以下资源以支持开发：

- 在 FreeBSD.org 集群或开发者可便捷访问的其他位置提供构建和测试自动化支持。嵌入式平台可在 FreeBSD.org 集群使用模拟器代替真实硬件。
- 被纳入 `make universe` 和 `make tinderbox` 目标。
- 在某个 FreeBSD 集群中提供专用硬件，用于构建包（可为原生或通过 qemu-user 进行）。

开发者集体需要履行以下义务以维持某平台的一级状态：

- 不得在明知的情况下，使对源代码树的修改破坏一级平台的构建。
- 一级架构必须拥有成熟且健康的用户和活跃开发者生态。
- 开发者应能在常见可用的非嵌入式一级系统上构建软件包。这既可以是原生构建（如果该平台常见有非嵌入式系统），也可以是基于其他一级架构的交叉构建。
- 修改不得破坏用户空间 ABI。若需更改 ABI，应通过符号版本控制或共享库版本提升来为现有二进制提供兼容性。
- 合并到 STABLE 分支的更改不得破坏受保护的内核 ABI 部分。若需更改内核 ABI，应调整该更改以保持现有内核模块的功能。

##### 21.2.2. 二级（Tier 2）：开发中与小众架构

二级平台是功能可用但欠缺成熟的 FreeBSD 平台。它们不受安全官、版本工程以及 Ports 管理团队的支持。

二级平台可能是仍在积极开发中的一级候选平台。生命周期接近终结的架构也可能由一级降为二级，因为维持其生产级状态的资源逐渐不足。有良好支持的小众架构也可能属于二级。

FreeBSD 项目向二级平台的用户提供以下保证：

- Ports 基础设施应包含对二级架构的基本支持，足以构建 ports 和软件包。这包括对 ports-mgmt/pkg 等基础包的支持，但不能保证任意 ports 都可构建或正常运行。
- 新特性如果不是平台特定的，在二级架构上应具备实现的可行性，即使尚未实现。
- 二级平台将被包含在源代码树中。
- 二级平台应能自举构建（self-hosting），无论是通过源内工具链还是外部工具链。若需外部工具链，将提供该工具链的官方二进制包。
- 二级平台应能提供可用的内核和用户空间，即使未提供官方发行版。

为保持二级平台的成熟度，FreeBSD 项目将维持以下资源以支持开发：

- 被纳入 `make universe` 和 `make tinderbox` 目标。

开发者集体需要履行以下义务以维持某平台的二级状态：

- 不得在明知的情况下，使对源代码树的修改破坏二级平台的构建。
- 二级架构必须拥有活跃的用户和开发者生态。
- 修改可以破坏用户空间 ABI，但不应无故破坏。重要的用户空间 ABI 变更应限制在主版本。
- 尚未在二级架构上实现的新特性应提供关闭方式以避免影响这些架构。

##### 21.2.3. 三级（Tier 3）：实验性架构

三级平台至少具备部分 FreeBSD 支持。它们 **不受** 安全官、版本工程以及 Ports 管理团队的支持。

三级平台可能处于开发早期，针对非主流硬件平台，或被视为不太可能广泛使用的旧架构。三级平台的初始支持可能存在于独立仓库而不是主源码仓库。

FreeBSD 项目对三级平台用户不提供任何保证，也不承诺维持开发支持资源。三级平台可能无法始终构建，内核或用户空间 ABI 也不被视为稳定。

#### 21.2.4. 不支持的架构

其他平台在任何形式下都不受项目支持。此前项目将这些称为四级系统。

在某个平台转变为不支持状态后，将从源代码树、ports 和文档树中移除对该平台的所有支持。注意，只要该平台在某个受 ports 支持的分支中仍然受支持，ports 支持应继续保留。


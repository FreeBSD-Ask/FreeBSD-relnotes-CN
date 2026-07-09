# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库概览

这是 FreeBSD 发行说明（Release Notes）的中文翻译项目。基于 GitBook 格式，发布在 <https://relnotes.bsdcn.org/>。

源内容为 Markdown 文件，由 GitBook 平台自动构建和部署，无需本地构建步骤。

**翻译基准：** 以 `en/` 文件夹下的 AsciiDoc 归档为唯一权威源。`en/` 按发行版目录组织（如 `en/14.4R/`、`en/15.1R/`），每个目录包含该发行版的全部文档（`relnotes.adoc`、`installation.adoc`、`hardware.adoc` 等）。

## 内容架构

### 核心文件

- **`SUMMARY.md`** — 全书唯一数据源，定义完整目录结构和导航树。GitBook 用它来生成侧边栏。 **第一行 `# Table of contents` 绝对不能变更** ，否则 GitBook 同步失效。
- **`CHANGELOG.md`** — 编辑日志，记录翻译进度和同步上游的 commit。
- **`README.md`** — 项目首页，包含发行计划、生命周期、平台支持等概览信息。

### 目录结构

- 本项目为 **扁平文件结构**，所有 `.md` 文件直接放在仓库根目录，不存在子目录章节模式。
- 文件命名遵循以下模式：
  - 单架构发行版：`<版本>.md`（如 `14.4.md`、`15.1.md`、`13.0.md`）
  - 多架构发行版：`<版本>-<架构>.md`（如 `6.4-amd64.md`、`5.2-amd64.md`、`4.4-i386.md`）
  - 早期命名变体：`freebsd-<版本>-fa-hang-shuo-ming.md`（如 `freebsd-14.0-fa-hang-shuo-ming.md`）为既有文件，保持原样
- `en/` — 英文 AsciiDoc 原版归档，按发行版目录组织：
  - 目录命名为 `<版本>R`（如 `en/14.4R/`、`en/15.1R/`、`en/6.4R/`、`en/1.1/`）
  - 每个目录包含该发行版的全部文档：`_index.adoc`、`announce.adoc`、`relnotes.adoc`、`installation.adoc`、`hardware.adoc`、`readme.adoc`、`errata.adoc`、`signatures.adoc`、`schedule.adoc` 等
  - 早期发行版（4.x-6.x）按架构分文件，如 `relnotes-amd64.adoc`、`relnotes-i386.adoc`、`relnotes-alpha.adoc`、`relnotes-sparc64.adoc`、`relnotes-powerpc.adoc`、`relnotes-pc98.adoc`、`installation-<arch>.adoc`、`hardware-<arch>.adoc`
  - 部分发行版含 `upgrading.adoc`（如 15.1R）或其他特殊文件（`todo.adoc`、`pressrelease.adoc`、`approvals.adoc`、`relnotes-detailed.adoc`）
  - 用于翻译对照参考，**不要修改或翻译其中的内容**

### 标题管理（关键约束）

`sync-headers.yml` 工作流会在每次 push 时自动将 `SUMMARY.md` 中的标题同步到对应 `.md` 文件的 H1。 **这意味着直接编辑 `.md` 文件的 `# 标题` 会被 CI 覆盖。** 修改章节标题时，只改 `SUMMARY.md` 中对应的 `* [标题](路径)` 条目即可。

## CI/CD 工作流

所有工作流位于 `.github/workflows/`：

| 工作流 | 触发条件 | 说明 |
| ------ | -------- | ---- |
| `sync-headers.yml` | push | 从 SUMMARY.md 同步一级标题到各 .md 文件 |
| `markdown-lint2.yml` | workflow_dispatch | markdownlint 检查，规则见 `.github/.markdownlint.json` |
| `Markdown-lint2-pr.yml` | workflow_dispatch | markdownlint 检查并创建 PR |
| `md-padding.yml` | workflow_dispatch | 自动在 CJK 与英文/数字间添加空格 |
| `AutoCorrect.yml` | --- | 自动修正常见中文笔误与格式问题 |
| `links.yml` | 定时 + workflow_dispatch | lychee 死链检查，配置见 `.github/lychee.toml` |
| `pdf.yml` | --- | 导出 PDF |

## 编写规范

### 格式

- **命令行前缀：** `#` 表示 root 权限，`$` 表示普通用户。不要使用 `sudo`。
- **提示块：** tip/important/note/warning/caution 使用 `>` 缩进引用，关键词 **加粗**。
- **代码块：** 无法判断的，再使用 ` ```sh ` 兜底，禁止使用 text 作为代码块标记，不窜改既有的 ` ```ini ` 标记。
- **表格：** 一律居中。
- **禁止 HTML：** 本项目不支持任何 HTML 语法。
- **文件命名：** 使用拼音 slug 或版本号，文件名中不得包含空格、中文字符或英文冒号 `:`，必须兼容 Windows 操作系统对文件名的要求。
- **路径与 IP：** 全书正文中的路径（带 `/` 或 `\` 的，如 `/etc/rc.conf`、`/usr/local/etc/`）和 IP 地址一律使用 **加粗**，不使用反引号 `` ` `` 包裹；不要混合使用 `*` 和 `` ` ``（如 `*`path`*` 是错误的）。
- **命令、选项、参数：** 命令、选项、可调选项、可调参数等格式使用 `行间代码`（反引号）包裹。
- **转义字符：** 除非是命令、选项和参数，否则含转义字符 `\` 的元素一律使用 **加粗** 包裹整个元素，不在正文中直接使用转义字符（如写 **PROTO_TYPE** 而非 `PROTO\_TYPE` 在正文里裸露）。逐个手动修改，禁止批量替换。
- **引号规范：** 正文禁止使用日式引号「」（如「livefs」），一律使用中文双引号“”（如“livefs”）。全书正文标点符号统一使用全角，包括“”及括号、引号等，避免半角混用。逐个手动修改，禁止批量替换。
- **避免滥用"已"字：** 如"XX 已新增"应改为"新增 XX"；"已修复"应改为"修复完成"。禁止机械替换。
- **避免滥用"一个 xx"：** 如"一个驱动"应改为"某驱动"或具体名称；"一个新功能"应改为"一项新功能"或具体功能名。禁止机械替换。
- **避免欧化汉语：** 倒装句、后置句、偷换主语、不必要的被动句应改为地道汉语表述。
- **禁止篡改：** 不要篡改软件版本号、用户名、带圈数字（如 ①②③ 等），确保其位置、数量和英语原文一致。
- **避免章节交叉引用：** 正文不要出现具体的章节交叉引用（如"参见第 5 章"），改用语义化链接。
- **内部锚点改外链：** 英文原文中的 HTML 锚点（如 `#ETHERNET`、`#BLUETOOTH`、`#INTRO` 等）在 Markdown 翻译中不存在对应锚点，必须改为指向 FreeBSD 官方网站对应页面的外链。URL 格式为 `https://www.freebsd.org/releases/<版本>R/<文档类型>.html#<锚点>`（如 `https://www.freebsd.org/releases/7.1R/hardware.html#ETHERNET`）。逐个手动修改，禁止批量替换。
- **代码块注释翻译：** 代码块（` ``` ` 围栏）内的英文注释必须翻译为中文（如 shell 注释 `# This is a comment` → `# 这是一个注释`）。只翻译注释部分，不修改实际命令或代码。保持代码结构和格式不变。
- **禁止 AsciiDoc 残留语法：** 禁止在 Markdown 中保留 AsciiDoc 的 `::` 定义列表语法（如 `mini-memstick::`、`dvd1::`）和 `+` 续行标记。`::` 双冒号一律不被允许。英文原文中的 AsciiDoc 定义列表术语（如 `dvd1::`、`disc1::`、`bootonly::`、`memstick::`、`mini-memstick::`、`FreeBSD/arm SD 卡镜像::`）必须转换为 Markdown 加粗标签格式：`**术语**` + 空行 + 描述文本。`+` 续行标记必须移除，段落间用空行分隔。如需链接，必须指向真实 URL，不得使用 `::` 伪引用。
- **fstab 不翻译：** fstab 文件表头（如 `# Device Mountpoint FStype Options Dump Pass#`）及其相关内容保持英文原样，不翻译。

### 术语

- `Ports` 保持英文不翻译，且保持首字母大写（注意区分真正的"端口"）禁止机械替换。
- "Jail" 保持英文（不翻译为"监狱"、"监牢"）禁止机械替换。
- "pkgbase" 保持英文不翻译（不翻译为"打包基系统"、"打包基本系统"、"基系统包"等）。禁止机械替换。
- "base system" → "基本系统"（不翻译为"基系统"等）。禁止机械替换。
- "package" / "packages" → "软件包"（不保留英文 "package"，不翻译为"包"）。代码块和命令输出中的 "package" 保留英文。禁止机械替换。
- "Google Summer of Code" → "谷歌编程之夏"，"GSoC" → "编程之夏"（"Google" 已单独翻译时不重复）。禁止机械替换。
- "拷贝" → "复制"，"壳/外壳" → "shell"。禁止机械替换。
- "The FreeBSD Foundation" → "FreeBSD 基金会"，注意前后空格自动调整（CJK 与 CJK 间不留空格，如"基金会的注册商标"、"基金会[捐赠]"；CJK 与 Latin 间保留空格，如"包括 FreeBSD 基金会、"）。禁止机械替换。
- 第二人称一律使用"你"而非"您"

### CJK 空格

中英文、中文与数字之间必须加半角空格。文件和命令名用 `` ` `` 括起来。`md-padding.yml` 和 `AutoCorrect.yml` 工作流会自动检测修复。

### 图片

在正文中插入图片，使用 markdown 格式。

### 翻译流程

1. 参考 `en/` 文件夹下对应发行版目录的 adoc 文件进行人工校对
2. 提交 PR 到 main 分支

### 翻译校对工作流程（Claude Code）

对已翻译章节进行质量审校时，参考以下步骤：

1. **获取原文**：以 `en/` 文件夹下对应发行版目录的 adoc 文件为唯一权威源（如 `en/14.4R/relnotes.adoc`、`en/6.4R/relnotes-amd64.adoc`），不再通过 `WebFetch` 抓取 handbook 页面。

2. **逐句对照**：将中文翻译与英文 adoc 原文逐句比对，重点检查以下问题类别：

   | 问题类型 | 示例 |
   | -------- | ---- |
   | 事实性错误 | "large parts" 误译为"三个文件" |
   | 漏译 | 英文原版有但中文缺失的句子 |
   | 机翻腔/表达生硬 | "在阅读本章后，你将会收获" → "通过阅读本章，你将了解" |
   | 用词不当 | "独家优势"应为"主要优势"（原文 "particular strengths"） |
   | 版本过时 | 15.0-CURRENT 未同步至 16.0-CURRENT |
   | 语法/文字错误 | 重复字词、"非常地"应为"非常" |
   | 欧化汉语、倒装句、后置句、偷换主语、不必要的被动句、滥用"一个 xx" | 自行联网制定标准，避免语法错误和非地道汉语表述 |

3. **修改原则**：
   - 既有标题不宜修改，除非严重扭曲原意
   - 允许意译，但不得扭曲原意
   - 禁止篡改代码块、版本号、用户名、URL、IP 地址、带圈数字
   - 禁止机械替换、批量修改，必须逐个手动修改
   - 修改前后复核确认问题真实存在且改动准确
   - 不要修改 `# 标题`——会被 `sync-headers.yml` CI 覆盖
   - 添加新内容时，确保翻译风格与上下文一致

4. **工作流**：比较一章，修复一章，复核一章，继续下一章。

5. **三轮 + 一轮复查递归**（核心约束）：
   - **逐行逐句子** 遍历内容，检查逻辑一致性，联网复核后修改
   - 完整执行三轮逐句校对，然后严格、完整地复查一轮；若仍有问题，继续执行三轮，递归直至无问题
   - **逐个修改**：修改时禁止机械修改、禁止批量；必须逐个手动修改，禁止使用软件工具批量替换或批量逐个复核
   - **修改前后复核**：每次修改前确认问题真实存在、修改后确认改动准确且未引入新错误
   - **不复查旧错**：不得复查以前已经完成三轮的错误；每轮查询内容必须是新的（若与之前的复查重复则跳过、不改，只看是否有新增内容）
   - **联网复查**：对于失效链接、版本号、API 端点等实际访问查询，需联网复查三次后修改
   - **禁止绕过审查**：不得以任何方式搜索、批量、绕过逐句子审查流程

## 发行版文档补全工作流

当某个发行版的文档集不完整（缺少 announce、installation、hardware、readme、errata、signatures、schedule 等）时，按本工作流处理。

### 1. 确定缺失文档

对照 `en/` 文件夹下对应发行版目录（如 `en/14.4R/`），检查该目录下有哪些 adoc 文件，与中文版已有 `.md` 文件对比，确定缺失的文档类型。

每个发行版可能包含的文档类型：

- `_index.adoc` → 索引页（通常不单独翻译，内容并入父级章节）
- `announce.adoc` → 发行公告
- `relnotes.adoc` → 发行说明（通常已有翻译）
- `installation.adoc` → 安装说明
- `hardware.adoc` → 硬件兼容列表
- `readme.adoc` → 自述文件
- `errata.adoc` → 勘误
- `signatures.adoc` → 签名校验文件
- `schedule.adoc` → 发布计划
- `upgrading.adoc` → 升级说明（如 15.1R）
- 其他特殊文件（`todo.adoc`、`pressrelease.adoc`、`approvals.adoc`、`relnotes-detailed.adoc`）视原版存在情况补译

### 2. 补译缺失文档

- 文件命名：`<版本>-<文档类型>.md`（如 `14.4-announce.md`、`14.4-installation.md`）
- 多架构发行版：`<版本>-<架构>-<文档类型>.md`（如 `6.4-amd64-installation.md`）
- 翻译时遵循术语规范，第二人称用"你"，`Ports`/`Jail` 保留英文
- 每个新增文件首行 `# 标题` 由 `sync-headers.yml` CI 从 `SUMMARY.md` 同步，**不要手动编辑 H1**
- 在 `SUMMARY.md` 对应父级章节下插入新文档条目（保持 `* [标题](路径)` 格式）

### 3. 多架构补齐

对于早期发行版（4.x-6.x），英文原版为每个架构提供独立的 `relnotes-<arch>.adoc`、`installation-<arch>.adoc`、`hardware-<arch>.adoc` 文件。需补齐所有架构的翻译：

- 架构包括：amd64、i386、alpha、sparc64、powerpc、pc98、ia64、arm 等（视原版存在情况）
- 文件命名遵循既有模式：`<版本>-<架构>.md`、`<版本>-<架构>-installation.md`、`<版本>-<架构>-hardware.md`

### 4. 重组 SUMMARY.md 结构

将扁平的 `* [标题](路径)` 列表重组为按发行版分组的嵌套结构：

- 每个发行版作为父级章节（无链接的 GitBook 分类标签），命名为 `FreeBSD <版本>-RELEASE`
- 父级章节下列出该发行版的所有文档子项
- 既有文件的 SUMMARY.md 条目文本保持不变（以保留 H1 不被 CI 覆盖）
- 新增文档按以下顺序排列：发行说明（relnotes）→ 发行公告（announce）→ 安装说明（installation）→ 硬件兼容列表（hardware）→ 自述文件（readme）→ 勘误（errata）→ 签名校验文件（signatures）→ 发布计划（schedule）

## Lint 配置

- **markdownlint**（`.github/.markdownlint.json`）：本地已安装 `markdownlint-cli2 v0.22.1`（基于 `markdownlint v0.40.0`），可在本地直接运行检查与修复
  - **本地运行命令**（在仓库根目录执行）：

    ```sh
    # 检查全部中文 .md（排除 en/、.github/、node_modules/、script/）
    markdownlint-cli2 "**/*.md" "!en/**" "!.github/**" "!node_modules/**" "!script/**" --config .github/.markdownlint.json

    # 自动修复可修复的问题（MD012 多余空行、MD047 末尾换行、MD034 裸 URL 等）
    markdownlint-cli2 "**/*.md" "!en/**" "!.github/**" "!node_modules/**" "!script/**" --config .github/.markdownlint.json --fix
    ```

  - **MD060 表格列风格规则（重要）**：配置为 `"style": "compact"` + `"aligned_delimiter": true`
    - **compact 风格**：管道符两侧各保留 **单个空格**，例如 `| cell1 | cell2 |`；空单元格写作 `| |`（不是 `||` 或 `|  |`）
    - **aligned_delimiter**：分隔行 `|---|` 的管道符位置必须与表头行的管道符位置对齐
    - **CJK 显示宽度**：markdownlint 按 **显示宽度** 计算列位置，**每个中文字符按 2 宽度** 计算（与英文 1 宽度不同）。因此含 CJK 的列宽 = CJK 字符数 × 2 + ASCII 字符数 × 1
    - **分隔行 dash 数量公式**：若某列内容显示宽度为 W，则分隔行该列总宽（含两侧空格）也应为 W，dash 数量 = W − 4（减去前后各 1 空格 + 前后各 1 冒号）。例如列内容 `FreeBSD 版本` 显示宽度 = 7+1+4 = 12，分隔行应为 ` :--------: `（8 个 dash）
    - **常见错误修复**：当 markdownlint 报 `MD060/table-column-style [Table pipe does not align with header for option "aligned_delimiter"]` 时，需手动扩展分隔行 dash 数量，使管道符位置与表头按显示宽度对齐；`--fix` 无法自动修复此类问题
  - **MD056 表格列数规则**：表头声明几列，所有数据行都必须有几列；末尾缺空单元格时需补 `| |`，而非省略管道符
- **lychee**（`.github/lychee.toml`）：6 线程、30 并发、30 秒超时、最多 3 次重试、Chrome UA、排除私有 IP 和 `ftp.freebsd.org`

## 其他注意事项

- **文件编码**：统一使用 UTF-8 但禁止使用 BOM 标记，换行符统一 LF
- **临时文件**：任何临时文件或脚本均放置在 `script/` 目录下，执行完成后不需要清理，保持原样即可
- **PowerShell 限制**：当想使用 PowerShell 时，尽量转成 Python 脚本
- **AI 不可见字符**：AI 生成文本可能夹带零宽字符（U+200B/200C/200D、U+2060）、BOM（U+FEFF）、双向标记（U+200E/200F、U+202A–202E、U+2066–2069）、Tag 块（U+E0000–E007F，疑似 LLM 水印）、变体选择符（U+FE00–FE0F、U+E0100–E01EF）、软连字符（U+00AD）、不换行空格（U+00A0）等不可见字符，会破坏搜索、字符串匹配与渲染。校对或新增内容时如怀疑混入此类字符，可运行检测脚本 `script/detect_invisible_chars.py`（基于 `unicodedata` 通用类别 + 可疑码点区间判定，排除 `en/`、`.github/`、`node_modules/`、`script/`）。**注意：** 检测会报出大量 U+0009（Tab），这是 Markdown 嵌套列表的合法缩进（如 hardware 文件中的 `*\tAdaptec`），**不得删除**，否则会破坏列表层级；真正的 AI 不可见字符才需清理。截至最近一次全量扫描（570 个 `.md` 文件，Python 扫描 + grep PCRE + 字节级核验三重验证），全书 AI 不可见字符数为 0。

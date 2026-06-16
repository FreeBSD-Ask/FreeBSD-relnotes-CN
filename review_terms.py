#!/usr/bin/env python3
"""审阅 FreeBSD 发行说明中文翻译术语一致性 - 增强版"""

import re
import os

BASE_DIR = r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN"

VERSIONS = ["9.3", "9.2", "9.1", "9.0", "8.4", "8.3", "8.2", "8.1", "8.0", "7.4", "7.3", "7.2", "7.1", "7.0"]

results = {}

for ver in VERSIONS:
    filepath = os.path.join(BASE_DIR, f"{ver}.md")
    if not os.path.exists(filepath):
        results[ver] = {"status": "文件不存在", "issues": []}
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.split("\n")

    issues = []
    in_code_block = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Track code blocks
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Helper: remove backtick content for analysis
        def no_code(s):
            return re.sub(r'`[^`]*`', '', s)

        # Helper: remove man page references
        def no_man(s):
            return re.sub(r'\b\w+\(\d+\)', '', s)

        # Helper: remove URLs
        def no_url(s):
            return re.sub(r'https?://\S+', '', s)

        clean = no_url(no_man(no_code(stripped)))

        # ============================================================
        # 1. "base system" → 中文应翻译为"基本系统"
        # ============================================================
        # Check if "base system" appears untranslated in Chinese text
        if re.search(r'\bbase\s+system\b', clean, re.IGNORECASE):
            issues.append((i, f'英文"base system"未翻译 → 应为"基本系统": {stripped[:120]}'))

        # Check for wrong translations
        if "基础系统" in line:
            issues.append((i, f'"基础系统" → 应为"基本系统": {stripped[:120]}'))
        if "基本体系" in line:
            issues.append((i, f'"基本体系" → 应为"基本系统": {stripped[:120]}'))

        # ============================================================
        # 2. "Jails"/"jails" → 中文应翻译为"Jail"（首字母大写，单数）
        #    但命令名/参数名/路径中的jail保持小写
        # ============================================================
        # Check for "jails" (plural) in Chinese prose (not code/commands)
        # Remove sysctl paths, man refs, and code first
        check = no_url(no_man(no_code(stripped)))
        # Remove sysctl-like paths (security.jail.*, etc.)
        check = re.sub(r'[\w.]+\.[\w.]+', '', check)
        # Remove /jails/ paths
        check = re.sub(r'/jails\b', '', check)

        # Look for "jails" as a standalone word in prose
        if re.search(r'\bjails\b', check, re.IGNORECASE):
            # Check it's not in a command context like "show jails"
            # If the line has "show jails" in backticks, it's ok
            if "show jails" not in stripped:
                issues.append((i, f'"jails" → 应为"Jail"（单数，首字母大写）: {stripped[:120]}'))

        # Check for "Jails" with capital J but plural (in prose, not code)
        if re.search(r'\bJails\b', check):
            issues.append((i, f'"Jails" → 应为"Jail"（单数形式）: {stripped[:120]}'))

        # Check for wrong Chinese translations
        if "监狱" in line:
            issues.append((i, f'"监狱" → 应为"Jail"（FreeBSD 术语不翻译）: {stripped[:120]}'))

        # ============================================================
        # 3. "Bhyve"/"bhyve" → 中文应保持原文"bhyve"（小写）
        # ============================================================
        if re.search(r'\bBhyve\b', clean):
            issues.append((i, f'"Bhyve" → 应为"bhyve"（小写）: {stripped[:120]}'))
        if re.search(r'\bBHYVE\b', clean):
            issues.append((i, f'"BHYVE" → 应为"bhyve"（小写）: {stripped[:120]}'))

        # ============================================================
        # 4. "FreeBSD Foundation" → 中文应翻译为"FreeBSD 基金会"
        # ============================================================
        # Check for untranslated "FreeBSD Foundation"
        if re.search(r'\bFreeBSD\s+Foundation\b', clean, re.IGNORECASE):
            # Check if it's "FreeBSD 基金会" (correct) or still English
            if "FreeBSD 基金会" not in line and "FreeBSD基金会" not in line:
                issues.append((i, f'"FreeBSD Foundation"未翻译 → 应为"FreeBSD 基金会": {stripped[:120]}'))

        # Check for "FreeBSD基金会" without space
        if "FreeBSD基金会" in line:
            issues.append((i, f'"FreeBSD基金会" → 应为"FreeBSD 基金会"（中间有空格）: {stripped[:120]}'))

        # Check for "FreeBSD基金" without "会"
        if re.search(r'FreeBSD基金(?!会)', line):
            issues.append((i, f'"FreeBSD基金" → 应为"FreeBSD 基金会": {stripped[:120]}'))

        # ============================================================
        # 5. "Ports"/"Port" → 中文应保持原文不翻译（大写P）
        #    指Ports Collection时用"Ports"，指单个port时用"Port"
        #    ports在路径中（如/usr/ports）保持小写
        # ============================================================
        # Check for "port/包" (lowercase p)
        if re.search(r'\bport/包\b', line) or re.search(r'\bport／包\b', line):
            issues.append((i, f'"port/包" → 应为"Port/包"（大写 P）: {stripped[:120]}'))

        # Check for "ports/包" (lowercase p)
        if re.search(r'\bports/包\b', line) or re.search(r'\bports／包\b', line):
            issues.append((i, f'"ports/包" → 应为"Ports/包"（大写 P）: {stripped[:120]}'))

        # Check for "ports" used as Ports Collection term in prose (lowercase)
        # This is tricky - need to exclude paths like /usr/ports, ports/Mk
        check_ports = no_url(no_man(no_code(stripped)))
        check_ports = re.sub(r'/usr/ports\S*', '', check_ports)
        check_ports = re.sub(r'ports/\w+', '', check_ports)
        # Remove "ports-mgmt" and similar port category paths
        check_ports = re.sub(r'ports-\w+', '', check_ports)

        # Look for standalone "ports" that refers to Ports Collection
        # Pattern: "主要 ports" or "ports 和" or "ports 中" etc.
        if re.search(r'[\u4e00-\u9fff]ports\b', check_ports):
            # Chinese char followed by "ports" - likely should be "Ports"
            issues.append((i, f'"ports"（Ports Collection 语境）→ 应为"Ports"（大写 P）: {stripped[:120]}'))

        # Also check for "Port" at start of section headers or list items
        # that should be capitalized

        # Check for "端口" used to translate "Port" in Ports Collection context
        if "端口" in line:
            ports_context = re.search(r'端口.*(Collection|集合|树|安装|软件|包|编译)', line)
            if ports_context:
                issues.append((i, f'"端口"在 Ports 语境中 → 应为"Port": {stripped[:120]}'))

    results[ver] = {"status": "已审阅", "issues": issues}

# Print report
print("=" * 80)
print("FreeBSD 发行说明中文翻译术语一致性审阅报告")
print("=" * 80)
print()
print("审阅规则:")
print('  1. "base system" → "基本系统"')
print('  2. "Jails"/"jails" → "Jail"（首字母大写，单数；命令/参数/路径中保持小写）')
print('  3. "Bhyve"/"bhyve" → "bhyve"（小写）')
print('  4. "FreeBSD Foundation" → "FreeBSD 基金会"')
print('  5. "Ports"/"Port" → 保持原文不翻译（大写 P；路径中保持小写）')
print()

total_issues = 0
for ver in VERSIONS:
    r = results[ver]
    print(f"## {ver}.md")
    if r["status"] != "已审阅":
        print(f"  状态: {r['status']}")
    elif not r["issues"]:
        print("  全部合规")
    else:
        total_issues += len(r["issues"])
        for line_no, desc in r["issues"]:
            print(f"  行 {line_no}: {desc}")
    print()

print("=" * 80)
print(f"总计: {total_issues} 个术语不一致问题")

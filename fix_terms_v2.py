#!/usr/bin/env python3
"""修复所有 Markdown 文件中的术语不一致问题 v2"""

import os
import re
from pathlib import Path

BASE_DIR = Path(r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN")
EXCLUDE = {"SUMMARY.md", "README.md", "CHANGELOG.md"}

def fix_file(filepath):
    """修复单个文件中的术语"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes = []

    # 1. "发布说明" → "发行说明"
    count = content.count("发布说明")
    if count > 0:
        content = content.replace("发布说明", "发行说明")
        changes.append(f"发布说明→发行说明 ({count}处)")

    # 2. "启动加载器" → "引导加载程序" (不匹配"启动加载程序")
    count = content.count("启动加载器")
    if count > 0:
        content = content.replace("启动加载器", "引导加载程序")
        changes.append(f"启动加载器→引导加载程序 ({count}处)")

    # 3. "引导加载器" → "引导加载程序"
    count = content.count("引导加载器")
    if count > 0:
        content = content.replace("引导加载器", "引导加载程序")
        changes.append(f"引导加载器→引导加载程序 ({count}处)")

    # 4. "启动加载程序" → "引导加载程序"
    count = content.count("启动加载程序")
    if count > 0:
        content = content.replace("启动加载程序", "引导加载程序")
        changes.append(f"启动加载程序→引导加载程序 ({count}处)")

    # 5. "发布版" → "发行版" (但跳过"预发布版"和"发布版本")
    # 先保护"预发布版"和"发布版本"
    content = content.replace("预发布版", "___PRE_RELEASE___")
    content = content.replace("发布版本", "___RELEASE_VERSION___")
    count = content.count("发布版")
    if count > 0:
        content = content.replace("发布版", "发行版")
        changes.append(f"发布版→发行版 ({count}处)")
    # 恢复保护的内容
    content = content.replace("___PRE_RELEASE___", "预发布版")
    content = content.replace("___RELEASE_VERSION___", "发布版本")

    if content != original:
        with open(filepath, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        return changes
    return None


def main():
    total_files = 0
    for filepath in sorted(BASE_DIR.glob("*.md")):
        if filepath.name in EXCLUDE:
            continue
        changes = fix_file(filepath)
        if changes:
            print(f"{filepath.name}: {', '.join(changes)}")
            total_files += 1

    print(f"\n共修改了 {total_files} 个文件")


if __name__ == "__main__":
    main()
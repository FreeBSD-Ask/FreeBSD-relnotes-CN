#!/usr/bin/env python3
"""全面扫描所有 Markdown 文件中的术语翻译不一致情况 v2"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN")
EXCLUDE = {"SUMMARY.md", "README.md", "CHANGELOG.md"}

# 术语检查规则：(pattern, 术语名, 期望/建议, 类别)
# 只检查明确有问题的术语，避免过度匹配
TERM_RULES = [
    # ===== Taiwan/大陆用语对照（明确有问题的） =====
    (r'档案系统', '档案系统', '应改为"文件系统"', '两岸用语'),
    (r'守护程序', '守护程序', '应改为"守护进程"', '两岸用语'),
    (r'伺服器', '伺服器', '应改为"服务器"', '两岸用语'),
    (r'记忆体', '记忆体', '应改为"内存"', '两岸用语'),
    (r'硬体', '硬体', '应改为"硬件"', '两岸用语'),
    (r'网路', '网路', '应改为"网络"', '两岸用语'),
    (r'资料夹', '资料夹', '应改为"目录"', '两岸用语'),
    (r'伫列', '伫列', '应改为"队列"', '两岸用语'),
    (r'韧体', '韧体', '应改为"固件"', '两岸用语'),
    (r'执行绪', '执行绪', '应改为"线程"', '两岸用语'),
    (r'函式库', '函式库', '应改为"库"', '两岸用语'),
    (r'汇流排', '汇流排', '应改为"总线"', '两岸用语'),
    (r'快取', '快取', '应改为"缓存"', '两岸用语'),
    (r'暂存器', '暂存器', '应改为"寄存器"', '两岸用语'),
    (r'号志', '号志', '应改为"信号量"', '两岸用语'),
    (r'管线', '管线', '应改为"管道"', '两岸用语'),
    (r'组态', '组态', '应改为"配置"', '两岸用语'),
    (r'介面', '介面', '应改为"接口"/"界面"', '两岸用语'),

    # ===== boot loader 变体（统一为"引导加载程序"）=====
    (r'启动加载程序', 'boot loader', '统一为"引导加载程序"', 'boot loader'),
    (r'启动加载器', 'boot loader', '统一为"引导加载程序"', 'boot loader'),
    (r'引导加载器', 'boot loader', '统一为"引导加载程序"', 'boot loader'),

    # ===== 发行版/发布版 =====
    (r'发布版(?!本)', 'release', '应统一为"发行版"', 'release'),

    # ===== 发行说明/发布说明 =====
    (r'发布说明', 'release notes', '应统一为"发行说明"', 'release notes'),
]


def scan_file(filepath):
    """扫描单个文件"""
    issues = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split("\n")
    except Exception as e:
        return issues

    # 标记代码块范围，避免扫描代码块内部
    in_code_block = False
    for line_idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        for pattern, term_name, suggestion, category in TERM_RULES:
            for m in re.finditer(pattern, line):
                matched = m.group(0)
                issues.append({
                    "file": str(filepath.relative_to(BASE_DIR)),
                    "line": line_idx,
                    "matched": matched,
                    "term": term_name,
                    "suggestion": suggestion,
                    "category": category,
                    "context": stripped[:150],
                })
    return issues


def main():
    all_issues = []
    stats = defaultdict(lambda: defaultdict(int))

    for filepath in sorted(BASE_DIR.glob("*.md")):
        if filepath.name in EXCLUDE:
            continue
        issues = scan_file(filepath)
        all_issues.extend(issues)
        for issue in issues:
            stats[issue["category"]][issue["term"]] += 1

    # 按类别统计
    print("=" * 60)
    print("术语不一致统计（按类别）")
    print("=" * 60)
    for category in sorted(stats.keys()):
        print(f"\n--- {category} ---")
        for term, count in sorted(stats[category].items(), key=lambda x: -x[1]):
            print(f"  {term}: {count} 处")

    print(f"\n{'=' * 60}")
    print(f"总计: {len(all_issues)} 个术语问题")
    print("=" * 60)

    # 按文件分组输出
    print("\n\n按文件分组详情：")
    print("=" * 60)
    current_file = None
    for issue in sorted(all_issues, key=lambda x: (x["file"], x["line"])):
        if issue["file"] != current_file:
            current_file = issue["file"]
            print(f"\n--- {current_file} ---")
        print(f"  L{issue['line']:>4d} [{issue['category']}] {issue['term']}: '{issue['matched']}'")
        print(f"         → {issue['suggestion']}")
        print(f"         上下文: {issue['context']}")

    # 保存 JSON
    output_path = BASE_DIR / "term_issues_v2.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_issues, f, ensure_ascii=False, indent=2)
    print(f"\n详细结果已保存到 {output_path}")


if __name__ == "__main__":
    main()
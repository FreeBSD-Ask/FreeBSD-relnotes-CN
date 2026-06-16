#!/usr/bin/env python3
"""全面扫描所有 Markdown 文件中的术语不一致 - 最终版"""

import os, re, json
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN")
EXCLUDE = {"SUMMARY.md", "README.md", "CHANGELOG.md"}

# 所有需要检查的术语规则
TERM_RULES = [
    # 两岸用语
    (r'档案系统', '档案系统', '"文件系统"'),
    (r'守护程序', '守护程序', '"守护进程"'),
    (r'伺服器', '伺服器', '"服务器"'),
    (r'记忆体', '记忆体', '"内存"'),
    (r'硬体', '硬体', '"硬件"'),
    (r'网路', '网路', '"网络"'),
    (r'资料夹', '资料夹', '"目录"'),
    (r'伫列', '伫列', '"队列"'),
    (r'韧体', '韧体', '"固件"'),
    (r'执行绪', '执行绪', '"线程"'),
    (r'函式库', '函式库', '"库"'),
    (r'汇流排', '汇流排', '"总线"'),
    (r'快取', '快取', '"缓存"'),
    (r'暂存器', '暂存器', '"寄存器"'),
    (r'号志', '号志', '"信号量"'),
    (r'管线', '管线', '"管道"'),
    (r'组态', '组态', '"配置"'),
    (r'介面', '介面', '"接口"/"界面"'),
    (r'磁碟', '磁碟', '"磁盘"'),
    (r'堆叠', '堆叠', '"栈"'),
    (r'变数', '变数', '"变量"'),
    (r'执行档', '执行档', '"可执行文件"'),
    (r'软体', '软体', '"软件"'),
    (r'资料(?![夹库])', '资料', '"数据"'),
    (r'档案(?![馆案])', '档案', '"文件"'),
    (r'指令(?!集|行)', '指令', '"命令"'),
    (r'连结', '连结', '"链接"'),
    (r'支援', '支援', '"支持"'),
    (r'存取', '存取', '"访问"'),
    (r'资讯', '资讯', '"信息"'),
    (r'程式(?![员])', '程式', '"程序"'),

    # boot loader 变体
    (r'启动加载器', 'boot loader', '"引导加载程序"'),
    (r'引导加载器', 'boot loader', '"引导加载程序"'),
    (r'启动加载程序', 'boot loader', '"引导加载程序"'),

    # 发布说明/发行说明
    (r'发布说明', 'release notes', '"发行说明"'),

    # 发布版/发行版
    (r'发布版(?!本)', 'release', '"发行版"'),

    # 基系统/基本系统
    (r'基系统', 'base system', '"基本系统"'),

    # 奈飞
    (r'奈飞', 'Netflix', 'Netflix'),

    # 预设
    (r'预设(?:显示|的|值|情况|状态|行为|模式|路径|配置|选项|参数|设置)', 'default', '"默认"'),

    # 缺省
    (r'缺省', 'default', '"默认"'),
]


def scan_file(filepath):
    issues = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        return issues

    in_code = False
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for pat, term, suggestion in TERM_RULES:
            for m in re.finditer(pat, line):
                issues.append({
                    "file": str(filepath.relative_to(BASE_DIR)),
                    "line": i,
                    "matched": m.group(),
                    "term": term,
                    "suggestion": suggestion,
                    "context": s[:120],
                })
    return issues


def main():
    all_issues = []
    stats = defaultdict(int)

    for fp in sorted(BASE_DIR.glob("*.md")):
        if fp.name in EXCLUDE:
            continue
        issues = scan_file(fp)
        if issues:
            all_issues.extend(issues)
            for issue in issues:
                stats[issue["term"]] += 1

    if not all_issues:
        print("未发现任何术语问题，所有文件已统一。")
        return

    print(f"发现 {len(all_issues)} 个术语问题：\n")
    for term, count in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {term}: {count} 处")

    print(f"\n按文件分组：")
    current = None
    for issue in sorted(all_issues, key=lambda x: (x["file"], x["line"])):
        if issue["file"] != current:
            current = issue["file"]
            print(f"\n== {current} ==")
        print(f"  L{issue['line']:>4d}: {issue['matched']!r} -> {issue['suggestion']}")
        print(f"         {issue['context']}")

    # 保存
    out = BASE_DIR / "term_issues_final.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(all_issues, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存到 {out}")


if __name__ == "__main__":
    main()
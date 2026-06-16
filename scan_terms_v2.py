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
# 使用 regex 捕获组匹配，注意不要捕获代码块和 man 引用中的内容
TERM_RULES = [
    # ===== Taiwan/大陆用语对照 =====
    (r'档案系统', '档案系统', '应改为"文件系统"', '两岸用语'),
    (r'守护程序', '守护程序', '应改为"守护进程"', '两岸用语'),
    (r'伺服器', '伺服器', '应改为"服务器"', '两岸用语'),
    (r'记忆体', '记忆体', '应改为"内存"', '两岸用语'),
    (r'磁碟(?!机)', '磁碟', '应改为"磁盘"', '两岸用语'),
    (r'硬体(?!件)', '硬体', '应改为"硬件"', '两岸用语'),
    (r'网路', '网路', '应改为"网络"', '两岸用语'),
    (r'资料夹', '资料夹', '应改为"目录"', '两岸用语'),
    (r'变数', '变数', '应改为"变量"', '两岸用语'),
    (r'伫列', '伫列', '应改为"队列"', '两岸用语'),
    (r'堆叠', '堆叠', '应改为"栈"', '两岸用语'),
    (r'号志', '号志', '应改为"信号量"', '两岸用语'),
    (r'管线', '管线', '应改为"管道"', '两岸用语'),
    (r'韧体', '韧体', '应改为"固件"', '两岸用语'),
    (r'执行绪', '执行绪', '应改为"线程"', '两岸用语'),
    (r'执行档', '执行档', '应改为"可执行文件"', '两岸用语'),
    (r'函式库', '函式库', '应改为"库"', '两岸用语'),
    (r'组态', '组态', '应改为"配置"', '两岸用语'),
    (r'汇流排', '汇流排', '应改为"总线"', '两岸用语'),
    (r'快取', '快取', '应改为"缓存"', '两岸用语'),
    (r'暂存器', '暂存器', '应改为"寄存器"', '两岸用语'),
    (r'连结(?![埠器])', '连结', '应改为"链接"', '两岸用语'),
    (r'支援', '支援', '应改为"支持"', '两岸用语'),
    (r'存取', '存取', '应改为"访问"', '两岸用语'),
    (r'线上(?!更)', '线上', '应改为"在线"', '两岸用语'),
    (r'资讯(?!安)', '资讯', '应改为"信息"', '两岸用语'),
    (r'程式(?!员)', '程式', '应改为"程序"', '两岸用语'),
    (r'资料(?!夹|库)', '资料', '应改为"数据"', '两岸用语'),
    (r'档案(?!馆|案)', '档案', '应改为"文件"', '两岸用语'),
    (r'指令(?!集|行)', '指令', '应改为"命令"', '两岸用语'),
    (r'介面', '介面', '应改为"接口"/"界面"', '两岸用语'),

    # ===== boot loader 变体 =====
    (r'启动加载程序', 'boot loader', '统一为"引导加载程序"', 'boot loader'),
    (r'启动加载器', 'boot loader', '统一为"引导加载程序"', 'boot loader'),
    (r'引导加载器', 'boot loader', '统一为"引导加载程序"', 'boot loader'),

    # ===== userland 变体 =====
    (r'用户空间', 'userland', '确认是否统一为"用户态"', 'userland'),
    (r'用户环境', 'userland', '确认是否统一为"用户态"', 'userland'),

    # ===== 专有名词不应翻译 =====
    (r'ZFS\s*文件系统', 'ZFS', 'ZFS不翻译，建议用"ZFS 文件系统"', '专有名词'),
    (r'Btrfs\s*文件系统', 'Btrfs', 'Btrfs不翻译，建议用"Btrfs 文件系统"', '专有名词'),
    (r'DTrace\s*追踪', 'DTrace', 'DTrace不翻译', '专有名词'),
    (r'NUMA\s*架构', 'NUMA', 'NUMA不翻译', '专有名词'),

    # ===== 发行版/发布版 =====
    (r'发布版(?!本)', 'release', '应统一为"发行版"', 'release'),
    (r'RELEASE\s*版本', 'RELEASE', '确认是否可简化为"RELEASE"', 'release'),

    # ===== 核心/内核（kernel vs core） =====
    (r'(?<![a-zA-Z])核心(?!团队|成员|部分|架构|数|的|是|上|中|之|内|外|地|性|设|想|概|观|价|技|任|业|功|能|服|产|品|商|标|竞|争|优|先|级|网|安|全|概|念|定|义|组|件|模|块|驱|动|程|序|代|码|文|件|库|目|录|系|统|层|次|架|构|服|务|器|协|议|算|法|数|据|结|构|策|略|模|式|框|架|工|具|实|用|程|序|命|令|配|置|选|项|参|数|设|置|值|内|存|磁|盘|网|络|硬|件|软|件|缓|存|总|线|寄|存|器|栈|队|列|管|道|信|号|量|锁|互|斥|体|条|件|变|量|线|程|进|程|守|护|进|程|套|接|字|接|口|界|面|端|口|连|接|链|路|协|议|栈|安|全|加|密|解|密|签|名|验|证|授|权|认|证|审|计|日|志|监|控|调|试|测|试|部|署|发|布|版|本|更|新|升|级|迁|移|备|份|恢|复|故|障|冗|余|负|载|均|衡|性|能|优|化|扩|展|伸|缩|虚|拟|化|容|器|隔|离|沙|箱|编|译|构|建|链|接|加|载|执|行|运|行|启|动|停|止|重|启|关|闭|开|机|引|导|初|始|化|配|置|安|装|卸|载|格|式|化|分|区|挂|载|卸|载|文|件|系|统|目|录|路|径|权|限|用|户|组|角|色|策|略|模|式|框|架|工|具|实|用|程|序|命|令|配|置|选|项|参|数|设|置|值)', '核心', '确认指kernel还是core，kernel应译为"内核"', 'kernel'),

    # ===== 发行/发布 一致性 =====
    (r'发行注记', 'release notes', '确认是否统一为"发行说明"', 'release notes'),
    (r'发布说明', 'release notes', '确认是否统一为"发行说明"', 'release notes'),

    # ===== 命令/指令 一致性 =====
    (r'指令集', 'instruction set', '确认"指令集"是否应该保留（CPU指令集）', '指令'),
    (r'命令行', 'command line', '确认是否统一为"命令行"', '命令'),
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
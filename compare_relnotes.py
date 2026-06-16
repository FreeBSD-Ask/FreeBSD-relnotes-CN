#!/usr/bin/env python3
"""Compare FreeBSD release notes translations against original English sources."""

import re
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

VERSIONS = {
    "12.1": {
        "local": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\12.1.md",
        "remote": "https://raw.githubusercontent.com/freebsd/freebsd-doc/refs/heads/main/website/content/en/releases/12.1R/relnotes.adoc",
    },
    "12.2": {
        "local": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\12.2.md",
        "remote": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/12.2R/relnotes.adoc",
    },
    "12.3": {
        "local": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\12.3.md",
        "remote": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/12.3R/relnotes.adoc",
    },
    "12.4": {
        "local": r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN\12.4.md",
        "remote": "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/12.4R/relnotes.adoc",
    },
}

def fetch_url(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ctx) as resp:
        return resp.read().decode("utf-8")

def read_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def extract_sa_ids(text):
    """Extract SA IDs from text (both English adoc and Chinese md)."""
    # Match patterns like FreeBSD-SA-19:01.syscall or SA-19:01.syscall
    pattern = r'FreeBSD-SA-\d{2}:\d{2}\.\w+'
    return sorted(set(re.findall(pattern, text)))

def extract_en_ids(text):
    """Extract EN IDs from text (both English adoc and Chinese md)."""
    pattern = r'FreeBSD-EN-\d{2}:\d{2}\.\w+'
    return sorted(set(re.findall(pattern, text)))

def extract_sections_en(text):
    """Extract section headings from English adoc."""
    # == and === headings
    pattern = r'^(={2,3})\s+(.+)$'
    sections = []
    for m in re.finditer(pattern, text, re.MULTILINE):
        level = len(m.group(1))
        title = m.group(2).strip()
        # Skip the very first title line (document title)
        if level == 1 and 'Release Notes' in title:
            continue
        sections.append((level, title))
    return sections

def extract_sections_cn(text):
    """Extract section headings from Chinese md."""
    pattern = r'^(#{2,3})\s+(.+)$'
    sections = []
    for m in re.finditer(pattern, text, re.MULTILINE):
        level = len(m.group(1))
        title = m.group(2).strip()
        if level == 1 and '发行说明' in title:
            continue
        sections.append((level, title))
    return sections

def extract_code_blocks(text):
    """Count code blocks (backtick fenced or inline code)."""
    # Fenced code blocks
    fenced = len(re.findall(r'^```', text, re.MULTILINE))
    # Inline code (single backtick, not part of fenced)
    # This is approximate
    inline = len(re.findall(r'(?<!`)`(?!`)[^`]+(?<!`)`(?!`)', text))
    return fenced, inline

def compare_version(ver, info):
    print(f"\n{'='*70}")
    print(f"  FreeBSD {ver} 对比报告")
    print(f"{'='*70}")
    
    # Read local
    try:
        cn_text = read_file(info["local"])
    except FileNotFoundError:
        print(f"  [错误] 本地文件未找到: {info['local']}")
        return
    
    # Fetch remote
    try:
        en_text = fetch_url(info["remote"])
    except Exception as e:
        print(f"  [错误] 无法获取远程文件: {e}")
        return
    
    # --- SA comparison ---
    en_sas = extract_sa_ids(en_text)
    cn_sas = extract_sa_ids(cn_text)
    
    print(f"\n--- 安全公告 (SA) ---")
    print(f"  英文原文 SA 数量: {len(en_sas)}")
    print(f"  中文翻译 SA 数量: {len(cn_sas)}")
    
    missing_sas = [sa for sa in en_sas if sa not in cn_sas]
    extra_sas = [sa for sa in cn_sas if sa not in en_sas]
    
    if missing_sas:
        print(f"  [缺失] 以下 SA 在翻译中不存在:")
        for sa in missing_sas:
            print(f"    - {sa}")
    else:
        print(f"  [OK] 无缺失 SA 条目")
    
    if extra_sas:
        print(f"  [多余] 以下 SA 在翻译中存在但原文中不存在:")
        for sa in extra_sas:
            print(f"    - {sa}")
    
    # --- EN comparison ---
    en_ens = extract_en_ids(en_text)
    cn_ens = extract_en_ids(cn_text)
    
    print(f"\n--- 勘误通知 (EN) ---")
    print(f"  英文原文 EN 数量: {len(en_ens)}")
    print(f"  中文翻译 EN 数量: {len(cn_ens)}")
    
    missing_ens = [en for en in en_ens if en not in cn_ens]
    extra_ens = [en for en in cn_ens if en not in en_ens]
    
    if missing_ens:
        print(f"  [缺失] 以下 EN 在翻译中不存在:")
        for en in missing_ens:
            print(f"    - {en}")
    else:
        print(f"  [OK] 无缺失 EN 条目")
    
    if extra_ens:
        print(f"  [多余] 以下 EN 在翻译中存在但原文中不存在:")
        for en in extra_ens:
            print(f"    - {en}")
    
    # --- Section comparison ---
    en_sections = extract_sections_en(en_text)
    cn_sections = extract_sections_cn(cn_text)
    
    print(f"\n--- 章节结构 ---")
    print(f"  英文原文章节数: {len(en_sections)}")
    print(f"  中文翻译章节数: {len(cn_sections)}")
    
    # Map English section names to Chinese equivalents for comparison
    section_map = {
        "Abstract": "摘要",
        "Introduction": "引言",
        "Upgrading from Previous Releases of FreeBSD": "从旧版 FreeBSD 升级",
        "Security and Errata": "安全与勘误",
        "Security Advisories": "安全公告",
        "Errata Notices": "勘误通知",
        "Userland": "用户空间",
        "Userland Configuration Changes": "用户空间配置变更",
        "Userland Application Changes": "用户空间应用程序变更",
        "Contributed Software": "第三方软件",
        "Deprecated Applications": "弃用的应用程序",
        "Runtime Libraries and API": "运行时库和 API",
        "Kernel": "内核",
        "General Kernel Changes": "一般内核变化",
        "Devices and Drivers": "设备与驱动",
        "Device Drivers": "设备驱动程序",
        "Storage": "存储",
        "General Storage": "一般存储",
        "Boot Loader Changes": "启动加载器变化",
        "Networking": "网络",
        "General Networking": "一般网络",
        "Ports and Packages Infrastructure": "Ports 和包基础设施",
        "Package Changes": "软件包变化",
        "General Notes on Future FreeBSD Releases": "关于后续 FreeBSD 版本的一般说明",
        "General Notes on Future FreeBSD Releases": "关于后续 FreeBSD 版本的常规说明",
        "Default `CPUTYPE` Change": "默认 `CPUTYPE` 变更",
        "FreeBSD EC2 AMI Ids": "FreeBSD EC2 AMI Ids",
    }
    
    # Check for missing sections by comparing mapped names
    en_section_names = []
    for level, title in en_sections:
        # Clean up asciidoc markup
        clean_title = re.sub(r'\{.*?\}', '', title).strip()
        clean_title = re.sub(r'\[.*?\]', '', clean_title).strip()
        en_section_names.append((level, clean_title))
    
    cn_section_names = []
    for level, title in cn_sections:
        cn_section_names.append((level, title))
    
    # Check which English sections have no corresponding Chinese section
    missing_sections = []
    for level, title in en_section_names:
        found = False
        # Check if Chinese section matches by mapping or partial match
        for cn_level, cn_title in cn_section_names:
            if title in section_map and section_map[title] in cn_title:
                found = True
                break
            elif title.lower().replace(" ", "") in cn_title.lower().replace(" ", ""):
                found = True
                break
        if not found:
            missing_sections.append((level, title))
    
    if missing_sections:
        print(f"  [缺失] 以下章节在翻译中可能缺失:")
        for level, title in missing_sections:
            indent = "  " * (level - 2)
            print(f"    {indent}- {title}")
    else:
        print(f"  [OK] 所有章节均已翻译")
    
    # --- Code blocks ---
    en_fenced, en_inline = extract_code_blocks(en_text)
    cn_fenced, cn_inline = extract_code_blocks(cn_text)
    
    print(f"\n--- 代码块 ---")
    print(f"  英文原文: 围栏代码块 {en_fenced} 个, 行内代码 {en_inline} 处")
    print(f"  中文翻译: 围栏代码块 {cn_fenced} 个, 行内代码 {cn_inline} 处")
    
    # Check for specific code patterns in English that should be in Chinese
    # Look for `code` patterns in English
    en_code_patterns = re.findall(r'`([^`]+)`', en_text)
    # Filter to meaningful code (not just man page refs)
    meaningful_code = [c for c in en_code_patterns if not c.startswith('/') and len(c) > 3 and not re.match(r'^[A-Z][a-z]+$', c)]
    
    print(f"  英文原文中有意义的行内代码片段约 {len(meaningful_code)} 处")

# Run for all versions
for ver in ["12.1", "12.2", "12.3", "12.4"]:
    compare_version(ver, VERSIONS[ver])

#!/usr/bin/env python3
"""Download and compare FreeBSD release notes English sources with Chinese translations."""

import urllib.request
import json
import os
import time
import re
import sys

BASE_DIR = r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN"
TMP_DIR = os.path.join(BASE_DIR, "tmp_en")
os.makedirs(TMP_DIR, exist_ok=True)

# Mapping: local_file -> github_dir_name
VERSION_MAP = {
    "3.0": "3.0R",
    "3.1": "3.1R",
    "3.2": "3.2R",
    "3.3": "3.3R",
    "3.4": "3.4R",
    "3.5": "3.5R",
    "2.0": "2.0",
    "2.0.5": "2.0.5R",
    "2.1": "2.1R",
    "2.1.5": "2.1.5R",
    "2.1.6": "2.1.6R",
    "2.1.7": "2.1.7R",
    "2.2": "2.2R",
    "2.2.1": "2.2.1R",
    "2.2.2": "2.2.2R",
    "2.2.5": "2.2.5R",
    "2.2.6": "2.2.6R",
    "2.2.7": "2.2.7R",
    "2.2.8": "2.2.8R",
    "1.0": "1.0",
    "1.1": "1.1",
    "1.1.5": "1.1.5",
    "1.1.5.1": "1.1.5.1",
}

API_BASE = "https://api.github.com/repos/freebsd/freebsd-doc/contents/website/content/en/releases"
RAW_BASE = "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases"


def fetch_url(url, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            resp = urllib.request.urlopen(req, timeout=30)
            return resp.read()
        except Exception as e:
            if i < retries - 1:
                time.sleep(2)
            else:
                return None


def list_dir(dir_name):
    """List files in a GitHub directory."""
    url = f"{API_BASE}/{dir_name}"
    data = fetch_url(url)
    if data is None:
        return None
    try:
        items = json.loads(data)
        return [(item["name"], item["type"]) for item in items]
    except:
        return None


def find_relnotes_file(dir_name):
    """Find the relnotes file in a directory."""
    items = list_dir(dir_name)
    if items is None:
        return None

    # Priority: relnotes.adoc > RELNOTES.*.txt > any file with 'relnotes' or 'RELNOTES'
    for name, ftype in items:
        if ftype == "file" and name.lower() == "relnotes.adoc":
            return name

    for name, ftype in items:
        if ftype == "file" and "relnotes" in name.lower():
            return name

    # Check _index.adoc as Hugo content file
    for name, ftype in items:
        if ftype == "file" and name == "_index.adoc":
            return name

    return None


def download_file(dir_name, filename):
    """Download a file from GitHub."""
    url = f"{RAW_BASE}/{dir_name}/{filename}"
    data = fetch_url(url)
    return data


def extract_sections_adoc(text):
    """Extract section structure from asciidoc text."""
    if text is None:
        return []

    lines = text.decode("utf-8", errors="replace").split("\n")
    sections = []
    current_section = None
    current_content = []

    for line in lines:
        # Match asciidoc headings
        heading_match = re.match(r'^(={1,6})\s+(.+)$', line)
        if heading_match:
            if current_section is not None:
                sections.append((current_section, "\n".join(current_content).strip()))
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            current_section = (level, title)
            current_content = []
        else:
            current_content.append(line)

    if current_section is not None:
        sections.append((current_section, "\n".join(current_content).strip()))

    return sections


def extract_code_blocks(text):
    """Extract code blocks from text."""
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="replace")
    blocks = re.findall(r'----\n(.*?)\n----', text, re.DOTALL)
    return blocks


def extract_inline_code(text):
    """Extract inline code (backtick content) from text."""
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="replace")
    return re.findall(r'`([^`]+)`', text)


def count_paragraphs(text):
    """Count non-empty paragraphs (separated by blank lines)."""
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="replace")
    paras = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    return len(paras)


def compare_versions(version, en_data, cn_data):
    """Compare English and Chinese versions, return list of differences."""
    diffs = []

    if en_data is None:
        diffs.append("无法获取英文原文")
        return diffs

    if cn_data is None:
        diffs.append("中文翻译文件不存在")
        return diffs

    en_text = en_data.decode("utf-8", errors="replace") if isinstance(en_data, bytes) else en_data
    cn_text = cn_data.decode("utf-8", errors="replace") if isinstance(cn_data, bytes) else cn_data

    # Extract sections
    en_sections = extract_sections_adoc(en_text.encode())
    cn_sections = extract_sections_adoc(cn_text.encode())

    en_section_titles = [(s[0][0], s[0][1]) for s in en_sections]
    cn_section_titles = [(s[0][0], s[0][1]) for s in cn_sections]

    # Check for missing sections in Chinese
    # We need fuzzy matching since titles are translated
    # Instead, let's compare section counts and content structure

    # Count top-level sections
    en_top_sections = [s for s in en_sections if s[0][0] <= 2]
    cn_top_sections = [s for s in cn_sections if s[0][0] <= 2]

    if len(en_top_sections) != len(cn_top_sections):
        diffs.append(f"章节数量不匹配: 英文 {len(en_top_sections)} 个, 中文 {len(cn_top_sections)} 个")
        # List English section titles
        for level, title in en_section_titles:
            if level <= 2:
                diffs.append(f"  英文章节: {'=' * level} {title}")

    # Check code blocks
    en_code_blocks = extract_code_blocks(en_text)
    cn_code_blocks = extract_code_blocks(cn_text)

    if len(en_code_blocks) != len(cn_code_blocks):
        diffs.append(f"代码块数量不匹配: 英文 {len(en_code_blocks)} 个, 中文 {len(cn_code_blocks)} 个")
        for i, block in enumerate(en_code_blocks):
            # Check if this code block exists in Chinese
            # Code blocks should be identical (not translated)
            block_stripped = block.strip()
            found = False
            for cn_block in cn_code_blocks:
                if cn_block.strip() == block_stripped:
                    found = True
                    break
            if not found:
                first_line = block_stripped.split("\n")[0][:80]
                diffs.append(f"  英文代码块 #{i+1} 在中文中未找到: {first_line}...")

    # Check inline code
    en_inline = extract_inline_code(en_text)
    cn_inline = extract_inline_code(cn_text)

    # Inline code that should appear in both (commands, paths, etc.)
    missing_inline = []
    for code in en_inline:
        if code not in cn_text:
            missing_inline.append(code)

    if missing_inline:
        diffs.append(f"缺失的内联代码 (共 {len(missing_inline)} 个):")
        for code in missing_inline[:20]:  # Limit to first 20
            diffs.append(f"  `{code}`")
        if len(missing_inline) > 20:
            diffs.append(f"  ... 还有 {len(missing_inline) - 20} 个")

    # Check for specific content markers - URLs, security advisories
    en_urls = re.findall(r'https?://[^\s\[\]]+', en_text)
    cn_urls = re.findall(r'https?://[^\s\[\]]+', cn_text)

    missing_urls = []
    for url in en_urls:
        if url not in cn_text:
            missing_urls.append(url)

    if missing_urls:
        diffs.append(f"缺失的 URL (共 {len(missing_urls)} 个):")
        for url in missing_urls[:10]:
            diffs.append(f"  {url}")
        if len(missing_urls) > 10:
            diffs.append(f"  ... 还有 {len(missing_urls) - 10} 个")

    # Check for security advisories
    en_sa = re.findall(r'FreeBSD-SA-\d+:\d+', en_text)
    cn_sa = re.findall(r'FreeBSD-SA-\d+:\d+', cn_text)

    missing_sa = [sa for sa in en_sa if sa not in cn_text]
    if missing_sa:
        diffs.append(f"缺失的安全公告 (共 {len(missing_sa)} 个): {', '.join(missing_sa)}")

    # Paragraph count comparison per section
    for i, (section_info, content) in enumerate(en_sections):
        level, title = section_info
        en_para_count = count_paragraphs(content)
        # Find corresponding Chinese section
        # Try to match by position for same-level sections
        cn_matching = [s for s in cn_sections if s[0][0] == level]
        if i < len(cn_matching):
            cn_para_count = count_paragraphs(cn_matching[i][1])
            if en_para_count > cn_para_count + 2:  # Allow some tolerance
                diffs.append(f"章节 '{title}' 段落数可能不匹配: 英文约 {en_para_count} 段, 对应中文约 {cn_para_count} 段")

    return diffs


def main():
    results = {}

    print("=" * 60)
    print("FreeBSD 发行说明中英对比检查")
    print("=" * 60)

    for version, dir_name in sorted(VERSION_MAP.items(), key=lambda x: x[0], reverse=True):
        print(f"\n--- 处理版本 {version} (目录: {dir_name}) ---")

        # Find the relnotes file
        relnotes_file = find_relnotes_file(dir_name)
        if relnotes_file is None:
            print(f"  未找到发行说明文件!")
            results[version] = ["在 GitHub 仓库中未找到发行说明文件"]
            continue

        print(f"  发行说明文件: {relnotes_file}")

        # Download English source
        en_data = download_file(dir_name, relnotes_file)
        if en_data is None:
            print(f"  下载英文原文失败!")
            results[version] = ["下载英文原文失败"]
            continue

        # Save English source
        en_path = os.path.join(TMP_DIR, f"{version}.adoc")
        with open(en_path, "wb") as f:
            f.write(en_data)
        print(f"  英文原文已下载: {len(en_data)} bytes")

        # Read Chinese translation
        cn_path = os.path.join(BASE_DIR, f"{version}.md")
        if os.path.exists(cn_path):
            with open(cn_path, "r", encoding="utf-8") as f:
                cn_data = f.read()
            print(f"  中文翻译已读取: {len(cn_data)} bytes")
        else:
            cn_data = None
            print(f"  中文翻译文件不存在!")

        # Compare
        diffs = compare_versions(version, en_data, cn_data)
        results[version] = diffs

        if diffs:
            print(f"  发现 {len(diffs)} 个差异:")
            for d in diffs:
                print(f"    {d}")
        else:
            print(f"  未发现明显缺失")

        time.sleep(1)  # Rate limiting

    # Print summary
    print("\n" + "=" * 60)
    print("汇总报告")
    print("=" * 60)

    for version in sorted(results.keys(), reverse=True):
        diffs = results[version]
        if diffs:
            print(f"\n版本 {version}:")
            for d in diffs:
                print(f"  - {d}")
        else:
            print(f"\n版本 {version}: 无缺失")


if __name__ == "__main__":
    main()

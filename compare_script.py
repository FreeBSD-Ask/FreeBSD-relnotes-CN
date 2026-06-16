#!/usr/bin/env python3
"""Download and compare FreeBSD release notes English sources with Chinese translations."""

import urllib.request
import os
import time
import re

BASE_DIR = r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN"
TMP_DIR = os.path.join(BASE_DIR, "tmp_en")
os.makedirs(TMP_DIR, exist_ok=True)

RAW_BASE = "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases"

# Mapping: local_version -> (github_dir, filename)
VERSION_FILES = {
    "3.0": ("3.0R", "notes.adoc"),
    "3.1": ("3.1R", "notes.adoc"),
    "3.2": ("3.2R", "notes.adoc"),
    "3.3": ("3.3R", "notes.adoc"),
    "3.4": ("3.4R", "notes.adoc"),
    "3.5": ("3.5R", "notes.adoc"),
    "2.0": ("2.0", "notes.adoc"),
    "2.0.5": ("2.0.5R", "notes.adoc"),
    "2.1": ("2.1R", "notes.adoc"),
    "2.1.5": ("2.1.5R", "notes.adoc"),
    "2.1.6": ("2.1.6R", "notes.adoc"),
    "2.1.7": ("2.1.7R", "notes.adoc"),
    "2.2": ("2.2R", "notes.adoc"),
    "2.2.1": ("2.2.1R", "notes.adoc"),
    "2.2.2": ("2.2.2R", "notes.adoc"),
    "2.2.5": ("2.2.5R", "notes.adoc"),
    "2.2.6": ("2.2.6R", "notes.adoc"),
    "2.2.7": ("2.2.7R", "notes.adoc"),
    "2.2.8": ("2.2.8R", "notes.adoc"),
    "1.0": ("1.0", "announce.adoc"),  # Only announce.adoc exists
    "1.1": ("1.1", "RELNOTES.FreeBSD.txt"),
    "1.1.5": ("1.1.5", "RELNOTES.FreeBSD.txt"),
    "1.1.5.1": ("1.1.5.1", "WHATS_NEW-1.1.5.1.txt"),  # No RELNOTES file
}


def fetch_url(url, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            resp = urllib.request.urlopen(req, timeout=30)
            return resp.read()
        except Exception as e:
            if i < retries - 1:
                time.sleep(3)
            else:
                print(f"  Failed to fetch {url}: {e}")
                return None


def extract_sections(text):
    """Extract section structure from text (asciidoc or plain text)."""
    sections = []
    current_section = None
    current_content = []

    for line in text.split("\n"):
        # Asciidoc headings
        heading_match = re.match(r'^(={1,6})\s+(.+)$', line)
        # Markdown headings
        md_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        # Plain text headings (all caps lines or lines ending with colon)
        plain_match = re.match(r'^([A-Z][A-Z\s/]+)$', line)

        if heading_match:
            if current_section is not None:
                sections.append((current_section, "\n".join(current_content).strip()))
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            current_section = (level, title)
            current_content = []
        elif md_match:
            if current_section is not None:
                sections.append((current_section, "\n".join(current_content).strip()))
            level = len(md_match.group(1))
            title = md_match.group(2).strip()
            current_section = (level, title)
            current_content = []
        elif plain_match and len(line.strip()) > 5:
            if current_section is not None:
                sections.append((current_section, "\n".join(current_content).strip()))
            current_section = (2, line.strip())
            current_content = []
        else:
            current_content.append(line)

    if current_section is not None:
        sections.append((current_section, "\n".join(current_content).strip()))

    return sections


def extract_code_blocks(text):
    """Extract code blocks from text."""
    # Asciidoc style
    blocks = re.findall(r'----\n(.*?)\n----', text, re.DOTALL)
    # Markdown style
    blocks += re.findall(r'```\w*\n(.*?)\n```', text, re.DOTALL)
    # Indented code blocks (4+ spaces or tab)
    return blocks


def extract_inline_code(text):
    """Extract inline code (backtick content) from text."""
    return re.findall(r'`([^`\n]+)`', text)


def count_paragraphs(text):
    """Count non-empty paragraphs."""
    paras = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip() and not p.strip().startswith('=') and not p.strip().startswith('#')]
    return len(paras)


def compare_versions(version, en_text, cn_text):
    """Compare English and Chinese versions, return list of differences."""
    diffs = []

    if en_text is None:
        diffs.append("无法获取英文原文")
        return diffs

    if cn_text is None:
        diffs.append("中文翻译文件不存在")
        return diffs

    # Extract sections
    en_sections = extract_sections(en_text)
    cn_sections = extract_sections(cn_text)

    en_top_sections = [s for s in en_sections if s[0][0] <= 2]
    cn_top_sections = [s for s in cn_sections if s[0][0] <= 2]

    # Check code blocks
    en_code_blocks = extract_code_blocks(en_text)
    cn_code_blocks = extract_code_blocks(cn_text)

    if len(en_code_blocks) != len(cn_code_blocks):
        diffs.append(f"代码块数量不匹配: 英文 {len(en_code_blocks)} 个, 中文 {len(cn_code_blocks)} 个")
        for i, block in enumerate(en_code_blocks):
            block_stripped = block.strip()
            found = False
            for cn_block in cn_code_blocks:
                if cn_block.strip() == block_stripped:
                    found = True
                    break
            if not found:
                first_line = block_stripped.split("\n")[0][:80]
                diffs.append(f"  英文代码块 #{i+1} 在中文中未找到: {first_line}...")

    # Check inline code - technical terms that should be preserved
    en_inline = extract_inline_code(en_text)
    missing_inline = []
    for code in en_inline:
        # Skip very short or common words
        if len(code) <= 2:
            continue
        if code not in cn_text:
            missing_inline.append(code)

    if missing_inline:
        diffs.append(f"缺失的内联代码 (共 {len(missing_inline)} 个):")
        for code in missing_inline[:30]:
            diffs.append(f"  `{code}`")
        if len(missing_inline) > 30:
            diffs.append(f"  ... 还有 {len(missing_inline) - 30} 个")

    # Check for URLs
    en_urls = re.findall(r'https?://[^\s\[\]`\)]+', en_text)
    missing_urls = []
    for url in en_urls:
        if url not in cn_text:
            missing_urls.append(url)

    if missing_urls:
        diffs.append(f"缺失的 URL (共 {len(missing_urls)} 个):")
        for url in missing_urls[:15]:
            diffs.append(f"  {url}")
        if len(missing_urls) > 15:
            diffs.append(f"  ... 还有 {len(missing_urls) - 15} 个")

    # Check for security advisories
    en_sa = re.findall(r'FreeBSD-SA-\d+:\d+', en_text)
    cn_sa = re.findall(r'FreeBSD-SA-\d+:\d+', cn_text)

    missing_sa = [sa for sa in en_sa if sa not in cn_text]
    if missing_sa:
        diffs.append(f"缺失的安全公告 (共 {len(missing_sa)} 个): {', '.join(sorted(set(missing_sa)))}")

    # Check for FreeBSD-SA pattern variations
    en_sa2 = re.findall(r'SA-\d+:\d+', en_text)
    missing_sa2 = [sa for sa in en_sa2 if sa not in cn_text]
    if missing_sa2 and not missing_sa:  # Only report if not already reported
        diffs.append(f"缺失的安全公告引用 (共 {len(missing_sa2)} 个): {', '.join(sorted(set(missing_sa2)))}")

    # Section count comparison
    if len(en_top_sections) != len(cn_top_sections):
        diffs.append(f"顶级章节数量不匹配: 英文 {len(en_top_sections)} 个, 中文 {len(cn_top_sections)} 个")
        for level, title in [(s[0][0], s[0][1]) for s in en_top_sections]:
            diffs.append(f"  英文章节: {'=' * level} {title}")

    # Detailed section-by-section comparison
    # Match sections by position for same-level
    for i, (section_info, content) in enumerate(en_sections):
        level, title = section_info
        en_para_count = count_paragraphs(content)

        # Find matching Chinese section by position
        cn_matching = [s for s in cn_sections if s[0][0] == level]
        if i < len(cn_matching):
            cn_para_count = count_paragraphs(cn_matching[i][1])
            # If English has significantly more paragraphs, flag it
            if en_para_count > 3 and en_para_count > cn_para_count * 1.5 + 2:
                diffs.append(f"章节 '{title}' 段落数可能不匹配: 英文约 {en_para_count} 段, 对应中文约 {cn_para_count} 段")

    # Check for specific important content markers
    # Check for man page references
    en_man_refs = re.findall(r'\w+\(\d\)', en_text)
    cn_man_refs = re.findall(r'\w+\(\d\)', cn_text)
    missing_man = [ref for ref in en_man_refs if ref not in cn_text]
    if missing_man:
        unique_missing = sorted(set(missing_man))
        if len(unique_missing) > 3:
            diffs.append(f"缺失的手册页引用 (共 {len(unique_missing)} 个): {', '.join(unique_missing[:20])}")
            if len(unique_missing) > 20:
                diffs.append(f"  ... 还有 {len(unique_missing) - 20} 个")
        elif unique_missing:
            diffs.append(f"缺失的手册页引用: {', '.join(unique_missing)}")

    # Check for file paths
    en_paths = re.findall(r'/[a-zA-Z][a-zA-Z0-9_/.-]+', en_text)
    missing_paths = []
    for path in en_paths:
        if len(path) > 5 and path not in cn_text:
            missing_paths.append(path)
    if missing_paths:
        unique_paths = sorted(set(missing_paths))
        if len(unique_paths) > 5:
            diffs.append(f"缺失的文件路径 (共 {len(unique_paths)} 个):")
            for p in unique_paths[:20]:
                diffs.append(f"  {p}")
            if len(unique_paths) > 20:
                diffs.append(f"  ... 还有 {len(unique_paths) - 20} 个")
        elif unique_paths:
            diffs.append(f"缺失的文件路径: {', '.join(unique_paths)}")

    return diffs


def main():
    results = {}

    print("=" * 60)
    print("FreeBSD 发行说明中英对比检查")
    print("=" * 60)

    for version in sorted(VERSION_FILES.keys(), key=lambda x: list(map(int, re.findall(r'\d+', x))), reverse=True):
        dir_name, filename = VERSION_FILES[version]
        print(f"\n--- 处理版本 {version} (目录: {dir_name}, 文件: {filename}) ---")

        # Download English source
        url = f"{RAW_BASE}/{dir_name}/{filename}"
        en_data = fetch_url(url)
        if en_data is None:
            results[version] = ["下载英文原文失败"]
            continue

        # Save English source
        en_path = os.path.join(TMP_DIR, f"{version}.txt")
        with open(en_path, "wb") as f:
            f.write(en_data)

        en_text = en_data.decode("utf-8", errors="replace")
        print(f"  英文原文已下载: {len(en_data)} bytes")

        # Read Chinese translation
        cn_path = os.path.join(BASE_DIR, f"{version}.md")
        if os.path.exists(cn_path):
            with open(cn_path, "r", encoding="utf-8") as f:
                cn_text = f.read()
            print(f"  中文翻译已读取: {len(cn_text)} bytes")
        else:
            cn_text = None
            print(f"  中文翻译文件不存在!")

        # Compare
        diffs = compare_versions(version, en_text, cn_text)
        results[version] = diffs

        if diffs:
            print(f"  发现 {len(diffs)} 个差异:")
            for d in diffs:
                print(f"    {d}")
        else:
            print(f"  未发现明显缺失")

        time.sleep(1)

    # Print summary
    print("\n\n" + "=" * 60)
    print("汇总报告")
    print("=" * 60)

    has_issues = False
    for version in sorted(results.keys(), key=lambda x: list(map(int, re.findall(r'\d+', x))), reverse=True):
        diffs = results[version]
        if diffs:
            has_issues = True
            print(f"\n版本 {version}:")
            for d in diffs:
                print(f"  - {d}")

    if not has_issues:
        print("\n所有版本均未发现缺失内容!")

    # Save report to file
    report_path = os.path.join(BASE_DIR, "comparison_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("FreeBSD 发行说明中英对比检查报告\n")
        f.write("=" * 60 + "\n\n")
        for version in sorted(results.keys(), key=lambda x: list(map(int, re.findall(r'\d+', x))), reverse=True):
            diffs = results[version]
            if diffs:
                f.write(f"版本 {version}:\n")
                for d in diffs:
                    f.write(f"  - {d}\n")
                f.write("\n")

    print(f"\n报告已保存到: {report_path}")


if __name__ == "__main__":
    main()

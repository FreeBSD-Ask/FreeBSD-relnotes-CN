#!/usr/bin/env python3
"""Accurate comparison of FreeBSD release notes EN vs CN."""

import os
import re

BASE_DIR = r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN"
TMP_DIR = os.path.join(BASE_DIR, "tmp_en")

VERSION_FILES = {
    "3.0": "3.0.txt", "3.1": "3.1.txt", "3.2": "3.2.txt",
    "3.3": "3.3.txt", "3.4": "3.4.txt", "3.5": "3.5.txt",
    "2.0": "2.0.txt", "2.0.5": "2.0.5.txt", "2.1": "2.1.txt",
    "2.1.5": "2.1.5.txt", "2.1.6": "2.1.6.txt", "2.1.7": "2.1.7.txt",
    "2.2": "2.2.txt", "2.2.1": "2.2.1.txt", "2.2.2": "2.2.2.txt",
    "2.2.5": "2.2.5.txt", "2.2.6": "2.2.6.txt", "2.2.7": "2.2.7.txt",
    "2.2.8": "2.2.8.txt",
    "1.0": "1.0.txt", "1.1": "1.1.txt", "1.1.5": "1.1.5.txt",
    "1.1.5.1": "1.1.5.1.txt",
}


def normalize_text(text):
    """Strip formatting, normalize whitespace."""
    # Remove Asciidoc front matter
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)
    # Remove Asciidoc literal block markers
    text = text.replace('....', '')
    # Remove Markdown/Asciidoc heading markers
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^={1,6}\s+', '', text, flags=re.MULTILINE)
    # Remove bold/italic markers
    text = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', text)
    text = re.sub(r'_{1,2}([^_]+)_{1,2}', r'\1', text)
    # Remove link markup
    text = re.sub(r'link:.*?\[.*?\]', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove code block markers
    text = re.sub(r'```\w*\n?', '', text)
    # Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_en_sections(text):
    """Extract sections from English asciidoc text."""
    sections = {}
    # Match numbered sections like "1. What's new" or "1.1. KERNEL CHANGES"
    # Also match unnumbered sections
    lines = text.split('\n')
    current_section = "Intro"
    current_content = []

    for line in lines:
        # Match section headers in the English format
        # Numbered: "1. What's new since 3.4-RELEASE"
        # Sub: "1.1. KERNEL CHANGES"
        # Or plain text headers followed by dashes
        sec_match = re.match(r'^(\d+(?:\.\d+)*)\.\s+(.+)$', line.strip())
        if sec_match:
            if current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = f"{sec_match.group(1)} {sec_match.group(2)}"
            current_content = []
        else:
            current_content.append(line)

    if current_content:
        sections[current_section] = '\n'.join(current_content).strip()

    return sections


def compare_version(version, en_file, cn_file):
    """Compare a single version."""
    diffs = []

    # Read English source
    en_path = os.path.join(TMP_DIR, en_file)
    if not os.path.exists(en_path):
        return [f"英文原文文件不存在: {en_path}"]

    with open(en_path, 'r', encoding='utf-8', errors='replace') as f:
        en_raw = f.read()

    # Read Chinese translation
    cn_path = os.path.join(BASE_DIR, f"{version}.md")
    if not os.path.exists(cn_path):
        return ["中文翻译文件不存在"]

    with open(cn_path, 'r', encoding='utf-8') as f:
        cn_raw = f.read()

    # Normalize both texts
    en_norm = normalize_text(en_raw)
    cn_norm = normalize_text(cn_raw)

    # 1. Check section structure
    # Extract section titles from English
    en_sections = re.findall(r'^(\d+(?:\.\d+)*)\.\s+(.+)$', en_norm, re.MULTILINE)
    # Extract section titles from Chinese
    cn_sections_md = re.findall(r'^(\d+(?:\.\d+)*)\.\s+(.+)$', cn_norm, re.MULTILINE)

    # Check if all numbered sections exist in Chinese
    for sec_num, sec_title in en_sections:
        # Check if the section number appears in Chinese
        if sec_num not in cn_norm and sec_num + '.' not in cn_norm:
            # Maybe it's translated with Chinese numbering
            # Check if the section title keywords appear
            diffs.append(f"可能缺失章节: {sec_num}. {sec_title}")

    # 2. Check security advisories
    en_sa = re.findall(r'FreeBSD-SA-\d+:\d+', en_raw)
    cn_sa = re.findall(r'FreeBSD-SA-\d+:\d+', cn_raw)
    missing_sa = sorted(set(en_sa) - set(cn_sa))
    if missing_sa:
        diffs.append(f"缺失的安全公告: {', '.join(missing_sa)}")

    # 3. Check CERT advisories
    en_cert = re.findall(r'CERT[ -]?(?:Advisory|advisory|CA-\d+\.?\d+)', en_raw)
    cn_cert = re.findall(r'CERT[ -]?(?:Advisory|advisory|CA-\d+\.?\d+)', cn_raw)
    missing_cert = sorted(set(en_cert) - set(cn_cert))
    if missing_cert:
        diffs.append(f"缺失的 CERT 公告: {', '.join(missing_cert)}")

    # 4. Check man page references
    en_man = sorted(set(re.findall(r'\b\w+\(\d[a-z]?\)', en_raw)))
    cn_man = set(re.findall(r'\b\w+\(\d[a-z]?\)', cn_raw))
    missing_man = [m for m in en_man if m not in cn_raw]
    if missing_man:
        diffs.append(f"缺失的手册页引用: {', '.join(missing_man)}")

    # 5. Check URLs
    en_urls = sorted(set(re.findall(r'https?://[^\s\[\]`\)"\'>]+', en_raw)))
    missing_urls = [u for u in en_urls if u.rstrip('.') not in cn_raw and u not in cn_raw]
    if missing_urls:
        diffs.append(f"缺失的 URL:")
        for u in missing_urls:
            diffs.append(f"  {u}")

    # 6. Check RFC references
    en_rfc = sorted(set(re.findall(r'RFC\s*\d+', en_raw)))
    cn_rfc = set(re.findall(r'RFC\s*\d+', cn_raw))
    missing_rfc = [r for r in en_rfc if r not in cn_raw]
    if missing_rfc:
        diffs.append(f"缺失的 RFC 引用: {', '.join(missing_rfc)}")

    # 7. Check code blocks - look for actual code/config content
    # Asciidoc code blocks use ---- delimiters
    en_code = re.findall(r'----\n(.*?)\n----', en_raw, re.DOTALL)
    cn_code = re.findall(r'```\w*\n(.*?)\n```', cn_raw, re.DOTALL)
    if len(en_code) != len(cn_code):
        diffs.append(f"代码块数量不匹配: 英文 {len(en_code)} 个, 中文 {len(cn_code)} 个")
        for i, block in enumerate(en_code):
            block_stripped = block.strip()
            if len(block_stripped) > 10:
                found = any(cn_block.strip() == block_stripped for cn_block in cn_code)
                if not found:
                    first_line = block_stripped.split('\n')[0][:80]
                    diffs.append(f"  英文代码块 #{i+1} 未在中文中找到: {first_line}...")

    # 8. Check for specific important content markers
    # Check for email addresses
    en_emails = sorted(set(re.findall(r'[\w.+-]+@[\w.-]+\.\w+', en_raw)))
    cn_emails = set(re.findall(r'[\w.+-]+@[\w.-]+\.\w+', cn_raw))
    missing_emails = [e for e in en_emails if e not in cn_raw]
    if missing_emails:
        diffs.append(f"缺失的邮件地址: {', '.join(missing_emails)}")

    # 9. Check for file paths (more carefully - only real paths)
    en_paths = sorted(set(re.findall(r'(?:/usr/|/etc/|/dev/|/var/|/tmp/|/lib/|/bin/|/sbin/|/boot/|/stand/|/src/)\S+', en_raw)))
    missing_paths = [p for p in en_paths if p.rstrip('.,;:)') not in cn_raw and p not in cn_raw]
    if missing_paths:
        diffs.append(f"缺失的系统路径:")
        for p in sorted(set(missing_paths)):
            diffs.append(f"  {p}")

    # 10. Check for kernel options / sysctl variables
    en_sysctl = sorted(set(re.findall(r'kern\.\w+', en_raw)))
    missing_sysctl = [s for s in en_sysctl if s not in cn_raw]
    if missing_sysctl:
        diffs.append(f"缺失的 sysctl 变量: {', '.join(missing_sysctl)}")

    # 11. Check for device driver names
    en_drivers = sorted(set(re.findall(r'\b(snd|pcm|ed|de|fxp|tx|xl|vx|ep|ex|fe|lnc|cs|ie|sn|xe|an|awi|wi|cnw|ray|aue|cue|kue|uhci|ohci|usb|umass|ulpt|ubsa|ucom|umodem|ums|ukbd|uhid|firewire|fwe|sbp|sbp2|sym|isp|ahc|ahd|amr|mlx|twe|ida|iir|mly|ciss|twed|aac|ips|mpt|trm|adv|adw|bt|aha|spigot|ctx|meteor|bktr|joy|lpt|ppc|sio|sab|cy|rc|rp|si|stl|stli|stliio|musycc|cm|ed|cs|ex|fe|ie|le|lnc|sn|tl|tx|vx|wb|xl|ze|zp)\d?\b', en_raw, re.IGNORECASE)))
    # This is too noisy, skip

    # 12. Check for important keywords that should be present
    # Look for specific technical terms
    en_terms = set(re.findall(r'`([^`\n]{3,})`', en_raw))
    missing_terms = []
    for term in en_terms:
        if term not in cn_raw:
            missing_terms.append(term)
    if missing_terms:
        unique_missing = sorted(set(missing_terms))
        if len(unique_missing) <= 10:
            diffs.append(f"缺失的内联代码/术语: {', '.join(f'`{t}`' for t in unique_missing)}")
        else:
            diffs.append(f"缺失的内联代码/术语 (共 {len(unique_missing)} 个): {', '.join(f'`{t}`' for t in unique_missing[:15])}...")

    # 13. Rough content length comparison
    en_words = len(en_norm.split())
    cn_words = len(cn_norm.split())
    ratio = cn_words / en_words if en_words > 0 else 0
    if ratio < 0.3:
        diffs.append(f"中文内容可能严重不完整: 英文约 {en_words} 词, 中文约 {cn_words} 词 (比例 {ratio:.1%})")
    elif ratio < 0.5:
        diffs.append(f"中文内容可能不完整: 英文约 {en_words} 词, 中文约 {cn_words} 词 (比例 {ratio:.1%})")

    return diffs


def main():
    results = {}

    for version in sorted(VERSION_FILES.keys(), key=lambda x: list(map(int, re.findall(r'\d+', x))), reverse=True):
        en_file = VERSION_FILES[version]
        diffs = compare_version(version, en_file, f"{version}.md")
        results[version] = diffs

    # Print report
    print("=" * 70)
    print("FreeBSD 发行说明中英对比检查报告")
    print("=" * 70)

    for version in sorted(results.keys(), key=lambda x: list(map(int, re.findall(r'\d+', x))), reverse=True):
        diffs = results[version]
        if diffs:
            print(f"\n{'='*50}")
            print(f"版本 {version}:")
            print(f"{'='*50}")
            for d in diffs:
                print(f"  - {d}")

    # Save report
    report_path = os.path.join(BASE_DIR, "comparison_report.txt")
    with open(report_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("FreeBSD 发行说明中英对比检查报告\n")
        f.write("=" * 70 + "\n\n")
        for version in sorted(results.keys(), key=lambda x: list(map(int, re.findall(r'\d+', x))), reverse=True):
            diffs = results[version]
            if diffs:
                f.write(f"版本 {version}:\n")
                for d in diffs:
                    f.write(f"  - {d}\n")
                f.write("\n")
            else:
                f.write(f"版本 {version}: 无明显缺失\n\n")

    print(f"\n报告已保存到: {report_path}")


if __name__ == "__main__":
    main()

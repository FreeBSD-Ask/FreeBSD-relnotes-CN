#!/usr/bin/env python3
"""Check terminology consistency in FreeBSD release notes Chinese translations."""

import os
import re
import urllib.request
import ssl

BASE_DIR = r"c:\Users\ykla\Documents\FreeBSD-relnotes-CN"
BASE_URL = "https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases"

# Target files
TARGET_FILES = [
    # 6.x
    "6.4-amd64.md", "6.3-amd64.md", "6.2-amd64.md", "6.1-amd64.md", "6.0-amd64.md",
    # 5.x
    "5.5-amd64.md", "5.4-amd64.md", "5.3-amd64.md", "5.2.1-amd64.md", "5.2-amd64.md", "5.1.md", "5.0.md",
    # 4.x
    "4.11.md", "4.10.md", "4.9.md", "4.8.md", "4.7-i386.md", "4.6.2-i386.md", "4.6-i386.md",
    "4.5-i386.md", "4.4-i386.md", "4.3.md", "4.2.md", "4.1.1.md", "4.1.md", "4.0.md",
    # 3.x
    "3.5.md", "3.4.md", "3.3.md", "3.2.md", "3.1.md", "3.0.md",
    # 2.x
    "2.2.8.md", "2.2.7.md", "2.2.6.md", "2.2.5.md", "2.2.2.md", "2.2.1.md", "2.2.md",
    "2.1.7.md", "2.1.6.md", "2.1.5.md", "2.1.md", "2.0.5.md", "2.0.md",
    # 1.x
    "1.1.5.1.md", "1.1.5.md", "1.1.md", "1.0.md",
]

# Rules:
# 1. "base system" -> "基本系统"
# 2. "Jails"/"jails" -> "Jail" (capitalized, singular; but command/path names keep lowercase)
# 3. "FreeBSD Foundation"/"The FreeBSD Foundation" -> "FreeBSD 基金会"
# 4. "Ports"/"Port" -> keep original (capital P, not translated)

def get_english_url(filename):
    """Determine the English original URL for a given Chinese translation file."""
    # Parse version and architecture
    base = filename.replace(".md", "")
    arch = None
    version = base

    if "-amd64" in base:
        version, arch = base.rsplit("-amd64", 1)
        version = version
    elif "-i386" in base:
        version, arch = base.rsplit("-i386", 1)
        version = version

    # Build URL
    release_tag = version + "R"
    if arch == "amd64":
        return f"{BASE_URL}/{release_tag}/relnotes-amd64.adoc"
    elif arch == "i386":
        return f"{BASE_URL}/{release_tag}/relnotes-i386.adoc"
    else:
        # For non-arch-specific files, try i386 first (most common for early versions)
        return f"{BASE_URL}/{release_tag}/relnotes-i386.adoc"


def fetch_english_original(url):
    """Fetch English original from GitHub."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None


def search_english_terms(text):
    """Search for the four terms in English original."""
    results = {}
    if not text:
        return results

    # 1. "base system"
    matches = re.findall(r'\bbase system\b', text, re.IGNORECASE)
    if matches:
        results["base_system"] = True

    # 2. "Jails"/"jails" (but not in command names like jail(8), jail(2), or paths)
    # Look for "Jails" or "jails" as standalone words (not in man page references)
    jail_matches = re.findall(r'\b[Jj]ails\b', text)
    # Filter out man page references like jail(8)
    jail_matches = [m for m in jail_matches if not re.search(r'jail\(\d\)', text)]
    if jail_matches:
        results["jails"] = True

    # Also check for singular "jail" used as a concept (not command/path)
    # This is harder to detect, so we'll look for specific patterns
    jail_concept_patterns = [
        r'jail\s+environment',
        r'jail\s+support',
        r'jail\s+feature',
        r'jail\s+implementation',
        r'jail\s+mechanism',
        r'jail\s+system',
        r'jail\s+startup',
        r'jail\s+script',
        r'using\s+jail',
        r'in\s+a\s+jail',
        r'within\s+a\s+jail',
        r'inside\s+a\s+jail',
        r'the\s+jail\b',
        r'a\s+jail\b',
        r'Jail\b',
    ]
    for pattern in jail_concept_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            results["jail_concept"] = True
            break

    # 3. "FreeBSD Foundation"
    if re.search(r'FreeBSD\s+Foundation', text):
        results["freebsd_foundation"] = True

    # 4. "Ports"/"Port" (capital P, referring to the Ports Collection)
    if re.search(r'\bPorts\b', text):
        results["ports_collection"] = True
    if re.search(r'\bPort\b', text):
        results["port_singular"] = True

    # Also check for "ports tree", "ports collection" (lowercase)
    if re.search(r'\bports\s+tree\b', text):
        results["ports_tree_lowercase"] = True
    if re.search(r'\bports\s+collection\b', text, re.IGNORECASE):
        results["ports_collection_lowercase"] = True

    return results


def check_chinese_terms(filepath, english_terms):
    """Check Chinese translation for terminology violations."""
    violations = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return [{"file": os.path.basename(filepath), "line": 0, "issue": "文件不存在", "text": ""}]

    for i, line in enumerate(lines, 1):
        # Skip URLs and code blocks
        if line.strip().startswith("```") or line.strip().startswith("http"):
            continue

        # 1. Check "base system" -> should be "基本系统"
        if english_terms.get("base_system"):
            # Check for wrong translations of "base system"
            if re.search(r'基础系统|根系统', line):
                violations.append({
                    "file": os.path.basename(filepath),
                    "line": i,
                    "issue": '"base system" 应翻译为"基本系统"，而非其他译法',
                    "text": line.strip()
                })

        # 2. Check "Jails"/"jails" -> should be "Jail" (capitalized, singular)
        # But allow lowercase in command names (jail(8), jail(2)), paths (/jails/foo), and variable names
        if english_terms.get("jails") or english_terms.get("jail_concept"):
            # Check for "Jails" (plural) in Chinese text (not in paths/commands)
            if re.search(r'Jails', line):
                # Exclude paths and command references
                if not re.search(r'/Jails|Jails\(\d\)', line):
                    violations.append({
                        "file": os.path.basename(filepath),
                        "line": i,
                        "issue": '"Jails" 应翻译为 "Jail"（首字母大写，单数形式）',
                        "text": line.strip()
                    })
            # Check for lowercase "jail" used as concept (not in commands/paths/variables)
            # This is tricky - we need to find "jail" that refers to the concept
            # but not in man page references, paths, or variable names
            if re.search(r'\bjail\b', line, re.IGNORECASE):
                # Skip if it's in a man page reference like jail(8), jail(2)
                if re.search(r'jail\(\d\)', line):
                    continue
                # Skip if it's in a path like /jails/foo, rc.d/jail
                if re.search(r'/jail|jail/', line):
                    continue
                # Skip if it's in a variable name like jail_name_flags, jail_interface
                if re.search(r'jail_\w+', line):
                    continue
                # Skip if it's in a URL
                if re.search(r'query=jail', line):
                    continue
                # Skip if it's in backticks (code)
                if re.search(r'`[^`]*jail[^`]*`', line):
                    continue
                # Check if "jail" is used as a concept word (should be "Jail")
                # Look for patterns like "jail 环境", "jail 支持", etc.
                if re.search(r'\bjail\b', line) and not re.search(r'[jJ]ail', line):
                    # Only lowercase "jail" found (not "Jail")
                    # Check context - if it's used as a concept, it should be "Jail"
                    pass  # This is too complex to check automatically

        # 3. Check "FreeBSD Foundation" -> should be "FreeBSD 基金会"
        if english_terms.get("freebsd_foundation"):
            # Check for "FreeBSD Foundation" not translated
            if re.search(r'FreeBSD\s+Foundation', line):
                violations.append({
                    "file": os.path.basename(filepath),
                    "line": i,
                    "issue": '"FreeBSD Foundation" 应翻译为 "FreeBSD 基金会"',
                    "text": line.strip()
                })

        # 4. Check "Ports"/"Port" -> should keep original with capital P
        if english_terms.get("ports_collection") or english_terms.get("ports_tree_lowercase"):
            # Check for "端口树" (wrong translation of "ports tree")
            if re.search(r'端口树', line):
                violations.append({
                    "file": os.path.basename(filepath),
                    "line": i,
                    "issue": '"ports tree" 应翻译为 "Ports 树"，而非 "端口树"',
                    "text": line.strip()
                })
            # Check for "ports 树" (lowercase p)
            if re.search(r'ports\s*树', line):
                violations.append({
                    "file": os.path.basename(filepath),
                    "line": i,
                    "issue": '"ports 树" 应为 "Ports 树"（大写 P）',
                    "text": line.strip()
                })
            # Check for "ports 集合" (lowercase p)
            if re.search(r'ports\s*集合', line):
                violations.append({
                    "file": os.path.basename(filepath),
                    "line": i,
                    "issue": '"ports 集合" 应为 "Ports 集合"（大写 P）',
                    "text": line.strip()
                })

        # Also check for standalone lowercase "ports" that refers to the Ports Collection
        # (not in URLs, paths, or variable names)
        if english_terms.get("ports_collection") or english_terms.get("ports_tree_lowercase"):
            # Find "ports" that's not in a URL, path, or code context
            # This is a simplified check
            pass

    return violations


def main():
    all_violations = []
    files_checked = 0
    files_skipped = 0

    for filename in TARGET_FILES:
        filepath = os.path.join(BASE_DIR, filename)
        if not os.path.exists(filepath):
            files_skipped += 1
            continue

        # Fetch English original
        url = get_english_url(filename)
        english_text = fetch_english_original(url)

        if not english_text:
            # Try alternative URL (some versions might have different structure)
            base = filename.replace(".md", "")
            alt_url = f"{BASE_URL}/{base.replace('-', '.').split('.')[0]}R/relnotes.adoc"
            # Skip if we can't get the English original
            files_skipped += 1
            # Still check the Chinese file for obvious violations
            english_terms = {
                "base_system": True,
                "jails": True,
                "jail_concept": True,
                "freebsd_foundation": True,
                "ports_collection": True,
                "ports_tree_lowercase": True,
            }
        else:
            english_terms = search_english_terms(english_text)
            files_checked += 1

        # Check Chinese translation
        violations = check_chinese_terms(filepath, english_terms)
        all_violations.extend(violations)

    # Print results
    print(f"检查完成：成功获取英文原文 {files_checked} 个，跳过 {files_skipped} 个")
    print(f"发现 {len(all_violations)} 处不符合规则的翻译：\n")

    # Group by file
    by_file = {}
    for v in all_violations:
        fname = v["file"]
        if fname not in by_file:
            by_file[fname] = []
        by_file[fname].append(v)

    for fname, violations in sorted(by_file.items()):
        print(f"### {fname}")
        for v in violations:
            print(f"  行 {v['line']}: {v['issue']}")
            print(f"    原文: {v['text'][:100]}")
        print()

    if not all_violations:
        print("全部合规！")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fetch and search for specific missing paragraphs in English source files."""

import urllib.request
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')

# 10.1 - missing r265229, r269432
print("=== FreeBSD 10.1 - Missing paragraphs ===")
en = fetch("https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/10.1R/relnotes.adoc")
for rev in ['265229', '269432']:
    for line in en.split('\n'):
        if rev in line:
            print(f"  r{rev}: {line.strip()[:200]}")

# 10.2 - missing r283505, r284094, r284096
print("\n=== FreeBSD 10.2 - Missing paragraphs ===")
en = fetch("https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/10.2R/relnotes.adoc")
for rev in ['283505', '284094', '284096']:
    for line in en.split('\n'):
        if rev in line:
            print(f"  r{rev}: {line.strip()[:200]}")

# 10.3 - missing r287079
print("\n=== FreeBSD 10.3 - Missing paragraphs ===")
en = fetch("https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/10.3R/relnotes.adoc")
for rev in ['287079']:
    for line in en.split('\n'):
        if rev in line:
            print(f"  r{rev}: {line.strip()[:200]}")

# 10.0 - missing r256773 (sendmail SSL)
print("\n=== FreeBSD 10.0 - Missing r256773 ===")
en = fetch("https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/10.0R/relnotes.adoc")
for line in en.split('\n'):
    if '256773' in line:
        print(f"  r256773: {line.strip()[:200]}")

# Also check for the "latest, up-to-date version" paragraph in 10.0
print("\n=== FreeBSD 10.0 - Check for 'latest, up-to-date' paragraph ===")
for line in en.split('\n'):
    if 'latest' in line.lower() and 'up-to-date' in line.lower():
        print(f"  Found: {line.strip()[:200]}")

#!/usr/bin/env python3
"""Get full text of missing paragraphs from English source."""

import urllib.request
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')

# 10.0 missing paragraphs
print("="*60)
print("FreeBSD 10.0 - Full text of missing paragraphs")
print("="*60)
en = fetch("https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/10.0R/relnotes.adoc")

missing_revs_100 = ['240135', '245652', '254466', '254885', '255524', '255744', '256773']
for rev in missing_revs_100:
    for line in en.split('\n'):
        if rev in line:
            print(f"\n--- r{rev} ---")
            print(line.strip())
            break

# 10.1 missing paragraphs
print("\n" + "="*60)
print("FreeBSD 10.1 - Full text of missing paragraphs")
print("="*60)
en = fetch("https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/10.1R/relnotes.adoc")

missing_revs_101 = ['265229', '269432']
for rev in missing_revs_101:
    for line in en.split('\n'):
        if rev in line:
            print(f"\n--- r{rev} ---")
            print(line.strip())
            break

# 10.2 missing paragraphs
print("\n" + "="*60)
print("FreeBSD 10.2 - Full text of missing paragraphs")
print("="*60)
en = fetch("https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/10.2R/relnotes.adoc")

missing_revs_102 = ['283505', '284094', '284096']
for rev in missing_revs_102:
    found = False
    for line in en.split('\n'):
        if rev in line:
            print(f"\n--- r{rev} ---")
            print(line.strip())
            found = True
    if not found:
        print(f"\n--- r{rev} --- NOT FOUND")

# 10.3 missing paragraphs
print("\n" + "="*60)
print("FreeBSD 10.3 - Full text of missing paragraphs")
print("="*60)
en = fetch("https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/10.3R/relnotes.adoc")

for line in en.split('\n'):
    if '287079' in line:
        print(f"\n--- r287079 ---")
        print(line.strip())
        break

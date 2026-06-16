import urllib.request
import sys

url = 'https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.6.2R/relnotes-i386.adoc'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        content = resp.read().decode('utf-8')
    with open('_en_source.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Saved {len(content)} chars, {content.count(chr(10))+1} lines')
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
    sys.exit(1)

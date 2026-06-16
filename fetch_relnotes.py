import urllib.request

# Try fetching the page again - it might have been updated
url = 'https://www.freebsd.org/releases/15.1R/relnotes/'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
})
with urllib.request.urlopen(req, timeout=30) as resp:
    content = resp.read().decode('utf-8')

# Search for the sections
import re

# Find all h2 headings
h2_pattern = re.compile(r'<h2[^>]*>(.*?)</h2>', re.DOTALL)
for m in h2_pattern.finditer(content):
    clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    print(f'h2: {clean}')

print()

# Search specifically for "Ports" and "Future"
for keyword in ['Ports Collection', 'ports', 'future-releases', 'Future FreeBSD', 'Packaging Changes']:
    idx = content.find(keyword)
    if idx != -1:
        print(f'Found "{keyword}" at index {idx}')
        print(f'  Context: ...{content[max(0,idx-100):idx+200]}...')
    else:
        print(f'NOT FOUND: "{keyword}"')

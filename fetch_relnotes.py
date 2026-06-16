import urllib.request
import re

# Fetch the page with a browser-like user agent
url = 'https://www.freebsd.org/releases/15.1R/relnotes/'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'identity',
    'Cache-Control': 'no-cache',
})
with urllib.request.urlopen(req, timeout=30) as resp:
    content = resp.read().decode('utf-8')

print(f'Total length: {len(content)}')

# Search for the content after Man Pages section
man_pages_idx = content.find('id="man-pages"')
if man_pages_idx != -1:
    # Get everything from man-pages to the end of the main content
    # Find the next sect1 div after man-pages
    after_man = content[man_pages_idx:]
    # Find the end of the documentation section
    sect1_end = after_man.find('<div class="sect1">')
    if sect1_end != -1:
        next_sect = after_man[sect1_end:sect1_end+2000]
        print('--- Next sect1 after man-pages ---')
        print(next_sect)
    else:
        # No more sect1 divs - check what comes after
        print('--- 2000 chars after man-pages ---')
        print(after_man[:2000])

print()
# Also search for "ports" and "future" in the entire content
for keyword in ['id="ports"', 'id="future-releases"', 'Ports Collection', 'General Notes']:
    idx = content.find(keyword)
    if idx != -1:
        print(f'Found "{keyword}" at index {idx}')
        print(f'  Context: ...{content[max(0,idx-100):idx+200]}...')
    else:
        print(f'NOT FOUND: "{keyword}"')

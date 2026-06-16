import urllib.request

url = 'https://www.freebsd.org/releases/15.0R/relnotes/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
with urllib.request.urlopen(req, timeout=30) as resp:
    content = resp.read().decode('utf-8')

# Find the future-releases section content (not just the TOC link)
search = 'id="future-releases"'
idx = content.find(search)
if idx >= 0:
    print(f'Found section header at index: {idx}')
    # Print the section content
    print(content[idx:idx+2000])
else:
    print('Section header not found')
    # Try searching for 'General Notes' in the body
    idx2 = content.rfind('General Notes')
    if idx2 >= 0:
        print(f'Found General Notes at index: {idx2}')
        print(content[max(0,idx2-200):idx2+2000])
    else:
        print('Not found either')
        print(f'Page length: {len(content)}')

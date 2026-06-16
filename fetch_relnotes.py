import urllib.request
import json
import base64

# Get the latest version of the 15.1 relnotes.adoc file from GitHub
url = 'https://api.github.com/repos/freebsd/freebsd-doc/contents/website/content/en/releases/15.1R/relnotes.adoc'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/vnd.github.v3+json'
})
with urllib.request.urlopen(req, timeout=30) as resp:
    data = json.loads(resp.read().decode('utf-8'))

content = base64.b64decode(data['content']).decode('utf-8')
lines = content.splitlines()

print(f'Total lines: {len(lines)}')
print(f'SHA: {data["sha"]}')

# Search for Ports and Future sections
for i, line in enumerate(lines):
    if '[[ports]]' in line or 'Ports Collection' in line:
        print(f'Line {i+1}: {line}')
    if '[[future-releases]]' in line or 'Future FreeBSD' in line:
        print(f'Line {i+1}: {line}')

# Print the last 20 lines
print()
print('--- Last 20 lines ---')
for line in lines[-20:]:
    print(line)

import urllib.request

url = 'https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.6.2R/relnotes-i386.adoc'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=30) as resp:
    content = resp.read().decode('utf-8')

lines = content.split('\n')

# Extract the userland section (around lines 870-1050)
# Let me get the full paragraphs for each missing item
ranges = [
    (870, 900, "m4 area"),
    (900, 920, "ngctl/patch area"),
    (918, 970, "pam area"),
    (975, 990, "reboot area"),
    (1005, 1020, "usbhidctl area"),
    (1030, 1050, "watch area"),
]

for start, end, label in ranges:
    print(f'\n=== {label} (lines {start}-{end}) ===')
    for i in range(start-1, min(end, len(lines))):
        print(f'{i+1}: {lines[i]}')

# Also search for pr( references
print('\n=== pr( references ===')
for i, line in enumerate(lines):
    if 'REFENTRYTITLE">pr<' in line or ('query=pr&' in line):
        start = max(0, i-2)
        end = min(len(lines), i+5)
        for j in range(start, end):
            print(f'{j+1}: {lines[j]}')
        print()

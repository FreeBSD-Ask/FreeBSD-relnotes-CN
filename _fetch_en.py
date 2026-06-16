import urllib.request

url = 'https://raw.githubusercontent.com/freebsd/freebsd-doc/main/website/content/en/releases/4.6.2R/relnotes-i386.adoc'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=30) as resp:
    content = resp.read().decode('utf-8')

keywords = ['m4', 'ngctl', 'patch', 'pam_opie', 'pam_radius', 'pam_ssh', 'pam_tacplus', 'pam_unix', 'reboot', 'usbhidctl', 'watch', 'bzip2', 'pr(']
for kw in keywords:
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if kw in line:
            start = max(0, i-1)
            end = min(len(lines), i+3)
            print(f'--- Found "{kw}" at line {i+1} ---')
            for j in range(start, end):
                print(f'  {j+1}: {lines[j][:200]}')
            print()

import urllib.request
import json

# Check the most recent commit to the relnotes.adoc file
url = 'https://api.github.com/repos/freebsd/freebsd-doc/commits?path=website/content/en/releases/15.1R/relnotes.adoc&per_page=5'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/vnd.github.v3+json'
})
with urllib.request.urlopen(req, timeout=30) as resp:
    commits = json.loads(resp.read().decode('utf-8'))

# Get the diff of the most recent commit
sha = commits[0]['sha']
print(f'Most recent commit: {sha}')
print(f'Message: {commits[0]["commit"]["message"][:200]}')
print()

# Get the commit diff
diff_url = f'https://api.github.com/repos/freebsd/freebsd-doc/commits/{sha}'
req2 = urllib.request.Request(diff_url, headers={
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/vnd.github.v3+json'
})
with urllib.request.urlopen(req2, timeout=30) as resp:
    commit_data = json.loads(resp.read().decode('utf-8'))

# Check the files changed
for f in commit_data.get('files', []):
    if 'relnotes' in f['filename']:
        print(f'File: {f["filename"]}')
        print(f'Status: {f["status"]}')
        print(f'Changes: +{f["additions"]} -{f["deletions"]}')
        # Print the patch if it's not too large
        patch = f.get('patch', '')
        if len(patch) < 5000:
            print('Patch:')
            print(patch)
        else:
            print(f'Patch too large ({len(patch)} chars), showing first 3000:')
            print(patch[:3000])

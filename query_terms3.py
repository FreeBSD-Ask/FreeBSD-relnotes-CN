import requests
import urllib.parse
import json
import re

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.termonline.cn/',
    'Origin': 'https://www.termonline.cn',
})

# Try the list API with databaseId
print("Trying list API with databaseId...")
for db_id in ['1', '2', '3', '4', '5']:
    url = f'https://api.termonline.cn/main-serve/business/tm/tmWord/list?term=kernel&match=2&pageSize=10&pageNo=1&databaseId={db_id}'
    try:
        resp = session.get(url, timeout=15)
        data = resp.json()
        if data.get('result') and data['result'].get('searchResult'):
            for sr in data['result']['searchResult']:
                total = sr['result']['totalRecords']
                if total > 0:
                    print(f"  databaseId={db_id}: total={total}")
                    for w in sr['result']['tmWordList'][:3]:
                        print(f"    cn={w.get('cn')}, en={w.get('en')}, subject={w.get('subjectName')}")
        elif data.get('result'):
            print(f"  databaseId={db_id}: result keys={list(data["result"].keys()) if isinstance(data["result"], dict) else type(data["result"])}")
        else:
            print(f"  databaseId={db_id}: {json.dumps(data, ensure_ascii=False)[:200]}")
    except Exception as e:
        print(f"  databaseId={db_id}: Error: {e}")

# Try fetching the JS bundle to find API configuration
print("\nFetching JS bundle to find API config...")
resp_js = session.get('https://www.termonline.cn/assets/js/index-1779d7fe.js', timeout=30)
js_content = resp_js.text

# Search for API-related patterns
patterns = [
    r'allSearch',
    r'searchSuggest',
    r'tmWord',
    r'databaseId',
    r'baseId',
    r'token',
    r'authorization',
    r'Bearer',
    r'apiKey',
    r'api-key',
]

for pattern in patterns:
    matches = re.findall(rf'.{{0,80}}{pattern}.{{0,80}}', js_content, re.IGNORECASE)
    if matches:
        print(f"\n  Pattern '{pattern}' found {len(matches)} times:")
        for m in matches[:3]:
            print(f"    ...{m}...")

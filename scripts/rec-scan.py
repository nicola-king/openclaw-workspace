#!/home/sayelf/.local/venvs/scraper/bin/python3
"""中东重建机会扫描"""
import sys; sys.path.insert(0, '/home/sayelf/.openclaw/workspace/scripts')
from scraper_v4 import search
from datetime import datetime

print(f"=== 重建监控 {datetime.now().strftime('%Y-%m-%d')} ===")

queries = [
    'Middle East post-war reconstruction contracts 2026',
    'Saudi infrastructure reconstruction tender Q3 2026',
    '中东 战后重建 招标 2026',
    'Middle East rebuilding projects Q4 2026',
]
seen = set()
for q in queries:
    try:
        r = search(q, count=5)
        for item in r:
            url = item['url'].split('?')[0]  # clean URL
            if url not in seen and 'bing.com/ck' not in url:
                seen.add(url)
                print(f'  [{item["title"][:55].strip()}]')
                print(f'    {url[:80]}')
    except Exception as e:
        print(f'  ❌ {q[:30]}: {e}')
print(f'\n不重复: {len(seen)} 条')

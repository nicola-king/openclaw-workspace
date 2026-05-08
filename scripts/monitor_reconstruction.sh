#!/bin/bash
# 中东战后重建机会监控 (修复版)
VENV=/home/sayelf/.local/venvs/scraper/bin/python3
cd /home/sayelf/.openclaw/workspace
echo "=== 重建监控 $(date +%Y-%m-%d) ==="
$VENV -c "
import sys; sys.path.insert(0, 'scripts')
from scraper_v4 import search
queries = [
    'Middle East post-war reconstruction contracts 2026',
    'Saudi Arabia infrastructure reconstruction tender Q3 2026',
    '中东 战后重建 招标 2026',
    'Middle East rebuilding projects Q4 2026 contract',
]
seen = set()
for q in queries:
    try:
        r = search(q, count=5)
        for res in r:
            if res['url'] not in seen:
                seen.add(res['url'])
                print(f'  [{res[\"title\"][:55]}] {res[\"url\"][:70]}')
    except Exception as e:
        print(f'  ❌ {q[:30]}: {e}')
print(f'\\n不重复: {len(seen)} 条')
" 2>&1 | tee -a data/reconstruction-monitor.log

#!/bin/bash
# 浏览器搜索器 v3 - Bing via Chromium 渲染，清理 URL
set -e

QUERY="$*"
[ -z "$QUERY" ] && echo "Usage: bsearch <query>" && exit 1

ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY'))")
PYTHON="/home/sayelf/.local/venvs/scraper/bin/python3"
OUTFILE=$(mktemp /tmp/bsearch-XXXXXX.html)

cleanup() { rm -f "$OUTFILE"; }
trap cleanup EXIT

# Bing search (via real browser = bypass anti-bot)
ENGINE="https://www.bing.com/search?q=$ENCODED&count=10"

chromium --headless --no-sandbox --disable-gpu \
    --dump-dom "$ENGINE" 2>/dev/null > "$OUTFILE"

$PYTHON -c "
import sys, re, json, urllib.parse
from bs4 import BeautifulSoup

with open('$OUTFILE') as f:
    html = f.read()

soup = BeautifulSoup(html, 'lxml')
results = []
seen = set()

def clean_bing_url(url):
    '''Extract real URL from Bing redirect'''
    if '/ck/a' in url or 'bing.com' in url.lower():
        # Try to extract from 'u' parameter
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        if 'u' in params:
            return params['u'][0]
        # Try to extract from 'p' or redirect chain
        if 'p=' in url:
            # Bing encoded redirect - can't easily decode, but skip
            pass
    return url

# Bing result structure
for li in soup.select('li.b_algo'):
    h2 = li.select_one('h2')
    if h2:
        a = h2.find('a')
        if a:
            url = a.get('href', '')
            title = a.get_text(strip=True)
            # Get snippet
            snippet_el = li.select_one('.b_caption p, .b_lineclamp2, .b_algoSlug')
            snippet = snippet_el.get_text(strip=True) if snippet_el else ''
            if url and title and len(title) > 5:
                clean_url = clean_bing_url(url)
                if clean_url and 'bing.com' not in clean_url and clean_url not in seen:
                    seen.add(clean_url)
                    results.append({'title': title, 'url': clean_url, 'snippet': snippet[:300]})

# Google result structure (used by some engines)
if not results:
    for a in soup.find_all('a', href=True):
        href = a['href']
        text = a.get_text(strip=True)
        if href.startswith('http') and 'bing.com' not in href and text and len(text) > 15:
            if href not in seen:
                seen.add(href)
                results.append({'title': text[:80], 'url': href, 'snippet': ''})

print(json.dumps(results[:10], ensure_ascii=False, indent=2))
exit(0 if results else 1)
" 2>&1

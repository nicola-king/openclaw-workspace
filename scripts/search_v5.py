#!/home/sayelf/.local/venvs/scraper/bin/python3
"""
搜索 Agent v5 — 统一情报搜索引擎 (修复版)
DDG Lite(Chromium) → Bing → Google → Brave
"""
import sys, re, json, time, hashlib, subprocess, tempfile, urllib.parse
from pathlib import Path

CACHE = Path.home() / ".openclaw" / "workspace" / ".cache" / "scraper"
CACHE.mkdir(parents=True, exist_ok=True)
CACHE_TTL = 1800

def _ck(s): return hashlib.sha256(s.encode()).hexdigest()[:16]

def _cg(k):
    p = CACHE / f"{k}.json"
    if p.exists() and time.time() - p.stat().st_mtime < CACHE_TTL:
        return json.loads(p.read_text())
    return None

def _cs(k, d):
    (CACHE / f"{k}.json").write_text(json.dumps(d, ensure_ascii=False))

def search_ddg_chromium(query, count=10):
    """DDG Lite via Chromium headless — 返回干净URL"""
    k = _ck(f"chromium_ddg:{query}")
    cached = _cg(k)
    if cached: return cached

    url = f"https://lite.duckduckgo.com/lite/?q={urllib.parse.quote(query)}"
    tmp = tempfile.mktemp(suffix=".html")
    try:
        subprocess.run(
            ["/snap/bin/chromium", "--headless", "--no-sandbox", "--disable-gpu",
             "--disable-dev-shm-usage", "--dump-dom", url],
            timeout=25, stdout=open(tmp, "w"), stderr=subprocess.DEVNULL
        )
        html = Path(tmp).read_text("utf-8", errors="ignore")
        results = []
        seen = set()
        # Extract from result links
        for m in re.finditer(r'<a[^>]*href="(https?://[^"]+)"[^>]*>([^<]+)</a>', html):
            u, t = m.group(1), m.group(2).strip()
            bad = ["duckduckgo.com", "google.com", "youtube.com"]
            if not any(d in u for d in bad) and u not in seen and len(t) > 5:
                seen.add(u)
                results.append({"title": t, "url": u.split("?")[0], "snippet": ""})
            if len(results) >= count: break
        _cs(k, results)
        return results
    except Exception as e:
        return []
    finally:
        Path(tmp).unlink(missing_ok=True)

def search_bing(query, count=10):
    """Bing HTML 搜索 + URL 探测"""
    k = _ck(f"bing:{query}")
    cached = _cg(k)
    if cached: return cached

    import cloudscraper
    scraper = cloudscraper.create_scraper(delay=1)
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"
    
    try:
        resp = scraper.get(
            f"https://www.bing.com/search?q={urllib.parse.quote(query)}&count={count}",
            headers={"User-Agent": ua}, timeout=15
        )
        if resp.status_code != 200: return []
        html = resp.text
        
        results = []
        seen_urls = set()
        # Extract from b_algo blocks
        blocks = re.findall(r'<li[^>]*class="b_algo"[^>]*>.*?</li>', html, re.DOTALL)
        for block in blocks:
            a = re.search(r'<h2>.*?<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', block, re.DOTALL)
            if not a: continue
            href = a.group(1)
            title = re.sub(r'<[^>]+>', '', a.group(2)).strip()
            if not title or len(title) < 5: continue
            if href in seen_urls: continue
            seen_urls.add(href)
            
            # Resolve real URL via HEAD request
            real_url = href
            if "bing.com/ck" in href or "bing.com/r" in href:
                try:
                    h = scraper.head(href, allow_redirects=True, timeout=5, headers={"User-Agent": ua})
                    real_url = str(h.url).split("?")[0]
                except: pass
            
            snippet = ""
            p = re.search(r'<p[^>]*>(.*?)</p>', block, re.DOTALL)
            if p: snippet = re.sub(r'<[^>]+>', '', p.group(1)).strip()[:300]
            
            results.append({"title": title, "url": real_url, "snippet": snippet})
            if len(results) >= count: break
        
        _cs(k, results)
        return results
    except: return []

def search(query, count=10):
    """统一搜索: DDG(Chromium) → Bing → 全部缓存"""
    k = _ck(f"search:{query}")
    cached = _cg(k)
    if cached: return cached

    results = []
    
    print(f"🔍 {query}")
    
    # 方法1: DDG Chromium
    results = search_ddg_chromium(query, count)
    print(f"  DDG: {len(results)} results")
    
    # 方法2: Bing 回退
    if not results:
        results = search_bing(query, count)
        print(f"  Bing: {len(results)} results")
    
    _cs(k, results)
    return results

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or "Saudi Arabia reconstruction tender 2026"
    results = search(query, 10)
    print(f"\n总计: {len(results)} 条")
    for r in results:
        print(f"  [{r['title'][:55]}] {r['url'][:70]}")

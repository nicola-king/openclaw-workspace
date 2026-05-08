#!/home/sayelf/.local/venvs/scraper/bin/python3
"""
太一轻量 SearXNG — 私有元搜索引擎 (Python 实现)
多源并行查询 + 结果去重合并 + 代理绕过 + 缓存
"""
import sys, json, re, time, hashlib, urllib.parse, subprocess, tempfile
from pathlib import Path
from datetime import datetime, timedelta

CACHE_DIR = Path.home() / ".openclaw" / "workspace" / ".cache" / "taiyi-searxng"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_TTL = 1800  # 30min

def _cache_key(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]

def _cache_get(key):
    p = CACHE_DIR / f"{key}.json"
    if p.exists() and time.time() - p.stat().st_mtime < CACHE_TTL:
        return json.loads(p.read_text())
    return None

def _cache_set(key, data):
    (CACHE_DIR / f"{key}.json").write_text(json.dumps(data, ensure_ascii=False))

def _fetch(url, timeout=15, bypass_proxy=True):
    """抓取页面，可选绕过系统代理"""
    import cloudscraper
    scraper = cloudscraper.create_scraper(delay=1)
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"
    try:
        if bypass_proxy:
            resp = scraper.get(url, headers={"User-Agent": ua}, timeout=timeout,
                               proxies={"http": "", "https": ""})  # 绕过代理
        else:
            resp = scraper.get(url, headers={"User-Agent": ua}, timeout=timeout)
        return resp.status_code, resp.text
    except Exception as e:
        return 0, str(e)

def _chromium_render(url, timeout=20):
    """用 Chromium 渲染 JS 页面（绕过代理）"""
    tmp = tempfile.mktemp(suffix=".html")
    try:
        env = {"http_proxy": "", "https_proxy": "", "no_proxy": "*"}
        subprocess.run(
            ["/snap/bin/chromium", "--headless", "--no-sandbox", "--disable-gpu",
             "--disable-dev-shm-usage", "--dump-dom", url],
            timeout=timeout, stdout=open(tmp, "w"), stderr=subprocess.DEVNULL,
            env=env
        )
        html = Path(tmp).read_text("utf-8", errors="ignore")
        return html
    except:
        return ""
    finally:
        Path(tmp).unlink(missing_ok=True)

# ==============================
# 引擎 1: DuckDuckGo HTML (cloudscraper)
# ==============================
def search_ddg(query, count=10):
    k = _cache_key(f"ddg:{query}")
    cached = _cache_get(k)
    if cached: return cached
    
    status, html = _fetch(f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}")
    results = []
    seen = set()
    
    if status == 200 and 'result__a' in html:
        for m in re.finditer(r'<a[^>]*rel="nofollow"[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL):
            href, title_raw = m.group(1), m.group(2)
            title = re.sub(r'<[^>]+>', '', title_raw).strip()
            if not title or len(title) < 5: continue
            url = _decode_url(href)
            if not url or url in seen or 'duckduckgo.com' in url: continue
            seen.add(url)
            results.append({"title": title, "url": url, "snippet": "", "engine": "ddg"})
            if len(results) >= count: break
    
    _cache_set(k, results)
    return results

# ==============================
# 引擎 2: Bing (cloudscraper，绕过代理)
# ==============================
def search_bing(query, count=10):
    k = _cache_key(f"bing:{query}")
    cached = _cache_get(k)
    if cached: return cached
    
    results = []
    seen = set()
    
    status, html = _fetch(f"https://www.bing.com/search?q={urllib.parse.quote(query)}&count={count}")
    
    if status == 200:
        for block in re.finditer(r'<li[^>]*class="b_algo"[^>]*>.*?</li>', html, re.DOTALL):
            block = block.group()
            a = re.search(r'<h2>.*?<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', block, re.DOTALL)
            if not a: continue
            href, title_raw = a.group(1), a.group(2)
            title = re.sub(r'<[^>]+>', '', title_raw).strip()
            if not title or len(title) < 5: continue
            url = href.split("?")[0]  # 取干净URL
            if url in seen: continue
            seen.add(url)
            p = re.search(r'<p[^>]*>(.*?)</p>', block, re.DOTALL)
            snippet = re.sub(r'<[^>]+>', '', p.group(1)).strip()[:300] if p else ""
            results.append({"title": title, "url": url, "snippet": snippet, "engine": "bing"})
            if len(results) >= count: break
    
    _cache_set(k, results)
    return results

# ==============================
# 引擎 3: Chromium + DDG Lite (无代理)
# ==============================
def search_chromium(query, count=10):
    k = _cache_key(f"chromium:{query}")
    cached = _cache_get(k)
    if cached: return cached
    
    html = _chromium_render(f"https://lite.duckduckgo.com/lite/?q={urllib.parse.quote(query)}")
    results = []
    seen = set()
    
    if html:
        for m in re.finditer(r'<a[^>]+href="(https?://[^"]+)"[^>]*>([^<]+)</a>', html):
            url, title = m.group(1), m.group(2).strip()
            bad = ["duckduckgo.com", "google.com", "youtube.com"]
            if not any(d in url for d in bad) and len(title) > 5 and url not in seen:
                seen.add(url)
                results.append({"title": title, "url": url.split("?")[0], "snippet": "", "engine": "chromium"})
                if len(results) >= count: break
    
    _cache_set(k, results)
    return results

# ==============================
# 引擎 4: 公共 SearXNG 实例 (绕过代理)
# ==============================
SEARXNG_INSTANCES = [
    "https://searx.be",
]

def search_searxng(query, count=10):
    k = _cache_key(f"searxng:{query}")
    cached = _cache_get(k)
    if cached: return cached
    
    results = []
    seen = set()
    
    for instance in SEARXNG_INSTANCES:
        url = f"{instance}/search?q={urllib.parse.quote(query)}&format=json&language=en-US"
        try:
            import cloudscraper
            scraper = cloudscraper.create_scraper(delay=0.5)
            resp = scraper.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10,
                               proxies={"http": "", "https": ""})
            if resp.status_code == 200:
                data = resp.json()
                for r in data.get("results", []):
                    u = r.get("url", "")
                    t = r.get("title", "")
                    if not t or len(t) < 5 or u in seen: continue
                    seen.add(u)
                    results.append({"title": t, "url": u, "snippet": r.get("content", "")[:300],
                                    "engine": f"searxng-{instance.split('/')[-1]}"})
                    if len(results) >= count: break
                if results: break  # 第一个成功的实例
        except: continue
    
    _cache_set(k, results)
    return results

# ==============================
# URL 解码 (DDG/Bing 跳转链接)
# ==============================
def _decode_url(raw):
    if not raw: return ""
    clean = raw.replace("&amp;", "&")
    # DDG uddg
    m = re.search(r'[?&]uddg=([^&]+)', clean)
    if m: return urllib.parse.unquote(m.group(1))
    # Google /url
    m = re.search(r'/url\?q=([^&]+)', clean)
    if m: return urllib.parse.unquote(m.group(1))
    # 直接 URL
    m = re.search(r'(https?://[^&\s<>"\']+)', clean)
    if m:
        url = m.group(1)
        bad = ["bing.com", "microsoft.com", "duckduckgo.com"]
        if not any(d in url for d in bad): return url
    return clean

# ==============================
# 统一搜索入口 — 多引擎聚合
# ==============================
engines = {
    "ddg": search_ddg,
    "bing": search_bing,
    "chromium": search_chromium,
    "searxng": search_searxng,
}

def search(query, count=10, engine_names=None):
    """
    多引擎并行搜索 + 结果去重合并
    engine_names: ["ddg", "bing", "chromium", "searxng"] 或 None (全部)
    """
    ck = _cache_key(f"taiyi_searxng:{query}")
    cached = _cache_get(ck)
    if cached: return cached
    
    if engine_names is None:
        engine_names = list(engines.keys())
    
    all_results = []
    seen_urls = set()
    
    print(f"🔍 {query}")
    for name in engine_names:
        fn = engines.get(name)
        if not fn: continue
        try:
            t0 = time.time()
            res = fn(query, count)
            elapsed = time.time() - t0
            print(f"  {name}: {len(res)} results ({elapsed:.1f}s)")
            for r in res:
                if r["url"] not in seen_urls:
                    seen_urls.add(r["url"])
                    all_results.append(r)
        except Exception as e:
            print(f"  {name}: error - {e}")
    
    # 按引擎优先级排序（保留原始顺序）
    engine_order = {n: i for i, n in enumerate(engine_names)}
    all_results.sort(key=lambda r: engine_order.get(r.get("engine"), 99))
    
    _cache_set(ck, all_results)
    print(f"  总计: {len(all_results)} 条 (去重后)")
    return all_results[:count]

# ==============================
# CLI
# ==============================
if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or "Saudi Arabia reconstruction 2026"
    engines_sel = sys.argv[2:] if len(sys.argv) > 2 else None
    
    print("=" * 50)
    print("太一轻量 SearXNG v1.0")
    print("=" * 50)
    
    results = search(query, 10, engines_sel)
    print(f"\n{'='*50}")
    print(f"结果: {len(results)} 条")
    print(f"{'='*50}")
    for r in results:
        print(f"  [{r.get('engine','?')}] [{r['title'][:55]}]")
        print(f"        {r['url'][:70]}")
        if r.get("snippet"):
            print(f"        {r['snippet'][:100]}")
        print()

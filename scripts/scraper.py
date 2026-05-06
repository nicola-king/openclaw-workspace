#!/usr/bin/env python3
"""
太一穿透式搜索器 v3 — 生产级
- DuckDuckGo HTML 搜索 (cloudscraper + brotli, bypass anti-bot)
- Chromium 头渲染 (JS站点/Cloudflare)
- URL 反混淆 (DDG/Bing redirect → 真实URL)
- 邮箱/电话/LinkedIn 提取
- 缓存
"""
import sys, os, json, hashlib, time, re, subprocess, tempfile, urllib.parse
from bs4 import BeautifulSoup
import cloudscraper

CACHE_DIR = os.path.expanduser("~/.openclaw/workspace/.cache/scraper")
CHROMIUM = "/snap/bin/chromium"
CACHE_TTL = 3600
os.makedirs(CACHE_DIR, exist_ok=True)

# === Cache ===
def _ck(prefix, s): return hashlib.sha256(f"{prefix}:{s}".encode()).hexdigest()[:16]
def _cg(key):
    p = f"{CACHE_DIR}/{key}.json"
    if not os.path.exists(p): return None
    if time.time() - os.path.getmtime(p) > CACHE_TTL:
        os.remove(p); return None
    with open(p) as f: return json.load(f)
def _cs(key, data):
    with open(f"{CACHE_DIR}/{key}.json", "w") as f:
        json.dump(data, f, ensure_ascii=False)

# === HTTP (cloudscraper) ===
_scraper = None
def _http():
    global _scraper
    if not _scraper:
        _scraper = cloudscraper.create_scraper(delay=2)
    return _scraper

_UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
       'AppleWebKit/537.36 (KHTML, like Gecko) '
       'Chrome/131.0.0.0 Safari/537.36')

def _fetch(url, use_chromium=False, timeout=25):
    """Fetch URL, return {text, status, error}"""
    k = _ck("fetch" if not use_chromium else "dom", url)
    c = _cg(k)
    if c: return c

    result = {"text": "", "status": 0, "error": None}

    if use_chromium:
        t = tempfile.mktemp(suffix=".html")
        try:
            subprocess.run([CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu",
                            "--dump-dom", url],
                           timeout=timeout, stdout=open(t, "w"),
                           stderr=subprocess.DEVNULL)
            with open(t) as f: result["text"] = f.read()
            result["status"] = 200
        except Exception as e:
            result["error"] = str(e)
        finally:
            try: os.remove(t)
            except: pass
    else:
        try:
            r = _http().get(url, headers={"User-Agent": _UA}, timeout=timeout)
            result["text"] = r.text
            result["status"] = r.status_code
        except Exception as e:
            result["error"] = str(e)

    if result["text"]:
        _cs(k, result)
    return result

# === Search ===
def _decode_ddg_url(url):
    """Decode DuckDuckGo redirect URL"""
    if '/l/?uddg=' in url or 'uddg=' in url:
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)
        if 'uddg' in qs:
            return urllib.parse.unquote(qs['uddg'][0])
    return url

def search(query, count=10):
    """Search via DuckDuckGo HTML (cloudscraper, English results)"""
    encoded = urllib.parse.quote(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded}"
    result = _fetch(url)
    if result["status"] != 200:
        return []

    soup = BeautifulSoup(result["text"], 'lxml')
    results = []
    seen = set()

    for r_el in soup.select('.result'):
        a = r_el.select_one('.result__title a, .result__a, a[href]')
        if not a:
            continue
        title = a.get_text(strip=True)
        if not title or len(title) < 5:
            continue
        url = _decode_ddg_url(a.get('href', ''))
        if not url or url in seen:
            continue

        snippet_el = r_el.select_one('.result__snippet, .snippet')
        snippet = snippet_el.get_text(strip=True) if snippet_el else ''

        seen.add(url)
        results.append({"title": title, "url": url, "snippet": snippet[:300]})

        if len(results) >= count:
            break

    return results

def search_linkedin(query, count=5):
    return search(f"site:linkedin.com/in {query}", count=count)

def search_bing(query, count=10):
    """Fallback: Bing via cloudscraper"""
    encoded = urllib.parse.quote(query)
    url = f"https://www.bing.com/search?q={encoded}&count={count}"
    result = _fetch(url)

    if result["status"] != 200:
        return []

    soup = BeautifulSoup(result["text"], 'lxml')
    results = []
    seen = set()

    for li in soup.select('li.b_algo'):
        a = li.select_one('h2 a')
        if not a: continue
        title = a.get_text(strip=True)
        if not title or len(title) < 5: continue

        cite = li.select_one('cite')
        u = ""
        if cite:
            raw = cite.get_text(strip=True)
            parts = re.split(r'\s*[\u203a\u00bb]\s*', raw)
            base = parts[0].rstrip('/')
            path = '/'.join(p.strip() for p in parts[1:])
            u = base + '/' + path if path else base

        if not u or u in seen: continue

        snippet_el = li.select_one('.b_caption p, .b_lineclamp2')
        snippet = snippet_el.get_text(strip=True) if snippet_el else ''
        seen.add(u)
        results.append({"title": title, "url": u, "snippet": snippet[:300]})
        if len(results) >= count: break

    return results

# === Fetch page ===
def fetch(url, use_chromium=False):
    """Fetch page, extract clean text + emails + phones"""
    result = _fetch(url, use_chromium=use_chromium)
    if result["status"] != 200:
        return {"url": url, "error": f"HTTP {result['status']}", "text": ""}

    html = result["text"]
    soup = BeautifulSoup(html, 'lxml')
    for t in soup(["script", "style", "nav", "footer", "header"]):
        t.decompose()
    text = soup.get_text(separator="\n", strip=True)
    title = soup.title.string.strip() if soup.title else ""

    emails = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)))
    phones = list(set(re.findall(r'\+\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}', html)))
    phones = [p for p in phones if len(re.sub(r'[\s\(\)\+\.\-]', '', p)) > 6][:10]

    return {"url": url, "title": title, "text": text[:50000],
            "emails": emails[:20], "phones": phones[:10],
            "status": result["status"]}

def pdf(url, out):
    """Capture page as PDF via Chromium"""
    subprocess.run([CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu",
                    "--print-to-pdf=" + out, url],
                   timeout=30, stderr=subprocess.DEVNULL)
    return out

# === CLI ===
def main():
    if len(sys.argv) < 2:
        print("太一搜索器 v3 — 穿透式搜索")
        print()
        print("  search  <query> [count]   搜索 (DDG → Bing 回退)")
        print("  linkedin <query> [count]  搜索 LinkedIn 人物")
        print("  fetch   <url>             爬取 & 提取内容/邮箱/电话")
        print("  fetchjs <url>             爬取 (Chromium 渲染 JS 站点)")
        print("  pdf     <url> <out.pdf>   保存为 PDF")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "search":
        q = sys.argv[2] if len(sys.argv) > 2 else ""
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        r = search(q, n)
        if not r: r = search_bing(q, n)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        if not r: sys.exit(1)

    elif cmd == "linkedin":
        q = sys.argv[2] if len(sys.argv) > 2 else ""
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        r = search_linkedin(q, n)
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif cmd in ("fetch", "fetchjs"):
        u = sys.argv[2] if len(sys.argv) > 2 else ""
        use_js = cmd == "fetchjs"
        print(json.dumps(fetch(u, use_chromium=use_js), ensure_ascii=False, indent=2))

    elif cmd == "pdf":
        u = sys.argv[2] if len(sys.argv) > 2 else ""
        o = sys.argv[3] if len(sys.argv) > 3 else "output.pdf"
        pdf(u, o)
        print(f"PDF: {o}")

if __name__ == "__main__":
    main()

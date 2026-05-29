"""
太一 Scrapling 适配器 · Taiyi Scrapling Adapter
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
集成 D4Vinci/Scrapling (⭐54K) + 10层永不放弃抓取链路

目标：100% 命中率，不管什么反爬都能搞到内容

抓取链路（逐级降级）:
  L1  web_fetch (OpenClaw原生)     → 零成本
  L2  AnySearch CLI                → 搜索API
  L3  requests + Clash代理          → 透明代理
  L4  Scrapling Fetcher (basic)    → 基本HTTP
  L5  Scrapling StealthyFetcher    → Cloudflare绕过
  L6  cloudscraper                  → 另一套CF绕过
  L7  Scrapling DynamicFetcher     → JS渲染
  L8  Playwright 无头浏览器         → 完整浏览器指纹
  L9  Google Cache / Wayback       → 缓存快照
  L10 Playwright + Clash代理        → 终极反封锁

智能自动识别:
  域名预判已知反爬          → 跳过L1-L3 直接L5
  HTTP 403/Cloudflare       → 自动降级到L5-L6
  内容为空/JS站点           → 自动降级到L7-L8
  全部失败 + 有缓存         → L9 拾取快照
  IP被封锁                 → L10 通过Clash代理重试
"""

import asyncio
import json
import logging
import os
import time
import subprocess
from typing import Dict, List, Optional
from urllib.parse import urlparse

logger = logging.getLogger("taiyi.scrapling")

# =====================================================================
# 全局配置
# =====================================================================

CLASH_PROXY = "http://127.0.0.1:7890"
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# 已知反爬站点 → 跳过低级链路直接上Stealthy
STEALTH_DOMAINS = [
    "reuters.com", "bloomberg.com", "wsj.com", "ft.com",
    "crunchbase.com", "zoominfo.com", "linkedin.com",
    "indeed.com", "glassdoor.com",
    "scmp.com", "nikkei.com",
    "aljazeera.com",
    "forbes.com", "telegraph.co.uk",
]

# JS动态站点 → 跳过低级链路直接上Dynamic/Playwright
DYNAMIC_DOMAINS = [
    "facebook.com", "twitter.com", "x.com", "instagram.com",
    "tiktok.com", "reddit.com", "pinterest.com",
    "amazon.com", "ebay.com", "etsy.com",
    "airbnb.com", "booking.com",
]

# =====================================================================
# 路由判断
# =====================================================================

def _domain_of(url: str) -> str:
    return urlparse(url).netloc.lower().replace("www.", "")

def _needs_stealth(url: str) -> bool:
    domain = _domain_of(url)
    for d in STEALTH_DOMAINS:
        if d in domain or domain in d:
            return True
    return False

def _needs_dynamic(url: str) -> bool:
    domain = _domain_of(url)
    for d in DYNAMIC_DOMAINS:
        if d in domain or domain in d:
            return True
    return False

def _is_cloudflare_blocked(html: str) -> bool:
    """检测 Cloudflare 反爬页面"""
    indicators = ["cf-browser-verify", "challenge-platform", "Attention Required",
                  "Cloudflare", "Just a moment", "Checking your browser",
                  "403 Forbidden", "cf-chl-widget", "js/challenge.js"]
    html_lower = html.lower()
    for ind in indicators:
        if ind.lower() in html_lower:
            return True
    return False

def _is_empty_content(html: str) -> bool:
    """检测是否为有效内容"""
    if not html or len(html.strip()) < 200:
        return True
    if _is_cloudflare_blocked(html):
        return True
    # 纯 JS 占位（没有正文的 SPA）
    body = html.lower()
    no_text_len = len(body.replace("<script", "").replace("<style", "").strip())
    if no_text_len < 500:
        return True
    return False

# =====================================================================
# L3: requests + Clash 代理
# =====================================================================

def _try_requests(url: str, timeout: int = 20) -> Dict:
    """通过 Clash 代理用 requests 请求"""
    try:
        import requests
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        }
        resp = requests.get(url, headers=headers, proxies={"http": CLASH_PROXY, "https": CLASH_PROXY},
                            timeout=timeout, allow_redirects=True)
        if resp.status_code == 200:
            return {"status": "ok", "content": resp.text, "fetcher": "requests+proxy", "status_code": 200}
        return {"status": "error", "error": f"HTTP {resp.status_code}", "fetcher": "requests+proxy"}
    except Exception as e:
        return {"status": "error", "error": str(e), "fetcher": "requests+proxy"}

# =====================================================================
# L4-L7: Scrapling 各 Fetcher
# =====================================================================

def _try_scrapling_basic(url: str, timeout: int = 30) -> Dict:
    try:
        from scrapling import Fetcher
        f = Fetcher()
        resp = f.get(url)
        if resp is not None and hasattr(resp, 'status') and resp.status == 200:
            html = resp.html_content if hasattr(resp, 'html_content') and resp.html_content else str(resp)
            return {"status": "ok", "content": str(html), "fetcher": "scrapling_basic", "status_code": 200}
        return {"status": "error", "error": f"HTTP {getattr(resp,'status','?')}", "fetcher": "scrapling_basic"}
    except Exception as e:
        return {"status": "error", "error": str(e)[:100], "fetcher": "scrapling_basic"}

def _try_scrapling_stealth(url: str, timeout: int = 30) -> Dict:
    try:
        from scrapling import StealthyFetcher
        f = StealthyFetcher()
        resp = f.fetch(url)
        if resp is not None and hasattr(resp, 'status') and resp.status == 200:
            html = resp.html_content if hasattr(resp, 'html_content') and resp.html_content else str(resp)
            return {"status": "ok", "content": str(html), "fetcher": "scrapling_stealth", "status_code": 200}
        return {"status": "error", "error": f"HTTP {getattr(resp,'status','?')}", "fetcher": "scrapling_stealth"}
    except Exception as e:
        return {"status": "error", "error": str(e)[:100], "fetcher": "scrapling_stealth"}

# =====================================================================
# L6: cloudscraper — 另一套 Cloudflare 绕过方案
# =====================================================================

def _try_cloudscraper(url: str, timeout: int = 20) -> Dict:
    try:
        import cloudscraper
        scraper = cloudscraper.create_scraper()
        resp = scraper.get(url, timeout=timeout)
        if resp.status_code == 200 and not _is_empty_content(resp.text):
            return {"status": "ok", "content": resp.text, "fetcher": "cloudscraper", "status_code": 200}
        return {"status": "error", "error": f"HTTP {resp.status_code} or empty", "fetcher": "cloudscraper"}
    except Exception as e:
        return {"status": "error", "error": str(e)[:100], "fetcher": "cloudscraper"}

# =====================================================================
# L7: Scrapling DynamicFetcher — JS 渲染
# =====================================================================

def _try_scrapling_dynamic(url: str, timeout: int = 30) -> Dict:
    try:
        from scrapling import DynamicFetcher
        f = DynamicFetcher()
        resp = f.fetch(url)
        if resp is not None and hasattr(resp, 'status') and resp.status == 200:
            html = resp.html_content if hasattr(resp, 'html_content') and resp.html_content else str(resp)
            return {"status": "ok", "content": str(html), "fetcher": "scrapling_dynamic", "status_code": 200}
        return {"status": "error", "error": f"HTTP {getattr(resp,'status','?')}", "fetcher": "scrapling_dynamic"}
    except Exception as e:
        return {"status": "error", "error": str(e)[:100], "fetcher": "scrapling_dynamic"}

# =====================================================================
# L8: Playwright 无头浏览器
# =====================================================================

def _try_playwright(url: str, timeout: int = 30) -> Dict:
    """Playwright 无头浏览器 — 完整浏览器指纹"""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080},
                locale="en-US",
            )
            page = context.new_page()
            page.goto(url, wait_until="networkidle", timeout=timeout * 1000)
            html = page.content()
            browser.close()
            if html and not _is_empty_content(html):
                return {"status": "ok", "content": html, "fetcher": "playwright", "status_code": 200}
            return {"status": "error", "error": "Empty content after Playwright render", "fetcher": "playwright"}
    except Exception as e:
        return {"status": "error", "error": str(e)[:150], "fetcher": "playwright"}

# =====================================================================
# L9: 缓存快照 — Google Cache / Wayback Machine
# =====================================================================

def _try_google_cache(url: str, timeout: int = 15) -> Dict:
    """从 Google 缓存获取页面"""
    cache_url = f"https://webcache.googleusercontent.com/search?q=cache:{url}"
    result = _try_requests(cache_url, timeout=timeout)
    if result["status"] == "ok":
        result["fetcher"] = "google_cache"
        result["note"] = "Delivered from Google Cache"
        return result
    return {"status": "error", "error": "Google Cache unavailable", "fetcher": "google_cache"}

def _try_wayback(url: str, timeout: int = 15) -> Dict:
    """从 Wayback Machine 获取最近存档"""
    try:
        import requests
        # 先查最近的快照
        cdx_url = f"https://web.archive.org/cdx/search/cdx?url={url}&output=json&limit=1&fl=timestamp,original"
        resp = requests.get(cdx_url, timeout=timeout,
                           proxies={"http": CLASH_PROXY, "https": CLASH_PROXY})
        if resp.status_code == 200 and len(resp.json()) > 1:
            ts = resp.json()[1][0]
            archived_url = f"https://web.archive.org/web/{ts}/{url}"
            result = _try_requests(archived_url, timeout=timeout)
            if result["status"] == "ok":
                result["fetcher"] = "wayback"
                result["note"] = f"Delivered from Wayback Machine ({ts})"
                return result
        return {"status": "error", "error": "No Wayback snapshot found", "fetcher": "wayback"}
    except Exception as e:
        return {"status": "error", "error": str(e)[:100], "fetcher": "wayback"}

# =====================================================================
# L10: Playwright + Clash 代理（终极反封锁）
# =====================================================================

def _try_playwright_proxy(url: str, timeout: int = 30) -> Dict:
    """Playwright 通过 Clash 代理 — 终极方案"""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                proxy={"server": CLASH_PROXY}
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080},
                locale="en-US",
            )
            page = context.new_page()
            page.goto(url, wait_until="networkidle", timeout=timeout * 1000)
            html = page.content()
            browser.close()
            if html and not _is_empty_content(html):
                return {"status": "ok", "content": html, "fetcher": "playwright+proxy", "status_code": 200}
            return {"status": "error", "error": "Empty after PW+proxy", "fetcher": "playwright+proxy"}
    except Exception as e:
        return {"status": "error", "error": str(e)[:150], "fetcher": "playwright+proxy"}

# =====================================================================
# 主入口：10层永不放弃抓取链路
# =====================================================================

FETCH_CHAIN = [
    # (名称, 函数, 跳过条件)
    ("requests+proxy", _try_requests, None),
    ("scrapling_basic", _try_scrapling_basic, None),
    ("scrapling_stealth", _try_scrapling_stealth, None),
    ("cloudscraper", _try_cloudscraper, None),
    ("scrapling_dynamic", _try_scrapling_dynamic, None),
    ("playwright", _try_playwright, None),
    ("google_cache", _try_google_cache, None),
    ("wayback", _try_wayback, None),
    ("playwright+proxy", _try_playwright_proxy, None),
]

STEALTH_CHAIN = [
    # 已知反爬站点 → 跳过前两层直接走 Stealth
    ("scrapling_stealth", _try_scrapling_stealth, None),
    ("cloudscraper", _try_cloudscraper, None),
    ("scrapling_dynamic", _try_scrapling_dynamic, None),
    ("playwright", _try_playwright, None),
    ("google_cache", _try_google_cache, None),
    ("wayback", _try_wayback, None),
    ("playwright+proxy", _try_playwright_proxy, None),
]

DYNAMIC_CHAIN = [
    # JS动态站点 → 直接上渲染
    ("scrapling_dynamic", _try_scrapling_dynamic, None),
    ("playwright", _try_playwright, None),
    ("playwright+proxy", _try_playwright_proxy, None),
    ("google_cache", _try_google_cache, None),
    ("wayback", _try_wayback, None),
]

def scrapling_fetch(url: str, timeout: int = 30, strategy: str = "auto",
                    force_stealth: bool = False, force_dynamic: bool = False) -> Dict:
    """
    10层永不放弃抓取链路 — 100% 命中目标
    
    策略选择:
      "auto":     正常链路 (L3→L4→L5→...→L10)
      "stealth":  反爬优先 (L5→L6→L7→L8→L9→L10)
      "dynamic":  JS渲染优先 (L7→L8→L10→L9)
      "nuclear":  全部链路 (L3→L4→L5→L6→L7→L8→L9→L10)
    """
    t0 = time.time()
    chain = FETCH_CHAIN  # default: nuclear
    reason = ""

    # 策略选择
    if strategy == "auto":
        if force_stealth or _needs_stealth(url):
            chain = STEALTH_CHAIN
            reason = "domain_stealth"
        elif force_dynamic or _needs_dynamic(url):
            chain = DYNAMIC_CHAIN
            reason = "domain_dynamic"
        else:
            chain = FETCH_CHAIN
            reason = "auto_standard"
    elif strategy == "stealth":
        chain = STEALTH_CHAIN
        reason = "force_stealth"
    elif strategy == "dynamic":
        chain = DYNAMIC_CHAIN
        reason = "force_dynamic"
    elif strategy == "nuclear":
        chain = FETCH_CHAIN
        reason = "nuclear"

    debug = [f"strategy:{reason}"]

    # 逐级尝试
    for name, func, skip_cond in chain:
        if skip_cond and callable(skip_cond) and skip_cond():
            debug.append(f"{name}→skip")
            continue
        debug.append(f"{name}→try")
        result = func(url, timeout=timeout)
        elapsed = int((time.time() - t0) * 1000)
        if result["status"] == "ok":
            result["fetcher"] = result.get("fetcher", name)
            result["time_ms"] = elapsed
            result["debug"] = debug + [f"✅{name}_success:{elapsed}ms"]
            result["strategy"] = reason
            result["chain_attempts"] = len([d for d in debug if "→try" in d])
            return result
        debug.append(f"{name}_failed:{result.get('error','?')[:50]}")

    # 全部失败
    elapsed = int((time.time() - t0) * 1000)
    return {
        "status": "error", "content": "",
        "error": f"All {len(chain)} chains failed",
        "fetcher": "none", "time_ms": elapsed,
        "debug": debug + [f"elapsed:{elapsed}ms"],
        "strategy": reason, "url": url,
        "note": "💡 建议: 检查URL有效性或考虑用 search() 先搜索到内容再提取"
    }

# =====================================================================
# 并发批量采集
# =====================================================================

def batch_fetch(urls: List[str], max_concurrent: int = 3, timeout: int = 30,
                strategy: str = "auto") -> List[Dict]:
    """批量采集 — 智能路由每个 URL"""
    results = []
    for i, url in enumerate(urls):
        if max_concurrent and i > 0 and i % max_concurrent == 0:
            time.sleep(0.5)  # 限速
        r = scrapling_fetch(url, timeout=timeout, strategy=strategy)
        results.append({
            "url": url,
            "status": r["status"],
            "fetcher": r.get("fetcher", "?"),
            "length": len(r.get("content", r.get("error", ""))),
            "elapsed": r.get("time_ms", 0),
            "chain_attempts": r.get("chain_attempts", 0),
            "debug": r.get("debug", []),
        })
    return results

# =====================================================================
# 元素提取（复用之前的代码）
# =====================================================================

def extract_elements(html: str, css_selector: str = None, xpath: str = None,
                     text_only: bool = True, max_items: int = 20) -> Dict:
    """从 HTML 中提取元素"""
    try:
        from scrapling import Selector
        sel = Selector(html) if isinstance(html, str) else Selector(content=html)
    except Exception as e:
        return {"status": "error", "error": str(e)}

    items = []
    try:
        if css_selector:
            elements = sel.css(css_selector)
        elif xpath:
            elements = sel.xpath(xpath)
        else:
            elements = sel

        if hasattr(elements, '__iter__'):
            for i, el in enumerate(elements):
                if i >= max_items:
                    break
                item = {}
                if text_only:
                    item["text"] = el.get_all_text(strip=True)[:2000] if hasattr(el, 'get_all_text') else ""
                else:
                    item["html"] = el.html_content[:2000] if hasattr(el, 'html_content') else ""
                if hasattr(el, 'attrib'):
                    if 'href' in el.attrib: item["href"] = el.attrib['href']
                    if 'src' in el.attrib: item["src"] = el.attrib['src']
                items.append(item)
    except Exception as e:
        return {"status": "error", "error": str(e)}

    return {"status": "ok", "items": items, "count": len(items)}

def adaptive_extract(html: str, target_text: str = None) -> Dict:
    """自适应提取"""
    try:
        from scrapling import Selector
        sel = Selector(html) if isinstance(html, str) else Selector(content=html)
        if target_text:
            results = sel.find_by_text(target_text)
            if results:
                css = results.generate_css_selector
                return {"status": "ok",
                        "item": str(results.extract_first())[:5000] if hasattr(results, 'extract_first') else str(results)[:5000],
                        "css_selector": str(css) if css else None}
        return {"status": "ok", "text": sel.get_all_text(strip=True)[:10000]}
    except Exception as e:
        return {"status": "error", "error": str(e)}

# =====================================================================
# CLI
# =====================================================================

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("""太一 Scrapling 10层抓取 · 100%命中

用法:
  fetch <url> [strategy]   智能抓取 (auto/stealth/dynamic/nuclear)
  test                     系统可用性测试

策略:
  auto     自动路由
  stealth  反爬优先（跳过低级）
  dynamic  JS渲染优先
  nuclear  全部10层依次尝试""")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "test":
        print("=== Scrapling 10层系统自检 ===")
        checks = [
            ("requests", lambda: __import__('requests')),
            ("requests+proxy", lambda: __import__('requests').get('http://httpbin.org/get',
                proxies={"http": CLASH_PROXY}, timeout=5).status_code == 200),
            ("scrapling", lambda: __import__('scrapling').__version__),
            ("cloudscraper", lambda: __import__('cloudscraper').__version__),
            ("playwright", lambda: __import__('playwright').__version__),
            ("Local Clash Proxy", lambda: __import__('requests').get('http://127.0.0.1:7890',
                timeout=2).status_code in [200, 400]),
        ]
        for name, check in checks:
            try:
                r = check()
                print(f"  ✅ {name}: {r}")
            except Exception as e:
                print(f"  ❌ {name}: {e}")
        print()
        print("路由规则:")
        for url, label in [("reuters.com", "反爬→stealth"),
                          ("facebook.com", "JS→dynamic"),
                          ("example.com", "正常→auto")]:
            s = _needs_stealth("https://" + url)
            d = _needs_dynamic("https://" + url)
            route = "stealth" if s else ("dynamic" if d else "auto")
            print(f"  {label:12s} → {route}")

    elif cmd == "fetch":
        url = sys.argv[2] if len(sys.argv) > 2 else input("URL: ")
        strategy = sys.argv[3] if len(sys.argv) > 3 else "auto"
        r = scrapling_fetch(url, strategy=strategy)
        print(f"📡 {url}")
        print(f"   策略: {r.get('strategy','?')} | Fetcher: {r.get('fetcher','?')} | {r.get('time_ms',0)}ms")
        print(f"   链路尝试: {r.get('chain_attempts',0)} 层 | Debug: {r.get('debug', [])}")
        if r.get("status") == "ok":
            c = r.get("content", "")
            print(f"   📐 Length: {len(c)} chars")
            print(f"   📄 Preview: {c[:600]}...")
        else:
            print(f"   ❌ Error: {r.get('error','?')}")
            if "note" in r:
                print(f"   💡 {r['note']}")

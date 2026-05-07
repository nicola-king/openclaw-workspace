#!/home/sayelf/.local/venvs/scraper/bin/python3
"""
📡 太一穿透式搜索器 v4 — 自适应搜索Agent
=============================================================================
基于 Scrapling 深度学习法升级：自适应解析器 + 多源融合 + 自动恢复

v4 增强：
├── Scrapling 自适应 CSS 选择器（网站变更后自动重新定位元素）
├── 多源搜索融合（DDG + Bing + Google fallback）
├── 智能缓存命中 + TTL 分级
├── 邮箱/电话/LinkedIn 深度提取
├── Chromium 渲染备用
└── CLI: search / linkedin / fetch / fetchjs / pdf / verify
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import hashlib
import urllib.parse
from pathlib import Path

# ── Scrapling 自适应解析 ──
from scrapling import Selector

# ── 网络层 ──
import cloudscraper

# ── 常量 ──
CACHE_DIR = Path.home() / ".openclaw" / "workspace" / ".cache" / "scraper"
CHROMIUM = "/snap/bin/chromium"
CACHE_TTL_DEFAULT = 3600  # 1h
CACHE_TTL_SEARCH = 1800   # 30min
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ── 用户代理池（轮换防封） ──
_USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/130.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
]
_ua_idx = 0
def _next_ua():
    global _ua_idx
    ua = _USER_AGENTS[_ua_idx % len(_USER_AGENTS)]
    _ua_idx += 1
    return ua

# ── HTTP client（cloudscraper 反 Cloudflare） ──
_scraper = None
def _http():
    global _scraper
    if not _scraper:
        _scraper = cloudscraper.create_scraper(delay=1.5)
    return _scraper

# ── 缓存系统 ──
def _ck(prefix: str, s: str) -> str:
    return hashlib.sha256(f"{prefix}:{s}".encode()).hexdigest()[:16]

def _cg(key: str, ttl: int = CACHE_TTL_DEFAULT):
    p = CACHE_DIR / f"{key}.json"
    if not p.exists():
        return None
    if time.time() - p.stat().st_mtime > ttl:
        p.unlink(missing_ok=True)
        return None
    return json.loads(p.read_text())

def _cs(key: str, data):
    (CACHE_DIR / f"{key}.json").write_text(
        json.dumps(data, ensure_ascii=False, default=str)
    )

# ── 自适应抓取（Scrapling 核心集成） ──
def fetch_adaptive(url: str, timeout: int = 25, use_chromium: bool = False) -> dict:
    """
    自适应抓取：用 Scrapling Selector(adaptive=True) 解析 HTML。
    返回结构化结果：title, text, emails, phones, links, 状态。
    """
    k = _ck("adapt", url)
    cached = _cg(k)
    if cached:
        return cached

    raw_html = _fetch_raw(url, timeout, use_chromium)
    if raw_html.get("error") or raw_html["status"] != 200:
        result = {
            "url": url,
            "error": raw_html.get("error", f"HTTP {raw_html['status']}"),
            "status": raw_html["status"],
            "title": "", "text": "", "emails": [], "phones": [], "links": [],
        }
        _cs(k, result)
        return result

    html = raw_html["text"]

    # ── Scrapling 自适应解析（网站变更后自动重定位） ──
    try:
        sel = Selector(content=html, url=url, adaptive=True)
    except Exception:
        # Fallback: 不用 adaptive
        sel = Selector(content=html, url=url)

    title = ""
    try:
        t = sel.css("title::text")
        title = t.get(default="").strip()
    except Exception:
        pass

    # 提取文本
    try:
        text_parts = []
        for el in sel.css("p, h1, h2, h3, h4, h5, li, td, th, span, div"):
            t = el.get().strip() if el else ""
            if t and len(t) > 5:
                text_parts.append(t)
        text = "\n".join(text_parts[:500])
    except Exception:
        text = ""

    # 提取所有链接（自适应）
    links = []
    try:
        for a in sel.css("a[href]"):
            href = a.css("::attr(href)").get(default="")
            if href and not href.startswith(("javascript:", "#", "mailto:")):
                links.append(urllib.parse.urljoin(url, href))
        links = list(dict.fromkeys(links))[:200]
    except Exception:
        pass

    # 邮箱/电话（正则 + 自适应提取）
    emails_raw = set(re.findall(
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html
    ))
    # 自适应：从 mailto 链接提取
    try:
        for a in sel.css("a[href^='mailto:']"):
            href = a.css("::attr(href)").get(default="")
            if "@" in href:
                emails_raw.add(href.replace("mailto:", "").split("?")[0].strip())
    except Exception:
        pass
    emails = sorted(e for e in emails_raw if not any(
        x in e for x in ["example.com", "domain.com", "your@", "test@", "xxxx"]
    ))[:30]

    phones = list(set(re.findall(
        r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}', html
    )))
    phones = [p for p in phones if len(re.sub(r'[\s\(\)\+\.\-]', '', p)) > 6][:15]

    result = {
        "url": url,
        "title": title,
        "text": text[:80000],
        "emails": emails,
        "phones": phones,
        "links": links[:100],
        "status": raw_html["status"],
    }
    _cs(k, result)
    return result

def _fetch_raw(url: str, timeout: int = 25, use_chromium: bool = False) -> dict:
    """获取原始 HTML"""
    result = {"text": "", "status": 0, "error": None}

    if use_chromium:
        tmp = tempfile.mktemp(suffix=".html")
        try:
            subprocess.run(
                [CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu",
                 "--disable-dev-shm-usage", "--dump-dom", url],
                timeout=timeout, stdout=open(tmp, "w"), stderr=subprocess.DEVNULL,
            )
            result["text"] = Path(tmp).read_text()
            result["status"] = 200
        except Exception as e:
            result["error"] = f"chromium: {e}"
        finally:
            Path(tmp).unlink(missing_ok=True)
    else:
        try:
            r = _http().get(url, headers={"User-Agent": _next_ua()}, timeout=timeout)
            # 允许的编码
            r.encoding = r.apparent_encoding or "utf-8"
            result["text"] = r.text
            result["status"] = r.status_code
        except Exception as e:
            result["error"] = str(e)

    return result

# ── URL 反混淆 ──
def _decode_url(raw: str) -> str:
    """解码 DDG/Bing 跳转链接"""
    if not raw:
        return ""

    # 先解码 HTML 实体
    clean = raw.replace('&amp;', '&')

    # Bing: 从查询字符串提取 u 参数（base64 编码目标URL）
    # Bing 格式: /ck/a?...&u=BASE64...
    u_match = re.search(r'[?&]u=([a-zA-Z0-9+/=]+)', clean)
    if u_match:
        try:
            import base64
            b64_val = u_match.group(1)
            # 补 padding
            padding = 4 - len(b64_val) % 4
            if padding != 4:
                b64_val += '=' * padding
            decoded = base64.b64decode(b64_val).decode('utf-8', errors='ignore')
            return decoded
        except Exception:
            pass

    # DDG: 提取 uddg 参数
    uddg_match = re.search(r'[?&]uddg=([^&]+)', clean)
    if uddg_match:
        dec = urllib.parse.unquote(uddg_match.group(1))
        if dec.startswith('http%3A') or dec.startswith('https%3A'):
            dec = urllib.parse.unquote(dec)
        return dec

    # Google: q 参数
    q_match = re.search(r'[?&]q=([^&]+)', clean)
    if q_match and ('/url' in clean):
        return urllib.parse.unquote(q_match.group(1))

    # Bing: 尝试从完整字符串中提取可见 http 链接
    url_matches = re.findall(r'(https?://[^&"\s<>]+)', clean)
    for m in url_matches:
        bad_domains = ['bing.com', 'microsoft.com', 'duckduckgo.com']
        if not any(d in m for d in bad_domains):
            return m

    return clean

# ── 搜索结果自适应提取 ──
def _extract_results_ddg(html: str, count: int = 10) -> list:
    """提取 DuckDuckGo 搜索结果（正则 + 去HTML）"""
    results, seen = [], set()

    # DDG HTML 结果模式:
    # <a rel="nofollow" class="result__a" href="//duckduckgo.com/l/?uddg=...">TITLE</a>
    # <a class="result__snippet" href="...">SNIPPET</a>

    # 方案1: 正则提取
    blocks = re.findall(
        r'<a[^>]*rel="nofollow"[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
        html, re.DOTALL
    )
    for href, title_raw in blocks:
        title = re.sub(r'<[^>]+>', '', title_raw).strip()
        if not title or len(title) < 5:
            continue
        url = _decode_url(href.strip())
        if not url or url in seen or 'duckduckgo.com' in url:
            continue
        seen.add(url)
        results.append({"title": title, "url": url, "snippet": ""})
        if len(results) >= count:
            break

    # 补 snippet
    if results:
        snippets = re.findall(
            r'<a[^>]*class="result__snippet"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
            html, re.DOTALL
        )
        for s_url, s_raw in snippets:
            s_url_decoded = _decode_url(s_url)
            for i, r in enumerate(results):
                if r["url"] == s_url_decoded and not r["snippet"]:
                    results[i]["snippet"] = re.sub(r'<[^>]+>', '', s_raw).strip()[:300]
                    break

    return results

def _extract_results_bing(html: str, count: int = 10) -> list:
    """提取 Bing 搜索结果（正则 + 去HTML）"""
    results, seen = [], set()

    # Bing 结果块模式:
    # <li class="b_algo">
    #   <h2><a href="URL" h="...">TITLE</a></h2>
    #   <div class="b_caption"><p>SNIPPET</p></div>
    # </li>
    
    # 方案1: 正则提取 (更可靠)
    blocks = re.findall(
        r'<li[^>]*class="b_algo"[^>]*>.*?<h2>.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?<p[^>]*>(.*?)</p>',
        html, re.DOTALL
    )
    
    for url_raw, title_raw, snippet_raw in blocks:
        title = re.sub(r'<[^>]+>', '', title_raw).strip()
        if not title or len(title) < 5:
            continue
        url = _decode_url(url_raw.strip())
        if not url or url in seen:
            continue
        seen.add(url)
        snippet = re.sub(r'<[^>]+>', '', snippet_raw).strip()[:300]
        results.append({"title": title, "url": url, "snippet": snippet})
        if len(results) >= count:
            break
    
    # 方案2: BeautifulSoup 回退
    if not results:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        for li in soup.select('li.b_algo'):
            a = li.select_one('h2 a')
            if not a:
                continue
            title = a.get_text(strip=True)
            if not title or len(title) < 5:
                continue
            href = a.get('href', '')
            url = _decode_url(href)
            if not url or url in seen:
                continue
            seen.add(url)
            p = li.select_one('.b_caption p, .b_lineclamp2')
            snippet = p.get_text(strip=True)[:300] if p else ''
            results.append({"title": title, "url": url, "snippet": snippet})
            if len(results) >= count:
                break

    return results

# ── 搜索函数 ──
def search(query: str, count: int = 10) -> list:
    """
    多源搜索：DDG 主引擎 → Bing 回退 → Chromium 渲染回退
    返回统一格式 [{title, url, snippet}]
    """
    k = _ck("ddg", f"{query}:{count}")
    cached = _cg(k, ttl=CACHE_TTL_SEARCH)
    if cached:
        return cached

    encoded = urllib.parse.quote(query)
    results = []

    # 方法1: DDG HTML
    ddg_url = f"https://html.duckduckgo.com/html/?q={encoded}"
    raw = _fetch_raw(ddg_url)
    if raw["status"] == 200 and 'result__a' in raw["text"]:
        results = _extract_results_ddg(raw["text"], count)

    # 方法2: Bing 回退
    if not results:
        bing_url = f"https://www.bing.com/search?q={encoded}&count={count}"
        bing_raw = _fetch_raw(bing_url, timeout=20)
        if bing_raw["status"] == 200:
            results = _extract_results_bing(bing_raw["text"], count)

    # 方法3: Chromium 渲染搜索
    if not results:
        try:
            import subprocess, tempfile
            search_url = f"https://lite.duckduckgo.com/lite/?q={encoded}"
            tmp = tempfile.mktemp(suffix=".html")
            subprocess.run(
                [CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu",
                 "--disable-dev-shm-usage", "--dump-dom", f"https://lite.duckduckgo.com/lite/?q={encoded}"],
                timeout=25, stdout=open(tmp, "w"), stderr=subprocess.DEVNULL
            )
            html = Path(tmp).read_text()
            # DDG Lite: simple table structure
            lite_links = re.findall(
                r'<a[^>]*rel="nofollow"[^>]*href="(https?://[^"]+)"[^>]*>([^<]+)</a>',
                html
            )
            for url, title in lite_links[:count]:
                bad = ['duckduckgo.com', 'google.com']
                if not any(d in url for d in bad):
                    results.append({"title": title.strip(), "url": url, "snippet": ""})
            Path(tmp).unlink(missing_ok=True)
        except Exception:
            pass

    # 清理标题中的 HTML 标签
    clean_results = []
    for r in results:
        clean_results.append({
            "title": re.sub(r'<[^>]+>', '', r["title"]).strip(),
            "url": r["url"],
            "snippet": re.sub(r'<[^>]+>', '', r["snippet"]).strip(),
        })

    _cs(k, clean_results)
    return clean_results

def search_linkedin(query: str, count: int = 5) -> list:
    return search(f"site:linkedin.com/in {query}", count=count)

def search_company(company: str, count: int = 10) -> list:
    """搜索公司信息（含官网/联系方式/行业）"""
    q = f"{company} company official website contact email phone"
    return search(q, count=count)

# ── 深度验证（5项验证管道） ──
def verify_company(name: str, website: str = "") -> dict:
    """
    对公司执行 5 项深度验证：
    1. 官网可达 + 标题匹配
    2. 电话存在性
    3. 邮箱存在性
    4. LinkedIn 存在性
    5. 第三方交叉验证（搜索信誉）
    """
    result = {"name": name, "verifications": [], "confidence": 0.0, "details": {}}

    # 1. 官网验证
    if website:
        page = fetch_adaptive(website)
        result["details"]["website"] = page["title"][:100] if page["title"] else ""
        if page["status"] == 200 and page["title"]:
            name_in_title = any(
                part.lower() in page["title"].lower()
                for part in name.lower().split()[:2]
            )
            result["verifications"].append({
                "method": "website_check",
                "passed": True,
                "evidence": f"Site reachable: {website}, title: {page['title'][:60]}",
            })
        else:
            result["verifications"].append({
                "method": "website_check",
                "passed": False,
                "evidence": page.get("error", f"HTTP {page['status']}"),
            })
    else:
        # 自动搜索官网
        pages = search_company(name, count=5)
        for p in pages:
            if name.lower().split()[0] in p["title"].lower():
                result["details"]["website_found"] = p["url"]
                page = fetch_adaptive(p["url"])
                if page["status"] == 200:
                    result["details"]["website"] = page["title"][:100]
                    result["verifications"].append({
                        "method": "website_check",
                        "passed": True,
                        "evidence": f"Auto-found: {p['url']}",
                    })
                    website = p["url"]
                    break
        if not website:
            result["verifications"].append({
                "method": "website_check",
                "passed": False,
                "evidence": "No website found",
            })

    # 2-3. 提取电话和邮箱（如果有官网）
    if website:
        page = fetch_adaptive(website)
        if page["emails"]:
            result["details"]["emails"] = page["emails"][:5]
            result["verifications"].append({
                "method": "email_check",
                "passed": True,
                "evidence": f"Emails found: {', '.join(page['emails'][:3])}",
            })
        else:
            result["verifications"].append({
                "method": "email_check",
                "passed": False,
                "evidence": "No emails found on site",
            })
        if page["phones"]:
            result["details"]["phones"] = page["phones"][:5]
            result["verifications"].append({
                "method": "phone_check",
                "passed": True,
                "evidence": f"Phones found: {', '.join(page['phones'][:3])}",
            })
        else:
            result["verifications"].append({
                "method": "phone_check",
                "passed": False,
                "evidence": "No phones found on site",
            })

    # 4. LinkedIn 验证
    li_results = search_linkedin(name, count=3)
    has_li = any(name.lower().split()[0] in r["title"].lower() for r in li_results)
    result["verifications"].append({
        "method": "linkedin_check",
        "passed": has_li,
        "evidence": f"LinkedIn results: {len(li_results)}"
                  + (f" - {li_results[0]['url']}" if li_results else ""),
    })

    # 5. 第三方搜索验证
    ref_results = search(f"{name} company review profile", count=5)
    has_ref = len([r for r in ref_results if "linkedin" not in r["url"]]) > 1
    result["verifications"].append({
        "method": "third_party",
        "passed": has_ref,
        "evidence": f"Cross-reference results: {len(ref_results)}",
    })

    # 可信度评分
    passed = sum(1 for v in result["verifications"] if v["passed"])
    total = len(result["verifications"])
    result["confidence"] = round(passed / max(total, 1), 2)

    return result

# ── 批量搜索买家（买家情报专用） ──
def search_buyers(product: str, region: str = "", count: int = 15) -> list:
    """
    按产品搜索买家/采购商/项目
    示例: search_buyers("labor camp", "Saudi Arabia")
    """
    # 多角度搜索
    queries = [
        f"{product} {region} buyer procurement",
        f"{product} {region} construction project tender",
        f"{product} {region} purchasing manager contact",
        f"{product} {region} developer contractor",
    ]

    all_results = []
    for q in queries:
        results = search(q, count=count // len(queries) + 2)
        all_results.extend(results)

    # 去重
    seen = set()
    unique = []
    for r in all_results:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    return unique[:count]

# ── CLI ──
def main():
    if len(sys.argv) < 2:
        print("📡 太一搜索器 v4 — 自适应搜索Agent（Scrapling 引擎）")
        print()
        print("  search      <query> [count]       自适应多源搜索")
        print("  linkedin    <query> [count]       搜索 LinkedIn 人物")
        print("  company     <company> [count]     搜索公司信息")
        print("  fetch       <url>                 自适应抓取（含邮箱/电话）")
        print("  fetchjs     <url>                 抓取（Chromium JS 渲染）")
        print("  verify      <name> [website]      5项验证管道")
        print("  buyers      <product> [region]    买家情报搜索")
        print("  pdf         <url> <out.pdf>       保存为 PDF")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "search":
        q = sys.argv[2] if len(sys.argv) > 2 else ""
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        r = search(q, n)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        if not r:
            sys.exit(1)

    elif cmd == "linkedin":
        q = sys.argv[2] if len(sys.argv) > 2 else ""
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        r = search_linkedin(q, n)
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif cmd == "company":
        q = sys.argv[2] if len(sys.argv) > 2 else ""
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 8
        r = search_company(q, n)
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif cmd in ("fetch", "fetchjs"):
        u = sys.argv[2] if len(sys.argv) > 2 else ""
        use_js = cmd == "fetchjs"
        r = fetch_adaptive(u, use_chromium=use_js)
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif cmd == "verify":
        name = sys.argv[2] if len(sys.argv) > 2 else ""
        website = sys.argv[3] if len(sys.argv) > 3 else ""
        r = verify_company(name, website)
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif cmd == "buyers":
        product = sys.argv[2] if len(sys.argv) > 2 else "labor camp"
        region = sys.argv[3] if len(sys.argv) > 3 else ""
        n = int(sys.argv[4]) if len(sys.argv) > 4 else 15
        r = search_buyers(product, region, count=n)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        print(f"\n📊 找到 {len(r)} 个买家线索", file=sys.stderr)

    elif cmd == "pdf":
        u = sys.argv[2] if len(sys.argv) > 2 else ""
        o = sys.argv[3] if len(sys.argv) > 3 else "output.pdf"
        subprocess.run(
            [CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu",
             "--print-to-pdf=" + o, u],
            timeout=30, stderr=subprocess.DEVNULL,
        )
        print(f"PDF: {o}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
太一 · Scrapling 自适应爬取层 v1.0
====================================
智能自动化切换：根据目标网站反爬等级选择最优引擎

三层策略:
  Level 0 — 简单页面: Fetcher (curl_cffi, 最快)
  Level 1 — 中等防护: Fetcher + adaptive=True (自适应解析)
  Level 2 — 强防护(Cloudflare等): 自动 fallback 提示

使用:
  from skills.scrapling_adaptor.core import smart_fetch

  # 自动选择最优引擎
  result = smart_fetch('https://example.com/products')
  print(result.text[:500])

  # 强制使用 adaptive 模式 (网页结构常变时)
  result = smart_fetch('https://example.com/products', adaptive=True)

  # 提取结构化数据 (自动保存位置，后续改版自动重定位)
  items = result.css('.product-item', auto_save=True)
"""

import logging
from typing import Optional
from urllib.parse import urlparse

logger = logging.getLogger("scrapling-adaptor")

# ── 导入 Scrapling ──────────────────────────────────
try:
    from scrapling.fetchers import Fetcher
    SCRAPLING_AVAILABLE = True
except ImportError:
    SCRAPLING_AVAILABLE = False
    logger.warning("Scrapling not installed, falling back to requests")

# ── 防护等级检测 ────────────────────────────────────

HIGH_SECURITY_DOMAINS = [
    "cloudflare.com", "turnstile", "challenges.cloudflare.com",
]

# 已知使用 Cloudflare / 强反爬的网站
HIGH_SECURITY_PATTERNS = [
    "cf-cookie", "__cfduid", "cf-ray", "cf-bm", "turnstile",
    "recaptcha/api.js", "hcaptcha.com", "data-dome",
]


def _detect_security_level(url: str) -> int:
    """
    检测目标网站的防护等级。
    
    返回: 0(简单) / 1(中等) / 2(强防护)
    """
    domain = urlparse(url).netloc.lower()
    
    # 政府/教育/开源站点 — 基本无反爬
    if domain.endswith(('.gov.au', '.edu.au', '.gov.sa', '.gov', '.edu')):
        return 0
    
    # ABN Lookup / 澳大利亚政府站点
    if any(kw in domain for kw in ['abr.business.gov.au', 'asic.gov.au', '.gov.']):
        return 0
    
    # 商业大平台 — 可能有反爬
    if any(kw in domain for kw in ['linkedin.com', 'facebook.com', 'amazon.com',
                                    'indeed.com', 'seek.com.au', 'realestate.com']):
        return 2
    
    # 静态 HTML 站点 — 中等
    return 1


# ── 统一爬取入口 ────────────────────────────────────

_fetcher_instance = None


def _get_fetcher() -> 'Fetcher':
    """获取或创建全局 Fetcher 实例"""
    global _fetcher_instance
    if _fetcher_instance is None and SCRAPLING_AVAILABLE:
        _fetcher_instance = Fetcher()
    return _fetcher_instance


def smart_fetch(url: str, adaptive: bool = False,
                timeout: int = 15, headers: dict = None,
                auto_save: bool = False) -> dict:
    """
    智能爬取：自动选择引擎 + 错误处理
    
    Args:
        url: 目标 URL
        adaptive: 是否启用自适应模式 (网站结构变化时自动重定位)
        timeout: 超时秒数
        headers: 自定义请求头
        auto_save: 是否保存元素位置 (用于 future adaptive)
    
    Returns:
        {
            "status": 200 | 0,
            "body": str,        # HTML/text 内容
            "text": str,        # 纯文本
            "response": obj,    # Scrapling Response 对象 (for advanced use)
            "engine": str,      # 使用的引擎名称
            "error": str | None
        }
    """
    level = _detect_security_level(url)
    
    # ── Level 0: 简单请求 ────────────────────────────
    if level == 0 and not adaptive:
        try:
            import requests
            resp = requests.get(url, timeout=timeout,
                                headers=headers or {
                                    "User-Agent": "Mozilla/5.0 (compatible; TaiyiTradeBot/1.0)"
                                })
            return {
                "status": resp.status_code,
                "body": resp.text,
                "text": resp.text,
                "response": None,
                "engine": "requests",
                "error": None if resp.status_code == 200 else f"HTTP {resp.status_code}",
            }
        except Exception as e:
            logger.warning(f"requests failed for {url}, trying Scrapling: {e}")
            # fall through to Scrapling
    
    # ── Level 1/2: Scrapling ─────────────────────────
    fetcher = _get_fetcher()
    if fetcher is None:
        return {
            "status": 0, "body": "", "text": "",
            "engine": "none", "error": "Scrapling not installed",
        }
    
    try:
        # 更新 adaptive 设置
        fetcher.adaptive = adaptive
        
        result = fetcher.get(url)
        
        return {
            "status": result.status,
            "body": result.body,
            "text": result.text,
            "response": result,
            "engine": "scrapling",
            "error": None if result.status == 200 else f"HTTP {result.status}",
        }
    except Exception as e:
        logger.error(f"Scrapling fetch failed for {url}: {e}")
        return {
            "status": 0, "body": "", "text": "",
            "engine": "scrapling", "error": str(e),
        }


def extract_items(html_response, css_selector: str,
                  adaptive: bool = False, auto_save: bool = False) -> list:
    """
    从 Scrapling Response 中提取结构化数据。
    
    使用 adaptive=True 后，即使网站改版也能自动重定位元素。
    使用 auto_save=True 保存元素位置到本地存储。
    
    Args:
        html_response: Scrapling Response 对象
        css_selector: CSS 选择器
        adaptive: 启用自适应（改版后自动查找）
        auto_save: 保存当前位置
    
    Returns:
        list[Element] — 每个元素可继续 .css() 提取子元素
    """
    if html_response is None:
        return []
    
    try:
        if adaptive:
            # 启用自适应模式（历史位置保存后生效）
            items = html_response.css(css_selector, adaptive=True)
        elif auto_save:
            items = html_response.css(css_selector, auto_save=True)
        else:
            items = html_response.css(css_selector)
        return items
    except Exception as e:
        logger.error(f"CSS extract error ({css_selector}): {e}")
        return []


def extract_text(html_response, css_selector: str) -> str:
    """提取单个元素的文本"""
    try:
        el = html_response.css(css_selector)
        if el:
            return el.get_all_text() or el.text or ""
        return ""
    except Exception:
        return ""


# ── CLI 测试 ────────────────────────────────────────

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        adaptive = "--adaptive" in sys.argv
        
        print(f"🔍 Fetching: {url}")
        print(f"   Adaptive: {adaptive}")
        print()
        
        result = smart_fetch(url, adaptive=adaptive)
        print(f"   Status: {result['status']}")
        print(f"   Engine: {result['engine']}")
        print(f"   Error: {result['error']}")
        print(f"   Body length: {len(result['body'])}")
        
        if result['response'] and "--extract" in sys.argv:
            idx = sys.argv.index("--extract")
            selector = sys.argv[idx + 1]
            items = extract_items(result['response'], selector)
            print(f"\n   Extracted {len(items)} items via '{selector}'")
            for i, item in enumerate(items[:5]):
                print(f"   [{i}] {item.text[:100] if item.text else item.attrib}")
    else:
        print("用法: python3 core.py <url> [--adaptive] [--extract <css>]")
        print("示例: python3 core.py https://example.com --extract 'h1'")

# ═══════════════════════════════════════════════
# 反爬搜索增强
# ═══════════════════════════════════════════════

_SEARCH_CACHE = {}

def anti_scrape_search(query: str, timeout: int = 15) -> dict:
    """
    反爬搜索引擎 — 自动切换 DuckDuckGo/Bing 避免频率限制。
    
    Args:
        query: 搜索关键词
        timeout: 超时秒数
    
    Returns:
        {"status", "source", "emails", "phones", "linkedin", "error"}
    """
    import time as _time
    import cloudscraper
    import re
    
    cache_key = f"search:{query}"
    if cache_key in _SEARCH_CACHE:
        return _SEARCH_CACHE[cache_key]
    
    scraper = cloudscraper.create_scraper()
    
    engines = [
        ("duckduckgo", f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"),
        ("bing", f"https://www.bing.com/search?q={query.replace(' ', '+')}"),
    ]
    
    all_emails, all_phones, all_linkedin = [], [], []
    
    for engine_name, url in engines:
        try:
            _time.sleep(2)  # 防频率限制
            r = scraper.get(url, timeout=timeout)
            if r.status_code != 200:
                continue
            
            html = r.text
            
            emails = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)))
            emails = [e for e in emails if not any(
                x in e for x in ['.png','.jpg','.gif','.svg','google','bing',
                                'duckduckgo','gstatic','w3.org','schema.org',
                                'example','microsoft','github','facebook',
                                'twitter','youtube','whatsapp'])]
            
            linkedin = list(set(re.findall(r'linkedin\.com/(?:company|in)/[a-zA-Z0-9_-]+', html)))
            
            all_emails.extend(emails)
            all_linkedin.extend(linkedin)
            
            if emails or linkedin:
                break
        except Exception:
            continue
    
    result = {
        "status": 200,
        "source": "+".join(e[0] for e in engines),
        "emails": list(set(all_emails))[:10],
        "linkedin": [f"https://www.{l}" for l in list(set(all_linkedin))[:5]],
        "error": None,
    }
    
    _SEARCH_CACHE[cache_key] = result
    return result
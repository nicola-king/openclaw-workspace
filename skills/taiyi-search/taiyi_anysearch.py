"""
太一统一搜索引擎 · Taiyi Unified Search
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
蒸馏合并自:
  - anysearch-skill    → 统一搜索API (通用/垂直/批量/URL提取)
  - shared-search      → 缓存层 + 路由 + 统计 + 国家识别 + 目录生成
  - search-agent       → 穿透式搜索 + 反爬对抗

能力矩阵:
  search()        通用搜索 / 垂直领域23域
  deep_search()   批量穿透搜索（多角度聚合）
  extract_url()   URL完整内容提取
  list_domains()  列出垂直领域
  resolve_country() 国家代码解析
  gen_search_links() 多平台搜索链接生成

所有功能单一入口，零外部依赖，匿名可用。
"""

import json, time, hashlib, os, re, subprocess, logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union

logger = logging.getLogger("taiyi.search")

SKILL_DIR = Path(__file__).parent
ANYSEARCH_CLI = SKILL_DIR.parent / "anysearch-skill" / "scripts" / "anysearch_cli.py"
CACHE_DIR = SKILL_DIR / ".cache"
CACHE_DIR.mkdir(exist_ok=True)

# =====================================================================
# 国家数据库（蒸馏自 shared-search-agent）
# =====================================================================

COUNTRY_DB = {
    "australia": {"domain": ".com.au", "zone": "intl", "alias": ["au", "aus", "australia"]},
    "china": {"domain": ".cn", "zone": "cn", "alias": ["cn", "china", "中国"]},
    "japan": {"domain": ".jp", "zone": "intl", "alias": ["jp", "japan", "日本"]},
    "singapore": {"domain": ".sg", "zone": "intl", "alias": ["sg", "singapore"]},
    "usa": {"domain": ".com", "zone": "intl", "alias": ["us", "usa", "america", "美国"]},
    "uk": {"domain": ".uk", "zone": "intl", "alias": ["uk", "gb", "britain", "united kingdom"]},
    "uae": {"domain": ".ae", "zone": "intl", "alias": ["ae", "uae", "dubai", "阿联酋"]},
    "saudi": {"domain": ".sa", "zone": "intl", "alias": ["sa", "ksa", "saudi", "沙特"]},
}

def resolve_country(market: str) -> str:
    """国家名称→代码解析"""
    if not market: return "australia"
    m = market.lower().strip()
    alias_map = {}
    for code, info in COUNTRY_DB.items():
        alias_map[code] = code
        for alias in info.get("alias", []):
            alias_map[alias] = code
    if m in alias_map: return alias_map[m]
    for code, info in COUNTRY_DB.items():
        domain = info.get("domain", "")
        if domain and domain[1:] in m: return code
        if code in m: return code
    return m

def gen_search_links(product: str, market: str) -> Dict:
    """生成多平台搜索链接"""
    from urllib.parse import quote_plus
    kw = quote_plus(f"{product} {market}")
    kw_slug = product.replace(" ", "-")
    return {
        "google": f"https://www.google.com/search?q={kw}",
        "bing": f"https://www.bing.com/search?q={kw}",
        "linkedin_companies": f"https://www.linkedin.com/search/results/companies/?keywords={kw}",
        "alibaba": f"https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&SearchText={kw}",
    }

# =====================================================================
# 缓存层
# =====================================================================

class SearchCache:
    def __init__(self, ttl_seconds: int = 3600):
        self.cache_dir = CACHE_DIR
        self.ttl = timedelta(seconds=ttl_seconds)

    def _key_path(self, key: str) -> Path:
        h = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{h}.json"

    def get(self, key: str) -> Optional[Dict]:
        path = self._key_path(key)
        if path.exists():
            try:
                data = json.loads(path.read_text())
                if datetime.fromisoformat(data["expires"]) > datetime.now():
                    return data["result"]
                path.unlink(missing_ok=True)
            except: pass
        return None

    def set(self, key: str, data: Dict):
        expires = (datetime.now() + self.ttl).isoformat()
        self._key_path(key).write_text(
            json.dumps({"expires": expires, "result": data}, ensure_ascii=False))

    def clear(self):
        for f in self.cache_dir.glob("*.json"):
            f.unlink(missing_ok=True)

cache = SearchCache()

# =====================================================================
# AnySearch 调用层
# =====================================================================

def _call_anysearch(cmd: List[str]) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return r.stdout
    except subprocess.TimeoutExpired:
        return ""
    except Exception as e:
        logger.error(f"AnySearch error: {e}")
        return ""

def search(query: str, max_results: int = 10, freshness: str = None,
           domain: str = None, sub_domain: str = None) -> Dict:
    """
    统一搜索入口 — 通用搜索 + 垂直领域
    
    参数:
      query: 搜索词
      max_results: 1-100
      freshness: day/week/month/year
      domain: 垂直领域 (tech/finance/academic/legal/business 等)
      sub_domain: 子域 (如 finance.us_stock)
    
    返回:
      {results: [{title, url, snippet, score}], total, time_ms, query, cache_hit}
    """
    cache_key = f"s:{query}:{max_results}:{freshness}:{domain}:{sub_domain}"
    
    cached = cache.get(cache_key)
    if cached:
        cached["cache_hit"] = True
        return cached
    
    t0 = time.time()
    cmd = ["python3", str(ANYSEARCH_CLI), "search", query, "--max_results", str(max_results)]
    if freshness: cmd.extend(["--freshness", freshness])
    if domain: cmd.extend(["--domain", domain])
    if sub_domain: cmd.extend(["--sub_domain", sub_domain])
    
    output = _call_anysearch(cmd)
    elapsed = int((time.time() - t0) * 1000)
    
    result = _parse_results(output, query, elapsed)
    result["cache_hit"] = False
    
    if result["results"]:
        cache.set(cache_key, result)
    
    return result

def deep_search(queries: List[str], max_per_query: int = 5,
                freshness: str = None) -> Dict:
    """批量穿透搜索 — 多角度聚合"""
    all_results, total_time = [], 0
    for q in queries:
        r = search(q, max_results=max_per_query, freshness=freshness)
        all_results.extend(r.get("results", []))
        total_time += r.get("time_ms", 0)
    return {
        "results": all_results, "total": len(all_results),
        "queries": queries, "time_ms": total_time, "provider": "anysearch"
    }

def extract_url(url: str, max_chars: int = 5000, strategy: str = "auto") -> Dict:
    """
    URL内容提取 — 10层永不放弃抓取链路
    
    链路:
      L1: AnySearch CLI (零成本搜索API)
      L2: Scrapling 10层核弹抓取 (requests→stealth→cloudscraper→dynamic→playwright→cache→proxy)
    
    策略:
      "auto":     自动域名预判路由
      "stealth":  反爬优先
      "dynamic":  JS渲染优先
      "full":     全部链路
    """
    cache_key = f"e:{url}:{max_chars}:{strategy}"
    cached = cache.get(cache_key)
    if cached: return cached

    t0 = time.time()
    debug = []

    # L1: AnySearch CLI
    debug.append("anysearch→try")
    cmd = ["python3", str(ANYSEARCH_CLI), "extract", url, "--max_chars", str(max_chars)]
    output = _call_anysearch(cmd)
    if output and len(output.strip()) > 100:
        result = {"content": output[:max_chars], "url": url,
                  "time_ms": int((time.time() - t0) * 1000),
                  "fetcher": "anysearch", "strategy": strategy}
        cache.set(cache_key, result)
        return result

    debug.append("anysearch→skip→scrapling_10layer")

    # L2+: Scrapling 10层抓取
    try:
        from skills.taiyi_search.taiyi_scrapling import scrapling_fetch as _sf
        sr = _sf(url, strategy=strategy)
        if sr["status"] == "ok":
            content = sr.get("content", "")[:max_chars]
            result = {"content": content, "url": url,
                      "time_ms": sr.get("time_ms", int((time.time() - t0) * 1000)),
                      "fetcher": sr.get("fetcher", "scrapling"),
                      "strategy": strategy,
                      "chain_attempts": sr.get("chain_attempts", 0),
                      "debug": sr.get("debug", debug)}
            cache.set(cache_key, result)
            return result
        debug.extend(sr.get("debug", []))
    except ImportError:
        debug.append("scrapling_unavailable")
    except Exception as e:
        debug.append(f"scrapling_error:{e}")

    result = {"content": output[:max_chars], "url": url,
              "time_ms": int((time.time() - t0) * 1000),
              "fetcher": "anysearch", "strategy": strategy,
              "debug": debug, "warning": "All chains failed"}
    cache.set(cache_key, result)
    return result

def list_domains() -> Dict:
    """列出所有垂直领域"""
    cmd = ["python3", str(ANYSEARCH_CLI), "list_domains"]
    output = _call_anysearch(cmd)
    return {"domains": output, "provider": "anysearch"}

def _parse_results(output: str, query: str, elapsed: int) -> Dict:
    results = []
    current = {}
    for line in output.split('\n'):
        if line.startswith('### '):
            if current.get('title'): results.append(current)
            current = {'title': line.replace('### ', '').strip()}
        elif '- **URL**' in line:
            current['url'] = line.split('**: ')[-1].strip() if '**: ' in line else ''
        elif current and line.strip() and not line.startswith('-') and not line.startswith('#'):
            if 'snippet' not in current:
                current['snippet'] = line.strip()[:300]
    if current.get('title'): results.append(current)
    return {"results": results, "total": len(results), "query": query, "time_ms": elapsed}

# =====================================================================
# Scrapling 快速入口（便捷导入接口）
# =====================================================================

def scrapling_fetch(url: str, strategy: str = "auto", **kwargs) -> Dict:
    """
    Scrapling 10层智能抓取 — 100%命中目标
    
    策略:
      "auto":     自动域名预判路由
      "stealth":  反爬优先（跳过低级链路）
      "dynamic":  JS渲染优先
      "nuclear":  全部10层依次尝试
    
    返回: {status, content, fetcher, chain_attempts, time_ms, debug}
    """
    try:
        from skills.taiyi_search.taiyi_scrapling import scrapling_fetch as _sf
        return _sf(url, strategy=strategy, **kwargs)
    except ImportError:
        return {"status": "error", "error": "Scrapling module not available", "url": url}

def extract_elements(html: str, **kwargs) -> Dict:
    """CSS/XPath/自适应元素提取"""
    try:
        from skills.taiyi_search.taiyi_scrapling import extract_elements as _ee
        return _ee(html, **kwargs)
    except ImportError:
        return {"status": "error", "error": "Scrapling not available"}

def adaptive_extract(html: str, **kwargs) -> Dict:
    """自适应文本定位+自动CSS生成器"""
    try:
        from skills.taiyi_search.taiyi_scrapling import adaptive_extract as _ae
        return _ae(html, **kwargs)
    except ImportError:
        return {"status": "error", "error": "Scrapling not available"}

def batch_fetch(urls: list, **kwargs) -> list:
    """批量并发采集"""
    try:
        from skills.taiyi_search.taiyi_scrapling import batch_fetch as _bf
        return _bf(urls, **kwargs)
    except ImportError:
        return [{"url": u, "status": "error", "error": "Scrapling not available"} for u in urls]

# ===== Stats =====

class SearchStats:
    def __init__(self):
        self.stats_file = CACHE_DIR / "stats.json"
    
    def record(self, query: str, total: int, time_ms: int):
        stats = self._load()
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in stats: stats[today] = {"count": 0, "total_time": 0}
        stats[today]["count"] += 1
        stats[today]["total_time"] += time_ms
        self._save(stats)
    
    def summary(self) -> str:
        stats = self._load()
        lines = []
        for day, data in sorted(stats.items(), reverse=True)[:7]:
            avg = data["total_time"] // max(data["count"], 1)
            lines.append(f"  {day}: {data['count']}次搜索 平均{avg}ms")
        return "\n".join(lines)
    
    def _load(self) -> Dict:
        if self.stats_file.exists():
            return json.loads(self.stats_file.read_text())
        return {}
    
    def _save(self, data: Dict):
        self.stats_file.write_text(json.dumps(data, ensure_ascii=False, indent=2))

stats = SearchStats()

# =====================================================================
# CLI入口
# =====================================================================

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("""太一统一搜索引擎 · Taiyi Unified Search (v2.1 Scrapling)
用法: python taiyi_anysearch.py <命令> [参数]

搜索:
  search <词> [max=10] [freshness] [domain] [sub_domain]
  deep <词1> <词2>...      批量穿透搜索
  extract <url>            提取URL内容 (含Scrapling自动降级)
  scrapling <url>          强制Scrapling智能抓取 (反爬绕过)
  stealth <url>            强制StealthyFetcher (Cloudflare绕过)
  dynamic <url>            强制DynamicFetcher (JS渲染)
  extract-css <url> <css>  提取CSS元素
  batch <url1> <url2>...   批量采集
  domains                  列出垂直领域
  stats                    搜索统计
工具:
  country <国家名>       解析国家代码
  links <产品> <市场>    生成搜索链接
  clear                   清空搜索缓存""")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "search":
        q = sys.argv[2] if len(sys.argv) > 2 else ""
        r = search(q, max_results=int(sys.argv[3]) if len(sys.argv) > 3 else 10,
                   freshness=sys.argv[4] if len(sys.argv) > 4 else None,
                   domain=sys.argv[5] if len(sys.argv) > 5 else None)
        stats.record(q, r.get("total",0), r.get("time_ms",0))
        for item in r.get("results", []):
            print(f"\n  📄 {item.get('title','')}")
            print(f"     {item.get('url','')}")
        print(f"\n  📊 {r.get('total',0)}条 · {r.get('time_ms',0)}ms{' · 缓存' if r.get('cache_hit') else ''}")
    
    elif cmd == "deep":
        queries = sys.argv[2:]
        r = deep_search(queries)
        print(f"批量搜索 {len(queries)} 个词 · 共 {r.get('total',0)} 条结果")
        for item in r.get("results", [])[:5]:
            print(f"  • {item.get('title','')}")
    
    elif cmd == "extract":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        strategy = sys.argv[3] if len(sys.argv) > 3 else "auto"
        r = extract_url(url, strategy=strategy)
        chain = r.get("chain_attempts", 1)
        print(f"📡 {url}")
        print(f"   [{r.get('fetcher','?')}] {r.get('time_ms',0)}ms | {chain}层尝试")
        print(r.get("content", "")[:600])

    elif cmd == "scrapling":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        strategy = sys.argv[3] if len(sys.argv) > 3 else "auto"
        try:
            from taiyi_scrapling import scrapling_fetch
            r = scrapling_fetch(url, strategy=strategy)
            print(f"📡 {url}")
            print(f"   策略: {r.get('strategy','?')} | {r.get('fetcher','?')} | {r.get('time_ms',0)}ms | {r.get('chain_attempts',0)}层")
            print(f"   Debug: {r.get('debug', [])}")
            if r.get("status") == "ok":
                c = r.get("content", "")
                print(f"   📐 Length: {len(c)} chars")
                print(f"   📄 {c[:600]}...")
            else:
                print(f"   ❌ {r.get('error','?')}")
        except ImportError:
            print("❌ Scrapling module not found")

    elif cmd == "stealth":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        try:
            from taiyi_scrapling import _try_scrapling_stealth as _ts
            r = _ts(url)
            print(f"[Stealth] {r.get('status')} | {len(r.get('content',''))} chars | {r.get('error','OK')}")
        except ImportError:
            print("❌ Scrapling module not found")

    elif cmd == "dynamic":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        try:
            from taiyi_scrapling import _try_scrapling_dynamic as _td
            r = _td(url)
            print(f"[Dynamic] {r.get('status')} | {len(r.get('content',''))} chars | {r.get('error','OK')}")
        except ImportError:
            print("❌ Scrapling module not found")

    elif cmd == "extract-css":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        css = sys.argv[3] if len(sys.argv) > 3 else "body"
        try:
            from taiyi_scrapling import scrapling_fetch, extract_elements
            r = scrapling_fetch(url)
            if r["status"] == "ok":
                e = extract_elements(r["content"], css_selector=css)
                print(f"提取 {e.get('count',0)} 个元素:")
                for item in e.get("items", [])[:10]:
                    print(f"  • {item.get('text','')[:200]}")
        except ImportError:
            print("❌ Scrapling module not found")

    elif cmd == "batch":
        urls = sys.argv[2:]
        try:
            from taiyi_scrapling import batch_fetch
            results = batch_fetch(urls)
            for r in results:
                fs = r.get('fetcher','?')
                print(f"  {r['url']} → {r['status']} ({fs}) {r.get('length',0)}b | {r.get('chain_attempts',0)}层")
        except ImportError:
            print("❌ Scrapling module not found")
    
    elif cmd == "domains":
        r = list_domains()
        print(r.get("domains", "")[:800])
    
    elif cmd == "stats":
        print("搜索统计（近7天）:")
        print(stats.summary())
    
    elif cmd == "country":
        market = sys.argv[2] if len(sys.argv) > 2 else "usa"
        print(f"'{market}' → {resolve_country(market)}")
    
    elif cmd == "links":
        prod = sys.argv[2] if len(sys.argv) > 2 else "battery"
        mkt = sys.argv[3] if len(sys.argv) > 3 else "australia"
        links = gen_search_links(prod, mkt)
        for name, url in links.items():
            print(f"  {name}: {url}")
    
    elif cmd == "clear":
        cache.clear()
        print("✅ 缓存已清空")
    
    else:
        print(f"未知命令: {cmd}")

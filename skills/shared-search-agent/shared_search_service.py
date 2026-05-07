#!/home/sayelf/.local/venvs/scraper/bin/python3
# -*- coding: utf-8 -*-
"""
太一统一情报引擎 v2 (Taiyi Unified Intelligence Engine)
============================================================
融合所有搜索/情报/验证功能到单一共享服务。

能力来源整合:
┌─ scripts/scraper_v4.py    Scrapling自适应搜索+验证
├─ multi_source_search.py   12国搜索资源+黄页目录
├─ auto_scraper.py          自动搜公司+深度爬取
├─ shared_search_service.py 缓存/统计/多Agent分发
└─ intelligence-hub         情报分析+趋势预警

使用方式:
    from shared_search_agent.shared_search_service import (
        TaiyiSharedSearchService,
        get_shared_search_service,
        SearchRequest, SearchResult
    )
    svc = get_shared_search_service()
    result = svc.search(SearchRequest(query="...", agent_type="cross_border_trade"))
"""

import json, logging, hashlib, time, sys, os, re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum

# ── 引入 scraper_v4 作为实际搜索引擎 ──
# 确保在 venv 环境中运行（含 scrapling 依赖）
_VENV_SITE = Path.home() / ".local" / "venvs" / "scraper" / "lib" / "python3.14" / "site-packages"
if str(_VENV_SITE) not in sys.path and _VENV_SITE.exists():
    sys.path.insert(0, str(_VENV_SITE))

_SCRAPER_V4_PATH = Path.home() / ".openclaw" / "workspace" / "scripts" / "scraper_v4.py"
sys.path.insert(0, str(_SCRAPER_V4_PATH.parent))
import importlib.util
_spec = importlib.util.spec_from_file_location("scraper_v4", str(_SCRAPER_V4_PATH))
_scraper_v4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_scraper_v4)

# ── Logging ──
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('TaiyiSearch')

# ── Paths ──
WORKSPACE = Path.home() / ".openclaw" / "workspace"
CACHE_DIR = WORKSPACE / "data" / "shared-search-cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
STATS_FILE = WORKSPACE / "data" / "shared-search-stats.json"

# =====================================================================
# 数据模型
# =====================================================================

class SearchMode(Enum):
    ADAPTIVE = "adaptive"    # Scrapling 自适应 (默认)
    FETCH = "fetch"          # 单页抓取
    VERIFY = "verify"        # 公司验证
    BUYERS = "buyers"        # 买家搜索
    LINKEDIN = "linkedin"    # LinkedIn搜索

class AgentType(Enum):
    CROSS_BORDER = "cross_border_trade"
    TRAVEL = "travel_explorer"
    GEO = "geo_outbound"
    GENERAL = "general"

@dataclass
class SearchRequest:
    query: str
    agent_type: str = "general"
    search_mode: str = "adaptive"
    country: Optional[str] = None
    max_results: int = 10
    use_cache: bool = True

    def to_dict(self) -> Dict:
        return asdict(self)

    def get_cache_key(self) -> str:
        key_data = f"{self.query}:{self.agent_type}:{self.country}:{self.search_mode}"
        return hashlib.md5(key_data.encode()).hexdigest()

@dataclass
class SearchResult:
    success: bool
    results: List[Dict]
    source: str
    agent_type: str
    query: str
    timestamp: str
    cache_hit: bool = False
    duration_ms: float = 0.0
    error_message: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)

# =====================================================================
# 国家搜索资源数据库（来自 multi_source_search.py）
# =====================================================================

COUNTRY_DB = {
    "australia": {
        "domain": ".au", "google_cc": "Australia",
        "directories": {
            "yellow_pages": "https://www.yellowpages.com.au/search/listings?clue={kw}",
            "abn_lookup": "https://abr.business.gov.au/SearchByKeyword?Keyword={kw}",
            "true_local": "https://www.truelocal.com.au/find/{kw}",
        },
        "trade": {"prefabaus": "https://www.prefabaus.org.au/search?q={kw}"},
        "lang": "en",
    },
    "saudi arabia": {
        "domain": ".sa", "google_cc": "Saudi+Arabia",
        "directories": {
            "saudi_business": "https://www.google.com/search?q={kw}+site:sa",
            "saudi_yellow": "https://www.google.com/search?q={kw}+%D8%AF%D9%84%D9%8A%D9%84+%D8%A7%D9%84%D8%B3%D8%B9%D9%88%D8%AF%D9%8A%D8%A9",
        },
        "lang": "en,ar",
    },
    "uae": {
        "domain": ".ae", "google_cc": "UAE",
        "directories": {
            "uae_business": "https://www.google.com/search?q={kw}+site:ae",
            "uae_yellow": "https://www.yellowpages.ae/search/{kw}.html",
        },
        "lang": "en,ar",
    },
    "qatar": {"domain": ".qa", "google_cc": "Qatar",
        "directories": {"qatar_business": "https://www.google.com/search?q={kw}+site:qa"}},
    "USA": {"domain": ".us", "google_cc": "USA",
        "directories": {
            "yellow_pages": "https://www.yellowpages.com/search?search_terms={kw}",
            "bbb": "https://www.bbb.org/search?find_country=USA&find_text={kw}",
        }},
    "UK": {"domain": ".uk", "google_cc": "UK",
        "directories": {
            "yell": "https://www.yell.com/ucs/UcsSearchAction.do?keywords={kw}",
            "companies_house": "https://find-and-update.company-information.service.gov.uk/search?q={kw}",
        }},
    "canada": {"domain": ".ca", "google_cc": "Canada",
        "directories": {"yellow_pages_ca": "https://www.yellowpages.ca/search/si/1/{kw}"}},
    "germany": {"domain": ".de", "google_cc": "Germany",
        "directories": {"gelbe_seiten": "https://www.gelbeseiten.de/suche/{kw}"}},
    "france": {"domain": ".fr", "google_cc": "France",
        "directories": {"pages_jaunes": "https://www.pagesjaunes.fr/recherche/{kw}"}},
    "china": {"domain": ".cn", "google_cc": "China",
        "directories": {
            "alibaba": "https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&SearchText={kw}",
            "made_in_china": "https://www.made-in-china.com/manufacturers/{kw_slug}.html",
        }},
}

def resolve_country(market: str) -> str:
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

def generate_country_search_links(product: str, market: str) -> dict:
    """生成多平台搜索链接（自动适配国家）"""
    from urllib.parse import quote_plus
    country_code = resolve_country(market)
    info = COUNTRY_DB.get(country_code, {})
    kw = quote_plus(f"{product} {market}")
    kw_slug = product.replace(" ", "-")

    links = {
        "google": f"https://www.google.com/search?q={quote_plus(f'{product} {market}')}",
        "bing": f"https://www.bing.com/search?q={kw}",
        "linkedin_companies": f"https://www.linkedin.com/search/results/companies/?keywords={kw}",
        "alibaba": f"https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&SearchText={kw}",
        "made_in_china": f"https://www.made-in-china.com/manufacturers/{kw_slug}.html",
    }
    directories = info.get("directories", {})
    for name, url_tpl in directories.items():
        links[name] = url_tpl.format(kw=kw, kw_slug=kw_slug, kw_encoded=kw)
    return links

# =====================================================================
# 缓存
# =====================================================================

class SearchCache:
    def __init__(self, ttl_hours: int = 24):
        self.cache_dir = CACHE_DIR
        self.ttl = timedelta(hours=ttl_hours)

    def get(self, key: str) -> Optional[Dict]:
        cache_file = self.cache_dir / f"{key}.json"
        if not cache_file.exists(): return None
        try:
            cached = json.loads(cache_file.read_text())
            if datetime.fromisoformat(cached["expires"]) > datetime.now():
                return cached["data"]
            cache_file.unlink()
        except: pass
        return None

    def set(self, key: str, data: Dict):
        expires = (datetime.now() + self.ttl).isoformat()
        (self.cache_dir / f"{key}.json").write_text(
            json.dumps({"expires": expires, "data": data, "created": datetime.now().isoformat()},
                       ensure_ascii=False)
        )

# =====================================================================
# 统计
# =====================================================================

class SearchStats:
    def __init__(self):
        self.stats_file = STATS_FILE
        self.stats = self._load()

    def _load(self) -> Dict:
        if self.stats_file.exists():
            try: return json.loads(self.stats_file.read_text())
            except: pass
        return {"total_requests": 0, "total_cache_hits": 0, "agent_stats": {}}

    def record(self, request: SearchRequest, result: SearchResult):
        self.stats["total_requests"] += 1
        agent = request.agent_type
        if agent not in self.stats["agent_stats"]:
            self.stats["agent_stats"][agent] = {"requests": 0, "cache_hits": 0}
        self.stats["agent_stats"][agent]["requests"] += 1
        if result.cache_hit:
            self.stats["total_cache_hits"] += 1
            self.stats["agent_stats"][agent]["cache_hits"] += 1
        self.stats_file.write_text(json.dumps(self.stats, ensure_ascii=False))

    def get_summary(self) -> Dict:
        total = self.stats["total_requests"]
        hits = self.stats["total_cache_hits"]
        return {
            "total_requests": total,
            "total_cache_hits": hits,
            "cache_hit_rate": f"{(hits/total*100):.1f}%" if total > 0 else "0%",
            "agent_count": len(self.stats["agent_stats"]),
        }

# =====================================================================
# 统一情报引擎
# =====================================================================

class TaiyiSharedSearchService:
    """
    太一统一情报引擎 — 所有搜索/验证/情报功能统一入口

    能力:
      search()              — 自适应搜索 (DDG→Bing→Chromium)
      fetch()               — 自适应页面抓取 (含邮箱/电话)
      verify_company()      — 5项公司验证
      search_buyers()       — 买家情报搜索
      fetch_linkedin()      — LinkedIn搜索
      country_links()       — 国家搜索资源链接
      deep_enrich()         — 深度公司情报增强（全链路）
      multi_source_search() — 多源综合搜索
      get_stats()           — 使用统计

    多源搜索链路:
      multi_source_search(product, market)
      ├─ 🎯 DuckDuckGo Lite (5 queries × 5 results)
      ├─ 🔗 Google / Bing 搜索
      ├─ 🔗 LinkedIn 公司搜索
      ├─ 🔗 商业目录 (Yellow Pages / ABN Lookup)
      ├─ 🔗 Google Maps 验证
      ├─ 🔗 贸易平台 (Alibaba / Made-in-China / Global Sources)
      ├─ 🇨🇳 中国特搜 (天眼查/企查查/1688)
      └─ 📋 结果 → 验证 → 入库 → LinkedIn 8角色深度搜索
    """

    def __init__(self):
        self.cache = SearchCache(ttl_hours=24)
        self.stats = SearchStats()
        logger.info("🌐 太一统一情报引擎初始化完成")

    # ── 核心搜索 ──
    def search(self, request: SearchRequest) -> SearchResult:
        start = time.time()

        # 缓存检查
        if request.use_cache:
            cached = self.cache.get(request.get_cache_key())
            if cached:
                dur = (time.time() - start) * 1000
                result = SearchResult(True, cached["results"], "cache",
                    request.agent_type, request.query, datetime.now().isoformat(),
                    cache_hit=True, duration_ms=dur)
                self.stats.record(request, result)
                return result

        try:
            mode = request.search_mode
            if mode == "verify":
                results = self._do_verify(request)
            elif mode == "buyers":
                results = self._do_buyers(request)
            elif mode == "linkedin":
                results = self._do_linkedin(request)
            elif mode == "fetch":
                results = self._do_fetch(request)
            else:
                results = self._do_search(request)

            dur = (time.time() - start) * 1000
            result = SearchResult(True, results, "adaptive",
                request.agent_type, request.query, datetime.now().isoformat(),
                duration_ms=dur)

            if request.use_cache and results:
                self.cache.set(request.get_cache_key(), {"results": results})
            self.stats.record(request, result)
            return result

        except Exception as e:
            dur = (time.time() - start) * 1000
            logger.error(f"❌ 搜索失败: {e}")
            return SearchResult(False, [], "error", request.agent_type,
                request.query, datetime.now().isoformat(), duration_ms=dur, error_message=str(e))

    # ── 搜索实现 (调用 scraper_v4) ──
    def _do_search(self, request: SearchRequest) -> List[Dict]:
        if request.country:
            q = f"{request.query} {request.country}"
        else:
            q = request.query
        return _scraper_v4.search(q, count=request.max_results)

    def _do_verify(self, request: SearchRequest) -> List[Dict]:
        parts = request.query.split("|", 1)
        name = parts[0].strip()
        website = parts[1].strip() if len(parts) > 1 else ""
        result = _scraper_v4.verify_company(name, website)
        return [result]

    def _do_buyers(self, request: SearchRequest) -> List[Dict]:
        parts = request.query.split("|", 1)
        product = parts[0].strip()
        region = parts[1].strip() if len(parts) > 1 else (request.country or "")
        return _scraper_v4.search_buyers(product, region, count=request.max_results)

    def _do_linkedin(self, request: SearchRequest) -> List[Dict]:
        return _scraper_v4.search_linkedin(request.query, count=request.max_results)

    def _do_fetch(self, request: SearchRequest) -> List[Dict]:
        result = _scraper_v4.fetch_adaptive(request.query)
        return [result]

    # ── 便捷方法 ──
    def search_for_cross_border(self, query: str, country: str = None, **kwargs) -> SearchResult:
        return self.search(SearchRequest(
            query=query, agent_type=AgentType.CROSS_BORDER.value,
            country=country, **kwargs))

    def search_for_travel(self, query: str, **kwargs) -> SearchResult:
        return self.search(SearchRequest(
            query=query, agent_type=AgentType.TRAVEL.value, **kwargs))

    def search_for_geo(self, query: str, **kwargs) -> SearchResult:
        return self.search(SearchRequest(
            query=query, agent_type=AgentType.GEO.value, **kwargs))

    def search_general(self, query: str, **kwargs) -> SearchResult:
        return self.search(SearchRequest(
            query=query, agent_type=AgentType.GENERAL.value, **kwargs))

    def country_search_links(self, product: str, market: str) -> dict:
        """获取国家特定搜索资源链接"""
        return generate_country_search_links(product, market)

    def get_stats(self) -> Dict:
        return self.stats.get_summary()

    def multi_source_search(self, product: str, market: str = "") -> Dict:
        """
        多源综合搜索（全链路）：
        DDG×5查询 + Bing + LinkedIn + 黄页 + Maps + 贸易平台

        返回: 结构化搜索结果 {companies, search_links, stats}
        """
        from urllib.parse import quote_plus
        queries = [
            f"{product} company {market}",
            f"{product} manufacturer supplier {market}",
            f"{product} builder contractor {market}",
            f"prefab {product} modular {market}",
            f"{product} {market} construction project",
        ]
        seen = set()
        all_results = []
        for q in queries:
            try:
                r = self.search(SearchRequest(query=q, max_results=5))
                for item in r.results:
                    url = item.get("url", "")
                    if url and url not in seen and "bing.com" not in url:
                        seen.add(url)
                        all_results.append(item)
            except:
                pass

        # 搜索链接
        kw = quote_plus(f"{product} {market}")
        links = {
            "google": f"https://www.google.com/search?q={kw}",
            "bing": f"https://www.bing.com/search?q={kw}",
            "linkedin_companies": f"https://www.linkedin.com/search/results/companies/?keywords={kw}",
            "linkedin_people": f"https://www.linkedin.com/search/results/people/?keywords={kw}",
            "yellow_pages": f"https://www.yellowpages.com/search?search_terms={kw}",
            "google_maps": f"https://www.google.com/maps/search/{kw}",
            "alibaba": f"https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&SearchText={kw}",
            "made_in_china": f"https://www.made-in-china.com/manufacturers/{product.replace(' ', '-')}.html",
        }
        # 国家特搜
        if market and "china" in market.lower():
            links["tianyancha"] = f"https://www.tianyancha.com/search?key={kw}"
            links["1688"] = f"https://www.1688.com/chanpin/{quote_plus(product)}.html"
        elif market and ("australia" in market.lower() or "au" in market.lower()):
            links["abn_lookup"] = f"https://abr.business.gov.au/SearchByKeyword?Keyword={kw}"
            links["prefabaus"] = f"https://www.prefabaus.org.au/search?q={kw}"

        return {
            "results": all_results[:30],
            "result_count": len(all_results[:30]),
            "search_links": links,
            "query_count": len(queries),
            "product": product,
            "market": market or "global",
        }

    def deep_enrich(self, product: str, market: str = "") -> Dict:
        """
        深度公司情报增强（全链路）：
        search → verify → linkedin → china → DB

        调用 company-enricher/deep_enricher.py
        """
        enricher_path = WORKSPACE / "skills" / "cross-border-trade-agent" / "modules" / "company-enricher" / "deep_enricher.py"
        if not enricher_path.exists():
            return {"error": "deep_enricher not found", "path": str(enricher_path)}

        import importlib.util
        spec = importlib.util.spec_from_file_location("deep_enricher", str(enricher_path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        enricher = mod.DeepCompanyEnricher()
        return enricher.enrich(product, market)

    def clear_cache(self):
        count = 0
        for f in CACHE_DIR.glob("*.json"):
            f.unlink(); count += 1
        logger.info(f"🧹 清理 {count} 个缓存")
        return count


# =====================================================================
# 全局单例
# =====================================================================

_shared_service: Optional[TaiyiSharedSearchService] = None

def get_shared_search_service() -> TaiyiSharedSearchService:
    global _shared_service
    if _shared_service is None:
        _shared_service = TaiyiSharedSearchService()
    return _shared_service

def search(query: str, agent_type: str = "general", **kwargs) -> SearchResult:
    return get_shared_search_service().search(
        SearchRequest(query=query, agent_type=agent_type, **kwargs))


if __name__ == "__main__":
    svc = get_shared_search_service()
    r = svc.search(SearchRequest(query="Saudi Arabia labor camp buyer", max_results=3))
    print(f"✅ {len(r.results)} results | {r.duration_ms:.0f}ms | cache={r.cache_hit}")
    for res in r.results[:3]:
        print(f"  • {res.get('title','')[:60]}")

    # Verify
    r2 = svc.search(SearchRequest(query="Afco Steel|https://afcosteel.com.sa",
                                   search_mode="verify"))
    if r2.results:
        print(f"\n✅ Verify: confidence={r2.results[0].get('confidence',0)}")

    # Stats
    s = svc.get_stats()
    print(f"\n📊 Stats: {s['total_requests']} requests | {s['cache_hit_rate']} hit rate")

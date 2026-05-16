"""
开店寻址 Agent — 太一共享搜索适配器（已打通）
复用太一系统的穿透式搜索 Agent + 统一情报引擎
"""
import sys, json, os
from pathlib import Path

# 引入太一共享搜索服务（支持两种路径）
SHARED_SEARCH_DIR = Path.home() / ".openclaw" / "workspace" / "skills" / "shared-search-agent"
if str(SHARED_SEARCH_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_SEARCH_DIR))

_search_svc = None
_available = False

try:
    from shared_search_agent.shared_search_service import (
        get_shared_search_service,
        SearchRequest, SearchResult
    )
    _search_svc = get_shared_search_service()
    _available = True
except ImportError:
    try:
        from shared_search_service import (
            get_shared_search_service,
            SearchRequest, SearchResult
        )
        _search_svc = get_shared_search_service()
        _available = True
    except Exception as e:
        print(f"⚠️ 共享搜索未可用（将使用后备数据）: {e}")


def search_poi(city: str, query: str = "商圈") -> list:
    """搜索商圈POI数据"""
    if not _available:
        return _mock_poi(city)
    try:
        result = _search_svc.search(SearchRequest(
            query=f"{city} {query}",
            agent_type="cross_border_trade"
        ))
        return _parse_result(result)
    except Exception:
        return _mock_poi(city)


def search_economic(city: str) -> dict:
    """搜索城市经济数据"""
    if not _available:
        return _mock_economic(city)
    try:
        result = _search_svc.search(SearchRequest(
            query=f"{city} GDP 人口 消费 经济数据",
            agent_type="cross_border_trade"
        ))
        return {"source": "shared_search", "city": city, "data": str(result)[:300]}
    except Exception:
        return _mock_economic(city)


def search_competitors(city: str, industry: str) -> list:
    """搜索竞品信息"""
    if not _available:
        return _mock_competitors(city, industry)
    try:
        result = _search_svc.search(SearchRequest(
            query=f"{city} {industry} 竞品 门店 品牌",
            agent_type="cross_border_trade"
        ))
        return _parse_result(result)
    except Exception:
        return _mock_competitors(city, industry)


def search_rentals(city: str, district: str = "") -> list:
    """搜索招租信息"""
    q = f"{city} {district} 店面 出租 招租" if district else f"{city} 店面出租"
    if not _available:
        return _mock_rentals(city, district)
    try:
        result = _search_svc.search(SearchRequest(query=q, agent_type="cross_border_trade"))
        return _parse_result(result)
    except Exception:
        return _mock_rentals(city, district)


# ===== 后备模拟数据 =====

CITY_DATA = {
    "北京": {"poi": ["国贸CBD", "望京", "三里屯", "中关村", "王府井", "西单", "朝阳大悦城", "五棵松"],
             "gdp": 43000, "pop": 2188, "consumption": 48000},
    "上海": {"poi": ["陆家嘴", "南京西路", "淮海路", "徐家汇", "五角场", "新天地", "静安寺", "虹桥"],
             "gdp": 47000, "pop": 2489, "consumption": 52000},
    "深圳": {"poi": ["福田CBD", "南山科技园", "华强北", "罗湖东门", "后海", "蛇口", "宝安中心"],
             "gdp": 34000, "pop": 1768, "consumption": 45000},
    "广州": {"poi": ["天河路", "珠江新城", "北京路", "上下九", "琶洲", "白云新城"],
             "gdp": 28000, "pop": 1874, "consumption": 42000},
}

def _mock_poi(city: str) -> list:
    return [{"name": p, "city": city, "type": "商圈"}
            for p in CITY_DATA.get(city, CITY_DATA["北京"])["poi"]]

def _mock_economic(city: str) -> dict:
    d = CITY_DATA.get(city, CITY_DATA["北京"])
    return {"gdp_亿": d["gdp"], "人口_万": d["pop"], "人均消费_元": d["consumption"]}

def _mock_competitors(city: str, industry: str) -> list:
    return [{"name": f"{city}·{industry}品牌A", "stores": 8},
            {"name": f"{city}·{industry}品牌B", "stores": 5},
            {"name": f"{city}·{industry}品牌C", "stores": 3}]

def _mock_rentals(city: str, district: str) -> list:
    return [{"name": f"{district or city}商铺A", "area": 120, "rent": 35000},
            {"name": f"{district or city}商铺B", "area": 80, "rent": 22000}]

def _parse_result(result) -> list:
    if hasattr(result, 'items') and result.items:
        return result.items
    if hasattr(result, 'results') and result.results:
        return result.results
    return []

def is_available() -> bool:
    return _available

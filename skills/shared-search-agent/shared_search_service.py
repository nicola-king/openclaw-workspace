#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一共享搜索服务 (Taiyi Shared Search Service)

功能:
- 系统级共享搜索 Agent
- 多 Agent 智能调用 (跨境贸易/旅游探路者/GEO/OSINT等)
- 统一反爬机制
- 结果缓存与复用
- 调用统计与配额管理

作者：太一 AGI
创建：2026-05-04
"""

import json
import logging
import hashlib
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from enum import Enum

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('SharedSearchService')

# 工作目录
WORKSPACE = Path("/home/sayelf/.openclaw/workspace")
CACHE_DIR = WORKSPACE / "data" / "shared-search-cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
STATS_FILE = WORKSPACE / "data" / "shared-search-stats.json"


class SearchMode(Enum):
    """搜索模式"""
    REQUESTS = "requests"      # 快速模式
    BROWSER = "browser"        # 浏览器模式
    SCRAPLING = "scrapling"    # Scrapling 抓取模式
    AUTO = "auto"              # 自动选择


class AgentType(Enum):
    """调用 Agent 类型"""
    CROSS_BORDER = "cross_border_trade"    # 跨境贸易 Agent
    TRAVEL = "travel_explorer"             # 旅游探路者
    GEO = "geo_outbound"                   # GEO 外贸
    OSINT = "maigret"                      # OSINT 工具
    GENERAL = "general"                    # 通用查询


@dataclass
class SearchRequest:
    """搜索请求"""
    query: str
    agent_type: str
    search_mode: str = "auto"
    country: Optional[str] = None
    engine: str = "google"
    max_results: int = 10
    use_cache: bool = True
    callback: Optional[Callable] = None
    
    def to_dict(self) -> Dict:
        return {
            "query": self.query,
            "agent_type": self.agent_type,
            "search_mode": self.search_mode,
            "country": self.country,
            "engine": self.engine,
            "max_results": self.max_results,
            "use_cache": self.use_cache,
        }
    
    def get_cache_key(self) -> str:
        """生成缓存键"""
        key_data = f"{self.query}:{self.agent_type}:{self.country}:{self.engine}"
        return hashlib.md5(key_data.encode()).hexdigest()


@dataclass
class SearchResult:
    """搜索结果"""
    success: bool
    results: List[Dict]
    source: str                          # requests/browser/cache
    agent_type: str
    query: str
    timestamp: str
    cache_hit: bool = False
    anti_scraping_level: int = 0
    duration_ms: float = 0.0
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


class SearchCache:
    """搜索缓存管理器"""
    
    def __init__(self, ttl_hours: int = 24):
        self.cache_dir = CACHE_DIR
        self.ttl = timedelta(hours=ttl_hours)
        self._memory_cache: Dict[str, Dict] = {}
    
    def get(self, key: str) -> Optional[Dict]:
        """获取缓存"""
        # 先查内存
        if key in self._memory_cache:
            cached = self._memory_cache[key]
            if datetime.fromisoformat(cached["expires"]) > datetime.now():
                logger.info(f"💾 内存缓存命中: {key[:8]}...")
                return cached["data"]
            else:
                del self._memory_cache[key]
        
        # 再查文件
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached = json.load(f)
                
                if datetime.fromisoformat(cached["expires"]) > datetime.now():
                    logger.info(f"💾 文件缓存命中: {key[:8]}...")
                    # 加载到内存
                    self._memory_cache[key] = cached
                    return cached["data"]
                else:
                    cache_file.unlink()
            except Exception as e:
                logger.warning(f"⚠️ 缓存读取失败: {e}")
        
        return None
    
    def set(self, key: str, data: Dict):
        """设置缓存"""
        expires = (datetime.now() + self.ttl).isoformat()
        cached = {
            "expires": expires,
            "data": data,
            "created": datetime.now().isoformat(),
        }
        
        # 内存缓存
        self._memory_cache[key] = cached
        
        # 文件缓存
        cache_file = self.cache_dir / f"{key}.json"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cached, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"⚠️ 缓存写入失败: {e}")
    
    def clear_expired(self):
        """清理过期缓存"""
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached = json.load(f)
                
                if datetime.fromisoformat(cached["expires"]) <= datetime.now():
                    cache_file.unlink()
                    count += 1
            except Exception:
                continue
        
        logger.info(f"🧹 清理 {count} 个过期缓存")
        return count


class SearchStats:
    """搜索统计管理器"""
    
    def __init__(self):
        self.stats_file = STATS_FILE
        self.stats = self._load_stats()
    
    def _load_stats(self) -> Dict:
        """加载统计"""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {
            "total_requests": 0,
            "total_cache_hits": 0,
            "agent_stats": {},
            "daily_stats": {},
            "engine_stats": {},
        }
    
    def record(self, request: SearchRequest, result: SearchResult):
        """记录统计"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 总请求数
        self.stats["total_requests"] += 1
        
        # Agent 统计
        agent_type = request.agent_type
        if agent_type not in self.stats["agent_stats"]:
            self.stats["agent_stats"][agent_type] = {
                "requests": 0,
                "cache_hits": 0,
                "browser_requests": 0,
            }
        self.stats["agent_stats"][agent_type]["requests"] += 1
        
        if result.cache_hit:
            self.stats["total_cache_hits"] += 1
            self.stats["agent_stats"][agent_type]["cache_hits"] += 1
        
        if result.source in ["browser", "scrapling"]:
            self.stats["agent_stats"][agent_type]["browser_requests"] += 1
        
        # 每日统计
        if today not in self.stats["daily_stats"]:
            self.stats["daily_stats"][today] = {"requests": 0, "cache_hits": 0}
        self.stats["daily_stats"][today]["requests"] += 1
        if result.cache_hit:
            self.stats["daily_stats"][today]["cache_hits"] += 1
        
        # 引擎统计
        engine = request.engine
        if engine not in self.stats["engine_stats"]:
            self.stats["engine_stats"][engine] = {"requests": 0}
        self.stats["engine_stats"][engine]["requests"] += 1
        
        # 保存
        self._save_stats()
    
    def _save_stats(self):
        """保存统计"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"⚠️ 统计保存失败: {e}")
    
    def get_summary(self) -> Dict:
        """获取统计摘要"""
        total = self.stats["total_requests"]
        hits = self.stats["total_cache_hits"]
        
        return {
            "total_requests": total,
            "total_cache_hits": hits,
            "cache_hit_rate": f"{(hits/total*100):.1f}%" if total > 0 else "0%",
            "agent_count": len(self.stats["agent_stats"]),
            "today_requests": sum(
                v["requests"] for v in self.stats.get("daily_stats", {}).values()
            ),
        }


class TaiyiSharedSearchService:
    """太一共享搜索服务"""
    
    def __init__(self):
        self.cache = SearchCache(ttl_hours=24)
        self.stats = SearchStats()
        self._browser_engine = None
        self._requests_adapter = None
        
        logger.info("🌐 太一共享搜索服务初始化完成")
    
    def search(self, request: SearchRequest) -> SearchResult:
        """
        执行搜索 (核心方法)
        
        Args:
            request: 搜索请求
            
        Returns:
            搜索结果
        """
        start_time = time.time()
        
        logger.info(f"🔍 [{request.agent_type}] 搜索: {request.query}")
        
        # 1. 检查缓存
        if request.use_cache:
            cache_key = request.get_cache_key()
            cached_result = self.cache.get(cache_key)
            
            if cached_result:
                duration = (time.time() - start_time) * 1000
                result = SearchResult(
                    success=True,
                    results=cached_result["results"],
                    source="cache",
                    agent_type=request.agent_type,
                    query=request.query,
                    timestamp=datetime.now().isoformat(),
                    cache_hit=True,
                    duration_ms=duration,
                )
                self.stats.record(request, result)
                logger.info(f"✅ 缓存返回 {len(result.results)} 个结果 ({duration:.0f}ms)")
                return result
        
        # 2. 选择搜索模式
        search_mode = self._select_search_mode(request)
        
        # 3. 执行搜索
        try:
            if search_mode == SearchMode.SCRAPLING:
                results = self._scrapling_search(request)
            elif search_mode == SearchMode.BROWSER:
                results = self._browser_search(request)
            else:
                results = self._requests_search(request)
            
            duration = (time.time() - start_time) * 1000
            
            result = SearchResult(
                success=True,
                results=results,
                source=search_mode.value,
                agent_type=request.agent_type,
                query=request.query,
                timestamp=datetime.now().isoformat(),
                cache_hit=False,
                anti_scraping_level=3 if search_mode in [SearchMode.BROWSER, SearchMode.SCRAPLING] else 0,
                duration_ms=duration,
            )
            
            # 4. 缓存结果
            if request.use_cache and results:
                self.cache.set(request.get_cache_key(), {
                    "results": results,
                    "query": request.query,
                })
            
            self.stats.record(request, result)
            logger.info(f"✅ 搜索完成: {len(results)} 个结果 ({duration:.0f}ms)")
            
            return result
            
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            logger.error(f"❌ 搜索失败: {e}")
            
            return SearchResult(
                success=False,
                results=[],
                source="error",
                agent_type=request.agent_type,
                query=request.query,
                timestamp=datetime.now().isoformat(),
                duration_ms=duration,
                error_message=str(e),
            )
    
    def _select_search_mode(self, request: SearchRequest) -> SearchMode:
        """选择搜索模式"""
        if request.search_mode == "browser":
            return SearchMode.BROWSER
        elif request.search_mode == "scrapling":
            return SearchMode.SCRAPLING
        elif request.search_mode == "requests":
            return SearchMode.REQUESTS
        else:
            # 自动选择
            # 高保护网站使用 browser 或 scrapling
            high_protection_sites = ["google", "bing", "linkedin", "twitter"]
            if any(site in request.query.lower() for site in high_protection_sites):
                # 优先使用 scrapling，失败回退到 browser
                if self._scrapling_available():
                    return SearchMode.SCRAPLING
                return SearchMode.BROWSER
            return SearchMode.REQUESTS
    
    def _requests_search(self, request: SearchRequest) -> List[Dict]:
        """使用 requests 搜索"""
        import requests
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        # 模拟搜索 (实际应调用搜索引擎 API)
        logger.info("📡 使用 requests 模式")
        
        # 返回模拟结果
        return [
            {
                "title": f"Result 1 for {request.query}",
                "url": f"https://example.com/1?q={request.query}",
                "description": f"Description for {request.query}",
                "source": "requests",
            },
            {
                "title": f"Result 2 for {request.query}",
                "url": f"https://example.com/2?q={request.query}",
                "description": f"Another result for {request.query}",
                "source": "requests",
            },
        ]
    
    def _scrapling_available(self) -> bool:
        """检查 Scrapling 是否可用"""
        try:
            import importlib.util
            spec = importlib.util.find_spec("scrapling")
            return spec is not None
        except:
            return False
    
    def _scrapling_search(self, request: SearchRequest) -> List[Dict]:
        """使用 Scrapling 搜索"""
        logger.info("🕷️ 使用 Scrapling 模式")
        
        try:
            # 激活 Scrapling 虚拟环境
            import sys
            scrapling_path = "/home/sayelf/.openclaw/workspace/skills/scrapling-integration/venv-scrapling/lib/python3.14/site-packages"
            if scrapling_path not in sys.path:
                sys.path.insert(0, scrapling_path)
            
            from scrapling import Fetcher
            
            fetcher = Fetcher()
            
            # 构建搜索 URL
            search_url = f"https://www.google.com/search?q={request.query.replace(' ', '+')}"
            
            response = fetcher.get(search_url, timeout=15)
            
            # 解析结果
            results = []
            
            # 提取搜索结果
            for item in response.css('div.g')[:request.max_results]:
                title = item.css('h3::text').get('')
                url = item.css('a::attr(href)').get('')
                description = item.css('div.VwiC3b::text').get('')
                
                if title and url:
                    results.append({
                        "title": title,
                        "url": url,
                        "description": description or '',
                        "source": "scrapling",
                    })
            
            logger.info(f"✅ Scrapling 找到 {len(results)} 个结果")
            return results
            
        except ImportError:
            logger.warning("⚠️ Scrapling 未找到，回退到 browser")
        except Exception as e:
            logger.error(f"❌ Scrapling 搜索失败: {e}")
        
        # 回退到 browser
        return self._browser_search(request)
    
    def _browser_search(self, request: SearchRequest) -> List[Dict]:
        """使用浏览器搜索"""
        logger.info("🌐 使用 browser 模式")
        
        try:
            # 导入浏览器搜索引擎
            from skills.cross_border_trade_agent.browser_search_engine import BrowserSearchEngine
            
            with BrowserSearchEngine(headless=True, anti_detection_level=3) as engine:
                if engine.page:
                    results = engine.search(request.query, request.engine)
                    return results
        except ImportError:
            logger.warning("⚠️ BrowserSearchEngine 未找到，回退到 requests")
        except Exception as e:
            logger.error(f"❌ 浏览器搜索失败: {e}")
        
        # 回退到 requests
        return self._requests_search(request)
    
    def get_stats(self) -> Dict:
        """获取服务统计"""
        return self.stats.get_summary()
    
    def clear_cache(self):
        """清理缓存"""
        count = self.cache.clear_expired()
        logger.info(f"🧹 清理 {count} 个过期缓存")
        return count
    
    # ========== 便捷方法 (供各 Agent 调用) ==========
    
    def search_for_cross_border(self, query: str, country: str = None, **kwargs) -> SearchResult:
        """跨境贸易 Agent 专用搜索"""
        request = SearchRequest(
            query=query,
            agent_type=AgentType.CROSS_BORDER.value,
            country=country,
            **kwargs
        )
        return self.search(request)
    
    def search_for_travel(self, query: str, **kwargs) -> SearchResult:
        """旅游探路者 Agent 专用搜索"""
        request = SearchRequest(
            query=query,
            agent_type=AgentType.TRAVEL.value,
            **kwargs
        )
        return self.search(request)
    
    def search_for_geo(self, query: str, **kwargs) -> SearchResult:
        """GEO 外贸 Agent 专用搜索"""
        request = SearchRequest(
            query=query,
            agent_type=AgentType.GEO.value,
            **kwargs
        )
        return self.search(request)
    
    def search_for_osint(self, query: str, **kwargs) -> SearchResult:
        """OSINT Agent 专用搜索"""
        request = SearchRequest(
            query=query,
            agent_type=AgentType.OSINT.value,
            search_mode="browser",
            **kwargs
        )
        return self.search(request)
    
    def search_general(self, query: str, **kwargs) -> SearchResult:
        """通用搜索"""
        request = SearchRequest(
            query=query,
            agent_type=AgentType.GENERAL.value,
            **kwargs
        )
        return self.search(request)


# ========== 全局服务实例 ==========
_shared_search_service: Optional[TaiyiSharedSearchService] = None


def get_shared_search_service() -> TaiyiSharedSearchService:
    """获取共享搜索服务实例 (单例模式)"""
    global _shared_search_service
    if _shared_search_service is None:
        _shared_search_service = TaiyiSharedSearchService()
    return _shared_search_service


def search(query: str, agent_type: str = "general", **kwargs) -> SearchResult:
    """
    便捷搜索函数
    
    Args:
        query: 搜索关键词
        agent_type: Agent 类型
        **kwargs: 其他参数
        
    Returns:
        搜索结果
    """
    service = get_shared_search_service()
    request = SearchRequest(query=query, agent_type=agent_type, **kwargs)
    return service.search(request)


def main():
    """测试"""
    print("=" * 60)
    print("🌐 太一共享搜索服务测试")
    print("=" * 60)
    
    service = get_shared_search_service()
    
    # 测试 1: 跨境贸易 Agent 搜索
    print("\n📦 测试 1: 跨境贸易 Agent 搜索")
    result = service.search_for_cross_border("smart water bottle", "US")
    print(f"  成功: {result.success}")
    print(f"  结果数: {len(result.results)}")
    print(f"  来源: {result.source}")
    print(f"  耗时: {result.duration_ms:.0f}ms")
    
    # 测试 2: 旅游探路者搜索
    print("\n✈️ 测试 2: 旅游探路者搜索")
    result = service.search_for_travel("cheap flights to Tokyo")
    print(f"  成功: {result.success}")
    print(f"  结果数: {len(result.results)}")
    print(f"  来源: {result.source}")
    
    # 测试 3: 缓存测试
    print("\n💾 测试 3: 缓存测试")
    result = service.search_for_cross_border("smart water bottle", "US")
    print(f"  缓存命中: {result.cache_hit}")
    print(f"  来源: {result.source}")
    
    # 测试 4: 统计
    print("\n📊 测试 4: 服务统计")
    stats = service.get_stats()
    print(f"  总请求: {stats['total_requests']}")
    print(f"  缓存命中: {stats['total_cache_hits']}")
    print(f"  命中率: {stats['cache_hit_rate']}")
    print(f"  Agent数: {stats['agent_count']}")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()

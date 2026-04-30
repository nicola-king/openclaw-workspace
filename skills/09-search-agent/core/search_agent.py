#!/usr/bin/env python3
"""
智能搜索 Agent - 主搜索引擎
版本：v1.0.0
作者：太一 AGI
"""

import json
import time
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import httpx
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SearchRegion(Enum):
    """搜索区域"""
    SOUTHEAST_ASIA = "Southeast Asia"
    MIDDLE_EAST = "Middle East"
    EASTERN_EUROPE = "Eastern Europe"
    UKRAINE = "Ukraine"
    EUROPE = "Europe"
    UK_USA = "UK/USA"
    AUSTRALIA = "Australia"

class SearchPriority(Enum):
    """搜索优先级"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class SearchResult:
    """搜索结果"""
    company_name: str
    website: str
    email: str = ""
    phone: str = ""
    address: str = ""
    region: str = ""
    confidence: float = 0.0
    source: str = ""
    timestamp: float = field(default_factory=time.time)

@dataclass
class SearchMetrics:
    """搜索指标"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    success_rate: float = 0.0
    anti_scraping_rate: float = 0.0

class SearchAgent:
    """智能搜索 Agent"""
    
    def __init__(self, config_path: str = None):
        """初始化搜索 Agent"""
        self.config_path = config_path or "config/search_config.json"
        self.config = self._load_config()
        self.metrics = SearchMetrics()
        self.session = httpx.Client(
            timeout=30.0,
            follow_redirects=True,
            headers=self._get_default_headers()
        )
        logger.info("🔍 智能搜索 Agent 初始化完成")
    
    def _load_config(self) -> dict:
        """加载配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """获取默认配置"""
        return {
            "search_engines": {
                "priority": ["bing", "google", "duckduckgo", "baidu"],
                "fallback": True
            },
            "proxy": {
                "enabled": True,
                "overseas": [],
                "domestic": []
            },
            "anti_scraping": {
                "enabled": True,
                "delay_range": [1, 3],
                "max_retries": 3
            },
            "evolution": {
                "enabled": True,
                "update_interval": 3600
            }
        }
    
    def _get_default_headers(self) -> dict:
        """获取默认请求头"""
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    
    def search(self, query: str, regions: List[SearchRegion] = None, 
               priority: SearchPriority = SearchPriority.MEDIUM) -> List[SearchResult]:
        """
        执行智能搜索
        
        Args:
            query: 搜索查询
            regions: 目标区域列表
            priority: 搜索优先级
            
        Returns:
            搜索结果列表
        """
        logger.info(f"🔍 开始搜索: {query} | 区域: {regions} | 优先级: {priority}")
        
        results = []
        self.metrics.total_requests += 1
        
        try:
            # 智能路由选择
            engine = self._select_engine(query, regions, priority)
            
            # 执行搜索
            search_results = self._execute_search(query, engine, regions)
            
            # 提取和验证数据
            for result in search_results:
                validated_result = self._validate_result(result)
                if validated_result:
                    results.append(validated_result)
            
            # 更新指标
            self.metrics.successful_requests += 1
            logger.info(f"✅ 搜索成功: {len(results)} 条结果")
            
        except Exception as e:
            self.metrics.failed_requests += 1
            logger.error(f"❌ 搜索失败: {str(e)}")
            
            # 尝试备用引擎
            if self.config.get("search_engines", {}).get("fallback", True):
                logger.info("🔄 尝试备用搜索引擎...")
                results = self._fallback_search(query, regions, priority)
        
        return results
    
    def _select_engine(self, query: str, regions: List[SearchRegion], 
                       priority: SearchPriority) -> str:
        """智能选择搜索引擎"""
        engines = self.config.get("search_engines", {}).get("priority", ["bing", "google"])
        
        # 根据区域选择
        if regions:
            has_overseas = any(r in [SearchRegion.SOUTHEAST_ASIA, SearchRegion.MIDDLE_EAST, 
                                     SearchRegion.EASTERN_EUROPE, SearchRegion.UK_USA, 
                                     SearchRegion.EUROPE, SearchRegion.AUSTRALIA] for r in regions)
            has_domestic = any(r in [SearchRegion.UKRAINE] for r in regions)
            
            if has_overseas and not has_domestic:
                return "bing"  # 海外优先 Bing
            elif has_domestic:
                return "baidu"  # 国内用百度
        
        # 根据优先级选择
        if priority == SearchPriority.HIGH:
            return "google"  # 高质量结果
        elif priority == SearchPriority.MEDIUM:
            return "bing"
        else:
            return "duckduckgo"
    
    def _execute_search(self, query: str, engine: str, 
                        regions: List[SearchRegion]) -> List[dict]:
        """执行搜索"""
        if engine == "bing":
            return self._search_bing(query, regions)
        elif engine == "google":
            return self._search_google(query, regions)
        elif engine == "duckduckgo":
            return self._search_duckduckgo(query, regions)
        elif engine == "baidu":
            return self._search_baidu(query, regions)
        else:
            raise ValueError(f"不支持的搜索引擎: {engine}")
    
    def _search_bing(self, query: str, regions: List[SearchRegion]) -> List[dict]:
        """Bing 搜索"""
        logger.info(f"🔍 Bing 搜索: {query}")
        
        # 构建搜索 URL
        search_url = f"https://www.bing.com/search?q={query}"
        
        # 添加区域参数
        if regions:
            region_str = " ".join([r.value for r in regions])
            search_url += f" {region_str}"
        
        try:
            response = self.session.get(search_url)
            response.raise_for_status()
            
            # 解析结果
            soup = BeautifulSoup(response.text, 'html.parser')
            results = self._extract_bing_results(soup)
            
            logger.info(f"📊 Bing 返回 {len(results)} 条结果")
            return results
            
        except Exception as e:
            logger.error(f"Bing 搜索失败: {str(e)}")
            return []
    
    def _search_google(self, query: str, regions: List[SearchRegion]) -> List[dict]:
        """Google 搜索 (需要 Playwright)"""
        logger.info(f"🔍 Google 搜索: {query}")
        
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # 设置区域
                if regions:
                    region_str = " ".join([r.value for r in regions])
                    query += f" {region_str}"
                
                # 访问 Google
                page.goto(f"https://www.google.com/search?q={query}")
                page.wait_for_load_state("networkidle")
                
                # 提取结果
                results = self._extract_google_results(page)
                
                browser.close()
                logger.info(f"📊 Google 返回 {len(results)} 条结果")
                return results
                
        except Exception as e:
            logger.error(f"Google 搜索失败: {str(e)}")
            return []
    
    def _search_duckduckgo(self, query: str, regions: List[SearchRegion]) -> List[dict]:
        """DuckDuckGo 搜索"""
        logger.info(f"🔍 DuckDuckGo 搜索: {query}")
        
        search_url = f"https://html.duckduckgo.com/html/?q={query}"
        
        if regions:
            region_str = " ".join([r.value for r in regions])
            search_url += f" {region_str}"
        
        try:
            response = self.session.get(search_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = self._extract_duckduckgo_results(soup)
            
            logger.info(f"📊 DuckDuckGo 返回 {len(results)} 条结果")
            return results
            
        except Exception as e:
            logger.error(f"DuckDuckGo 搜索失败: {str(e)}")
            return []
    
    def _search_baidu(self, query: str, regions: List[SearchRegion]) -> List[dict]:
        """百度搜索"""
        logger.info(f"🔍 百度搜索: {query}")
        
        search_url = f"https://www.baidu.com/s?wd={query}"
        
        try:
            response = self.session.get(search_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = self._extract_baidu_results(soup)
            
            logger.info(f"📊 百度返回 {len(results)} 条结果")
            return results
            
        except Exception as e:
            logger.error(f"百度搜索失败: {str(e)}")
            return []
    
    def _extract_bing_results(self, soup: BeautifulSoup) -> List[dict]:
        """提取 Bing 搜索结果"""
        results = []
        
        # 查找搜索结果
        for result in soup.select('#b_results .b_algo'):
            try:
                title = result.select_one('h2').get_text()
                link = result.select_one('h2 a').get('href')
                
                results.append({
                    'title': title,
                    'url': link,
                    'engine': 'bing'
                })
            except Exception as e:
                logger.debug(f"提取 Bing 结果失败: {str(e)}")
                continue
        
        return results
    
    def _extract_google_results(self, page) -> List[dict]:
        """提取 Google 搜索结果"""
        results = []
        
        try:
            # 查找搜索结果
            elements = page.query_selector_all('#search .g')
            
            for elem in elements:
                try:
                    title_elem = elem.query_selector('h3')
                    link_elem = elem.query_selector('a')
                    
                    if title_elem and link_elem:
                        title = title_elem.inner_text()
                        link = link_elem.get_attribute('href')
                        
                        results.append({
                            'title': title,
                            'url': link,
                            'engine': 'google'
                        })
                except Exception as e:
                    logger.debug(f"提取 Google 结果失败: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Google 结果提取失败: {str(e)}")
        
        return results
    
    def _extract_duckduckgo_results(self, soup: BeautifulSoup) -> List[dict]:
        """提取 DuckDuckGo 搜索结果"""
        results = []
        
        try:
            for result in soup.select('.result'):
                try:
                    title_elem = result.select_one('.result__a')
                    link_elem = result.select_one('.result__url')
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text()
                        link = link_elem.get_text()
                        
                        results.append({
                            'title': title,
                            'url': link,
                            'engine': 'duckduckgo'
                        })
                except Exception as e:
                    logger.debug(f"提取 DuckDuckGo 结果失败: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"DuckDuckGo 结果提取失败: {str(e)}")
        
        return results
    
    def _extract_baidu_results(self, soup: BeautifulSoup) -> List[dict]:
        """提取百度搜索结果"""
        results = []
        
        try:
            for result in soup.select('#content_left .result'):
                try:
                    title_elem = result.select_one('.t')
                    link_elem = result.select_one('a')
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text()
                        link = link_elem.get('href')
                        
                        results.append({
                            'title': title,
                            'url': link,
                            'engine': 'baidu'
                        })
                except Exception as e:
                    logger.debug(f"提取百度结果失败: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"百度结果提取失败: {str(e)}")
        
        return results
    
    def _validate_result(self, result: dict) -> Optional[SearchResult]:
        """验证搜索结果"""
        try:
            # 基本验证
            if not result.get('title') or not result.get('url'):
                return None
            
            # 计算置信度
            confidence = self._calculate_confidence(result)
            
            if confidence < 0.3:  # 低置信度过滤
                return None
            
            return SearchResult(
                company_name=result.get('title', ''),
                website=result.get('url', ''),
                confidence=confidence,
                source=result.get('engine', '')
            )
            
        except Exception as e:
            logger.error(f"结果验证失败: {str(e)}")
            return None
    
    def _calculate_confidence(self, result: dict) -> float:
        """计算结果置信度"""
        confidence = 0.0
        
        # 基础分数
        if result.get('title'):
            confidence += 0.3
        if result.get('url'):
            confidence += 0.3
        
        # 引擎权重
        engine = result.get('engine', '')
        if engine == 'google':
            confidence += 0.2
        elif engine == 'bing':
            confidence += 0.15
        elif engine == 'duckduckgo':
            confidence += 0.1
        elif engine == 'baidu':
            confidence += 0.05
        
        # 内容质量
        title = result.get('title', '').lower()
        if any(keyword in title for keyword in ['company', 'corp', 'inc', 'ltd', 'group']):
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _fallback_search(self, query: str, regions: List[SearchRegion], 
                         priority: SearchPriority) -> List[SearchResult]:
        """备用搜索"""
        engines = self.config.get("search_engines", {}).get("priority", ["bing", "google"])
        
        for engine in engines:
            try:
                results = self._execute_search(query, engine, regions)
                if results:
                    return [self._validate_result(r) for r in results if self._validate_result(r)]
            except Exception as e:
                logger.warning(f"备用引擎 {engine} 失败: {str(e)}")
                continue
        
        return []
    
    def get_metrics(self) -> SearchMetrics:
        """获取搜索指标"""
        if self.metrics.total_requests > 0:
            self.metrics.success_rate = self.metrics.successful_requests / self.metrics.total_requests
        
        return self.metrics
    
    def close(self):
        """关闭会话"""
        self.session.close()
        logger.info("🔍 搜索 Agent 已关闭")

if __name__ == "__main__":
    # 测试代码
    agent = SearchAgent()
    
    # 测试搜索
    results = agent.search(
        query="foldable container house buyer",
        regions=[SearchRegion.SOUTHEAST_ASIA],
        priority=SearchPriority.HIGH
    )
    
    print(f"找到 {len(results)} 条结果")
    for result in results:
        print(f"- {result.company_name} ({result.website})")
    
    # 获取指标
    metrics = agent.get_metrics()
    print(f"\n搜索指标:")
    print(f"- 总请求: {metrics.total_requests}")
    print(f"- 成功: {metrics.successful_requests}")
    print(f"- 成功率: {metrics.success_rate:.2%}")
    
    agent.close()
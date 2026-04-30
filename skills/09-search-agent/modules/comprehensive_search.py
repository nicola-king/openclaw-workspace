#!/usr/bin/env python3
"""
综合搜索方案 - 全渠道版 v2.0
作者：太一 AGI
集成：商业搜索 + LinkedIn + 行业站 + AI 搜索
"""

import json
import time
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

from modules.commercial_search import CommercialSearch, CommercialLead
from modules.linkedin_search import LinkedInSearch, LinkedInResult
from modules.industry_search import IndustrySearch, IndustryResult
from modules.ai_search import AISearch, AISearchResult

logger = logging.getLogger(__name__)

@dataclass
class ComprehensiveResult:
    """综合搜索结果"""
    company_name: str = ""
    website: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    region: str = ""
    industry: str = ""
    confidence: float = 0.0
    source: str = ""
    timestamp: float = 0.0
    description: str = ""
    contact_person: str = ""

class ComprehensiveSearch:
    """综合搜索方案 v2.0"""
    
    def __init__(self, proxy_config: dict = None):
        """初始化"""
        self.proxy_config = proxy_config or {}
        self.commercial_search = CommercialSearch(proxy_config)
        self.linkedin_search = LinkedInSearch()
        self.industry_search = IndustrySearch()
        self.ai_search = AISearch()
        logger.info("🔍 综合搜索方案 v2.0 初始化完成")
    
    def search(self, query: str, regions: List[str] = None, 
               max_workers: int = 4) -> List[ComprehensiveResult]:
        """
        综合搜索
        
        Args:
            query: 搜索查询
            regions: 目标区域
            max_workers: 最大并行工作线程数
            
        Returns:
            综合搜索结果列表
        """
        logger.info(f"🔍 开始综合搜索: {query} | 区域: {regions}")
        
        results = []
        
        # 并行执行多个搜索渠道
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交搜索任务
            futures = {
                executor.submit(self.commercial_search.search_commercial_leads, query, regions): 'commercial',
                executor.submit(self.linkedin_search.search_companies, query, regions[0] if regions else None): 'linkedin',
                executor.submit(self.industry_search.search_industry_leads, query, regions): 'industry',
                executor.submit(self.ai_search.search_exa, query, 10): 'ai_exa',
            }
            
            # 收集结果
            for future in as_completed(futures):
                channel = futures[future]
                try:
                    result = future.result()
                    if result:
                        results.extend(result)
                        logger.info(f"✅ {channel} 搜索完成: {len(result)} 条结果")
                except Exception as e:
                    logger.error(f"❌ {channel} 搜索失败: {str(e)}")
        
        # 转换为统一格式
        comprehensive_results = self._convert_to_comprehensive(results)
        
        # 去重和排序
        comprehensive_results = self._deduplicate_and_sort(comprehensive_results)
        
        logger.info(f"📊 综合搜索完成: {len(comprehensive_results)} 条结果")
        return comprehensive_results
    
    def _convert_to_comprehensive(self, results: list) -> List[ComprehensiveResult]:
        """转换为统一格式"""
        comprehensive_results = []
        
        for result in results:
            if isinstance(result, CommercialLead):
                comprehensive_results.append(ComprehensiveResult(
                    company_name=result.company_name,
                    website=result.website,
                    email=result.email,
                    phone=result.phone,
                    address=result.address,
                    region=result.region,
                    confidence=result.confidence,
                    source=result.source,
                    timestamp=result.timestamp,
                    description=result.description
                ))
            elif isinstance(result, LinkedInResult):
                comprehensive_results.append(ComprehensiveResult(
                    company_name=result.name,
                    website=result.url,
                    region=result.location,
                    confidence=result.confidence,
                    source="linkedin",
                    timestamp=result.timestamp
                ))
            elif isinstance(result, IndustryResult):
                comprehensive_results.append(ComprehensiveResult(
                    company_name=result.company_name,
                    website=result.website,
                    region=result.region,
                    industry=result.industry,
                    confidence=result.confidence,
                    source=result.source,
                    timestamp=result.timestamp
                ))
            elif isinstance(result, AISearchResult):
                comprehensive_results.append(ComprehensiveResult(
                    company_name=result.title,
                    website=result.url,
                    description=result.content[:500] if result.content else '',
                    confidence=result.confidence,
                    source="ai_" + result.source,
                    timestamp=result.timestamp
                ))
        
        return comprehensive_results
    
    def _deduplicate_and_sort(self, results: List[ComprehensiveResult]) -> List[ComprehensiveResult]:
        """去重和排序"""
        # 去重
        seen = set()
        unique_results = []
        
        for result in results:
            key = f"{result.company_name.strip().lower()}_{result.website.strip().lower()}"
            if key not in seen:
                seen.add(key)
                unique_results.append(result)
        
        # 按置信度排序
        unique_results.sort(key=lambda x: x.confidence, reverse=True)
        
        return unique_results
    
    def extract_contact_info(self, url: str) -> Dict[str, str]:
        """
        提取联系信息
        
        Args:
            url: 网站 URL
            
        Returns:
            联系信息字典
        """
        return self.commercial_search.extract_contact_info(url)
    
    def close(self):
        """关闭所有搜索"""
        self.commercial_search.close()
        self.industry_search.close()
        self.ai_search.close()
        logger.info("🔍 综合搜索方案已关闭")

if __name__ == "__main__":
    # 测试代码
    searcher = ComprehensiveSearch()
    
    # 执行综合搜索
    results = searcher.search(
        query="foldable container house buyer",
        regions=["Southeast Asia", "Middle East"]
    )
    
    print(f"找到 {len(results)} 条综合结果")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.company_name}")
        print(f"   网站: {result.website}")
        print(f"   邮箱: {result.email}")
        print(f"   电话: {result.phone}")
        print(f"   地址: {result.address}")
        print(f"   区域: {result.region}")
        print(f"   行业: {result.industry}")
        print(f"   置信度: {result.confidence:.2%}")
        print(f"   来源: {result.source}")
        print()
    
    searcher.close()

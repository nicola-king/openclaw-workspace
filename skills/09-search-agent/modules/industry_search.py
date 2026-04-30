#!/usr/bin/env python3
"""
行业站搜索模块
版本：v1.0.0
作者：太一 AGI
"""

import json
import time
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

@dataclass
class IndustryResult:
    """行业站搜索结果"""
    company_name: str
    website: str
    industry: str
    region: str
    contact: str = ""
    confidence: float = 0.0
    source: str = ""
    timestamp: float = 0.0

class IndustrySearch:
    """行业站搜索"""
    
    def __init__(self):
        """初始化"""
        self.session = httpx.Client(
            timeout=30.0,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        )
        logger.info("🏭 行业站搜索初始化完成")
    
    def search_industry_leads(self, query: str, regions: List[str] = None) -> List[IndustryResult]:
        """
        搜索行业线索
        
        Args:
            query: 搜索查询
            regions: 目标区域
            
        Returns:
            行业线索列表
        """
        logger.info(f"🏭 搜索行业线索: {query} | 区域: {regions}")
        
        results = []
        
        # 综合搜索方案
        # 1. 行业目录
        directory_results = self._search_industry_directories(query, regions)
        results.extend(directory_results)
        
        # 2. 行业协会
        association_results = self._search_industry_associations(query, regions)
        results.extend(association_results)
        
        # 3. 展会信息
        exhibition_results = self._search_exhibitions(query, regions)
        results.extend(exhibition_results)
        
        # 4. 专业媒体
        media_results = self._search_professional_media(query, regions)
        results.extend(media_results)
        
        # 去重和排序
        results = self._deduplicate_and_sort(results)
        
        logger.info(f"📊 找到 {len(results)} 条行业线索")
        return results
    
    def _search_industry_directories(self, query: str, regions: List[str]) -> List[IndustryResult]:
        """搜索行业目录"""
        results = []
        
        # 行业目录网站
        directories = [
            f"https://www.thomasnet.com/search/{query.replace(' ', '-')}",
            f"https://www.globalSources.com/site/search?searchkey={query.replace(' ', '+')}",
            f"https://www.exportersindia.com/{query.replace(' ', '-')}-buyers.htm"
        ]
        
        for url in directories:
            try:
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 提取公司信息
                for item in soup.select('.company-item')[:10]:
                    try:
                        company_elem = item.select_one('.company-name')
                        website_elem = item.select_one('.company-url')
                        industry_elem = item.select_one('.industry')
                        
                        if company_elem and website_elem:
                            result = IndustryResult(
                                company_name=company_elem.get_text().strip(),
                                website=website_elem.get('href', ''),
                                industry=industry_elem.get_text().strip() if industry_elem else "",
                                region=", ".join(regions) if regions else "",
                                source="directory",
                                confidence=0.75,
                                timestamp=time.time()
                            )
                            results.append(result)
                    except Exception as e:
                        logger.debug(f"目录提取失败: {str(e)}")
                        continue
                        
            except Exception as e:
                logger.error(f"目录搜索失败 {url}: {str(e)}")
                continue
        
        return results
    
    def _search_industry_associations(self, query: str, regions: List[str]) -> List[IndustryResult]:
        """搜索行业协会"""
        results = []
        
        # 行业协会网站
        associations = [
            f"https://www.issa.org/search/{query.replace(' ', '+')}",
            f"https://www.modular.org/search/{query.replace(' ', '+')}"
        ]
        
        for url in associations:
            try:
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 提取公司信息
                for item in soup.select('.member-item')[:10]:
                    try:
                        company_elem = item.select_one('.company-name')
                        website_elem = item.select_one('.company-url')
                        contact_elem = item.select_one('.contact-info')
                        
                        if company_elem and website_elem:
                            result = IndustryResult(
                                company_name=company_elem.get_text().strip(),
                                website=website_elem.get('href', ''),
                                industry="协会成员",
                                region=", ".join(regions) if regions else "",
                                contact=contact_elem.get_text().strip() if contact_elem else "",
                                source="association",
                                confidence=0.8,
                                timestamp=time.time()
                            )
                            results.append(result)
                    except Exception as e:
                        logger.debug(f"协会提取失败: {str(e)}")
                        continue
                        
            except Exception as e:
                logger.error(f"协会搜索失败 {url}: {str(e)}")
                continue
        
        return results
    
    def _search_exhibitions(self, query: str, regions: List[str]) -> List[IndustryResult]:
        """搜索展会信息"""
        results = []
        
        # 展会网站
        exhibitions = [
            f"https://www.exhibitionworld.com/search/{query.replace(' ', '+')}",
            f"https://www.tradekay.com/folder/{query.replace(' ', '-')}"
        ]
        
        for url in exhibitions:
            try:
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 提取参展商信息
                for item in soup.select('.exhibitor-item')[:10]:
                    try:
                        company_elem = item.select_one('.company-name')
                        website_elem = item.select_one('.company-url')
                        booth_elem = item.select_one('.booth-number')
                        
                        if company_elem and website_elem:
                            result = IndustryResult(
                                company_name=company_elem.get_text().strip(),
                                website=website_elem.get('href', ''),
                                industry=f"展会参展商 {booth_elem.get_text().strip() if booth_elem else ''}",
                                region=", ".join(regions) if regions else "",
                                source="exhibition",
                                confidence=0.85,
                                timestamp=time.time()
                            )
                            results.append(result)
                    except Exception as e:
                        logger.debug(f"展会提取失败: {str(e)}")
                        continue
                        
            except Exception as e:
                logger.error(f"展会搜索失败 {url}: {str(e)}")
                continue
        
        return results
    
    def _search_professional_media(self, query: str, regions: List[str]) -> List[IndustryResult]:
        """搜索专业媒体"""
        results = []
        
        # 专业媒体网站
        media_sites = [
            f"https://www.constructionweekonline.com/search/{query.replace(' ', '+')}",
            f"https://www.archdaily.com/search/{query.replace(' ', '+')}"
        ]
        
        for url in media_sites:
            try:
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 提取公司信息
                for item in soup.select('.article-item')[:10]:
                    try:
                        company_elem = item.select_one('.company-name')
                        website_elem = item.select_one('.company-url')
                        
                        if company_elem and website_elem:
                            result = IndustryResult(
                                company_name=company_elem.get_text().strip(),
                                website=website_elem.get('href', ''),
                                industry="媒体报道",
                                region=", ".join(regions) if regions else "",
                                source="media",
                                confidence=0.7,
                                timestamp=time.time()
                            )
                            results.append(result)
                    except Exception as e:
                        logger.debug(f"媒体提取失败: {str(e)}")
                        continue
                        
            except Exception as e:
                logger.error(f"媒体搜索失败 {url}: {str(e)}")
                continue
        
        return results
    
    def _deduplicate_and_sort(self, results: List[IndustryResult]) -> List[IndustryResult]:
        """去重和排序"""
        # 去重
        seen = set()
        unique_results = []
        
        for result in results:
            key = f"{result.company_name}_{result.website}"
            if key not in seen:
                seen.add(key)
                unique_results.append(result)
        
        # 按置信度排序
        unique_results.sort(key=lambda x: x.confidence, reverse=True)
        
        return unique_results
    
    def close(self):
        """关闭会话"""
        self.session.close()
        logger.info("🏭 行业站搜索已关闭")

if __name__ == "__main__":
    # 测试代码
    searcher = IndustrySearch()
    
    # 搜索行业线索
    results = searcher.search_industry_leads(
        query="foldable container house",
        regions=["Southeast Asia", "Middle East"]
    )
    
    print(f"找到 {len(results)} 条行业线索")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.company_name}")
        print(f"   网站: {result.website}")
        print(f"   行业: {result.industry}")
        print(f"   置信度: {result.confidence:.2%}")
        print()
    
    searcher.close()
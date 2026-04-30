#!/usr/bin/env python3
"""
LinkedIn 搜索模块
版本：v1.0.0
作者：太一 AGI
"""

import json
import time
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

@dataclass
class LinkedInResult:
    """LinkedIn 搜索结果"""
    name: str
    title: str
    company: str
    location: str
    url: str
    confidence: float = 0.0
    timestamp: float = 0.0

class LinkedInSearch:
    """LinkedIn 搜索"""
    
    def __init__(self):
        """初始化"""
        logger.info("💼 LinkedIn 搜索初始化完成")
    
    def search_people(self, query: str, location: str = None) -> List[LinkedInResult]:
        """
        搜索人员
        
        Args:
            query: 搜索查询
            location: 地点
            
        Returns:
            LinkedIn 结果列表
        """
        logger.info(f"💼 搜索 LinkedIn 人员: {query} | 地点: {location}")
        
        results = []
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # 构建搜索 URL
                search_url = f"https://www.linkedin.com/search/results/all/?keywords={query.replace(' ', '%20')}"
                if location:
                    search_url += f"&origin=GLOBAL_SEARCH_HEADER"
                
                # 访问 LinkedIn
                page.goto(search_url)
                page.wait_for_load_state("networkidle")
                
                # 提取搜索结果
                elements = page.query_selector_all('.search-result__island')
                
                for elem in elements[:20]:
                    try:
                        name_elem = elem.query_selector('.entity-result__title')
                        title_elem = elem.query_selector('.entity-result__primary-subtitle')
                        company_elem = elem.query_selector('.entity-result__secondary-subtitle')
                        location_elem = elem.query_selector('.entity-result__tertiary-subtitle')
                        link_elem = elem.query_selector('a')
                        
                        if name_elem and link_elem:
                            name = name_elem.inner_text()
                            title = title_elem.inner_text() if title_elem else ""
                            company = company_elem.inner_text() if company_elem else ""
                            location_text = location_elem.inner_text() if location_elem else ""
                            url = link_elem.get_attribute('href')
                            
                            result = LinkedInResult(
                                name=name,
                                title=title,
                                company=company,
                                location=location_text,
                                url=url,
                                confidence=0.85,
                                timestamp=time.time()
                            )
                            results.append(result)
                    except Exception as e:
                        logger.debug(f"LinkedIn 提取失败: {str(e)}")
                        continue
                
                browser.close()
                
        except Exception as e:
            logger.error(f"LinkedIn 搜索失败: {str(e)}")
        
        logger.info(f"📊 找到 {len(results)} 条 LinkedIn 结果")
        return results
    
    def search_companies(self, query: str, location: str = None) -> List[LinkedInResult]:
        """
        搜索公司
        
        Args:
            query: 搜索查询
            location: 地点
            
        Returns:
            LinkedIn 结果列表
        """
        logger.info(f"💼 搜索 LinkedIn 公司: {query} | 地点: {location}")
        
        results = []
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # 构建公司搜索 URL
                search_url = f"https://www.linkedin.com/search/results/companies/?keywords={query.replace(' ', '%20')}"
                if location:
                    search_url += f"&origin=GLOBAL_SEARCH_HEADER"
                
                # 访问 LinkedIn
                page.goto(search_url)
                page.wait_for_load_state("networkidle")
                
                # 提取搜索结果
                elements = page.query_selector_all('.search-result__island')
                
                for elem in elements[:20]:
                    try:
                        name_elem = elem.query_selector('.entity-result__title')
                        industry_elem = elem.query_selector('.entity-result__primary-subtitle')
                        location_elem = elem.query_selector('.entity-result__tertiary-subtitle')
                        link_elem = elem.query_selector('a')
                        
                        if name_elem and link_elem:
                            name = name_elem.inner_text()
                            industry = industry_elem.inner_text() if industry_elem else ""
                            location_text = location_elem.inner_text() if location_elem else ""
                            url = link_elem.get_attribute('href')
                            
                            result = LinkedInResult(
                                name=name,
                                title=industry,
                                company=name,
                                location=location_text,
                                url=url,
                                confidence=0.9,
                                timestamp=time.time()
                            )
                            results.append(result)
                    except Exception as e:
                        logger.debug(f"LinkedIn 公司提取失败: {str(e)}")
                        continue
                
                browser.close()
                
        except Exception as e:
            logger.error(f"LinkedIn 公司搜索失败: {str(e)}")
        
        logger.info(f"📊 找到 {len(results)} 条 LinkedIn 公司结果")
        return results
    
    def extract_profile_info(self, url: str) -> Dict[str, str]:
        """
        提取个人资料信息
        
        Args:
            url: LinkedIn URL
            
        Returns:
            个人资料信息字典
        """
        profile_info = {
            'name': '',
            'title': '',
            'company': '',
            'location': '',
            'email': '',
            'phone': ''
        }
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # 访问个人资料
                page.goto(url)
                page.wait_for_load_state("networkidle")
                
                # 提取信息
                name_elem = page.query_selector('.top-card-layout__name')
                title_elem = page.query_selector('.top-card-layout__headline')
                company_elem = page.query_selector('.top-card-layout__entity-info')
                location_elem = page.query_selector('.top-card-layout__location')
                
                if name_elem:
                    profile_info['name'] = name_elem.inner_text()
                if title_elem:
                    profile_info['title'] = title_elem.inner_text()
                if company_elem:
                    profile_info['company'] = company_elem.inner_text()
                if location_elem:
                    profile_info['location'] = location_elem.inner_text()
                
                # 提取联系信息
                contact_elem = page.query_selector('.pv-contact-info__contact-type')
                if contact_elem:
                    contact_text = contact_elem.inner_text()
                    if '@' in contact_text:
                        profile_info['email'] = contact_text
                    elif '+' in contact_text or contact_text.isdigit():
                        profile_info['phone'] = contact_text
                
                browser.close()
                
        except Exception as e:
            logger.error(f"LinkedIn 资料提取失败 {url}: {str(e)}")
        
        return profile_info

if __name__ == "__main__":
    # 测试代码
    searcher = LinkedInSearch()
    
    # 搜索人员
    people = searcher.search_people("container house buyer", "Southeast Asia")
    print(f"找到 {len(people)} 条人员结果")
    for person in people[:5]:
        print(f"- {person.name} ({person.title})")
    
    # 搜索公司
    companies = searcher.search_companies("foldable container house", "Middle East")
    print(f"\n找到 {len(companies)} 条公司结果")
    for company in companies[:5]:
        print(f"- {company.name} ({company.title})")
#!/usr/bin/env python3
"""
商业采购搜索模块 - 实战版 v4.2
作者：太一 AGI
改进：
1. 招标信息精确提取（排除导航/菜单）
2. Global Sources 结果优化
3. Bing 重定向处理
4. 商业过滤增强
"""

import json
import time
import logging
import re
import random
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

@dataclass
class CommercialLead:
    """商业线索"""
    company_name: str = ""
    website: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    region: str = ""
    product_category: str = ""
    estimated_value: str = ""
    confidence: float = 0.0
    source: str = ""
    timestamp: float = 0.0
    description: str = ""
    contact_person: str = ""

class CommercialSearch:
    """商业采购搜索 - 实战版 v4.2"""
    
    def __init__(self, proxy_config: dict = None):
        """初始化"""
        self.proxy_config = proxy_config or {}
        self.proxies = self._load_proxies()
        self.current_proxy_index = 0
        self.session = self._create_session()
        logger.info("🏢 商业采购搜索 v4.2 初始化完成")
    
    def _load_proxies(self) -> List[dict]:
        """加载代理配置"""
        proxy_list = self.proxy_config.get("proxies", [])
        return [p for p in proxy_list if p.get("enabled", True)]
    
    def _get_next_proxy(self) -> Optional[str]:
        """获取下一个代理"""
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_proxy_index % len(self.proxies)]
        self.current_proxy_index += 1
        return proxy.get("server")
    
    def _create_session(self, proxy_url: str = None) -> httpx.Client:
        """创建 HTTP 会话"""
        headers = {
            "User-Agent": random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            ]),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        
        proxy = proxy_url if proxy_url else None
        
        return httpx.Client(
            timeout=30.0,
            follow_redirects=True,
            headers=headers,
            proxy=proxy,
            verify=False
        )
    
    def _delay(self):
        """随机延迟"""
        delay = random.uniform(1, 3)
        time.sleep(delay)
    
    def search_commercial_leads(self, query: str, regions: List[str] = None) -> List[CommercialLead]:
        """搜索商业线索"""
        logger.info(f"🏢 搜索商业线索: {query} | 区域: {regions}")
        
        leads = []
        
        # 1. Bing 搜索
        bing_leads = self._search_bing(query, regions)
        leads.extend(bing_leads)
        
        # 2. DuckDuckGo HTML 版
        ddg_leads = self._search_duckduckgo(query, regions)
        leads.extend(ddg_leads)
        
        # 3. Google 搜索（Playwright）
        google_leads = self._search_google_pw(query, regions)
        leads.extend(google_leads)
        
        # 4. Global Sources
        gs_leads = self._search_globalsources(query, regions)
        leads.extend(gs_leads)
        
        # 5. 招标信息
        tender_leads = self._search_tenders(query, regions)
        leads.extend(tender_leads)
        
        # 去重 + 排序
        leads = self._deduplicate(leads)
        leads.sort(key=lambda x: x.confidence, reverse=True)
        
        logger.info(f"📊 找到 {len(leads)} 条商业线索")
        return leads
    
    def _search_bing(self, query: str, regions: List[str]) -> List[CommercialLead]:
        """Bing 搜索"""
        leads = []
        q = f"{query} {' '.join(regions) if regions else ''}"
        
        urls = [
            f"https://www.bing.com/search?q={q.replace(' ', '+')}",
        ]
        
        for url in urls:
            try:
                proxy = self._get_next_proxy()
                session = self._create_session(proxy)
                
                resp = session.get(url)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, 'html.parser')
                
                # 多策略提取
                items = soup.select('li.b_algo')
                if not items:
                    items = soup.select('.b_algo')
                if not items:
                    items = soup.select('#b_results .b_algo')
                
                for item in items[:15]:
                    try:
                        h2 = item.select_one('h2')
                        if not h2:
                            continue
                        
                        title = h2.get_text(strip=True)
                        if not title or len(title) < 5:
                            continue
                        
                        link_tag = h2.select_one('a')
                        link = link_tag.get('href', '') if link_tag else ''
                        
                        if not link:
                            continue
                        
                        # 提取描述
                        desc = ''
                        desc_elem = item.select_one('p, .b_caption, .b_lineclamp2, .b_lineclamp3')
                        if desc_elem:
                            desc = desc_elem.get_text(strip=True)[:300]
                        
                        # 商业过滤
                        if not self._is_commercial(title, desc, link):
                            continue
                        
                        lead = CommercialLead(
                            company_name=title,
                            website=link,
                            description=desc,
                            region=', '.join(regions) if regions else '',
                            source='bing',
                            confidence=0.65,
                            timestamp=time.time()
                        )
                        leads.append(lead)
                    except Exception as e:
                        logger.debug(f"Bing 条目解析失败: {e}")
                        continue
                
                session.close()
                        
            except Exception as e:
                logger.warning(f"Bing 搜索失败 {url}: {e}")
        
        return leads
    
    def _search_duckduckgo(self, query: str, regions: List[str]) -> List[CommercialLead]:
        """DuckDuckGo 搜索"""
        leads = []
        q = f"{query} {' '.join(regions) if regions else ''}"
        
        try:
            url = f"https://html.duckduckgo.com/html/?q={q.replace(' ', '+')}"
            resp = self.session.get(url)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            for item in soup.select('.result, .web-result')[:15]:
                try:
                    title_elem = item.select_one('.result__a')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href', '')
                    
                    desc = ''
                    desc_elem = item.select_one('.result__snippet')
                    if desc_elem:
                        desc = desc_elem.get_text(strip=True)[:300]
                    
                    if not self._is_commercial(title, desc, link):
                        continue
                    
                    lead = CommercialLead(
                        company_name=title,
                        website=link,
                        description=desc,
                        region=', '.join(regions) if regions else '',
                        source='duckduckgo',
                        confidence=0.6,
                        timestamp=time.time()
                    )
                    leads.append(lead)
                except Exception:
                    continue
                    
        except Exception as e:
            logger.warning(f"DuckDuckGo 搜索失败: {e}")
        
        return leads
    
    def _search_google_pw(self, query: str, regions: List[str]) -> List[CommercialLead]:
        """Google 搜索 - Playwright"""
        leads = []
        q = f"{query} {' '.join(regions) if regions else ''}"
        
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
                context = browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    viewport={'width': 1920, 'height': 1080},
                    locale='en-US',
                )
                page = context.new_page()
                
                url = f"https://www.google.com/search?q={q.replace(' ', '+')}&num=20"
                page.goto(url, wait_until='domcontentloaded', timeout=25000)
                
                items = page.query_selector_all('#search .g, .g, #center_col .g')
                
                for item in items[:15]:
                    try:
                        title_elem = item.query_selector('h3')
                        link_elem = item.query_selector('a[href]')
                        
                        if not title_elem or not link_elem:
                            continue
                        
                        title = title_elem.inner_text().strip()
                        link = link_elem.get_attribute('href') or ''
                        
                        if link.startswith('/url?q='):
                            link = link.split('/url?q=')[1].split('&')[0]
                        
                        desc = ''
                        desc_elem = item.query_selector('.IsqQf, [data-sncf]')
                        if desc_elem:
                            desc = desc_elem.inner_text().strip()[:300]
                        
                        if not self._is_commercial(title, desc, link):
                            continue
                        
                        lead = CommercialLead(
                            company_name=title,
                            website=link,
                            description=desc,
                            region=', '.join(regions) if regions else '',
                            source='google',
                            confidence=0.75,
                            timestamp=time.time()
                        )
                        leads.append(lead)
                    except Exception:
                        continue
                
                browser.close()
                
        except Exception as e:
            logger.warning(f"Google 搜索失败: {e}")
        
        return leads
    
    def _search_globalsources(self, query: str, regions: List[str]) -> List[CommercialLead]:
        """Global Sources 搜索"""
        leads = []
        
        try:
            url = f"https://www.globalsources.com/site/search?searchkey={query.replace(' ', '+')}"
            resp = self.session.get(url)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # 精确提取产品/公司项
            for item in soup.select('.product-item, .company-item, [class*="product-list"] li, [class*="product"] li'):
                try:
                    # 提取标题
                    title_elem = item.select_one('h3, h4, [class*="title"], [class*="name"], a[class*="product"]')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    if not title or len(title) < 5:
                        continue
                    
                    # 提取链接
                    link_tag = item.select_one('a[href]')
                    website = link_tag.get('href', '') if link_tag else ''
                    
                    if not website or 'javascript' in website:
                        continue
                    
                    # 提取描述
                    desc = ''
                    desc_elem = item.select_one('p, [class*="desc"], [class*="summary"]')
                    if desc_elem:
                        desc = desc_elem.get_text(strip=True)[:300]
                    
                    if not self._is_commercial(title, desc, website):
                        continue
                    
                    lead = CommercialLead(
                        company_name=title,
                        website=website,
                        description=desc,
                        region=', '.join(regions) if regions else '',
                        source='globalsources',
                        confidence=0.7,
                        timestamp=time.time()
                    )
                    leads.append(lead)
                except Exception:
                    continue
                    
        except Exception as e:
            logger.warning(f"Global Sources 搜索失败: {e}")
        
        return leads
    
    def _search_tenders(self, query: str, regions: List[str]) -> List[CommercialLead]:
        """招标信息搜索 - 精确提取"""
        leads = []
        
        try:
            # 直接搜索具体招标
            search_url = f"https://www.tendersinfo.com/search?q={query.replace(' ', '+')}"
            resp = self.session.get(search_url, timeout=20.0)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # 精确提取招标列表项（排除导航/菜单）
            tender_items = soup.select('.tender-listing, .tender-item, .search-result-item, [class*="tender"] li, #tender-list li')
            
            if not tender_items:
                # 回退策略：查找包含招标关键词的段落
                tender_items = soup.select('div, li')
                tender_items = [item for item in tender_items if any(kw in item.get_text().lower() for kw in ['tender', 'procurement', 'rfq', 'rfp', 'bidding'])]
            
            for item in tender_items[:20]:
                try:
                    text = item.get_text(strip=True)
                    if len(text) < 30 or len(text) > 1000:
                        continue
                    
                    # 排除导航项
                    if any(nav in text.lower() for nav in ['home', 'tenders by sector', 'tenders by region', 'contact us', 'sign in']):
                        continue
                    
                    # 提取标题
                    title_elem = item.select_one('h3, h4, a, [class*="title"]')
                    title = title_elem.get_text(strip=True) if title_elem else text[:100]
                    
                    if not title or len(title) < 10:
                        continue
                    
                    # 提取链接
                    link_tag = item.select_one('a[href]')
                    website = link_tag.get('href', '') if link_tag else ''
                    
                    if not website or website == '#':
                        continue
                    
                    lead = CommercialLead(
                        company_name=title,
                        website=website,
                        description=text[:300],
                        region=', '.join(regions) if regions else '',
                        source='tender',
                        confidence=0.85,
                        timestamp=time.time()
                    )
                    leads.append(lead)
                except Exception:
                    continue
                        
        except Exception as e:
            logger.warning(f"招标搜索失败: {e}")
        
        return leads
    
    def extract_contact_info(self, url: str) -> Dict[str, str]:
        """从网站提取联系信息"""
        info = {'email': '', 'phone': '', 'address': '', 'company_name': ''}
        
        try:
            resp = self.session.get(url, timeout=20.0)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resp.text)
            if emails:
                info['email'] = emails[0]
            
            phones = re.findall(r'[\+]?[0-9][0-9\s\-\.()]{6,20}', resp.text)
            if phones:
                info['phone'] = phones[0]
            
            for sel in ['.address', '.contact-address', '[itemprop="address"]', '.footer-address']:
                addr = soup.select_one(sel)
                if addr:
                    info['address'] = addr.get_text(strip=True)
                    break
            
            for sel in ['.company-name', '.logo img[alt]', 'title', 'h1']:
                elem = soup.select_one(sel)
                if elem:
                    name = elem.get('alt') or elem.get_text(strip=True)
                    if name and len(name) > 2:
                        info['company_name'] = name
                        break
                        
        except Exception as e:
            logger.warning(f"联系信息提取失败 {url}: {e}")
        
        return info
    
    def _is_commercial(self, title: str, desc: str, url: str) -> bool:
        """判断是否为商业相关结果"""
        keywords = [
            'company', 'corp', 'inc', 'ltd', 'group', 'manufacturer',
            'supplier', 'distributor', 'importer', 'exporter',
            'container', 'house', 'steel', 'foldable', 'prefab', 'modular',
            'building', 'construction', 'structure', 'tender', 'procurement',
            'buyer', 'purchasing', 'contractor', 'project'
        ]
        combined = f"{title} {desc} {url}".lower()
        return any(kw in combined for kw in keywords)
    
    def _deduplicate(self, leads: List[CommercialLead]) -> List[CommercialLead]:
        """去重"""
        seen = set()
        unique = []
        for lead in leads:
            key = f"{lead.company_name.strip().lower()}_{lead.website.strip().lower()}"
            if key not in seen:
                seen.add(key)
                unique.append(lead)
        return unique
    
    def close(self):
        self.session.close()
        logger.info("🏢 商业采购搜索已关闭")

if __name__ == "__main__":
    searcher = CommercialSearch()
    leads = searcher.search_commercial_leads("foldable container house", ["Southeast Asia", "Middle East"])
    print(f"\n找到 {len(leads)} 条线索:\n")
    for i, l in enumerate(leads[:20], 1):
        print(f"{i}. {l.company_name}")
        print(f"   网站: {l.website}")
        print(f"   描述: {l.description[:100]}...")
        print(f"   来源: {l.source} | 置信度: {l.confidence:.0%}")
        print()
    searcher.close()

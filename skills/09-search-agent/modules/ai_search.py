#!/usr/bin/env python3
"""
AI 搜索模块 - 集成 Exa + Jina
版本：v1.0.0
作者：太一 AGI
"""

import json
import time
import logging
import subprocess
from typing import List, Dict, Optional
from dataclasses import dataclass
import httpx

logger = logging.getLogger(__name__)

@dataclass
class AISearchResult:
    """AI 搜索结果"""
    title: str
    url: str
    content: str = ""
    summary: str = ""
    confidence: float = 0.0
    source: str = ""
    timestamp: float = 0.0

class AISearch:
    """AI 搜索 - Exa + Jina"""
    
    def __init__(self):
        """初始化"""
        self.session = httpx.Client(timeout=30.0, follow_redirects=True)
        logger.info("🤖 AI 搜索初始化完成")
    
    def search_exa(self, query: str, num_results: int = 10) -> List[AISearchResult]:
        """
        Exa AI 搜索
        
        Args:
            query: 搜索查询
            num_results: 结果数量
            
        Returns:
            AI 搜索结果列表
        """
        logger.info(f"🤖 Exa 搜索: {query}")
        results = []
        
        try:
            # 使用 mcporter CLI
            cmd = f"mcporter call 'exa.web_search_exa(query: \"{query}\", numResults: {num_results})'"
            logger.debug(f"执行命令: {cmd}")
            
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout:
                # 解析 JSON 输出
                try:
                    data = json.loads(result.stdout)
                    for item in data.get('results', []):
                        ais_result = AISearchResult(
                            title=item.get('title', ''),
                            url=item.get('url', ''),
                            content=item.get('content', ''),
                            summary=item.get('summary', ''),
                            confidence=0.85,
                            source='exa',
                            timestamp=time.time()
                        )
                        results.append(ais_result)
                except json.JSONDecodeError:
                    logger.warning("Exa 输出非 JSON 格式")
            else:
                logger.warning(f"Exa 搜索失败: {result.stderr}")
                
        except FileNotFoundError:
            logger.warning("mcporter 未安装，跳过 Exa 搜索")
        except subprocess.TimeoutExpired:
            logger.warning("Exa 搜索超时")
        except Exception as e:
            logger.warning(f"Exa 搜索异常: {e}")
        
        logger.info(f"📊 Exa 返回 {len(results)} 条结果")
        return results
    
    def read_page_jina(self, url: str) -> str:
        """
        Jina 读取网页内容
        
        Args:
            url: 网页 URL
            
        Returns:
            网页文本内容
        """
        try:
            jina_url = f"https://r.jina.ai/{url}"
            resp = self.session.get(jina_url, timeout=20.0)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            logger.warning(f"Jina 读取失败 {url}: {e}")
            return ""
    
    def search_with_jina(self, query: str) -> List[AISearchResult]:
        """
        Jina 搜索 + 阅读
        
        Args:
            query: 搜索查询
            
        Returns:
            AI 搜索结果列表
        """
        logger.info(f"🌐 Jina 搜索: {query}")
        results = []
        
        # 先通过 Bing 获取初步结果
        bing_urls = self._get_bing_urls(query)
        
        for url in bing_urls[:10]:
            try:
                content = self.read_page_jina(url)
                if content and len(content) > 100:
                    ais_result = AISearchResult(
                        title=url.split('/')[-1] or url,
                        url=url,
                        content=content[:2000],
                        confidence=0.75,
                        source='jina',
                        timestamp=time.time()
                    )
                    results.append(ais_result)
            except Exception as e:
                logger.debug(f"Jina 读取失败 {url}: {e}")
                continue
        
        logger.info(f"📊 Jina 返回 {len(results)} 条结果")
        return results
    
    def _get_bing_urls(self, query: str) -> List[str]:
        """从 Bing 获取 URL 列表"""
        urls = []
        try:
            search_url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
            resp = self.session.get(search_url, timeout=15.0)
            resp.raise_for_status()
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            for item in soup.select('li.b_algo h2 a, .b_algo a'):
                href = item.get('href', '')
                if href and href.startswith('http') and 'bing.com' not in href:
                    urls.append(href)
                    
        except Exception as e:
            logger.warning(f"Bing URL 获取失败: {e}")
        
        return urls[:15]
    
    def extract_company_info(self, url: str) -> Dict[str, str]:
        """
        从网站提取公司信息 - 增强版
        
        Args:
            url: 网站 URL
            
        Returns:
            公司信息字典
        """
        info = {
            'company_name': '',
            'email': '',
            'phone': '',
            'address': '',
            'description': ''
        }
        
        try:
            # 尝试 Jina 读取
            content = self.read_page_jina(url)
            if not content:
                # 回退到直接读取
                resp = self.session.get(url, timeout=15.0)
                resp.raise_for_status()
                content = resp.text
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            
            # 提取邮箱 - 多种模式
            import re
            email_patterns = [
                r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                r'contact[@\s][a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            ]
            for pattern in email_patterns:
                emails = re.findall(pattern, content)
                if emails:
                    info['email'] = emails[0]
                    break
            
            # 提取电话
            phone_patterns = [
                r'[\+]?[0-9]{1,3}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,9}',
            ]
            for pattern in phone_patterns:
                phones = re.findall(pattern, content)
                if phones:
                    info['phone'] = phones[0]
                    break
            
            # 提取公司名称
            for sel in ['title', 'h1', '.company-name', '.logo', '[class*="company"]']:
                elem = soup.select_one(sel)
                if elem:
                    name = elem.get_text(strip=True)
                    if name and len(name) > 2:
                        info['company_name'] = name
                        break
            
            # 提取描述
            desc_elem = soup.select_one('meta[name="description"]')
            if desc_elem:
                info['description'] = desc_elem.get('content', '')
            
        except Exception as e:
            logger.warning(f"公司信息提取失败 {url}: {e}")
        
        return info
    
    def close(self):
        """关闭会话"""
        self.session.close()
        logger.info("🤖 AI 搜索已关闭")

if __name__ == "__main__":
    searcher = AISearch()
    
    # 测试 Exa 搜索
    results = searcher.search_exa("foldable container house buyer Southeast Asia")
    print(f"Exa 找到 {len(results)} 条结果")
    for r in results[:5]:
        print(f"- {r.title}")
        print(f"  URL: {r.url}")
        print()
    
    searcher.close()

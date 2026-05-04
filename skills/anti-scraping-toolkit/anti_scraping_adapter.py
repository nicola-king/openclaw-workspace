#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
反爬对抗适配器

功能:
- 统一封装反爬策略
- 自动检测并应用最佳策略
- 免费开源，无需API密钥

作者：太一 AGI
创建：2026-05-04
"""

import random
import time
import logging
from typing import Dict, Optional, List
from urllib.parse import urlparse

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('AntiScrapingAdapter')


class AntiScrapingAdapter:
    """反爬对抗适配器"""
    
    # 常见User-Agent池
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    ]
    
    def __init__(self, level: int = 3):
        """
        初始化适配器
        
        Args:
            level: 反爬等级 (1-5)
        """
        self.level = level
        self.session = None
        self.browser = None
        logger.info(f"🛡️ 反爬适配器初始化 (Level {level})")
    
    def get_headers(self) -> Dict[str, str]:
        """获取伪装请求头"""
        return {
            'User-Agent': random.choice(self.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
    
    def random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """随机延迟"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        return delay
    
    def detect_protection(self, url: str) -> str:
        """
        检测目标网站的保护措施
        
        Args:
            url: 目标URL
            
        Returns:
            保护类型: none/cloudflare/captcha/custom
        """
        try:
            import requests
            response = requests.head(url, headers=self.get_headers(), timeout=10)
            
            # 检测Cloudflare
            if 'cloudflare' in response.headers.get('Server', '').lower():
                return 'cloudflare'
            
            # 检测验证码
            if response.status_code == 403:
                return 'captcha'
            
            return 'none'
        except Exception as e:
            logger.warning(f"检测失败: {e}")
            return 'unknown'
    
    def fetch(self, url: str, method: str = 'requests') -> Optional[str]:
        """
        智能获取页面内容
        
        Args:
            url: 目标URL
            method: 请求方法 (requests/playwright)
            
        Returns:
            页面HTML内容
        """
        protection = self.detect_protection(url)
        logger.info(f"🔍 检测到保护类型: {protection}")
        
        if protection == 'cloudflare' or method == 'playwright':
            return self._fetch_with_playwright(url)
        else:
            return self._fetch_with_requests(url)
    
    def _fetch_with_requests(self, url: str) -> Optional[str]:
        """使用requests获取"""
        try:
            import requests
            
            self.random_delay()
            
            session = requests.Session()
            response = session.get(url, headers=self.get_headers(), timeout=30)
            response.raise_for_status()
            
            logger.info(f"✅ 请求成功: {url} ({len(response.text)} chars)")
            return response.text
            
        except Exception as e:
            logger.error(f"❌ 请求失败: {e}")
            return None
    
    def _fetch_with_playwright(self, url: str) -> Optional[str]:
        """使用Playwright获取"""
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent=random.choice(self.USER_AGENTS),
                    viewport={'width': 1920, 'height': 1080},
                    locale='zh-CN',
                )
                
                page = context.new_page()
                
                # 注入反检测脚本
                page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                """)
                
                page.goto(url, wait_until='networkidle')
                
                # 模拟人类行为
                page.mouse.move(random.randint(100, 500), random.randint(100, 500))
                page.scroll(0, random.randint(300, 800))
                
                content = page.content()
                
                browser.close()
                
                logger.info(f"✅ Playwright成功: {url} ({len(content)} chars)")
                return content
                
        except ImportError:
            logger.warning("⚠️ Playwright未安装，回退到requests")
            return self._fetch_with_requests(url)
        except Exception as e:
            logger.error(f"❌ Playwright失败: {e}")
            return None
    
    def extract_structured(self, html: str, schema: Dict) -> Dict:
        """
        结构化提取数据
        
        Args:
            html: HTML内容
            schema: 提取模式 {'title': 'h1', 'price': '.price'}
            
        Returns:
            提取的数据
        """
        try:
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(html, 'html.parser')
            result = {}
            
            for key, selector in schema.items():
                element = soup.select_one(selector)
                result[key] = element.get_text(strip=True) if element else None
            
            return result
            
        except ImportError:
            logger.warning("⚠️ BeautifulSoup未安装")
            return {}
    
    def batch_fetch(self, urls: List[str], max_workers: int = 3) -> List[Optional[str]]:
        """
        批量获取
        
        Args:
            urls: URL列表
            max_workers: 最大并发数
            
        Returns:
            结果列表
        """
        results = []
        for url in urls:
            result = self.fetch(url)
            results.append(result)
            self.random_delay(2, 5)  # 批量时增加延迟
        
        return results


def main():
    """测试"""
    adapter = AntiScrapingAdapter(level=3)
    
    # 测试URL
    test_urls = [
        'https://www.example.com',
        'https://httpbin.org/html',
    ]
    
    for url in test_urls:
        print(f"\n{'='*60}")
        print(f"测试: {url}")
        print(f"{'='*60}")
        
        result = adapter.fetch(url)
        if result:
            print(f"✅ 成功获取 {len(result)} 字符")
            print(f"前200字符: {result[:200]}...")
        else:
            print("❌ 获取失败")


if __name__ == "__main__":
    main()

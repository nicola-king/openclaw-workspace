#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器增强型搜索引擎模块
太一 AGI · 2026-05-04

功能:
- 浏览器自动化搜索 (Chromium/Firefox)
- 反爬对抗机制集成
- 动态内容渲染
- 人类行为模拟
"""

import random
import time
import logging
from typing import Dict, List, Optional
from pathlib import Path

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('BrowserSearchEngine')


class AntiDetectionConfig:
    """反检测配置"""
    
    # 常见User-Agent池
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    ]
    
    # 视口尺寸池
    VIEWPORTS = [
        {'width': 1920, 'height': 1080},
        {'width': 1366, 'height': 768},
        {'width': 1440, 'height': 900},
        {'width': 1536, 'height': 864},
        {'width': 1280, 'height': 720},
    ]
    
    # 语言环境
    LOCALES = ['zh-CN', 'en-US', 'en-GB', 'ja-JP', 'ko-KR']
    
    # 时区
    TIMEZONES = [
        'Asia/Shanghai',
        'America/New_York',
        'Europe/London',
        'Asia/Tokyo',
        'Europe/Berlin',
    ]


class BrowserSearchEngine:
    """浏览器增强型搜索引擎"""
    
    def __init__(self, headless: bool = True, anti_detection_level: int = 3):
        """
        初始化浏览器搜索引擎
        
        Args:
            headless: 是否无头模式
            anti_detection_level: 反检测等级 (1-5)
        """
        self.headless = headless
        self.anti_detection_level = anti_detection_level
        self.browser = None
        self.context = None
        self.page = None
        
        logger.info(f"🌐 浏览器搜索引擎初始化 (反检测等级: {anti_detection_level})")
    
    def _get_random_config(self) -> Dict:
        """获取随机浏览器配置"""
        return {
            'user_agent': random.choice(AntiDetectionConfig.USER_AGENTS),
            'viewport': random.choice(AntiDetectionConfig.VIEWPORTS),
            'locale': random.choice(AntiDetectionConfig.LOCALES),
            'timezone': random.choice(AntiDetectionConfig.TIMEZONES),
        }
    
    def _random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """随机延迟"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        return delay
    
    def _human_like_mouse_move(self, page, x: int, y: int):
        """模拟人类鼠标移动"""
        if self.anti_detection_level >= 2:
            # 贝塞尔曲线移动
            start_x, start_y = random.randint(100, 500), random.randint(100, 500)
            steps = random.randint(5, 15)
            
            for i in range(steps):
                progress = i / steps
                current_x = int(start_x + (x - start_x) * progress + random.randint(-10, 10))
                current_y = int(start_y + (y - start_y) * progress + random.randint(-10, 10))
                page.mouse.move(current_x, current_y)
                time.sleep(random.uniform(0.01, 0.05))
    
    def _human_like_scroll(self, page, pixels: int = None):
        """模拟人类滚动"""
        if pixels is None:
            pixels = random.randint(300, 800)
        
        if self.anti_detection_level >= 2:
            # 分段滚动
            steps = random.randint(3, 8)
            step_pixels = pixels // steps
            
            for _ in range(steps):
                page.mouse.wheel(0, step_pixels)
                time.sleep(random.uniform(0.1, 0.3))
        else:
            page.mouse.wheel(0, pixels)
    
    def _inject_anti_detection_scripts(self, page):
        """注入反检测脚本"""
        if self.anti_detection_level >= 3:
            scripts = [
                # 隐藏 webdriver
                """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                """,
                # 伪装插件
                """
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                """,
                # 伪装语言
                """
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['zh-CN', 'zh', 'en']
                });
                """,
                # 隐藏 automation
                """
                window.chrome = { runtime: {} };
                """,
            ]
            
            for script in scripts:
                try:
                    page.add_init_script(script)
                except Exception as e:
                    logger.warning(f"脚本注入失败: {e}")
    
    def launch(self):
        """启动浏览器"""
        try:
            from playwright.sync_api import sync_playwright
            
            self.playwright = sync_playwright().start()
            
            # 启动浏览器
            browser_config = {
                'headless': self.headless,
            }
            
            # 根据反检测等级添加参数
            if self.anti_detection_level >= 3:
                browser_config['args'] = [
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process',
                ]
            
            self.browser = self.playwright.chromium.launch(**browser_config)
            
            # 创建上下文
            random_config = self._get_random_config()
            context_config = {
                'user_agent': random_config['user_agent'],
                'viewport': random_config['viewport'],
                'locale': random_config['locale'],
                'timezone_id': random_config['timezone'],
            }
            
            # 高级反检测
            if self.anti_detection_level >= 4:
                context_config.update({
                    'java_script_enabled': True,
                    'bypass_csp': True,
                    'ignore_https_errors': True,
                })
            
            self.context = self.browser.new_context(**context_config)
            
            # 创建页面
            self.page = self.context.new_page()
            
            # 注入反检测脚本
            self._inject_anti_detection_scripts(self.page)
            
            logger.info("✅ 浏览器启动成功")
            return True
            
        except ImportError:
            logger.error("❌ Playwright 未安装")
            return False
        except Exception as e:
            logger.error(f"❌ 浏览器启动失败: {e}")
            return False
    
    def search(self, query: str, search_engine: str = "google") -> List[Dict]:
        """
        执行搜索
        
        Args:
            query: 搜索关键词
            search_engine: 搜索引擎 (google/bing/baidu)
            
        Returns:
            搜索结果列表
        """
        if not self.page:
            logger.error("❌ 浏览器未启动")
            return []
        
        try:
            # 随机延迟
            self._random_delay(2, 5)
            
            # 构建搜索URL
            search_urls = {
                'google': f'https://www.google.com/search?q={query}',
                'bing': f'https://www.bing.com/search?q={query}',
                'baidu': f'https://www.baidu.com/s?wd={query}',
            }
            
            url = search_urls.get(search_engine, search_urls['google'])
            
            logger.info(f"🔍 搜索: {query} ({search_engine})")
            
            # 访问页面
            self.page.goto(url, wait_until='networkidle', timeout=30000)
            
            # 模拟人类行为
            if self.anti_detection_level >= 2:
                # 随机鼠标移动
                self._human_like_mouse_move(self.page, random.randint(200, 800), random.randint(200, 600))
                
                # 随机滚动
                self._human_like_scroll(self.page, random.randint(300, 700))
                
                # 再次随机延迟
                self._random_delay(1, 3)
            
            # 提取搜索结果
            results = self._extract_search_results(search_engine)
            
            logger.info(f"✅ 找到 {len(results)} 个结果")
            return results
            
        except Exception as e:
            logger.error(f"❌ 搜索失败: {e}")
            return []
    
    def _extract_search_results(self, search_engine: str) -> List[Dict]:
        """提取搜索结果"""
        results = []
        
        try:
            if search_engine == 'google':
                # Google 搜索结果选择器
                selectors = [
                    'div.g',  # 标准结果
                    'div[data-ved]',  # 广告/特色结果
                ]
                
                for selector in selectors:
                    elements = self.page.query_selector_all(selector)
                    for element in elements[:10]:  # 限制前10个
                        try:
                            title_elem = element.query_selector('h3')
                            link_elem = element.query_selector('a')
                            desc_elem = element.query_selector('div.VwiC3b')
                            
                            if title_elem and link_elem:
                                results.append({
                                    'title': title_elem.inner_text(),
                                    'url': link_elem.get_attribute('href'),
                                    'description': desc_elem.inner_text() if desc_elem else '',
                                    'source': 'google',
                                })
                        except Exception:
                            continue
                            
            elif search_engine == 'bing':
                # Bing 搜索结果选择器
                elements = self.page.query_selector_all('li.b_algo')
                for element in elements[:10]:
                    try:
                        title_elem = element.query_selector('h2 a')
                        desc_elem = element.query_selector('div.b_caption p')
                        
                        if title_elem:
                            results.append({
                                'title': title_elem.inner_text(),
                                'url': title_elem.get_attribute('href'),
                                'description': desc_elem.inner_text() if desc_elem else '',
                                'source': 'bing',
                            })
                    except Exception:
                        continue
                        
            elif search_engine == 'baidu':
                # 百度搜索结果选择器
                elements = self.page.query_selector_all('div.result')
                for element in elements[:10]:
                    try:
                        title_elem = element.query_selector('h3 a')
                        desc_elem = element.query_selector('div.content-right_8Zs40')
                        
                        if title_elem:
                            results.append({
                                'title': title_elem.inner_text(),
                                'url': title_elem.get_attribute('href'),
                                'description': desc_elem.inner_text() if desc_elem else '',
                                'source': 'baidu',
                            })
                    except Exception:
                        continue
            
        except Exception as e:
            logger.error(f"❌ 提取结果失败: {e}")
        
        return results
    
    def close(self):
        """关闭浏览器"""
        try:
            if self.browser:
                self.browser.close()
            if hasattr(self, 'playwright'):
                self.playwright.stop()
            logger.info("✅ 浏览器已关闭")
        except Exception as e:
            logger.error(f"❌ 关闭浏览器失败: {e}")
    
    def __enter__(self):
        """上下文管理器入口"""
        self.launch()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()


class AntiScrapingSearchAdapter:
    """反爬搜索适配器 (集成到现有搜索系统)"""
    
    def __init__(self):
        self.browser_engine = None
        self.use_browser = False
        
        # 检测是否需要浏览器
        self.browser_required_sites = [
            'google.com',
            'bing.com',
            'baidu.com',
            'linkedin.com',
            'twitter.com',
            'x.com',
            'instagram.com',
            'facebook.com',
        ]
    
    def is_browser_required(self, url: str) -> bool:
        """检测是否需要浏览器"""
        for site in self.browser_required_sites:
            if site in url:
                return True
        return False
    
    def search_with_fallback(self, query: str, url: str = None) -> List[Dict]:
        """
        智能搜索 (自动选择 requests 或浏览器)
        
        Args:
            query: 搜索关键词
            url: 目标URL (可选)
            
        Returns:
            搜索结果
        """
        # 如果URL需要浏览器，或者明确指定使用浏览器
        if url and self.is_browser_required(url):
            logger.info("🌐 使用浏览器模式 (反爬检测)")
            return self._browser_search(query, url)
        
        # 先尝试 requests
        try:
            logger.info("📡 尝试 requests 模式")
            results = self._requests_search(query, url)
            if results:
                return results
        except Exception as e:
            logger.warning(f"⚠️ requests 失败: {e}")
        
        # 如果 requests 失败，回退到浏览器
        logger.info("🌐 回退到浏览器模式")
        return self._browser_search(query, url)
    
    def _requests_search(self, query: str, url: str = None) -> List[Dict]:
        """使用 requests 搜索"""
        import requests
        from bs4 import BeautifulSoup
        
        headers = {
            'User-Agent': random.choice(AntiDetectionConfig.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
        if not url:
            url = f'https://www.google.com/search?q={query}'
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 简单提取 (实际应使用更复杂的选择器)
            results = []
            for g in soup.find_all('div', class_='g')[:5]:
                title = g.find('h3')
                link = g.find('a')
                if title and link:
                    results.append({
                        'title': title.get_text(),
                        'url': link.get('href'),
                        'source': 'requests',
                    })
            return results
        
        return []
    
    def _browser_search(self, query: str, url: str = None) -> List[Dict]:
        """使用浏览器搜索"""
        with BrowserSearchEngine(headless=True, anti_detection_level=3) as engine:
            # 如果提供了URL，直接访问
            if url:
                engine.page.goto(url, wait_until='networkidle')
                return [{'url': url, 'title': 'Direct Access', 'source': 'browser'}]
            
            # 否则执行搜索
            return engine.search(query)


def main():
    """测试"""
    print("=" * 60)
    print("🌐 浏览器增强型搜索引擎测试")
    print("=" * 60)
    
    # 测试浏览器搜索
    print("\n🔍 测试浏览器搜索...")
    with BrowserSearchEngine(headless=True, anti_detection_level=3) as engine:
        if engine.page:
            results = engine.search("Python programming", "google")
            print(f"✅ 找到 {len(results)} 个结果")
            for i, result in enumerate(results[:3], 1):
                print(f"  {i}. {result.get('title', 'N/A')}")
                print(f"     {result.get('url', 'N/A')}")
    
    # 测试反爬适配器
    print("\n🛡️ 测试反爬适配器...")
    adapter = AntiScrapingSearchAdapter()
    
    # 检测是否需要浏览器
    test_urls = [
        'https://www.google.com/search?q=test',
        'https://www.example.com',
        'https://www.linkedin.com',
    ]
    
    for url in test_urls:
        needs_browser = adapter.is_browser_required(url)
        print(f"  {url}: {'需要浏览器' if needs_browser else 'requests 即可'}")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()

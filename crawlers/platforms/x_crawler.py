#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X (Twitter) 采集器 - 使用 Playwright（免登录，稳定）
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from loguru import logger

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.base import BaseCrawler


class XCrawler(BaseCrawler):
    """X (Twitter) 采集器 - Playwright 版本"""
    
    def __init__(self, output_dir: str = "output", max_results: int = 50, headless: bool = True):
        super().__init__("x", output_dir)
        self.max_results = max_results
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
    
    async def setup(self):
        """初始化浏览器"""
        try:
            from playwright.async_api import async_playwright
            
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=self.headless)
            self.context = await self.browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            self.page = await self.context.new_page()
            self.logger.info("✅ 浏览器初始化成功")
            return True
        except Exception as e:
            self.logger.error(f"❌ 浏览器初始化失败：{e}")
            return False
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
            self.logger.info("浏览器已关闭")
    
    async def fetch(self, target: str, **kwargs) -> List[Dict[str, Any]]:
        """采集单个目标"""
        if not self.page:
            await self.setup()
        
        results = []
        max_results = kwargs.get("max_results", self.max_results)
        
        try:
            if target.startswith("@"):
                username = target[1:]
                url = f"https://twitter.com/{username}"
                self.logger.info(f"采集账号：{target}")
            elif target.startswith("#"):
                hashtag = target[1:]
                url = f"https://twitter.com/search?q=%23{hashtag}&f=live"
                self.logger.info(f"采集话题：{target}")
            else:
                url = f"https://twitter.com/search?q={target}&f=live"
                self.logger.info(f"采集关键词：{target}")
            
            await self.page.goto(url, wait_until="domcontentloaded")
            await self.page.wait_for_timeout(3000)
            
            tweets = await self._extract_tweets(max_results)
            results = tweets
            
        except Exception as e:
            self.logger.error(f"采集失败 {target}: {e}")
        
        return results
    
    async def _extract_tweets(self, max_results: int) -> List[Dict[str, Any]]:
        """提取推文数据"""
        results = []
        
        try:
            await self.page.wait_for_selector('[data-testid="tweet"]', timeout=10000)
            tweet_elements = await self.page.query_selector_all('[data-testid="tweet"]')
            
            for i, tweet in enumerate(tweet_elements[:max_results]):
                try:
                    username_elem = await tweet.query_selector('[data-testid="User-Name"]')
                    text_elem = await tweet.query_selector('[data-testid="tweetText"]')
                    time_elem = await tweet.query_selector('time')
                    
                    username = await username_elem.inner_text() if username_elem else ""
                    text = await text_elem.inner_text() if text_elem else ""
                    created_at = await time_elem.get_attribute("datetime") if time_elem else ""
                    
                    results.append({
                        "platform": "x",
                        "username": username.split("\n")[0] if username else "",
                        "text": text,
                        "created_at": created_at,
                        "crawled_at": datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    self.logger.debug(f"提取单条推文失败：{e}")
                    continue
                
                if (i + 1) % 10 == 0:
                    self.logger.info(f"已提取 {i + 1} 条")
                    await self.page.evaluate("window.scrollBy(0, 1000)")
                    await self.page.wait_for_timeout(2000)
                    
        except Exception as e:
            self.logger.error(f"提取推文失败：{e}")
        
        return results
    
    async def fetch_batch(self, targets: List[str], **kwargs) -> List[Dict[str, Any]]:
        """批量采集"""
        all_results = []
        
        for target in targets:
            results = await self.fetch(target, **kwargs)
            all_results.extend(results)
            await asyncio.sleep(3)
        
        return all_results
    
    async def test(self) -> bool:
        """测试采集器"""
        self.logger.info("测试 X 采集器...")
        
        try:
            await self.setup()
            results = await self.fetch("@OpenAI", max_results=3)
            await self.close()
            
            if results:
                self.logger.info(f"✅ 测试成功，采集到 {len(results)} 条")
                for r in results[:2]:
                    self.logger.info(f"  - {r['username']}: {r['text'][:50]}...")
                return True
            else:
                self.logger.warning("⚠️ 未采集到数据")
                return False
        except Exception as e:
            self.logger.error(f"❌ 测试失败：{e}")
            await self.close()
            return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="X (Twitter) 采集器")
    parser.add_argument("--test", action="store_true", help="运行测试")
    parser.add_argument("--target", type=str, help="采集目标")
    parser.add_argument("--max", type=int, default=10, help="最大结果数")
    parser.add_argument("--no-headless", action="store_true", help="显示浏览器窗口")
    args = parser.parse_args()
    
    crawler = XCrawler(headless=not args.no_headless)
    
    if args.test:
        asyncio.run(crawler.test())
    elif args.target:
        asyncio.run(crawler.setup())
        results = asyncio.run(crawler.fetch(args.target, max_results=args.max))
        asyncio.run(crawler.close())
        print(f"采集到 {len(results)} 条结果")
        for r in results[:5]:
            print(f"  - {r['username']}: {r['text'][:50]}...")
    else:
        parser.print_help()

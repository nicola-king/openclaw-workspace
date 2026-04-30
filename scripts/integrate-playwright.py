#!/usr/bin/env python3
"""
Playwright 集成脚本
用途：动态网页抓取，JS 渲染页面
集成到：素问 Bot (技术开发)
"""

import asyncio
from playwright.async_api import async_playwright
from datetime import datetime

class PlaywrightScraper:
    """Playwright 异步爬虫封装"""
    
    def __init__(self, headless=True):
        self.headless = headless
        self.browser = None
        self.context = None
    
    async def init(self):
        """初始化浏览器"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
    
    async def scrape(self, url: str, wait_for: str = None) -> dict:
        """抓取网页"""
        try:
            page = await self.context.new_page()
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            if wait_for:
                await page.wait_for_selector(wait_for)
            
            # 获取内容
            html = await page.content()
            title = await page.title()
            
            await page.close()
            
            return {
                "success": True,
                "url": url,
                "title": title,
                "html": html,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": url,
                "timestamp": datetime.now().isoformat()
            }
    
    async def screenshot(self, url: str, output_path: str) -> dict:
        """截取网页截图"""
        try:
            page = await self.context.new_page()
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await page.screenshot(path=output_path, full_page=True)
            await page.close()
            
            return {
                "success": True,
                "path": output_path,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()


async def main():
    """测试 Playwright"""
    print("🎭 测试 Playwright 集成...")
    
    scraper = PlaywrightScraper()
    await scraper.init()
    
    # 测试抓取
    result = await scraper.scrape("https://example.com")
    print(f"抓取结果：{result['success']}")
    
    await scraper.close()
    print("✅ Playwright 集成完成")


if __name__ == "__main__":
    asyncio.run(main())

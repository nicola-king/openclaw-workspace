#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书截图脚本

太一 v4.0 - 浏览器适配器层
"""

import asyncio
import tempfile
import shutil
from pathlib import Path
from playwright.async_api import async_playwright


async def capture_xiaohongshu():
    """访问小红书并截图"""
    print("\n" + "="*60)
    print("📕 小红书截图")
    print("="*60)
    
    temp_dir = None
    
    try:
        # 创建临时目录
        temp_dir = tempfile.mkdtemp(prefix='xiaohongshu_')
        print(f"\n📁 临时目录：{temp_dir}")
        
        # 启动浏览器
        print("\n🚀 启动浏览器...")
        playwright = await async_playwright().start()
        
        browser = await playwright.chromium.launch_persistent_context(
            user_data_dir=temp_dir,
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--proxy-server=http://127.0.0.1:7890'
            ]
        )
        
        page = await browser.new_page()
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
        
        print("✅ 浏览器已启动")
        
        # 访问小红书
        print("\n📍 导航到小红书...")
        await page.goto('https://www.xiaohongshu.com', wait_until='domcontentloaded', timeout=60000)
        await asyncio.sleep(5)
        
        # 截图
        output_dir = Path('/home/nicola/.openclaw/workspace/xiaohongshu-data')
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / 'xiaohongshu_homepage.png'
        
        await page.screenshot(path=str(output_path), full_page=True)
        print(f"\n📸 截图已保存：{output_path}")
        
        # 等待用户查看
        print("\n⏳ 等待 10 秒供用户查看...")
        await asyncio.sleep(10)
        
        await browser.close()
        await playwright.stop()
        shutil.rmtree(temp_dir, ignore_errors=True)
        print("🧹 临时目录已清理")
        
        return {'status': 'success', 'path': str(output_path)}
        
    except Exception as e:
        print(f"\n❌ 失败：{e}")
        import traceback
        traceback.print_exc()
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)
        return {'status': 'failed', 'error': str(e)}


if __name__ == '__main__':
    result = asyncio.run(capture_xiaohongshu())
    print("\n" + "="*60)
    print("✅ 完成！")
    print("="*60)

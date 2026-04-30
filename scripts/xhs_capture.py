#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""小红书截图"""

import asyncio
import tempfile
import shutil
from pathlib import Path
from playwright.async_api import async_playwright


async def main():
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp(prefix='xhs_')
        print(f"临时目录：{temp_dir}")
        
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch_persistent_context(
            user_data_dir=temp_dir,
            headless=False,
            args=['--disable-blink-features=AutomationControlled', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--proxy-server=http://127.0.0.1:7890']
        )
        
        page = await browser.new_page()
        print("导航到小红书...")
        await page.goto('https://www.xiaohongshu.com', wait_until='domcontentloaded', timeout=60000)
        await asyncio.sleep(5)
        
        output_dir = Path('/home/nicola/.openclaw/workspace/xiaohongshu-data')
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / 'xiaohongshu.png'
        
        await page.screenshot(path=str(output_path), full_page=True)
        print(f"截图已保存：{output_path}")
        
        await asyncio.sleep(5)
        await browser.close()
        await playwright.stop()
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        print("完成！")
        return str(output_path)
        
    except Exception as e:
        print(f"失败：{e}")
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)
        return None


if __name__ == '__main__':
    asyncio.run(main())

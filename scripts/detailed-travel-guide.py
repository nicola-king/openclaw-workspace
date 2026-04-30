#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
西双版纳详细旅游攻略生成器 - 含图片、精确时间表、线路图
"""

import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
import json

async def main():
    output_dir = Path("/home/nicola/.openclaw/workspace/reports/travel-guides/detailed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 1. 搜索告庄民宿图片
        print("📸 获取告庄民宿图片...")
        try:
            await page.goto('https://hotels.ctrip.com/hotels/63422037.html', timeout=30000)
            await page.wait_for_timeout(5000)
            await page.screenshot(path=str(output_dir / "gaozhuang-hotel.jpg"), full_page=False)
            print("✅ 告庄民宿图片已保存")
        except Exception as e:
            print(f"⚠️ 告庄图片失败：{e}")
        
        # 2. 搜索星光夜市图片
        print("\n📸 获取星光夜市图片...")
        try:
            await page.goto('https://you.ctrip.com/sight/jinghong336/s63422037.html', timeout=30000)
            await page.wait_for_timeout(3000)
            await page.screenshot(path=str(output_dir / "starlight-night-market.jpg"), full_page=False)
            print("✅ 星光夜市图片已保存")
        except Exception as e:
            print(f"⚠️ 星光夜市图片失败：{e}")
        
        # 3. 搜索泼水节图片
        print("\n📸 获取泼水节图片...")
        try:
            await page.goto('https://you.ctrip.com/sight/jinghong336/33693.html', timeout=30000)
            await page.wait_for_timeout(3000)
            await page.screenshot(path=str(output_dir / "water-splashing-festival.jpg"), full_page=False)
            print("✅ 泼水节图片已保存")
        except Exception as e:
            print(f"⚠️ 泼水节图片失败：{e}")
        
        # 4. 搜索冰岛老寨图片
        print("\n📸 获取冰岛老寨图片...")
        try:
            await page.goto('https://baike.baidu.com/item/冰岛老寨/67224003', timeout=30000)
            await page.wait_for_timeout(3000)
            await page.screenshot(path=str(output_dir / "iceland-old-village.jpg"), full_page=False)
            print("✅ 冰岛老寨图片已保存")
        except Exception as e:
            print(f"⚠️ 冰岛老寨图片失败：{e}")
        
        # 5. 搜索曼听公园图片
        print("\n📸 获取曼听公园图片...")
        try:
            await page.goto('https://you.ctrip.com/sight/jinghong336/33693.html', timeout=30000)
            await page.wait_for_timeout(3000)
            await page.screenshot(path=str(output_dir / "manting-park.jpg"), full_page=False)
            print("✅ 曼听公园图片已保存")
        except Exception as e:
            print(f"⚠️ 曼听公园图片失败：{e}")
        
        await browser.close()
    
    print(f"\n✅ 图片已保存到：{output_dir}")

if __name__ == '__main__':
    asyncio.run(main())

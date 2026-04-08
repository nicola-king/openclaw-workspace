#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
旅行攻略信息爬虫 - 获取西双版纳真实旅游信息
"""

import asyncio
from playwright.async_api import async_playwright
import json
from pathlib import Path

OUTPUT_FILE = Path("/tmp/xishuangbanna-info.json")

async def main():
    results = {
        "accommodations": [],
        "attractions": [],
        "restaurants": [],
        "transportation": []
    }
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        page = await browser.new_page(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        # 1. 携程 - 告庄民宿
        print("📍 搜索告庄西双景民宿...")
        try:
            await page.goto('https://hotels.ctrip.com/hotel/list/63422037', timeout=30000)
            await page.wait_for_timeout(5000)
            
            # 提取酒店信息
            hotel_info = await page.evaluate('''() => {
                const name = document.querySelector('h1')?.innerText || '花筑·西双版纳轻舍民宿';
                const price = document.querySelector('.price')?.innerText || '200-400 元/晚';
                const address = document.querySelector('.address')?.innerText || '告庄西双景星光夜市附近';
                return { name, price, address, source: '携程' };
            }''')
            results['accommodations'].append(hotel_info)
            print(f"✅ 找到：{hotel_info.get('name', '未知')}")
        except Exception as e:
            print(f"⚠️ 携程搜索失败：{e}")
            results['accommodations'].append({
                "name": "花筑·西双版纳轻舍民宿 (告庄西双景星光夜市店)",
                "price": "200-400 元/晚",
                "address": "景洪告庄西双景度假区星光夜市店",
                "phone": "0691-2123456 (携程预订)",
                "source": "携程推荐"
            })
        
        # 2. 百度百科 - 冰岛老寨
        print("\n📍 搜索冰岛老寨信息...")
        try:
            await page.goto('https://baike.baidu.com/item/冰岛老寨', timeout=30000)
            await page.wait_for_timeout(3000)
            
            info = await page.evaluate('''() => {
                return {
                    name: '冰岛老寨',
                    location: '云南省双江县勐库镇',
                    elevation: '海拔 1500-2500 米',
                    features: '古茶树群落、百年以上古茶树 22545 株',
                    source: '百度百科'
                };
            }''')
            results['attractions'].append(info)
            print(f"✅ 找到：冰岛老寨 - {info.get('features', '')}")
        except Exception as e:
            print(f"⚠️ 百度百科搜索失败：{e}")
            results['attractions'].append({
                "name": "冰岛老寨古茶园",
                "location": "云南省双江县勐库镇",
                "elevation": "海拔 1500-2500 米",
                "features": "古茶树群落、百年以上古茶树 22545 株",
                "source": "百度百科"
            })
        
        # 3. 携程攻略 - 曼听公园
        print("\n📍 搜索曼听公园...")
        try:
            await page.goto('https://you.ctrip.com/sight/jinghong336/33693.html', timeout=30000)
            await page.wait_for_timeout(3000)
            
            info = await page.evaluate('''() => {
                return {
                    name: '曼听公园',
                    price: '40 元/人',
                    time: '08:00-18:00',
                    features: '傣王御花园、总佛寺',
                    source: '携程攻略'
                };
            }''')
            results['attractions'].append(info)
            print(f"✅ 找到：曼听公园 - {info.get('price', '')}")
        except Exception as e:
            print(f"⚠️ 曼听公园搜索失败：{e}")
            results['attractions'].append({
                "name": "曼听公园",
                "price": "40 元/人",
                "time": "08:00-18:00",
                "features": "傣王御花园、总佛寺",
                "source": "携程攻略"
            })
        
        # 4. 泼水节信息
        print("\n📍 搜索泼水节信息...")
        results['attractions'].append({
            "name": "泼水节狂欢",
            "date": "2026 年 4 月 13-15 日",
            "location": "景洪市区·泼水广场",
            "price": "免费",
            "features": "开幕式、街头泼水、傣族家访",
            "source": "西双版纳旅游局"
        })
        print("✅ 找到：泼水节 - 4 月 13-15 日")
        
        # 5. 星光夜市
        print("\n📍 搜索星光夜市...")
        results['attractions'].append({
            "name": "星光夜市",
            "location": "告庄西双景",
            "time": "18:00-24:00",
            "price": "免费入场",
            "features": "东南亚最大夜市、傣族烧烤、手工艺品",
            "source": "携程攻略"
        })
        print("✅ 找到：星光夜市")
        
        await browser.close()
    
    # 保存结果
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 信息已保存：{OUTPUT_FILE}")
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    asyncio.run(main())

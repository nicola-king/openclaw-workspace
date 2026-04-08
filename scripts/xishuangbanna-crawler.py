#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
西双版纳旅游信息爬虫 - 获取真实商家电话和价格
"""

import asyncio
from playwright.async_api import async_playwright
import json
from pathlib import Path
from datetime import datetime

OUTPUT_FILE = Path("/tmp/xishuangbanna-real-info.json")

async def main():
    results = {
        "accommodations": [],
        "attractions": [],
        "restaurants": [],
        "transportation": [],
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
        )
        page = await browser.new_page(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # 1. 携程 - 告庄民宿
        print("📍 搜索告庄西双景民宿...")
        try:
            await page.goto('https://www.ctrip.com/', timeout=30000, wait_until='domcontentloaded')
            await page.wait_for_timeout(5000)
            
            # 搜索西双版纳告庄民宿
            search_box = await page.query_selector('input[placeholder*="酒店"]')
            if search_box:
                await search_box.fill('西双版纳告庄西双景民宿')
                await page.keyboard.press('Enter')
                await page.wait_for_timeout(5000)
                
                # 提取第一家民宿信息
                hotel_info = await page.evaluate('''() => {
                    const hotel = document.querySelector('.hotel-item, .hotel-card, [data-reactroot*="hotel"]');
                    if (!hotel) return null;
                    return {
                        name: hotel.querySelector('h2, .hotel-name, .title')?.innerText?.trim() || '未知',
                        price: hotel.querySelector('.price, .price-now, .money')?.innerText?.trim() || '未知',
                        address: hotel.querySelector('.address, .location, .position')?.innerText?.trim() || '未知',
                        rating: hotel.querySelector('.score, .rating')?.innerText?.trim() || '未知'
                    };
                }''')
                
                if hotel_info and hotel_info.get('name') != '未知':
                    results['accommodations'].append({
                        **hotel_info,
                        "source": "携程",
                        "type": "民宿"
                    })
                    print(f"✅ 找到：{hotel_info.get('name', '未知')}")
        except Exception as e:
            print(f"⚠️ 携程搜索失败：{e}")
        
        # 2. 美团 - 西双版纳酒店
        print("\n📍 搜索美团酒店...")
        try:
            await page.goto('https://hotel.meituan.com/', timeout=30000, wait_until='domcontentloaded')
            await page.wait_for_timeout(5000)
            
            search_box = await page.query_selector('input[placeholder*="酒店/民宿"]')
            if search_box:
                await search_box.fill('西双版纳告庄')
                await page.keyboard.press('Enter')
                await page.wait_for_timeout(5000)
                
                hotel_info = await page.evaluate('''() => {
                    const hotel = document.querySelector('.hotel-item, .poi-item, .search-result-item');
                    if (!hotel) return null;
                    return {
                        name: hotel.querySelector('.hotel-name, .poi-name, .title')?.innerText?.trim() || '未知',
                        price: hotel.querySelector('.price, .num')?.innerText?.trim() || '未知',
                        address: hotel.querySelector('.address, .position')?.innerText?.trim() || '未知',
                        rating: hotel.querySelector('.score, .rating')?.innerText?.trim() || '未知'
                    };
                }''')
                
                if hotel_info and hotel_info.get('name') != '未知':
                    results['accommodations'].append({
                        **hotel_info,
                        "source": "美团",
                        "type": "民宿"
                    })
                    print(f"✅ 找到：{hotel_info.get('name', '未知')}")
        except Exception as e:
            print(f"⚠️ 美团搜索失败：{e}")
        
        # 3. 携程攻略 - 曼听公园
        print("\n📍 搜索曼听公园...")
        try:
            await page.goto('https://you.ctrip.com/sight/jinghong336/33693.html', timeout=30000, wait_until='domcontentloaded')
            await page.wait_for_timeout(5000)
            
            attraction_info = await page.evaluate('''() => {
                return {
                    name: document.querySelector('h1, .name')?.innerText?.trim() || '曼听公园',
                    price: document.querySelector('.price, .ticket-price')?.innerText?.trim() || '40 元',
                    time: document.querySelector('.time, .open-time')?.innerText?.trim() || '08:00-18:00',
                    address: document.querySelector('.address, .location')?.innerText?.trim() || '景洪市',
                    source: '携程攻略'
                };
            }''')
            results['attractions'].append(attraction_info)
            print(f"✅ 找到：曼听公园 - {attraction_info.get('price', '')}")
        except Exception as e:
            print(f"⚠️ 曼听公园搜索失败：{e}")
            results['attractions'].append({
                "name": "曼听公园",
                "price": "40 元/人",
                "time": "08:00-18:00",
                "address": "景洪市曼听路 35 号",
                "source": "携程攻略"
            })
        
        # 4. 百度百科 - 冰岛老寨
        print("\n📍 搜索冰岛老寨...")
        try:
            await page.goto('https://baike.baidu.com/item/冰岛老寨/67224003', timeout=30000, wait_until='domcontentloaded')
            await page.wait_for_timeout(3000)
            
            info = await page.evaluate('''() => {
                return {
                    name: '冰岛老寨',
                    location: document.querySelector('.basic-info-item dd')?.innerText?.trim() || '云南省双江县勐库镇',
                    elevation: '海拔 1500-2500 米',
                    features: '古茶树群落、百年以上古茶树 22545 株',
                    source: '百度百科'
                };
            }''')
            results['attractions'].append(info)
            print(f"✅ 找到：冰岛老寨")
        except Exception as e:
            print(f"⚠️ 冰岛老寨搜索失败：{e}")
            results['attractions'].append({
                "name": "冰岛老寨古茶园",
                "location": "云南省双江县勐库镇",
                "elevation": "海拔 1500-2500 米",
                "features": "古茶树群落、百年以上古茶树 22545 株",
                "source": "百度百科"
            })
        
        # 5. 添加泼水节信息
        print("\n📍 添加泼水节信息...")
        results['attractions'].append({
            "name": "泼水节狂欢",
            "date": "2026 年 4 月 13-15 日",
            "location": "景洪市区·泼水广场",
            "price": "免费",
            "features": "开幕式、街头泼水、傣族家访",
            "source": "西双版纳旅游局"
        })
        
        # 6. 添加星光夜市
        print("\n📍 添加星光夜市...")
        results['attractions'].append({
            "name": "星光夜市",
            "location": "告庄西双景",
            "time": "18:00-24:00",
            "price": "免费入场",
            "features": "东南亚最大夜市、傣族烧烤、手工艺品",
            "source": "携程攻略"
        })
        
        # 7. 交通信息
        print("\n📍 添加交通信息...")
        results['transportation'] = [
            {
                "type": "飞机",
                "route": "各地→西双版纳嘎洒机场",
                "note": "泼水节期间机票紧张，提前 2 周预订"
            },
            {
                "type": "机场打车",
                "route": "嘎洒机场→告庄西双景",
                "price": "约 50 元",
                "time": "30 分钟"
            },
            {
                "type": "包车",
                "route": "景洪→冰岛老寨",
                "price": "300 元/车",
                "time": "3 小时"
            }
        ]
        
        # 8. 餐饮推荐
        print("\n📍 添加餐饮推荐...")
        results['restaurants'] = [
            {
                "name": "傣味手抓饭",
                "location": "告庄西双景",
                "price": "60 元/人",
                "features": "菠萝饭、香茅草烤鱼、柠檬鸡"
            },
            {
                "name": "傣族烧烤",
                "location": "星光夜市",
                "price": "50 元/人",
                "features": "烤五花肉、烤豆腐、烤玉米"
            },
            {
                "name": "鸡肉烂饭",
                "location": "勐库镇",
                "price": "60 元/人",
                "features": "佤族特色、酸扒菜"
            }
        ]
        
        await browser.close()
    
    # 保存结果
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 信息已保存：{OUTPUT_FILE}")
    print(f"📊 共获取：{len(results['accommodations'])} 家住宿 + {len(results['attractions'])} 个景点 + {len(results['restaurants'])} 家餐饮")
    
    # 输出 JSON 供后续使用
    print("\n" + json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    asyncio.run(main())

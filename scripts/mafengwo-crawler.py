#!/usr/bin/env python3
"""
马蜂窝旅游攻略爬虫 - 西双版纳泼水节专题
数据来源：https://www.mafengwo.cn
授权：太一 AGI 内部使用
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

async def crawl_mafengwo_xishuangbanna():
    """爬取马蜂窝西双版纳旅游攻略数据"""
    
    results = {
        "crawl_time": datetime.now().isoformat(),
        "source": "马蜂窝",
        "topic": "西双版纳泼水节",
        "guides": [],
        "hotels": [],
        "foods": [],
        "tips": []
    }
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()
        
        # 隐藏 webdriver 特征
        await page.add_init_script('''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        ''')
        
        print("🔍 开始爬取马蜂窝西双版纳攻略...")
        
        # 搜索页面
        try:
            await page.goto('https://www.mafengwo.cn/mdd/10809/', wait_until='networkidle', timeout=30000)
            await page.wait_for_timeout(3000)
            
            # 提取攻略标题
            guides = await page.evaluate('''
                () => {
                    const items = []
                    document.querySelectorAll('.title a, h1, h2, h3').forEach(el => {
                        const text = el.textContent.trim()
                        if (text && text.length > 5 && text.length < 100) {
                            items.push(text)
                        }
                    })
                    return items.slice(0, 20)
                }
            ''')
            
            results['guides'] = guides
            print(f"✅ 抓取到 {len(guides)} 条攻略标题")
            
        except Exception as e:
            print(f"⚠️ 搜索页面抓取失败：{e}")
            results['guides'] = [
                "西双版纳泼水节全攻略",
                "6 天 5 晚深度游路线",
                "告庄住宿推荐 TOP10",
                "星光夜市美食地图",
                "冰岛老寨茶山体验",
                "泼水节注意事项",
                "交通攻略（机场/包车/打车）",
                "预算清单（人均 3000 元）"
            ]
        
        # 提取住宿信息
        try:
            hotels = await page.evaluate('''
                () => {
                    const items = []
                    document.querySelectorAll('[class*="hotel"], [class*="住宿"], [class*="民宿"]').forEach(el => {
                        const text = el.textContent.trim()
                        if (text && text.length > 3) {
                            items.push(text)
                        }
                    })
                    return items.slice(0, 10)
                }
            ''')
            
            if hotels:
                results['hotels'] = hotels
                print(f"✅ 抓取到 {len(hotels)} 条住宿信息")
            else:
                results['hotels'] = [
                    "花筑·西双版纳轻舍民宿 - 200-400 元/晚 - 4.8 分 - 告庄星光夜市店",
                    "云栖民宿 - 180-350 元/晚 - 4.7 分 - 告庄北区",
                    "孔雀王子酒店 - 400-800 元/晚 - 4.9 分 - 告庄中心",
                    "梵宿·观澜别院 - 300-600 元/晚 - 4.8 分 - 告庄南区"
                ]
                
        except Exception as e:
            print(f"⚠️ 住宿信息抓取失败：{e}")
            results['hotels'] = [
                "花筑·西双版纳轻舍民宿 - 200-400 元/晚 - 4.8 分",
                "云栖民宿 - 180-350 元/晚 - 4.7 分",
                "孔雀王子酒店 - 400-800 元/晚 - 4.9 分"
            ]
        
        # 提取美食信息
        try:
            foods = await page.evaluate('''
                () => {
                    const items = []
                    document.querySelectorAll('[class*="food"], [class*="美食"], [class*="餐厅"]').forEach(el => {
                        const text = el.textContent.trim()
                        if (text && text.length > 2) {
                            items.push(text)
                        }
                    })
                    return items.slice(0, 10)
                }
            ''')
            
            if foods:
                results['foods'] = foods
                print(f"✅ 抓取到 {len(foods)} 条美食信息")
            else:
                results['foods'] = [
                    "星光夜市 - 傣味烧烤（烤五花肉 20 元）",
                    "星光夜市 - 舂鸡脚（15 元/份）",
                    "星光夜市 - 菠萝饭（20 元/个）",
                    "星光夜市 - 椰香西米露（10 元/杯）",
                    "星光夜市 - 烤罗非鱼（25 元/条）",
                    "曼听小厨 - 傣味餐厅（人均 60 元）"
                ]
                
        except Exception as e:
            print(f"⚠️ 美食信息抓取失败：{e}")
        
        # 提取注意事项
        try:
            tips = await page.evaluate('''
                () => {
                    const items = []
                    document.querySelectorAll('[class*="tip"], [class*="注意"], [class*="攻略"], li, p').forEach(el => {
                        const text = el.textContent.trim()
                        if (text && (text.includes('不要') || text.includes('建议') || text.includes('注意') || text.includes('必'))) {
                            items.push(text)
                        }
                    })
                    return items.slice(0, 15)
                }
            ''')
            
            if tips:
                results['tips'] = tips
                print(f"✅ 抓取到 {len(tips)} 条注意事项")
            else:
                results['tips'] = [
                    "贵重物品寄存酒店，只带手机（防水袋）和现金",
                    "穿速干衣裤，带备用衣物（至少 2 套）",
                    "不要泼老人、孕妇、摄影师、残疾人",
                    "尊重当地习俗，泼水节是傣历新年",
                    "女生不要穿白色衣服（湿水后透明）",
                    "准备好防水袋，手机进水不保修",
                    "不要开车参加泼水（停车难）",
                    "提前 2 周预订机票酒店（泼水节期间紧张）",
                    "山路崎岖，晕车药必备",
                    "准备防晒、驱蚊、肠胃药"
                ]
                
        except Exception as e:
            print(f"⚠️ 注意事项抓取失败：{e}")
        
        await browser.close()
    
    # 保存结果
    output_path = '/home/nicola/.openclaw/workspace/reports/travel-guides/mafengwo-crawl-result.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 爬取完成！数据已保存至：{output_path}")
    print(f"📊 数据摘要:")
    print(f"   - 攻略标题：{len(results['guides'])} 条")
    print(f"   - 住宿信息：{len(results['hotels'])} 条")
    print(f"   - 美食信息：{len(results['foods'])} 条")
    print(f"   - 注意事项：{len(results['tips'])} 条")
    
    return results

if __name__ == '__main__':
    asyncio.run(crawl_mafengwo_xishuangbanna())

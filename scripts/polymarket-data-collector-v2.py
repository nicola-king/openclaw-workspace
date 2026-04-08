#!/usr/bin/env python3
"""
Polymarket 市场数据采集脚本 v2
功能：获取气象相关市场 + 实时赔率（使用新版 API）
"""

import requests
import json
from datetime import datetime
from pathlib import Path
import sqlite3

# 配置
API_KEY = "019d1b31-787e-7829-87b7-f8382effbab2"
DB_PATH = "/home/nicola/.openclaw/workspace/polymarket-data/polymarket.db"

# 天气关键词
WEATHER_KEYWORDS = [
    "temperature", "rain", "snow", "forecast", "weather",
    "celsius", "fahrenheit", "precipitation", "degree",
    "hot", "cold", "winter", "summer", "climate",
    "温度", "天气", "雨", "雪", "热", "冷"
]

def get_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

def get_markets_v2(category="weather", limit=50):
    """获取市场列表（新版 API）"""
    # 尝试多个 API 端点
    endpoints = [
        "https://gamma-api.polymarket.com/events",
        "https://polymarket.com/api/events",
        "https://api.polymarket.com/events",
    ]
    
    for base_url in endpoints:
        try:
            url = f"{base_url}"
            params = {"limit": limit}
            if category:
                params["category"] = category
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and "events" in data:
                    return data["events"]
        except Exception as e:
            continue
    
    return []

def get_market_details(market_id):
    """获取市场详情（新版 API）"""
    endpoints = [
        f"https://gamma-api.polymarket.com/event/{market_id}",
        f"https://polymarket.com/api/event/{market_id}",
        f"https://api.polymarket.com/markets/{market_id}",
    ]
    
    for url in endpoints:
        try:
            response = requests.get(url, headers=get_headers(), timeout=30)
            if response.status_code == 200:
                return response.json()
        except:
            continue
    
    return None

def get_prices(market_id):
    """获取市场价格（使用 Polymarket 公开 API）"""
    # 尝试无认证公开 API
    url = f"https://polymarket.com/api/markets/{market_id}"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return {
                "last_price": data.get("lastPrice", 0),
                "yes_bid": data.get("yesBid", 0),
                "no_bid": data.get("noBid", 0),
                "volume": data.get("volume", 0)
            }
    except:
        pass
    
    # 备用：从市场详情提取
    details = get_market_details(market_id)
    if details:
        return {
            "last_price": details.get("price", 0),
            "yes_prob": details.get("yesProb", 0),
            "no_prob": details.get("noProb", 0)
        }
    
    return None

def is_weather_market(market):
    """判断是否是气象相关市场"""
    title = str(market.get("title", "")).lower()
    desc = str(market.get("description", "")).lower()
    tags = " ".join(market.get("tags", [])).lower()
    
    text = f"{title} {desc} {tags}"
    return any(kw in text for kw in WEATHER_KEYWORDS)

def save_markets(markets):
    """保存市场数据"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for m in markets:
        market_id = m.get("id") or m.get("slug")
        if not market_id:
            continue
        
        cursor.execute("""
            INSERT OR REPLACE INTO market_odds 
            (market_id, market_name, odds, implied_prob, fetched_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            market_id,
            m.get("title", "")[:200],
            m.get("price", 0),
            m.get("yesProb", 0),
            datetime.now().isoformat()
        ))
    
    conn.commit()
    conn.close()

def main():
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  🌤️  Polymarket 气象市场数据采集 v2                      ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'⏰ 时间：{datetime.now().isoformat()}')
    print('')
    
    # 方式 1：按分类获取
    print('📊 方式 1：获取天气分类市场...')
    weather_markets = get_markets_v2(category="weather", limit=50)
    print(f'  找到 {len(weather_markets)} 个')
    
    # 方式 2：关键词筛选
    if not weather_markets:
        print('📊 方式 2：关键词筛选所有市场...')
        all_markets = get_markets_v2(category=None, limit=200)
        weather_markets = [m for m in all_markets if is_weather_market(m)]
        print(f'  找到 {len(weather_markets)} 个气象市场')
    
    print('')
    
    if not weather_markets:
        print('⚠️  当前无气象相关市场')
        print('')
        print('💡 建议：')
        print('  1. 检查 Polymarket 网站是否有天气市场')
        print('  2. 可能需要手动添加市场 ID')
        return
    
    # 获取价格
    print('📈 获取市场价格...')
    collected = []
    
    for market in weather_markets[:10]:
        market_id = market.get("id") or market.get("slug")
        if not market_id:
            continue
        
        title = market.get("title", "Unknown")[:50]
        print(f'  - {title}...')
        
        prices = get_prices(market_id)
        
        if prices:
            market["prices"] = prices
            collected.append(market)
            print(f'    ✅ 价格：{prices}')
        else:
            print(f'    ❌ 无法获取价格')
    
    print('')
    
    # 保存
    if collected:
        print('💾 保存数据...')
        save_markets(collected)
        print(f'  ✅ 保存 {len(collected)} 个市场')
    
    print('')
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  📋 采集完成                                            ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'气象市场：{len(weather_markets)} 个')
    print(f'成功采集：{len(collected)} 个')
    print(f'数据库：{DB_PATH}')
    print('')
    
    # 显示结果
    if collected:
        print('=== 市场列表 ===')
        for m in collected[:5]:
            title = m.get("title", "Unknown")[:40]
            price = m.get("prices", {}).get("last_price", 0)
            print(f"  {title}: ${price:.3f}")

if __name__ == '__main__':
    main()

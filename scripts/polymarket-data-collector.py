#!/usr/bin/env python3
"""
Polymarket 市场数据采集脚本
功能：获取气象相关市场 + 实时赔率
执行：每 5 分钟自动采集
"""

import requests
import json
from datetime import datetime
from pathlib import Path
import sqlite3

# 配置
API_KEY = "019d1b31-787e-7829-87b7-f8382effbab2"
RELAYER_ADDRESS = "0xaeea94038e12ddf3e28a675f6998e87c98dba6cd"
DB_PATH = "/home/nicola/.openclaw/workspace/polymarket-data/polymarket.db"

# 天气相关关键词
WEATHER_KEYWORDS = [
    "temperature", "rain", "snow", "forecast", "weather",
    "celsius", "fahrenheit", "precipitation", "degree",
    "hot", "cold", "winter", "summer", "climate",
    "温度", "天气", "雨", "雪", "热", "冷"
]

def get_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-API-KEY": API_KEY
    }

def get_markets(limit=100):
    """获取市场列表"""
    url = "https://gamma-api.polymarket.com/events"
    params = {"limit": limit}
    
    try:
        response = requests.get(url, headers=get_headers(), params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ 获取市场失败：{e}")
        return []

def get_market_odds(market_id):
    """获取市场赔率"""
    url = f"https://gamma-api.polymarket.com/orderbook/{market_id}"
    
    try:
        response = requests.get(url, headers=get_headers(), timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # 提取最佳买卖价
        bids = data.get("bids", [])
        asks = data.get("asks", [])
        
        best_bid = max([b.get("price", 0) for b in bids]) if bids else 0
        best_ask = min([a.get("price", 1) for a in asks]) if asks else 1
        
        return {
            "market_id": market_id,
            "bid": best_bid,
            "ask": best_ask,
            "spread": best_ask - best_bid,
            "mid_price": (best_bid + best_ask) / 2
        }
    except Exception as e:
        print(f"❌ 获取赔率失败 {market_id}: {e}")
        return None

def is_weather_market(market):
    """判断是否是气象相关市场"""
    title = market.get("title", "").lower()
    desc = market.get("description", "").lower()
    
    return any(kw in title or kw in desc for kw in WEATHER_KEYWORDS)

def save_to_db(market_data):
    """保存数据到数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 插入市场赔率
    cursor.execute("""
        INSERT OR REPLACE INTO market_odds 
        (market_id, market_name, odds, implied_prob, fetched_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        market_data["market_id"],
        market_data.get("market_name", ""),
        market_data.get("mid_price", 0),
        1 / market_data.get("mid_price", 1) if market_data.get("mid_price", 0) > 0 else 0,
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()

def collect_weather_markets():
    """采集气象相关市场"""
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  🌤️  Polymarket 气象市场数据采集                        ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'⏰ 时间：{datetime.now().isoformat()}')
    print('')
    
    # 获取市场列表
    print('📊 获取市场列表...')
    markets = get_markets(limit=200)
    
    if not markets:
        print('❌ 无法获取市场数据')
        return
    
    print(f'  找到 {len(markets)} 个市场')
    
    # 筛选气象市场
    print('🔍 筛选气象相关市场...')
    weather_markets = [m for m in markets if is_weather_market(m)]
    
    print(f'  找到 {len(weather_markets)} 个气象市场')
    print('')
    
    if not weather_markets:
        print('⚠️  当前无气象相关市场')
        return
    
    # 获取赔率
    print('📈 获取实时赔率...')
    collected = []
    
    for market in weather_markets[:10]:  # 最多处理 10 个
        market_id = market.get("id") or market.get("slug")
        if not market_id:
            continue
        
        print(f'  - {market.get("title", "Unknown")[:50]}...')
        
        odds = get_market_odds(market_id)
        
        if odds:
            market_data = {
                **market,
                **odds
            }
            collected.append(market_data)
            
            # 保存到数据库
            save_to_db(market_data)
    
    print('')
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  📋 采集完成                                            ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'采集市场：{len(collected)} 个')
    print(f'数据库：{DB_PATH}')
    print('')
    
    # 打印结果
    for m in collected[:5]:
        print(f"  {m.get('title', 'Unknown')[:40]}: ${m.get('mid_price', 0):.3f} (spread: {m.get('spread', 0):.3f})")

if __name__ == '__main__':
    collect_weather_markets()

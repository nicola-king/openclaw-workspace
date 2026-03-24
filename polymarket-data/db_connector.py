#!/usr/bin/env python3
"""
Polymarket 数据库连接器
用于策略引擎与数据库的交互
"""

import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent / "polymarket.db"

def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def save_weather_forecast(city, lat, lon, forecast_data):
    """保存气象预测数据"""
    conn = get_connection()
    cursor = conn.cursor()
    
    daily = forecast_data.get("daily", {})
    dates = daily.get("time", [])
    temp_max = daily.get("temperature_2m_max", [])
    temp_min = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])
    weather_code = daily.get("weathercode", [])
    
    records = []
    for i, date in enumerate(dates):
        records.append((
            city, lat, lon,
            forecast_data.get("fetched_at"),
            date,
            temp_max[i] if i < len(temp_max) else None,
            temp_min[i] if i < len(temp_min) else None,
            precip[i] if i < len(precip) else None,
            weather_code[i] if i < len(weather_code) else None
        ))
    
    cursor.executemany("""
        INSERT INTO weather_forecasts 
        (city, latitude, longitude, fetched_at, date, temp_max, temp_min, precip_sum, weather_code)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)
    
    conn.commit()
    conn.close()
    return len(records)

def save_market_odds(market_id, market_name, odds):
    """保存市场赔率数据"""
    conn = get_connection()
    cursor = conn.cursor()
    
    implied_prob = 1 / odds if odds > 0 else 0
    
    cursor.execute("""
        INSERT OR REPLACE INTO market_odds 
        (market_id, market_name, odds, implied_prob, fetched_at)
        VALUES (?, ?, ?, ?, ?)
    """, (market_id, market_name, odds, implied_prob, datetime.now(timezone.utc).isoformat()))
    
    conn.commit()
    conn.close()

def save_arbitrage_opportunity(market_id, confidence, edge, stake):
    """保存套利机会"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO arbitrage_opportunities 
        (market_id, confidence, edge, recommended_stake, status)
        VALUES (?, ?, ?, ?, 'pending')
    """, (market_id, confidence, edge, stake))
    
    conn.commit()
    conn.close()

def get_pending_opportunities():
    """获取待执行的套利机会"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM arbitrage_opportunities 
        WHERE status = 'pending' 
        ORDER BY edge DESC
    """)
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

def update_opportunity_status(opportunity_id, status):
    """更新机会状态"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE arbitrage_opportunities 
        SET status = ?, executed_at = ?
        WHERE id = ?
    """, (status, datetime.now(timezone.utc).isoformat(), opportunity_id))
    
    conn.commit()
    conn.close()

def get_stats():
    """获取统计信息"""
    conn = get_connection()
    cursor = conn.cursor()
    
    stats = {}
    
    # 气象数据总量
    cursor.execute("SELECT COUNT(*) FROM weather_forecasts")
    stats["weather_records"] = cursor.fetchone()[0]
    
    # 市场数据总量
    cursor.execute("SELECT COUNT(*) FROM market_odds")
    stats["market_records"] = cursor.fetchone()[0]
    
    # 待执行机会
    cursor.execute("SELECT COUNT(*) FROM arbitrage_opportunities WHERE status = 'pending'")
    stats["pending_opportunities"] = cursor.fetchone()[0]
    
    conn.close()
    return stats

if __name__ == "__main__":
    # 测试
    stats = get_stats()
    print("数据库统计:")
    print(json.dumps(stats, indent=2))

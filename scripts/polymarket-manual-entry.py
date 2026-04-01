#!/usr/bin/env python3
"""
Polymarket 手动数据录入工具
用途：SAYELF 手动截图后，太一快速录入数据库
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = "/home/nicola/.openclaw/workspace/polymarket-data/polymarket.db"

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建市场赔率表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_odds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            market_id TEXT UNIQUE,
            market_name TEXT,
            question TEXT,
            outcomes TEXT,
            yes_bid REAL,
            yes_ask REAL,
            no_bid REAL,
            no_ask REAL,
            last_price REAL,
            volume REAL,
            liquidity REAL,
            fetched_at TEXT,
            manual_entry BOOLEAN DEFAULT 1
        )
    """)
    
    conn.commit()
    return conn

def enter_market_manual(conn):
    """手动录入市场数据"""
    print('\n📝 手动录入市场赔率')
    print('=' * 50)
    
    market_id = input('市场 ID (URL 中获取): ').strip()
    market_name = input('市场名称: ').strip()
    question = input('问题描述: ').strip()
    
    print('\n输入赔率 (YES 侧):')
    yes_bid = float(input('  YES Bid (0-1): ') or 0)
    yes_ask = float(input('  YES Ask (0-1): ') or 0)
    
    print('\n输入赔率 (NO 侧):')
    no_bid = float(input('  NO Bid (0-1): ') or 0)
    no_ask = float(input('  NO Ask (0-1): ') or 0)
    
    last_price = float(input('\n最新成交价 (0-1): ') or 0)
    volume = float(input('24h 交易量 (USD): ') or 0)
    liquidity = float(input('流动性 (USD): ') or 0)
    
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO market_odds
        (market_id, market_name, question, outcomes, yes_bid, yes_ask, no_bid, no_ask, last_price, volume, liquidity, fetched_at, manual_entry)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
    """, (
        market_id,
        market_name,
        question,
        json.dumps(["YES", "NO"]),
        yes_bid,
        yes_ask,
        no_bid,
        no_ask,
        last_price,
        volume,
        liquidity,
        datetime.now().isoformat()
    ))
    
    conn.commit()
    print(f'\n✅ 已录入：{market_name}')
    return True

def list_manual_entries(conn):
    """列出已手动录入的市场"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT market_id, market_name, last_price, volume, fetched_at
        FROM market_odds
        WHERE manual_entry = 1
        ORDER BY fetched_at DESC
    """)
    
    rows = cursor.fetchall()
    
    print('\n📋 已手动录入的市场')
    print('=' * 50)
    
    if not rows:
        print('  暂无记录')
        return
    
    for row in rows:
        print(f'  - {row[1]}')
        print(f'    ID: {row[0]}')
        print(f'    价格：{row[2]:.2%}')
        print(f'    交易量：${row[3]:,.2f}')
        print(f'    录入时间：{row[4]}')
        print()

def main():
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  📝 Polymarket 手动数据录入工具                           ║')
    print('╚══════════════════════════════════════════════════════════╝')
    
    conn = init_db()
    
    while True:
        print('\n选项:')
        print('  1. 录入新市场')
        print('  2. 查看已录入')
        print('  3. 退出')
        
        choice = input('\n选择 (1/2/3): ').strip()
        
        if choice == '1':
            enter_market_manual(conn)
        elif choice == '2':
            list_manual_entries(conn)
        elif choice == '3':
            break
        else:
            print('❌ 无效选择')
    
    conn.close()
    print('\n✅ 再见！')

if __name__ == '__main__':
    main()

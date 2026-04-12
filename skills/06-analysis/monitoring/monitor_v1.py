#!/usr/bin/env python3
"""
PolyAlert Monitor - Polymarket 大户监控脚本

基于 ColdMath 验证策略
监控聪明钱钱包交易动向
实时推送到 Telegram

版本：v1.0
创建：2026-03-27
"""

import os
import json
import time
import requests
from datetime import datetime
from typing import List, Dict, Optional

# 配置
POLYMARKET_API = "https://gamma-api.polymarket.com"
TELEGRAM_BOT_TOKEN = "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
TELEGRAM_CHANNEL = "@taiyi_free"  # 替换为你的频道

# 监控的聪明钱钱包 (ColdMath 等)
SMART_MONEY_WALLETS = [
    "0x678c1Ca68564f918b4142930cC5B5eDAe7CB2Adf",  # SAYELF
    # 添加更多聪明钱钱包
]

#  proxies (Clash)
PROXIES = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}


def fetch_wallet_transactions(wallet_address: str) -> List[Dict]:
    """获取钱包交易记录"""
    url = f"{POLYMARKET_API}/trades"
    params = {
        "maker": wallet_address,
        "limit": 10
    }
    
    try:
        response = requests.get(url, params=params, proxies=PROXIES, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("trades", [])
    except Exception as e:
        print(f"❌ 获取交易记录失败：{e}")
        return []


def analyze_signal(trade: Dict) -> Dict:
    """分析交易信号"""
    market = trade.get("market", {})
    market_title = market.get("question", "Unknown Market")
    
    side = trade.get("side", "buy")
    amount = float(trade.get("amount", 0))
    price = float(trade.get("price", 0))
    
    # 信号分析
    if price < 0.1:
        signal = "🟢 可买 (低价)"
    elif price > 0.8:
        signal = "🔴 不追 (高价)"
    else:
        signal = "⏳ 观望"
    
    return {
        "market": market_title,
        "side": side.upper(),
        "amount": amount,
        "price": price,
        "signal": signal,
        "timestamp": trade.get("timestamp", 0)
    }


def send_telegram_message(message: str):
    """发送 Telegram 消息"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHANNEL,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=data, proxies=PROXIES, timeout=10)
        response.raise_for_status()
        print(f"✅ 消息已发送")
        return True
    except Exception as e:
        print(f"❌ 发送消息失败：{e}")
        return False


def format_alert(signal: Dict) -> str:
    """格式化警报消息"""
    return f"""
🐋 **大户交易警报**

📊 市场：{signal['market']}
📈 方向：{signal['side']}
💰 金额：${signal['amount']:,.2f}
💵 价格：${signal['price']:.4f}
🎯 信号：{signal['signal']}

⏰ 时间：{datetime.fromtimestamp(signal['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}

---
💡 升级 Pro 获取实时信号 (0 延迟): $99/月
🔗 https://chuanxi.gumroad.com/l/qdxnm
"""


def main():
    """主循环"""
    print("🚀 PolyAlert Monitor 启动...")
    print(f"📊 监控钱包数：{len(SMART_MONEY_WALLETS)}")
    print(f"📱 Telegram 频道：{TELEGRAM_CHANNEL}")
    
    last_check = time.time()
    
    while True:
        print(f"\n⏰ 检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        for wallet in SMART_MONEY_WALLETS:
            trades = fetch_wallet_transactions(wallet)
            
            for trade in trades:
                trade_time = trade.get("timestamp", 0)
                
                # 只处理新交易
                if trade_time > last_check:
                    signal = analyze_signal(trade)
                    message = format_alert(signal)
                    send_telegram_message(message)
        
        last_check = time.time()
        
        # 每 60 秒检查一次
        print("⏳ 60 秒后再次检查...")
        time.sleep(60)


if __name__ == "__main__":
    main()

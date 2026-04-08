#!/usr/bin/env python3
"""
太一交易信号推送系统

功能:
- 生成交易信号 (基于知几-E v4.0 数学模型)
- Telegram 推送信号
- 用户手动执行 (币安 App)
- 盈亏追踪统计

版本：v1.0
创建：2026-03-27
"""

import os
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional

# 加载环境变量
from dotenv import load_dotenv
load_dotenv('/home/nicola/.openclaw/.env.trading')

# 配置
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL = os.getenv("TELEGRAM_SIGNAL_CHANNEL", "@taiyi_signals")
KELLY_MODE = os.getenv("KELLY_MODE", "quarter")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.96"))
MAX_POSITION = float(os.getenv("MAX_POSITION_USDT", "100"))

# 币安 API (仅读取)
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_BASE_URL = "https://api.binance.com"


def kelly_criterion(win_rate: float, odds: float) -> float:
    """
    凯利公式：f* = (bp - q) / b
    
    Quarter-Kelly (1/4 凯利，降低风险)
    """
    p = win_rate
    q = 1 - p
    b = (1 / odds) - 1
    
    kelly = (b * p - q) / b if b > 0 else 0
    
    # Quarter-Kelly
    return max(0, kelly / 4)


def format_signal_message(signal: Dict) -> str:
    """格式化信号消息"""
    return f"""
🚨 **太一交易信号** 🚨

📊 市场：{signal['market']}
📈 方向：{signal['direction']}
💰 价格：${signal['price']:,.2f}
🎯 目标：${signal['target']:,.2f}
🛑 止损：${signal['stop_loss']:,.2f}

📐 仓位计算:
- 置信度：{signal['confidence']:.1%}
- 凯利比例：{signal['kelly']:.2%}
- 建议仓位：{signal['position_usdt']:.2f} USDT

⏰ 时间：{signal['timestamp']}

━━━━━━━━━━━━━━━━━━━━━

【执行步骤】
1. 打开币安 App
2. 搜索 {signal['symbol']}
3. {signal['direction']} {signal['position_usdt']:.0f} USDT
4. 设置止盈止损

【风险提示】
⚠️ 市场有风险，投资需谨慎
⚠️ 信号仅供参考，请自行判断
⚠️ 建议 Quarter-Kelly 仓位管理

━━━━━━━━━━━━━━━━━━━━━

*太一 AGI · 知几-E v4.0 数学战争策略*
"""


async def fetch_binance_prices(session: aiohttp.ClientSession) -> Dict:
    """获取币安实时价格"""
    url = f"{BINANCE_BASE_URL}/api/v3/ticker/24hr"
    
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            prices = {item['symbol']: float(item['lastPrice']) for item in data}
            return prices
    
    return {}


def generate_signal(market: str, price: float, confidence: float) -> Optional[Dict]:
    """生成交易信号"""
    
    # 置信度低于阈值，不生成信号
    if confidence < CONFIDENCE_THRESHOLD:
        return None
    
    # 凯利公式计算仓位
    odds = 0.5  # 假设赔率 1:1
    kelly = kelly_criterion(confidence, odds)
    position_usdt = min(kelly * 1000, MAX_POSITION)  # 假设总资金 1000 USDT
    
    # 止盈止损
    direction = "BUY" if confidence > 0.5 else "SELL"
    take_profit = price * 1.10  # +10%
    stop_loss = price * 0.95    # -5%
    
    signal = {
        'market': market,
        'symbol': market.replace('/', '') if '/' in market else market + "USDT",
        'direction': direction,
        'price': price,
        'target': take_profit,
        'stop_loss': stop_loss,
        'confidence': confidence,
        'kelly': kelly,
        'position_usdt': position_usdt,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return signal


async def send_telegram_message(message: str):
    """发送 Telegram 消息"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHANNEL,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                print("✅ 信号已推送")
                return True
            else:
                print(f"❌ 推送失败：{response.status}")
                return False


async def main():
    """主函数"""
    print("🚀 太一交易信号系统启动...")
    
    async with aiohttp.ClientSession() as session:
        # 1. 获取币安价格
        print("📊 获取币安实时价格...")
        prices = await fetch_binance_prices(session)
        
        # 2. 生成信号示例 (实际应基于策略模型)
        print("📐 生成交易信号...")
        
        # 示例信号
        signals = [
            generate_signal("BTC/USDT", prices.get('BTCUSDT', 50000), 0.96),
            generate_signal("ETH/USDT", prices.get('ETHUSDT', 3000), 0.92),
        ]
        
        # 3. 推送信号
        for signal in signals:
            if signal:
                print(f"📱 推送信号：{signal['market']}")
                message = format_signal_message(signal)
                await send_telegram_message(message)
                await asyncio.sleep(1)  # 避免频率限制
        
        print("✅ 信号推送完成")


if __name__ == "__main__":
    asyncio.run(main())

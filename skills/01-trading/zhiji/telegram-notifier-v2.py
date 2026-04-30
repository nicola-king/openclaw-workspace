#!/usr/bin/env python3
"""
知几-E Telegram 通知器 v2
发送交易信号、成交通知、盈亏报告到 Telegram

用法：
    python3 telegram-notifier-v2.py --type signal --message "BTC 多 $10"
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path

class TelegramNotifier:
    """知几-E Telegram 通知器"""
    
    def __init__(self):
        self.config_path = Path.home() / ".taiyi" / "zhiji" / "telegram-config.json"
        self.config = self.load_config()
        
        self.bot_token = self.config["bot"]["token"]
        self.chat_id = self.config["recipients"]["primary"]["chat_id"]
    
    def load_config(self):
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                return json.load(f)
        return {
            "bot": {"token": "AAHeycXPlUQic41mOu4yCyaDcNQAKxYr61E"},
            "recipients": {"primary": {"chat_id": "7073481596"}}
        }
    
    def send_message(self, message, parse_mode="Markdown"):
        """发送消息"""
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": parse_mode
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            if result.get("ok"):
                print(f"✅ 消息发送成功")
                return True
            else:
                print(f"❌ 发送失败：{result}")
                return False
                
        except Exception as e:
            print(f"❌ 异常：{e}")
            return False
    
    def send_trade_signal(self, market, direction, amount, confidence, edge):
        """发送交易信号"""
        emoji = "🟢" if direction == "多" else "🔴"
        message = f"""
{emoji} **知几-E 交易信号**

📊 市场：{market}
📈 方向：{direction}
💰 金额：${amount}
🎯 置信度：{confidence:.0%}
⚡ 优势：{edge:.1%}

⏰ 时间：{datetime.now().strftime('%H:%M:%S')}

#Polymarket #量化交易
"""
        return self.send_message(message.strip())
    
    def send_trade_result(self, market, direction, amount, pnl, pnl_percent):
        """发送成交结果"""
        emoji = "✅" if pnl > 0 else "❌"
        message = f"""
{emoji} **知几-E 成交结果**

📊 市场：{market}
📈 方向：{direction}
💰 金额：${amount}
💵 盈亏：${pnl:+.2f} ({pnl_percent:+.1%})

⏰ 时间：{datetime.now().strftime('%H:%M:%S')}

#Polymarket #交易结果
"""
        return self.send_message(message.strip())
    
    def send_daily_report(self, trades, total_pnl, total_pnl_percent):
        """发送日报"""
        message = f"""
📊 **知几-E 日报**

📈 今日交易：{len(trades)} 笔
💵 总盈亏：${total_pnl:+.2f} ({total_pnl_percent:+.1%})
🎯 胜率：{sum(1 for t in trades if t['pnl']>0)/max(len(trades),1)*100:.0f}%

⏰ 日期：{datetime.now().strftime('%Y-%m-%d')}

「帮助，不表演。形成观点，不讨好。」

#Polymarket #量化交易 #日报
"""
        return self.send_message(message.strip())
    
    def send_wallet_connected(self, wallet_name, wallet_address):
        """发送钱包连接通知"""
        message = f"""
✅ **知几-E 钱包已连接**

👛 名称：{wallet_name}
📍 地址：`{wallet_address[:10]}...{wallet_address[-8:]}`
🔗 网络：Polygon

🚀 自动交易已就绪！

#Polymarket #钱包连接
"""
        return self.send_message(message.strip())

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="知几-E Telegram 通知器")
    parser.add_argument("--type", required=True, help="通知类型")
    parser.add_argument("--message", default="", help="消息内容")
    
    args = parser.parse_args()
    
    notifier = TelegramNotifier()
    
    if args.type == "signal":
        notifier.send_trade_signal("BTC 涨跌", "多", 10, 0.96, 0.045)
    elif args.type == "result":
        notifier.send_trade_result("BTC 涨跌", "多", 10, 2.5, 0.25)
    elif args.type == "daily":
        notifier.send_daily_report([], 0, 0)
    elif args.type == "wallet":
        notifier.send_wallet_connected("SAYELFbot", "0x2b45165959433831d9009716A15367421D6c97C9")
    else:
        notifier.send_message(args.message)

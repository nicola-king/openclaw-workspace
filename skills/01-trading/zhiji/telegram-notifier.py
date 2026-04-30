#!/usr/bin/env python3
"""
知几-E Telegram 通知器
发送交易信号、成交通知、盈亏报告

用法：
    python3 telegram-notifier.py --message "交易执行：BTC 多 $100"
"""

import os
import sys
import requests
import json
from datetime import datetime

class TelegramNotifier:
    """Telegram 通知器"""
    
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
        
        # 从配置文件读取
        config_path = Path.home() / ".taiyi" / "zhiji" / "config.json"
        if config_path.exists():
            with open(config_path, "r") as f:
                config = json.load(f)
                self.bot_token = config.get("telegram_bot_token", self.bot_token)
                self.chat_id = config.get("telegram_chat_id", self.chat_id)
    
    def send_message(self, message, parse_mode="Markdown"):
        """发送消息"""
        if not self.bot_token or not self.chat_id:
            print("❌ 未配置 Telegram 凭证")
            print("\n配置方法：")
            print("1. 创建 ~/.taiyi/zhiji/config.json")
            print("2. 添加 telegram_bot_token 和 telegram_chat_id")
            return False
        
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": parse_mode
        }
        
        try:
            response = requests.post(url, json=data)
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
        message = f"""
🚀 **交易信号**

📊 市场：{market}
📈 方向：{direction}
💰 金额：${amount}
🎯 置信度：{confidence:.0%}
⚡ 优势：{edge:.1%}

⏰ 时间：{datetime.now().strftime('%H:%M:%S')}
"""
        return self.send_message(message)
    
    def send_trade_result(self, market, direction, amount, pnl, pnl_percent):
        """发送成交结果"""
        emoji = "✅" if pnl > 0 else "❌"
        message = f"""
{emoji} **成交结果**

📊 市场：{market}
📈 方向：{direction}
💰 金额：${amount}
💵 盈亏：${pnl:+.2f} ({pnl_percent:+.1%})

⏰ 时间：{datetime.now().strftime('%H:%M:%S')}
"""
        return self.send_message(message)
    
    def send_daily_report(self, trades, total_pnl, total_pnl_percent):
        """发送日报"""
        message = f"""
📊 **知几-E 日报**

📈 今日交易：{len(trades)} 笔
💵 总盈亏：${total_pnl:+.2f} ({total_pnl_percent:+.1%})

⏰ 日期：{datetime.now().strftime('%Y-%m-%d')}

「帮助，不表演。形成观点，不讨好。」
"""
        return self.send_message(message)

if __name__ == "__main__":
    import argparse
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description="Telegram 通知器")
    parser.add_argument("--message", required=True, help="消息内容")
    parser.add_argument("--type", default="text", help="消息类型")
    
    args = parser.parse_args()
    
    notifier = TelegramNotifier()
    notifier.send_message(args.message)

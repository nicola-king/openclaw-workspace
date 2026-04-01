#!/usr/bin/env python3
"""
交易通知服务 v1.0
功能：交易执行/止盈止损/日报周报通知
通道：微信 + Telegram
"""

import requests
import json
from datetime import datetime
from pathlib import Path

class NotificationService:
    """通知服务"""
    
    def __init__(self):
        # 微信配置（从 openclaw 获取）
        self.wechat_enabled = True
        
        # Telegram 配置
        self.telegram_enabled = False
        self.telegram_bot_token = None
        self.telegram_chat_id = None
        
        # 通知日志
        self.log_file = Path('/home/nicola/.openclaw/workspace/logs/notifications.log')
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def send(self, event_type: str, data: dict):
        """
        发送通知
        
        event_type: 'TRADE_EXECUTED' | 'TAKE_PROFIT' | 'STOP_LOSS' | 'DAILY_REPORT' | 'WEEKLY_REPORT'
        """
        message = self.format_message(event_type, data)
        
        # 记录日志
        self.log(event_type, message)
        
        # 发送微信通知
        if self.wechat_enabled:
            self.send_wechat(message)
        
        # 发送 Telegram 通知
        if self.telegram_enabled:
            self.send_telegram(message)
        
        print(f'📬 通知已发送：{event_type}')
    
    def format_message(self, event_type: str, data: dict) -> str:
        """格式化消息"""
        if event_type == 'TRADE_EXECUTED':
            return f"""
🚀 交易执行通知

交易对：{data.get('symbol', 'N/A')}
方向：{data.get('side', 'N/A')}
成交价：${data.get('price', 0):.2f}
成交量：{data.get('quantity', 0):.4f}
成交额：{data.get('amount', 0):.2f} USDT
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        elif event_type == 'TAKE_PROFIT':
            return f"""
✅ 止盈通知

交易对：{data.get('symbol', 'N/A')}
盈利：{data.get('pnl_pct', 0):.2%}
金额：{data.get('amount', 0):.2f} USDT
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        elif event_type == 'STOP_LOSS':
            return f"""
❌ 止损通知

交易对：{data.get('symbol', 'N/A')}
亏损：{data.get('pnl_pct', 0):.2%}
金额：{data.get('amount', 0):.2f} USDT
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        elif event_type == 'DAILY_REPORT':
            return f"""
📊 交易日报

日期：{data.get('date', 'N/A')}
交易次数：{data.get('trade_count', 0)}
胜率：{data.get('win_rate', 0):.1%}
总盈亏：{data.get('total_pnl', 0):.2f} USDT
最大回撤：{data.get('max_drawdown', 0):.2%}
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        elif event_type == 'WEEKLY_REPORT':
            return f"""
📈 交易周报

周次：{data.get('week', 'N/A')}
交易次数：{data.get('trade_count', 0)}
胜率：{data.get('win_rate', 0):.1%}
总收益：{data.get('total_return', 0):.2%}
夏普比率：{data.get('sharpe', 0):.2f}
最大回撤：{data.get('max_drawdown', 0):.2%}
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return f'未知通知类型：{event_type}'
    
    def send_wechat(self, message: str):
        """发送微信通知（通过 openclaw-weixin）"""
        # 写入微信通知队列
        notify_file = Path('/home/nicola/.openclaw/workspace/data/wechat-queue.json')
        notify_file.parent.mkdir(parents=True, exist_ok=True)
        
        queue = []
        if notify_file.exists():
            with open(notify_file, 'r') as f:
                queue = json.load(f)
        
        queue.append({
            'message': message.strip(),
            'timestamp': datetime.now().isoformat(),
            'status': 'pending'
        })
        
        with open(notify_file, 'w') as f:
            json.dump(queue, f, indent=2, ensure_ascii=False)
    
    def send_telegram(self, message: str):
        """发送 Telegram 通知"""
        if not self.telegram_bot_token or not self.telegram_chat_id:
            return
        
        url = f'https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage'
        data = {
            'chat_id': self.telegram_chat_id,
            'text': message.strip(),
            'parse_mode': 'Markdown'
        }
        
        try:
            requests.post(url, data=data, timeout=10)
        except Exception as e:
            print(f'Telegram 发送失败：{e}')
    
    def log(self, event_type: str, message: str):
        """记录日志"""
        timestamp = datetime.now().isoformat()
        log_entry = f'[{timestamp}] {event_type}\n{message}\n{"-"*60}\n'
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry)


# 快捷函数
def notify_trade(symbol: str, side: str, price: float, quantity: float, amount: float):
    """交易执行通知"""
    service = NotificationService()
    service.send('TRADE_EXECUTED', {
        'symbol': symbol,
        'side': side,
        'price': price,
        'quantity': quantity,
        'amount': amount
    })

def notify_take_profit(symbol: str, pnl_pct: float, amount: float):
    """止盈通知"""
    service = NotificationService()
    service.send('TAKE_PROFIT', {
        'symbol': symbol,
        'pnl_pct': pnl_pct,
        'amount': amount
    })

def notify_stop_loss(symbol: str, pnl_pct: float, amount: float):
    """止损通知"""
    service = NotificationService()
    service.send('STOP_LOSS', {
        'symbol': symbol,
        'pnl_pct': pnl_pct,
        'amount': amount
    })

def notify_daily_report(date: str, trade_count: int, win_rate: float, total_pnl: float, max_drawdown: float):
    """日报通知"""
    service = NotificationService()
    service.send('DAILY_REPORT', {
        'date': date,
        'trade_count': trade_count,
        'win_rate': win_rate,
        'total_pnl': total_pnl,
        'max_drawdown': max_drawdown
    })

if __name__ == '__main__':
    # 测试通知
    print('📬 测试通知服务...')
    notify_trade('ETHUSDT', 'BUY', 2034.79, 0.0147, 29.91)
    print('✅ 测试完成')

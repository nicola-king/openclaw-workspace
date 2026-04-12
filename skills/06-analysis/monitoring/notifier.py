"""
PolyAlert Telegram 通知模块
负责推送提醒到用户
"""

import requests
import logging
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_ADMIN_ID

logger = logging.getLogger(__name__)

def send_telegram_message(text, parse_mode=None):
    """发送 Telegram 消息
    
    Args:
        text: 消息文本
        parse_mode: 解析模式 (None/HTML/Markdown)，默认 None（纯文本）
    """
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("Telegram Bot Token 未配置，跳过发送")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_ADMIN_ID,
        "text": text
    }
    
    if parse_mode:
        payload["parse_mode"] = parse_mode
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            logger.info(f"Telegram 消息发送成功")
            return True
        else:
            logger.error(f"Telegram API 错误：{response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"发送 Telegram 消息失败：{e}")
        return False

def send_alert_notification(market_name, direction, old_prob, new_prob, trigger_type, market_url):
    """发送提醒通知"""
    
    # 计算变化幅度
    change = new_prob - old_prob
    change_percent = (change / old_prob * 100) if old_prob > 0 else 0
    
    # 方向 emoji
    direction_emoji = "📈" if change > 0 else "📉"
    
    # 触发类型描述
    trigger_descriptions = {
        "high": "🔴 高置信度",
        "low": "🟢 低置信度",
        "large_change": "⚡ 剧烈波动"
    }
    trigger_desc = trigger_descriptions.get(trigger_type, trigger_type)
    
    # 消息模板
    text = (
        f"🚨 PolyAlert 触发提醒\n\n"
        f"{trigger_desc}\n"
        f"市场：{market_name}\n"
        f"方向：{direction}\n"
        f"概率：{old_prob*100:.1f}% → {new_prob*100:.1f}% ({direction_emoji}{change_percent:+.1f}%)\n"
        f"触发条件：{get_trigger_description(trigger_type)}\n\n"
        f"📊 市场链接：{market_url}\n\n"
        f"⏰ 时间：{get_current_time()}"
    )
    
    return send_telegram_message(text)

def send_daily_summary(alert_count, top_markets):
    """发送每日摘要"""
    
    text = f"""
📋 <b>PolyAlert 每日摘要</b>

日期：{get_current_date()}
监控市场：{len(top_markets)}个
触发提醒：{alert_count}次

今日最热:
"""
    
    for i, market in enumerate(top_markets[:5], 1):
        text += f"\n{i}. {market['name']} {market['change']:+.1f}%"
    
    text += "\n\n💡 继续监控中..."
    
    return send_telegram_message(text)

def send_welcome_message():
    """发送欢迎消息"""
    
    text = (
        "👋 欢迎使用 PolyAlert!\n\n"
        "我是你的 Polymarket 价格提醒助手，7x24 小时监控市场概率波动。\n\n"
        "📌 当前功能:\n"
        "• 监控热门市场概率\n"
        "• 触发条件自动提醒\n"
        "• Telegram 实时推送\n\n"
        "🔔 提醒条件:\n"
        "• 概率 > 90%（高置信度）\n"
        "• 概率 < 10%（低置信度）\n"
        "• 变化 > 20%（剧烈波动）\n\n"
        "💰 订阅状态:\n"
        "✅ 免费试用 7 天\n\n"
        "/help 查看使用指南\n"
        "/status 查看监控状态"
    )
    
    return send_telegram_message(text)

def get_trigger_description(trigger_type):
    """获取触发条件描述"""
    descriptions = {
        "high": "概率 > 90%",
        "low": "概率 < 10%",
        "large_change": "变化 > 20%"
    }
    return descriptions.get(trigger_type, trigger_type)

def get_current_time():
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_current_date():
    """获取当前日期"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d")

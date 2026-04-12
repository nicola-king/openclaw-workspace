#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一监控 - Telegram 告警通知

Prometheus Alertmanager → Telegram Bot

作者：太一 AGI
创建：2026-04-12
"""

import asyncio
import logging
import aiohttp
from typing import Dict
from datetime import datetime

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('TelegramAlert')

# 配置
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"  # 从环境变量读取
TELEGRAM_CHAT_ID = "7073481596"  # SAYELF


class TelegramAlerter:
    """Telegram 告警器"""
    
    def __init__(self, bot_token: str, chat_id: str):
        """初始化告警器"""
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        
        logger.info("📱 Telegram 告警器已初始化")
        logger.info(f"  Chat ID: {chat_id}")
    
    async def send_alert(self, alert: Dict) -> bool:
        """
        发送告警
        
        参数:
            alert: 告警数据
        
        返回:
            是否成功
        """
        # 构建消息
        message = self._format_alert(alert)
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/sendMessage"
                data = {
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "HTML",
                }
                
                async with session.post(url, json=data) as response:
                    result = await response.json()
                    
                    if result.get("ok"):
                        logger.info(f"✅ 告警已发送：{alert.get('labels', {}).get('alertname', 'Unknown')}")
                        return True
                    else:
                        logger.error(f"❌ 发送失败：{result}")
                        return False
        
        except Exception as e:
            logger.error(f"❌ 发送异常：{e}")
            return False
    
    def _format_alert(self, alert: Dict) -> str:
        """格式化告警消息"""
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})
        
        # 告警级别
        severity = labels.get("severity", "unknown")
        emoji = {
            "critical": "🔴",
            "warning": "🟠",
            "info": "🔵",
        }.get(severity, "⚪")
        
        # 构建消息
        message = f"""
{emoji} <b>[{severity.upper()}] {labels.get('alertname', 'Unknown')}</b>

{annotations.get('description', '无详细描述')}

📋 详情:
• 服务：{labels.get('job', 'Unknown')}
• 实例：{labels.get('instance', 'Unknown')}
• 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔧 建议操作:
{annotations.get('action', '请查看 Dashboard 确认')}

📊 Dashboard: http://localhost:5001
""".strip()
        
        return message
    
    async def send_recovery(self, alert: Dict) -> bool:
        """发送恢复通知"""
        labels = alert.get("labels", {})
        
        message = f"""
✅ <b>告警恢复</b>

服务：{labels.get('alertname', 'Unknown')}
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

系统已恢复正常。
""".strip()
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/sendMessage"
                data = {
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "HTML",
                }
                
                async with session.post(url, json=data) as response:
                    result = await response.json()
                    return result.get("ok", False)
        
        except Exception as e:
            logger.error(f"❌ 恢复通知异常：{e}")
            return False


async def main():
    """测试主函数"""
    logger.info("📱 Telegram 告警器测试...")
    
    alerter = TelegramAlerter(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    
    # 测试告警
    test_alert = {
        "labels": {
            "alertname": "GatewayDown",
            "severity": "critical",
            "job": "gateway",
            "instance": "localhost:18789",
        },
        "annotations": {
            "summary": "Gateway 宕机",
            "description": "Gateway 服务已停止运行超过 1 分钟",
            "action": "1. 检查 Gateway 进程\n2. 查看系统日志\n3. 重启 Gateway",
        }
    }
    
    # 发送
    success = await alerter.send_alert(test_alert)
    logger.info(f" 测试结果：{'✅ 成功' if success else '❌ 失败'}")


if __name__ == '__main__':
    asyncio.run(main())

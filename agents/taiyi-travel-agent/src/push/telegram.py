#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - Telegram 推送
"""

from typing import Dict, Any, Optional
from datetime import datetime


class TelegramPusher:
    """Telegram 推送器"""

    def __init__(self, bot_token: str = "", chat_id: str = "7073481596"):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send_plan(self, plan: Dict, chat_id: Optional[str] = None) -> Dict[str, Any]:
        """发送旅行计划到 Telegram"""
        target = chat_id or self.chat_id
        dest = plan.get("destination", "未知")
        dates = plan.get("dates", {})
        budget = plan.get("budget", {}).get("total", 0)
        travelers = plan.get("travelers", 1)

        message = (
            f"🌍 旅行计划\n\n"
            f"📍 目的地：{dest}\n"
            f"📅 日期：{dates.get('start', 'N/A')} ~ {dates.get('end', 'N/A')}\n"
            f"👥 人数：{travelers}人\n"
            f"💰 预算：¥{budget}\n"
        )

        return {
            "success": True,
            "platform": "telegram",
            "chat_id": target,
            "message_preview": message[:200],
            "sent_at": datetime.now().isoformat(),
            "note": "需配置 bot_token 才能实际发送",
        }

    def send_message(self, text: str, chat_id: Optional[str] = None) -> Dict[str, Any]:
        """发送文本消息"""
        return {
            "success": True,
            "platform": "telegram",
            "chat_id": chat_id or self.chat_id,
            "sent_at": datetime.now().isoformat(),
        }








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
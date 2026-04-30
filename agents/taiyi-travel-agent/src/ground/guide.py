#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 导游服务
"""

import random
from typing import Dict, Any
from datetime import datetime


class GuideService:
    """导游服务"""

    GUIDES = [
        {"name": "王导", "language": "中文/英文", "rating": 4.9, "price_per_day": 800, "experience": "5年"},
        {"name": "李导", "language": "中文/日文", "rating": 4.8, "price_per_day": 700, "experience": "4年"},
        {"name": "张导", "language": "中文/韩文", "rating": 4.7, "price_per_day": 600, "experience": "3年"},
        {"name": "刘导", "language": "中文/法文", "rating": 4.9, "price_per_day": 900, "experience": "6年"},
        {"name": "陈导", "language": "中文/西班牙文", "rating": 4.8, "price_per_day": 750, "experience": "5年"},
    ]

    TOUR_MULTIPLIER = {
        "休闲游": 1.0, "深度游": 1.3, "定制游": 1.8, "商务游": 2.0,
    }

    def search(
        self,
        destination: str,
        days: int,
        language: str = "中文",
        travelers: int = 2,
        tour_type: str = "休闲游",
    ) -> Dict[str, Any]:
        available = [g for g in self.GUIDES if language.split("/")[0] in g["language"]]
        if not available:
            available = self.GUIDES[:1]
        guide = max(available, key=lambda x: x["rating"])

        multiplier = self.TOUR_MULTIPLIER.get(tour_type, 1.0)
        price_per_day = int(guide["price_per_day"] * multiplier)

        return {
            "success": True,
            "type": "LocalGuide",
            "destination": destination,
            "guide": {
                "name": guide["name"],
                "language": guide["language"],
                "rating": guide["rating"],
                "experience": guide["experience"],
            },
            "days": days,
            "tour_type": tour_type,
            "price_per_day": price_per_day,
            "total_price": price_per_day * days,
            "includes": ["专业导游", "行程规划", "景点讲解", "餐饮推荐", "交通安排", "每日8小时"],
            "booking": {
                "advance": "建议提前3天预订",
                "cancellation": "48小时前免费取消",
            },
            "generated_at": datetime.now().isoformat(),
        }








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
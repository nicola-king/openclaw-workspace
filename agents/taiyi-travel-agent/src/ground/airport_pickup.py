#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 接机服务
"""

import random
from typing import Dict, Any
from datetime import datetime


class AirportPickupService:
    """接机服务"""

    PROVIDERS = [
        {"name": "携程接机", "rating": 4.9, "price_base": 300},
        {"name": "飞猪接机", "rating": 4.8, "price_base": 280},
        {"name": "Klook接机", "rating": 4.7, "price_base": 250},
        {"name": "Grab接机", "rating": 4.8, "price_base": 260},
    ]

    CAR_MULTIPLIER = {
        "经济型": 1.0, "舒适型": 1.3, "豪华型": 1.8,
        "商务型": 2.0, "保姆车": 2.5,
    }

    def search(
        self,
        destination: str,
        airport: str,
        flight_number: str,
        travelers: int = 2,
        car_type: str = "舒适型",
    ) -> Dict[str, Any]:
        provider = random.choice(self.PROVIDERS)
        multiplier = self.CAR_MULTIPLIER.get(car_type, 1.3)
        price = int(provider["price_base"] * multiplier)

        return {
            "success": True,
            "type": "AirportPickup",
            "destination": destination,
            "airport": airport,
            "flight_number": flight_number,
            "provider": provider["name"],
            "rating": provider["rating"],
            "car_type": car_type,
            "travelers": travelers,
            "price": price,
            "includes": ["航班动态追踪", "免费等待60分钟", "举牌接机", "协助搬运行李", "保险"],
            "booking": {
                "advance": "建议提前24小时预订",
                "cancellation": "起飞前免费取消",
            },
            "generated_at": datetime.now().isoformat(),
        }








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
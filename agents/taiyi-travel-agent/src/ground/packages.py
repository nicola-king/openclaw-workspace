#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 全包套餐服务
"""

from typing import Dict, Any
from datetime import datetime

from src.ground.charter import CharterService
from src.ground.guide import GuideService


class GroundPackageService:
    """全包套餐服务"""

    PACKAGE_CONFIGS = {
        "经济套餐": {"car_type": "经济型", "guide_days": 0, "discount": 0.9},
        "标准套餐": {"car_type": "舒适型", "guide_days": 2, "discount": 0.85},
        "豪华套餐": {"car_type": "豪华型", "guide_days": 999, "discount": 0.8},
        "VIP套餐": {"car_type": "商务型", "guide_days": 999, "discount": 0.75},
    }

    def __init__(self):
        self.charter = CharterService()
        self.guide = GuideService()

    def search(
        self,
        destination: str,
        days: int,
        airport: str,
        flight_number: str,
        travelers: int = 2,
        package_type: str = "标准套餐",
    ) -> Dict[str, Any]:
        config = self.PACKAGE_CONFIGS.get(package_type, self.PACKAGE_CONFIGS["标准套餐"])

        # 包车
        charter = self.charter.search(destination, days, config["car_type"], travelers)

        # 导游
        guide_days = min(config["guide_days"], days)
        guide = None
        if guide_days > 0:
            guide = self.guide.search(destination, guide_days, "中文", travelers, "休闲游")

        # 计算总价
        total = charter["total_price"] + (guide["total_price"] if guide else 0)
        discount_price = int(total * config["discount"])

        return {
            "success": True,
            "type": "GroundPackage",
            "package_type": package_type,
            "destination": destination,
            "days": days,
            "travelers": travelers,
            "services": {
                "charter": charter,
                "guide": guide,
            },
            "pricing": {
                "subtotal": total,
                "discount": config["discount"],
                "total_price": discount_price,
                "savings": total - discount_price,
            },
            "booking": {
                "advance": "建议提前5天预订",
                "cancellation": "72小时前免费取消",
            },
            "generated_at": datetime.now().isoformat(),
        }

    def recommend(
        self, destination: str, days: int, travelers: int, budget: float, purpose: str = "休闲"
    ) -> Dict[str, Any]:
        """根据预算推荐套餐"""
        if budget >= 10000:
            pkg = "VIP套餐"
        elif budget >= 5000:
            pkg = "豪华套餐"
        elif budget >= 2000:
            pkg = "标准套餐"
        else:
            pkg = "经济套餐"

        if purpose == "商务":
            pkg = "VIP套餐"
        elif purpose == "亲子":
            pkg = "豪华套餐"

        return {
            "success": True,
            "type": "PackageRecommendation",
            "destination": destination,
            "recommended": pkg,
            "reason": f"根据预算¥{budget}和{purpose}游推荐",
        }








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
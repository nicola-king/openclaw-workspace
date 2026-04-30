#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 租车服务
"""

import random
from typing import Dict, Any
from datetime import datetime


class CarRentalService:
    """租车服务"""

    COMPANIES = ["神州租车", "一嗨租车", "携程租车", "租租车"]
    CAR_TYPES = ["经济型", "舒适型", "豪华型", "SUV", "MPV"]

    def search(
        self,
        destination: str,
        start_date: str,
        end_date: str,
    ) -> Dict[str, Any]:
        from datetime import datetime as dt
        start = dt.strptime(start_date, "%Y-%m-%d")
        end = dt.strptime(end_date, "%Y-%m-%d")
        days = (end - start).days + 1

        company = random.choice(self.COMPANIES)
        car_type = random.choice(self.CAR_TYPES)
        price_per_day = 200 + random.randint(0, 300)

        return {
            "success": True,
            "type": "CarRental",
            "destination": destination,
            "company": company,
            "car_type": car_type,
            "price_per_day": price_per_day,
            "days": days,
            "total_price": price_per_day * days,
            "includes": ["保险", "不限里程", "24小时救援"],
            "pickup": f"{destination}机场店",
            "return": f"{destination}机场店",
            "generated_at": datetime.now().isoformat(),
        }








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
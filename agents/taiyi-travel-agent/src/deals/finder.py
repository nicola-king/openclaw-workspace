#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 优惠发现器

功能:
1. 机票优惠扫描
2. 酒店优惠扫描
3. 套餐折扣发现
4. 价格趋势分析

作者：太一 AGI
版本：2.0.0
"""

import random
from typing import Dict, List, Any
from datetime import datetime, timedelta


class DealsFinder:
    """优惠发现器"""

    # 热门目的地基准价格
    BASE_PRICES: Dict[str, Dict[str, int]] = {
        "东京": {"flight": 2500, "hotel": 600, "package_discount": 0.15},
        "首尔": {"flight": 1800, "hotel": 400, "package_discount": 0.12},
        "曼谷": {"flight": 1500, "hotel": 300, "package_discount": 0.18},
        "新加坡": {"flight": 2200, "hotel": 500, "package_discount": 0.10},
        "巴厘岛": {"flight": 3000, "hotel": 350, "package_discount": 0.20},
        "大阪": {"flight": 2600, "hotel": 550, "package_discount": 0.15},
        "京都": {"flight": 2600, "hotel": 500, "package_discount": 0.14},
        "普吉岛": {"flight": 2800, "hotel": 320, "package_discount": 0.18},
    }

    def find_deals(
        self,
        origin: str,
        flexible: bool = True,
        max_results: int = 5,
    ) -> Dict[str, Any]:
        """
        查找优惠旅行方案

        Args:
            origin: 出发地
            flexible: 日期/目的地是否灵活
            max_results: 最大返回结果数

        Returns:
            优惠方案列表
        """
        destinations = list(self.BASE_PRICES.keys())
        deals = []

        for dest in destinations:
            base = self.BASE_PRICES[dest]
            # 模拟浮动价格
            flight_var = random.randint(-300, 300)
            hotel_var = random.randint(-100, 100)

            deal = {
                "destination": dest,
                "flight_price": max(500, base["flight"] + flight_var),
                "hotel_price_per_night": max(200, base["hotel"] + hotel_var),
                "package_discount": f"{int(base['package_discount'] * 100)}%",
                "valid_until": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "flexible_discount": "额外 5% (灵活日期)" if flexible else None,
            }
            deals.append(deal)

        # 按价格排序
        deals.sort(key=lambda x: x["flight_price"])

        result = {
            "success": True,
            "type": "TravelDeals",
            "origin": origin,
            "deals": deals[:max_results],
            "total_found": len(deals),
            "generated_at": datetime.now().isoformat(),
        }

        return result








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 多城路线优化器 (TSP/VRP)

功能:
1. 多城市路线优化
2. 最短路径计算
3. 预算分配优化
4. 时间约束规划

作者：太一 AGI
版本：2.0.0
"""

import itertools
from typing import Dict, List, Any
from datetime import datetime


class RouteOptimizer:
    """多城市路线优化器"""

    # 城市间距离矩阵（简化版，单位：km）
    DISTANCE_MATRIX: Dict[str, Dict[str, int]] = {
        "北京": {"上海": 1200, "东京": 2100, "首尔": 950, "曼谷": 3300},
        "上海": {"北京": 1200, "东京": 1800, "首尔": 830, "曼谷": 3000},
        "东京": {"北京": 2100, "上海": 1800, "首尔": 1160, "曼谷": 4600},
        "首尔": {"北京": 950, "上海": 830, "东京": 1160, "曼谷": 3800},
        "曼谷": {"北京": 3300, "上海": 3000, "东京": 4600, "首尔": 3800},
    }

    def optimize(
        self,
        cities: List[str],
        budget: float = 20000,
        max_days: int = 14,
    ) -> Dict[str, Any]:
        """
        优化多城市路线

        Args:
            cities: 城市列表
            budget: 总预算
            max_days: 最大天数

        Returns:
            优化结果
        """
        if len(cities) < 2:
            return {"error": "至少需要 2 个城市", "success": False}

        # 计算所有排列的总距离
        best_route = None
        best_distance = float("inf")

        for perm in itertools.permutations(cities):
            distance = self._calc_route_distance(list(perm))
            if distance < best_distance:
                best_distance = distance
                best_route = list(perm)

        # 预算分配
        per_city_budget = budget // len(cities)
        city_suggestions = []
        for city in best_route:
            city_suggestions.append({
                "city": city,
                "days_recommended": max(2, max_days // len(cities)),
                "budget": per_city_budget,
                "highlights": self._get_highlights(city),
            })

        result = {
            "success": True,
            "type": "MultiCityRoute",
            "optimized_route": best_route,
            "total_distance_km": best_distance,
            "city_suggestions": city_suggestions,
            "total_budget": budget,
            "per_city_budget": per_city_budget,
            "generated_at": datetime.now().isoformat(),
        }

        return result

    def _calc_route_distance(self, route: List[str]) -> int:
        """计算路线总距离"""
        total = 0
        for i in range(len(route) - 1):
            from_city = route[i]
            to_city = route[i + 1]
            matrix = self.DISTANCE_MATRIX.get(from_city, {})
            total += matrix.get(to_city, 2000)  # 默认 2000km
        return total

    def _get_highlights(self, city: str) -> List[str]:
        """获取城市亮点"""
        highlights_map = {
            "北京": ["故宫", "长城", "颐和园"],
            "上海": ["外滩", "迪士尼", "东方明珠"],
            "东京": ["东京塔", "浅草寺", "涩谷"],
            "首尔": ["景福宫", "南山塔", "明洞"],
            "曼谷": ["大皇宫", "卧佛寺", "考山路"],
        }
        return highlights_map.get(city, [f"{city}景点 A", f"{city}景点 B"])








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
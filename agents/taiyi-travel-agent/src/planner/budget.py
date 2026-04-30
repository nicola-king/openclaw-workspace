#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 预算管理模块
"""

from typing import Dict, Any


class BudgetAllocator:
    """预算分配器"""

    # 默认预算分配比例
    DEFAULT_RATIOS = {
        "flights": 0.30,
        "accommodation": 0.30,
        "meals": 0.15,
        "activities": 0.10,
        "shopping": 0.10,
        "transport": 0.05,
    }

    def allocate(self, total: float, travelers: int, destination: str = "") -> Dict[str, Any]:
        """
        分配预算

        Args:
            total: 总预算
            travelers: 人数
            destination: 目的地（用于智能调整）

        Returns:
            预算分配字典
        """
        ratios = dict(self.DEFAULT_RATIOS)

        # 根据目的地智能调整
        if any(c in destination for c in ["日本", "东京", "大阪", "京都"]):
            ratios["flights"] = 0.25
            ratios["accommodation"] = 0.35
        elif any(c in destination for c in ["泰国", "曼谷", "普吉", "清迈"]):
            ratios["meals"] = 0.20
            ratios["activities"] = 0.15

        allocation = {}
        remaining = total
        keys = list(ratios.keys())
        for i, key in enumerate(keys):
            if i == len(keys) - 1:
                allocation[key] = int(remaining)
            else:
                val = int(total * ratios[key])
                allocation[key] = val
                remaining -= val

        return allocation








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
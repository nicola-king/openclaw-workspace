#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 置信度评估
"""

from typing import Dict, Any


class ConfidenceScorer:
    """置信度评估器"""

    # 信息源权重
    SOURCE_WEIGHTS = {
        "马蜂窝": 0.15,
        "穷游网": 0.12,
        "携程旅行": 0.15,
        "小红书": 0.10,
        "知乎": 0.08,
        "TripAdvisor": 0.15,
        "Lonely Planet": 0.10,
        "Booking.com": 0.08,
        "Airbnb": 0.07,
    }

    def calculate(
        self,
        sources_used: int,
        data_consistency: float,
        recency_score: float,
    ) -> float:
        """
        计算置信度

        Args:
            sources_used: 使用的信息源数量
            data_consistency: 数据一致性 (0-1)
            recency_score: 数据新鲜度 (0-1)

        Returns:
            置信度分数 (0-1)
        """
        source_factor = min(sources_used / 9.0, 1.0) * 0.4
        consistency_factor = data_consistency * 0.4
        recency_factor = recency_score * 0.2

        confidence = source_factor + consistency_factor + recency_factor
        return round(min(max(confidence, 0.0), 1.0), 3)

    def evaluate(self, fused_data: Dict) -> float:
        """评估融合数据的置信度"""
        sources = fused_data.get("sources_used", 5)
        consistency = fused_data.get("consistency", 0.8)
        recency = fused_data.get("recency", 0.9)
        return self.calculate(sources, consistency, recency)








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 自动优化器 (Auto Optimizer)

根据模式识别结果自动调整推荐权重
"""

from typing import Dict, List, Any
from datetime import datetime

from src.evolve.experience_store import ExperienceStore
from src.evolve.pattern_recognition import PatternRecognition


class AutoOptimizer:
    """自动优化器"""

    def __init__(self, store: ExperienceStore = None):
        self.store = store or ExperienceStore()
        self.pattern_rec = PatternRecognition(self.store)

    def optimize_recommendations(self) -> Dict[str, Any]:
        """
        优化推荐算法

        Returns:
            优化结果
        """
        patterns = self.pattern_rec.analyze_all()

        # 基于模式生成推荐分数
        recommendations = []

        # 热门目的地 + 高评分 = 高推荐
        popularity = {p["destination"]: p["count"] for p in patterns.get("destination_popularity", [])}
        ratings = {p["destination"]: p["avg_rating"] for p in patterns.get("rating_patterns", [])}
        budgets = {p["destination"]: p["avg_budget"] for p in patterns.get("budget_patterns", [])}

        all_destinations = set(popularity.keys()) | set(ratings.keys()) | set(budgets.keys())

        for dest in all_destinations:
            pop_score = min(popularity.get(dest, 0) * 10, 40)
            rating_score = (ratings.get(dest, 0) / 5.0) * 40
            budget_score = 20  # 默认预算分

            total_score = pop_score + rating_score + budget_score
            recommendations.append({
                "destination": dest,
                "score": round(total_score, 1),
                "popularity": popularity.get(dest, 0),
                "avg_rating": ratings.get(dest, 0),
                "avg_budget": budgets.get(dest, 0),
            })

        recommendations.sort(key=lambda x: x["score"], reverse=True)

        result = {
            "success": True,
            "type": "RecommendationOptimization",
            "recommendations": recommendations[:10],
            "patterns_analyzed": {
                "popularity": len(patterns.get("destination_popularity", [])),
                "budget": len(patterns.get("budget_patterns", [])),
                "seasonal": len(patterns.get("seasonal_patterns", [])),
                "rating": len(patterns.get("rating_patterns", [])),
            },
            "optimized_at": datetime.now().isoformat(),
        }

        return result

    def get_optimized_destinations(self, top_n: int = 5) -> List[str]:
        """获取优化后的推荐目的地列表"""
        result = self.optimize_recommendations()
        return [r["destination"] for r in result["recommendations"][:top_n]]








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
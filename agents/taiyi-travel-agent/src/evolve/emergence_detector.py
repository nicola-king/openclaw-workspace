#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 涌现检测器 (Emergence Detector)

检测能力涌现信号：
1. 目的地请求频率 > 阈值 → 创建新目的地模块
2. 预算模式异常 → 创建预算优化技能
3. 高评分目的地 → 创建推荐技能
4. 新功能需求积累 → 创建新模块
"""

from typing import Dict, List, Any
from datetime import datetime

from src.evolve.experience_store import ExperienceStore


class EmergenceDetector:
    """涌现检测器"""

    # 涌现阈值配置
    THRESHOLDS = {
        "destination_request_count": 3,  # 目的地请求次数阈值
        "budget_variance_ratio": 0.5,    # 预算方差比率阈值
        "high_rating_threshold": 4.5,    # 高评分阈值
        "feedback_count_threshold": 5,   # 反馈数量阈值
    }

    def __init__(self, store: ExperienceStore = None):
        self.store = store or ExperienceStore()

    def detect_all(self) -> List[Dict[str, Any]]:
        """执行全量涌现检测"""
        signals = []
        signals.extend(self._detect_destination_emergence())
        signals.extend(self._detect_budget_anomaly())
        signals.extend(self._detect_high_rating_emergence())
        signals.extend(self._detect_feedback_emergence())
        return signals

    def _detect_destination_emergence(self) -> List[Dict]:
        """检测目的地涌现：请求频率超过阈值"""
        signals = []
        destinations = self.store.get_destinations()

        for dest in destinations:
            count = self.store.get_destination_count(dest)
            if count >= self.THRESHOLDS["destination_request_count"]:
                signals.append({
                    "type": "DestinationEmergence",
                    "destination": dest,
                    "count": count,
                    "threshold": self.THRESHOLDS["destination_request_count"],
                    "priority": "P1",
                    "reason": f"{dest} 出现 {count} 次 (阈值 {self.THRESHOLDS['destination_request_count']})，建议创建专门目的地模块",
                    "suggested_action": f"create_destination_module:{dest}",
                    "detected_at": datetime.now().isoformat(),
                })
        return signals

    def _detect_budget_anomaly(self) -> List[Dict]:
        """检测预算异常：方差过大"""
        signals = []
        destinations = self.store.get_destinations()

        for dest in destinations:
            trips = self.store.get_trips(destination=dest, limit=100)
            if len(trips) >= 5:
                budgets = [t["budget"] for t in trips]
                avg = sum(budgets) / len(budgets)
                variance = sum((b - avg) ** 2 for b in budgets) / len(budgets)

                if avg > 0 and (variance / avg) > self.THRESHOLDS["budget_variance_ratio"]:
                    signals.append({
                        "type": "BudgetAnomaly",
                        "destination": dest,
                        "avg_budget": round(avg, 0),
                        "variance": round(variance, 0),
                        "priority": "P2",
                        "reason": f"{dest} 预算波动大 (方差/均值={variance/avg:.2f})，建议创建预算优化技能",
                        "suggested_action": f"create_budget_optimizer:{dest}",
                        "detected_at": datetime.now().isoformat(),
                    })
        return signals

    def _detect_high_rating_emergence(self) -> List[Dict]:
        """检测高评分涌现"""
        signals = []
        destinations = self.store.get_destinations()

        for dest in destinations:
            avg_rating = self.store.get_avg_rating(dest)
            if avg_rating >= self.THRESHOLDS["high_rating_threshold"]:
                signals.append({
                    "type": "HighRatingEmergence",
                    "destination": dest,
                    "avg_rating": round(avg_rating, 2),
                    "priority": "P2",
                    "reason": f"{dest} 评分高 ({avg_rating:.1f}/5.0)，建议创建推荐技能",
                    "suggested_action": f"create_recommender:{dest}",
                    "detected_at": datetime.now().isoformat(),
                })
        return signals

    def _detect_feedback_emergence(self) -> List[Dict]:
        """检测反馈涌现：大量反馈需要新处理能力"""
        signals = []
        trips = self.store.get_trips(limit=1000)
        feedback_trips = [t for t in trips if t.get("feedback", "")]

        if len(feedback_trips) >= self.THRESHOLDS["feedback_count_threshold"]:
            signals.append({
                "type": "FeedbackVolume",
                "count": len(feedback_trips),
                "priority": "P2",
                "reason": f"积累了 {len(feedback_trips)} 条反馈，建议创建反馈分析技能",
                "suggested_action": "create_feedback_analyzer",
                "detected_at": datetime.now().isoformat(),
            })
        return signals

    def get_summary(self) -> Dict[str, Any]:
        """获取涌现检测摘要"""
        signals = self.detect_all()
        return {
            "total_signals": len(signals),
            "p1_signals": len([s for s in signals if s["priority"] == "P1"]),
            "p2_signals": len([s for s in signals if s["priority"] == "P2"]),
            "signals": signals,
            "checked_at": datetime.now().isoformat(),
        }








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
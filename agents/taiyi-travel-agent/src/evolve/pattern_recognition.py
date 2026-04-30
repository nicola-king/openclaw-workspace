#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 模式识别 (Pattern Recognition)

分析历史经验，发现规律：
- "XX 季节去 XX 预算最优"
- "XX 目的地评分最高"
- "XX 预算区间最受欢迎"
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from collections import Counter

from src.evolve.experience_store import ExperienceStore


class PatternRecognition:
    """模式识别引擎"""

    def __init__(self, store: Optional[ExperienceStore] = None):
        self.store = store or ExperienceStore()
        self.patterns_file = self.store.data_dir / "patterns.json"

    def analyze_all(self) -> Dict[str, Any]:
        """执行全量模式分析"""
        patterns = {
            "destination_popularity": self._detect_popularity(),
            "budget_patterns": self._detect_budget_patterns(),
            "seasonal_patterns": self._detect_seasonal_patterns(),
            "rating_patterns": self._detect_rating_patterns(),
            "traveler_patterns": self._detect_traveler_patterns(),
        }
        self._save_patterns(patterns)
        return patterns

    def _detect_popularity(self) -> List[Dict]:
        """检测热门目的地模式"""
        trips = self.store.get_trips(limit=1000)
        dest_counts = Counter(t["destination"] for t in trips)
        return [
            {"destination": d, "count": c, "rank": i + 1}
            for i, (d, c) in enumerate(dest_counts.most_common(10))
        ]

    def _detect_budget_patterns(self) -> List[Dict]:
        """检测预算模式"""
        trips = self.store.get_trips(limit=1000)
        dest_budgets: Dict[str, List[float]] = {}
        for t in trips:
            dest_budgets.setdefault(t["destination"], []).append(t["budget"])

        patterns = []
        for dest, budgets in dest_budgets.items():
            if len(budgets) >= 2:
                avg = sum(budgets) / len(budgets)
                patterns.append({
                    "destination": dest,
                    "avg_budget": round(avg, 0),
                    "min_budget": min(budgets),
                    "max_budget": max(budgets),
                    "sample_size": len(budgets),
                    "pattern": f"{dest} 平均预算 ¥{avg:.0f}",
                })
        return patterns

    def _detect_seasonal_patterns(self) -> List[Dict]:
        """检测季节性模式"""
        trips = self.store.get_trips(limit=1000)
        dest_season_budgets: Dict[str, Dict[str, List[float]]] = {}

        for t in trips:
            start = t.get("start_date", "")
            if start:
                try:
                    month = int(start.split("-")[1])
                    if month in (3, 4, 5):
                        season = "春"
                    elif month in (6, 7, 8):
                        season = "夏"
                    elif month in (9, 10, 11):
                        season = "秋"
                    else:
                        season = "冬"
                except (ValueError, IndexError):
                    season = "未知"
            else:
                season = "未知"

            dest_season_budgets.setdefault(t["destination"], {}).setdefault(season, []).append(t["budget"])

        patterns = []
        for dest, seasons in dest_season_budgets.items():
            for season, budgets in seasons.items():
                if len(budgets) >= 2:
                    avg = sum(budgets) / len(budgets)
                    patterns.append({
                        "destination": dest,
                        "season": season,
                        "avg_budget": round(avg, 0),
                        "sample_size": len(budgets),
                        "pattern": f"{season}季去{dest}平均预算 ¥{avg:.0f}",
                    })
        return patterns

    def _detect_rating_patterns(self) -> List[Dict]:
        """检测评分模式"""
        trips = self.store.get_trips(limit=1000)
        dest_ratings: Dict[str, List[float]] = {}
        for t in trips:
            if t.get("rating", 0) > 0:
                dest_ratings.setdefault(t["destination"], []).append(t["rating"])

        patterns = []
        for dest, ratings in dest_ratings.items():
            if len(ratings) >= 2:
                avg = sum(ratings) / len(ratings)
                patterns.append({
                    "destination": dest,
                    "avg_rating": round(avg, 2),
                    "sample_size": len(ratings),
                    "pattern": f"{dest} 平均评分 {avg:.1f}/5.0",
                })
        patterns.sort(key=lambda x: x["avg_rating"], reverse=True)
        return patterns

    def _detect_traveler_patterns(self) -> List[Dict]:
        """检测旅行者模式"""
        trips = self.store.get_trips(limit=1000)
        group_sizes: Dict[int, List[float]] = {}
        for t in trips:
            travelers = t.get("travelers", 1)
            group_sizes.setdefault(travelers, []).append(t["budget"])

        patterns = []
        for size, budgets in group_sizes.items():
            if len(budgets) >= 2:
                avg = sum(budgets) / len(budgets)
                patterns.append({
                    "group_size": size,
                    "avg_budget": round(avg, 0),
                    "sample_size": len(budgets),
                    "pattern": f"{size}人团平均预算 ¥{avg:.0f}",
                })
        return patterns

    def _save_patterns(self, patterns: Dict) -> None:
        """保存模式数据"""
        patterns["_updated_at"] = datetime.now().isoformat()
        with open(self.patterns_file, "w", encoding="utf-8") as f:
            json.dump(patterns, f, indent=2, ensure_ascii=False)

    def get_patterns(self) -> Dict:
        """加载已保存的模式"""
        if self.patterns_file.exists():
            with open(self.patterns_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
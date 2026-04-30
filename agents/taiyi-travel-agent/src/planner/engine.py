#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 核心规划引擎

功能:
1. 智能旅行规划
2. 航班/酒店查询
3. 预算管理
4. 景点推荐
5. 旅行清单生成
6. 天气查询
7. 多平台推送

作者：太一 AGI
版本：2.0.0
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

from src.planner.budget import BudgetAllocator
from src.planner.checklist import ChecklistGenerator
from src.planner.weather import WeatherService


class PlannerEngine:
    """太一旅行核心规划引擎"""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).parent.parent.parent / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.budget_allocator = BudgetAllocator()
        self.checklist_gen = ChecklistGenerator()
        self.weather = WeatherService()

    def plan_trip(
        self,
        origin: str,
        destination: str,
        start_date: str,
        end_date: str,
        budget: float = 10000,
        travelers: int = 1,
        need_car_rental: bool = False,
        need_local_guide: bool = False,
    ) -> Dict[str, Any]:
        """
        智能旅行规划

        Args:
            origin: 出发地
            destination: 目的地
            start_date: 出发日期 (YYYY-MM-DD)
            end_date: 返回日期 (YYYY-MM-DD)
            budget: 总预算
            travelers: 人数
            need_car_rental: 是否需要租车
            need_local_guide: 是否需要地陪

        Returns:
            旅行计划
        """
        # 预算分配
        budget_allocation = self.budget_allocator.allocate(
            total=budget, travelers=travelers, destination=destination
        )

        # 旅行清单
        days = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days + 1
        checklist = self.checklist_gen.generate(destination, days)

        # 天气
        weather = self.weather.query(destination)

        trip_plan = {
            "type": "TripPlan",
            "origin": origin,
            "destination": destination,
            "dates": {"start": start_date, "end": end_date},
            "travelers": travelers,
            "budget": {"total": budget, "allocation": budget_allocation},
            "checklist": checklist,
            "weather": weather,
            "needs": {
                "car_rental": need_car_rental,
                "local_guide": need_local_guide,
            },
            "generated_at": datetime.now().isoformat(),
        }

        self._save_plan(trip_plan, f"{destination}_{start_date}")
        return trip_plan

    def generate_checklist(self, destination: str, days: int, purpose: str = "休闲") -> Dict:
        """生成旅行清单"""
        return self.checklist_gen.generate(destination, days, purpose)

    def _save_plan(self, plan: Dict, name: str) -> Path:
        """保存旅行计划"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.data_dir / f"{name}_{timestamp}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        return output_file








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
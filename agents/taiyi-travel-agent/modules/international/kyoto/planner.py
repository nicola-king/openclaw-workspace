#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
京都模块 - 旅行规划器

功能:
1. 京都旅行规划
2. 预算分配
3. 旅行清单生成

作者：太一 AGI
创建：2026-04-24
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class KyotoPlanner:
    """京都旅行规划器"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            self.data_dir = Path(__file__).parent.parent.parent.parent / "data"
        else:
            self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        print(f"⛩️ 京都规划器启动")
    
    def plan_trip(self, origin: str, destination: str = "京都",
                 start_date: str = "2026-05-01", end_date: str = "2026-05-07",
                 budget: float = 12000, travelers: int = 1,
                 preferences: Optional[List[str]] = None) -> Dict:
        print(f"⛩️ 京都行程规划：{origin} → {destination}")
        
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days = (end - start).days + 1
        
        if preferences is None:
            preferences = ["历史文化", "自然风光", "文化体验"]
        
        budget_allocation = {
            "航班": round(budget * 0.30, 2),
            "住宿": round(budget * 0.25, 2),
            "餐饮": round(budget * 0.20, 2),
            "活动": round(budget * 0.15, 2),
            "购物": round(budget * 0.10, 2),
        }
        
        attractions = {
            "历史文化": [
                {"name": "金阁寺", "duration": "1.5h", "cost": 400},
                {"name": "清水寺", "duration": "2h", "cost": 0},
                {"name": "伏见稻荷大社", "duration": "2h", "cost": 0},
                {"name": "二条城", "duration": "2h", "cost": 600},
            ],
            "自然风光": [
                {"name": "岚山竹林", "duration": "2h", "cost": 0},
                {"name": "哲学之道", "duration": "1.5h", "cost": 0},
            ],
            "文化体验": [
                {"name": "祇园", "duration": "2h", "cost": 0},
                {"name": "花见小路", "duration": "1h", "cost": 0},
            ],
        }
        
        itinerary = []
        for day in range(1, days + 1):
            daily_attractions = []
            for pref in preferences:
                if pref in attractions:
                    daily_attractions.extend(attractions[pref][:2])
            
            day_plan = {
                "day": day,
                "date": (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=day-1)).strftime("%Y-%m-%d"),
                "attractions": daily_attractions[:3],
                "meal_breakfast": "酒店早餐/抹茶早餐",
                "meal_lunch": "怀石料理",
                "meal_dinner": "汤豆腐/京料理",
            }
            itinerary.append(day_plan)
        
        result = {
            "type": "Kyoto Travel Plan",
            "origin": origin,
            "destination": destination,
            "start_date": start_date,
            "end_date": end_date,
            "days": days,
            "travelers": travelers,
            "mode": "跨国游",
            "budget": budget,
            "budget_per_person": budget / travelers,
            "budget_allocation": budget_allocation,
            "preferences": preferences,
            "daily_itinerary": itinerary,
            "timestamp": datetime.now().isoformat(),
        }
        
        print(f"  ✅ 行程规划完成：{days} 天，预算 ¥{budget}")
        return result
    
    def save_plan(self, plan: Dict, filename: str) -> Path:
        output_file = self.data_dir / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        print(f"✅ 行程已保存：{output_file}")
        return output_file


def main():
    print("=" * 60)
    print("⛩️ 京都规划器测试")
    print("=" * 60)
    
    planner = KyotoPlanner()
    plan = planner.plan_trip("北京", "京都", "2026-05-01", "2026-05-07", budget=12000, travelers=2)
    planner.save_plan(plan, "kyoto_plan")
    
    print("\n" + "=" * 60)
    print("✅ 京都规划器测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()

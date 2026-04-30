#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
巴厘岛模块 - 旅行规划器

功能:
1. 巴厘岛旅行规划
2. 预算分配
3. 旅行清单生成

作者：太一 AGI
创建：2026-04-24
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class BaliPlanner:
    """巴厘岛旅行规划器"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            self.data_dir = Path(__file__).parent.parent.parent.parent / "data"
        else:
            self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        print(f"🌺 巴厘岛规划器启动")
    
    def plan_trip(self, origin: str, destination: str = "巴厘岛",
                 start_date: str = "2026-05-01", end_date: str = "2026-05-07",
                 budget: float = 10000, travelers: int = 1,
                 preferences: Optional[List[str]] = None) -> Dict:
        print(f"🌺 巴厘岛行程规划：{origin} → {destination}")
        
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days = (end - start).days + 1
        
        if preferences is None:
            preferences = ["自然风光", "文化体验", "美食"]
        
        budget_allocation = {
            "航班": round(budget * 0.30, 2),
            "住宿": round(budget * 0.25, 2),
            "餐饮": round(budget * 0.20, 2),
            "活动": round(budget * 0.15, 2),
            "购物": round(budget * 0.10, 2),
        }
        
        attractions = {
            "自然风光": [
                {"name": "库塔海滩", "duration": "1d", "cost": 0},
                {"name": "德格拉朗梯田", "duration": "2h", "cost": 20000},
                {"name": "海神庙", "duration": "2h", "cost": 50000},
            ],
            "文化体验": [
                {"name": "乌布皇宫", "duration": "1.5h", "cost": 30000},
                {"name": "圣泉寺", "duration": "2h", "cost": 30000},
                {"name": "乌布市场", "duration": "2h", "cost": 0},
            ],
            "美食": [
                {"name": "水明漾", "duration": "3h", "cost": 100000},
                {"name": "金巴伦海滩", "duration": "2h", "cost": 150000},
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
                "meal_breakfast": "酒店早餐/印尼早餐",
                "meal_lunch": "印尼炒饭",
                "meal_dinner": "烤乳猪",
            }
            itinerary.append(day_plan)
        
        result = {
            "type": "Bali Travel Plan",
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
    print("🌺 巴厘岛规划器测试")
    print("=" * 60)
    
    planner = BaliPlanner()
    plan = planner.plan_trip("北京", "巴厘岛", "2026-05-01", "2026-05-07", budget=10000, travelers=2)
    planner.save_plan(plan, "bali_plan")
    
    print("\n" + "=" * 60)
    print("✅ 巴厘岛规划器测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()

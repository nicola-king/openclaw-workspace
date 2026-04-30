#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北京模块 - 旅行规划器

功能:
1. 北京旅行规划
2. 预算分配
3. 旅行清单生成
4. 酒店/包车/导游搜索

作者：太一 AGI
创建：2026-04-24
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class BeijingPlanner:
    """北京旅行规划器"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        初始化北京规划器
        
        Args:
            data_dir: 数据目录
        """
        if data_dir is None:
            self.data_dir = Path(__file__).parent.parent.parent.parent / "data"
        else:
            self.data_dir = data_dir
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
        print(f"🏛️ 北京规划器启动")
        print(f"  数据目录：{self.data_dir}")
    
    # ========== 1. 智能行程规划 ==========
    
    def plan_trip(self, origin: str, destination: str = "北京",
                 start_date: str = "2026-05-01", end_date: str = "2026-05-05",
                 budget: float = 5000, travelers: int = 1,
                 preferences: Optional[List[str]] = None) -> Dict:
        """
        智能行程规划
        
        Args:
            origin: 出发地
            destination: 目的地 (默认北京)
            start_date: 出发日期
            end_date: 返回日期
            budget: 预算
            travelers: 人数
            preferences: 偏好
        
        Returns:
            行程规划
        """
        print(f"🏛️ 北京行程规划：{origin} → {destination}")
        
        # 计算天数
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days = (end - start).days + 1
        
        # 默认偏好
        if preferences is None:
            preferences = ["历史文化", "美食", "购物"]
        
        # 预算分配
        budget_allocation = self._allocate_budget(budget, travelers, days)
        
        # 生成每日行程
        daily_itinerary = self._generate_daily_itinerary(days, preferences)
        
        # 生成旅行清单
        packing_list = self._generate_packing_list()
        
        result = {
            "type": "Beijing Travel Plan",
            "origin": origin,
            "destination": destination,
            "start_date": start_date,
            "end_date": end_date,
            "days": days,
            "travelers": travelers,
            "mode": "国内游",
            "budget": budget,
            "budget_per_person": budget / travelers,
            "budget_allocation": budget_allocation,
            "preferences": preferences,
            "daily_itinerary": daily_itinerary,
            "packing_list": packing_list,
            "timestamp": datetime.now().isoformat(),
        }
        
        print(f"  ✅ 行程规划完成：{days} 天，预算 ¥{budget}")
        return result
    
    # ========== 2. 预算分配 ==========
    
    def _allocate_budget(self, budget: float, travelers: int, days: int) -> Dict:
        """
        预算分配
        
        Args:
            budget: 总预算
            travelers: 人数
            days: 天数
        
        Returns:
            预算分配
        """
        allocation = {
            "交通": round(budget * 0.25, 2),
            "住宿": round(budget * 0.30, 2),
            "餐饮": round(budget * 0.20, 2),
            "活动": round(budget * 0.15, 2),
            "购物": round(budget * 0.10, 2),
        }
        
        return allocation
    
    # ========== 3. 每日行程生成 ==========
    
    def _generate_daily_itinerary(self, days: int, preferences: List[str]) -> List[Dict]:
        """
        生成每日行程
        
        Args:
            days: 天数
            preferences: 偏好
        
        Returns:
            每日行程
        """
        # 北京景点库
        attractions = {
            "历史文化": [
                {"name": "故宫", "duration": "3h", "cost": 60},
                {"name": "长城", "duration": "1d", "cost": 40},
                {"name": "天坛", "duration": "2h", "cost": 15},
                {"name": "颐和园", "duration": "3h", "cost": 30},
                {"name": "圆明园", "duration": "2h", "cost": 10},
            ],
            "美食": [
                {"name": "全聚德烤鸭", "duration": "1.5h", "cost": 200},
                {"name": "东来顺涮羊肉", "duration": "1.5h", "cost": 150},
                {"name": "王府井小吃街", "duration": "2h", "cost": 100},
            ],
            "购物": [
                {"name": "王府井大街", "duration": "3h", "cost": 0},
                {"name": "西单商场", "duration": "3h", "cost": 0},
                {"name": "三里屯", "duration": "3h", "cost": 0},
            ],
            "文化体验": [
                {"name": "南锣鼓巷", "duration": "2h", "cost": 0},
                {"name": "什刹海", "duration": "2h", "cost": 0},
                {"name": "798 艺术区", "duration": "3h", "cost": 0},
            ],
        }
        
        # 生成每日行程
        itinerary = []
        for day in range(1, days + 1):
            # 每天选择 2-3 个景点
            daily_attractions = []
            for pref in preferences:
                if pref in attractions:
                    daily_attractions.extend(attractions[pref][:2])
            
            day_plan = {
                "day": day,
                "date": (datetime.strptime("2026-05-01", "%Y-%m-%d") + timedelta(days=day-1)).strftime("%Y-%m-%d"),
                "attractions": daily_attractions[:3],
                "meal_breakfast": "酒店早餐/豆汁焦圈",
                "meal_lunch": "北京烤鸭/涮羊肉",
                "meal_dinner": "王府井小吃街",
            }
            itinerary.append(day_plan)
        
        return itinerary
    
    # ========== 4. 旅行清单生成 ==========
    
    def _generate_packing_list(self) -> Dict:
        """
        生成旅行清单
        
        Returns:
            旅行清单
        """
        return {
            "证件类": ["身份证", "学生证 (优惠)", "军官证 (优惠)"],
            "电子类": ["手机", "充电器", "充电宝", "相机"],
            "衣物类": ["换洗衣物", "舒适的鞋", "外套 (春秋)"],
            "洗漱类": ["牙刷", "牙膏", "毛巾", "护肤品"],
            "其他": ["防晒用品", "雨具", "水壶"],
        }
    
    # ========== 5. 保存行程 ==========
    
    def save_plan(self, plan: Dict, filename: str) -> Path:
        """
        保存行程到文件
        
        Args:
            plan: 行程规划
            filename: 文件名
        
        Returns:
            文件路径
        """
        output_file = self.data_dir / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 行程已保存：{output_file}")
        return output_file


def main():
    """测试"""
    print("=" * 60)
    print("🏛️ 北京规划器测试")
    print("=" * 60)
    
    planner = BeijingPlanner()
    
    # 测试 1: 智能行程规划
    print("\n🏛️ 测试 1: 智能行程规划")
    plan = planner.plan_trip(
        origin="上海",
        destination="北京",
        start_date="2026-05-01",
        end_date="2026-05-05",
        budget=5000,
        travelers=2,
        preferences=["历史文化", "美食", "购物"]
    )
    planner.save_plan(plan, "beijing_plan")
    
    print("\n" + "=" * 60)
    print("✅ 北京规划器测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()

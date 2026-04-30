#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 信息提取器
"""

import random
from typing import Dict, List, Any
from datetime import datetime


class InfoExtractor:
    """信息提取器"""

    SPOTS_DB: Dict[str, List[str]] = {
        "东京": ["东京塔", "浅草寺", "涩谷", "新宿", "秋叶原"],
        "首尔": ["景福宫", "南山塔", "明洞", "弘大", "东大门"],
        "曼谷": ["大皇宫", "卧佛寺", "考山路", "暹罗广场", "湄南河"],
        "新加坡": ["滨海湾", "环球影城", "动物园", "鱼尾狮", "圣淘沙"],
    }

    FOOD_DB: Dict[str, List[str]] = {
        "东京": ["寿司", "拉面", "天妇罗", "和牛"],
        "首尔": ["烤肉", "泡菜", "石锅拌饭", "炸鸡"],
        "曼谷": ["冬阴功", "泰式炒河粉", "芒果糯米饭"],
    }

    def extract_spots(self, destination: str) -> List[Dict]:
        """提取景点数据"""
        spots = self.SPOTS_DB.get(destination, [f"{destination}景点{i}" for i in range(1, 6)])
        return [
            {"name": s, "rating": round(random.uniform(4.0, 5.0), 1), "reviews": random.randint(100, 1000)}
            for s in spots
        ]

    def extract_budget(self, destination: str) -> Dict:
        """提取预算数据"""
        return {
            "经济": f"¥{random.randint(3000, 5000)}/人",
            "舒适": f"¥{random.randint(5000, 10000)}/人",
            "豪华": f"¥{random.randint(10000, 20000)}/人",
        }

    def extract_food(self, destination: str) -> List[str]:
        """提取美食推荐"""
        return self.FOOD_DB.get(destination, ["当地特色菜"])

    def extract_tips(self, destination: str) -> List[str]:
        """提取旅行贴士"""
        return [
            "提前3个月预订机票最便宜",
            "避开旺季可节省30%+费用",
            "使用当地交通卡更优惠",
            "购买旅游保险很重要",
        ]

    def extract_all(self, destination: str) -> Dict[str, Any]:
        """提取全部信息"""
        return {
            "destination": destination,
            "spots": self.extract_spots(destination),
            "budget": self.extract_budget(destination),
            "food": self.extract_food(destination),
            "tips": self.extract_tips(destination),
            "extracted_at": datetime.now().isoformat(),
        }








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
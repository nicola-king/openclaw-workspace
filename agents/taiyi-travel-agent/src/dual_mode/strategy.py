#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 双模式策略 (国内/跨国)
"""

from typing import Dict, List, Any
from datetime import datetime


class DualModeStrategy:
    """双模式旅游策略"""

    DOMESTIC_DESTINATIONS = {
        "北京": {"type": "历史文化", "days": "4-5天", "season": "9-11月", "budget": "¥3000-5000/人", "highlights": ["故宫", "长城", "颐和园"]},
        "上海": {"type": "现代都市", "days": "3-4天", "season": "3-5月", "budget": "¥4000-6000/人", "highlights": ["外滩", "迪士尼", "东方明珠"]},
        "成都": {"type": "休闲美食", "days": "3-4天", "season": "3-6月", "budget": "¥2500-4000/人", "highlights": ["大熊猫", "宽窄巷子", "火锅"]},
        "西安": {"type": "历史文化", "days": "3-4天", "season": "3-5月", "budget": "¥2500-4000/人", "highlights": ["兵马俑", "大雁塔", "城墙"]},
        "云南": {"type": "自然风光", "days": "6-8天", "season": "10月-次年4月", "budget": "¥4000-7000/人", "highlights": ["丽江", "大理", "香格里拉"]},
    }

    INTERNATIONAL_DESTINATIONS = {
        "日本": {"type": "文化购物", "days": "5-7天", "season": "3-5月/10-11月", "budget": "¥8000-15000/人", "visa": "需要(简化)", "highlights": ["东京", "大阪", "京都"]},
        "韩国": {"type": "购物美食", "days": "4-6天", "season": "4-5月/9-10月", "budget": "¥5000-10000/人", "visa": "济州岛免签", "highlights": ["首尔", "济州岛"]},
        "泰国": {"type": "海岛度假", "days": "5-7天", "season": "11月-次年2月", "budget": "¥4000-8000/人", "visa": "落地签", "highlights": ["曼谷", "普吉岛"]},
        "新加坡": {"type": "城市观光", "days": "3-5天", "season": "全年", "budget": "¥8000-15000/人", "visa": "需要", "highlights": ["滨海湾", "环球影城"]},
    }

    def get_travel_mode(self, origin: str, destination: str) -> str:
        """判断旅游模式"""
        china_cities = ["北京", "上海", "广州", "深圳", "成都", "西安", "杭州", "南京"]
        if any(c in origin for c in china_cities):
            if any(c in destination for c in china_cities) or any(p in destination for p in ["云南", "四川", "陕西", "浙江", "江苏"]):
                return "domestic"
        return "international"

    def get_strategy(self, origin: str, destination: str) -> Dict[str, Any]:
        """获取旅游策略"""
        mode = self.get_travel_mode(origin, destination)
        if mode == "domestic":
            dest_info = self.DOMESTIC_DESTINATIONS.get(destination, {})
            return {
                "mode": "domestic",
                "destination": destination,
                "market": {"language": "中文", "currency": "人民币", "payment": "支付宝/微信", "visa": "无需"},
                "destination_info": dest_info,
                "tips": ["节假日人流量大，建议错峰出行", "热门景点提前网上购票"],
            }
        else:
            dest_info = self.INTERNATIONAL_DESTINATIONS.get(destination, {})
            return {
                "mode": "international",
                "destination": destination,
                "market": {"language": "可能需要翻译", "currency": "需兑换外币", "payment": "信用卡/现金", "visa": dest_info.get("visa", "需确认")},
                "destination_info": dest_info,
                "tips": ["护照有效期6个月以上", "购买旅游保险", "尊重当地文化"],
            }

    def recommend_mode(self, experience: str = "beginner", budget: str = "medium", time: str = "medium") -> str:
        """根据旅行者画像推荐模式"""
        if experience == "beginner" or budget == "low" or time == "short":
            return "domestic"
        elif experience == "advanced" and budget == "high" and time == "long":
            return "international"
        return "depends"








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
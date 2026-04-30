#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 天气服务模块
"""

from typing import Dict, Any


class WeatherService:
    """天气查询服务"""

    # 目的地气候数据（备用，API 不可用时）
    CLIMATE_DATA: Dict[str, Dict] = {
        "东京": {"best_months": "3-5, 10-11", "avg_temp": "5-25°C", "season": "四季分明"},
        "首尔": {"best_months": "4-5, 9-10", "avg_temp": "-5-28°C", "season": "四季分明"},
        "曼谷": {"best_months": "11-2", "avg_temp": "25-35°C", "season": "热带"},
        "新加坡": {"best_months": "全年", "avg_temp": "25-32°C", "season": "热带雨林"},
        "北京": {"best_months": "9-11", "avg_temp": "-5-30°C", "season": "四季分明"},
        "上海": {"best_months": "3-5, 9-11", "avg_temp": "2-28°C", "season": "亚热带"},
    }

    def query(self, destination: str) -> Dict[str, Any]:
        """
        查询天气

        Args:
            destination: 目的地

        Returns:
            天气信息
        """
        climate = self.CLIMATE_DATA.get(destination, {})
        return {
            "destination": destination,
            "best_months": climate.get("best_months", "全年适宜"),
            "avg_temp": climate.get("avg_temp", "未知"),
            "season": climate.get("season", "未知"),
            "note": "如需实时天气，请配置 weatherstack API",
        }








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
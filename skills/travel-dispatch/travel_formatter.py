#!/usr/bin/env python3
"""
travel-formatter v1.0.0
太一旅游探路者 · 输出格式化模板

遵循 RENDERING-PRINCIPLES.md + SESSION-OUTPUT-RULE.md
所有输出转为"人话"，不暴露基础设施细节
"""

import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional


class TravelFormatter:
    """旅游输出格式化器"""

    @staticmethod
    def format_selected(data: Dict[str, Any]) -> str:
        """精选模式 → 人话"""
        city = data.get("city", "").title()
        sections = data.get("sections", [])
        if not sections:
            return f"📍 {city} 暂无推荐数据"

        lines = [f"📍 {city} · 精选推荐", "=" * 30, ""]

        for sec in sections:
            label = sec.get("label", "")
            items = sec.get("items", [])
            if not items:
                continue
            lines.append(f"▸ {label}")
            for i, item in enumerate(items, 1):
                name = item.get("name", "")
                rating = item.get("rating", "")
                price = item.get("price", "")
                extra = ""
                if rating:
                    extra += f" ⭐{rating}"
                if price:
                    extra += f" | {price}"
                lines.append(f"  {i}. {name}{extra}")
            lines.append("")

        total = data.get("total", 0)
        lines.append(f"共 {total} 条推荐 · 数据来源: 太一旅游探路者")
        return "\n".join(lines)

    @staticmethod
    def format_daily(data: Dict[str, Any]) -> str:
        """行程模式 → 人话"""
        city = data.get("city", "").title()
        days = data.get("days", 3)
        budget = data.get("total_budget", 0)
        itinerary = data.get("itinerary", [])
        tips = data.get("tips", [])

        lines = [f"🗺️  {city} {days}日游 · 完整行程", "=" * 35, ""]

        for day in itinerary:
            d = day.get("day", "?")
            date = day.get("date", "")
            weekday = TravelFormatter._weekday(date) if date else ""
            lines.append(f"📅 第{d}天 ({date} {weekday})")
            lines.append("-" * 30)

            for item in day.get("schedule", []):
                time = item.get("time", "")
                activity = item.get("activity", "")
                cost = item.get("cost", 0)
                cost_str = f"¥{cost}" if cost else "免费"
                lines.append(f"  {time}  {activity}  ({cost_str})")

            db = day.get("daily_budget", 0)
            lines.append(f"  本日预算: ¥{db}")
            lines.append("")

        if tips:
            lines.append(f"💡 旅行建议:")
            for tip in tips:
                lines.append(f"  • {tip}")
            lines.append("")

        if budget:
            lines.append(f"总预算: ¥{budget}")
        lines.append("数据来源: 太一旅游探路者")
        return "\n".join(lines)

    @staticmethod
    def format_all(data: Dict[str, Any]) -> str:
        """全量模式 → 人话"""
        city = data.get("city", "").title()
        sections = data.get("sections", [])
        if not sections:
            return f"📍 {city} 暂无数据"

        lines = [f"📍 {city} · 全部信息", "=" * 30, ""]
        for sec in sections:
            label = sec.get("label", "")
            count = sec.get("count", 0)
            items = sec.get("items", [])
            lines.append(f"▸ {label}（共{count}条）")
            for i, item in enumerate(items, 1):
                name = item.get("name", "")
                rating = item.get("rating", "")
                price = item.get("price", "")
                extra = ""
                if rating: extra += f" ⭐{rating}"
                if price: extra += f" | {price}"
                lines.append(f"  {i}. {name}{extra}")
            lines.append("")
        lines.append("数据来源: 太一旅游探路者")
        return "\n".join(lines)

    @staticmethod
    def format_error(data: Dict[str, Any]) -> str:
        """错误 → 人话+建议"""
        error = data.get("error", "未知错误")
        suggestion = data.get("suggestion", "")
        msg = f"⚠️ {error}"
        if suggestion:
            msg += f"\n💡 {suggestion}"
        return msg

    @staticmethod
    def format_bot_dispatch(bot_name: str, role: str, result: str) -> str:
        """单个 Bot 的输出（用于跨域聚合）"""
        return f"[{bot_name} · {role}]\n{result}\n"

    @staticmethod
    def format_full(data: Dict[str, Any]) -> str:
        """自动识别模式并格式化"""
        if data.get("status") == "error":
            return TravelFormatter.format_error(data)
        mode = data.get("mode", "selected")
        if mode == "selected":
            return TravelFormatter.format_selected(data)
        elif mode == "daily":
            return TravelFormatter.format_daily(data)
        elif mode == "all":
            return TravelFormatter.format_all(data)
        else:
            return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def _weekday(date_str: str) -> str:
        try:
            dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
            return ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][dt.weekday()]
        except:
            return ""


# ── 快捷 CLI ──

def main():
    import sys, os
    # Test formatter
    print(TravelFormatter.format_selected({
        "city": "成都", "sections": [
            {"label": "精选景点", "items": [
                {"name": "大熊猫基地", "rating": 4.8, "price": "55元"},
                {"name": "都江堰", "rating": 4.7, "price": "80元"},
            ], "count": 2},
        ], "total": 2
    }))
    print()
    print(TravelFormatter.format_daily({
        "city": "北京", "days": 2, "total_budget": 3000,
        "itinerary": [
            {"day": 1, "date": "2026-05-10", "schedule": [
                {"time": "09:00-12:00", "activity": "参观故宫", "cost": 60},
                {"time": "12:00-13:30", "activity": "午餐", "cost": 80},
            ], "daily_budget": 1500},
        ],
        "tips": ["提前预订门票"]
    }))


if __name__ == "__main__":
    main()

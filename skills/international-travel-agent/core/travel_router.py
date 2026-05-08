#!/usr/bin/env python3
"""
travel-router v1.0.0 — 国际版
太一国际旅游探路者 · 三层路由引擎

国际城市数据：东京/大阪/曼谷/普吉/首尔/新加坡/吉隆坡/纽约/洛杉矶/伦敦/巴黎/罗马/悉尼/奥克兰
"""

import json, logging, re, sys, os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

logger = logging.getLogger("travel-router-intl")

# 国际城市精选数据
TOP_PICKS_INTL = {
    "tokyo": {
        "attractions": [
            {"name": "浅草寺", "rating": 4.7, "price": "免费", "duration": "1.5h", "category": "文化"},
            {"name": "涩谷十字路口", "rating": 4.5, "price": "免费", "duration": "0.5h", "category": "地标"},
            {"name": "秋叶原", "rating": 4.6, "price": "免费", "duration": "2h", "category": "购物"},
            {"name": "新宿御苑", "rating": 4.6, "price": "500日元", "duration": "2h", "category": "自然"},
            {"name": "东京塔", "rating": 4.5, "price": "1200日元", "duration": "1.5h", "category": "地标"},
        ],
        "restaurants": [
            {"name": "数寄屋桥次郎", "rating": 4.9, "price": "¥30000+", "cuisine": "寿司"},
            {"name": "一兰拉面", "rating": 4.4, "price": "¥1000-2000", "cuisine": "拉面"},
            {"name": "筑地市场", "rating": 4.5, "price": "¥2000-5000", "cuisine": "海鲜"},
        ],
        "hotels": [
            {"name": "东京半岛酒店", "rating": 4.9, "price_range": "¥80000+/晚", "location": "丸之内"},
            {"name": "涩谷格兰贝尔", "rating": 4.5, "price_range": "¥20000-40000/晚", "location": "涩谷"},
        ],
    },
    "bangkok": {
        "attractions": [
            {"name": "大皇宫", "rating": 4.7, "price": "500泰铢", "duration": "2h", "category": "文化"},
            {"name": "卧佛寺", "rating": 4.5, "price": "200泰铢", "duration": "1h", "category": "宗教"},
            {"name": "郑王庙", "rating": 4.6, "price": "100泰铢", "duration": "1h", "category": "地标"},
        ],
        "restaurants": [
            {"name": "Jay Fai", "rating": 4.7, "price": "人均1000泰铢", "cuisine": "泰式"},
            {"name": "建兴酒家", "rating": 4.5, "price": "人均500泰铢", "cuisine": "泰式中餐"},
        ],
        "hotels": [
            {"name": "曼谷文华东方", "rating": 4.9, "price_range": "¥3000+/晚", "location": "湄南河畔"},
        ],
    },
    "seoul": {
        "attractions": [
            {"name": "景福宫", "rating": 4.6, "price": "3000韩元", "duration": "2h", "category": "历史"},
            {"name": "明洞", "rating": 4.4, "price": "免费", "duration": "2h", "category": "购物"},
            {"name": "N首尔塔", "rating": 4.5, "price": "12000韩元", "duration": "1.5h", "category": "地标"},
        ],
        "restaurants": [
            {"name": "明洞饺子", "rating": 4.5, "price": "人均10000韩元", "cuisine": "韩式"},
            {"name": "土俗村参鸡汤", "rating": 4.6, "price": "人均15000韩元", "cuisine": "韩定食"},
        ],
        "hotels": [
            {"name": "首尔朝鲜酒店", "rating": 4.8, "price_range": "¥2000+/晚", "location": "明洞"},
        ],
    },
    "singapore": {
        "attractions": [
            {"name": "滨海湾金沙", "rating": 4.7, "price": "免费(外观)", "duration": "1h", "category": "地标"},
            {"name": "圣淘沙岛", "rating": 4.6, "price": "免费上岛", "duration": "4h", "category": "乐园"},
        ],
        "restaurants": [
            {"name": "了凡油鸡饭面", "rating": 4.4, "price": "人均5SGD", "cuisine": "新加坡小贩"},
            {"name": "珍宝海鲜", "rating": 4.6, "price": "人均80SGD", "cuisine": "辣椒螃蟹"},
        ],
        "hotels": [
            {"name": "滨海湾金沙酒店", "rating": 4.8, "price_range": "¥3000+/晚", "location": "滨海湾"},
        ],
    },
    "london": {
        "attractions": [
            {"name": "大英博物馆", "rating": 4.8, "price": "免费", "duration": "3h", "category": "文化"},
            {"name": "伦敦塔桥", "rating": 4.6, "price": "免费(外观)", "duration": "1h", "category": "地标"},
        ],
        "restaurants": [
            {"name": "Dishoom", "rating": 4.6, "price": "人均£20", "cuisine": "印度菜"},
            {"name": "Flat Iron", "rating": 4.5, "price": "人均£12", "cuisine": "牛排"},
        ],
        "hotels": [
            {"name": "伦敦丽兹酒店", "rating": 4.9, "price_range": "£500+/晚", "location": "梅菲尔"},
        ],
    },
    "paris": {
        "attractions": [
            {"name": "埃菲尔铁塔", "rating": 4.7, "price": "€26", "duration": "2h", "category": "地标"},
            {"name": "卢浮宫", "rating": 4.8, "price": "€17", "duration": "3h", "category": "文化"},
        ],
        "restaurants": [
            {"name": "L'Ambroisie", "rating": 4.9, "price": "€300+", "cuisine": "法餐"},
            {"name": "花神咖啡馆", "rating": 4.4, "price": "€10-20", "cuisine": "法式简餐"},
        ],
        "hotels": [
            {"name": "巴黎香格里拉", "rating": 4.9, "price_range": "€1000+/晚", "location": "16区"},
        ],
    },
}


class TravelRouterIntl:
    def __init__(self):
        pass

    def query(self, mode="selected", city="", days=3, budget=5000,
              preferences="综合", category=None, max_items=10) -> Dict[str, Any]:
        mode = mode or "selected"
        city = city.lower()
        logger.info(f"国际路由: mode={mode} city={city}")

        if mode == "selected":
            return self._selected(city, category, max_items)
        elif mode == "daily":
            return self._daily(city, days, budget)
        elif mode == "all":
            return self._all(city, category, max_items)
        else:
            return {"status": "error", "error": f"无效 mode: {mode}"}

    def _selected(self, city, category, max_items):
        picks = TOP_PICKS_INTL.get(city, {})
        if not picks:
            return {"status": "error", "city": city, "suggestion": "试试东京/曼谷/首尔/新加坡/伦敦/巴黎"}
        sections = []
        if not category or category == "attractions":
            items = picks.get("attractions", [])
            sections.append({"label": "精选景点", "items": items[:max_items], "count": len(items)})
        if not category or category == "restaurants":
            items = picks.get("restaurants", [])
            sections.append({"label": "必吃餐厅", "items": items[:max_items], "count": len(items)})
        if not category or category == "hotels":
            items = picks.get("hotels", [])
            sections.append({"label": "推荐住宿", "items": items[:max_items], "count": len(items)})
        return {"mode": "selected", "city": city, "sections": sections,
                "total": sum(s["count"] for s in sections)}

    def _daily(self, city, days, budget):
        picks = TOP_PICKS_INTL.get(city, {})
        itinerary = []
        if picks:
            attractions = picks.get("attractions", [])[:days * 2]
            restaurants = picks.get("restaurants", [])[:days]
            hotels = picks.get("hotels", [])[:1]
            daily_budget = budget / days
            for day in range(1, days + 1):
                plan = {"day": day, "date": (datetime.now() + timedelta(days=day-1)).strftime("%Y-%m-%d"),
                        "schedule": [], "daily_budget": round(daily_budget, 2)}
                if len(attractions) >= day * 2 - 1:
                    a = attractions[day * 2 - 2]
                    plan["schedule"].append({"time": "09:00-12:00", "activity": f"参观 {a['name']}",
                        "cost": re.findall(r'\d+', a.get("price","0"))[0] if re.findall(r'\d+', a.get("price","0")) else 0})
                plan["schedule"].append({"time": "12:00-13:30", "activity": "午餐", "cost": 100})
                if len(attractions) >= day * 2:
                    a = attractions[day * 2 - 1]
                    plan["schedule"].append({"time": "14:00-17:00", "activity": f"参观 {a['name']}",
                        "cost": re.findall(r'\d+', a.get("price","0"))[0] if re.findall(r'\d+', a.get("price","0")) else 0})
                if day <= len(restaurants):
                    r = restaurants[day - 1]
                    plan["schedule"].append({"time": "18:30-20:00", "activity": f"晚餐: {r['name']}",
                        "cost": re.findall(r'\d+', r.get("price","0"))[0] if re.findall(r'\d+', r.get("price","0")) else 100})
                itinerary.append(plan)
        return {"mode": "daily", "city": city, "days": days, "total_budget": budget,
                "itinerary": itinerary, "daily_budget": round(budget/days, 2) if days else 0,
                "tips": ["确认签证有效期", "购买旅行保险", "下载离线地图"]}

    def _all(self, city, category, max_items):
        picks = TOP_PICKS_INTL.get(city, {})
        sections = []
        if not category or category in ["attractions", None]:
            items = picks.get("attractions", [])
            sections.append({"label": "全部景点", "items": items[:max_items], "count": len(items)})
        if not category or category in ["restaurants", None]:
            items = picks.get("restaurants", [])
            sections.append({"label": "全部餐馆", "items": items[:max_items], "count": len(items)})
        if not category or category in ["hotels", None]:
            items = picks.get("hotels", [])
            sections.append({"label": "全部住宿", "items": items[:max_items], "count": len(items)})
        return {"mode": "all", "city": city, "sections": sections, "total": sum(s["count"] for s in sections)}

    def health_check(self) -> Dict[str, Any]:
        return {"module": "travel-router-intl", "version": "1.0.0",
                "status": "active", "cities": list(TOP_PICKS_INTL.keys())}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="selected")
    parser.add_argument("--city", default="")
    parser.add_argument("--days", type=int, default=3)
    parser.add_argument("--budget", type=int)
    parser.add_argument("--category")
    args = parser.parse_args()

    router = TravelRouterIntl()
    kw = {"city": args.city, "days": args.days}
    if args.budget: kw["budget"] = args.budget
    if args.category: kw["category"] = args.category
    result = router.query(args.mode, **kw)
    print(json.dumps(result, indent=2, ensure_ascii=False))

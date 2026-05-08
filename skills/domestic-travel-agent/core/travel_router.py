#!/usr/bin/env python3
"""
travel-router v1.0.0
太一旅游探路者 · 三层路由引擎

借鉴 AI HOT 精选/日报/全量 模式，为旅游信息提供统一查询入口。
纯路由层，不依赖 core 模块的具体实现，输出标准 dict 结构。
"""

import json, logging, re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

logger = logging.getLogger("travel-router")

# 示例精选数据（TODO: 接入真实数据集）
TOP_PICKS = {
    "beijing": {
        "attractions": [
            {"name": "故宫博物院", "rating": 4.8, "price": "60元", "duration": "4h", "category": "历史"},
            {"name": "八达岭长城", "rating": 4.7, "price": "40元", "duration": "5h", "category": "历史"},
            {"name": "颐和园", "rating": 4.7, "price": "30元", "duration": "3h", "category": "园林"},
            {"name": "天坛公园", "rating": 4.6, "price": "15元", "duration": "2h", "category": "历史"},
        ],
        "restaurants": [
            {"name": "全聚德烤鸭", "rating": 4.5, "price": "人均200", "cuisine": "京菜"},
            {"name": "东来顺涮肉", "rating": 4.4, "price": "人均150", "cuisine": "火锅"},
            {"name": "护国寺小吃", "rating": 4.3, "price": "人均50", "cuisine": "小吃"},
        ],
        "hotels": [
            {"name": "北京王府井希尔顿", "rating": 4.8, "price_range": "¥1200-2000", "location": "王府井"},
            {"name": "北京建国饭店", "rating": 4.5, "price_range": "¥600-1000", "location": "建国门"},
        ],
    },
    "chengdu": {
        "attractions": [
            {"name": "大熊猫繁育基地", "rating": 4.8, "price": "55元", "duration": "3h", "category": "自然"},
            {"name": "都江堰", "rating": 4.7, "price": "80元", "duration": "4h", "category": "历史"},
            {"name": "武侯祠", "rating": 4.5, "price": "50元", "duration": "1.5h", "category": "历史"},
            {"name": "宽窄巷子", "rating": 4.4, "price": "免费", "duration": "2h", "category": "街区"},
        ],
        "restaurants": [
            {"name": "小龙坎火锅", "rating": 4.6, "price": "人均120", "cuisine": "川味火锅"},
            {"name": "陈麻婆豆腐", "rating": 4.5, "price": "人均80", "cuisine": "川菜"},
            {"name": "龙抄手", "rating": 4.3, "price": "人均30", "cuisine": "小吃"},
        ],
        "hotels": [
            {"name": "成都博舍", "rating": 4.9, "price_range": "¥1500-3000", "location": "太古里"},
            {"name": "成都瑞吉", "rating": 4.8, "price_range": "¥1200-2500", "location": "天府广场"},
        ],
    },
    "chongqing": {
        "attractions": [
            {"name": "洪崖洞", "rating": 4.6, "price": "免费", "duration": "2h", "category": "夜景"},
            {"name": "磁器口古镇", "rating": 4.4, "price": "免费", "duration": "2h", "category": "古镇"},
            {"name": "长江索道", "rating": 4.5, "price": "20元", "duration": "0.5h", "category": "体验"},
        ],
        "restaurants": [
            {"name": "周师兄火锅", "rating": 4.7, "price": "人均100", "cuisine": "重庆火锅"},
            {"name": "曾老幺鱼庄", "rating": 4.5, "price": "人均80", "cuisine": "江湖菜"},
        ],
        "hotels": [
            {"name": "重庆来福士洲际", "rating": 4.8, "price_range": "¥1000-2000", "location": "解放碑"},
        ],
    },
    "shanghai": {
        "attractions": [
            {"name": "外滩", "rating": 4.7, "price": "免费", "duration": "1.5h", "category": "景观"},
            {"name": "迪士尼乐园", "rating": 4.8, "price": "475元", "duration": "9h", "category": "乐园"},
            {"name": "东方明珠", "rating": 4.5, "price": "199元", "duration": "2h", "category": "地标"},
        ],
        "restaurants": [
            {"name": "南翔馒头店", "rating": 4.4, "price": "人均80", "cuisine": "本帮菜"},
            {"name": "老吉士", "rating": 4.5, "price": "人均150", "cuisine": "本帮菜"},
        ],
        "hotels": [
            {"name": "上海和平饭店", "rating": 4.9, "price_range": "¥2000-4000", "location": "外滩"},
        ],
    },
    "sanya": {
        "attractions": [
            {"name": "亚龙湾", "rating": 4.8, "price": "免费", "duration": "4h", "category": "海滩"},
            {"name": "蜈支洲岛", "rating": 4.7, "price": "136元", "duration": "5h", "category": "海岛"},
        ],
        "restaurants": [
            {"name": "第一市场海鲜", "rating": 4.5, "price": "人均200", "cuisine": "海鲜"},
        ],
        "hotels": [
            {"name": "三亚艾迪逊", "rating": 4.9, "price_range": "¥2000-5000", "location": "海棠湾"},
        ],
    },
}


class TravelRouter:
    """
    三层路由引擎
    
    用法:
        router = TravelRouter()
        router.query("selected", city="beijing")
        router.query("daily", city="chengdu", days=3)
        router.query("all", city="chongqing")
    """

    def __init__(self, agent_type: str = "domestic"):
        self.agent_type = agent_type

    # ═══════════════════════════════════════════
    # 三层路由入口
    # ═══════════════════════════════════════════

    def query(self, mode="selected", city="", days=3, budget=5000,
              preferences="综合", category=None, max_items=10) -> Dict[str, Any]:
        """
        统一旅游查询入口
        """
        mode = mode or "selected"
        city = city.lower()
        logger.info(f"三层路由: mode={mode} city={city} days={days}")

        if mode == "selected":
            return self._selected(city, days, category, max_items)
        elif mode == "daily":
            return self._daily(city, days, budget, preferences)
        elif mode == "all":
            return self._all(city, category, max_items)
        else:
            return {"status": "error", "error": f"无效 mode: {mode}"}

    def _selected(self, city: str, days: int, category: str, max_items: int) -> Dict[str, Any]:
        """精选层 — Top N 精华推荐"""
        picks = TOP_PICKS.get(city, {})
        if not picks:
            return {"status": "error", "city": city, "error": f"暂无{city}的精选数据", "suggestion": "试试北京/上海/成都/重庆/三亚"}

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

        return {"mode": "selected", "city": city, "days": days, "sections": sections,
                "total": sum(s["count"] for s in sections)}

    def _daily(self, city: str, days: int, budget: int, preferences: str) -> Dict[str, Any]:
        """日报层 — 完整行程"""
        picks = TOP_PICKS.get(city, {})
        if not picks:
            return {"status": "error", "city": city, "error": f"暂无{city}的行程数据"}

        # 分配每日行程
        attractions = picks.get("attractions", [])[:days * 2]
        restaurants = picks.get("restaurants", [])[:days]
        hotels = picks.get("hotels", [])[:1]

        itinerary = []
        daily_budget = budget / days
        for day in range(1, days + 1):
            day_plan = {
                "day": day,
                "date": (datetime.now() + timedelta(days=day - 1)).strftime("%Y-%m-%d"),
                "schedule": [],
                "daily_budget": round(daily_budget, 2),
            }
            # 上午
            if len(attractions) >= day * 2 - 1:
                a = attractions[day * 2 - 2]
                day_plan["schedule"].append({
                    "time": "09:00-12:00", "activity": f"参观 {a['name']}",
                    "cost": re.findall(r'\d+', a.get("price", "0"))[0] if re.findall(r'\d+', a.get("price", "0")) else 0,
                })
            day_plan["schedule"].append({"time": "12:00-13:30", "activity": "午餐", "cost": 80})
            # 下午
            if len(attractions) >= day * 2:
                a = attractions[day * 2 - 1]
                day_plan["schedule"].append({
                    "time": "14:00-17:00", "activity": f"参观 {a['name']}",
                    "cost": re.findall(r'\d+', a.get("price", "0"))[0] if re.findall(r'\d+', a.get("price", "0")) else 0,
                })
            # 晚餐
            if day <= len(restaurants):
                r = restaurants[day - 1]
                day_plan["schedule"].append({
                    "time": "18:30-20:00", "activity": f"晚餐: {r['name']}",
                    "cost": re.findall(r'\d+', r.get("price", "0"))[0] if re.findall(r'\d+', r.get("price", "0")) else 100,
                })
            itinerary.append(day_plan)

        return {
            "mode": "daily", "city": city, "days": days,
            "total_budget": budget, "preferences": preferences,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "itinerary": itinerary,
            "daily_budget": round(daily_budget, 2),
            "tips": ["建议提前预订门票", "带好身份证", "预留半天灵活时间"],
            "hotel": hotels[0] if hotels else None,
        }

    def _all(self, city: str, category: str, max_items: int) -> Dict[str, Any]:
        """全量层 — 全部数据"""
        picks = TOP_PICKS.get(city, {})
        sections = []
        if not category or category == "attractions":
            items = picks.get("attractions", [])
            sections.append({"label": "全部景点", "items": items[:max_items], "count": len(items)})
        if not category or category == "restaurants":
            items = picks.get("restaurants", [])
            sections.append({"label": "全部餐馆", "items": items[:max_items], "count": len(items)})
        if not category or category == "hotels":
            items = picks.get("hotels", [])
            sections.append({"label": "全部住宿", "items": items[:max_items], "count": len(items)})
        return {"mode": "all", "city": city, "sections": sections, "total": sum(s["count"] for s in sections)}

    # ═══════════════════════════════════════════
    # 语义路由工具
    # ═══════════════════════════════════════════

    @staticmethod
    def resolve_mode(text: str) -> str:
        t = text.lower()
        if any(kw in t for kw in ["推荐", "精华", "经典", "必去", "必吃", "top"]):
            return "selected"
        if any(kw in t for kw in ["行程", "攻略", "规划", "安排", "路线"]):
            return "daily"
        if any(kw in t for kw in ["全部", "所有", "全量", "完整"]):
            return "all"
        return "selected"

    @staticmethod
    def resolve_category(text: str) -> Optional[str]:
        t = text.lower()
        if any(kw in t for kw in ["酒店", "住宿", "住"]):
            return "hotels"
        if any(kw in t for kw in ["吃", "餐厅", "餐馆", "美食", "饭店"]):
            return "restaurants"
        if any(kw in t for kw in ["景点", "玩", "景区", "打卡"]):
            return "attractions"
        return None

    def health_check(self) -> Dict[str, Any]:
        return {"module": "travel-router", "version": "1.0.0", "status": "active",
                "cities": list(TOP_PICKS.keys())}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="selected")
    parser.add_argument("--city", default="")
    parser.add_argument("--days", type=int, default=3)
    parser.add_argument("--budget", type=int)
    parser.add_argument("--category")
    parser.add_argument("--preferences", default="综合")
    args = parser.parse_args()

    router = TravelRouter()
    kw = {"city": args.city, "days": args.days, "preferences": args.preferences}
    if args.budget: kw["budget"] = args.budget
    if args.category: kw["category"] = args.category
    result = router.query(args.mode, **kw)
    print(json.dumps(result, indent=2, ensure_ascii=False))

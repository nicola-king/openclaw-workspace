#!/usr/bin/env python3
"""
省钱技能引擎 v2.0 — 8大比价技能 + 验证链接
融合自 ai_travel_explorer v1.0 (8 skills) + company-enricher 验证体系

技能清单:
1. cheapest_date_scanner   — 查前后7天最低价
2. lowest_fare_finder      — 4周内最低航班
3. multi_route_optimizer   — 复杂行程优化
4. promo_code_finder       — 航司优惠码
5. fee_minimizer           — 隐藏费用分解
6. price_match_email       — 价格协商邮件模板
7. refund_flexibility      — 退改政策评估
8. hidden_city_ticketing   — 中转下机省票 (⚠️高风险)
"""
import json, re, math
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta

# 验证链接模板
VERIFICATION_LINKS = {
    "google_flights": lambda q: {"label":"Google Flights","url":f"https://www.google.com/travel/flights?q={q}","status":"比价参考"},
    "ctrip": lambda q: {"label":"携程","url":f"https://flights.ctrip.com/online/search/domestic?depart={q}","status":"国内比价"},
    "12306": lambda r: {"label":"12306","url":f"https://www.12306.cn/index/","status":"铁路官方"},
    "fliggy": lambda q: {"label":"飞猪","url":f"https://www.fliggy.com/","status":"阿里旅行"},
}

class SavingsEngine:
    """8大省钱技能引擎"""
    
    def cheapest_date_scanner(self, origin: str, destination: str,
                               target_date: str, days_range: int = 7) -> Dict:
        """技能1: 扫描目标日期前后 range 天，找到最便宜的出行日期"""
        from urllib.parse import quote_plus
        results = []
        target = datetime.strptime(target_date, "%Y-%m-%d")
        for offset in range(-days_range, days_range + 1):
            date = target + timedelta(days=offset)
            price = self._simulate_price(date, origin, destination)
            results.append({"date": date.strftime("%Y-%m-%d"), "price": price})
        results.sort(key=lambda x: x["price"])
        best = results[0]
        avg_price = sum(r["price"] for r in results) / len(results)
        savings = avg_price - best["price"]
        return {
            "skill": "Cheapest Date Scanner",
            "origin": origin, "destination": destination,
            "best_date": best["date"], "best_price": best["price"],
            "savings": round(savings, 2),
            "all_dates": results[:5],
            "verification_links": [
                VERIFICATION_LINKS["google_flights"](quote_plus(f"{origin} to {destination} {best['date']}")),
                VERIFICATION_LINKS["ctrip"](quote_plus(f"{origin}-{destination}")),
            ]
        }
    
    def lowest_fare_finder(self, origin: str, destination: str,
                            weeks_range: int = 4) -> Dict:
        """技能2: 4周内最低票价"""
        from urllib.parse import quote_plus
        results = []
        for week in range(weeks_range):
            price = self._simulate_price(
                datetime.now() + timedelta(weeks=week), origin, destination)
            results.append({"week": week + 1, "approx_price": price})
        results.sort(key=lambda x: x["approx_price"])
        return {
            "skill": "Lowest Fare Finder",
            "origin": origin, "destination": destination,
            "best_week": results[0]["week"],
            "best_price": results[0]["approx_price"],
            "all_weeks": results,
            "verification_links": [
                VERIFICATION_LINKS["google_flights"](quote_plus(f"{origin} to {destination}")),
                VERIFICATION_LINKS["fliggy"](None),
            ]
        }
    
    def multi_route_optimizer(self, routes: List[Dict],
                               max_layover: int = 6) -> Dict:
        """技能3: 多段路线优化"""
        total_price = sum(r.get("price", 500) for r in routes)
        total_hours = sum(r.get("hours", 2) for r in routes)
        return {
            "skill": "Multi-Route Optimizer",
            "segments": routes,
            "total_price": total_price,
            "total_duration": f"{total_hours}h",
            "savings": round(total_price * 0.15, 2),
            "note": "分段购买通常比直飞便宜15-30%",
        }
    
    def promo_code_finder(self, airline: str = "", route: str = "") -> Dict:
        """技能4: 促销码查找"""
        from urllib.parse import quote_plus
        return {
            "skill": "Promo Code Finder",
            "airline": airline or "通用",
            "promos": [
                {"source": "航空公司官网", "url": f"https://www.{'ctrip' if not airline else airline}.com/promos",
                 "tip": "注册会员可获取专属优惠"},
                {"source": "银行合作", "tip": "招行/建行信用卡常有满减"},
            ],
            "verification_links": [
                {"label": "携程优惠", "url": "https://promo.ctrip.com/", "status": "实时"},
                {"label": "飞猪优惠", "url": "https://traveldetail.fliggy.com/", "status": "实时"},
            ]
        }
    
    def fee_minimizer(self, flight_price: float) -> Dict:
        """技能5: 费用最小化"""
        base = flight_price * 0.85
        taxes = flight_price * 0.08
        fuel = flight_price * 0.05
        insurance = 50
        service = flight_price * 0.02
        return {
            "skill": "Fee Minimizer",
            "breakdown": {
                "base_fare": round(base, 2),
                "taxes": round(taxes, 2),
                "fuel_surcharge": round(fuel, 2),
                "insurance": insurance,
                "service_fee": round(service, 2),
                "total": round(base + taxes + fuel + insurance + service, 2),
            },
            "saving_tips": [
                "提前在线值机免选座费",
                "自带餐食节省机上消费",
                "比价后使用银行优惠支付",
            ]
        }
    
    def price_match_email(self, airline: str, competitor_price: float) -> str:
        """技能6: 价格匹配邮件模板"""
        return f"""Subject: Price Match Request — Better Rate Found

Dear {airline} Customer Service,

I recently booked a flight with your airline. However, I have found
a lower price of ${competitor_price} on a competing platform.

Could you please match this price?

Booking Details:
- Competitor Price: ${competitor_price}

Thank you for your consideration.

Best regards,
[Your Name]
[Your Booking Reference]

P.S. I am a loyal customer and would prefer to stay with {airline}."""
    
    def refund_flexibility_check(self, ticket_type: str = "economy") -> Dict:
        """技能7: 退款灵活性检查"""
        flexibility = {"flexible": True, "change_fee": 0, "cancellation_fee": 0, "score": 10}
        if ticket_type == "economy":
            flexibility = {"flexible": False, "change_fee": 300, "cancellation_fee": 500, "score": 4}
        elif ticket_type == "business":
            flexibility = {"flexible": True, "change_fee": 100, "cancellation_fee": 200, "score": 7}
        return {
            "skill": "Refund & Flexibility Check",
            "ticket_type": ticket_type,
            "policy": flexibility,
            "recommendation": "建议购买灵活票或退改险" if not flexibility["flexible"] else "该票种灵活性良好",
        }
    
    def hidden_city_ticketing(self, origin: str, destination: str,
                               via: str) -> Dict:
        """技能8: 隐秘之城（中转下机）"""
        regular_price = self._simulate_price(datetime.now(), origin, destination)
        hidden_price = regular_price * 0.75
        return {
            "skill": "Hidden City Ticketing",
            "origin": origin, "destination": destination,
            "via": via,
            "regular_price": round(regular_price, 2),
            "hidden_city_price": round(hidden_price, 2),
            "savings": round(regular_price - hidden_price, 2),
            "risks": [
                "⚠️ 只能携带随身行李（托运直挂到最终站）",
                "⚠️ 航空公司可能禁止此行为",
                "⚠️ 回程可能被取消",
                "⚠️ 常旅客积分可能受影响",
            ],
            "verification_links": [
                {"label": "Google Flights 比价", "url": f"https://www.google.com/travel/flights?q={origin}+to+{destination}", "status": "验证价格"},
            ]
        }
    
    def _simulate_price(self, date: datetime, origin: str, destination: str) -> float:
        """模拟价格（实际应接入API）"""
        import hashlib
        seed = int(hashlib.md5(f"{date.strftime('%Y%m%d')}{origin}{destination}".encode()).hexdigest()[:8], 16)
        base = 500 + (seed % 2000)
        # 周末略贵
        if date.weekday() >= 5:
            base *= 1.2
        return round(base, 2)
    
    def all_skills(self) -> List[str]:
        """列出所有技能"""
        return [
            "cheapest_date_scanner — 查前后7天最低价",
            "lowest_fare_finder — 4周内最低航班",
            "multi_route_optimizer — 多段路线优化",
            "promo_code_finder — 航司优惠码",
            "fee_minimizer — 隐藏费用分解",
            "price_match_email — 价格协商邮件",
            "refund_flexibility_check — 退改政策",
            "hidden_city_ticketing — 隐秘之城 (⚠️高风险)",
        ]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="省钱技能引擎")
    parser.add_argument("--skill", type=int, choices=range(1,9), help="技能编号 1-8")
    parser.add_argument("--origin", default="重庆")
    parser.add_argument("--destination", default="北京")
    parser.add_argument("--date", default=(datetime.now()+timedelta(days=7)).strftime("%Y-%m-%d"))
    parser.add_argument("--list", action="store_true", help="列出所有技能")
    args = parser.parse_args()
    
    engine = SavingsEngine()
    
    if args.list:
        print("8大省钱技能:\n")
        for s in engine.all_skills():
            print(f"  {s}")
        exit()
    
    skills = {
        1: engine.cheapest_date_scanner(args.origin, args.destination, args.date),
        2: engine.lowest_fare_finder(args.origin, args.destination),
        3: engine.multi_route_optimizer([
            {"from":args.origin,"to":args.destination,"price":600,"hours":2.5},
            {"from":args.destination,"to":args.origin,"price":550,"hours":2.5}]),
        4: engine.promo_code_finder(),
        5: engine.fee_minimizer(1200),
        6: {"email_template": engine.price_match_email("中国国航", 900)},
        7: engine.refund_flexibility_check(),
        8: engine.hidden_city_ticketing(args.origin, args.destination, "西安"),
    }
    
    result = skills.get(args.skill, skills[1])
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))

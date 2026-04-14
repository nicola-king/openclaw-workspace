#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一旅行落地服务模块 - Ground Services

功能:
1. 落地包车服务
2. 落地接机服务
3. 落地导游服务
4. 多城市联程服务
5. VIP 定制服务

作者：太一 AGI
创建：2026-04-14
"""

import random
from datetime import datetime
from typing import Dict, List, Optional


class GroundServices:
    """落地服务模块"""
    
    def __init__(self):
        self.service_providers = {
            "包车": [
                {"name": "神州专车", "rating": 4.9, "price_per_day": 800},
                {"name": "滴滴豪华车", "rating": 4.8, "price_per_day": 700},
                {"name": "携程包车", "rating": 4.7, "price_per_day": 600},
                {"name": "飞猪包车", "rating": 4.8, "price_per_day": 650},
            ],
            "接机": [
                {"name": "携程接机", "rating": 4.9, "price_base": 300},
                {"name": "飞猪接机", "rating": 4.8, "price_base": 280},
                {"name": "Klook 接机", "rating": 4.7, "price_base": 250},
                {"name": "Grab 接机", "rating": 4.8, "price_base": 260},
            ],
            "导游": [
                {"name": "王导", "language": "中文/英文", "rating": 4.9, "price_per_day": 800, "experience": "5 年"},
                {"name": "李导", "language": "中文/日文", "rating": 4.8, "price_per_day": 700, "experience": "4 年"},
                {"name": "张导", "language": "中文/韩文", "rating": 4.7, "price_per_day": 600, "experience": "3 年"},
                {"name": "刘导", "language": "中文/法文", "rating": 4.9, "price_per_day": 900, "experience": "6 年"},
                {"name": "陈导", "language": "中文/西班牙文", "rating": 4.8, "price_per_day": 750, "experience": "5 年"},
            ],
        }
        
        self.car_types = {
            "经济型": {"seats": 4, "luggage": 2, "price_multiplier": 1.0},
            "舒适型": {"seats": 4, "luggage": 3, "price_multiplier": 1.3},
            "豪华型": {"seats": 4, "luggage": 3, "price_multiplier": 1.8},
            "商务型": {"seats": 6, "luggage": 4, "price_multiplier": 2.0},
            "保姆车": {"seats": 7, "luggage": 5, "price_multiplier": 2.5},
        }
    
    # ========== 落地包车服务 ==========
    
    def search_charter_car(self, destination: str, days: int, 
                          car_type: str = "舒适型", 
                          travelers: int = 2) -> Dict:
        """
        搜索包车服务
        
        Args:
            destination: 目的地
            days: 使用天数
            car_type: 车型 (经济型/舒适型/豪华型/商务型/保姆车)
            travelers: 人数
        
        Returns:
            包车服务信息
        """
        print(f"🚐 搜索包车服务：{destination} ({days}天)")
        
        # 选择服务商
        provider = random.choice(self.service_providers["包车"])
        
        # 计算价格
        base_price = provider["price_per_day"]
        multiplier = self.car_types.get(car_type, {}).get("price_multiplier", 1.0)
        total_price = int(base_price * multiplier * days)
        
        # 生成服务信息
        service = {
            "type": "Charter Car",
            "destination": destination,
            "provider": provider["name"],
            "provider_rating": provider["rating"],
            "car_type": car_type,
            "car_info": self.car_types.get(car_type, {}),
            "days": days,
            "price_per_day": int(base_price * multiplier),
            "total_price": total_price,
            "includes": [
                "专业司机",
                "燃油费",
                "过路费",
                "停车费",
                "保险",
                f"每日{8}小时服务",
            ],
            "notes": [
                "超时按¥50/小时计费",
                "夜间服务 (22:00-6:00) 加收 20%",
                "偏远地区可能加收",
            ],
            "booking_info": {
                "advance_booking": "建议提前 3 天预订",
                "cancellation": "24 小时前免费取消",
                "payment": "上车支付/在线支付",
            },
        }
        
        print(f"  服务商：{provider['name']} (评分：{provider['rating']})")
        print(f"  车型：{car_type}")
        print(f"  价格：¥{total_price} ({days}天)")
        
        return service
    
    # ========== 落地接机服务 ==========
    
    def search_airport_pickup(self, destination: str, airport: str,
                             flight_number: str, travelers: int = 2,
                             car_type: str = "舒适型") -> Dict:
        """
        搜索接机服务
        
        Args:
            destination: 目的地城市
            airport: 机场名称
            flight_number: 航班号
            travelers: 人数
            car_type: 车型
        
        Returns:
            接机服务信息
        """
        print(f"🚗 搜索接机服务：{airport} → {destination}")
        
        # 选择服务商
        provider = random.choice(self.service_providers["接机"])
        
        # 计算价格
        base_price = provider["price_base"]
        multiplier = self.car_types.get(car_type, {}).get("price_multiplier", 1.0)
        total_price = int(base_price * multiplier)
        
        # 生成服务信息
        service = {
            "type": "Airport Pickup",
            "destination": destination,
            "airport": airport,
            "flight_number": flight_number,
            "provider": provider["name"],
            "provider_rating": provider["rating"],
            "car_type": car_type,
            "car_info": self.car_types.get(car_type, {}),
            "travelers": travelers,
            "price": total_price,
            "includes": [
                "航班动态追踪",
                "免费等待 60 分钟",
                "举牌接机",
                "协助搬运行李",
                "保险",
            ],
            "driver_info": {
                "contact": "预订后提供",
                "vehicle_plate": "预订后提供",
                "meeting_point": f"{airport}到达厅出口",
            },
            "notes": [
                "航班延误免费等待",
                "夜间服务 (22:00-6:00) 加收 20%",
                "超大行李可能加收",
            ],
            "booking_info": {
                "advance_booking": "建议提前 24 小时预订",
                "cancellation": "起飞前免费取消",
                "payment": "在线支付/上车支付",
            },
        }
        
        print(f"  服务商：{provider['name']} (评分：{provider['rating']})")
        print(f"  价格：¥{total_price}")
        
        return service
    
    # ========== 落地导游服务 ==========
    
    def search_local_guide(self, destination: str, days: int,
                          language: str = "中文",
                          travelers: int = 2,
                          tour_type: str = "休闲游") -> Dict:
        """
        搜索导游服务
        
        Args:
            destination: 目的地
            days: 服务天数
            language: 语言需求
            travelers: 人数
            tour_type: 游览类型 (休闲游/深度游/定制游)
        
        Returns:
            导游服务信息
        """
        print(f"👨‍🦯 搜索导游服务：{destination} ({days}天)")
        
        # 筛选符合条件的导游
        available_guides = [
            g for g in self.service_providers["导游"]
            if language.split("/")[0] in g["language"]
        ]
        
        if not available_guides:
            available_guides = self.service_providers["导游"][:1]
        
        # 选择评分最高的导游
        guide = max(available_guides, key=lambda x: x["rating"])
        
        # 根据游览类型调整价格
        type_multiplier = {
            "休闲游": 1.0,
            "深度游": 1.3,
            "定制游": 1.8,
            "商务游": 2.0,
        }.get(tour_type, 1.0)
        
        total_price = int(guide["price_per_day"] * type_multiplier * days)
        
        # 生成服务信息
        service = {
            "type": "Local Guide",
            "destination": destination,
            "guide": {
                "name": guide["name"],
                "language": guide["language"],
                "rating": guide["rating"],
                "experience": guide["experience"],
                "specialties": [
                    "历史文化讲解",
                    "美食推荐",
                    "拍照指导",
                    "行程规划",
                ],
            },
            "days": days,
            "tour_type": tour_type,
            "price_per_day": int(guide["price_per_day"] * type_multiplier),
            "total_price": total_price,
            "includes": [
                "专业导游服务",
                "行程规划",
                "景点讲解",
                "餐饮推荐",
                "交通安排建议",
                f"每日{8}小时服务",
            ],
            "excludes": [
                "景点门票",
                "餐饮费用",
                "交通费用",
                "小费 (自愿)",
            ],
            "notes": [
                "超时按¥100/小时计费",
                "夜间服务 (22:00-6:00) 加收 30%",
                "特殊景点可能需额外费用",
            ],
            "booking_info": {
                "advance_booking": "建议提前 3 天预订",
                "cancellation": "48 小时前免费取消",
                "payment": "服务结束后支付",
            },
        }
        
        print(f"  导游：{guide['name']} ({guide['language']})")
        print(f"  评分：{guide['rating']} (经验：{guide['experience']})")
        print(f"  价格：¥{total_price} ({days}天)")
        
        return service
    
    # ========== 套餐服务 ==========
    
    def search_ground_package(self, destination: str, days: int,
                             airport: str, flight_number: str,
                             travelers: int = 2,
                             package_type: str = "标准套餐") -> Dict:
        """
        搜索落地服务套餐
        
        Args:
            destination: 目的地
            days: 天数
            airport: 机场
            flight_number: 航班号
            travelers: 人数
            package_type: 套餐类型 (经济/标准/豪华/VIP)
        
        Returns:
            套餐服务信息
        """
        print(f"🎁 搜索落地服务套餐：{destination} ({days}天)")
        
        # 套餐配置
        packages = {
            "经济套餐": {
                "car_type": "经济型",
                "guide_days": 0,  # 不含导游
                "discount": 0.9,
            },
            "标准套餐": {
                "car_type": "舒适型",
                "guide_days": 2,  # 含 2 天导游
                "discount": 0.85,
            },
            "豪华套餐": {
                "car_type": "豪华型",
                "guide_days": days,  # 全程导游
                "discount": 0.8,
            },
            "VIP 套餐": {
                "car_type": "商务型",
                "guide_days": days,  # 全程导游
                "discount": 0.75,
            },
        }
        
        package_config = packages.get(package_type, packages["标准套餐"])
        
        # 接机服务
        pickup = self.search_airport_pickup(
            destination, airport, flight_number, travelers,
            package_config["car_type"]
        )
        
        # 包车服务 (全程)
        charter = self.search_charter_car(
            destination, days, package_config["car_type"], travelers
        )
        
        # 导游服务 (部分天数)
        guide = None
        if package_config["guide_days"] > 0:
            guide = self.search_local_guide(
                destination, package_config["guide_days"],
                "中文", travelers, "休闲游"
            )
        
        # 计算总价
        total = pickup["price"] + charter["total_price"]
        if guide:
            total += guide["total_price"]
        
        # 套餐折扣
        discount_price = int(total * package_config["discount"])
        savings = total - discount_price
        
        # 生成套餐信息
        package = {
            "type": "Ground Services Package",
            "package_type": package_type,
            "destination": destination,
            "days": days,
            "travelers": travelers,
            "services": {
                "airport_pickup": pickup,
                "charter_car": charter,
                "local_guide": guide,
            },
            "pricing": {
                "pickup_price": pickup["price"],
                "charter_price": charter["total_price"],
                "guide_price": guide["total_price"] if guide else 0,
                "subtotal": total,
                "discount": package_config["discount"],
                "savings": savings,
                "total_price": discount_price,
            },
            "includes": [
                "落地接机服务",
                f"{days}天包车服务",
                f"{package_config['guide_days']}天地陪导游",
                "专业司机",
                "航班动态追踪",
                "24 小时客服",
            ],
            "booking_info": {
                "advance_booking": "建议提前 5 天预订",
                "cancellation": "72 小时前免费取消",
                "payment": "在线支付/分期支付",
            },
        }
        
        print(f"\n  套餐类型：{package_type}")
        print(f"  原价：¥{total}")
        print(f"  套餐价：¥{discount_price}")
        print(f"  节省：¥{savings}")
        
        return package
    
    # ========== 推荐服务 ==========
    
    def recommend_services(self, destination: str, days: int,
                          travelers: int, budget: float,
                          purpose: str = "休闲") -> Dict:
        """
        推荐落地服务
        
        Args:
            destination: 目的地
            days: 天数
            travelers: 人数
            budget: 预算
            purpose: 旅行目的
        
        Returns:
            推荐方案
        """
        print(f"\n💡 推荐落地服务：{destination}")
        
        # 根据预算推荐套餐
        if budget >= 10000:
            package_type = "VIP 套餐"
        elif budget >= 5000:
            package_type = "豪华套餐"
        elif budget >= 2000:
            package_type = "标准套餐"
        else:
            package_type = "经济套餐"
        
        # 根据旅行目的调整
        if purpose == "商务":
            package_type = "VIP 套餐"
        elif purpose == "亲子":
            package_type = "豪华套餐"
        elif purpose == "情侣":
            package_type = "标准套餐"
        
        recommendation = {
            "type": "Recommendation",
            "destination": destination,
            "recommended_package": package_type,
            "reason": f"根据预算¥{budget}和{purpose}游推荐",
            "alternative_packages": [
                pkg for pkg in ["经济套餐", "标准套餐", "豪华套餐", "VIP 套餐"]
                if pkg != package_type
            ][:2],
        }
        
        print(f"  推荐套餐：{package_type}")
        print(f"  原因：{recommendation['reason']}")
        
        return recommendation


def main():
    """测试"""
    print("=" * 60)
    print("🚐 太一旅行落地服务测试")
    print("=" * 60)
    
    services = GroundServices()
    
    # 测试 1: 包车服务
    print("\n🚐 测试 1: 包车服务")
    charter = services.search_charter_car(
        destination="东京",
        days=5,
        car_type="舒适型",
        travelers=2
    )
    
    # 测试 2: 接机服务
    print("\n🚗 测试 2: 接机服务")
    pickup = services.search_airport_pickup(
        destination="东京",
        airport="成田国际机场",
        flight_number="CA181",
        travelers=2,
        car_type="舒适型"
    )
    
    # 测试 3: 导游服务
    print("\n👨‍🦯 测试 3: 导游服务")
    guide = services.search_local_guide(
        destination="东京",
        days=3,
        language="中文",
        travelers=2,
        tour_type="深度游"
    )
    
    # 测试 4: 套餐服务
    print("\n🎁 测试 4: 套餐服务")
    package = services.search_ground_package(
        destination="东京",
        days=5,
        airport="成田国际机场",
        flight_number="CA181",
        travelers=2,
        package_type="豪华套餐"
    )
    
    # 测试 5: 推荐服务
    print("\n💡 测试 5: 推荐服务")
    recommendation = services.recommend_services(
        destination="东京",
        days=5,
        travelers=2,
        budget=8000,
        purpose="休闲"
    )
    
    print("\n" + "=" * 60)
    print("✅ 落地服务测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()

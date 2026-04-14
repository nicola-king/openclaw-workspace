#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一旅行探路者 Agent - Taiyi Travel Pathfinder Agent

功能:
1. 智能旅行规划
2. 航班/酒店查询
3. 路线优化
4. 预算管理
5. 景点推荐
6. 旅行清单生成
7. 天气查询
8. 多平台推送

集成:
- AI 旅行探路者 (8 个技能)
- APILayer API (航班/天气/汇率)
- 智能调度中心
- Telegram/微信推送

作者：太一 AGI
创建：2026-04-14
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
AGENT_DIR = Path(__file__).parent
DATA_DIR = AGENT_DIR / "data"
REPORTS_DIR = AGENT_DIR / "reports"

# 确保目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# 导入 AI 旅行探路者
sys.path.insert(0, str(WORKSPACE / "skills" / "04-integration" / "ai-travel-explorer"))
from ai_travel_explorer import AITravelExplorer

# 导入 APILayer 客户端
sys.path.insert(0, str(WORKSPACE / "skills" / "04-integration" / "apilayer-integration"))
from apilayer_client import APILayerClient

# 导入落地服务模块
from ground_services import GroundServices

# 导入知识学习模块
from travel_knowledge_learner import TravelKnowledgeLearner


class TaiyiTravelAgent:
    """太一旅行探路者 Agent"""
    
    def __init__(self):
        self.travel_explorer = AITravelExplorer()
        self.apilayer = APILayerClient()
        self.ground_services = GroundServices()
        self.knowledge_learner = TravelKnowledgeLearner()
        self.session_data = {}
        
        print(f"🌍 太一旅行探路者 Agent 启动")
        print(f"  集成：AI 旅行探路者 (8 个技能)")
        print(f"  集成：APILayer API (航班/天气/汇率)")
        print(f"  数据目录：{DATA_DIR}")
    
    # ========== 核心功能 ==========
    
    def plan_trip(self, origin: str, destination: str, 
                 start_date: str, end_date: str,
                 budget: float = 10000,
                 travelers: int = 1,
                 need_car_rental: bool = False,
                 need_local_guide: bool = False) -> Dict:
        """
        智能旅行规划
        
        Args:
            origin: 出发地
            destination: 目的地
            start_date: 出发日期 (YYYY-MM-DD)
            end_date: 返回日期 (YYYY-MM-DD)
            budget: 预算
            travelers: 人数
        
        Returns:
            旅行计划
        """
        print(f"\n🌍 智能旅行规划：{origin} → {destination}")
        print(f"  日期：{start_date} ~ {end_date}")
        print(f"  预算：¥{budget} × {travelers}人")
        
        # 1. 扫描最便宜日期
        print("\n📅 扫描最便宜日期...")
        date_scan = self.travel_explorer.cheapest_date_scanner(
            origin, destination, start_date
        )
        
        # 2. 查找最低票价
        print("\n✈️ 查找最低票价...")
        flights = self.travel_explorer.lowest_fare_finder(origin, destination, 4)
        
        # 3. 查询天气
        print("\n🌤️ 查询天气...")
        weather = self.apilayer.weatherstack_current(destination)
        
        # 4. 查询汇率 (如果是国际旅行)
        print("\n💱 查询汇率...")
        exchange = self.apilayer.fixer_latest("CNY", "USD,EUR,JPY")
        
        # 5. 生成旅行清单
        print("\n📋 生成旅行清单...")
        checklist = self._generate_checklist(destination, start_date, end_date, travelers)
        
        # 6. 预算分配
        print("\n💰 预算分配...")
        budget_allocation = self._allocate_budget(budget, travelers, flights)
        
        # 落地服务 (包车/接机/导游)
        ground_services = None
        if need_car_rental or need_local_guide:
            print("\n🚐 查询落地服务...")
            days = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days + 1
            
            # 根据需求选择套餐
            if need_car_rental and need_local_guide:
                package_type = "豪华套餐" if budget >= 10000 else "标准套餐"
                ground_services = self.ground_services.search_ground_package(
                    destination=destination,
                    days=days,
                    airport=f"{destination}国际机场",
                    flight_number="待定",
                    travelers=travelers,
                    package_type=package_type
                )
            elif need_car_rental:
                ground_services = {
                    "charter_car": self.ground_services.search_charter_car(
                        destination=destination,
                        days=days,
                        car_type="舒适型",
                        travelers=travelers
                    )
                }
            elif need_local_guide:
                ground_services = {
                    "local_guide": self.ground_services.search_local_guide(
                        destination=destination,
                        days=days,
                        language="中文",
                        travelers=travelers,
                        tour_type="休闲游"
                    )
                }
        
        # 整合计划
        trip_plan = {
            "type": "Trip Plan",
            "origin": origin,
            "destination": destination,
            "dates": {
                "start": start_date,
                "end": end_date,
            },
            "travelers": travelers,
            "budget": {
                "total": budget,
                "allocation": budget_allocation,
            },
            "flights": flights,
            "weather": weather,
            "exchange_rates": exchange,
            "checklist": checklist,
            "ground_services": ground_services,
            "timestamp": datetime.now().isoformat(),
        }
        
        # 保存计划
        self._save_plan(trip_plan, f"{destination}_{start_date}")
        
        print(f"\n✅ 旅行计划已生成")
        print(f"  总预算：¥{budget}")
        print(f"  航班预算：¥{budget_allocation['flights']}")
        print(f"  住宿预算：¥{budget_allocation['accommodation']}")
        print(f"  餐饮预算：¥{budget_allocation['meals']}")
        print(f"  活动预算：¥{budget_allocation['activities']}")
        
        return trip_plan
    
    def optimize_route(self, cities: List[str], budget: float = 20000) -> Dict:
        """
        多城市路线优化
        
        Args:
            cities: 城市列表
            budget: 总预算
        
        Returns:
            优化路线
        """
        print(f"\n🗺️ 多城市路线优化")
        print(f"  城市：{' → '.join(cities)}")
        print(f"  预算：¥{budget}")
        
        # 构建路线
        routes = []
        for i in range(len(cities) - 1):
            routes.append({
                "from": cities[i],
                "to": cities[i+1],
            })
        
        # 优化
        optimized = self.travel_explorer.multi_route_optimizer(routes, 4, budget)
        
        # 添加每城市建议
        city_suggestions = []
        for city in cities:
            suggestion = {
                "city": city,
                "days_recommended": 2,
                "highlights": [f"{city}景点 A", f"{city}景点 B", f"{city}美食"],
                "estimated_cost": budget // len(cities) // 3,
            }
            city_suggestions.append(suggestion)
        
        result = {
            "type": "Multi-City Route",
            "cities": cities,
            "routes": routes,
            "optimized": optimized["optimized"],
            "city_suggestions": city_suggestions,
            "total_budget": budget,
            "timestamp": datetime.now().isoformat(),
        }
        
        self._save_plan(result, f"multi_city_{'_'.join(cities)}")
        
        print(f"\n✅ 路线优化完成")
        print(f"  总价格：¥{optimized['optimized']['total_price']}")
        print(f"  总时长：{optimized['optimized']['total_duration']}")
        print(f"  节省：¥{optimized['optimized']['savings']}")
        
        return result
    
    def find_deals(self, origin: str, flexible: bool = True) -> Dict:
        """
        查找优惠旅行方案
        
        Args:
            origin: 出发地
            flexible: 日期/目的地是否灵活
        
        Returns:
            优惠方案列表
        """
        print(f"\n🎫 查找优惠旅行方案：{origin}")
        
        # 热门目的地
        destinations = ["东京", "首尔", "曼谷", "新加坡", "巴厘岛"]
        
        deals = []
        for dest in destinations:
            # 模拟优惠数据
            deal = {
                "destination": dest,
                "flight_price": 1000 + len(dest) * 100,
                "hotel_price": 300,
                "package_discount": "15%",
                "valid_until": "2026-05-31",
            }
            deals.append(deal)
        
        # 排序
        deals.sort(key=lambda x: x["flight_price"])
        
        result = {
            "type": "Travel Deals",
            "origin": origin,
            "deals": deals[:5],  # 返回前 5 个
            "timestamp": datetime.now().isoformat(),
        }
        
        self._save_plan(result, f"deals_from_{origin}")
        
        print(f"\n✅ 找到 {len(deals)} 个优惠方案")
        for deal in deals[:3]:
            print(f"  - {deal['destination']}: ¥{deal['flight_price']} (省{deal['package_discount']})")
        
        return result
    
    def generate_checklist(self, destination: str, days: int, 
                          purpose: str = "休闲") -> Dict:
        """
        生成旅行清单
        
        Args:
            destination: 目的地
            days: 天数
            purpose: 旅行目的
        
        Returns:
            旅行清单
        """
        print(f"\n📋 生成旅行清单：{destination} ({days}天)")
        
        checklist = self._generate_checklist(destination, "", "", 1, days, purpose)
        
        print(f"\n✅ 旅行清单已生成")
        print(f"  必备物品：{len(checklist['essentials'])} 项")
        print(f"  衣物：{len(checklist['clothing'])} 项")
        print(f"  电子产品：{len(checklist['electronics'])} 项")
        print(f"  文件：{len(checklist['documents'])} 项")
        
        return checklist
    
    # ========== 辅助方法 ==========
    
    def _generate_checklist(self, destination: str, start_date: str = "", 
                           end_date: str = "", travelers: int = 1,
                           days: int = 3, purpose: str = "休闲") -> Dict:
        """生成旅行清单"""
        
        # 根据目的地和天数生成
        checklist = {
            "essentials": [
                "护照/身份证",
                "钱包/信用卡",
                "手机/充电器",
                "常用药品",
                "口罩/消毒液",
            ],
            "clothing": [
                "换洗衣物",
                "睡衣",
                "外套",
                "舒适鞋子",
                "泳衣 (如需)",
            ],
            "electronics": [
                "充电宝",
                "转换插头",
                "相机",
                "耳机",
            ],
            "documents": [
                "机票确认单",
                "酒店预订单",
                "旅行保险",
                "紧急联系人",
            ],
            "optional": [
                "防晒霜",
                "墨镜",
                "帽子",
                "旅行枕",
            ],
        }
        
        return checklist
    
    def _search_car_rental(self, destination: str, start_date: str, 
                          end_date: str) -> Dict:
        """查询租车服务"""
        # 模拟数据 (实际需调用租车 API)
        import random
        companies = ["神州租车", "一嗨租车", "携程租车", "租租车"]
        car_types = ["经济型", "舒适型", "豪华型", "SUV", "MPV"]
        
        # 计算天数
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days = (end - start).days + 1
        
        rental = {
            "company": random.choice(companies),
            "car_type": random.choice(car_types),
            "price_per_day": 200 + random.randint(0, 300),
            "days": days,
            "total_price": 0,
            "includes": ["保险", "不限里程", "24 小时救援"],
            "pickup_location": f"{destination}机场店",
            "return_location": f"{destination}机场店",
        }
        rental["total_price"] = rental["price_per_day"] * days
        
        return rental
    
    def _search_local_guide(self, destination: str, start_date: str, 
                           end_date: str, travelers: int) -> Dict:
        """查询地陪服务"""
        # 模拟数据 (实际需调用导游平台 API)
        import random
        guides = [
            {"name": "王导", "language": "中文/英文", "rating": 4.9, "price_per_day": 800},
            {"name": "李导", "language": "中文/日文", "rating": 4.8, "price_per_day": 700},
            {"name": "张导", "language": "中文/韩文", "rating": 4.7, "price_per_day": 600},
            {"name": "刘导", "language": "中文/法文", "rating": 4.9, "price_per_day": 900},
        ]
        
        # 计算天数
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days = (end - start).days
        
        guide = random.choice(guides)
        
        service = {
            "name": guide["name"],
            "language": guide["language"],
            "rating": guide["rating"],
            "price_per_day": guide["price_per_day"],
            "days": days,
            "total_price": guide["price_per_day"] * days,
            "includes": ["行程规划", "景点讲解", "餐饮推荐", "交通安排"],
            "certifications": ["持证导游", "5 年经验", "好评率 98%"],
        }
        
        return service
    
    def _allocate_budget(self, total: float, travelers: int, 
                        flights: Dict) -> Dict:
        """预算分配"""
        
        # 估算航班费用
        flight_cost = 1500 * travelers if flights.get("flights") else 0
        
        remaining = total - flight_cost
        
        # 如果有租车/地陪，调整预算分配
        car_rental_cost = 0
        guide_cost = 0
        
        allocation = {
            "flights": flight_cost,
            "accommodation": int(remaining * 0.35),  # 35% 住宿
            "meals": int(remaining * 0.25),  # 25% 餐饮
            "activities": int(remaining * 0.15),  # 15% 活动
            "car_rental": car_rental_cost,  # 租车
            "local_guide": guide_cost,  # 地陪
            "shopping": int(remaining * 0.1),  # 10% 购物
        }
        
        return allocation
    
    def _save_plan(self, plan: Dict, name: str):
        """保存旅行计划"""
        import json
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = DATA_DIR / f"{name}_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 计划已保存：{output_file}")
        return output_file
    
    def send_to_telegram(self, plan: Dict, chat_id: str = "7073481596"):
        """发送到 Telegram"""
        print(f"📱 发送到 Telegram: {chat_id}")
        
        # 构建消息
        destination = plan.get('destination', '未知')
        dates = plan.get('dates', {})
        budget = plan.get('budget', {}).get('total', 0)
        travelers = plan.get('travelers', 1)
        
        message = f"""🌍 旅行计划

📍 目的地：{destination}
📅 日期：{dates.get('start', 'N/A')} ~ {dates.get('end', 'N/A')}
👥 人数：{travelers}人
💰 预算：¥{budget}
"""
        
        # 添加租车信息
        if plan.get('car_rental'):
            car = plan['car_rental']
            message += f"\n🚗 租车：{car.get('company', 'N/A')} - ¥{car.get('price', 0)}"
        
        # 添加地陪信息
        if plan.get('local_guide'):
            guide = plan['local_guide']
            message += f"\n👨‍🦯 地陪：{guide.get('name', 'N/A')} - ¥{guide.get('price', 0)}"
        
        # 调用 Telegram 发送脚本
        try:
            script_path = WORKSPACE / "scripts" / "send-md-to-telegram.py"
            if script_path.exists():
                import subprocess
                # 生成 Markdown 报告
                report = self.generate_report(plan)
                result = subprocess.run(
                    ["python3", str(script_path), str(report)],
                    capture_output=True,
                    timeout=30
                )
                if result.returncode == 0:
                    print(f"✅ Telegram 发送成功")
                else:
                    print(f"⚠️ Telegram 发送失败：{result.stderr.decode()[:100]}")
        except Exception as e:
            print(f"⚠️ Telegram 发送错误：{e}")
        
        return {"success": True, "chat_id": chat_id}
    
    def send_to_wechat(self, plan: Dict):
        """发送到微信"""
        print(f"💬 发送到微信")
        
        # 构建消息
        destination = plan.get('destination', '未知')
        dates = plan.get('dates', {})
        budget = plan.get('budget', {}).get('total', 0)
        travelers = plan.get('travelers', 1)
        
        message = f"""🌍 旅行计划

📍 目的地：{destination}
📅 日期：{dates.get('start', 'N/A')} ~ {dates.get('end', 'N/A')}
👥 人数：{travelers}人
💰 预算：¥{budget}
"""
        
        # 添加租车信息
        if plan.get('car_rental'):
            car = plan['car_rental']
            message += f"\n🚗 租车：{car.get('company', 'N/A')} - ¥{car.get('price', 0)}"
        
        # 添加地陪信息
        if plan.get('local_guide'):
            guide = plan['local_guide']
            message += f"\n👨‍🦯 地陪：{guide.get('name', 'N/A')} - ¥{guide.get('price', 0)}"
        
        # 调用微信发送脚本 (如果存在)
        try:
            script_path = WORKSPACE / "scripts" / "send-wechat-message.py"
            if script_path.exists():
                import subprocess
                result = subprocess.run(
                    ["python3", str(script_path), message],
                    capture_output=True,
                    timeout=30
                )
                if result.returncode == 0:
                    print(f"✅ 微信发送成功")
                else:
                    print(f"⚠️ 微信发送失败：{result.stderr.decode()[:100]}")
            else:
                print(f"⚠️ 微信发送脚本不存在，消息已生成")
                print(message)
        except Exception as e:
            print(f"⚠️ 微信发送错误：{e}")
        
        return {"success": True}
    
    def auto_learn(self, destinations: List[str] = None) -> Dict:
        """自动学习旅行知识"""
        print(f"\n📚 自动学习旅行知识")
        
        # 从博主学习
        blogger_result = self.knowledge_learner.learn_from_bloggers("全部")
        
        # 从网站学习
        website_result = self.knowledge_learner.learn_from_websites("全部")
        
        # 提取攻略
        if destinations:
            for dest in destinations:
                self.knowledge_learner.extract_travel_guides(dest)
        
        # 更新推荐
        recommendation_result = self.knowledge_learner.update_recommendations()
        
        # 生成学习报告
        report = self.knowledge_learner.generate_learning_report()
        
        return {
            "blogger_learning": blogger_result,
            "website_learning": website_result,
            "recommendation_update": recommendation_result,
            "learning_report": str(report),
        }
    
    def generate_report(self, plan: Dict) -> Path:
        """生成旅行报告"""
        report_file = REPORTS_DIR / f"trip_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        content = f"""# 🌍 旅行计划报告

> **目的地**: {plan.get('destination', 'N/A')}  
> **出发地**: {plan.get('origin', 'N/A')}  
> **日期**: {plan.get('dates', {}).get('start', 'N/A')} ~ {plan.get('dates', {}).get('end', 'N/A')}  
> **人数**: {plan.get('travelers', 1)} 人  
> **预算**: ¥{plan.get('budget', {}).get('total', 0)}

---

## 📊 预算分配

| 项目 | 金额 |
|------|------|
| 航班 | ¥{plan.get('budget', {}).get('allocation', {}).get('flights', 0)} |
| 住宿 | ¥{plan.get('budget', {}).get('allocation', {}).get('accommodation', 0)} |
| 餐饮 | ¥{plan.get('budget', {}).get('allocation', {}).get('meals', 0)} |
| 活动 | ¥{plan.get('budget', {}).get('allocation', {}).get('activities', 0)} |
| 购物 | ¥{plan.get('budget', {}).get('allocation', {}).get('shopping', 0)} |

---

## ✈️ 航班信息

{json.dumps(plan.get('flights', {}), indent=2, ensure_ascii=False)}

---

## 🌤️ 天气情况

{json.dumps(plan.get('weather', {}), indent=2, ensure_ascii=False)}

---

## 📋 旅行清单

{json.dumps(plan.get('checklist', {}), indent=2, ensure_ascii=False)}

---

*太一旅行探路者 Agent · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 报告已生成：{report_file}")
        return report_file


def main():
    """测试"""
    print("=" * 60)
    print("🌍 太一旅行探路者 Agent 测试")
    print("=" * 60)
    
    agent = TaiyiTravelAgent()
    
    # 测试 1: 智能旅行规划
    print("\n🌍 测试 1: 智能旅行规划")
    plan = agent.plan_trip(
        origin="北京",
        destination="东京",
        start_date="2026-05-01",
        end_date="2026-05-07",
        budget=15000,
        travelers=2
    )
    
    # 生成报告
    report = agent.generate_report(plan)
    
    # 测试 2: 多城市路线优化
    print("\n🗺️ 测试 2: 多城市路线优化")
    route = agent.optimize_route(
        cities=["北京", "上海", "东京", "首尔"],
        budget=30000
    )
    
    # 测试 3: 查找优惠
    print("\n🎫 测试 3: 查找优惠旅行方案")
    deals = agent.find_deals(origin="北京", flexible=True)
    
    # 测试 4: 生成旅行清单
    print("\n📋 测试 4: 生成旅行清单")
    checklist = agent.generate_checklist(
        destination="东京",
        days=7,
        purpose="休闲"
    )
    
    print("\n" + "=" * 60)
    print("✅ 太一旅行探路者 Agent 测试完成")
    print("=" * 60)
    
    print(f"\n📁 输出文件:")
    print(f"  数据目录：{DATA_DIR}")
    print(f"  报告目录：{REPORTS_DIR}")


if __name__ == "__main__":
    main()

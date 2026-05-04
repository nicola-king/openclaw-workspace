#!/usr/bin/env python3
"""
supply-chain v10.0
供应链全链路管理引擎
蒸馏来源：物流优化 + 供应商匹配 + 销售预测 + 天机趋势
"""

import json
import os
import math
from datetime import datetime
from typing import Dict, List, Optional, Any

class SupplyChainManager:
    """供应链全链路管理引擎"""

    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.supplier_db = self._init_supplier_db()

    def _load_config(self, path: str) -> dict:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "supply_chain": {"enabled": True, "auto_optimize": True, "review_interval": 604800},
            "inventory": {"safety_stock_days": 30, "reorder_point_method": "EOQ", "abc_classification": True},
            "logistics": {"optimize_mode": "cost", "max_transit_time": 45, "multi_modal": True}
        }

    def _init_supplier_db(self) -> dict:
        """初始化供应商数据库"""
        return {
            "foldable_house": [
                {
                    "id": "SUP-001",
                    "name": "重庆赛力成钢结构",
                    "location": "重庆",
                    "rating": 4.5,
                    "price_range": [800, 1500],
                    "moq": 1,
                    "lead_time": 15,
                    "certifications": ["ISO9001", "CE"],
                    "capacity": 50
                },
                {
                    "id": "SUP-002",
                    "name": "广东雅居乐集成房屋",
                    "location": "广东",
                    "rating": 4.3,
                    "price_range": [1000, 1800],
                    "moq": 2,
                    "lead_time": 20,
                    "certifications": ["ISO9001", "CE", "ASTM"],
                    "capacity": 80
                }
            ]
        }

    def optimize(self, product: str, market: str, suppliers: Optional[List[str]] = None) -> Dict[str, Any]:
        """供应链全链路优化"""
        result = {
            "product": product,
            "market": market,
            "timestamp": datetime.now().isoformat(),
            "supply_chain_score": 0,
            "suppliers": [],
            "inventory_optimization": {},
            "logistics_plan": {},
            "demand_forecast": {},
            "risks": []
        }

        # 供应商评估
        result["suppliers"] = self._evaluate_suppliers(product, market)

        # 库存优化
        result["inventory_optimization"] = self.optimize_inventory(product, 100, 30)

        # 物流计划
        result["logistics_plan"] = self._optimize_logistics(product, market)

        # 需求预测
        result["demand_forecast"] = self.demand_forecast(product, market, 6)

        # 综合评分
        result["supply_chain_score"] = self._calculate_supply_chain_score(result)

        # 风险识别
        result["risks"] = self._identify_supply_risks(result)

        return result

    def _evaluate_suppliers(self, product: str, market: str) -> List[dict]:
        """供应商评估"""
        suppliers = self.supplier_db.get("foldable_house", [])
        evaluated = []
        for sup in suppliers:
            score = self._score_supplier(sup, market)
            evaluated.append({
                **sup,
                "market_score": score,
                "recommendation": "recommended" if score >= 80 else "backup" if score >= 60 else "not_recommended"
            })
        return sorted(evaluated, key=lambda x: x["market_score"], reverse=True)

    def _score_supplier(self, supplier: dict, market: str) -> int:
        """供应商评分"""
        score = 0
        score += supplier["rating"] * 10  # 45 分
        score += min(20, 30 - supplier["lead_time"])  # 交期越短分数越高
        cert_count = len(supplier["certifications"])
        score += cert_count * 5  # 认证加分
        if "ASTM" in supplier["certifications"] and market == "USA":
            score += 15
        if "CE" in supplier["certifications"] and market in ["Australia", "EU"]:
            score += 10
        return min(100, score)

    def optimize_inventory(self, product: str, current_stock: int, lead_time: int) -> Dict[str, Any]:
        """库存优化"""
        # 简化的 EOQ 模型
        daily_demand = 2  # 假设日均需求
        holding_cost = 5  # 单位持有成本
        ordering_cost = 200  # 订货成本

        # EOQ = sqrt(2DS/H)
        annual_demand = daily_demand * 365
        eoq = math.sqrt(2 * annual_demand * ordering_cost / holding_cost)

        # 安全库存 = 日均需求 × 提前期 × 安全系数
        safety_stock = daily_demand * lead_time * 1.5

        # 再订货点
        reorder_point = daily_demand * lead_time + safety_stock

        return {
            "product": product,
            "current_stock": current_stock,
            "eoq": round(eoq),
            "safety_stock": round(safety_stock),
            "reorder_point": round(reorder_point),
            "status": "adequate" if current_stock > reorder_point else "reorder_needed",
            "recommendation": f"建议订货 {round(eoq)} 单位" if current_stock <= reorder_point else "库存充足"
        }

    def _optimize_logistics(self, product: str, market: str) -> Dict[str, Any]:
        """物流优化"""
        routes = {
            "Australia": [
                {"mode": "sea", "route": "重庆→上海→悉尼", "days": 30, "cost": 3500, "capacity": "40HQ"},
                {"mode": "sea", "route": "重庆→广州→悉尼", "days": 25, "cost": 3200, "capacity": "40HQ"},
                {"mode": "rail+sea", "route": "重庆→新加坡→悉尼", "days": 35, "cost": 2800, "capacity": "40HQ"}
            ],
            "USA": [
                {"mode": "sea", "route": "重庆→上海→洛杉矶", "days": 25, "cost": 4000, "capacity": "40HQ"},
                {"mode": "sea", "route": "重庆→深圳→洛杉矶", "days": 22, "cost": 3800, "capacity": "40HQ"}
            ],
            "EU": [
                {"mode": "rail", "route": "重庆→杜伊斯堡", "days": 18, "cost": 5000, "capacity": "40HQ"},
                {"mode": "sea", "route": "重庆→上海→汉堡", "days": 35, "cost": 3500, "capacity": "40HQ"}
            ]
        }

        available_routes = routes.get(market, routes["Australia"])
        # 按成本排序
        best_route = min(available_routes, key=lambda x: x["cost"])

        return {
            "product": product,
            "market": market,
            "available_routes": available_routes,
            "recommended_route": best_route,
            "optimization": f"推荐 {best_route['mode']} 路线，成本 {best_route['cost']} USD，时效 {best_route['days']} 天"
        }

    def demand_forecast(self, product: str, market: str, horizon_months: int = 6) -> Dict[str, Any]:
        """需求预测"""
        import random
        base_demand = 50  # 月均基础需求
        seasonal_factors = {
            1: 0.8, 2: 0.7, 3: 1.0, 4: 1.2, 5: 1.3, 6: 1.1,
            7: 0.9, 8: 1.0, 9: 1.2, 10: 1.3, 11: 1.0, 12: 0.8
        }

        forecast = []
        current_month = datetime.now().month
        for i in range(horizon_months):
            month = (current_month + i - 1) % 12 + 1
            factor = seasonal_factors.get(month, 1.0)
            demand = int(base_demand * factor * (1 + random.uniform(-0.1, 0.1)))
            forecast.append({
                "month": month,
                "predicted_demand": demand,
                "seasonal_factor": factor,
                "confidence": 0.85 - i * 0.05
            })

        return {
            "product": product,
            "market": market,
            "horizon_months": horizon_months,
            "forecast": forecast,
            "total_predicted": sum(f["predicted_demand"] for f in forecast),
            "peak_month": max(forecast, key=lambda x: x["predicted_demand"])["month"],
            "recommendation": "建议在旺季前 2 个月增加库存"
        }

    def _calculate_supply_chain_score(self, result: dict) -> int:
        """计算供应链综合评分"""
        score = 0
        # 供应商评分
        if result["suppliers"]:
            score += result["suppliers"][0].get("market_score", 50) * 0.3
        # 库存评分
        inv = result.get("inventory_optimization", {})
        score += 20 if inv.get("status") == "adequate" else 10
        # 物流评分
        logistics = result.get("logistics_plan", {})
        route = logistics.get("recommended_route", {})
        score += 20 if route.get("days", 99) < 30 else 10
        # 预测评分
        forecast = result.get("demand_forecast", {})
        score += 15 if forecast else 5
        return min(100, round(score))

    def _identify_supply_risks(self, result: dict) -> List[str]:
        """识别供应链风险"""
        risks = []
        if result["inventory_optimization"].get("status") == "reorder_needed":
            risks.append("库存不足，需立即补货")
        if len(result.get("suppliers", [])) < 2:
            risks.append("供应商单一，建议开发备选供应商")
        logistics = result.get("logistics_plan", {})
        route = logistics.get("recommended_route", {})
        if route.get("days", 0) > 30:
            risks.append("物流时效较长，考虑多式联运")
        return risks


if __name__ == "__main__":
    manager = SupplyChainManager()
    result = manager.optimize("折叠房屋", "Australia")
    print(json.dumps(result, ensure_ascii=False, indent=2))

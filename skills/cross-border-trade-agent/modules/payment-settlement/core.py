#!/usr/bin/env python3
"""
payment-settlement v10.0
支付结算与汇率管理引擎
蒸馏来源：金融情报 + 天机 + 汇率预测 + 二阶思维
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class PaymentSettlement:
    """支付结算与汇率管理引擎"""

    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.exchange_rates = self._init_exchange_rates()
        self.payment_methods = self._init_payment_methods()

    def _load_config(self, path: str) -> dict:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "payment": {"enabled": True, "default_method": "TT", "supported_methods": ["TT", "LC", "D/P", "PayPal", "Stripe"]},
            "exchange": {"auto_hedge": False, "hedge_threshold": 0.03, "monitor_interval": 3600},
            "risk": {"fraud_detection": True, "credit_check": True, "alert_threshold": 0.05}
        }

    def _init_exchange_rates(self) -> dict:
        """初始化汇率数据库（模拟）"""
        return {
            "CNY/AUD": {"rate": 0.21, "spread": 0.003, "trend": "stable"},
            "CNY/USD": {"rate": 0.14, "spread": 0.002, "trend": "stable"},
            "CNY/EUR": {"rate": 0.13, "spread": 0.003, "trend": "weak"},
            "CNY/GBP": {"rate": 0.11, "spread": 0.004, "trend": "stable"},
            "CNY/JPY": {"rate": 21.5, "spread": 0.005, "trend": "strong"},
            "USD/AUD": {"rate": 1.52, "spread": 0.002, "trend": "stable"},
            "USD/EUR": {"rate": 0.92, "spread": 0.002, "trend": "stable"},
            "AUD/USD": {"rate": 0.66, "spread": 0.003, "trend": "weak"}
        }

    def _init_payment_methods(self) -> dict:
        """初始化支付方式"""
        return {
            "TT": {
                "name": "电汇 (Telegraphic Transfer)",
                "fee_rate": 0.003,
                "min_fee": 50,
                "max_fee": 500,
                "settlement_days": 3,
                "risk_level": "LOW",
                "suitable_for": ["B2B", "large_amount"]
            },
            "LC": {
                "name": "信用证 (Letter of Credit)",
                "fee_rate": 0.008,
                "min_fee": 200,
                "max_fee": 2000,
                "settlement_days": 7,
                "risk_level": "VERY_LOW",
                "suitable_for": ["B2B", "new_customer", "large_amount"]
            },
            "D/P": {
                "name": "付款交单 (Documents against Payment)",
                "fee_rate": 0.005,
                "min_fee": 100,
                "max_fee": 1000,
                "settlement_days": 5,
                "risk_level": "MEDIUM",
                "suitable_for": ["B2B", "medium_amount"]
            },
            "PayPal": {
                "name": "PayPal",
                "fee_rate": 0.044,
                "min_fee": 0.3,
                "max_fee": None,
                "settlement_days": 1,
                "risk_level": "MEDIUM",
                "suitable_for": ["B2C", "small_amount", "sample"]
            },
            "Stripe": {
                "name": "Stripe",
                "fee_rate": 0.029,
                "min_fee": 0.3,
                "max_fee": None,
                "settlement_days": 2,
                "risk_level": "LOW",
                "suitable_for": ["B2C", "small_amount", "online"]
            }
        }

    def settle(self, amount: float, from_currency: str, to_currency: str,
               payment_method: str = "TT") -> Dict[str, Any]:
        """结算计算"""
        pair = f"{from_currency}/{to_currency}"
        rate_data = self.exchange_rates.get(pair, {})
        rate = rate_data.get("rate", 1.0)
        spread = rate_data.get("spread", 0.005)

        # 实际汇率 = 中间价 - 点差
        actual_rate = rate * (1 - spread)
        converted_amount = amount * actual_rate

        # 手续费
        method = self.payment_methods.get(payment_method, {})
        fee_rate = method.get("fee_rate", 0.003)
        fee = max(method.get("min_fee", 0), min(amount * fee_rate, method.get("max_fee", float('inf'))))

        net_amount = converted_amount - fee

        result = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "original_amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "exchange_rate": rate,
            "actual_rate": round(actual_rate, 6),
            "spread": spread,
            "converted_amount": round(converted_amount, 2),
            "payment_method": payment_method,
            "fee": round(fee, 2),
            "net_amount": round(net_amount, 2),
            "settlement_days": method.get("settlement_days", 3),
            "risk_level": method.get("risk_level", "MEDIUM"),
            "trend": rate_data.get("trend", "unknown"),
            "hedge_recommendation": self._check_hedge_needed(rate_data)
        }

        return result

    def _check_hedge_needed(self, rate_data: dict) -> Optional[dict]:
        """检查是否需要锁汇"""
        trend = rate_data.get("trend", "stable")
        if trend in ["weak", "strong"]:
            return {
                "needed": True,
                "reason": f"汇率趋势 {trend}，建议锁汇",
                "method": "forward_contract",
                "duration": "3个月"
            }
        return None

    def monitor_exchange_rate(self, pair: str) -> Dict[str, Any]:
        """汇率监控"""
        rate_data = self.exchange_rates.get(pair, {})
        return {
            "pair": pair,
            "current_rate": rate_data.get("rate", 0),
            "trend": rate_data.get("trend", "unknown"),
            "spread": rate_data.get("spread", 0),
            "timestamp": datetime.now().isoformat(),
            "alert": None
        }

    def assess_payment_risk(self, buyer: str, amount: float, currency: str) -> Dict[str, Any]:
        """支付风险评估"""
        risk_score = 50  # 基础分数

        # 金额风险
        if amount > 100000:
            risk_score += 20
        elif amount > 50000:
            risk_score += 10

        # 币种风险
        if currency in ["ARS", "TRY", "VEF"]:
            risk_score += 30
        elif currency in ["USD", "EUR", "AUD", "GBP"]:
            risk_score -= 10

        risk_level = "LOW" if risk_score < 40 else "MEDIUM" if risk_score < 70 else "HIGH"

        return {
            "buyer": buyer,
            "amount": amount,
            "currency": currency,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "recommendation": self._get_risk_recommendation(risk_level),
            "timestamp": datetime.now().isoformat()
        }

    def _get_risk_recommendation(self, risk_level: str) -> str:
        """获取风险建议"""
        recommendations = {
            "LOW": "风险较低，可使用 TT 或 PayPal",
            "MEDIUM": "风险中等，建议使用 LC 或 D/P",
            "HIGH": "风险较高，必须使用 LC，建议购买信用保险"
        }
        return recommendations.get(risk_level, "请进一步评估")

    def compare_payment_methods(self, amount: float) -> List[dict]:
        """支付方式对比"""
        comparisons = []
        for method_id, method in self.payment_methods.items():
            fee = max(method["min_fee"], min(amount * method["fee_rate"], method.get("max_fee") or float('inf')))
            comparisons.append({
                "method": method_id,
                "name": method["name"],
                "fee": round(fee, 2),
                "fee_rate": method["fee_rate"],
                "settlement_days": method["settlement_days"],
                "risk_level": method["risk_level"]
            })
        return sorted(comparisons, key=lambda x: x["fee"])


if __name__ == "__main__":
    ps = PaymentSettlement()
    result = ps.settle(50000, "CNY", "AUD", "TT")
    print(json.dumps(result, ensure_ascii=False, indent=2))

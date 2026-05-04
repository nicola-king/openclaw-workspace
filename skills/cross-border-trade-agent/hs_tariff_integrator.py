#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HS 关税代码查询集成模块 - Deftship 核心能力
太一 AGI · 2026-04-20 21:25

功能:
- HS 关税代码查询 (Deftship)
- 产品关税分类
- 关税税率计算
- 海关合规检查
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('HSTariffIntegrator')

WORKSPACE = Path("/home/sayelf/.openclaw/workspace")
HS_DIR = WORKSPACE / "data" / "cross-border" / "hs_tariff"
HS_DIR.mkdir(parents=True, exist_ok=True)


class HSTariffIntegrator:
    """HS 关税代码查询集成模块"""
    
    # HS 编码前缀分类
    HS_CATEGORIES = {
        "01-05": "动物产品",
        "06-15": "植物产品",
        "16-24": "食品饮料",
        "25-27": "矿产品",
        "28-38": "化工产品",
        "39-40": "塑料橡胶",
        "41-43": "皮革制品",
        "44-46": "木制品",
        "47-49": "纸制品",
        "50-63": "纺织品",
        "64-67": "鞋类",
        "68-70": "石材陶瓷",
        "71-71": "珠宝贵金属",
        "72-83": "金属制品",
        "84-85": "机械设备",
        "86-89": "交通工具",
        "90-92": "仪器仪表",
        "93-93": "武器弹药",
        "94-96": "杂项制品"
    }
    
    def __init__(self):
        self.hs_file = HS_DIR / "hs_tariff.json"
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        if self.hs_file.exists():
            with open(self.hs_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"queries": [], "classifications": [], "tariff_rates": []}
    
    def query_hs_code(self, product_description: str, target_country: str = "US") -> Dict:
        """查询 HS 关税代码 (Deftship 核心功能)"""
        logger.info(f"🔍 查询 HS 代码：{product_description} ({target_country})")
        
        query_result = {
            "id": f"HS_QUERY_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "product_description": product_description,
            "target_country": target_country,
            "timestamp": datetime.now().isoformat(),
            "hs_code": self._classify_product(product_description),
            "tariff_rate": self._get_tariff_rate(product_description, target_country),
            "requirements": self._get_customs_requirements(product_description, target_country),
            "recommendations": []
        }
        
        # 生成建议
        query_result["recommendations"] = self._generate_recommendations(query_result)
        
        self.data["queries"].append(query_result)
        self._save_data()
        
        logger.info(f"✅ HS 代码查询完成：{query_result['hs_code']['code']}")
        return query_result
    
    def _classify_product(self, description: str) -> Dict:
        """产品分类 (AI 分类)"""
        # 模拟 AI 分类 (实际应调用 Deftship API 或本地 AI 模型)
        keywords = description.lower()
        
        hs_mapping = {
            "power": {"code": "8507.60", "description": "锂离子电池"},
            "solar": {"code": "8541.40", "description": "太阳能电池"},
            "battery": {"code": "8506", "description": "原电池"},
            "phone": {"code": "8517.12", "description": "智能手机"},
            "laptop": {"code": "8471.30", "description": "笔记本电脑"},
            "clothing": {"code": "61", "description": "针织服装"},
            "shoes": {"code": "64", "description": "鞋类"},
            "furniture": {"code": "94", "description": "家具"},
            "toy": {"code": "9503", "description": "玩具"},
            "watch": {"code": "9102", "description": "手表"}
        }
        
        for keyword, hs_info in hs_mapping.items():
            if keyword in keywords:
                return {
                    "code": hs_info["code"],
                    "description": hs_info["description"],
                    "category": self._get_category(hs_info["code"]),
                    "confidence": 0.85
                }
        
        # 默认分类
        return {
            "code": "9999.99",
            "description": "需人工确认",
            "category": "杂项制品",
            "confidence": 0.50
        }
    
    def _get_category(self, hs_code: str) -> str:
        """获取 HS 编码类别"""
        try:
            prefix = int(hs_code.split(".")[0][:2])
            for code_range, category in self.HS_CATEGORIES.items():
                start, end = map(int, code_range.split("-"))
                if start <= prefix <= end:
                    return category
        except:
            pass
        return "未知类别"
    
    def _get_tariff_rate(self, description: str, country: str) -> Dict:
        """获取关税税率"""
        # 模拟税率数据 (实际应查询官方关税数据库)
        tariff_rates = {
            "US": {"rate": 5.5, "currency": "USD"},
            "EU": {"rate": 7.0, "currency": "EUR"},
            "JP": {"rate": 4.0, "currency": "JPY"},
            "UK": {"rate": 6.5, "currency": "GBP"},
            "CA": {"rate": 5.0, "currency": "CAD"},
            "AU": {"rate": 5.0, "currency": "AUD"}
        }
        
        rate_info = tariff_rates.get(country, {"rate": 5.0, "currency": "USD"})
        
        return {
            "rate": rate_info["rate"],
            "currency": rate_info["currency"],
            "calculation_base": "CIF 价值",
            "additional_taxes": self._get_additional_taxes(country)
        }
    
    def _get_additional_taxes(self, country: str) -> List[Dict]:
        """获取附加税"""
        taxes = {
            "US": [{"name": "关税", "rate": "varies"}],
            "EU": [{"name": "VAT", "rate": "19-27%"}, {"name": "关税", "rate": "varies"}],
            "UK": [{"name": "VAT", "rate": "20%"}, {"name": "关税", "rate": "varies"}],
            "JP": [{"name": "消费税", "rate": "10%"}, {"name": "关税", "rate": "varies"}]
        }
        return taxes.get(country, [{"name": "关税", "rate": "varies"}])
    
    def _get_customs_requirements(self, description: str, country: str) -> Dict:
        """获取海关要求"""
        return {
            "documents_required": [
                "商业发票",
                "装箱单",
                "提单",
                "原产地证"
            ],
            "certifications": self._get_required_certifications(description, country),
            "restrictions": self._get_restrictions(description, country),
            "processing_time": "3-5 工作日"
        }
    
    def _get_required_certifications(self, description: str, country: str) -> List[str]:
        """获取所需认证"""
        certs = []
        keywords = description.lower()
        
        if "battery" in keywords or "power" in keywords:
            certs.extend(["UN38.3", "MSDS", "CE"])
        if "electronic" in keywords or "electric" in keywords:
            certs.extend(["CE", "FCC", "RoHS"])
        if "food" in keywords:
            certs.extend(["FDA", "HACCP"])
        if "toy" in keywords:
            certs.extend(["EN71", "ASTM F963"])
        
        return certs
    
    def _get_restrictions(self, description: str, country: str) -> List[str]:
        """获取限制条件"""
        restrictions = []
        
        # 模拟限制检查
        if "battery" in description.lower():
            restrictions.append("锂电池运输限制")
        if "liquid" in description.lower():
            restrictions.append("液体运输限制")
        
        return restrictions
    
    def _generate_recommendations(self, query_result: Dict) -> List[Dict]:
        """生成建议"""
        recommendations = []
        
        # HS 代码置信度低
        if query_result["hs_code"]["confidence"] < 0.7:
            recommendations.append({
                "priority": "P0",
                "category": "HS 分类",
                "action": "建议人工确认 HS 编码",
                "reason": f"AI 分类置信度仅{query_result['hs_code']['confidence']*100:.0f}%"
            })
        
        # 关税税率高
        if query_result["tariff_rate"]["rate"] > 10:
            recommendations.append({
                "priority": "P1",
                "category": "关税优化",
                "action": "考虑自由贸易协定优惠税率",
                "reason": f"当前税率{query_result['tariff_rate']['rate']}%较高"
            })
        
        # 认证要求
        if query_result["requirements"]["certifications"]:
            recommendations.append({
                "priority": "P0",
                "category": "合规认证",
                "action": f"准备认证：{', '.join(query_result['requirements']['certifications'])}",
                "reason": "目标市场强制要求"
            })
        
        return recommendations
    
    def calculate_landed_cost(self, product_value: float, hs_query_result: Dict) -> Dict:
        """计算到岸成本"""
        logger.info(f"💰 计算到岸成本：${product_value}")
        
        tariff_rate = hs_query_result["tariff_rate"]["rate"] / 100
        tariff_amount = product_value * tariff_rate
        
        # 估算其他费用
        shipping = product_value * 0.15  # 运费 15%
        insurance = product_value * 0.01  # 保险 1%
        handling = 50  # 手续费固定
        
        total_landed_cost = product_value + tariff_amount + shipping + insurance + handling
        
        calculation = {
            "id": f"LANDED_COST_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "product_value": product_value,
            "tariff": tariff_amount,
            "shipping": shipping,
            "insurance": insurance,
            "handling": handling,
            "total_landed_cost": total_landed_cost,
            "effective_rate": round((total_landed_cost - product_value) / product_value * 100, 2),
            "calculated_at": datetime.now().isoformat()
        }
        
        self.data["tariff_rates"].append(calculation)
        self._save_data()
        
        logger.info(f"✅ 到岸成本计算完成：${total_landed_cost:.2f}")
        return calculation
    
    def batch_query(self, products: List[Dict], target_country: str = "US") -> List[Dict]:
        """批量查询 HS 代码"""
        logger.info(f"📦 批量查询 HS 代码：{len(products)}个产品")
        
        results = []
        for product in products:
            result = self.query_hs_code(product["description"], target_country)
            result["product_name"] = product.get("name", "Unknown")
            results.append(result)
        
        logger.info(f"✅ 批量查询完成：{len(results)}个产品")
        return results
    
    def _save_data(self):
        HS_DIR.mkdir(parents=True, exist_ok=True)
        with open(self.hs_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def get_summary(self) -> Dict:
        """获取 HS 关税集成摘要"""
        return {
            "total_queries": len(self.data["queries"]),
            "total_classifications": len(self.data["classifications"]),
            "total_calculations": len(self.data["tariff_rates"])
        }


def main():
    logger.info("=" * 60)
    logger.info("🌍 HS 关税代码查询集成 - Deftship 核心能力")
    logger.info("=" * 60)
    
    integrator = HSTariffIntegrator()
    
    # 演示 HS 代码查询
    logger.info(f"\n🔍 查询 HS 代码...")
    result = integrator.query_hs_code("portable power station 20000mAh", "US")
    logger.info(f"  HS 代码：{result['hs_code']['code']}")
    logger.info(f"  产品描述：{result['hs_code']['description']}")
    logger.info(f"  类别：{result['hs_code']['category']}")
    logger.info(f"  关税税率：{result['tariff_rate']['rate']}%")
    logger.info(f"  所需认证：{result['requirements']['certifications']}")
    logger.info(f"  建议数：{len(result['recommendations'])}条")
    
    # 演示到岸成本计算
    logger.info(f"\n💰 计算到岸成本...")
    landed = integrator.calculate_landed_cost(100, result)
    logger.info(f"  产品价值：${100}")
    logger.info(f"  关税：${landed['tariff']:.2f}")
    logger.info(f"  总到岸成本：${landed['total_landed_cost']:.2f}")
    logger.info(f"  综合税率：{landed['effective_rate']}%")
    
    # 获取摘要
    logger.info(f"\n📊 HS 关税集成摘要:")
    summary = integrator.get_summary()
    logger.info(f"  总查询：{summary['total_queries']}次")
    logger.info(f"  总分类：{summary['total_classifications']}个")
    logger.info(f"  总计算：{summary['total_calculations']}个")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ HS 关税查询演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()

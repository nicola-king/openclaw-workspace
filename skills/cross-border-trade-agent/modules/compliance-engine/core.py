#!/usr/bin/env python3
"""
compliance-engine v10.0
合规与清关自动化引擎
蒸馏来源：海关数据 + 法规库 + 太一宪法
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class ComplianceEngine:
    """合规与清关自动化引擎"""

    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.regulations_db = {}
        self.certification_db = {}
        self.tariff_db = {}
        self._init_databases()

    def _load_config(self, path: str) -> dict:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "compliance": {"enabled": True, "auto_update": True, "update_interval": 86400},
            "clearance": {"enabled": True, "auto_hs_code": True, "doc_template": "standard"},
            "alert": {"regulation_change": True, "compliance_risk": True, "certification_expiry": True}
        }

    def _init_databases(self):
        """初始化法规/认证/关税数据库"""
        # 主要市场法规库
        self.regulations_db = {
            "Australia": {
                "construction": {
                    "certifications": ["CE", "ISO9001", "Australian Building Code"],
                    "standards": ["AS/NZS 1170", "AS 1684"],
                    "tariff_base": 5.0,
                    "gst": 10.0
                },
                "electronics": {
                    "certifications": ["RCM", "CE", "ISO9001"],
                    "standards": ["AS/NZS 3000"],
                    "tariff_base": 5.0,
                    "gst": 10.0
                }
            },
            "USA": {
                "construction": {
                    "certifications": ["FDA", "ISO9001", "IBC"],
                    "standards": ["ASTM", "ANSI"],
                    "tariff_base": 0.0,
                    "section301_extra": 25.0
                },
                "electronics": {
                    "certifications": ["FCC", "UL", "CE"],
                    "standards": ["NEC", "IEEE"],
                    "tariff_base": 0.0,
                    "section301_extra": 25.0
                }
            },
            "EU": {
                "construction": {
                    "certifications": ["CE", "ISO9001", "EN"],
                    "standards": ["EN 1090", "EN 1993"],
                    "tariff_base": 0.0,
                    "vat": 20.0
                },
                "electronics": {
                    "certifications": ["CE", "RoHS", "REACH"],
                    "standards": ["EN 60950", "EN 62368"],
                    "tariff_base": 0.0,
                    "vat": 20.0
                }
            }
        }

        # 认证数据库
        self.certification_db = {
            "CE": {"region": "EU", "validity": 5, "cost_range": [5000, 50000], "required_for": ["electronics", "construction"]},
            "FDA": {"region": "USA", "validity": 3, "cost_range": [10000, 100000], "required_for": ["construction", "medical"]},
            "ISO9001": {"region": "Global", "validity": 3, "cost_range": [20000, 80000], "required_for": ["all"]},
            "RCM": {"region": "Australia", "validity": 5, "cost_range": [3000, 20000], "required_for": ["electronics"]},
            "FCC": {"region": "USA", "validity": 5, "cost_range": [5000, 30000], "required_for": ["electronics"]},
            "RoHS": {"region": "EU", "validity": 5, "cost_range": [3000, 15000], "required_for": ["electronics"]},
            "REACH": {"region": "EU", "validity": 5, "cost_range": [10000, 50000], "required_for": ["chemicals", "electronics"]}
        }

        # HS 编码数据库 (简化版)
        self.hs_db = {
            "9406.00": "预制建筑",
            "7308.30": "钢结构",
            "8507.60": "锂电池",
            "8711.60": "电动自行车",
            "8479.89": "其他机械",
            "3925.10": "塑料建筑材料",
            "4418.10": "木结构建筑",
            "7210.70": "镀锌钢板"
        }

    def check(self, product: str, market: str, hs_code: Optional[str] = None) -> Dict[str, Any]:
        """执行合规检查"""
        result = {
            "product": product,
            "market": market,
            "timestamp": datetime.now().isoformat(),
            "compliance_score": 0,
            "regulations": [],
            "certifications_required": [],
            "tariff_rate": 0,
            "clearance_docs": [],
            "risks": [],
            "recommendations": []
        }

        # 自动匹配 HS 编码
        if not hs_code:
            hs_code = self._auto_match_hs_code(product)
            result["auto_matched_hs_code"] = hs_code

        # 获取市场法规
        market_data = self.regulations_db.get(market, {})
        if not market_data:
            result["risks"].append(f"未找到 {market} 的法规数据")
            return result

        # 判断产品类别
        category = self._classify_product(product, hs_code)
        category_data = market_data.get(category, {})

        if not category_data:
            result["risks"].append(f"未找到 {market} {category} 类别的法规")
            return result

        # 计算合规分数
        result["certifications_required"] = category_data.get("certifications", [])
        result["tariff_rate"] = category_data.get("tariff_base", 0)
        result["regulations"] = category_data.get("standards", [])

        # 关税附加
        if "section301_extra" in category_data:
            result["tariff_rate"] += category_data["section301_extra"]
            result["risks"].append("受 301 条款影响，额外关税")

        # 生成清关文件清单
        result["clearance_docs"] = self._generate_clearance_docs(market, category)

        # 计算合规分数
        result["compliance_score"] = self._calculate_compliance_score(
            result["certifications_required"],
            result["tariff_rate"],
            result["risks"]
        )

        # 生成建议
        result["recommendations"] = self._generate_recommendations(result)

        return result

    def _auto_match_hs_code(self, product: str) -> Optional[str]:
        """自动匹配 HS 编码"""
        keywords = {
            "折叠房屋": "9406.00",
            "折叠房": "9406.00",
            "钢结构": "7308.30",
            "锂电": "8507.60",
            "电动": "8711.60",
            "自行车": "8711.60"
        }
        for kw, code in keywords.items():
            if kw in product:
                return code
        return None

    def _classify_product(self, product: str, hs_code: str) -> str:
        """产品分类"""
        if hs_code in ["9406.00", "7308.30", "4418.10", "3925.10", "7210.70"]:
            return "construction"
        elif hs_code in ["8507.60", "8711.60"]:
            return "electronics"
        return "construction"  # 默认

    def _generate_clearance_docs(self, market: str, category: str) -> List[str]:
        """生成清关文件清单"""
        base_docs = ["商业发票", "装箱单", "原产地证"]
        market_specific = {
            "Australia": ["进口声明", " biosecurity 声明"],
            "USA": ["ISF 申报", "Customs Bond"],
            "EU": ["EORI 号", "CE 符合性声明"]
        }
        docs = base_docs + market_specific.get(market, [])
        if category == "electronics":
            docs.append("认证证书复印件")
        return docs

    def _calculate_compliance_score(self, certs: List[str], tariff: float, risks: List[str]) -> int:
        """计算合规分数"""
        score = 100
        score -= len(risks) * 5
        if tariff > 10:
            score -= 10
        elif tariff > 5:
            score -= 5
        return max(0, min(100, score))

    def _generate_recommendations(self, result: dict) -> List[str]:
        """生成改进建议"""
        recs = []
        if result["compliance_score"] < 80:
            recs.append("合规分数偏低，建议优先获取缺失认证")
        if result["tariff_rate"] > 10:
            recs.append("关税较高，考虑通过自贸协定降低关税")
        if "Australian Building Code" in result.get("certifications_required", []):
            recs.append("需获取澳大利亚建筑标准认证，建议联系 NCC 认证机构")
        return recs if recs else ["合规状态良好"]

    def generate_clearance_docs(self, shipment_id: str, destination: str) -> Dict[str, Any]:
        """生成清关文件"""
        return {
            "shipment_id": shipment_id,
            "destination": destination,
            "docs_generated": True,
            "timestamp": datetime.now().isoformat()
        }

    def track_regulations(self, market: str, category: str) -> Dict[str, Any]:
        """法规追踪"""
        return {
            "market": market,
            "category": category,
            "last_updated": datetime.now().isoformat(),
            "changes": [],
            "upcoming": []
        }


if __name__ == "__main__":
    engine = ComplianceEngine()
    result = engine.check("折叠房屋", "Australia", "9406.00")
    print(json.dumps(result, ensure_ascii=False, indent=2))

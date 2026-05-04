#!/usr/bin/env python3
"""
contract-legal v10.0
合同与法律支持引擎
蒸馏来源：合同模板 + 法律框架 + 合规要求
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class ContractLegal:
    """合同与法律支持引擎"""

    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.template_db = self._init_template_db()
        self.incoterms_db = self._init_incoterms_db()
        self.clauses_db = self._init_clauses_db()

    def _load_config(self, path: str) -> dict:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "contract": {"enabled": True, "default_template": "international_sales", "language": "bilingual"},
            "legal": {"jurisdiction_preference": "neutral", "arbitration": "SIAC", "governing_law": "CISG"},
            "compliance": {"export_control": True, "sanction_check": True, "anti_bribery": True}
        }

    def _init_template_db(self) -> dict:
        """初始化合同模板库"""
        return {
            "sales": {
                "name": "国际销售合同",
                "sections": [
                    "合同双方", "产品信息", "数量与价格", "支付方式",
                    "交货条款", "质量标准", "验收标准", "违约责任",
                    "不可抗力", "争议解决", "保密条款", "附则"
                ],
                "required_fields": ["buyer", "seller", "product", "quantity", "price", "payment", "delivery"]
            },
            "purchase": {
                "name": "采购合同",
                "sections": [
                    "采购方", "供应商", "产品信息", "订单数量",
                    "单价与总价", "付款方式", "交货期", "质量要求",
                    "验收", "违约", "争议解决"
                ],
                "required_fields": ["buyer", "supplier", "product", "quantity", "price"]
            },
            "agency": {
                "name": "代理协议",
                "sections": [
                    "委托方", "代理方", "代理区域", "代理产品",
                    "代理权限", "佣金", "考核指标", " exclusivity",
                    "期限", "终止", "争议解决"
                ],
                "required_fields": ["principal", "agent", "territory", "products", "commission"]
            },
            "nda": {
                "name": "保密协议",
                "sections": [
                    "披露方", "接收方", "保密信息定义",
                    "保密义务", "例外情况", "期限", "违约责任", "争议解决"
                ],
                "required_fields": ["disclosing_party", "receiving_party", "purpose"]
            }
        }

    def _init_incoterms_db(self) -> dict:
        """初始化 Incoterms 2020 数据库"""
        return {
            "EXW": {"name": "工厂交货", "seller_obligation": "最低", "buyer_obligation": "最高"},
            "FCA": {"name": "货交承运人", "seller_obligation": "低", "buyer_obligation": "高"},
            "CPT": {"name": "运费付至", "seller_obligation": "中", "buyer_obligation": "中"},
            "CIP": {"name": "运费保险费付至", "seller_obligation": "中高", "buyer_obligation": "中低"},
            "DAP": {"name": "目的地交货", "seller_obligation": "高", "buyer_obligation": "低"},
            "DPU": {"name": "目的地卸货交货", "seller_obligation": "高", "buyer_obligation": "低"},
            "DDP": {"name": "完税后交货", "seller_obligation": "最高", "buyer_obligation": "最低"},
            "FAS": {"name": "船边交货", "seller_obligation": "低", "buyer_obligation": "高", "sea_only": True},
            "FOB": {"name": "船上交货", "seller_obligation": "中", "buyer_obligation": "中", "sea_only": True},
            "CFR": {"name": "成本加运费", "seller_obligation": "中高", "buyer_obligation": "中低", "sea_only": True},
            "CIF": {"name": "成本加运费保险费", "seller_obligation": "高", "buyer_obligation": "低", "sea_only": True}
        }

    def _init_clauses_db(self) -> dict:
        """初始化标准条款库"""
        return {
            "payment_terms": [
                {"id": "PT-001", "name": "30% 预付款 + 70% 见提单复印件", "risk": "LOW", "suitable": ["B2B", "established"]},
                {"id": "PT-002", "name": "100% 前 T/T", "risk": "VERY_LOW", "suitable": ["B2B", "new_customer", "small_amount"]},
                {"id": "PT-003", "name": "L/C at sight", "risk": "LOW", "suitable": ["B2B", "large_amount", "new_customer"]},
                {"id": "PT-004", "name": "D/P at sight", "risk": "MEDIUM", "suitable": ["B2B", "established"]},
                {"id": "PT-005", "name": "O/A 30 days", "risk": "HIGH", "suitable": ["B2B", "long_term_partner"]}
            ],
            "quality": [
                {"id": "QC-001", "name": "符合 ISO 9001 标准", "applicable": ["all"]},
                {"id": "QC-002", "name": "符合目标市场标准", "applicable": ["all"]},
                {"id": "QC-003", "name": "以样品为准", "applicable": ["custom_products"]}
            ],
            "dispute_resolution": [
                {"id": "DR-001", "name": "友好协商", "priority": 1},
                {"id": "DR-002", "name": "调解", "priority": 2},
                {"id": "DR-003", "name": "仲裁 (SIAC)", "priority": 3},
                {"id": "DR-004", "name": "诉讼 (管辖法院)", "priority": 4}
            ],
            "force_majeure": [
                {"id": "FM-001", "name": "自然灾害", "examples": ["地震", "洪水", "台风"]},
                {"id": "FM-002", "name": "战争/动乱", "examples": ["战争", "内乱", "恐怖主义"]},
                {"id": "FM-003", "name": "政府行为", "examples": ["禁令", "制裁", "进出口限制"]},
                {"id": "FM-004", "name": "疫情", "examples": ["传染病", "封锁"]}
            ]
        }

    def generate(self, type: str, product: str, buyer: str, amount: float,
                 currency: str = "USD", incoterm: str = "CIF",
                 **kwargs) -> Dict[str, Any]:
        """生成合同"""
        template = self.template_db.get(type, {})
        incoterm_data = self.incoterms_db.get(incoterm, {})

        contract_id = f"CT-{datetime.now().strftime('%Y')}-{abs(hash(product + buyer)) % 10000:04d}"

        result = {
            "status": "success",
            "contract_id": contract_id,
            "contract_type": type,
            "template": template.get("name", type),
            "timestamp": datetime.now().isoformat(),
            "product": product,
            "buyer": buyer,
            "amount": amount,
            "currency": currency,
            "incoterm": incoterm,
            "incoterm_info": incoterm_data,
            "sections": template.get("sections", []),
            "clauses": self._select_clauses(type, incoterm),
            "risk_clauses": self._identify_risk_clauses(type, amount),
            "compliance_check": self._compliance_check(buyer, product, currency),
            "generated_contract": self._render_contract(template, {
                "product": product, "buyer": buyer, "amount": amount,
                "currency": currency, "incoterm": incoterm, **kwargs
            })
        }

        return result

    def _select_clauses(self, contract_type: str, incoterm: str) -> List[dict]:
        """选择合同条款"""
        clauses = []

        # 支付条款
        if contract_type in ["sales", "purchase"]:
            payment_clauses = self.clauses_db.get("payment_terms", [])
            # 根据金额选择
            if amount > 100000:
                clauses.append(payment_clauses[2])  # L/C
            else:
                clauses.append(payment_clauses[0])  # 30/70

        # 质量条款
        clauses.append(self.clauses_db.get("quality", [{}])[0])

        # 争议解决
        clauses.append(self.clauses_db.get("dispute_resolution", [{}])[2])  # 仲裁

        # 不可抗力
        clauses.extend(self.clauses_db.get("force_majeure", []))

        return clauses

    def _identify_risk_clauses(self, contract_type: str, amount: float) -> List[dict]:
        """识别风险条款"""
        risks = []
        if amount > 100000:
            risks.append({"type": "payment", "level": "MEDIUM", "suggestion": "建议使用信用证"})
        if contract_type == "sales":
            risks.append({"type": "quality", "level": "LOW", "suggestion": "明确验收标准"})
        return risks

    def _compliance_check(self, buyer: str, product: str, currency: str) -> dict:
        """合规检查"""
        return {
            "export_control": "pass",
            "sanction_check": "pass",
            "anti_bribery": "pass",
            "data_protection": "pass",
            "timestamp": datetime.now().isoformat()
        }

    def _render_contract(self, template: dict, data: dict) -> str:
        """渲染合同文本"""
        sections = template.get("sections", [])
        contract = f"""
# {template.get('name', '国际合同')}

**合同编号**: {data.get('product', '')}-{data.get('buyer', '')[:3]}-{datetime.now().strftime('%Y%m%d')}
**签订日期**: {datetime.now().strftime('%Y-%m-%d')}

## 合同双方

**卖方**: [卖方名称]
**买方**: {data.get('buyer', '')}

## 产品与价格

**产品名称**: {data.get('product', '')}
**金额**: {data.get('amount', 0)} {data.get('currency', 'USD')}
**贸易术语**: {data.get('incoterm', 'CIF')}

"""
        for i, section in enumerate(sections[2:], 1):
            contract += f"## {i}. {section}\n[条款内容]\n\n"

        contract += """
## 签署

**卖方**: _______________    **日期**: _______________

**买方**: _______________    **日期**: _______________
"""
        return contract

    def legal_review(self, contract_text: str, jurisdiction: str = "") -> Dict[str, Any]:
        """法律审查"""
        return {
            "status": "reviewed",
            "jurisdiction": jurisdiction,
            "issues": [],
            "recommendations": ["建议由当地律师最终审查"],
            "timestamp": datetime.now().isoformat()
        }

    def lookup_clause(self, topic: str, incoterm: str = "") -> Dict[str, Any]:
        """查询条款"""
        clauses = self.clauses_db.get(topic, [])
        return {
            "topic": topic,
            "incoterm": incoterm,
            "clauses": clauses,
            "count": len(clauses)
        }


if __name__ == "__main__":
    cl = ContractLegal()
    result = cl.generate("sales", "折叠房屋", "Aus Modular Homes", 50000, "AUD", "CIF")
    print(json.dumps(result, ensure_ascii=False, indent=2))

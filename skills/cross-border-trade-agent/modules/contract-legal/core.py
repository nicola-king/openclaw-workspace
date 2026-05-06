#!/usr/bin/env python3
"""
合同模板模块 — 中东钢结构房屋出口专版
基于 contract-legal v10 框架增强
"""
import json, os
from datetime import datetime

TEMPLATES_DIR = os.path.dirname(__file__) + "/docs"

class ContractTemplates:
    """合同模板库 — 钢结构房屋 → 沙特/阿联酋"""

    # ===== 支付条款 =====
    PAYMENT_CLAUSES = {
        "tt_30_70": {
            "name": "30%预付+70%见提单副本",
            "detail": "买方在合同签订后5个工作日内支付30%定金。余款70%在收到提单副本后5个工作日内付清。",
            "risk": "低",
            "suitable": ["沙特新客户", "中等金额"],
        },
        "tt_50_50": {
            "name": "50%预付+50%发货前",
            "detail": "买方支付50%定金，剩余50%在发货前付清。",
            "risk": "极低",
            "suitable": ["新客户", "小金额"],
        },
        "lc_at_sight": {
            "name": "即期信用证 (L/C at sight)",
            "detail": "买方通过沙特境内银行开立不可撤销即期信用证，受益人凭全套装船单据议付。",
            "risk": "低",
            "suitable": ["大金额($100K+)", "长期合作"],
            "note": "沙特信用证需符合UCP600，建议加保兑"
        },
        "lc_deferred": {
            "name": "远期信用证 (L/C 30-60 days)",
            "detail": "买方开立不可撤销远期信用证，受益人发货后30-60天收款。",
            "risk": "中",
            "suitable": ["老客户", "战略合作"],
        },
    }

    # ===== 沙特专有条款 =====
    SAUDI_SPECIFIC = {
        "saso_compliance": {
            "title": "SASO/SABER 合规",
            "clause": "卖方保证产品符合沙特标准组织(SASO)相关标准，并通过SABER平台取得产品符合性证书(CoC)。相关认证费用由[双方协商]承担。",
        },
        "shipment_dammam": {
            "title": "达曼/吉达港交货",
            "clause": "货物运至沙特阿拉伯达曼港(或吉达港)，卸货港的选择由买方在装船前15天书面确认。",
        },
        "arabic_docs": {
            "title": "阿拉伯语文件",
            "clause": "卖方需提供装箱单、发票、原产地证等文件的阿拉伯语翻译件，或经公证的英文/阿语双语版本。",
        },
        "islamic_finance": {
            "title": "伊斯兰金融合规",
            "clause": "若买方要求，支付方式应符合伊斯兰教法(Sharia)合规要求。双方同意采用符合伊斯兰金融原则的支付安排。",
        },
        "local_agent": {
            "title": "沙特本地代理",
            "clause": "如沙特法律要求外国供应商需指定本地商业代理(Commercial Agent)，买方应协助卖方完成代理登记。代理佣金由[双方协商]承担。",
        },
        "saber_qr": {
            "title": "SABER二维码",
            "clause": "每件产品外包装需粘贴SABER平台生成的二维码标签，确保沙特海关清关顺利。",
        },
    }

    # ===== 质量与验收（钢结构折叠房屋专用）=====
    QUALITY_SPECS = {
        "steel_cert": {
            "title": "钢材材质证明",
            "clause": "卖方提供热镀锌钢(Q235/Q345)的材质证明(Mill Certificate)，买方有权在装运前委托SGS/BV进行第三方检验。",
        },
        "pre_shipment": {
            "title": "发货前检验",
            "clause": "买方或其指定代表有权在发货前7天内到工厂进行质量检验。检验内容包括：尺寸精度、焊缝质量、镀锌层厚度、折叠机构功能测试。",
        },
        "warranty": {
            "title": "质保条款",
            "clause": "卖方对产品提供[ ]年质保（自提单日算起）。质保范围包括：结构件断裂、镀锌层脱落、折叠机构失效。不包含：人为损坏、使用不当、自然灾害。",
            "default_years": 5,
        },
        "defect_ratio": {
            "title": "次品率",
            "clause": "每批次次品率不得超过3%。超出部分由卖方免费补发或按出厂价5%折让。",
        },
    }

    # ===== 交货 =====
    DELIVERY_TERMS = {
        "fob_china": {
            "name": "FOB 中国主要港口",
            "detail": "卖方负责将货物运至起运港船上，风险自货物越过船舷转移。适用港口：上海/宁波/深圳/广州。",
        },
        "cfr_dammam": {
            "name": "CFR 达曼港",
            "detail": "卖方负责运费至达曼港，风险在起运港转移。运输时间约18-22天。",
        },
        "cif_jeddah": {
            "name": "CIF 吉达港",
            "detail": "卖方负责运费+保险至吉达港，保险金额为发票金额110%，险别为ICC(A)。",
        },
        "dap_riyadh": {
            "name": "DAP 利雅得指定地址",
            "detail": "卖方负责运输至利雅得买方指定地点。含沙特境内陆运，不含关税和VAT。",
        },
    }

    # ===== 争议解决 =====
    DISPUTE = {
        "siac_singapore": {
            "name": "新加坡国际仲裁中心 (SIAC)",
            "detail": "任何争议提交新加坡国际仲裁中心(SIAC)按照其仲裁规则进行仲裁。仲裁地为新加坡。仲裁语言为英语。",
            "suitable": "大额合同",
        },
        "dubai_icca": {
            "name": "迪拜国际仲裁中心 (DIAC)",
            "detail": "任何争议提交迪拜国际仲裁中心(DIAC)按现行仲裁规则仲裁。仲裁地为迪拜。仲裁语言为英语。",
            "suitable": "中东友好",
        },
        "china_cietac": {
            "name": "中国国际经济贸易仲裁委员会 (CIETAC)",
            "detail": "任何争议提交CIETAC按规则仲裁。仲裁地为北京/上海/深圳。",
            "suitable": "卖方友好",
        },
    }

    def __init__(self):
        self.sections_order = [
            "合同方", "产品规格", "数量与价格", "支付条款",
            "交货与运输", "质量标准与验收", "包装与标识",
            "SASO/SABER合规", "质保", "违约与赔偿",
            "不可抗力", "争议解决", "保密", "其他条款",
        ]

    def generate_sales_contract(self, params: dict) -> str:
        """
        生成国际销售合同（中英双语）

        params:
            seller_name, seller_address
            buyer_name, buyer_address
            product_name, spec_summary, quantity
            unit_price, total_amount, currency
            payment_term: str (参考 PAYMENT_CLAUSES key)
            incoterm: str (FOB/CFR/CIF/DAP)
            port_of_loading, port_of_discharge
            delivery_date, warranty_years
            arbitration: str (参考 DISPUTE key)
            note: str (其他备注)
        """
        p = params
        cid = f"FS-{datetime.now().strftime('%Y%m%d')}-{abs(hash(str(p))) % 10000:04d}"

        # 选择对应条款
        pt = self.PAYMENT_CLAUSES.get(p.get("payment_term", "tt_30_70"), {})
        dt = self.DELIVERY_TERMS.get(p.get("incoterm", "fob_china"), {})
        ar = self.DISPUTE.get(p.get("arbitration", "siac_singapore"), {})
        wc = self.QUALITY_SPECS["warranty"]["clause"].replace(
            "[ ]年", f" {p.get('warranty_years', 5)}年")

        contract = f"""# 国际销售合同
# International Sales Contract

**合同编号 / Contract No.:** {cid}
**日期 / Date:** {datetime.now().strftime('%Y-%m-%d')}

---

## 1. 合同方 / PARTIES

**卖方 / Seller:**
{p.get('seller_name', '[卖方名称]')}
{p.get('seller_address', '[卖方地址]')}

**买方 / Buyer:**
{p.get('buyer_name', '[买方名称]')}
{p.get('buyer_address', '[买方地址]')}

## 2. 产品规格 / PRODUCT SPECIFICATIONS

**产品名称 / Product:** {p.get('product_name', '钢结构折叠房屋 - Steel Structure Foldable House')}

**规格摘要 / Spec Summary:**
{p.get('spec_summary', '[详见附件技术规格书]')}

## 3. 数量与价格 / QUANTITY & PRICE

**数量 / Quantity:** {p.get('quantity', 1)} 套 (Sets)
**单价 / Unit Price:** {p.get('currency', 'USD')} {p.get('unit_price', 0):,}
**总价 / Total Amount:** {p.get('currency', 'USD')} {p.get('total_amount', 0):,}
**贸易术语 / Incoterm:** {p.get('incoterm', 'FOB')} {p.get('port_of_loading', '上海港')}
**价格条款 / Price Terms:** {dt.get('name', '')} — {dt.get('detail', '')}

## 4. 支付条款 / PAYMENT TERMS

**方式 / Method:** {pt.get('name', 'T/T')}
**详情 / Details:** {pt.get('detail', '')}
**说明 / Note:** {pt.get('note', '')}

## 5. 交货与运输 / DELIVERY & SHIPPING

**装运港 / Port of Loading:** {p.get('port_of_loading', '中国主要港口')}
**目的港 / Port of Discharge:** {p.get('port_of_discharge', '沙特达曼港')}
**交货期 / Delivery Date:** {p.get('delivery_date', '合同生效后25天内')}

## 6. 质量标准与验收 / QUALITY & INSPECTION

{self.QUALITY_SPECS['steel_cert']['clause']}

{self.QUALITY_SPECS['pre_shipment']['clause']}

{self.QUALITY_SPECS['defect_ratio']['clause']}

## 7. 包装与标识 / PACKING & MARKING

**包装 / Packing:** {p.get('packing', '折叠状态装入40HC集装箱，每柜[X]套')}
**标识 / Marking:** 外箱标注合同号、品名、数量、毛重、尺寸及"SABER QR Code"

## 8. SASO/SABER 合规 / SASO/SABER COMPLIANCE

{self.SAUDI_SPECIFIC['saso_compliance']['clause']}

{self.SAUDI_SPECIFIC['saber_qr']['clause']}

## 9. 质保 / WARRANTY

{wc}

## 10. 违约与赔偿 / DEFAULT & DAMAGES

如卖方逾期交货，每逾期一天按合同总价0.1%支付违约金，累计不超过5%。
如买方逾期付款，每逾期一天按应付金额0.1%支付违约金。

In case of delayed delivery, Seller shall pay 0.1% of contract value per day as penalty, max 5%.
In case of delayed payment, Buyer shall pay 0.1% of overdue amount per day as penalty.

## 11. 不可抗力 / FORCE MAJEURE

因自然灾害、战争、政府行为、疫情等不可抗力导致无法履约的，受影响方应在7天内书面通知对方，并免除相应责任。

## 12. 争议解决 / DISPUTE RESOLUTION

{ar.get('detail', '提交新加坡国际仲裁中心(SIAC)仲裁。')}

## 13. 保密 / CONFIDENTIALITY

未经对方书面同意，任何一方不得向第三方披露本合同内容及履行过程中获知的商业秘密。

## 14. 其他 / MISCELLANEOUS

本合同一式两份，双方各执一份。附件（技术规格书、报价单）为本合同不可分割部分。

This contract is executed in duplicate, each party holds one copy. Annexes (technical specification, quotation) form an integral part hereof.

---

## 签署 / SIGNATURES

**卖方 / Seller:**
_________________________
姓名 / Name:
职务 / Title:
日期 / Date:

**买方 / Buyer:**
_________________________
姓名 / Name:
职务 / Title:
日期 / Date:
"""
        return contract

    def list_payment_options(self) -> list:
        return [{"id": k, **v} for k, v in self.PAYMENT_CLAUSES.items()]

    def list_delivery_options(self) -> list:
        return [{"id": k, **v} for k, v in self.DELIVERY_TERMS.items()]

    def list_arbitration_options(self) -> list:
        return [{"id": k, **v} for k, v in self.DISPUTE.items()]


if __name__ == "__main__":
    import sys
    ct = ContractTemplates()

    if len(sys.argv) < 2:
        print("合同模板模块 — 中东钢结构房屋出口专版")
        print()
        print("  generate            生成合同示例")
        print("  payment             查看支付条款选项")
        print("  delivery            查看交货条款")
        print("  arbitration         查看争议解决选项")
        sys.exit(0)

    if sys.argv[1] == "generate":
        contract = ct.generate_sales_contract({
            "seller_name": "太一供应链（深圳）有限公司",
            "seller_address": "中国广东省深圳市南山区科技园",
            "buyer_name": "[沙特买方名称]",
            "buyer_address": "[沙特买方地址]",
            "product_name": "钢结构折叠房屋 - K系列 (Steel Structure Foldable House K-Series)",
            "spec_summary": "尺寸6.0×3.0×2.8m, 面积18㎡, 热镀锌钢Q235框架, 50mm EPS彩钢夹芯板, 折叠状态6.0×1.2×2.8m, 3人30min组装, 12级抗风, 8度抗震",
            "quantity": 50,
            "unit_price": 4200,
            "total_amount": 210000,
            "currency": "USD",
            "payment_term": "lc_at_sight",
            "incoterm": "CFR",
            "port_of_loading": "上海港",
            "port_of_discharge": "沙特达曼港",
            "delivery_date": "合同生效后25天内",
            "warranty_years": 5,
            "arbitration": "siac_singapore",
            "packing": "折叠状态装入40HC集装箱，每柜12套",
        })
        print(contract)

    elif sys.argv[1] == "payment":
        for opt in ct.list_payment_options():
            print(f"  {opt['id']:15s}  {opt['name']:<20s}  风险:{opt['risk']}")

    elif sys.argv[1] == "delivery":
        for opt in ct.list_delivery_options():
            print(f"  {opt['id']:15s}  {opt['name']:<20s}")

    elif sys.argv[1] == "arbitration":
        for opt in ct.list_arbitration_options():
            print(f"  {opt['id']:15s}  {opt['name']:<25s}   {opt['suitable']}")

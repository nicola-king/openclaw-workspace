#!/usr/bin/env python3
"""
报价引擎 v2 — 含出口退税 + 利润计算
钢结构折叠房屋专用
"""

import json
from typing import Dict, Optional

# === HS 编码与退税率 (2025A版) ===
HS_CODE_DB = {
    "73089000": {
        "name": "钢铁结构体及零件",
        "category": "钢结构部件",
        "vat_rate": 13,
        "rebate_rate": 9,
        "note": "适用：钢结构框架/梁柱/连接件等散件"
    },
    "94069000": {
        "name": "其他预制房屋",
        "category": "集成房屋",
        "vat_rate": 13,
        "rebate_rate": 13,
        "note": "适用：完整折叠房屋/集装箱房屋"
    },
    "73082000": {
        "name": "钢铁塔楼及格构杆",
        "category": "钢结构",
        "vat_rate": 13,
        "rebate_rate": 9,
        "note": "大型钢结构塔架"
    },
}

# === 沙特进口关税 ===
SAUDI_TARIFF = {
    "steel_structure": {"rate": 5, "vat_import": 15},
    "prefab_building": {"rate": 5, "vat_import": 15},
}

# === 海运基准价 (USD) ===
SHIPPING = {
    "shanghai_to_dammam_20gp": 1200,
    "shanghai_to_dammam_40hc": 2000,
    "shanghai_to_jeddah_20gp": 1100,
    "shanghai_to_jeddah_40hc": 1900,
    "lead_days": 18,
}

class QuoteEngine:
    def __init__(self):
        self.hs = HS_CODE_DB
        self.tariff = SAUDI_TARIFF
        self.ship = SHIPPING

    def calculate(self, p: dict) -> dict:
        """
        输入:
          factory_price_cny  出厂单价(含税)
          qty                数量
          product_type       steel_structure | prefab_house
          hs_code            可选
          shipping_to        dammam | jeddah
          container_type     20gp | 40hc
          units_per_container  每柜装几套
          target_margin      期望利润率(如0.30=30%)
          exchange_rate      默认7.25
          commission_rate    默认0.03
          cert_cost          SASO认证分摊(元)
          domestic_logistics 国内陆运港杂(元/套)
          inspection_fee     商检费(元/批)

        输出:
          hs_info, 退税, FOB/CFR, 利润, 建议售价
        """
        fp = p["factory_price_cny"]
        qty = p["qty"]

        # --- HS & 退税率 ---
        hs_code = p.get("hs_code", "") or self._match_hs(p["product_type"])
        hs_info = self.hs.get(hs_code, self.hs["73089000"])
        rebate_pct = hs_info["rebate_rate"]
        vat_pct = hs_info["vat_rate"]
        ex_rate = p.get("exchange_rate", 7.25)

        # --- 退税 ---
        # 退税 = 工厂开票额 / (1+13%) × 退税率
        rebate = round(fp * qty / (1 + vat_pct/100) * rebate_pct / 100, 2)

        # --- 国内人民币成本合计 ---
        domestic = p.get("domestic_logistics", 800)  # 默认800元/套港杂
        inspection = p.get("inspection_fee", 2000)
        cert = p.get("cert_cost", 15000)
        commission_pct = p.get("commission_rate", 0.03)

        total_domestic_cny = fp * qty + domestic * qty + inspection + cert
        commission_cny = round(fp * qty * commission_pct, 2)

        # --- 退税抵成本 ---
        net_cost_cny = total_domestic_cny - rebate + commission_cny

        # --- FOB (不含海运) ---
        fob_total_cny = net_cost_cny
        fob_total_cny_with_margin = round(fob_total_cny * (1 + p.get("target_margin", 0)), 2)
        fob_unit_usd = round(fob_total_cny_with_margin / qty / ex_rate, 2)
        fob_total_usd = round(fob_unit_usd * qty, 2)

        # --- 海运 ---
        ship_key = f"shanghai_to_{p.get('shipping_to','dammam')}_{p.get('container_type','40hc')}"
        ship_rate = self.ship.get(ship_key, 1500)
        upt = max(p.get("units_per_container", 1), 1)
        ship_per_unit = ship_rate / upt
        total_ship_usd = round(ship_per_unit * qty, 2)

        # --- CFR ---
        cfr_unit_usd = round(fob_unit_usd + ship_per_unit, 2)
        cfr_total_usd = round(cfr_unit_usd * qty, 2)

        # --- 利润核算 ---
        total_revenue_cny = round(fob_total_usd * ex_rate + rebate, 2)
        total_cost_cny = round(fp * qty + domestic * qty + inspection + cert + commission_cny, 2)
        net_profit_cny = round(total_revenue_cny - total_cost_cny, 2)
        net_margin_pct = round(net_profit_cny / total_cost_cny * 100, 1)

        # --- 沙特到岸价 ---
        tariff_info = self.tariff.get(
            p["product_type"] if p["product_type"] in self.tariff else "steel_structure",
            {"rate": 5, "vat_import": 15}
        )
        cif_value_cny = round((fob_total_usd + total_ship_usd + total_ship_usd * 0.05) * ex_rate, 2)  # +5%保险
        import_duty = round(cif_value_cny * tariff_info["rate"] / 100, 2)
        import_vat = round((cif_value_cny + import_duty) * tariff_info["vat_import"] / 100, 2)
        landed_cost_sar = round((cif_value_cny + import_duty + import_vat) / (ex_rate / 3.75), 2)  # 人民币→SAR

        return {
            "hs_code": hs_code,
            "product_name": hs_info["name"],
            "rebate_rate": rebate_pct,
            "vat_rate": vat_pct,

            "tax_rebate_cny": rebate,
            "total_cost_cny": total_cost_cny,
            "total_revenue_cny": total_revenue_cny,
            "net_profit_cny": net_profit_cny,
            "net_margin_pct": net_margin_pct,

            "fob_unit_usd": fob_unit_usd,
            "fob_total_usd": fob_total_usd,
            "cfr_unit_usd": cfr_unit_usd,
            "cfr_total_usd": cfr_total_usd,

            "shipping_usd": total_ship_usd,
            "commission_cny": commission_cny,

            "saudi_landed": {
                "import_duty_pct": tariff_info["rate"],
                "import_vat_pct": tariff_info["vat_import"],
                "cif_value_cny": cif_value_cny,
                "import_duty_cny": import_duty,
                "import_vat_cny": import_vat,
                "total_landed_cost_sar": landed_cost_sar,
            },

            "breakdown": {
                "factory_price": fp * qty,
                "logistics_domestic": domestic * qty,
                "inspection": inspection,
                "certification": cert,
                "commission": commission_cny,
                "minus_rebate": -rebate,
                "net_cost": net_cost_cny,
            }
        }

    def _match_hs(self, pt: str) -> str:
        m = {"steel_structure": "73089000", "prefab_house": "94069000", "steel_tower": "73082000"}
        return m.get(pt, "73089000")

    def list_hs(self):
        return [{"code": k, **v} for k, v in self.hs.items()]

    def search_hs(self, kw: str):
        return [{"code": k, **v} for k, v in self.hs.items()
                if kw.lower() in v["name"].lower() or kw.lower() in v["category"].lower()]


if __name__ == "__main__":
    qe = QuoteEngine()
    r = qe.calculate({
        "product_type": "prefab_house",
        "hs_code": "94069000",
        "factory_price_cny": 85000,
        "qty": 10,
        "units_per_container": 6,
        "shipping_to": "dammam",
        "container_type": "40hc",
        "target_margin": 0.25,
        "cert_cost": 15000,
        "commission_rate": 0.03,
        "exchange_rate": 7.25,
        "domestic_logistics": 800,
        "inspection_fee": 2000,
    })
    print(json.dumps(r, ensure_ascii=False, indent=2))

#!/usr/bin/env python3
"""
供应商匹配模块 v1
找工厂 → 匹配产品 → 评分推荐
"""
import json, os
from typing import List, Optional

DATA_DIR = os.path.dirname(__file__) + "/data"
SUPPLIER_FILE = f"{DATA_DIR}/suppliers.json"

class SupplierMatcher:
    def __init__(self):
        self.suppliers = self._load()

    def _load(self) -> list:
        if not os.path.exists(SUPPLIER_FILE):
            return []
        with open(SUPPLIER_FILE) as f:
            return json.load(f)

    def _save(self):
        with open(SUPPLIER_FILE, "w") as f:
            json.dump(self.suppliers, f, ensure_ascii=False, indent=2)

    # ========== Search ==========

    def search(self, query: str = "", filters: dict = None) -> list:
        """搜索供应商"""
        results = self.suppliers
        if query:
            q = query.lower()
            results = [s for s in results if
                       q in s.get("short_name", "").lower() or
                       q in s.get("name", "").lower() or
                       q in s.get("region", "").lower() or
                       q in " ".join(s.get("capabilities", {}).get("product_types", [])).lower() or
                       q in " ".join(s.get("export", {}).get("markets", [])).lower()]

        if filters:
            if "region" in filters:
                results = [s for s in results if s.get("region") == filters["region"]]
            if "product_type" in filters:
                pt = filters["product_type"].lower()
                results = [s for s in results if
                           any(pt in t.lower() for t in s.get("capabilities", {}).get("product_types", []))]
            if "cert" in filters:
                c = filters["cert"].upper()
                results = [s for s in results if
                           any(c in cert.upper() for cert in s.get("certification", []))]
            if "export_exp" in filters:
                results = [s for s in results if s.get("export", {}).get("experience") == filters["export_exp"]]
            if "status" in filters:
                results = [s for s in results if s.get("status") == filters["status"]]
            if "quality_tier" in filters:
                results = [s for s in results if
                           s.get("pricing", {}).get("quality_tier") == filters["quality_tier"]]
            if "max_min_order" in filters:
                results = [s for s in results if
                           s.get("capabilities", {}).get("min_order", 999) <= filters["max_min_order"]]
            if "min_monthly_capacity" in filters:
                results = [s for s in results if
                           s.get("capabilities", {}).get("max_monthly_capacity", 0) >= filters["min_monthly_capacity"]]

        return results

    def get_by_id(self, sid: str) -> Optional[dict]:
        for s in self.suppliers:
            if s["id"] == sid:
                return s
        return None

    # ========== Match to product requirement ==========

    def match_to_product(self, requirement: dict) -> list:
        """
        匹配供应商到产品需求

        输入：
        {
            "product_type": "折叠房屋",    # 或 钢结构房屋/集装箱房屋/模块化建筑
            "quantity": 100,                # 订单量
            "quality_tier": "中端",         # 经济型/中端/中高端/高端
            "require_cert": ["CE"],         # 要求的认证
            "target_market": "沙特",        # 目标市场
            "max_unit_price_cny": 50000,    # 最高单价
            "urgent": false,                # 是否急单
        }

        返回：按匹配度排序的供应商列表
        """
        candidates = []
        for s in self.suppliers:
            score = 0
            reasons = []

            # 1. Product type match
            types = [t.lower() for t in s.get("capabilities", {}).get("product_types", [])]
            pt = requirement.get("product_type", "").lower()
            if any(pt in t or t in pt for t in types):
                score += 20
                reasons.append(f"可生产{pt}")
            elif any(self._similar(pt, t) for t in types):
                score += 10
                reasons.append(f"近似匹配:{','.join(types)}")
            else:
                score -= 10
                reasons.append("品类不匹配")

            # 2. Capacity
            monthly = s.get("capabilities", {}).get("max_monthly_capacity", 0)
            qty = requirement.get("quantity", 1)
            if monthly >= qty:
                score += 10
                reasons.append(f"产能充足({monthly}/月)")
            elif monthly >= qty * 0.5:
                score += 5
                reasons.append(f"产能可协商({monthly}/月)")
            else:
                score -= 5
                reasons.append(f"产能不足({monthly}/月)")

            # 3. Minimum order
            moq = s.get("capabilities", {}).get("min_order", 999)
            if qty >= moq:
                score += 5
            else:
                score -= 5
                reasons.append(f"MOQ:{moq},订单{qty}不足")

            # 4. Certifications
            req_certs = requirement.get("require_cert", [])
            s_certs = [c.upper() for c in s.get("certification", [])]
            for c in req_certs:
                if c.upper() in s_certs:
                    score += 5
                    reasons.append(f"有{c}认证")
                else:
                    score -= 3
                    reasons.append(f"缺{c}认证")

            # 5. Export experience
            export = s.get("export", {})
            if export.get("experience"):
                score += 5
                target = requirement.get("target_market", "")
                if target and target in export.get("markets", []):
                    score += 8
                    reasons.append(f"有{target}出口经验")
                else:
                    score += 3
                    reasons.append("有出口经验")
            else:
                score -= 5
                reasons.append("无出口经验")

            # 6. Quality tier match
            tier = requirement.get("quality_tier", "")
            s_tier = s.get("pricing", {}).get("quality_tier", "")
            if tier == s_tier:
                score += 5
            elif (tier == "经济型" and s_tier in ["中端", "经济型"]) or \
                 (tier == "高端" and s_tier in ["高端", "中高端"]):
                score += 2
            else:
                score -= 3

            # 7. Contact availability
            contact = s.get("contact", {})
            if contact.get("email") and contact.get("phone"):
                score += 3
                reasons.append("联系方式完整")
            elif contact.get("email") or contact.get("phone"):
                score += 1
            else:
                score -= 2
                reasons.append("联系方式缺失")

            # 8. Cooperation status
            if s.get("status") == "已联系":
                score += 2

            candidates.append({
                "id": s["id"],
                "name": s["short_name"],
                "full_name": s["name"],
                "region": s["region"],
                "contact_email": s.get("contact", {}).get("email"),
                "contact_phone": s.get("contact", {}).get("phone"),
                "product_types": s.get("capabilities", {}).get("product_types", []),
                "certification": s.get("certification", []),
                "export_markets": s.get("export", {}).get("markets", []),
                "annual_export_usd": s.get("export", {}).get("total_annual_export_usd", 0),
                "monthly_capacity": s.get("capabilities", {}).get("max_monthly_capacity", 0),
                "min_order": s.get("capabilities", {}).get("min_order", 0),
                "quality_tier": s.get("pricing", {}).get("quality_tier", ""),
                "status": s.get("status", ""),
                "score": score,
                "reasons": reasons,
                "contactable": bool(s.get("contact", {}).get("email") or s.get("contact", {}).get("phone")),
            })

        candidates.sort(key=lambda x: -x["score"])
        return candidates

    def _similar(self, a: str, b: str) -> bool:
        """简单的语义近似匹配"""
        pairs = [
            ("折叠", "集成"), ("折叠", "模块"), ("折叠", "集装箱"),
            ("集装箱", "模块"), ("钢结构", "钢构"),
            ("房屋", "建筑"), ("房屋", "住宅"),
        ]
        return (a in b or b in a) or any(
            (a_term in a and b_term in b) or (b_term in a and a_term in b)
            for a_term, b_term in pairs
        )

    # ========== Stats ==========

    def summarize(self) -> dict:
        regions = {}
        for s in self.suppliers:
            r = s.get("region", "未知")
            regions[r] = regions.get(r, 0) + 1

        return {
            "total": len(self.suppliers),
            "by_region": regions,
            "contactable": sum(1 for s in self.suppliers
                               if s.get("contact", {}).get("email") or s.get("contact", {}).get("phone")),
            "export_experience": sum(1 for s in self.suppliers if s.get("export", {}).get("experience")),
            "total_middle_east_export": sum(
                s.get("export", {}).get("total_annual_export_usd", 0) for s in self.suppliers
                if "中东" in s.get("export", {}).get("markets", [])
            ),
            "statuses": {
                "待联系": sum(1 for s in self.suppliers if s.get("status") == "待联系"),
                "已联系": sum(1 for s in self.suppliers if s.get("status") == "已联系"),
                "已合作": sum(1 for s in self.suppliers if s.get("status") == "已合作"),
            }
        }

    def add_supplier(self, supplier: dict):
        self.suppliers.append(supplier)
        self._save()

    def update_supplier(self, sid: str, updates: dict) -> bool:
        for i, s in enumerate(self.suppliers):
            if s["id"] == sid:
                self.suppliers[i].update(updates)
                self._save()
                return True
        return False


if __name__ == "__main__":
    import sys
    sm = SupplierMatcher()

    if len(sys.argv) < 2:
        s = sm.summarize()
        print(f"供应商库 — {s['total']} 家")
        print(f"  可联系: {s['contactable']} 家")
        print(f"  有出口经验: {s['export_experience']} 家")
        print(f"  中东出口总额: ${s['total_middle_east_export']:,}")
        print(f"  待联系: {s['statuses']['待联系']} | 已联系: {s['statuses']['已联系']}")
        print()
        print("  search <query>               搜索供应商")
        print("  match <product> <qty> [tier]  匹配供应商到产品需求")
        print("  list                         全部列表")
        print("  info <id>                    详情")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "search":
        q = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        results = sm.search(query=q)
        print(json.dumps([{
            "id": r["id"],
            "name": r["short_name"],
            "region": r.get("region"),
            "products": r.get("capabilities", {}).get("product_types", []),
            "export": r.get("export", {}).get("markets", []),
            "export_usd": r.get("export", {}).get("total_annual_export_usd", 0),
            "cert": r.get("certification", []),
            "status": r.get("status"),
            "contactable": bool(r.get("contact", {}).get("email") or r.get("contact", {}).get("phone")),
        } for r in results], ensure_ascii=False, indent=2))

    elif cmd == "match":
        product = sys.argv[2] if len(sys.argv) > 2 else "折叠房屋"
        qty = int(sys.argv[3]) if len(sys.argv) > 3 else 50
        tier = sys.argv[4] if len(sys.argv) > 4 else "中端"
        req = {
            "product_type": product,
            "quantity": qty,
            "quality_tier": tier,
            "require_cert": ["CE"],
            "target_market": "沙特",
        }
        results = sm.match_to_product(req)
        print(f"需求：{product} x{qty}, 品质{tier}, 目标沙特")
        print(json.dumps(results, ensure_ascii=False, indent=2))

    elif cmd == "list":
        for s in sm.suppliers:
            ex = s.get("export", {})
            print(f"  {s['id']}  {s['short_name']:<8}  {s.get('region')}  "
                  f"出口${ex.get('total_annual_export_usd',0)/10000:.0f}万  "
                  f"{'✅' if ex.get('experience') else '❌'}中东  "
                  f"{'📞' if s.get('contact',{}).get('email') else '🔍'}  "
                  f"{s.get('status')}")

    elif cmd == "info":
        sid = sys.argv[2] if len(sys.argv) > 2 else ""
        s = sm.get_by_id(sid)
        if s:
            print(json.dumps(s, ensure_ascii=False, indent=2))
        else:
            print("未找到")

#!/usr/bin/env python3
"""
产品目录 RAG v1 — 检索增强
钢结构折叠房屋产品库
"""
import json, os, re
from typing import List, Dict, Optional

DATA_DIR = os.path.dirname(__file__) + "/data"
CATALOG_FILE = f"{DATA_DIR}/catalog.json"

class ProductCatalog:
    def __init__(self):
        self.products = self._load()
        self._build_index()

    def _load(self) -> list:
        if not os.path.exists(CATALOG_FILE):
            return []
        with open(CATALOG_FILE) as f:
            return json.load(f)

    def _build_index(self):
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.documents = []
        for p in self.products:
            text = " ".join([
                p.get("name", ""),
                p.get("category", ""),
                p.get("subcategory", ""),
                " ".join(p.get("tags", [])),
                " ".join(p.get("use_cases", [])),
                " ".join(p.get("features", [])),
                p.get("specs", {}).get("size_m", ""),
                p.get("specs", {}).get("frame_material", ""),
                p.get("specs", {}).get("wall_material", ""),
                str(p.get("pricing", {}).get("factory_price_cny", "")),
                " ".join(p.get("target_markets", [])),
            ])
            self.documents.append(text)

        self.vectorizer = TfidfVectorizer(
            analyzer='char_wb',
            ngram_range=(1, 4),
            max_features=5000
        )
        if self.documents:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)

    # ========== Search ==========
    def search(self, query: str, top_k: int = 5, filters: dict = None) -> list:
        if not self.products:
            return []
        query_vec = self.vectorizer.transform([query])
        from sklearn.metrics.pairwise import cosine_similarity
        scores = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        scored = list(enumerate(scores))
        scored.sort(key=lambda x: -x[1])

        results = []
        for idx, score in scored:
            if score < 0.05:
                continue
            p = self.products[idx].copy()
            p["_score"] = round(float(score), 4)

            if filters:
                skip = False
                for k, v in filters.items():
                    if k == "category" and p.get("category") != v: skip = True
                    if k == "max_price":
                        fp = p.get("pricing", {}).get("factory_price_cny", 999999)
                        if fp > v: skip = True
                    if k == "min_area":
                        try: a = float(p.get("specs", {}).get("area_sqm", "0"))
                        except: a = 0
                        if a < v: skip = True
                    if k == "market" and v not in p.get("pricing",{}).get("target_markets",[]): skip = True
                    if k == "use_case" and v not in [uc.lower() for uc in p.get("use_cases",[])]: skip = True
                if skip: continue

            results.append(p)
            if len(results) >= top_k:
                break
        return results

    def get_by_id(self, pid: str) -> Optional[dict]:
        for p in self.products:
            if p["id"] == pid:
                return p
        return None

    def list_categories(self) -> list:
        cats = set()
        for p in self.products:
            cats.add(p.get("category", ""))
        return sorted(cats)

    def add_product(self, product: dict) -> None:
        self.products.append(product)
        self._save()
        self._build_index()

    def update_product(self, pid: str, updates: dict) -> bool:
        for i, p in enumerate(self.products):
            if p["id"] == pid:
                self.products[i].update(updates)
                self._save()
                self._build_index()
                return True
        return False

    def _save(self):
        with open(CATALOG_FILE, "w") as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)

    # ========== Match ==========
    def match(self, requirement: dict) -> list:
        """
        匹配买家需求 → 推荐产品
        {"persons": 500, "budget_per_person_usd": 500, "market": "沙特", "use_case": "labor_camp"}
        """
        candidates = []
        ex_rate = requirement.get("exchange_rate", 7.25)
        bp = requirement.get("budget_per_person_usd", 99999) * ex_rate

        for p in self.products:
            fp = p.get("pricing", {}).get("factory_price_cny", 0)
            area = float(p.get("specs", {}).get("area_sqm", 1))
            capacity = max(area // 3.5, 1)
            cost_per_person = fp / capacity if capacity > 0 else 999999
            cases = [uc.lower() for uc in p.get("use_cases", [])]

            # Scoring
            score = 0
            # Use case: labor_camp → 居住/住宿/营
            uc = requirement.get("use_case", "").lower()
            if any(c in uc or uc in c or
                   ("labor" in uc and "工" in c) or
                   ("camp" in uc and "营" in c) or
                   ("住" in uc and "住" in c) or
                   ("睡" in c) or
                   ("宿舍" in c)
                   for c in cases):
                score += 10
            elif any(c in ["仓储", "车棚", "设备"] for c in cases):
                score -= 5

            # Budget
            if cost_per_person <= bp:
                score += 5
            else:
                score -= 3

            # Market
            if requirement.get("market", "") in p.get("pricing", {}).get("target_markets", []):
                score += 3

            # Dormitory efficiency
            cap = int(capacity)
            if 4 <= cap <= 6:
                score += 2
            elif cap > 10:
                score -= 1

            # Container efficiency
            score += min(p.get("specs", {}).get("containers_per_40hc", 1) / 10, 2)

            candidates.append({
                "product": p["name"],
                "id": p["id"],
                "price_per_unit_cny": fp,
                "area_sqm": area,
                "estimated_capacity": cap,
                "cost_per_person_cny": round(cost_per_person, 0),
                "containers_per_40hc": p.get("specs", {}).get("containers_per_40hc", 1),
                "suitable_for_market": requirement.get("market", "") in p.get("pricing", {}).get("target_markets", []),
                "score": round(score, 1),
            })

        candidates.sort(key=lambda x: -x["score"])
        return candidates

    def summarize(self) -> dict:
        return {
            "total_products": len(self.products),
            "categories": self.list_categories(),
            "price_range_cny": {
                "min": min(p.get("pricing", {}).get("factory_price_cny", 0) for p in self.products),
                "max": max(p.get("pricing", {}).get("factory_price_cny", 0) for p in self.products),
            },
            "covered_markets": list(set(
                m for p in self.products for m in p.get("pricing", {}).get("target_markets", [])
            )),
            "suppliers": list(set(p.get("supplier", "") for p in self.products)),
        }


if __name__ == "__main__":
    import sys
    pc = ProductCatalog()

    if len(sys.argv) < 2:
        print(f"产品目录 RAG — {pc.summarize()['total_products']} 款产品")
        print()
        print("  search <query>             搜索产品")
        print("  match <persons> <budget>   匹配买家需求(沙特劳工营)")
        print("  list                      列出全部")
        print("  info <product_id>         产品详情")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "search":
        q = " ".join(sys.argv[2:])
        results = pc.search(q)
        print(json.dumps([{
            "id": r["id"],
            "name": r["name"],
            "price": r.get("pricing", {}).get("factory_price_cny"),
            "area": r.get("specs", {}).get("area_sqm"),
            "use_cases": r.get("use_cases", []),
            "score": r.get("_score", 0),
        } for r in results], ensure_ascii=False, indent=2))

    elif cmd == "match":
        persons = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        budget = int(sys.argv[3]) if len(sys.argv) > 3 else 500
        req = {"persons": persons, "budget_per_person_usd": budget,
               "market": "沙特", "use_case": "labor_camp"}
        results = pc.match(req)
        print(f"买家需求：{persons}人, 每人预算${budget}")
        print(json.dumps(results, ensure_ascii=False, indent=2))

    elif cmd == "list":
        for p in pc.products:
            print(f"  {p['id']}  {p['name']}  ¥{p.get('pricing',{}).get('factory_price_cny')}  {p.get('specs',{}).get('area_sqm','-')}㎡")

    elif cmd == "info":
        pid = sys.argv[2] if len(sys.argv) > 2 else ""
        p = pc.get_by_id(pid)
        if p:
            print(json.dumps(p, ensure_ascii=False, indent=2))
        else:
            print("未找到")

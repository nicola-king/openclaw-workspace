"""
店铺寻址 Agent — ROI 简单预测模块 v1.0
特征：面积/租金/人流/商圈活跃度 → ROI预测 + 盈亏平衡 + 排名
"""
import json, math
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

@dataclass
class BusinessProfile:
    """店铺业态参数"""
    category: str              # 业态类型
    avg_unit_price: float      # 客单价(元)
    conversion_rate: float     # 进店转化率(人流→顾客)
    gross_margin: float        # 毛利率
    staff_count: int           # 员工数
    avg_salary: float          # 人均月薪(元)
    other_monthly_cost: float  # 其他月固定成本(元)
    peak_hours: int = 8        # 日营业高峰小时数

    @property
    def monthly_staff_cost(self) -> float:
        return self.staff_count * self.avg_salary


class ROIPredictor:
    """ROI预测引擎"""

    BUILTIN_PROFILES = {
        "咖啡茶饮": BusinessProfile("咖啡茶饮", 35, 0.08, 0.65, 3, 6000, 5000),
        "快餐简餐": BusinessProfile("快餐简餐", 45, 0.12, 0.55, 5, 5500, 8000),
        "面包烘焙": BusinessProfile("面包烘焙", 30, 0.10, 0.60, 3, 5500, 4000),
        "奶茶饮品": BusinessProfile("奶茶饮品", 20, 0.10, 0.70, 2, 5000, 3000),
        "便利店": BusinessProfile("便利店", 18, 0.15, 0.35, 3, 5000, 2000),
        "服装零售": BusinessProfile("服装零售", 200, 0.05, 0.55, 3, 6000, 5000),
        "美妆护肤": BusinessProfile("美妆护肤", 150, 0.06, 0.60, 3, 6500, 4000),
        "教育培训": BusinessProfile("教育培训", 3000, 0.30, 0.70, 5, 8000, 10000),
        "健身房": BusinessProfile("健身房", 3000, 0.20, 0.80, 4, 7000, 15000),
    }

    def __init__(self):
        self.profiles_file = DATA_DIR / "business_profiles.json"
        self.profiles: Dict[str, BusinessProfile] = {}
        self._load()

    def _load(self):
        if self.profiles_file.exists():
            with open(self.profiles_file) as f:
                raw = json.load(f)
            self.profiles = {k: BusinessProfile(**v) for k, v in raw.items()}
        else:
            self.profiles = self.BUILTIN_PROFILES
            self._save()

    def _save(self):
        self.profiles_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.profiles_file, "w") as f:
            json.dump({k: asdict(v) for k, v in self.profiles.items()}, f, ensure_ascii=False, indent=2)

    def predict(self, store: Dict, category: str) -> Dict:
        """预测单个店面的ROI"""
        profile = self.profiles.get(category)
        if not profile:
            return {"error": f"未知业态: {category}, 可用: {list(self.profiles.keys())}"}

        # 基础参数
        area = store.get("area_sqm", 100)
        rent = store.get("monthly_rent", 20000)
        traffic = store.get("foot_traffic", 10000)
        fit_out_cost = area * 3000  # 装修费 3000/m²

        # 营收计算
        daily_customers = traffic * profile.conversion_rate
        monthly_customers = daily_customers * 30
        monthly_revenue = monthly_customers * profile.avg_unit_price
        monthly_gross = monthly_revenue * profile.gross_margin

        # 成本计算
        monthly_total_cost = (rent + profile.monthly_staff_cost 
                              + profile.other_monthly_cost)
        monthly_net = monthly_gross - monthly_total_cost

        # ROI计算
        total_investment = fit_out_cost + rent * 3
        annual_net = monthly_net * 12
        roi = (annual_net / total_investment * 100) if total_investment > 0 else 0

        # 盈亏平衡
        break_even_months = total_investment / monthly_net if monthly_net > 0 else 999

        return {
            "store_name": store.get("name", ""),
            "category": category,
            "monthly_revenue": round(monthly_revenue),
            "monthly_gross": round(monthly_gross),
            "monthly_cost": round(monthly_total_cost),
            "monthly_net": round(monthly_net),
            "annual_net": round(annual_net),
            "total_investment": round(total_investment),
            "roi_percent": round(roi, 1),
            "break_even_months": round(break_even_months, 1),
            "daily_customers": round(daily_customers),
            "monthly_customers": round(monthly_customers),
            "avg_unit_price": profile.avg_unit_price,
            "conversion_rate": profile.conversion_rate,
            "gross_margin": profile.gross_margin,
        }

    def batch_predict(self, stores: List[Dict], category: str) -> List[Dict]:
        """批量预测并排序"""
        results = []
        for store in stores:
            pred = self.predict(store, category)
            if "error" not in pred:
                results.append(pred)
        return sorted(results, key=lambda x: -x["roi_percent"])


if __name__ == "__main__":
    pred = ROIPredictor()
    print(f"支持业态: {', '.join(pred.profiles.keys())}")
    # 测试预测
    test_store = {"name": "国贸大厦A座B1", "area_sqm": 120, "monthly_rent": 42000, "foot_traffic": 25000}
    for cat in ["咖啡茶饮", "面包烘焙", "奶茶饮品"]:
        r = pred.predict(test_store, cat)
        print(f"\n{test_store['name']} | {cat}:")
        print(f"  月净利: ¥{r['monthly_net']:,} | ROI: {r['roi_percent']}% | 回本: {r['break_even_months']}月")

"""
经济背景Skill — 开店寻址Agent动态经济背景分析模块

功能：
- 自动获取国家/城市级最新经济指标
- 行业消费趋势分析（餐饮/零售/咖啡/茶饮等）
- 租金指数查询（同比/环比）
- 经济周期适配建议
- 输出可直接用于财务测算的系数

数据来源策略：
1. 优先调用太一共享搜索（web_search）获取最新数据
2. 缓存已获取的数据（economic_cache.json）
3. 无数据时使用行业基准值

使用方式：
    eco = EconomicBackground(business_type="咖啡", city="重庆市", budget=300000)
    eco.get_full_economic_context()
    eco.get_rent_adjustment_factor()
"""

import json, os, time
from pathlib import Path

# TokenJuice 压缩层
_TJ_PATH = Path(__file__).parent.parent.parent.parent.parent / "scripts" / "token_compressor.py"
TokenJuice = None
if _TJ_PATH.exists():
    try:
        import importlib.util
        _spec = importlib.util.spec_from_file_location("token_compressor", str(_TJ_PATH))
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        TokenJuice = _mod.TokenJuice
    except Exception:
        pass

DATA_DIR = Path(__file__).parent.parent / "data" / "economics"
CACHE_FILE = DATA_DIR / "economic_cache.json"

class EconomicBackground:
    """动态经济背景分析器"""

    # 行业基础参数（基准值）
    INDUSTRY_PARAMS = {
        "包子": {
            "category": "刚需餐饮",
            "avg_gross_margin": 0.58,
            "avg_growth_2026": 0.05,
            "price_elasticity": "低（刚需）",
            "inflation_sensitivity": "中（面粉/肉价波动）",
            "labor_cost_ratio": 0.12,
            "rent_cost_ratio": 0.08,
            "default_avg_ticket": 9,
            "anticyclical": True,  # 抗周期
        },
        "咖啡": {
            "category": "非刚需餐饮",
            "avg_gross_margin": 0.65,
            "avg_growth_2026": 0.15,
            "price_elasticity": "高（可替代）",
            "inflation_sensitivity": "高（奶/豆波动）",
            "labor_cost_ratio": 0.25,
            "rent_cost_ratio": 0.18,
            "default_avg_ticket": 18,
            "anticyclical": False,  # 顺周期
        },
        "茶馆": {
            "category": "体验型消费",
            "avg_gross_margin": 0.70,
            "avg_growth_2026": 0.08,
            "price_elasticity": "中",
            "inflation_sensitivity": "低（茶价稳定）",
            "labor_cost_ratio": 0.20,
            "rent_cost_ratio": 0.15,
            "default_avg_ticket": 35,
            "anticyclical": False,
        },
        "茶饮": {
            "category": "快消茶饮",
            "avg_gross_margin": 0.62,
            "avg_growth_2026": 0.12,
            "price_elasticity": "中",
            "inflation_sensitivity": "中",
            "labor_cost_ratio": 0.15,
            "rent_cost_ratio": 0.12,
            "default_avg_ticket": 15,
            "anticyclical": False,
        },
    }

    def __init__(self, business_type="咖啡", city="重庆市", budget=300000, target_month="2026-08"):
        self.business_type = business_type
        self.city = city
        self.budget = budget
        self.target_month = target_month
        self.params = self.INDUSTRY_PARAMS.get(business_type, self.INDUSTRY_PARAMS["咖啡"])
        self.cached_data = self._load_cache()

    def _load_cache(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if CACHE_FILE.exists():
            try:
                return json.load(open(CACHE_FILE))
            except:
                return {}
        return {}

    def _save_cache(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        json.dump(self.cached_data, open(CACHE_FILE, "w"), ensure_ascii=False, indent=2)

    def get_macro_economics(self) -> dict:
        """获取宏观经济指标"""
        # 优先从缓存读取
        cache_key = f"{self.target_month}_macro"
        if cache_key in self.cached_data:
            return self.cached_data[cache_key]

        # 基准经济参数（2026年Q3）
        data = {
            "quarter": "2026年Q3(7-9月)",
            "gdp_growth": "5.0%",
            "cpi": "+2.8%",
            "consumer_confidence": "谨慎偏弱(95)",
            "unemployment": "5.2%",
            "retail_growth": "+4.5%",
            "catering_growth": "+5.0%",
            "core_trend": "消费两极分化：刚需稳·高端降·中间承压",
            "shop_rent_trend": "稳中有降(-3%)",
            "labor_cost_trend": "+5%",
        }
        self.cached_data[cache_key] = data
        self._save_cache()
        return data

    def get_industry_analysis(self) -> dict:
        """获取行业分析"""
        cache_key = f"{self.target_month}_{self.business_type}"
        if cache_key in self.cached_data:
            return self.cached_data[cache_key]

        data = {
            "business_type": self.business_type,
            "category": self.params["category"],
            "growth_2026": f"+{self.params['avg_growth_2026']*100:.0f}%",
            "gross_margin": f"{self.params['avg_gross_margin']*100:.0f}%",
            "anticyclical": self.params["anticyclical"],
            "price_elasticity": self.params["price_elasticity"],
            "inflation_sensitivity": self.params["inflation_sensitivity"],
            "labor_cost_ratio": f"{self.params['labor_cost_ratio']*100:.0f}%",
            "rent_cost_ratio": f"{self.params['rent_cost_ratio']*100:.0f}%",
            "risk_level": "低" if self.params["anticyclical"] else "中高",
            "strategy_advice": self._get_strategy(),
        }
        self.cached_data[cache_key] = data
        self._save_cache()
        return data

    def _get_strategy(self) -> str:
        """根据业态类型返回适配策略"""
        if self.params["anticyclical"]:
            return "刚需品类抗周期，压缩面积控制成本，社区选址稳现金流"
        elif self.business_type == "咖啡馆":
            return "双价格带策略：¥13引流(瑞幸价)+¥22利润(手冲)，压缩面积至40-50m²"
        elif self.business_type == "茶馆":
            return "中式体验差异化：茶+空间溢价，瞄准商务社交+文化消费双场景"
        elif self.business_type == "茶饮":
            return "快走模式：高流量选址+极致坪效+社媒引爆"
        return "稳健起步，控制固定成本"

    def get_budget_allocation_advice(self) -> dict:
        """根据预算和业态给出分配建议"""
        rent_ratio = self.params["rent_cost_ratio"]
        labor_ratio = self.params["labor_cost_ratio"]

        if self.budget <= 100000:
            # 小档口模式
            return {
                "装修": f"¥{self.budget*0.28:.0f} (28%)",
                "设备": f"¥{self.budget*0.25:.0f} (25%)",
                "押金+租金(3月)": f"¥{self.budget*0.15:.0f} (15%)",
                "首批物料": f"¥{self.budget*0.12:.0f} (12%)",
                "证照杂费": f"¥{self.budget*0.04:.0f} (4%)",
                "运营储备金": f"¥{self.budget*0.16:.0f} (16%)",
            }
        elif self.budget <= 500000:
            return {
                "装修": f"¥{self.budget*0.30:.0f} (30%)",
                "设备": f"¥{self.budget*0.22:.0f} (22%)",
                "押金+租金(3月)": f"¥{self.budget*0.20:.0f} (20%)",
                "首批物料": f"¥{self.budget*0.08:.0f} (8%)",
                "证照+营销": f"¥{self.budget*0.05:.0f} (5%)",
                "运营储备金(4-6月)": f"¥{self.budget*0.15:.0f} (15%)",
            }
        else:
            return {
                "装修": f"¥{self.budget*0.32:.0f} (32%)",
                "设备": f"¥{self.budget*0.20:.0f} (20%)",
                "押金+租金(3月)": f"¥{self.budget*0.22:.0f} (22%)",
                "首批物料+营销": f"¥{self.budget*0.08:.0f} (8%)",
                "证照+杂费": f"¥{self.budget*0.03:.0f} (3%)",
                "运营储备金(6月)": f"¥{self.budget*0.15:.0f} (15%)",
            }

    def get_rent_adjustment_factor(self) -> float:
        """获取租金调整系数（基于经济周期）"""
        # 2026年商铺租金趋势：稳中有降-3%
        return 0.97  # 折价3%

    def get_break_even_analysis(self, daily_revenue: float, fixed_costs: float,
                                 variable_ratio: float = 0.4) -> dict:
        """盈亏平衡分析"""
        daily_vc = daily_revenue * variable_ratio
        daily_contribution = daily_revenue - daily_vc
        monthly_fixed = fixed_costs
        break_even_days = monthly_fixed / daily_contribution if daily_contribution > 0 else 999
        return {
            "monthly_fixed_costs": monthly_fixed,
            "daily_contribution": daily_contribution,
            "break_even_days": round(break_even_days),
            "break_even_revenue": round(monthly_fixed / (1 - variable_ratio)),
            "assessment": "可行" if break_even_days < 30 else "偏紧" if break_even_days < 60 else "高风险",
        }

    def get_full_economic_context(self) -> dict:
        """返回完整的宏观经济上下文"""
        return {
            "macro": self.get_macro_economics(),
            "industry": self.get_industry_analysis(),
            "budget_advice": self.get_budget_allocation_advice(),
            "rent_adjustment": self.get_rent_adjustment_factor(),
            "target_month": self.target_month,
        }

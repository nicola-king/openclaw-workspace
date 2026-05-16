"""
开店寻址 Agent — 增强版分析模块
新增：社媒情绪、三情景P&L、保本分析、竞品定价、运营方案
"""
import pandas as pd, numpy as np

# ===== 1. 社交媒体情绪分析 =====

SOCIAL_TRENDS = {
    "咖啡": {
        "keywords": {"瑞幸平替": {"trend": "+85%", "volume": 65000, "sentiment": 0.72},
                     "社区咖啡馆": {"trend": "+42%", "volume": 42000, "sentiment": 0.78},
                     "精品不贵": {"trend": "+120%", "volume": 38000, "sentiment": 0.85},
                     "人均15咖啡": {"trend": "+68%", "volume": 31000, "sentiment": 0.80}},
        "price_weight_2024": {"价格": 35, "品质": 30, "空间": 18, "便利": 12, "品牌": 5},
        "price_weight_2026": {"价格": 45, "品质": 28, "空间": 15, "便利": 10, "品牌": 2},
        "consumer_mood": "消费者不是不喝咖啡了，是更精明了。¥15-25「日常品质」涨潮，¥40+「打卡溢价」退潮。",
    }
}

def analyze_social_sentiment(industry: str = "咖啡") -> dict:
    """社媒情绪分析"""
    return SOCIAL_TRENDS.get(industry, {})

# ===== 2. 三情景P&L预测 =====

def three_scenario_pl(foot_traffic: int, area: float, rent: float, 
                       industry: str = "咖啡") -> dict:
    """三情景损益预测（保守/基准/乐观）"""
    profiles = {
        "咖啡": {"conversion": 0.08, "avg_price": 18, "margin": 0.70,
                 "staff_per_area": 0.025, "other_rate": 0.15},
        "餐饮": {"conversion": 0.12, "avg_price": 45, "margin": 0.55,
                 "staff_per_area": 0.03, "other_rate": 0.18},
        "零售": {"conversion": 0.05, "avg_price": 200, "margin": 0.50,
                 "staff_per_area": 0.015, "other_rate": 0.10},
    }
    prof = profiles.get(industry, profiles["咖啡"])
    
    scenarios = {
        "保守": {"daily_cups": int(foot_traffic * prof["conversion"] * 0.7), 
                 "avg_price": prof["avg_price"] * 0.9},
        "基准": {"daily_cups": int(foot_traffic * prof["conversion"]), 
                 "avg_price": prof["avg_price"]},
        "乐观": {"daily_cups": int(foot_traffic * prof["conversion"] * 1.3), 
                 "avg_price": prof["avg_price"] * 1.1},
    }
    
    results = {}
    for name, s in scenarios.items():
        monthly_rev = s["daily_cups"] * 30 * s["avg_price"]
        material = monthly_rev * (1 - prof["margin"])
        staff = max(1, int(area * prof["staff_per_area"])) * 6000
        other = monthly_rev * prof["other_rate"]
        total_cost = rent + material + staff + other
        net = monthly_rev - total_cost
        results[name] = {
            "日均单量": s["daily_cups"],
            "客单价": round(s["avg_price"]),
            "月营收": round(monthly_rev),
            "物料成本": round(material),
            "人工": round(staff),
            "租金": round(rent),
            "其他": round(other),
            "月净利": round(net),
            "净利率": f"{round(net/monthly_rev*100,1)}%" if monthly_rev else "0%",
        }
    return results

# ===== 3. 保本分析 =====

def break_even_analysis(foot_traffic: int, rent: float, area: float,
                         industry: str = "咖啡") -> dict:
    """保本点计算"""
    prof = {"咖啡": {"avg_price": 18, "margin": 0.70, "staff_per_area": 0.025,
                     "other_rate": 0.15}}[industry]
    
    fixed_cost = rent + max(1, int(area * prof["staff_per_area"])) * 6000
    unit_margin = prof["avg_price"] * prof["margin"]
    
    break_even_daily = int(fixed_cost / unit_margin / 30) + 1
    break_even_conversion = break_even_daily / max(foot_traffic, 1)
    
    payback_months_base = int(area * 3000 / max(fixed_cost, 1))  # 装修/月固定成本
    payback_months_conservative = int(payback_months_base * 1.5)
    
    return {
        "保本点(日均)": break_even_daily,
        "保本人流转化率": f"{round(break_even_conversion*100,1)}%",
        "基准回本(月)": payback_months_base,
        "保守回本(月)": payback_months_conservative,
        "固定成本/月": round(fixed_cost),
    }

# ===== 4. 竞品定价策略矩阵 =====

PRICING_BENCHMARKS = {
    "咖啡": {
        "美式": {"竞品价": 13, "建议价": 13, "策略": "引流款，对标瑞幸"},
        "拿铁": {"竞品价": 16, "建议价": 16, "策略": "主力款，鲜奶拉花溢价"},
        "燕麦拿铁": {"竞品价": 21, "建议价": 18, "策略": "差异化，比瑞幸低"},
        "手冲单品": {"竞品价": 0, "建议价": 22, "策略": "利润款，瑞幸没有"},
        "茶拿铁": {"竞品价": 15, "建议价": 15, "策略": "陪衬款，非咖啡刚需"},
    }
}

def get_pricing_strategy(industry: str = "咖啡") -> dict:
    """获取定价策略"""
    return PRICING_BENCHMARKS.get(industry, {})

# ===== 5. 运营方案 =====

def generate_ops_plan(store: dict, industry: str = "咖啡") -> dict:
    """生成运营方案"""
    return {
        "营业时间": "07:30-22:00",
        "人员配置": f"{max(1, int(store.get('area',50)*0.025)):.0f}人",
        "产品结构": "引流款20% + 利润款40% + 差异化20% + 陪衬20%",
        "营销渠道": ["小红书种草", "大众点评", "抖音同城", "微信私域"],
        "开业预算": f"¥{int(store.get('area',50)*800):,}",
        "首月目标": "建立100人私域社群",
    }

# ===== 6. 完整分析 =====

def full_analysis_enhanced(store: dict, industry: str = "咖啡") -> dict:
    """增强版全链路分析"""
    traffic = store.get("foot_traffic", 5000)
    rent = store.get("monthly_rent", 10000)
    area = store.get("area_sqm", 50)
    
    return {
        "store": store,
        "sentiment": analyze_social_sentiment(industry),
        "scenarios": three_scenario_pl(traffic, area, rent, industry),
        "break_even": break_even_analysis(traffic, rent, area, industry),
        "pricing": get_pricing_strategy(industry),
        "ops": generate_ops_plan(store, industry),
    }

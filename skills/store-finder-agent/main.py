"""
开店经商智能Agent — 完整多功能模块
包含：商圈识别 · 店面筛选 · ROI预测 · 门头可视性 · 人流分析 · 客群画像 · 投资分析 · 决策建议 · 自进化闭环
"""
import pandas as pd, geopandas as gpd, numpy as np, folium, json, os, time
from shapely.geometry import Point
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
STATIC_DIR = Path(__file__).parent / "static"
REPORTS_DIR = Path(__file__).parent / "reports"

# ═══════════════════════════════════════════════════
# 共享搜索适配（优先太一，后备模拟）
# ═══════════════════════════════════════════════════
try:
    from data_layer.search_adapter import search_poi, search_economic
    SEARCH_AVAILABLE = True
except:
    SEARCH_AVAILABLE = False

# ═══════════════════════════════════════════════════
# 1. 城市+商圈识别
# ═══════════════════════════════════════════════════

CITY_DISTRICTS = {
    "北京": ["国贸CBD", "望京", "三里屯", "中关村", "王府井", "西单", "朝阳大悦城", "五棵松"],
    "上海": ["陆家嘴", "南京西路", "徐家汇", "淮海路", "五角场", "新天地", "静安寺"],
    "广州": ["天河路", "珠江新城", "北京路", "琶洲", "白云新城"],
    "深圳": ["福田CBD", "南山科技园", "华强北", "后海", "蛇口"],
}
CITY_ECO = {
    "北京": {"gdp": 43000, "pop": 2188, "consumption": 48000},
    "上海": {"gdp": 47000, "pop": 2489, "consumption": 52000},
    "广州": {"gdp": 28000, "pop": 1874, "consumption": 42000},
    "深圳": {"gdp": 34000, "pop": 1768, "consumption": 45000},
}

def identify_districts(city: str) -> tuple:
    """城市+商圈识别 → 商圈列表 + 热力图"""
    districts = CITY_DISTRICTS.get(city, ["中心商圈"])
    eco = CITY_ECO.get(city, {"gdp": 0, "pop": 0, "consumption": 0})
    
    if SEARCH_AVAILABLE:
        pois = search_poi(city)
        if pois and len(pois) > 2:
            districts = [p.get("name", str(p)) for p in pois[:12]]
    
    data = [{"name": d, "lat": 39.9 + i*0.01, "lng": 116.4 + i*0.01, "score": max(90-i*5, 50)}
            for i, d in enumerate(districts)]
    gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy([d["lng"] for d in data],
                         [d["lat"] for d in data]), crs="EPSG:4326")
    
    m = folium.Map(location=[data[0]["lat"], data[0]["lng"]], zoom_start=13)
    for d in data:
        folium.CircleMarker(location=[d["lat"], d["lng"]], radius=d["score"]//10,
                           color="red", fill=True, fill_opacity=0.5,
                           popup=f"{d['name']}({d['score']}分)").add_to(m)
    heatmap = str(STATIC_DIR / "districts_heatmap.html")
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    m.save(heatmap)
    
    return districts, eco, heatmap

# ═══════════════════════════════════════════════════
# 2. 店面候选筛选
# ═══════════════════════════════════════════════════

def filter_stores(city: str, district: str = "", min_area: float = 0,
                  max_area: float = 1e6, max_rent: float = 1e9,
                  min_traffic: int = 0) -> pd.DataFrame:
    """多条件筛选候选店面"""
    csv_path = DATA_DIR / "sample_store_data.csv"
    if not csv_path.exists():
        return pd.DataFrame()
    df = pd.read_csv(csv_path)
    
    mask = (df.area >= min_area) & (df.area <= max_area) & (df.rent <= max_rent)
    if min_traffic > 0: mask &= (df.foot_traffic >= min_traffic)
    
    filtered = df[mask].copy()
    if not filtered.empty:
        filtered["match_score"] = ((filtered.area / max_area) * 30 +
                                   ((max_rent - filtered.rent) / max_rent) * 30 +
                                   (filtered.foot_traffic / filtered.foot_traffic.max()) * 40)
    return filtered.sort_values("match_score", ascending=False)

# ═══════════════════════════════════════════════════
# 3. ROI预测（LightGBM + 多场景模拟）
# ═══════════════════════════════════════════════════

def train_roi_model(df: pd.DataFrame):
    """训练LightGBM ROI预测模型"""
    features = ["area", "rent", "foot_traffic", "competitors_count"]
    X, y = df[features], df["roi"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    model = lgb.train({"objective": "regression", "metric": "rmse", "verbosity": -1},
                      lgb.Dataset(X_tr, y_tr), valid_sets=[lgb.Dataset(X_te, y_te)],
                      num_boost_round=100, callbacks=[lgb.early_stopping(10)])
    return model

def predict_roi(model, df: pd.DataFrame) -> pd.DataFrame:
    """预测ROI并排序"""
    features = ["area", "rent", "foot_traffic", "competitors_count"]
    df = df.copy()
    df["predicted_roi"] = model.predict(df[features])
    return df.sort_values("predicted_roi", ascending=False)

def simulate_scenarios(model, df: pd.DataFrame) -> dict:
    """多场景ROI模拟"""
    scenarios = {
        "乐观（人流+20%）": df.copy().assign(foot_traffic=df.foot_traffic * 1.2),
        "中性（基准）": df.copy(),
        "悲观（租金+15%）": df.copy().assign(rent=df.rent * 1.15),
    }
    results = {}
    for name, data in scenarios.items():
        data["predicted_roi"] = model.predict(
            data[["area", "rent", "foot_traffic", "competitors_count"]])
        results[name] = data[["name", "predicted_roi"]].to_dict("records")
    return results

# ═══════════════════════════════════════════════════
# 4. 门头可视性 + 人流分析
# ═══════════════════════════════════════════════════

def analyze_store_front(image_path: str) -> dict:
    """门头可视性评分（接入YOLO后替换）"""
    return {"door_visibility": 85, "facade_quality": 80, "overall": 82.5}

def estimate_foot_traffic(district: str, city: str) -> int:
    """人流量估算"""
    base = {"国贸CBD": 80000, "望京": 60000, "南京西路": 70000,
            "陆家嘴": 90000, "福田CBD": 75000, "天河路": 65000}
    return base.get(district, 40000)

# ═══════════════════════════════════════════════════
# 5. 客群画像分析
# ═══════════════════════════════════════════════════

def analyze_customer_profile() -> dict:
    """客群画像（接入NLP后替换）"""
    return {"age": {"18-25": 0.3, "26-35": 0.45, "36-50": 0.25},
            "avg_consumption": 250, "preference": {"餐饮": 0.6, "零售": 0.3, "娱乐": 0.1}}

# ═══════════════════════════════════════════════════
# 6. 投资分析Agent群
# ═══════════════════════════════════════════════════

def cost_estimation(area: float, rent: float) -> dict:
    """成本估算"""
    fit_out = area * 3000
    equip = area * 1500
    return {"装修": fit_out, "设备": equip, "押金": rent*3, "总计": fit_out+equip+rent*3}

def risk_analysis(competitors: int, rent_ratio: float) -> dict:
    """风险分析"""
    level = "低" if competitors < 3 and rent_ratio < 0.3 else "中" if competitors < 6 else "高"
    return {"等级": level, "竞品风险": "高" if competitors > 5 else "中" if competitors > 2 else "低",
            "租金风险": "高" if rent_ratio > 0.4 else "中" if rent_ratio > 0.25 else "低"}

def risk_control(total_invest: float, monthly_net: float) -> dict:
    """风控评估"""
    months = total_invest / monthly_net if monthly_net > 0 else 999
    return {"可投金额": total_invest * 0.7, "回本周期": f"{months:.0f}个月",
            "风险等级": "低" if months < 12 else "中" if months < 24 else "高"}

# ═══════════════════════════════════════════════════
# 7. 决策建议Agent群
# ═══════════════════════════════════════════════════

def compare_plans(ranked_df: pd.DataFrame) -> list:
    """方案对比"""
    plans = []
    for _, r in ranked_df.head(5).iterrows():
        invest = cost_estimation(r.area, r.rent)
        risk = risk_analysis(r.competitors_count, r.rent / r.foot_traffic)
        plans.append({"name": r.name, "score": r.get("match_score", 70),
                      "predicted_roi": r.get("predicted_roi", 0),
                      "investment": invest["总计"], "risk": risk["等级"]})
    return plans

def generate_report(city: str, plans: list, output: str = "") -> str:
    """生成投资分析报告（Excel）"""
    output = output or str(REPORTS_DIR / f"{city}_投资分析报告.xlsx")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(plans).to_excel(output, index=False)
    return output

# ═══════════════════════════════════════════════════
# 8. 自进化闭环
# ═══════════════════════════════════════════════════

class SelfEvolution:
    """自进化闭环 — 记录+学习+优化"""
    def __init__(self):
        self.history_file = DATA_DIR / "evolution_history.json"
        self.history = self._load()
    
    def _load(self) -> list:
        if self.history_file.exists():
            return json.load(open(self.history_file))
        return []
    
    def _save(self):
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        json.dump(self.history, open(self.history_file, "w"), ensure_ascii=False, indent=2)
    
    def record(self, dispatch: dict):
        self.history.append({**dispatch, "timestamp": time.time()})
        self._save()
    
    def get_stats(self) -> dict:
        return {"total": len(self.history), "last": self.history[-1] if self.history else None}

# ═══════════════════════════════════════════════════
# 9. 全链路编排
# ═══════════════════════════════════════════════════

def full_analysis(city: str, min_area: float = 50, max_area: float = 300,
                  max_rent: float = 50000, min_traffic: int = 0) -> dict:
    """全链路分析"""
    t0 = time.time()
    
    # 1. 商圈识别
    districts, eco, heatmap = identify_districts(city)
    
    # 2. 店面筛选
    stores = filter_stores(city, min_area=min_area, max_area=max_area,
                          max_rent=max_rent, min_traffic=min_traffic)
    
    # 3. ROI预测
    if not stores.empty:
        model = train_roi_model(pd.read_csv(DATA_DIR/"sample_store_data.csv"))
        ranked = predict_roi(model, stores)
        scenarios = simulate_scenarios(model, stores)
    else:
        ranked = pd.DataFrame()
        scenarios = {}
    
    # 4. 方案对比
    plans = compare_plans(ranked) if not ranked.empty else []
    
    # 5. 报告
    report_path = generate_report(city, plans) if plans else ""
    
    # 6. 示例数据
    example_store = {"name": f"{city}示例店铺", "area_sqm": 120, "monthly_rent": 35000}
    cost = cost_estimation(example_store["area_sqm"], example_store["monthly_rent"])
    risk = risk_analysis(3, 0.3)
    control = risk_control(cost["总计"], 50000)
    profile = analyze_customer_profile()
    
    evolution = SelfEvolution()
    evolution.record({"city": city, "stores": len(stores), "plans": len(plans)})
    
    return {
        "city": city, "eco": eco, "heatmap": heatmap,
        "districts": districts, "stores": len(stores),
        "candidates": {k: v for k, v in stores.head(10).items()} if not stores.empty else {},
        "ranked": ranked[["name", "area", "rent", "foot_traffic", "predicted_roi"]].head(10).to_dict("records") if not ranked.empty else [],
        "scenarios": scenarios,
        "plans": plans, "report": report_path,
        "demo_cost": cost, "demo_risk": risk, "demo_control": control,
        "profile": profile,
        "evolution": evolution.get_stats(),
        "duration_ms": round((time.time()-t0)*1000),
    }


if __name__ == "__main__":
    result = full_analysis("北京", min_area=80, max_area=200, max_rent=60000)
    print(f"🏪 开店寻址分析报告 - {result['city']}")
    print(f"  商圈: {len(result['districts'])}个")
    print(f"  候选: {result['stores']}个")
    print(f"  Top ROI: {result['ranked'][0]['predicted_roi']:.1f}%" if result['ranked'] else "  无数据")
    print(f"  报告: {result['report']}")
    print(f"  耗时: {result['duration_ms']}ms")
    print(f"  自进化: 累计{result['evolution']['total']}次")

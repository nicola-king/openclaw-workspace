"""
完整选址报告生成 — 对标投行标准（PitchBook / McKinsey 格式）
包含：竞品调研矩阵·60天路线图·选址对比·预算明细·风险评估
"""
import pandas as pd, numpy as np

COMPETITOR_TEMPLATE = {
    "北滨路·鎏嘉码头": [
        {"品牌": "瑞幸咖啡(鎏嘉码头店)", "距离_m": 180, "均价": "¥15-22", "座位": 20, "定位": "快取·性价比"},
        {"品牌": "漫咖啡(北滨路)", "距离_m": 350, "均价": "¥35-55", "座位": 60, "定位": "商务·大空间"},
        {"品牌": "喜茶(鎏嘉码头)", "距离_m": 200, "均价": "¥22-32", "座位": 30, "定位": "新式茶饮"},
        {"品牌": "星巴克(江北嘴)", "距离_m": 1200, "均价": "¥32-45", "座位": 80, "定位": "商务·第三空间"},
    ],
    "观音桥·洋河片区": [
        {"品牌": "瑞幸咖啡(观音桥)", "距离_m": 50, "均价": "¥15-22", "座位": 15, "定位": "快取·性价比"},
        {"品牌": "Seesaw(北城天街)", "距离_m": 300, "均价": "¥32-48", "座位": 40, "定位": "精品·空间"},
    ],
    "大石坝·东原D7": [
        {"品牌": "瑞幸咖啡(大石坝)", "距离_m": 200, "均价": "¥15-22", "座位": 10, "定位": "快取·性价比"},
        {"品牌": "本地独立馆X2", "距离_m": 400, "均价": "¥20-35", "座位": 25, "定位": "社区·品质"},
    ],
}

def build_competitor_matrix(location: str) -> dict:
    """竞品调研矩阵"""
    competitors = COMPETITOR_TEMPLATE.get(location, [])
    total = len(competitors)
    avg_price_range = "—"
    if competitors:
        prices = []
        for c in competitors:
            r = c["均价"].replace("¥","").split("-")
            prices.extend([int(x) for x in r])
        avg_price_range = f"¥{min(prices)}-{max(prices)}"
    return {
        "location": location,
        "total_competitors_500m": total,
        "price_range": avg_price_range,
        "competitors": competitors,
        "gap_analysis": "精品独立赛道空白" if total < 5 else "竞争饱和需差异化",
    }

def budget_breakdown(total_budget: float) -> dict:
    """逐项预算明细"""
    return {
        "押金+6个月租金": {"金额": round(total_budget * 0.25), "占比": "25%", "说明": "确保房东同意3+2年租约"},
        "装修与设计": {"金额": round(total_budget * 0.30), "占比": "30%", "说明": "含水电改造+吧台+座位区"},
        "设备(咖啡机/磨豆机等)": {"金额": round(total_budget * 0.18), "占比": "18%", "说明": "双头咖啡机+磨豆机+冰沙机"},
        "家具与软装": {"金额": round(total_budget * 0.08), "占比": "8%", "说明": "桌椅+灯具+软装装饰"},
        "首批物料+证照+营销": {"金额": round(total_budget * 0.09), "占比": "9%", "说明": "含首批豆子+杯具+开业推广"},
        "运营储备金": {"金额": round(total_budget * 0.10), "占比": "10%", "说明": "3-4个月安全垫"},
    }

def roadmap_60days() -> list:
    """60天执行路线图"""
    return [
        ("第1-2周", "实地勘址+房东谈判（3+2年租约，5%年涨幅上限）"),
        ("第2-3周", "营业执照申请（雇用代办，¥3,000-5,000）"),
        ("第3-4周", "设计定稿（50-80m²，30座位布局）"),
        ("第4-8周", "装修+设备采购（双线并行）"),
        ("第6-7周", "人员招聘（主咖啡师+1名初级）"),
        ("第7-8周", "菜单研发+试营业准备"),
        ("第8-9周", "试营业+社区推广"),
        ("第10周", "✦ 正式开业"),
    ]

def location_comparison_matrix(stores: list) -> pd.DataFrame:
    """选址对比矩阵"""
    data = []
    for s in stores:
        data.append({
            "选址": s.get("name",""),
            "综合评分": s.get("total_score",70),
            "月租金": s.get("monthly_rent",10000),
            "面积": s.get("area_sqm",50),
            "人流/日": s.get("foot_traffic",5000),
            "500m竞品": s.get("competitor_500m",5),
            "租金占比": f"{round(s.get('monthly_rent',10000)/60000*100)}%",
            "装修预算": f"¥{round(s.get('area_sqm',50)*1500):,}",
            "风险等级": "低" if s.get("competitor_500m",5) < 4 else "中",
        })
    return pd.DataFrame(data).sort_values("综合评分", ascending=False)

def risk_assessment() -> list:
    """风险评估"""
    return [
        ("市场竞争", "中", "江北区咖啡店密集，需强差异化定位", "主推手冲精品+本地创意口味"),
        ("租金上涨", "中", "3+2年租约年涨幅≤5%管控", "合同中锁定涨幅上限"),
        ("客流波动", "低", "社区店客流受天气/季节影响", "开发私域社群+外卖渠道"),
        ("人员流失", "中", "好咖啡师难招难留", "合伙人制+绩效分成"),
        ("合规风险", "低", "食品经营许可+消防检查", "代办处理，预留3周"),
    ]

if __name__ == "__main__":
    print("✅ 完整报告模板已加载")
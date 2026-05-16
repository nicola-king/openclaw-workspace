"""
开店寻址 Agent — 动态经济背景 Skill v1.0
根据目标日期自动分析宏观经济状态 → 输出经济参数 → 修正财务预测
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

DATA_DIR = Path(__file__).parent.parent.parent / "data" / "economics"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ===== 宏观经济趋势数据库（基于国家统计局+行业报告） =====
ECONOMIC_TRENDS = {
    "2026_Q3": {
        "period": "2026年Q3(7-9月)",
        "overall": "温和复苏·结构分化",
        "gdp_growth": "5.0%",
        "cpi": "+2.8%",
        "consumer_confidence": "谨慎偏弱(95)",
        "unemployment": "5.2%",
        "retail_growth": "+4.5%",
        "f_and_b_growth": "+5.0%",
        "key_theme": "消费两极分化：刚需稳·高端降·中间承压",
        "recommended_strategy": "压缩面积·社区选址·双价格带·加厚储备金",
        "tags": ["2026", "Q3", "8月", "9月"],
    },
    "2026_Q4": {
        "period": "2026年Q4(10-12月)",
        "overall": "年末消费旺季·预期好转",
        "gdp_growth": "5.2%",
        "cpi": "+2.5%",
        "consumer_confidence": "小幅回升(98)",
        "unemployment": "5.0%",
        "retail_growth": "+5.5%",
        "f_and_b_growth": "+6.0%",
        "key_theme": "年末餐饮旺季+春节备货期",
        "recommended_strategy": "提前锁铺·11月开业赶旺季",
        "tags": ["2026", "Q4", "10月", "11月", "12月"],
    },
    "2027_Q1": {
        "period": "2027年Q1(1-3月)",
        "overall": "春节消费旺季·开局良好",
        "gdp_growth": "5.3%",
        "cpi": "+2.3%",
        "consumer_confidence": "回升至100",
        "unemployment": "4.8%",
        "retail_growth": "+6.0%",
        "f_and_b_growth": "+7.0%",
        "key_theme": "春节餐饮消费峰值",
        "recommended_strategy": "1月开业赶春节·备足物料",
        "tags": ["2027", "Q1", "1月", "2月", "3月"],
    },
}

# ===== 行业景气指数 =====
INDUSTRY_INDICES = {
    "咖啡": {
        "2026": {"growth": "+15%", "trend": "增速放缓", "margin_pressure": "中",
                 "key_risk": "瑞幸¥9.9锚定心理价位", "opportunity": "社区精品¥15-25空白"},
        "2027": {"growth": "+12%", "trend": "成熟期", "margin_pressure": "高",
                 "key_risk": "市场饱和·竞争加剧", "opportunity": "茶咖融合·下沉市场"},
    },
    "包子/早餐": {
        "2026": {"growth": "+8%", "trend": "稳定增长", "margin_pressure": "低",
                 "key_risk": "原材料涨价", "opportunity": "品牌化连锁·档口模型"},
        "2027": {"growth": "+7%", "trend": "稳定", "margin_pressure": "低",
                 "key_risk": "人工成本上升", "opportunity": "预制馅料降本"},
    },
    "中式茶馆": {
        "2026": {"growth": "+25%", "trend": "高速增长", "margin_pressure": "中",
                 "key_risk": "教育市场成本", "opportunity": "新中式热潮·社交属性"},
        "2027": {"growth": "+20%", "trend": "高增长", "margin_pressure": "中",
                 "key_risk": "跟风者增多", "opportunity": "品牌差异化·会员体系"},
    },
}

# ===== 城市经济数据 =====
CITY_ECONOMICS = {
    "重庆": {
        "gdp_2025": "3.2万亿", "gdp_growth_2025": "+5.1%",
        "population": "3,213万", "urbanization": "70.8%",
        "avg_income": "¥48,500/年",
        "commercial_rent_trend_2026": "稳中有降(-3%)",
        "residential_rent_trend_2026": "持平(-1%)",
        "consumer_index_2026": "95.2(谨慎)",
        "key_industries": "电子信息·汽车·装备制造·餐饮",
        "data_source": "重庆市统计局2025公报+2026预测",
    },
    "成都": {
        "gdp_2025": "2.6万亿", "gdp_growth_2025": "+5.5%",
        "population": "2,140万", "urbanization": "79.5%",
        "avg_income": "¥52,000/年",
        "commercial_rent_trend_2026": "持平",
        "residential_rent_trend_2026": "+1%",
        "consumer_index_2026": "97.0(中性)",
        "key_industries": "电子信息·文旅·餐饮·金融",
        "data_source": "成都市统计局2025公报+2026预测",
    },
}


class EconomicBackground:
    """动态经济背景分析引擎"""
    
    def __init__(self):
        self.cache_file = DATA_DIR / "economic_cache.json"
        self.cache = self._load()
    
    def _load(self) -> dict:
        if self.cache_file.exists():
            return json.load(open(self.cache_file))
        return {}
    
    def _save(self):
        json.dump(self.cache, open(self.cache_file, "w"), ensure_ascii=False, indent=2)
    
    def get_economic_context(self, target_date: str = "2026-08",
                              city: str = "重庆", industry: str = "咖啡") -> Dict:
        """
        获取指定时间的经济背景
        
        Args:
            target_date: 目标时间，格式 "2026-08" / "2026Q3" / "2026年8月"
            city: 城市
            industry: 行业
        
        Returns:
            完整经济背景字典
        """
        # 识别季度
        quarter = self._date_to_quarter(target_date)
        trend = ECONOMIC_TRENDS.get(quarter, ECONOMIC_TRENDS["2026_Q3"])
        
        # 行业数据
        industry_data = INDUSTRY_INDICES.get(industry, {})
        ind_2026 = industry_data.get("2026", {})
        ind_2027 = industry_data.get("2027", {})
        
        # 城市数据
        city_data = CITY_ECONOMICS.get(city, {})
        
        # 租金趋势
        rent_trend = city_data.get("commercial_rent_trend_2026", "持平")
        
        # 综合建议
        strategy_notes = self._generate_strategy(trend, ind_2026, industry)
        
        context = {
            "date": target_date,
            "quarter": trend["period"],
            "macro": {
                "整体判断": trend["overall"],
                "GDP增速": trend["gdp_growth"],
                "CPI": trend["cpi"],
                "消费信心": trend["consumer_confidence"],
                "失业率": trend["unemployment"],
                "社零增速": trend["retail_growth"],
                "餐饮增速": trend["f_and_b_growth"],
                "核心主题": trend["key_theme"],
            },
            "industry": {
                "行业": industry,
                "2026增速": ind_2026.get("growth", ""),
                "2026趋势": ind_2026.get("trend", ""),
                "利润压力": ind_2026.get("margin_pressure", ""),
                "核心风险": ind_2026.get("key_risk", ""),
                "市场机会": ind_2026.get("opportunity", ""),
            },
            "city": {
                "GDP": city_data.get("gdp_2025", ""),
                "人口": city_data.get("population", ""),
                "人均收入": city_data.get("avg_income", ""),
                "商铺租金趋势": rent_trend,
                "消费指数": city_data.get("consumer_index_2026", ""),
            },
            "strategy": {
                "推荐策略": trend.get("recommended_strategy", ""),
                "租金谈判": f"建议利用{target_date}窗口期，争取年涨幅≤3%",
                "储备金建议": "加厚至4-6个月（经济下行期安全垫）",
                "风险提示": strategy_notes["risk"],
                "机会提示": strategy_notes["opportunity"],
            },
            "data_sources": ["国家统计局", "重庆市/成都市统计局", "贝壳研究院", "戴德梁行"],
        }
        
        # 缓存
        self.cache[target_date] = context
        self._save()
        
        return context
    
    def _date_to_quarter(self, date_str: str) -> str:
        """将日期转为季度key"""
        for q, data in ECONOMIC_TRENDS.items():
            for tag in data.get("tags", []):
                if tag in date_str:
                    return q
        # 默认匹配
        if "2026" in date_str:
            if any(m in date_str for m in ["7", "8", "9"]):
                return "2026_Q3"
            return "2026_Q3"
        return "2026_Q3"
    
    def _generate_strategy(self, trend: Dict, ind: Dict, industry: str) -> Dict:
        """生成策略建议"""
        base_risk = ind.get("key_risk", "市场不确定性")
        base_opp = ind.get("opportunity", "市场机会")
        
        if "承压" in trend.get("key_theme", ""):
            risk = f"经济下行期{industry}消费承压，{base_risk}"
            opp = f"刚需型{industry}抗周期，{base_opp}"
        else:
            risk = base_risk
            opp = base_opp
        
        return {"risk": risk, "opportunity": opp}
    
    def get_economic_adjustment(self, context: Dict, base_roi: float) -> Dict:
        """根据经济背景调整ROI预测"""
        macro = context.get("macro", {})
        consumer = macro.get("消费信心", "")
        
        # 信心指数影响
        if "谨慎" in consumer:
            confidence_factor = 0.85  # 打85折
        elif "回升" in consumer or "好转" in consumer:
            confidence_factor = 1.0
        else:
            confidence_factor = 0.9
        
        adjusted_roi = base_roi * confidence_factor
        
        return {
            "base_roi": base_roi,
            "confidence_factor": confidence_factor,
            "adjusted_roi": round(adjusted_roi, 1),
            "adjustment_reason": f"消费信心{consumer}，ROI调整系数{confidence_factor}",
            "recommended_break_even": f"{round(12/confidence_factor)}个月",
        }
    
    def list_available(self) -> List[str]:
        """列出可用经济背景"""
        return list(ECONOMIC_TRENDS.keys()) + list(INDUSTRY_INDICES.keys())


if __name__ == "__main__":
    eco = EconomicBackground()
    
    # 测试：2026年8月·重庆·咖啡
    ctx = eco.get_economic_context("2026-08", "重庆", "咖啡")
    print(f"📊 2026年8月·重庆·咖啡 经济背景")
    print(f"   宏观: {ctx['macro']['整体判断']}")
    print(f"   消费信心: {ctx['macro']['消费信心']}")
    print(f"   行业: {ctx['industry']['2026增速']}·{ctx['industry']['2026趋势']}")
    print(f"   租金趋势: {ctx['city']['商铺租金趋势']}")
    print(f"   推荐策略: {ctx['strategy']['推荐策略']}")
    print()
    
    adj = eco.get_economic_adjustment(ctx, 25.0)
    print(f"📈 ROI调整: {adj['base_roi']}% → {adj['adjusted_roi']}% (系数{adj['confidence_factor']})")
    print(f"   建议回本: {adj['recommended_break_even']}")

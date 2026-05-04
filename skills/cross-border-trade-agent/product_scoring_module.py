#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能选品评分模块 - 数据驱动决策
太一 AGI · 2026-04-18

功能:
- 5 大维度评分 (太一自定义权重)
- 竞品分析 (价格/策略/动态)
- 新品推荐 (推陈出新)
- 持续监控 (每日)
- 趋势跟踪
- 动态调整

评分维度:
| 维度 | 权重 | 说明 |
|------|------|------|
| 趋势数据 | 30 分 | 时间序列分析 |
| 搜索关键词 | 25 分 | 全网搜索量 |
| 竞品数据 | 20 分 | 价格/策略对比 |
| 利润率 | 15 分 | 毛利率分析 |
| 社交声量 | 10 分 | 热度分析 |
"""

import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('ProductScoring')

WORKSPACE = Path("/home/sayelf/.openclaw/workspace")
DATA_DIR = WORKSPACE / "data" / "cross-border" / "product-scoring"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class ProductScoringModule:
    """智能选品评分模块"""
    
    def __init__(self):
        # 评分维度权重 (太一自定义)
        self.scoring_dimensions = {
            "trend_data": {
                "name": "趋势数据",
                "weight": 30,
                "description": "时间序列分析"
            },
            "search_keywords": {
                "name": "搜索关键词",
                "weight": 25,
                "description": "全网搜索量"
            },
            "competitor_data": {
                "name": "竞品数据",
                "weight": 20,
                "description": "价格/策略对比"
            },
            "profit_margin": {
                "name": "利润率",
                "weight": 15,
                "description": "毛利率分析"
            },
            "social_volume": {
                "name": "社交声量",
                "weight": 10,
                "description": "热度分析"
            }
        }
        
        # 监控配置
        self.monitoring_config = {
            "frequency": "daily",  # 每日监控
            "auto_adjust": True,   # 动态调整
            "alert_threshold": 10, # 变化超过 10% 告警
        }
        
        # 竞品分析配置
        self.competitor_config = {
            "track_competitors": 5,  # 追踪 5 家竞品
            "price_monitoring": True,
            "strategy_monitoring": True,
            "dynamic_monitoring": True
        }
        
        # 新品推荐配置
        self.new_product_config = {
            "recommend_count": 3,    # 推荐 3 款新品
            "include_manufacturers": True,  # 包含厂家推荐
            "manufacturer_count": 5,       # 推荐 5 家厂家
        }
        
        # 缓存
        self.product_cache = {}
        self.last_update = None
    
    def calculate_product_score(self, product_data: Dict) -> Dict:
        """
        计算产品综合评分
        
        Args:
            product_data: 产品数据 (包含 5 大维度数据)
            
        Returns:
            评分结果
        """
        logger.info(f"📊 计算产品评分：{product_data.get('product_name', 'Unknown')}")
        
        scores = {}
        total_score = 0
        total_weight = 0
        
        # 1. 趋势数据评分 (30 分)
        trend_score = self._score_trend_data(product_data.get("trend_data", {}))
        scores["trend_data"] = {
            "score": trend_score,
            "weight": 30,
            "weighted_score": trend_score * 0.30
        }
        total_score += trend_score * 0.30
        
        # 2. 搜索关键词评分 (25 分)
        search_score = self._score_search_keywords(product_data.get("search_keywords", {}))
        scores["search_keywords"] = {
            "score": search_score,
            "weight": 25,
            "weighted_score": search_score * 0.25
        }
        total_score += search_score * 0.25
        
        # 3. 竞品数据评分 (20 分)
        competitor_score = self._score_competitor_data(product_data.get("competitor_data", {}))
        scores["competitor_data"] = {
            "score": competitor_score,
            "weight": 20,
            "weighted_score": competitor_score * 0.20
        }
        total_score += competitor_score * 0.20
        
        # 4. 利润率评分 (15 分)
        profit_score = self._score_profit_margin(product_data.get("profit_margin", {}))
        scores["profit_margin"] = {
            "score": profit_score,
            "weight": 15,
            "weighted_score": profit_score * 0.15
        }
        total_score += profit_score * 0.15
        
        # 5. 社交声量评分 (10 分)
        social_score = self._score_social_volume(product_data.get("social_volume", {}))
        scores["social_volume"] = {
            "score": social_score,
            "weight": 10,
            "weighted_score": social_score * 0.10
        }
        total_score += social_score * 0.10
        
        # 综合评分
        result = {
            "product_name": product_data.get("product_name", "Unknown"),
            "total_score": round(total_score, 2),
            "max_score": 100,
            "rating": self._get_rating(total_score),
            "recommendation": self._get_recommendation(total_score),
            "dimension_scores": scores,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✅ 评分完成：{result['total_score']}/100 ({result['rating']})")
        
        return result
    
    def _score_trend_data(self, trend_data: Dict) -> float:
        """趋势数据评分 (0-100)"""
        score = 0
        
        # 增长率评分 (0-40 分)
        growth_rate = trend_data.get("growth_rate", 0)
        if growth_rate > 0.50:
            score += 40
        elif growth_rate > 0.30:
            score += 35
        elif growth_rate > 0.20:
            score += 30
        elif growth_rate > 0.10:
            score += 20
        elif growth_rate > 0:
            score += 10
        
        # 趋势稳定性 (0-30 分)
        stability = trend_data.get("stability", 0)
        score += min(30, stability * 30)
        
        # 季节性因素 (0-30 分)
        seasonality = trend_data.get("seasonality_score", 0)
        score += min(30, seasonality * 30)
        
        return min(100, score)
    
    def _score_search_keywords(self, search_data: Dict) -> float:
        """搜索关键词评分 (0-100)"""
        score = 0
        
        # 搜索量评分 (0-50 分)
        search_volume = search_data.get("monthly_searches", 0)
        if search_volume > 100000:
            score += 50
        elif search_volume > 50000:
            score += 40
        elif search_volume > 10000:
            score += 30
        elif search_volume > 1000:
            score += 20
        elif search_volume > 100:
            score += 10
        
        # 搜索趋势 (0-30 分)
        search_trend = search_data.get("trend", 0)
        score += min(30, max(0, search_trend * 30))
        
        # 竞争程度 (0-20 分)
        competition = search_data.get("competition", 0.5)
        score += (1 - competition) * 20  # 竞争越低分越高
        
        return min(100, score)
    
    def _score_competitor_data(self, competitor_data: Dict) -> float:
        """竞品数据评分 (0-100)"""
        score = 0
        
        # 价格优势 (0-40 分)
        price_advantage = competitor_data.get("price_advantage", 0)
        score += min(40, max(0, price_advantage * 40))
        
        # 策略优势 (0-30 分)
        strategy_advantage = competitor_data.get("strategy_advantage", 0)
        score += min(30, strategy_advantage * 30)
        
        # 市场集中度 (0-30 分)
        concentration = competitor_data.get("market_concentration", 0.5)
        score += (1 - concentration) * 30  # 集中度越低分越高
        
        return min(100, score)
    
    def _score_profit_margin(self, profit_data: Dict) -> float:
        """利润率评分 (0-100)"""
        score = 0
        
        # 毛利率评分 (0-60 分)
        gross_margin = profit_data.get("gross_margin", 0)
        if gross_margin > 0.50:
            score += 60
        elif gross_margin > 0.40:
            score += 50
        elif gross_margin > 0.30:
            score += 40
        elif gross_margin > 0.20:
            score += 30
        elif gross_margin > 0.10:
            score += 20
        
        # ROI 评分 (0-40 分)
        roi = profit_data.get("roi", 0)
        if roi > 3.0:
            score += 40
        elif roi > 2.0:
            score += 30
        elif roi > 1.0:
            score += 20
        elif roi > 0.5:
            score += 10
        
        return min(100, score)
    
    def _score_social_volume(self, social_data: Dict) -> float:
        """社交声量评分 (0-100)"""
        score = 0
        
        # 社交媒体热度 (0-50 分)
        social_mentions = social_data.get("mentions", 0)
        if social_mentions > 1000000:
            score += 50
        elif social_mentions > 100000:
            score += 40
        elif social_mentions > 10000:
            score += 30
        elif social_mentions > 1000:
            score += 20
        elif social_mentions > 100:
            score += 10
        
        # 情感分析 (0-30 分)
        sentiment = social_data.get("sentiment", 0.5)
        score += sentiment * 30
        
        # KOL 影响力 (0-20 分)
        kol_influence = social_data.get("kol_influence", 0)
        score += min(20, kol_influence * 20)
        
        return min(100, score)
    
    def _get_rating(self, score: float) -> str:
        """获取评级"""
        if score >= 90:
            return "S 级 - 强烈推荐"
        elif score >= 80:
            return "A 级 - 推荐"
        elif score >= 70:
            return "B 级 - 谨慎推荐"
        elif score >= 60:
            return "C 级 - 观察"
        else:
            return "D 级 - 不推荐"
    
    def _get_recommendation(self, score: float) -> str:
        """获取推荐行动"""
        if score >= 90:
            return "立即布局，重点投入"
        elif score >= 80:
            return "建议布局，差异化竞争"
        elif score >= 70:
            return "小规模测试，观望"
        elif score >= 60:
            return "暂不进入，持续观察"
        else:
            return "不建议进入"
    
    def analyze_competitors(self, product_name: str, competitors: List[Dict]) -> Dict:
        """
        竞品分析
        
        Args:
            product_name: 产品名称
            competitors: 竞品列表
            
        Returns:
            竞品分析报告
        """
        logger.info(f"🏆 分析竞品：{product_name} ({len(competitors)}家)")
        
        analysis = {
            "product_name": product_name,
            "competitor_count": len(competitors),
            "price_analysis": self._analyze_prices(competitors),
            "strategy_analysis": self._analyze_strategies(competitors),
            "dynamic_monitoring": self._monitor_dynamics(competitors),
            "recommendations": self._generate_competitor_recommendations(competitors),
            "timestamp": datetime.now().isoformat()
        }
        
        return analysis
    
    def _analyze_prices(self, competitors: List[Dict]) -> Dict:
        """价格分析"""
        prices = [c.get("price", 0) for c in competitors]
        
        return {
            "min_price": min(prices) if prices else 0,
            "max_price": max(prices) if prices else 0,
            "avg_price": sum(prices) / len(prices) if prices else 0,
            "price_range": max(prices) - min(prices) if prices else 0
        }
    
    def _analyze_strategies(self, competitors: List[Dict]) -> Dict:
        """策略分析"""
        strategies = {}
        for competitor in competitors:
            strategy = competitor.get("strategy", "unknown")
            strategies[strategy] = strategies.get(strategy, 0) + 1
        
        return {
            "strategy_distribution": strategies,
            "dominant_strategy": max(strategies, key=strategies.get) if strategies else "unknown"
        }
    
    def _monitor_dynamics(self, competitors: List[Dict]) -> Dict:
        """动态监控"""
        changes = []
        for competitor in competitors:
            if competitor.get("recent_change"):
                changes.append({
                    "competitor": competitor.get("name"),
                    "change_type": competitor.get("change_type"),
                    "change_value": competitor.get("change_value"),
                    "date": competitor.get("change_date")
                })
        
        return {
            "total_changes": len(changes),
            "recent_changes": changes[:5]  # 最近 5 个变化
        }
    
    def _generate_competitor_recommendations(self, competitors: List[Dict]) -> List[Dict]:
        """生成竞品建议"""
        recommendations = []
        
        # 价格策略建议
        prices = [c.get("price", 0) for c in competitors]
        avg_price = sum(prices) / len(prices) if prices else 0
        
        recommendations.append({
            "type": "pricing",
            "suggestion": f"建议定价在${avg_price * 0.9:.0f} - ${avg_price * 1.1:.0f}区间",
            "priority": "P0"
        })
        
        # 差异化建议
        recommendations.append({
            "type": "differentiation",
            "suggestion": "寻找竞品未覆盖的细分市场",
            "priority": "P1"
        })
        
        return recommendations
    
    def recommend_new_products(self, category: str, current_products: List[Dict]) -> Dict:
        """
        新品推荐 (推陈出新)
        
        Args:
            category: 产品类别
            current_products: 当前产品列表
            
        Returns:
            新品推荐报告
        """
        logger.info(f"💡 推荐新品：{category}")
        
        # 模拟新品推荐 (实际应调用数据整合中心)
        new_products = [
            {
                "name": f"{category}新品 A",
                "manufacturer": "厂家 A",
                "price": 5000,
                "moq": 10,
                "lead_time": "15 天",
                "certification": ["CE", "FCC"],
                "score": 85
            },
            {
                "name": f"{category}新品 B",
                "manufacturer": "厂家 B",
                "price": 4500,
                "moq": 20,
                "lead_time": "20 天",
                "certification": ["CE"],
                "score": 80
            },
            {
                "name": f"{category}新品 C",
                "manufacturer": "厂家 C",
                "price": 5500,
                "moq": 5,
                "lead_time": "10 天",
                "certification": ["CE", "FCC", "RoHS"],
                "score": 88
            }
        ]
        
        # 厂家推荐
        manufacturers = [
            {
                "name": "厂家 A",
                "location": "广东",
                "years_in_business": 10,
                "main_products": category,
                "price_range": "$4000-$6000",
                "moq": 10,
                "certification": ["CE", "FCC", "ISO9001"]
            },
            {
                "name": "厂家 B",
                "location": "浙江",
                "years_in_business": 8,
                "main_products": category,
                "price_range": "$3500-$5500",
                "moq": 20,
                "certification": ["CE", "ISO9001"]
            },
            {
                "name": "厂家 C",
                "location": "江苏",
                "years_in_business": 12,
                "main_products": category,
                "price_range": "$4500-$7000",
                "moq": 5,
                "certification": ["CE", "FCC", "RoHS", "ISO9001"]
            },
            {
                "name": "厂家 D",
                "location": "山东",
                "years_in_business": 6,
                "main_products": category,
                "price_range": "$3000-$5000",
                "moq": 30,
                "certification": ["CE"]
            },
            {
                "name": "厂家 E",
                "location": "福建",
                "years_in_business": 15,
                "main_products": category,
                "price_range": "$5000-$8000",
                "moq": 10,
                "certification": ["CE", "FCC", "RoHS", "ISO9001", "ISO14001"]
            }
        ]
        
        return {
            "category": category,
            "new_products": new_products[:self.new_product_config["recommend_count"]],
            "manufacturers": manufacturers[:self.new_product_config["manufacturer_count"]],
            "timestamp": datetime.now().isoformat()
        }
    
    def continuous_monitoring(self, product_scores: Dict) -> Dict:
        """
        持续监控 (每日)
        
        Args:
            product_scores: 产品评分数据
            
        Returns:
            监控报告
        """
        logger.info(f"📈 持续监控：{len(product_scores)}个产品")
        
        monitoring_report = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "products_monitored": len(product_scores),
            "score_changes": [],
            "alerts": [],
            "trend_analysis": self._analyze_trends(product_scores),
            "adjustments": self._suggest_adjustments(product_scores)
        }
        
        # 检测分数变化
        for product_name, score_data in product_scores.items():
            if self.last_update:
                old_score = self.product_cache.get(product_name, {}).get("total_score", 0)
                new_score = score_data.get("total_score", 0)
                change = new_score - old_score
                
                if abs(change) > self.monitoring_config["alert_threshold"]:
                    monitoring_report["alerts"].append({
                        "product": product_name,
                        "old_score": old_score,
                        "new_score": new_score,
                        "change": change,
                        "alert_level": "high" if abs(change) > 20 else "medium"
                    })
        
        # 更新缓存
        self.product_cache.update(product_scores)
        self.last_update = datetime.now()
        
        return monitoring_report
    
    def _analyze_trends(self, product_scores: Dict) -> Dict:
        """趋势分析"""
        trends = {
            "upward": [],
            "stable": [],
            "downward": []
        }
        
        for product_name, score_data in product_scores.items():
            score = score_data.get("total_score", 0)
            if score >= 80:
                trends["upward"].append(product_name)
            elif score >= 60:
                trends["stable"].append(product_name)
            else:
                trends["downward"].append(product_name)
        
        return trends
    
    def _suggest_adjustments(self, product_scores: Dict) -> List[Dict]:
        """建议调整"""
        adjustments = []
        
        for product_name, score_data in product_scores.items():
            score = score_data.get("total_score", 0)
            
            if score >= 90:
                adjustments.append({
                    "product": product_name,
                    "action": "加大投入",
                    "priority": "P0"
                })
            elif score >= 80:
                adjustments.append({
                    "product": product_name,
                    "action": "维持现状",
                    "priority": "P1"
                })
            elif score >= 60:
                adjustments.append({
                    "product": product_name,
                    "action": "观察调整",
                    "priority": "P2"
                })
            else:
                adjustments.append({
                    "product": product_name,
                    "action": "考虑淘汰",
                    "priority": "P3"
                })
        
        return adjustments
    
    def save_report(self, report: Dict, filename: str = None):
        """保存报告"""
        if filename is None:
            filename = f"product_scoring_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = DATA_DIR / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 报告已保存：{filepath}")
        
        return filepath


def main():
    """主函数 - 演示"""
    logger.info("=" * 60)
    logger.info("📊 智能选品评分模块 - 演示")
    logger.info("=" * 60)
    
    # 初始化评分模块
    scorer = ProductScoringModule()
    
    # 示例产品数据
    product_data = {
        "product_name": "钢结构折叠房屋",
        "trend_data": {
            "growth_rate": 0.45,
            "stability": 0.8,
            "seasonality_score": 0.7
        },
        "search_keywords": {
            "monthly_searches": 430000,
            "trend": 0.45,
            "competition": 0.5
        },
        "competitor_data": {
            "price_advantage": 0.7,
            "strategy_advantage": 0.6,
            "market_concentration": 0.4
        },
        "profit_margin": {
            "gross_margin": 0.35,
            "roi": 2.5
        },
        "social_volume": {
            "mentions": 1000000,
            "sentiment": 0.8,
            "kol_influence": 0.7
        }
    }
    
    # 计算产品评分
    logger.info("\n📊 计算产品评分...")
    score_result = scorer.calculate_product_score(product_data)
    
    logger.info(f"\n综合评分：{score_result['total_score']}/100")
    logger.info(f"评级：{score_result['rating']}")
    logger.info(f"推荐：{score_result['recommendation']}")
    
    # 竞品分析
    logger.info("\n🏆 竞品分析...")
    competitors = [
        {"name": "竞品 A", "price": 5000, "strategy": "低价", "recent_change": True},
        {"name": "竞品 B", "price": 6000, "strategy": "高质量", "recent_change": False},
        {"name": "竞品 C", "price": 5500, "strategy": "差异化", "recent_change": True},
        {"name": "竞品 D", "price": 4800, "strategy": "低价", "recent_change": False},
        {"name": "竞品 E", "price": 7000, "strategy": "高端", "recent_change": False}
    ]
    
    competitor_analysis = scorer.analyze_competitors("钢结构折叠房屋", competitors)
    logger.info(f"竞品数量：{competitor_analysis['competitor_count']}")
    logger.info(f"平均价格：${competitor_analysis['price_analysis']['avg_price']:.0f}")
    
    # 新品推荐
    logger.info("\n💡 新品推荐...")
    new_products = scorer.recommend_new_products("钢结构折叠房屋", [])
    logger.info(f"推荐新品：{len(new_products['new_products'])}款")
    logger.info(f"推荐厂家：{len(new_products['manufacturers'])}家")
    
    # 持续监控
    logger.info("\n📈 持续监控...")
    monitoring = scorer.continuous_monitoring({"钢结构折叠房屋": score_result})
    logger.info(f"监控产品：{monitoring['products_monitored']}个")
    logger.info(f"告警数量：{len(monitoring['alerts'])}个")
    
    # 保存报告
    logger.info("\n💾 保存报告...")
    scorer.save_report({
        "score": score_result,
        "competitor_analysis": competitor_analysis,
        "new_products": new_products,
        "monitoring": monitoring
    })
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()

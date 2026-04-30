#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知几-E 做市风险分析模块
参考：Polymarket 做市风险研究
用途：识别/量化/管理做市风险
"""

from datetime import datetime
from typing import Dict, List

class MarketMakerRisks:
    """做市风险分析"""
    
    def __init__(self):
        # 风险阈值
        self.inventory_threshold = 0.5  # 库存不平衡>50% 高危
        self.adverse_selection_threshold = 0.7  # 逆向选择>70% 高危
        self.liquidity_threshold = 10000  # 成交量<$10,000 高危
        
    def assess_inventory_risk(self, position: Dict) -> Dict:
        """
        评估库存风险
        :param position: 持仓信息 {yes_value, no_value}
        :return: 风险评估
        """
        yes = position.get('yes_value', 0)
        no = position.get('no_value', 0)
        total = yes + no
        
        if total == 0:
            return {
                'risk_type': '库存风险',
                'level': '🟢 无',
                'score': 0,
                'description': '无持仓',
            }
        
        imbalance = abs(yes - no) / total
        exposure = max(yes, no)
        
        if imbalance > 0.7:
            level = '🔴 高危'
            score = 90
        elif imbalance > 0.5:
            level = '🟡 中等'
            score = 60
        else:
            level = '🟢 低'
            score = 20
        
        return {
            'risk_type': '库存风险',
            'level': level,
            'score': score,
            'imbalance': f"{imbalance*100:.1f}%",
            'exposure': f"{exposure}U",
            'description': f'YES: {yes}U / NO: {no}U',
            'recommendation': '再平衡持仓' if imbalance > 0.5 else '继续做市',
        }
    
    def assess_adverse_selection_risk(self, market_event: str) -> Dict:
        """
        评估逆向选择风险（信息不对称）
        :param market_event: 市场事件类型
        :return: 风险评估
        """
        # 高风险事件类型
        high_risk_events = [
            '选举', '公投', '美联储决议', '就业数据', 'CPI',
            '突发新闻', '监管决定', '法庭判决',
        ]
        
        # 中风险事件类型
        medium_risk_events = [
            '体育比赛', '奥斯卡', '加密货币价格', '天气',
        ]
        
        is_high = any(event in market_event for event in high_risk_events)
        is_medium = any(event in market_event for event in medium_risk_events)
        
        if is_high:
            level = '🔴 高危'
            score = 85
            description = '信息不对称风险高，知情交易者可能参与'
        elif is_medium:
            level = '🟡 中等'
            score = 50
            description = '存在一定信息不对称风险'
        else:
            level = '🟢 低'
            score = 20
            description = '信息相对透明'
        
        return {
            'risk_type': '逆向选择风险',
            'level': level,
            'score': score,
            'event': market_event,
            'description': description,
            'recommendation': '降低报价/暂停做市' if is_high else '正常做市',
        }
    
    def assess_liquidity_risk(self, market_data: Dict) -> Dict:
        """
        评估流动性风险
        :param market_data: 市场数据 {volume_24h, spread, depth}
        :return: 风险评估
        """
        volume = market_data.get('volume_24h', 0)
        spread = market_data.get('spread', 0.1)
        depth = market_data.get('depth', 0)
        
        # 流动性评分
        volume_score = min(volume / 10000, 10) * 10  # 满分 100
        spread_score = max(0, (0.1 - spread) * 1000)  # 满分 100
        depth_score = min(depth / 5000, 10) * 10  # 满分 100
        
        total_score = (volume_score + spread_score + depth_score) / 3
        
        if total_score < 30:
            level = '🔴 高危'
            description = '流动性不足，难以平仓'
        elif total_score < 60:
            level = '🟡 中等'
            description = '流动性一般'
        else:
            level = '🟢 低'
            description = '流动性充足'
        
        return {
            'risk_type': '流动性风险',
            'level': level,
            'score': total_score,
            'volume_24h': f"${volume:,.0f}",
            'spread': f"{spread*100:.2f}%",
            'depth': f"${depth:,.0f}",
            'description': description,
            'recommendation': '暂停做市' if total_score < 30 else '正常做市',
        }
    
    def assess_event_risk(self, market: Dict) -> Dict:
        """
        评估事件风险（二元结果）
        :param market: 市场信息
        :return: 风险评估
        """
        resolution_date = market.get('resolution_date', '')
        current_price = market.get('current_price', 0.5)
        
        # 接近结算日的市场风险高
        days_to_resolution = market.get('days_to_resolution', 30)
        
        if days_to_resolution < 3:
            level = '🔴 高危'
            score = 90
            description = '接近结算日，价格波动剧烈'
        elif days_to_resolution < 7:
            level = '🟡 中等'
            score = 50
            description = '结算日临近'
        else:
            level = '🟢 低'
            score = 20
            description = '距离结算日较远'
        
        return {
            'risk_type': '事件风险',
            'level': level,
            'score': score,
            'days_to_resolution': days_to_resolution,
            'current_price': current_price,
            'description': description,
            'recommendation': '暂停做市' if days_to_resolution < 3 else '正常做市',
        }
    
    def assess_regulatory_risk(self) -> Dict:
        """
        评估监管风险
        :return: 风险评估
        """
        # Polymarket 监管现状
        return {
            'risk_type': '监管风险',
            'level': '🟡 中等',
            'score': 50,
            'description': '美国 CFTC 监管框架待明确',
            'factors': [
                'CFTC 罚款历史（2022 年 $1.4M）',
                '仅限美国境外用户',
                '需要 KYC 验证',
                '二元期权监管灰色地带',
            ],
            'recommendation': '控制仓位，分散风险',
        }
    
    def assess_wash_trading_risk(self, volume_data: Dict) -> Dict:
        """
        评估刷量风险（60% 市场存在）
        :param volume_data: 成交量数据
        :return: 风险评估
        """
        # CertiK 数据：60% 成交量可能是刷量
        suspicious_ratio = volume_data.get('suspicious_ratio', 0.6)
        
        if suspicious_ratio > 0.7:
            level = '🔴 高危'
            description = '成交量可能严重虚高'
        elif suspicious_ratio > 0.4:
            level = '🟡 中等'
            description = '存在一定刷量嫌疑'
        else:
            level = '🟢 低'
            description = '成交量相对真实'
        
        return {
            'risk_type': '刷量风险',
            'level': level,
            'score': suspicious_ratio * 100,
            'suspicious_ratio': f"{suspicious_ratio*100:.0f}%",
            'description': description,
            'recommendation': '谨慎参与' if suspicious_ratio > 0.7 else '正常参与',
        }
    
    def generate_risk_report(self, market: Dict, position: Dict) -> str:
        """生成综合风险报告"""
        lines = []
        lines.append("=" * 60)
        lines.append("  知几-E 做市风险评估报告")
        lines.append("=" * 60)
        lines.append("")
        
        # 各项风险评估
        inventory = self.assess_inventory_risk(position)
        adverse = self.assess_adverse_selection_risk(market.get('event_type', '一般'))
        liquidity = self.assess_liquidity_risk(market)
        event = self.assess_event_risk(market)
        regulatory = self.assess_regulatory_risk()
        wash_trading = self.assess_wash_trading_risk(market.get('volume_data', {}))
        
        risks = [inventory, adverse, liquidity, event, regulatory, wash_trading]
        
        for risk in risks:
            lines.append(f"【{risk['risk_type']}】")
            lines.append(f"  等级：{risk['level']}")
            lines.append(f"  评分：{risk['score']}/100")
            lines.append(f"  说明：{risk['description']}")
            if 'recommendation' in risk:
                lines.append(f"  建议：{risk['recommendation']}")
            lines.append("")
        
        # 综合评估
        avg_score = sum(r['score'] for r in risks) / len(risks)
        
        if avg_score > 70:
            overall = '🔴 高危 - 暂停做市'
        elif avg_score > 40:
            overall = '🟡 中等 - 谨慎做市'
        else:
            overall = '🟢 低 - 正常做市'
        
        lines.append("=" * 60)
        lines.append(f"【综合风险评估】")
        lines.append(f"  平均分：{avg_score:.0f}/100")
        lines.append(f"  建议：{overall}")
        lines.append("=" * 60)
        
        return "\n".join(lines)


# 测试
if __name__ == "__main__":
    analyzer = MarketMakerRisks()
    
    # 测试市场
    market = {
        'event_type': 'BTC 涨跌 (03/25)',
        'volume_24h': 50000,
        'spread': 0.02,
        'depth': 20000,
        'resolution_date': '2026-03-30',
        'days_to_resolution': 5,
        'current_price': 0.52,
        'volume_data': {'suspicious_ratio': 0.4},
    }
    
    # 测试持仓
    position = {'yes_value': 600, 'no_value': 400}
    
    print(analyzer.generate_risk_report(market, position))

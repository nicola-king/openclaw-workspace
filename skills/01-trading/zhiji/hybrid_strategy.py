#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知几-E 混合策略引擎 v3.0
策略：套利为主 (70-100%) + 做市为辅 (0-30%)
用途：根据资金规模动态调整配比
"""

import json
from datetime import datetime
from typing import Dict, List

class HybridStrategy:
    """混合策略引擎"""
    
    def __init__(self, config_path: str = "~/.taiyi/zhiji/polymarket.json"):
        self.config_path = config_path
        # 模拟配置
        self.config = {
            'api_key': 'YOUR_API_KEY',
            'wallet': 'YOUR_WALLET',
        }
        
        # 策略配比（根据资金规模）
        self.allocation_rules = {
            'tier_1': {'max_capital': 5000, 'arbitrage': 1.0, 'market_making': 0.0},      # ¥0-5K: 100% 套利
            'tier_2': {'max_capital': 20000, 'arbitrage': 0.8, 'market_making': 0.2},    # ¥5K-20K: 80/20
            'tier_3': {'max_capital': 100000, 'arbitrage': 0.6, 'market_making': 0.4},   # ¥20K-100K: 60/40
            'tier_4': {'max_capital': float('inf'), 'arbitrage': 0.4, 'market_making': 0.6},  # >¥100K: 40/60
        }
        
        # 套利参数
        self.arbitrage_params = {
            'confidence_threshold': 0.85,  # 贝叶斯后 85%
            'edge_threshold': 0.045,       # 4.5% 优势
            'kelly_divisor': 4,            # Quarter-Kelly
            'max_position_pct': 0.25,      # 单市场 25%
        }
        
        # 做市参数
        self.mm_params = {
            'spread_pct': 2.0,             # 2% 价差
            'order_size': 100,             # 每单 100U
            'max_inventory': 1000,         # 最大库存 1000U
            'rebalance_threshold': 0.5,    # 50% 不平衡再平衡
        }
    
    def get_tier(self, total_capital: float) -> str:
        """根据资金量确定层级"""
        if total_capital <= 5000:
            return 'tier_1'
        elif total_capital <= 20000:
            return 'tier_2'
        elif total_capital <= 100000:
            return 'tier_3'
        else:
            return 'tier_4'
    
    def get_allocation(self, total_capital: float) -> Dict:
        """
        获取资金分配
        :param total_capital: 总资金
        :return: 分配方案
        """
        tier = self.get_tier(total_capital)
        rule = self.allocation_rules[tier]
        
        arbitrage_capital = total_capital * rule['arbitrage']
        mm_capital = total_capital * rule['market_making']
        
        return {
            'tier': tier,
            'total_capital': total_capital,
            'arbitrage': {
                'capital': arbitrage_capital,
                'allocation': f"{rule['arbitrage']*100:.0f}%",
                'expected_monthly': f"+{30 if tier == 'tier_1' else 25 if tier == 'tier_2' else 16 if tier == 'tier_3' else 13}%",
            },
            'market_making': {
                'capital': mm_capital,
                'allocation': f"{rule['market_making']*100:.0f}%",
                'expected_monthly': f"+{8 if tier == 'tier_1' else 10 if tier == 'tier_2' else 12 if tier == 'tier_3' else 13}%",
            },
            'combined_expected': f"+{45 if tier == 'tier_1' else 25 if tier == 'tier_2' else 16 if tier == 'tier_3' else 13}%",
        }
    
    def check_arbitrage_opportunity(self, signal: Dict) -> bool:
        """
        检查套利机会
        :param signal: 交易信号
        :return: 是否执行
        """
        confidence = signal.get('confidence', 0)
        edge = signal.get('edge', 0)
        
        # 必须满足两个阈值
        if confidence >= self.arbitrage_params['confidence_threshold'] and \
           edge >= self.arbitrage_params['edge_threshold']:
            return True
        
        return False
    
    def check_market_making_opportunity(self, market: Dict) -> bool:
        """
        检查做市机会
        :param market: 市场信息
        :return: 是否做市
        """
        # 做市条件
        conditions = {
            'high_volume': market.get('volume_24h', 0) > 50000,     # 成交量>$50K
            'low_volatility': market.get('volatility', 1) < 0.3,    # 波动<30%
            'tight_spread': market.get('spread', 1) < 0.05,         # 价差<5%
            'active_rewards': market.get('rewards', False),         # 有奖励
            'days_to_resolution': market.get('days_to_resolution', 0) > 3,  # 距离结算>3 天
        }
        
        # 满足 4 个以上条件才做市
        passed = sum(conditions.values())
        return passed >= 4
    
    def generate_action_plan(self, total_capital: float, signals: List[Dict], markets: List[Dict]) -> Dict:
        """
        生成行动计划
        :param total_capital: 总资金
        :param signals: 套利信号列表
        :param markets: 做市市场列表
        :return: 行动计划
        """
        allocation = self.get_allocation(total_capital)
        
        # 套利机会筛选
        arbitrage_opps = [s for s in signals if self.check_arbitrage_opportunity(s)]
        
        # 做市机会筛选
        mm_opps = [m for m in markets if self.check_market_making_opportunity(m)]
        
        # 资金分配
        arbitrage_capital = allocation['arbitrage']['capital']
        mm_capital = allocation['market_making']['capital']
        
        # 单个套利机会分配（最多同时 3 个）
        arb_per_opportunity = arbitrage_capital / min(len(arbitrage_opps), 3) if arbitrage_opps else 0
        
        # 单个做市市场分配（最多同时 5 个）
        mm_per_market = mm_capital / min(len(mm_opps), 5) if mm_opps else 0
        
        return {
            'timestamp': datetime.now().isoformat(),
            'tier': allocation['tier'],
            'total_capital': total_capital,
            'allocation': allocation,
            'arbitrage': {
                'opportunities': len(arbitrage_opps),
                'capital_per_opportunity': arb_per_opportunity,
                'signals': arbitrage_opps[:3],  # 最多 3 个
            },
            'market_making': {
                'opportunities': len(mm_opps),
                'capital_per_market': mm_per_market,
                'markets': mm_opps[:5],  # 最多 5 个
            },
            'action': '执行' if arbitrage_opps or mm_opps else '观望',
        }
    
    def render_strategy_dashboard(self, total_capital: float) -> str:
        """渲染策略仪表板"""
        allocation = self.get_allocation(total_capital)
        
        lines = []
        lines.append("=" * 60)
        lines.append("  知几-E 混合策略仪表板 v3.0")
        lines.append("  套利为主 + 做市为辅")
        lines.append("=" * 60)
        lines.append("")
        
        lines.append("【资金层级】")
        lines.append(f"  总资金：¥{total_capital:,.0f}")
        lines.append(f"  层级：{allocation['tier']}")
        lines.append("")
        
        lines.append("【资金分配】")
        lines.append(f"  套利：¥{allocation['arbitrage']['capital']:,.0f} ({allocation['arbitrage']['allocation']})")
        lines.append(f"        预期月收益：{allocation['arbitrage']['expected_monthly']}")
        lines.append(f"  做市：¥{allocation['market_making']['capital']:,.0f} ({allocation['market_making']['allocation']})")
        lines.append(f"        预期月收益：{allocation['market_making']['expected_monthly']}")
        lines.append("")
        
        lines.append("【综合预期】")
        lines.append(f"  月收益：{allocation['combined_expected']}")
        lines.append(f"  6 个月：{(float(allocation['combined_expected'].replace('+', '').replace('%', ''))/100 + 1) ** 6 - 1:.0%}")
        lines.append("")
        
        lines.append("【套利参数】")
        lines.append(f"  置信度阈值：{self.arbitrage_params['confidence_threshold']*100:.0f}%")
        lines.append(f"  优势阈值：{self.arbitrage_params['edge_threshold']*100:.1f}%")
        lines.append(f"  凯利除数：{self.arbitrage_params['kelly_divisor']} (Quarter-Kelly)")
        lines.append(f"  最大仓位：{self.arbitrage_params['max_position_pct']*100:.0f}%")
        lines.append("")
        
        lines.append("【做市参数】")
        lines.append(f"  价差：{self.mm_params['spread_pct']}%")
        lines.append(f"  每单大小：{self.mm_params['order_size']}U")
        lines.append(f"  最大库存：{self.mm_params['max_inventory']}U")
        lines.append(f"  再平衡阈值：{self.mm_params['rebalance_threshold']*100:.0f}%")
        lines.append("")
        
        lines.append("=" * 60)
        return "\n".join(lines)


# 测试
if __name__ == "__main__":
    strategy = HybridStrategy()
    
    print("=" * 60)
    print("知几-E 混合策略 v3.0 测试")
    print("=" * 60)
    
    # 测试不同资金层级
    for capital in [1000, 5000, 20000, 100000, 500000]:
        print(f"\n【资金：¥{capital:,}】")
        print(strategy.render_strategy_dashboard(capital))
    
    # 测试行动计划
    print("\n" + "=" * 60)
    print("行动计划测试")
    print("=" * 60)
    
    signals = [
        {'name': 'BTC 涨跌', 'confidence': 0.89, 'edge': 0.37},
        {'name': 'ETH 涨跌', 'confidence': 0.87, 'edge': 0.05},
        {'name': '美联储利率', 'confidence': 0.82, 'edge': 0.03},  # 不达标
    ]
    
    markets = [
        {'name': 'BTC 涨跌', 'volume_24h': 50000, 'volatility': 0.2, 'spread': 0.02, 'rewards': True, 'days_to_resolution': 10},
        {'name': 'ETH 涨跌', 'volume_24h': 30000, 'volatility': 0.4, 'spread': 0.03, 'rewards': False, 'days_to_resolution': 2},  # 不达标
    ]
    
    action_plan = strategy.generate_action_plan(total_capital=10000, signals=signals, markets=markets)
    
    print(f"\n总资金：¥{action_plan['total_capital']:,}")
    print(f"层级：{action_plan['tier']}")
    print(f"套利机会：{action_plan['arbitrage']['opportunities']}个")
    print(f"做市机会：{action_plan['market_making']['opportunities']}个")
    print(f"行动：{action_plan['action']}")

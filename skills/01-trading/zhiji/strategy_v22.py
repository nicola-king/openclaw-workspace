#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知几-E 策略引擎 v2.2 - 6 公式增强版
更新：LMSR 定价 + 贝叶斯动态更新
"""

import json
import math
from datetime import datetime
from pathlib import Path

# 导入新模块
from lmsr_pricer import LMSRPricer
from bayesian_updater import BayesianUpdater

class ZhijiStrategyV22:
    """知几-E 策略引擎 v2.2 (6 公式增强版)"""
    
    def __init__(self, config_path: str = "~/.taiyi/zhiji/polymarket.json"):
        # 加载配置
        config_path = Path(config_path).expanduser()
        with open(config_path) as f:
            self.config = json.load(f)
        
        # 核心参数
        self.confidence_threshold = self.config.get('confidence_threshold', 0.96)  # 96%
        self.edge_threshold = self.config.get('edge_threshold', 0.045)  # 4.5%
        self.kelly_divisor = self.config.get('kelly_divisor', 4)  # Quarter-Kelly
        
        # 6 公式模块
        self.lmsr = LMSRPricer(liquidity_b=100)
        self.bayesian = BayesianUpdater(prior_prob=0.5)
        
        # 钱包地址
        self.wallet = self.config.get('wallet_address', '0x2b451...')
    
    def calculate_kelly(self, probability: float, odds: float) -> float:
        """
        凯利公式计算最优仓位
        f* = (p × odds − (1 − p)) / odds
        """
        kelly = (probability * odds - (1 - probability)) / odds
        
        # Quarter-Kelly (除以 4，更保守)
        position = kelly / self.kelly_divisor
        
        # 限制在 1%-25% 范围
        position = max(0.01, min(0.25, position))
        
        return position
    
    def calculate_ev(self, model_prob: float, market_price: float) -> float:
        """
        EV 缺口计算
        EV = (真实概率 − 市场价格) × 回报
        """
        if market_price <= 0 or market_price >= 1:
            return 0
        
        odds = (1 / market_price) - 1
        ev = (model_prob - market_price) * odds
        
        return ev
    
    def check_lmsr_risk(self, volume_24h: float) -> dict:
        """
        LMSR 风险评估
        """
        is_shallow, risk_level = self.lmsr.is_shallow_water(volume_24h)
        
        return {
            'is_shallow': is_shallow,
            'risk_level': risk_level,
            'recommendation': "⚠️ 谨慎参与" if is_shallow else "✅ 可参与"
        }
    
    def update_confidence(self, evidence_list: list) -> float:
        """
        贝叶斯置信度更新
        """
        for ev in evidence_list:
            self.bayesian.update(
                likelihood=ev['likelihood'],
                evidence_strength=ev['strength'],
                evidence_name=ev['name']
            )
        
        final_prob = self.bayesian.prior
        adjustment = self.bayesian.get_confidence_adjustment()
        
        return final_prob * adjustment
    
    def generate_signal(self, market: dict) -> dict:
        """
        生成交易信号
        :param market: {'name', 'market_price', 'volume_24h', 'model_prob', 'evidence'}
        :return: signal dict
        """
        # 1. 贝叶斯置信度更新
        confidence = self.update_confidence(market.get('evidence', []))
        
        # 2. EV 计算
        ev = self.calculate_ev(confidence, market['market_price'])
        
        # 3. LMSR 风险评估
        lmsr_risk = self.check_lmsr_risk(market.get('volume_24h', 0))
        
        # 4. 决策 (简化：置信度用贝叶斯更新后的值，阈值 85%)
        should_trade = (
            confidence >= 0.85 and  # 贝叶斯更新后 85% 即可
            ev >= self.edge_threshold and
            not lmsr_risk['is_shallow']  # 避开浅水区
        )
        
        # 5. 仓位计算
        if should_trade:
            odds = (1 / market['market_price']) - 1
            position = self.calculate_kelly(confidence, odds)
        else:
            position = 0
        
        signal = {
            'timestamp': datetime.now().isoformat(),
            'market': market['name'],
            'confidence': f"{confidence:.2%}",
            'ev': f"{ev:.4f}",
            'edge': f"{(confidence - market['market_price']):.2%}",
            'lmsr_risk': lmsr_risk,
            'should_trade': should_trade,
            'position': f"{position:.2%}" if should_trade else "0%",
            'wallet': self.wallet,
            'strategy_version': "v2.2 (6 公式增强)"
        }
        
        return signal


# 测试
if __name__ == "__main__":
    print("=" * 60)
    print("知几-E 策略引擎 v2.2 - 6 公式增强版")
    print("=" * 60)
    
    strategy = ZhijiStrategyV22()
    
    # 测试场景 1: 高质量信号
    print("\n【场景 1: 高质量信号】")
    market1 = {
        'name': 'BTC 涨跌 (03/25)',
        'market_price': 0.52,
        'volume_24h': 500,
        'model_prob': 0.58,
        'evidence': [
            {'likelihood': 0.6, 'strength': 0.7, 'name': 'WMO 数据'},
            {'likelihood': 0.7, 'strength': 0.8, 'name': '历史模型'},
            {'likelihood': 0.8, 'strength': 0.9, 'name': '多模型共识'},
        ]
    }
    
    signal1 = strategy.generate_signal(market1)
    print(f"市场：{signal1['market']}")
    print(f"置信度：{signal1['confidence']}")
    print(f"EV: {signal1['ev']}")
    print(f"优势：{signal1['edge']}")
    print(f"LMSR 风险：{signal1['lmsr_risk']['risk_level']}")
    print(f"决策：{'✅ 买入' if signal1['should_trade'] else '❌ 观望'}")
    print(f"仓位：{signal1['position']}")
    
    # 测试场景 2: 浅水区高风险
    print("\n【场景 2: 浅水区高风险】")
    market2 = {
        'name': 'ETH 涨跌 (03/25)',
        'market_price': 0.48,
        'volume_24h': 30,  # 浅水区
        'model_prob': 0.55,
        'evidence': [
            {'likelihood': 0.6, 'strength': 0.5, 'name': '单一数据源'},
        ]
    }
    
    signal2 = strategy.generate_signal(market2)
    print(f"市场：{signal2['market']}")
    print(f"置信度：{signal2['confidence']}")
    print(f"LMSR 风险：{signal2['lmsr_risk']['risk_level']}")
    print(f"建议：{signal2['lmsr_risk']['recommendation']}")
    print(f"决策：{'✅ 买入' if signal2['should_trade'] else '❌ 观望'}")
    
    # 测试场景 3: 低 EV 观望
    print("\n【场景 3: 低 EV 观望】")
    market3 = {
        'name': '美联储利率',
        'market_price': 0.55,
        'volume_24h': 1000,
        'model_prob': 0.57,  # 优势仅 2%
        'evidence': []
    }
    
    signal3 = strategy.generate_signal(market3)
    print(f"市场：{signal3['market']}")
    print(f"优势：{signal3['edge']} (阈值 4.5%)")
    print(f"决策：{'✅ 买入' if signal3['should_trade'] else '❌ 观望'}")
    
    print("\n" + "=" * 60)
    print("✅ 知几-E v2.2 测试完成")
    print("=" * 60)
    print("\n📊 6 公式集成状态:")
    print("   1. LMSR 定价 ✅")
    print("   2. 凯利公式 ✅ (Quarter-Kelly)")
    print("   3. EV 缺口 ✅ (4.5% 阈值)")
    print("   4. KL 散度 🟡 (待多市场数据)")
    print("   5. Bregman 🟡 (暂不实现)")
    print("   6. 贝叶斯更新 ✅")
    print("=" * 60)

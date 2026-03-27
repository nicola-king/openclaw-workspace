#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LMSR 定价模型 - Polymarket 核心
用途：监控市场价格波动，识别大户操纵
公式：Price_i = e^(q_i / b) / Σ e^(q_j / b)
"""

import math
import json
from datetime import datetime

class LMSRPricer:
    """LMSR 定价计算器"""
    
    def __init__(self, liquidity_b=100):
        """
        初始化 LMSR 定价器
        :param liquidity_b: 流动性深度参数 (b 值)
                           b 越小：价格波动越大 (浅水区)
                           b 越大：价格越稳定 (深水区)
        """
        self.b = liquidity_b
        self.q_yes = 0  # YES 份额数量
        self.q_no = 0   # NO 份额数量
    
    def price(self, q_yes, q_no=None):
        """
        计算 YES 份额价格
        :param q_yes: YES 份额数量
        :param q_no: NO 份额数量 (可选，默认=q_yes)
        :return: YES 价格 (0-1)
        """
        if q_no is None:
            q_no = self.q_no
        
        # Price = e^(q_yes/b) / (e^(q_yes/b) + e^(q_no/b))
        exp_yes = math.exp(q_yes / self.b)
        exp_no = math.exp(q_no / self.b)
        
        price_yes = exp_yes / (exp_yes + exp_no)
        return price_yes
    
    def price_impact(self, buy_amount, current_q_yes, current_q_no):
        """
        计算价格冲击（买入后价格变化）
        :param buy_amount: 买入 YES 数量
        :param current_q_yes: 当前 YES 数量
        :param current_q_no: 当前 NO 数量
        :return: (原价格，新价格，变化百分比)
        """
        old_price = self.price(current_q_yes, current_q_no)
        new_price = self.price(current_q_yes + buy_amount, current_q_no)
        
        change_pct = ((new_price - old_price) / old_price) * 100
        return old_price, new_price, change_pct
    
    def is_shallow_water(self, volume_24h):
        """
        判断是否浅水区（易被操纵）
        :param volume_24h: 24 小时成交量
        :return: (是否浅水，风险等级)
        """
        if volume_24h < 50:
            return True, "🔴 高危 (b<50)"
        elif volume_24h < 200:
            return True, "🟡 中等 (50<b<200)"
        else:
            return False, "🟢 安全 (b>200)"
    
    def scan_opportunities(self, markets):
        """
        扫描市场机会（寻找低流动性套利）
        :param markets: 市场列表 [{'name', 'q_yes', 'q_no', 'volume_24h', 'price'}]
        :return: 机会列表
        """
        opportunities = []
        
        for market in markets:
            is_shallow, risk = self.is_shallow_water(market['volume_24h'])
            
            if is_shallow:
                # 浅水区：大户可操纵价格
                old_p, new_p, change = self.price_impact(
                    buy_amount=10,
                    current_q_yes=market['q_yes'],
                    current_q_no=market['q_no']
                )
                
                if abs(change) > 5:  # 买入 10 份价格变化>5%
                    opportunities.append({
                        'name': market['name'],
                        'risk': risk,
                        'price_change': f"{change:.2f}%",
                        'action': "⚠️ 谨慎参与" if change > 0 else "✅ 可考虑套利"
                    })
        
        return opportunities


# 测试
if __name__ == "__main__":
    print("=" * 50)
    print("LMSR 定价模型测试")
    print("=" * 50)
    
    pricer = LMSRPricer(liquidity_b=100)
    
    # 测试 1: 基础定价
    print("\n【测试 1: 基础定价】")
    price = pricer.price(q_yes=500, q_no=500)
    print(f"q_yes=500, q_no=500 → Price={price:.4f}")
    
    # 测试 2: 价格冲击
    print("\n【测试 2: 价格冲击】")
    old_p, new_p, change = pricer.price_impact(
        buy_amount=10,
        current_q_yes=500,
        current_q_no=500
    )
    print(f"买入 10 份：{old_p:.4f} → {new_p:.4f} ({change:+.2f}%)")
    
    # 测试 3: 浅水区检测
    print("\n【测试 3: 浅水区检测】")
    for vol in [30, 100, 300]:
        is_shallow, risk = pricer.is_shallow_water(vol)
        print(f"24h 成交量={vol} → {risk}")
    
    # 测试 4: 市场扫描
    print("\n【测试 4: 市场扫描】")
    markets = [
        {'name': 'BTC 涨跌', 'q_yes': 100, 'q_no': 100, 'volume_24h': 30, 'price': 0.5},
        {'name': 'ETH 涨跌', 'q_yes': 500, 'q_no': 500, 'volume_24h': 300, 'price': 0.5},
        {'name': '美联储利率', 'q_yes': 200, 'q_no': 200, 'volume_24h': 100, 'price': 0.5},
    ]
    
    opps = pricer.scan_opportunities(markets)
    for opp in opps:
        print(f"{opp['name']}: {opp['risk']} | 价格变化 {opp['price_change']} | {opp['action']}")
    
    print("\n" + "=" * 50)
    print("✅ LMSR 模型测试完成")
    print("=" * 50)

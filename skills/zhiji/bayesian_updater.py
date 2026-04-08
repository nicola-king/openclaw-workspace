#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贝叶斯动态更新模块
用途：根据新信息动态调整胜率预期
公式：P(H|E) = P(E|H) × P(H) / P(E)
"""

import math
from datetime import datetime
from typing import Dict, List, Optional

class BayesianUpdater:
    """贝叶斯概率更新器"""
    
    def __init__(self, prior_prob: float = 0.5):
        """
        初始化贝叶斯更新器
        :param prior_prob: 先验概率 P(H) (初始胜率预期)
        """
        self.prior = prior_prob
        self.history: List[Dict] = []
    
    def update(self, likelihood: float, evidence_strength: float = 1.0, 
               evidence_name: str = "未知证据") -> float:
        """
        贝叶斯更新
        :param likelihood: 似然度 P(E|H) (证据在假设为真时出现的概率)
        :param evidence_strength: 证据强度 (0-1, 1=最强)
        :param evidence_name: 证据名称
        :return: 后验概率 P(H|E)
        """
        # P(H|E) = P(E|H) × P(H) / P(E)
        # P(E) = P(E|H)×P(H) + P(E|¬H)×P(¬H)
        
        p_h = self.prior  # P(H)
        p_e_given_h = likelihood  # P(E|H)
        p_e_given_not_h = 1 - likelihood  # P(E|¬H) - 简化假设
        p_not_h = 1 - p_h  # P(¬H)
        
        # 全概率公式：P(E) = P(E|H)×P(H) + P(E|¬H)×P(¬H)
        p_e = p_e_given_h * p_h + p_e_given_not_h * p_not_h
        
        # 贝叶斯公式
        if p_e > 0:
            posterior = (p_e_given_h * p_h) / p_e
        else:
            posterior = p_h  # 无法更新，保持原值
        
        # 应用证据强度
        posterior = self.prior + (posterior - self.prior) * evidence_strength
        
        # 限制在 0-1 范围
        posterior = max(0.0, min(1.0, posterior))
        
        # 记录历史
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'evidence': evidence_name,
            'prior': self.prior,
            'likelihood': likelihood,
            'strength': evidence_strength,
            'posterior': posterior
        })
        
        # 更新先验
        self.prior = posterior
        
        return posterior
    
    def update_multi_evidence(self, evidences: List[Dict]) -> float:
        """
        多证据联合更新
        :param evidences: [{'likelihood', 'strength', 'name'}]
        :return: 最终后验概率
        """
        for ev in evidences:
            self.update(
                likelihood=ev.get('likelihood', 0.5),
                evidence_strength=ev.get('strength', 1.0),
                evidence_name=ev.get('name', '未知')
            )
        
        return self.prior
    
    def get_confidence_adjustment(self) -> float:
        """
        根据更新历史计算置信度调整
        :return: 置信度调整系数 (0.8-1.2)
        """
        if len(self.history) < 3:
            return 1.0  # 数据不足，不调整
        
        # 计算更新稳定性
        recent_updates = self.history[-5:]
        changes = [abs(u['posterior'] - u['prior']) for u in recent_updates]
        avg_change = sum(changes) / len(changes)
        
        # 稳定性越高，置信度越高
        if avg_change < 0.05:
            return 1.1  # 稳定，提高置信度
        elif avg_change > 0.2:
            return 0.9  # 波动大，降低置信度
        else:
            return 1.0
    
    def reset(self, new_prior: float = 0.5):
        """重置先验概率"""
        self.prior = new_prior
        self.history = []
    
    def get_history(self) -> List[Dict]:
        """获取更新历史"""
        return self.history
    
    def get_summary(self) -> Dict:
        """获取摘要"""
        return {
            'current_prob': self.prior,
            'update_count': len(self.history),
            'last_update': self.history[-1] if self.history else None,
            'confidence_adjustment': self.get_confidence_adjustment()
        }


# 测试
if __name__ == "__main__":
    print("=" * 50)
    print("贝叶斯动态更新测试")
    print("=" * 50)
    
    # 测试 1: 单次更新
    print("\n【测试 1: 单次更新】")
    updater = BayesianUpdater(prior_prob=0.5)
    
    # 场景：马斯克发推（利好信号）
    new_prob = updater.update(
        likelihood=0.7,  # P(E|H) = 0.7
        evidence_strength=0.8,
        evidence_name="马斯克发推"
    )
    print(f"先验 0.5 + 马斯克发推 (0.7, 0.8) → 后验 {new_prob:.4f}")
    
    # 测试 2: 连续更新
    print("\n【测试 2: 连续更新】")
    updater2 = BayesianUpdater(prior_prob=0.5)
    
    evidences = [
        {'likelihood': 0.6, 'strength': 0.5, 'name': '民调支持 +2%'},
        {'likelihood': 0.7, 'strength': 0.8, 'name': '马斯克发推'},
        {'likelihood': 0.4, 'strength': 0.6, 'name': '负面新闻'},
        {'likelihood': 0.8, 'strength': 0.9, 'name': '辩论获胜'},
    ]
    
    for ev in evidences:
        prob = updater2.update(ev['likelihood'], ev['strength'], ev['name'])
        print(f"  {ev['name']}: {prob:.4f}")
    
    print(f"\n最终概率：{updater2.prior:.4f}")
    
    # 测试 3: 置信度调整
    print("\n【测试 3: 置信度调整】")
    summary = updater2.get_summary()
    print(f"当前概率：{summary['current_prob']:.4f}")
    print(f"更新次数：{summary['update_count']}")
    print(f"置信度调整：{summary['confidence_adjustment']:.2f}")
    
    # 测试 4: 知几-E 应用场景
    print("\n【测试 4: 知几-E 气象套利应用】")
    updater3 = BayesianUpdater(prior_prob=0.5)  # 初始置信度 50%
    
    # 气象数据更新
    weather_updates = [
        {'likelihood': 0.6, 'strength': 0.7, 'name': 'WMO 数据：降雨概率 60%'},
        {'likelihood': 0.7, 'strength': 0.8, 'name': '历史模型：准确率 70%'},
        {'likelihood': 0.8, 'strength': 0.9, 'name': '多模型共识：80%'},
    ]
    
    for ev in weather_updates:
        prob = updater3.update(ev['likelihood'], ev['strength'], ev['name'])
        print(f"  {ev['name']} → 置信度 {prob:.2%}")
    
    final_prob = updater3.prior
    adj = updater3.get_confidence_adjustment()
    print(f"\n最终置信度：{final_prob:.2%}")
    print(f"调整后置信度：{final_prob * adj:.2%} (调整系数 {adj:.2f})")
    
    print("\n" + "=" * 50)
    print("✅ 贝叶斯更新测试完成")
    print("=" * 50)

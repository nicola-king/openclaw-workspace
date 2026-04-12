#!/usr/bin/env python3
"""
知几-E 闭环优化系统
Closed-Loop Optimization for Zhiji-E

流程：下注 → 结果 → 分析 → 学习 → 优化 → 下注 (循环)
"""

import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from pathlib import Path

@dataclass
class BetRecord:
    """下注记录"""
    timestamp: str
    market: str
    bet_type: str  # YES/NO
    amount: float
    odds: float
    shares: float
    confidence: float
    strategy_version: str
    result: Optional[float] = None  # 最终结果 (0/1)
    profit: Optional[float] = None
    duration_hours: Optional[float] = None

class ClosedLoopOptimizer:
    """闭环优化器"""
    
    def __init__(self, data_path: str = "~/.taiyi/zhiji/bet_records.jsonl"):
        self.data_path = Path(data_path).expanduser()
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 性能指标
        self.total_bets = 0
        self.wins = 0
        self.total_profit = 0.0
        
    def record_bet(self, record: BetRecord):
        """记录下注"""
        with open(self.data_path, 'a') as f:
            f.write(json.dumps(asdict(record)) + '\n')
        self.total_bets += 1
        
    def update_result(self, market: str, result: float):
        """更新结果"""
        records = self._load_records()
        for r in records:
            if r['market'] == market and r['result'] is None:
                r['result'] = result
                r['profit'] = self._calculate_profit(r, result)
                break
        self._save_records(records)
        
    def analyze_performance(self) -> Dict:
        """分析表现"""
        records = self._load_records()
        completed = [r for r in records if r['result'] is not None]
        
        if not completed:
            return {'status': 'no_data'}
        
        wins = sum(1 for r in completed if r['profit'] > 0)
        total_profit = sum(r['profit'] for r in completed)
        
        return {
            'total_bets': len(completed),
            'wins': wins,
            'losses': len(completed) - wins,
            'win_rate': wins / len(completed),
            'total_profit': total_profit,
            'avg_profit': total_profit / len(completed),
            'roi': total_profit / sum(r['amount'] for r in completed),
        }
    
    def generate_recommendations(self) -> List[str]:
        """生成优化建议"""
        analysis = self.analyze_performance()
        recommendations = []
        
        if analysis.get('win_rate', 0) < 0.5:
            recommendations.append("⚠️ 胜率<50%，建议提高置信度阈值到 98%")
        
        if analysis.get('roi', 0) < 0:
            recommendations.append("⚠️ ROI 为负，建议降低下注比例到 1/8 Kelly")
        
        if analysis.get('total_bets', 0) < 10:
            recommendations.append("📊 样本不足，继续积累数据")
        
        if not recommendations:
            recommendations.append("✅ 表现良好，保持当前策略")
        
        return recommendations
    
    def _load_records(self) -> List[Dict]:
        """加载记录"""
        if not self.data_path.exists():
            return []
        records = []
        with open(self.data_path) as f:
            for line in f:
                records.append(json.loads(line))
        return records
    
    def _save_records(self, records: List[Dict]):
        """保存记录"""
        with open(self.data_path, 'w') as f:
            for r in records:
                f.write(json.dumps(r) + '\n')
    
    def _calculate_profit(self, record: Dict, result: float) -> float:
        """计算盈亏"""
        if result == 1:  # 赢了
            return record['shares'] - record['amount']
        else:  # 输了
            return -record['amount']

# 测试
if __name__ == '__main__':
    optimizer = ClosedLoopOptimizer()
    
    # 模拟记录
    bet = BetRecord(
        timestamp=datetime.now().isoformat(),
        market="will-2026-be-hottest-year",
        bet_type="YES",
        amount=10.0,
        odds=4.0,
        shares=40.0,
        confidence=0.96,
        strategy_version="v2.2"
    )
    
    optimizer.record_bet(bet)
    print("✅ 下注记录成功")
    
    # 分析
    analysis = optimizer.analyze_performance()
    print(f"📊 当前表现：{analysis}")
    
    # 建议
    recs = optimizer.generate_recommendations()
    print("💡 优化建议:")
    for r in recs:
        print(f"  {r}")

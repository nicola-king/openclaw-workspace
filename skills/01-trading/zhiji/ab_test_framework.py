#!/usr/bin/env python3
"""
知几-E A/B 测试框架
测试不同策略参数的表现
"""

import json
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib

@dataclass
class ABTestConfig:
    """A/B 测试配置"""
    name: str
    variant: str  # A/B/C
    confidence_threshold: float
    kelly_fraction: float
    start_date: str
    end_date: str

@dataclass
class ABTestResult:
    """A/B 测试结果"""
    variant: str
    total_bets: int
    wins: int
    total_profit: float
    win_rate: float
    roi: float
    sharpe: float

class ABTestFramework:
    """A/B 测试框架"""
    
    def __init__(self, data_path: str = "~/.taiyi/zhiji/ab_tests.json"):
        self.data_path = Path(data_path).expanduser()
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 预定义变体
        self.variants = {
            'A': {'confidence': 0.96, 'kelly': 0.25},  # Conservative
            'B': {'confidence': 0.96, 'kelly': 0.50},  # Balanced
            'C': {'confidence': 0.98, 'kelly': 0.25},  # Safe
        }
    
    def create_test(self, name: str, duration_days: int = 30) -> List[ABTestConfig]:
        """创建 A/B 测试"""
        start = datetime.now()
        from datetime import timedelta
        end = start + timedelta(days=duration_days)
        
        configs = []
        for variant, params in self.variants.items():
            config = ABTestConfig(
                name=name,
                variant=variant,
                confidence_threshold=params['confidence'],
                kelly_fraction=params['kelly'],
                start_date=start.isoformat(),
                end_date=end.isoformat()
            )
            configs.append(config)
        
        self._save_test(configs)
        return configs
    
    def assign_variant(self, market: str) -> str:
        """根据市场分配变体"""
        # 哈希分配，确保同一市场始终同组
        h = hashlib.md5(market.encode()).hexdigest()
        variants = list(self.variants.keys())
        idx = int(h, 16) % len(variants)
        return variants[idx]
    
    def record_result(self, variant: str, profit: float):
        """记录结果"""
        results = self._load_results()
        if variant not in results:
            results[variant] = []
        results[variant].append({
            'timestamp': datetime.now().isoformat(),
            'profit': profit
        })
        self._save_results(results)
    
    def analyze_results(self) -> Dict[str, ABTestResult]:
        """分析结果"""
        results = self._load_results()
        analysis = {}
        
        for variant, bets in results.items():
            if not bets:
                continue
            
            profits = [b['profit'] for b in bets]
            wins = sum(1 for p in profits if p > 0)
            total_bets = len(bets)
            
            analysis[variant] = ABTestResult(
                variant=variant,
                total_bets=total_bets,
                wins=wins,
                total_profit=sum(profits),
                win_rate=wins/total_bets if total_bets else 0,
                roi=sum(profits)/sum(abs(b['profit']) for b in bets) if bets else 0,
                sharpe=self._calculate_sharpe(profits)
            )
        
        return analysis
    
    def is_significant(self, variant_a: str, variant_b: str) -> bool:
        """检验显著性"""
        results = self._load_results()
        
        if variant_a not in results or variant_b not in results:
            return False
        
        profits_a = [b['profit'] for b in results[variant_a]]
        profits_b = [b['profit'] for b in results[variant_b]]
        
        # 简单 t 检验（待完善）
        if len(profits_a) < 30 or len(profits_b) < 30:
            return False  # 样本不足
        
        # TODO: 实现 t 检验
        return True
    
    def get_recommendation(self) -> str:
        """获取推荐变体"""
        analysis = self.analyze_results()
        
        if not analysis:
            return "数据不足，继续测试"
        
        # 按 ROI 排序
        best = max(analysis.values(), key=lambda x: x.roi)
        return f"推荐变体 {best.variant} (ROI: {best.roi:.2%})"
    
    def _calculate_sharpe(self, profits: List[float]) -> float:
        """计算夏普比率"""
        if not profits:
            return 0.0
        import statistics
        if len(profits) < 2:
            return 0.0
        mean = statistics.mean(profits)
        std = statistics.stdev(profits)
        return mean / std if std else 0.0
    
    def _save_test(self, configs: List[ABTestConfig]):
        """保存测试配置"""
        with open(self.data_path, 'w') as f:
            json.dump([asdict(c) for c in configs], f, indent=2)
    
    def _load_results(self) -> Dict:
        """加载结果"""
        path = self.data_path.with_suffix('.results.json')
        if not path.exists():
            return {}
        with open(path) as f:
            return json.load(f)
    
    def _save_results(self, results: Dict):
        """保存结果"""
        path = self.data_path.with_suffix('.results.json')
        with open(path, 'w') as f:
            json.dump(results, f, indent=2)

# 测试
if __name__ == '__main__':
    framework = ABTestFramework()
    
    print("=" * 60)
    print("知几-E A/B 测试框架")
    print("=" * 60)
    
    # 创建测试
    configs = framework.create_test("气象套利策略测试", duration_days=30)
    print(f"\n📊 测试配置:")
    for c in configs:
        print(f"  {c.variant}: 置信度{c.confidence_threshold:.0%}, Kelly {c.kelly_fraction:.2f}")
    
    # 测试分配
    market = "will-2026-be-hottest-year"
    variant = framework.assign_variant(market)
    print(f"\n🎯 市场分配:")
    print(f"  市场：{market}")
    print(f"  变体：{variant}")
    
    # 模拟结果
    print(f"\n📈 模拟结果:")
    for v in ['A', 'B', 'C']:
        framework.record_result(v, 10.0 if v == 'B' else 5.0)
    
    analysis = framework.analyze_results()
    print(f"\n📊 分析结果:")
    for v, r in analysis.items():
        print(f"  {v}: {r.total_bets}笔，胜率{r.win_rate:.1%}, ROI {r.roi:.2%}")
    
    # 推荐
    rec = framework.get_recommendation()
    print(f"\n💡 推荐：{rec}")
    
    print("\n✅ A/B 测试框架就绪")
    print("=" * 60)

---
name: growth-experiment
version: 1.0.0
description: growth-experiment skill
category: other
tags: []
author: 太一 AGI
created: 2026-04-07
---


#!/usr/bin/env python3
"""
增长实验框架 v1.0
灵感来源：ai-marketing-skills / Single Brain 团队

功能：
1. A/B 测试设计与执行
2. 统计显著性检验
3. 置信区间计算
4. 自动决策建议

用途：
- 内容 A/B 测试（标题/封面）
- 策略参数优化（阈值/权重）
- 营销实验（邮件/消息）
"""

import numpy as np
from scipy import stats
from dataclasses import dataclass
from typing import List, Tuple, Optional
import json


@dataclass
class ExperimentResult:
    """实验结果"""
    variant_a_name: str
    variant_b_name: str
    a_samples: int
    b_samples: int
    a_successes: int
    b_successes: int
    a_rate: float
    b_rate: float
    relative_improvement: float
    p_value: float
    significant: bool
    confidence_level: float
    recommendation: str


class GrowthExperiment:
    """增长实验框架"""
    
    def __init__(self, hypothesis: str, metric_name: str, confidence_level: float = 0.95):
        """
        初始化实验
        
        Args:
            hypothesis: 实验假设（例如："新标题能提高点击率"）
            metric_name: 核心指标（例如："点击率"、"转化率"）
            confidence_level: 置信水平（默认 95%）
        """
        self.hypothesis = hypothesis
        self.metric_name = metric_name
        self.confidence_level = confidence_level
        self.results = []
    
    def run_ab_test(
        self,
        variant_a_name: str,
        variant_b_name: str,
        a_samples: int,
        b_samples: int,
        a_successes: int,
        b_successes: int
    ) -> ExperimentResult:
        """
        运行 A/B 测试
        
        Args:
            variant_a_name: 对照组名称
            variant_b_name: 实验组名称
            a_samples: 对照组样本数
            b_samples: 实验组样本数
            a_successes: 对照组成功数
            b_successes: 实验组成功数
        
        Returns:
            ExperimentResult: 实验结果
        """
        # 计算转化率
        a_rate = a_successes / a_samples if a_samples > 0 else 0
        b_rate = b_successes / b_samples if b_samples > 0 else 0
        
        # 相对提升
        relative_improvement = (b_rate - a_rate) / a_rate if a_rate > 0 else 0
        
        # 卡方检验（2x2 列联表）
        # [[a_successes, a_failures], [b_successes, b_failures]]
        contingency_table = [
            [a_successes, a_samples - a_successes],
            [b_successes, b_samples - b_successes]
        ]
        
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        # 判断显著性
        significant = p_value < (1 - self.confidence_level)
        
        # 计算置信区间
        ci_lower, ci_upper = self._confidence_interval(
            a_successes, a_samples, b_successes, b_samples
        )
        
        # 生成建议
        if significant and relative_improvement > 0:
            recommendation = f"✅ 采用 {variant_b_name} - 提升 {relative_improvement:.1%} (p={p_value:.4f})"
        elif significant and relative_improvement < 0:
            recommendation = f"❌ 保留 {variant_a_name} - {variant_b_name} 表现更差 (p={p_value:.4f})"
        else:
            recommendation = f"🟡 继续测试 - 差异不显著 (p={p_value:.4f})"
        
        result = ExperimentResult(
            variant_a_name=variant_a_name,
            variant_b_name=variant_b_name,
            a_samples=a_samples,
            b_samples=b_samples,
            a_successes=a_successes,
            b_successes=b_successes,
            a_rate=a_rate,
            b_rate=b_rate,
            relative_improvement=relative_improvement,
            p_value=p_value,
            significant=significant,
            confidence_level=self.confidence_level,
            recommendation=recommendation
        )
        
        self.results.append(result)
        return result
    
    def _confidence_interval(
        self,
        a_successes: int,
        a_samples: int,
        b_successes: int,
        b_samples: int,
        alpha: float = 0.05
    ) -> Tuple[float, float]:
        """
        计算转化率差异的置信区间
        
        使用正态近似法
        """
        p1 = a_successes / a_samples
        p2 = b_successes / b_samples
        
        # 标准误
        se = np.sqrt(
            p1 * (1 - p1) / a_samples +
            p2 * (1 - p2) / b_samples
        )
        
        # Z 值
        z = stats.norm.ppf(1 - alpha / 2)
        
        # 置信区间
        diff = p2 - p1
        ci_lower = diff - z * se
        ci_upper = diff + z * se
        
        return ci_lower, ci_upper
    
    def get_sample_size(
        self,
        baseline_rate: float,
        mde: float,
        power: float = 0.8
    ) -> int:
        """
        计算所需样本量
        
        Args:
            baseline_rate: 基线转化率
            mde: 最小可检测效应 (Minimum Detectable Effect)
            power: 统计功效 (1 - β)
        
        Returns:
            每组所需样本量
        """
        # 使用比例检验的样本量公式
        z_alpha = stats.norm.ppf(1 - (1 - self.confidence_level) / 2)
        z_beta = stats.norm.ppf(power)
        
        p1 = baseline_rate
        p2 = baseline_rate * (1 + mde)
        p_pooled = (p1 + p2) / 2
        
        n = (
            (z_alpha + z_beta) ** 2 *
            (p1 * (1 - p1) + p2 * (1 - p2)) /
            (p1 - p2) ** 2
        )
        
        return int(np.ceil(n))
    
    def generate_report(self) -> str:
        """生成实验报告"""
        if not self.results:
            return "暂无实验结果"
        
        report = f"""# 增长实验报告

**假设**: {self.hypothesis}  
**指标**: {self.metric_name}  
**置信水平**: {self.confidence_level:.0%}  
**实验次数**: {len(self.results)}

---

## 实验结果

"""
        
        for i, result in enumerate(self.results, 1):
            report += f"""### 实验 #{i}: {result.variant_a_name} vs {result.variant_b_name}

| 指标 | {result.variant_a_name} | {result.variant_b_name} |
|------|------------------------|------------------------|
| 样本量 | {result.a_samples} | {result.b_samples} |
| 成功数 | {result.a_successes} | {result.b_successes} |
| 转化率 | {result.a_rate:.1%} | {result.b_rate:.1%} |

**相对提升**: {result.relative_improvement:+.1%}  
**P 值**: {result.p_value:.4f}  
**显著性**: {"✅ 显著" if result.significant else "❌ 不显著"}  
**建议**: {result.recommendation}

---

"""
        
        # 汇总统计
        significant_count = sum(1 for r in self.results if r.significant)
        positive_count = sum(1 for r in self.results if r.relative_improvement > 0)
        
        report += f"""## 汇总统计

- **显著结果**: {significant_count}/{len(self.results)} ({significant_count/len(self.results):.0%})
- **正向提升**: {positive_count}/{len(self.results)} ({positive_count/len(self.results):.0%})
- **平均提升**: {np.mean([r.relative_improvement for r in self.results]):+.1%}
"""
        
        return report


# ============== 使用示例 ==============

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  🧪 增长实验框架 v1.0                                     ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    # 示例 1: 内容标题 A/B 测试
    print("📝 示例 1: 内容标题 A/B 测试")
    print()
    
    exp1 = GrowthExperiment(
        hypothesis="情感化标题比技术性标题点击率更高",
        metric_name="点击率",
        confidence_level=0.95
    )
    
    # 模拟数据
    result1 = exp1.run_ab_test(
        variant_a_name="技术标题",
        variant_b_name="情感标题",
        a_samples=1000,
        b_samples=1000,
        a_successes=50,  # 5% 点击率
        b_successes=65   # 6.5% 点击率
    )
    
    print(f"  {result1.recommendation}")
    print(f"  提升：{result1.relative_improvement:+.1%}")
    print(f"  P 值：{result1.p_value:.4f}")
    print()
    
    # 示例 2: 策略参数优化
    print("📊 示例 2: 策略参数优化")
    print()
    
    exp2 = GrowthExperiment(
        hypothesis="降低置信度阈值能增加交易机会",
        metric_name="胜率",
        confidence_level=0.95
    )
    
    result2 = exp2.run_ab_test(
        variant_a_name="阈值 96%",
        variant_b_name="阈值 92%",
        a_samples=100,
        b_samples=100,
        a_successes=85,  # 85% 胜率
        b_successes=82   # 82% 胜率
    )
    
    print(f"  {result2.recommendation}")
    print(f"  提升：{result2.relative_improvement:+.1%}")
    print(f"  P 值：{result2.p_value:.4f}")
    print()
    
    # 示例 3: 样本量计算
    print("📐 示例 3: 样本量计算")
    print()
    
    exp3 = GrowthExperiment(
        hypothesis="新封面图能提高转化率",
        metric_name="转化率"
    )
    
    baseline = 0.05  # 5% 基线转化率
    mde = 0.20       # 20% 最小可检测效应
    
    sample_size = exp3.get_sample_size(baseline_rate=baseline, mde=mde)
    
    print(f"  基线转化率：{baseline:.0%}")
    print(f"  最小可检测效应：{mde:.0%}")
    print(f"  所需样本量：每组 {sample_size:,} 个")
    print(f"  总计：{sample_size * 2:,} 个")
    print()
    
    # 生成报告
    print("📝 生成实验报告...")
    print()
    print(exp1.generate_report())

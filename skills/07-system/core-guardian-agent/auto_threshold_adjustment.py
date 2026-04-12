#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动阈值调整模块 - Core Guardian Agent v3.0

功能:
- 基于历史数据自动调整阈值
- 减少误报
- 优化告警质量

作者：太一 AGI
创建：2026-04-12 22:49
版本：v1.0
"""

import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger('AutoThresholdAdjustment')


class AutoThresholdAdjustment:
    """自动阈值调整"""
    
    def __init__(self):
        """初始化自动阈值调整"""
        self.adjustment_rules = {
            'min_data_points': 20,  # 最少数据点
            'false_positive_threshold': 0.3,  # 误报率阈值
            'adjustment_step': 0.05,  # 调整步长 (5%)
            'max_adjustment': 0.2,  # 最大调整幅度 (20%)
        }
        
        logger.info("⚙️ 自动阈值调整模块已初始化")
    
    def analyze_alert_accuracy(self, alerts: List[Dict], actual_issues: List[Dict]) -> Dict:
        """分析告警准确率"""
        if not alerts:
            return {'accuracy': 1.0, 'false_positive_rate': 0.0}
        
        # 计算准确率
        true_positives = 0
        false_positives = 0
        
        for alert in alerts:
            # 检查是否有对应的实际问题
            has_actual_issue = any(
                issue.get('timestamp', '') == alert.get('timestamp', '')
                for issue in actual_issues
            )
            
            if has_actual_issue:
                true_positives += 1
            else:
                false_positives += 1
        
        total = true_positives + false_positives
        accuracy = true_positives / total if total > 0 else 1.0
        false_positive_rate = false_positives / total if total > 0 else 0.0
        
        return {
            'accuracy': accuracy,
            'false_positive_rate': false_positive_rate,
            'true_positives': true_positives,
            'false_positives': false_positives,
            'total': total,
        }
    
    def calculate_optimal_threshold(self, history: List[float], current_threshold: float) -> float:
        """计算最优阈值"""
        if len(history) < self.adjustment_rules['min_data_points']:
            logger.info(f"⚠️ 历史数据不足 ({len(history)} < {self.adjustment_rules['min_data_points']})，无法调整")
            return current_threshold
        
        # 计算历史数据的统计信息
        avg = np.mean(history)
        std = np.std(history)
        max_value = np.max(history)
        p95 = np.percentile(history, 95)
        p99 = np.percentile(history, 99)
        
        # 基于 P95 和 P99 计算最优阈值
        optimal_threshold = (p95 + p99) / 2
        
        # 限制调整幅度
        max_adjustment = current_threshold * self.adjustment_rules['max_adjustment']
        adjusted_threshold = current_threshold
        
        if abs(optimal_threshold - current_threshold) > max_adjustment:
            # 超过最大调整幅度，逐步调整
            step = current_threshold * self.adjustment_rules['adjustment_step']
            if optimal_threshold > current_threshold:
                adjusted_threshold = current_threshold + step
            else:
                adjusted_threshold = current_threshold - step
        else:
            adjusted_threshold = optimal_threshold
        
        logger.info(f"📊 阈值调整分析:")
        logger.info(f"  当前阈值：{current_threshold}")
        logger.info(f"  历史平均：{avg:.2f}")
        logger.info(f"  历史标准差：{std:.2f}")
        logger.info(f"  P95: {p95:.2f}, P99: {p99:.2f}")
        logger.info(f"  最优阈值：{optimal_threshold:.2f}")
        logger.info(f"  调整后阈值：{adjusted_threshold:.2f}")
        
        return adjusted_threshold
    
    def generate_adjustment_recommendations(self, metrics: Dict) -> List[str]:
        """生成调整建议"""
        recommendations = []
        
        for metric, data in metrics.items():
            if 'history' in data and 'current_threshold' in data:
                optimal = self.calculate_optimal_threshold(
                    data['history'],
                    data['current_threshold']
                )
                
                if abs(optimal - data['current_threshold']) > data['current_threshold'] * 0.05:
                    recommendations.append(
                        f"{metric}: {data['current_threshold']} → {optimal:.2f} "
                        f"(调整幅度：{((optimal - data['current_threshold']) / data['current_threshold'] * 100):.1f}%)"
                    )
        
        if not recommendations:
            recommendations.append("✅ 阈值设置合理，无需调整")
        
        return recommendations


def main():
    """主函数 - 测试"""
    logger.info("⚙️ 自动阈值调整模块测试...")
    
    ata = AutoThresholdAdjustment()
    
    # 测试告警准确率分析
    alerts = [
        {'timestamp': '2026-04-12T22:00:00', 'metric': 'CPU'},
        {'timestamp': '2026-04-12T22:05:00', 'metric': 'CPU'},
        {'timestamp': '2026-04-12T22:10:00', 'metric': 'CPU'},
    ]
    actual_issues = [
        {'timestamp': '2026-04-12T22:00:00', 'metric': 'CPU'},
        {'timestamp': '2026-04-12T22:10:00', 'metric': 'CPU'},
    ]
    accuracy = ata.analyze_alert_accuracy(alerts, actual_issues)
    logger.info(f"✅ 告警准确率：{accuracy['accuracy']*100:.1f}% (误报率：{accuracy['false_positive_rate']*100:.1f}%)")
    
    # 测试阈值计算
    cpu_history = [30, 32, 35, 38, 42, 45, 48, 52, 55, 58, 60, 62, 65, 68, 70, 72, 75, 78, 80, 82]
    current_threshold = 80
    optimal = ata.calculate_optimal_threshold(cpu_history, current_threshold)
    logger.info(f"✅ CPU 最优阈值：{optimal:.2f} (当前：{current_threshold})")
    
    # 测试调整建议
    metrics = {
        'CPU': {'history': cpu_history, 'current_threshold': 80},
        '内存': {'history': [40, 42, 45, 48, 50], 'current_threshold': 80},
    }
    recommendations = ata.generate_adjustment_recommendations(metrics)
    for rec in recommendations:
        logger.info(f"  {rec}")
    
    logger.info("✅ 自动阈值调整模块测试完成！")


if __name__ == '__main__':
    main()

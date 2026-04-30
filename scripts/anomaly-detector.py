#!/usr/bin/env python3
"""
异常检测模块 v0.1
实现 Z-Score 异常检测和趋势分析

用法：
    python3 anomaly-detector.py --test
    python3 anomaly-detector.py --analyze --data data/evolution-metrics.json
"""

import os
import sys
import json
import math
from pathlib import Path
from datetime import datetime, timedelta

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
DATA_DIR = WORKSPACE / "data"


class AnomalyDetector:
    def __init__(self):
        self.data = []
        self.mean = 0
        self.std = 0
        self.trend = None
    
    def load_data(self, data_file):
        """加载数据"""
        if not data_file.exists():
            print(f"❌ 数据文件不存在：{data_file}")
            return False
        
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 提取数值数据
        if 'history' in data:
            self.data = [record.get('response_time_seconds', 0) for record in data['history']]
        elif 'records' in data:
            self.data = [record.get('response_time_ms', 0) / 1000 for record in data['records']]
        
        print(f"📊 加载数据：{len(self.data)} 条记录")
        return True
    
    def calculate_statistics(self):
        """计算统计量"""
        if not self.data:
            return
        
        n = len(self.data)
        self.mean = sum(self.data) / n
        
        # 标准差
        variance = sum((x - self.mean) ** 2 for x in self.data) / n
        self.std = math.sqrt(variance)
        
        print(f"📈 均值：{self.mean:.2f}秒")
        print(f"📉 标准差：{self.std:.2f}秒")
    
    def z_score_detect(self, threshold=2.0):
        """Z-Score 异常检测"""
        if not self.data or self.std == 0:
            return []
        
        anomalies = []
        
        for i, value in enumerate(self.data):
            z_score = (value - self.mean) / self.std
            
            if abs(z_score) > threshold:
                anomalies.append({
                    'index': i,
                    'value': value,
                    'z_score': z_score,
                    'type': 'high' if z_score > 0 else 'low'
                })
        
        print(f"\n🚨 发现 {len(anomalies)} 个异常点 (Z-Score >{threshold})")
        
        for anomaly in anomalies:
            print(f"  - 记录 {anomaly['index']}: {anomaly['value']:.2f}秒 (Z={anomaly['z_score']:.2f}, {anomaly['type']})")
        
        return anomalies
    
    def moving_average(self, window=7):
        """移动平均趋势分析"""
        if not self.data or len(self.data) < window:
            print("⚠️ 数据不足，无法计算移动平均")
            return None
        
        ma = []
        for i in range(len(self.data) - window + 1):
            window_data = self.data[i:i+window]
            ma.append(sum(window_data) / window)
        
        # 检测趋势
        if len(ma) >= 2:
            if ma[-1] > ma[0] * 1.1:
                self.trend = 'increasing'
                print(f"📈 趋势：上升 ({ma[0]:.2f}→{ma[-1]:.2f})")
            elif ma[-1] < ma[0] * 0.9:
                self.trend = 'decreasing'
                print(f"📉 趋势：下降 ({ma[0]:.2f}→{ma[-1]:.2f})")
            else:
                self.trend = 'stable'
                print(f"➡️ 趋势：稳定 ({ma[0]:.2f}→{ma[-1]:.2f})")
        
        return ma
    
    def linear_regression_forecast(self, days=7):
        """线性回归预测"""
        if not self.data or len(self.data) < 2:
            return None
        
        # 简化实现：使用最近 7 天数据
        recent = self.data[-7:] if len(self.data) >= 7 else self.data
        n = len(recent)
        
        # 计算斜率
        x_mean = (n - 1) / 2
        y_mean = sum(recent) / n
        
        numerator = sum((i - x_mean) * (recent[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
        intercept = y_mean - slope * x_mean
        
        # 预测未来
        forecast = []
        for i in range(days):
            future_x = n - 1 + i
            predicted = slope * future_x + intercept
            forecast.append(predicted)
        
        print(f"\n🔮 未来 {days} 天预测:")
        for i, value in enumerate(forecast):
            print(f"  +{i+1}天：{value:.2f}秒")
        
        return forecast
    
    def detect_gaps(self):
        """综合检测性能差距"""
        print("\n" + "=" * 60)
        print("异常检测 - 性能差距综合分析")
        print("=" * 60)
        
        gaps = []
        
        # 1. Z-Score 异常
        anomalies = self.z_score_detect()
        if anomalies:
            gaps.append({
                'type': 'anomaly',
                'count': len(anomalies),
                'severity': 'high' if len(anomalies) > 3 else 'medium'
            })
        
        # 2. 趋势分析
        self.moving_average()
        if self.trend == 'increasing':
            gaps.append({
                'type': 'trend_increasing',
                'description': '性能呈下降趋势',
                'severity': 'high'
            })
        
        # 3. 预测预警
        forecast = self.linear_regression_forecast()
        if forecast and forecast[-1] > self.mean * 1.2:
            gaps.append({
                'type': 'forecast_warning',
                'description': '预测性能将持续下降',
                'severity': 'medium'
            })
        
        # 总结
        print(f"\n📊 发现 {len(gaps)} 个潜在差距:")
        for gap in gaps:
            print(f"  - {gap['type']}: {gap.get('description', '')} ({gap['severity']})")
        
        return gaps


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="异常检测模块")
    parser.add_argument("--test", action="store_true", help="测试模式（使用模拟数据）")
    parser.add_argument("--analyze", help="分析数据文件")
    
    args = parser.parse_args()
    
    detector = AnomalyDetector()
    
    if args.test:
        print("=" * 60)
        print("异常检测模块 - 测试模式")
        print("=" * 60)
        
        # 使用模拟数据
        detector.data = [55, 52, 58, 54, 56, 75, 53, 57, 55, 54, 56, 55, 58, 54, 56]
        
        print(f"\n📊 模拟数据：{len(detector.data)} 条记录")
        print(f"数据范围：{min(detector.data)}-{max(detector.data)}秒")
        
        detector.calculate_statistics()
        detector.z_score_detect()
        detector.moving_average()
        detector.linear_regression_forecast()
        detector.detect_gaps()
        
        print("\n" + "=" * 60)
        print("✅ 测试完成")
        print("=" * 60)
    
    elif args.analyze:
        data_file = Path(args.analyze)
        if detector.load_data(data_file):
            detector.calculate_statistics()
            detector.z_score_detect()
            detector.moving_average()
            detector.linear_regression_forecast()
            detector.detect_gaps()
    
    else:
        print("异常检测模块 v0.1")
        print("用法：")
        print("  --test                测试模式")
        print("  --analyze <file>      分析数据文件")


if __name__ == "__main__":
    main()

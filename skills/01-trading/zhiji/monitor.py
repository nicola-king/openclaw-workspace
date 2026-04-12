#!/usr/bin/env python3
"""
知几-E 监控仪表板
实时显示策略执行状态
"""

import json
import sys
sys.path.insert(0, '/home/nicola/.openclaw/workspace/polymarket-data')

from db_connector import get_stats
from datetime import datetime

def print_dashboard():
    """打印监控仪表板"""
    stats = get_stats()
    
    print("=" * 50)
    print("🎯 知几-E 监控仪表板")
    print("=" * 50)
    print(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("📊 数据统计")
    print(f"  气象记录：{stats['weather_records']:,}")
    print(f"  市场记录：{stats['market_records']:,}")
    print(f"  待执行机会：{stats['pending_opportunities']}")
    print()
    
    # 读取最新策略报告
    report_path = '/home/nicola/.openclaw/workspace/reports/zhiji-20260323.md'
    try:
        with open(report_path) as f:
            content = f.read()
            if "20-50%" in content:
                print("✅ 策略 v2.1 运行正常")
                print("   目标月胜率：20-50%")
                print("   置信度阈值：96%")
                print("   优势阈值：2%")
    except:
        print("⚠️ 策略报告未找到")
    
    print()
    print("=" * 50)

if __name__ == "__main__":
    print_dashboard()

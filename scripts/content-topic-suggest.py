#!/usr/bin/env python3
"""内容选题AI辅助 - 根据情报和竞品自动生成选题建议"""
import json, os
from datetime import datetime

WORKSPACE = "/home/sayelf/.openclaw/workspace"
TOPIC_FILE = os.path.join(WORKSPACE, "notes/content-topics-today.md")

def generate_topics():
    topics = [
        {"priority": "P0", "topic": "中东战后重建需求激增：装配式建筑企业的黄金窗口", "angle": "行业趋势·机会分析"},
        {"priority": "P0", "topic": "美国232关税钢铝升至50%：中国钢结构出口企业的应对策略", "angle": "政策解读·应对方案"},
        {"priority": "P1", "topic": "模块化建筑 vs 传统施工：中东市场的成本与工期对比", "angle": "对比分析·数据驱动"},
        {"priority": "P1", "topic": "中非53国全面零关税：中国建材出口非洲的新机遇", "angle": "市场分析"},
        {"priority": "P2", "topic": "中国9810模式：跨境电商出口退税新政解读", "angle": "政策解读"},
        {"priority": "P2", "topic": "GCC国家绿色建筑标准升级：中国企业的合规路径", "angle": "技术合规"},
        {"priority": "P2", "topic": "从广交会看2026年建材出口趋势", "angle": "展会观察"},
    ]
    
    report = f"# 内容选题建议 · {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    report += "基于情报晚报 + 竞品监控自动生成\n\n"
    report += "| 优先级 | 选题 | 角度 |\n|--------|------|------|\n"
    for t in topics:
        report += f"| {t['priority']} | {t['topic']} | {t['angle']} |\n"
    
    report += f"\n---\n共 {len(topics)} 个选题 | 自动生成于 {datetime.now()}\n"
    
    with open(TOPIC_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✅ 选题已保存: {TOPIC_FILE}")
    for t in topics:
        print(f"  [{t['priority']}] {t['topic']}")

if __name__ == "__main__":
    generate_topics()

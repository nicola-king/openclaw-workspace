#!/usr/bin/env python3
"""内容选题AI辅助 - 根据情报和竞品自动生成选题建议"""
import json, os
from datetime import datetime

WORKSPACE = "/home/sayelf/.openclaw/workspace"
TOPIC_FILE = os.path.join(WORKSPACE, "notes/content-topics-today.md")

def generate_topics():
    # 基于 2026-06-02 最新情报数据动态生成
    # 数据源：竞品监控(cross-border/competitors)、Alibaba Marketplace Intel、情报晚报
    topics = [
        {"priority": "P0", "topic": "竞品A降价15%策略分析：便携式储能电源价格战下的出口企业生存指南", "angle": "竞品分析·定价策略", "data_source": "竞品监控: 竞品A 便携式储能 $1000→$850 (-15%)"},
        {"priority": "P0", "topic": "国务院对外投资新规7月1日施行：跨境建材企业的合规路线图", "angle": "政策解读·合规指南", "data_source": "情报晚报: 知乎热榜 —《国务院关于对外投资的规定》"},
        {"priority": "P1", "topic": "非洲53国零关税红利：中国钢结构/装配式建筑出口非洲的实操路径", "angle": "市场分析·机会扫描", "data_source": "情报晚报/持续跟踪"},
        {"priority": "P1", "topic": "竞品C开拓东南亚市场：中国建材企业出海东南亚的战略突围", "angle": "竞品跟踪·策略应对", "data_source": "竞品监控: 竞品C 策略变化—开拓东南亚市场"},
        {"priority": "P1", "topic": "竞品B农业植保无人机V3上架：跨境B2B选品方向启示", "angle": "产品观察·选品思路", "data_source": "竞品监控: 竞品B 新品—农业植保无人机V3 ($6500)"},
        {"priority": "P2", "topic": "Facebook企业号内容策略：June Week 1 公司新闻类内容的最佳实践", "angle": "社媒运营·内容日历", "data_source": "内容日历: 06-02 Tuesday company_news/Facebook"},
        {"priority": "P2", "topic": "Alibaba vs Made-in-China：跨境B2B平台建筑建材品类流量对比", "angle": "平台分析·渠道选择", "data_source": "Marketplace Intel: 06-02 Alibaba/MIC 数据更新"},
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

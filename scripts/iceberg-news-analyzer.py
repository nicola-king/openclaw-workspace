#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
冰山理论新闻分析 - 太一自主判断重要性
太一 AGI · 全球新闻搜索系统 v1.0 (自进化)
创建：2026-04-19
"""

import os
import json
from datetime import datetime
from pathlib import Path

# 配置
WORKSPACE = "/home/nicola/.openclaw/workspace"
OUTPUT_DIR = f"{WORKSPACE}/news/iceberg"
DATE = datetime.now().strftime("%Y-%m-%d")
# 使用兼容的中文文件名（避免特殊字符）
OUTPUT_FILE = f"{OUTPUT_DIR}/冰山理论新闻分析-{DATE}.md"

# 新闻重要性评估权重
WEIGHTS = {
    'impact_scope': 0.25,
    'impact_depth': 0.25,
    'urgency': 0.20,
    'duration': 0.15,
    'uncertainty': 0.15
}


def evaluate_importance(news_item):
    """评估新闻重要性（太一自主判断）"""
    scores = {
        'impact_scope': 0,
        'impact_depth': 0,
        'urgency': 0,
        'duration': 0,
        'uncertainty': 0
    }
    
    title = news_item.get('title', '').lower()
    content = news_item.get('content', '').lower()
    
    # 关键词匹配
    global_keywords = ['global', 'world', 'international', '全球', '世界', '国际']
    paradigm_keywords = ['breakthrough', 'revolution', '突破', '革命', '历史性']
    crisis_keywords = ['war', 'conflict', 'crisis', '战争', '危机', '灾难']
    economic_keywords = ['economy', 'market', 'gdp', '经济', '市场']
    
    # 影响范围评分
    if any(kw in title or kw in content for kw in global_keywords):
        scores['impact_scope'] = 100
    elif '区域' in content:
        scores['impact_scope'] = 75
    elif '中国' in title:
        scores['impact_scope'] = 60
    else:
        scores['impact_scope'] = 40
    
    # 影响深度评分
    if any(kw in title or kw in content for kw in paradigm_keywords):
        scores['impact_depth'] = 100
    elif any(kw in title or kw in content for kw in crisis_keywords):
        scores['impact_depth'] = 80
    elif any(kw in title or kw in content for kw in economic_keywords):
        scores['impact_depth'] = 60
    else:
        scores['impact_depth'] = 40
    
    # 紧急程度评分
    if '突发' in title or 'breaking' in title:
        scores['urgency'] = 100
    elif '今日' in title:
        scores['urgency'] = 75
    else:
        scores['urgency'] = 50
    
    # 持续性评分
    if '政策' in content or 'policy' in content:
        scores['duration'] = 80
    elif '趋势' in content:
        scores['duration'] = 70
    else:
        scores['duration'] = 50
    
    # 不确定性评分
    if '更新' in content or 'developing' in content:
        scores['uncertainty'] = 100
    elif '确认' in content:
        scores['uncertainty'] = 40
    else:
        scores['uncertainty'] = 60
    
    # 计算加权总分
    total_score = sum(scores[k] * WEIGHTS[k] for k in scores)
    
    # 确定等级
    if total_score >= 90:
        grade = 'S'
    elif total_score >= 80:
        grade = 'A'
    elif total_score >= 70:
        grade = 'B'
    elif total_score >= 60:
        grade = 'C'
    else:
        grade = 'D'
    
    return {
        'total': round(total_score, 1),
        'grade': grade,
        'details': scores
    }


def iceberg_analysis(news_item, importance):
    """冰山理论深度分析（5 层）"""
    title = news_item.get('title', '未知')
    content = news_item.get('content', '')
    source = news_item.get('source', '未知')
    category = news_item.get('category', '未知')
    
    analysis = f"""## 🧊 {title}

**重要性评分**: {importance['total']} 分 | **等级**: {importance['grade']}  
**类别**: {category} | **来源**: {source}

---

### 📰 第一层：表面现象（10% 可见）

**事件概述**:
{content[:200] if content else '待补充详细报道'}

**时空坐标**:
- 时间：{datetime.now().strftime('%Y-%m-%d')}
- 地点：待确认

**关键参与方**:
- 待分析

---

### 🔍 第二层：直接原因（30% 浅层）

**触发因素**:
- [太一分析] 直接触发事件待识别

**相关方利益**:
| 相关方 | 利益诉求 | 立场 |
|--------|---------|------|
| 待分析 | - | - |

**历史背景**:
- 相关历史事件待补充

---

### 🏗️ 第三层：结构因素（40% 中层）

**系统动力**:
- [太一洞察] 推动事件的系统性力量

**权力关系**:
- 各方权力对比待分析
- 权力结构变化待观察

**制度约束**:
- 制度框架影响
- 规则限制

---

### 💎 第四层：核心矛盾（20% 深层）

**根本矛盾**:
- [太一智慧] 深层结构性矛盾

**范式转移**:
- 是否在发生范式级变化

**文明趋势**:
- 长期历史趋势
- 人类文明方向

---

### 🔮 第五层：二阶思维推演

| 时间维度 | 影响预测 | 概率 |
|---------|---------|------|
| **短期** (1-3 月) | 待推演 | - |
| **中期** (3-12 月) | 待推演 | - |
| **长期** (1-5 年) | 待推演 | - |

**黑天鹅风险**:
- 小概率高影响事件待识别

---

"""
    return analysis


def select_top_news(all_news, top_n=5):
    """选择最重要的 N 条新闻"""
    for news in all_news:
        news['importance'] = evaluate_importance(news)
    
    filtered = [n for n in all_news if n['importance']['grade'] != 'D']
    sorted_news = sorted(filtered, key=lambda x: x['importance']['total'], reverse=True)
    
    return sorted_news[:top_n]


def generate_iceberg_report(selected_news):
    """生成冰山分析报告"""
    report = f"""# 🧊 冰山理论新闻分析 · {DATE}

> **分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
> **选择标准**: 太一自主判断（5 维度加权）  
> **分析模型**: 冰山理论（5 层深度）  
> **系统状态**: 🧬 自进化系统 v1.0

---

## 📊 今日新闻重要性排名

| 排名 | 新闻标题 | 重要性评分 | 等级 | 类别 |
|------|---------|-----------|------|------|
"""
    
    for i, news in enumerate(selected_news, 1):
        title = news['title'][:30] + '...' if len(news['title']) > 30 else news['title']
        report += f"| {i} | {title} | {news['importance']['total']} 分 | {news['importance']['grade']} | {news['category']} |\n"
    
    report += """
---

## 🧊 深度分析

> 以下按重要性降序排列，每条新闻进行冰山理论 5 层分析

"""
    
    for news in selected_news:
        report += iceberg_analysis(news, news['importance'])
        report += "\n"
    
    report += f"""
---

## 📈 分析总结

### 今日新闻特征

- **S 级新闻**: {sum(1 for n in selected_news if n['importance']['grade'] == 'S')} 条
- **A 级新闻**: {sum(1 for n in selected_news if n['importance']['grade'] == 'A')} 条
- **B 级新闻**: {sum(1 for n in selected_news if n['importance']['grade'] == 'B')} 条

### 核心主题

1. [太一提炼] 今日核心主题 1
2. [太一提炼] 今日核心主题 2
3. [太一提炼] 今日核心主题 3

### 趋势洞察

- **短期关注**: [1-3 个月重点关注]
- **中期布局**: [3-12 个月趋势判断]
- **长期方向**: [1-5 年文明趋势]

---

*太一 AGI · 冰山理论分析系统 v1.0 (自进化)*  
*分析完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    
    return report


def main():
    """主函数"""
    print(f"🧊 冰山理论新闻分析启动")
    print(f"📍 工作目录：{WORKSPACE}")
    print(f"📅 分析日期：{DATE}")
    print(f"{'='*60}")
    
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    sample_news = [
        {
            'title': 'IMF 下调全球增长预期至 3.1%',
            'content': 'IMF 下调全球增长预期至 3.1%，全球经济弱但稳定。中东冲突影响全球经济展望。',
            'source': 'IMF',
            'category': '国际经济'
        },
        {
            'title': '伊朗对霍尔木兹海峡船只开火',
            'content': '伊朗革命卫队对霍尔木兹海峡过往船只开火，美国海军第五舰队宣布进入高度戒备状态。国际油价应声上涨 3%。',
            'source': 'Reuters',
            'category': '国际时事'
        },
        {
            'title': '斯坦福发布 2026 AI 指数报告',
            'content': 'AI 能力快速进步，但测量和管理能力跟不上。2026 年是可靠 AI 世界模型突破年。',
            'source': 'Stanford HAI',
            'category': 'AI 新闻'
        },
        {
            'title': '量子科技从理论走向工程化产业化',
            'content': '全球量子科技发展趋势报告发布，量子科技加速从理论走向工程化与产业化。',
            'source': '北京前沿未来研究院',
            'category': '前沿科技'
        },
        {
            'title': '中国 Q1 稳增长政策包发布',
            'content': '2026 年 Q1 稳增长政策包发布，含财政扩张、货币宽松、产业扶持三大举措。',
            'source': '新华网',
            'category': '中国政经'
        },
        {
            'title': '数控刀具东南亚市场爆发',
            'content': '月搜索 72 万，+55% 增长，毛利 42%，ROI 300%。重点市场：越南/泰国/印尼。',
            'source': '跨境贸易 Agent',
            'category': '产品趋势'
        },
        {
            'title': '英国发射 SPOQC 量子卫星',
            'content': '20 亿英镑量子投资计划，量子安全通信实现。',
            'source': '量子信息科学研究院',
            'category': '前沿科技'
        }
    ]
    
    print(f"\n📰 待分析新闻：{len(sample_news)} 条")
    selected_news = select_top_news(sample_news, top_n=5)
    print(f"✅ 选中新闻：{len(selected_news)} 条")
    
    print(f"\n📊 重要性排名:")
    for i, news in enumerate(selected_news, 1):
        print(f"  {i}. [{news['importance']['grade']}] {news['title']} ({news['importance']['total']}分)")
    
    print(f"\n🧊 生成冰山分析报告...")
    report = generate_iceberg_report(selected_news)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已保存：{OUTPUT_FILE}")
    print(f"{'='*60}")
    
    # 自动发送到 Telegram
    try:
        import sys
        sys.path.insert(0, f"{WORKSPACE}/skills/01-trading/cross-border-trade-agent")
        from telegram_md_sender_fixed import send_md_file
        
        # 使用中文文件名（与存储文件名一致，兼容格式）
        custom_filename = f"冰山理论新闻分析-{DATE}.md"
        
        result = send_md_file(
            OUTPUT_FILE,
            '🧊 冰山理论新闻分析 - 太一自主判断 Top5',
            check_duplicate=False,
            custom_filename=custom_filename
        )
        
        if result.get('ok'):
            print(f"✅ Telegram 推送成功！")
            print(f"📄 显示文件名：{custom_filename}")
        else:
            print(f"⚠️ Telegram 推送失败：{result}")
    except Exception as e:
        print(f"⚠️ Telegram 发送异常：{e}")
    
    return OUTPUT_FILE


if __name__ == "__main__":
    main()

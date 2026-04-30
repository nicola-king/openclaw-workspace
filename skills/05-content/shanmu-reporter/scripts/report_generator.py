#!/usr/bin/env python3
"""
山木 - 研报生成器
完整 workflow: 信号聚类 → 章节写作 → 最终组装
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

DB_PATH = "/home/nicola/.openclaw/workspace/polymarket-data/polymarket.db"

class ReportGenerator:
    """研报生成器 - 三阶段 pipeline"""
    
    def __init__(self):
        self.db_path = DB_PATH
    
    def cluster_signals(self, signals: List[Dict]) -> List[Dict]:
        """
        阶段 1: 聚类信号到 3-5 个主题
        
        Args:
            signals: 信号列表 [{"id": 1, "text": "...", "confidence": 0.95}, ...]
        
        Returns:
            clusters: [{"theme_title": "...", "signal_ids": [1,3,5], "rationale": "..."}, ...]
        """
        # 简单实现：按关键词聚类
        # 实际应该调用 LLM 进行智能聚类
        
        themes = {
            "气象异常": [],
            "市场流动性": [],
            "模型准确性": [],
            "套利机会": []
        }
        
        keywords_map = {
            "气象异常": ["天气", "温度", "降水", "极端", "气候"],
            "市场流动性": ["流动性", "交易量", "资金", "规模"],
            "模型准确性": ["置信度", "准确率", "模型", "预测"],
            "套利机会": ["套利", "机会", "收益", "下注"]
        }
        
        for signal in signals:
            text = signal.get("text", "").lower()
            assigned = False
            
            for theme, keywords in keywords_map.items():
                if any(kw in text for kw in keywords):
                    themes[theme].append(signal)
                    assigned = True
                    break
            
            if not assigned:
                themes["套利机会"].append(signal)
        
        # 转换为聚类格式
        clusters = []
        for theme, sigs in themes.items():
            if sigs:  # 只保留有信号的主题
                clusters.append({
                    "theme_title": theme,
                    "signal_ids": [s["id"] for s in sigs],
                    "signal_list": sigs,
                    "rationale": f"{len(sigs)} 个信号指向{theme}"
                })
        
        # 限制在 3-5 个主题
        clusters = sorted(clusters, key=lambda c: len(c["signal_ids"]), reverse=True)[:5]
        
        return clusters
    
    def write_section(self, cluster: Dict) -> str:
        """
        阶段 2: 为单个主题写深度分析章节
        
        Args:
            cluster: 主题聚类
        
        Returns:
            markdown: 章节内容
        """
        theme = cluster["theme_title"]
        signals = cluster["signal_list"]
        
        section = f"""## {theme}

### 核心信号
"""
        
        for i, sig in enumerate(signals[:5], 1):
            section += f"{i}. {sig['text']} (置信度：{sig.get('confidence', 'N/A'):.0%})\n"
        
        section += f"""
### 分析

基于 {len(signals)} 个信号的综合分析，{theme} 主题呈现以下特征：

1. **信号强度**: 平均置信度 {sum(s.get('confidence', 0.5) for s in signals) / len(signals):.0%}
2. **信号一致性**: {len(signals)} 个信号中有 {sum(1 for s in signals if s.get('confidence', 0.5) > 0.9)} 个高置信度 (>90%)
3. **时间分布**: 信号覆盖 {len(set(s.get('date', 'unknown') for s in signals))} 个时间点

### 图表配置

```json-chart
{{"type": "bar", "title": "{theme} - 信号置信度分布", "data": {json.dumps([{"label": f"信号{s['id']}", "value": s.get('confidence', 0.5)} for s in signals[:10]])}}}
```

"""
        
        return section
    
    def assemble_report(self, clusters: List[Dict], title: str = "Polymarket 分析报告") -> str:
        """
        阶段 3: 组装完整报告
        
        Args:
            clusters: 主题聚类列表
            title: 报告标题
        
        Returns:
            markdown: 完整报告
        """
        # 执行摘要
        summary_table = "| 主题 | 信号数 | 平均置信度 | 建议操作 |\n"
        summary_table += "|------|--------|-----------|----------|\n"
        
        for cluster in clusters:
            avg_conf = sum(s.get('confidence', 0.5) for s in cluster['signal_list']) / len(cluster['signal_list'])
            action = "增持" if avg_conf > 0.9 else "维持" if avg_conf > 0.8 else "观望"
            summary_table += f"| {cluster['theme_title']} | {len(cluster['signal_ids'])} | {avg_conf:.0%} | {action} |\n"
        
        report = f"""# {title}

> 生成时间：{datetime.now().isoformat()}
> 生成器：太一 AGI · 山木研报生成器 v1.0
> 信号总数：{sum(len(c['signal_ids']) for c in clusters)}
> 主题数量：{len(clusters)}

---

## Executive Summary

{summary_table}

---

## 深度分析

"""
        
        # 添加各章节
        for cluster in clusters:
            report += self.write_section(cluster)
            report += "\n---\n\n"
        
        # 风险因素
        report += """## 风险因素

1. **模型风险**: 策略基于历史数据，可能存在过拟合
2. **流动性风险**: 市场流动性不足可能影响执行
3. **黑天鹅风险**: 极端事件可能导致模型失效
4. **技术风险**: API 故障或数据延迟

---

## 参考资料

本报告基于 Polymarket 公开数据生成。

---

*生成：太一 AGI · 山木研报生成器 v1.0*
"""
        
        return report
    
    def generate_report(self, signals: List[Dict], title: str = "Polymarket 分析报告") -> str:
        """
        完整 pipeline: 聚类 → 写作 → 组装
        
        Args:
            signals: 信号列表
            title: 报告标题
        
        Returns:
            markdown: 完整报告
        """
        # 阶段 1: 聚类
        clusters = self.cluster_signals(signals)
        
        # 阶段 2+3: 组装 (包含写作)
        report = self.assemble_report(clusters, title)
        
        return report


def load_signals_from_db(limit=20):
    """从数据库加载信号"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title as text, sentiment_score as confidence, date as created_at
            FROM daily_news
            WHERE sentiment_score IS NOT NULL
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            "id": row[0],
            "text": row[1],
            "confidence": row[2] if row[2] else 0.5,
            "date": row[3]
        } for row in rows]
    
    except Exception as e:
        print(f"⚠️  数据库加载失败：{e}，使用模拟信号")
        return generate_synthetic_signals(limit)


def generate_synthetic_signals(limit=20):
    """生成模拟信号"""
    templates = [
        "BTC 突破 10 万美元，市场情绪高涨",
        "ETH ETF 通过 SEC 审核，机构资金流入",
        "美联储降息预期升温，风险资产受益",
        "Polymarket 日交易量创新高",
        "气象预测模型准确率提升至 96%",
    ]
    
    return [{
        "id": i,
        "text": templates[i % len(templates)] + f" (模拟#{i})",
        "confidence": 0.85 + (i % 10) * 0.01,
        "date": datetime.now().isoformat()
    } for i in range(limit)]


def main():
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  📝 山木研报生成器 v1.0                                    ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'⏰ 时间：{datetime.now().isoformat()}')
    print('')
    
    # 加载信号
    print('📊 加载信号...')
    signals = load_signals_from_db(limit=20)
    print(f'  ✅ {len(signals)} 个信号')
    print('')
    
    # 生成报告
    print('📝 生成报告...')
    generator = ReportGenerator()
    report = generator.generate_report(signals, title="Polymarket 气象套利分析报告")
    
    # 保存报告
    report_path = Path("/home/nicola/.openclaw/workspace/reports/shanmu-report-20260330.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f'  💾 报告已保存：{report_path}')
    print('')
    
    # 打印摘要
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  📊 报告生成摘要                                         ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'信号数：{len(signals)}')
    print(f'报告长度：{len(report)} 字符')
    print(f'输出文件：{report_path}')
    print('')
    print('✅ 报告生成完成')
    print('')


if __name__ == '__main__':
    main()

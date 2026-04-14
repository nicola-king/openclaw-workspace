#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
经验积累趋势图生成器

灵感：Auto Skill Optimizer
核心：73 → 79 → 70 → 84 → 87 (上升趋势)

功能:
1. 读取评估历史
2. 生成趋势数据
3. 生成 ASCII 趋势图
4. 生成 Markdown 趋势报告

作者：太一 AGI
创建：2026-04-14
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
REPORTS_DIR = WORKSPACE / "reports"

# 确保目录存在
REPORTS_DIR.mkdir(exist_ok=True)


class ExperienceTrendGenerator:
    """经验积累趋势图生成器"""
    
    def __init__(self):
        self.history_file = REPORTS_DIR / "skill-evaluation-history.json"
        self.trend_data: List[dict] = []
        self.load_history()
    
    def load_history(self):
        """加载评估历史"""
        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.trend_data = data.get('evaluations', [])
    
    def generate_trend_data(self) -> Dict:
        """生成趋势数据"""
        # 按时间分组
        time_groups = {}
        for item in self.trend_data:
            date = item['timestamp'][:10]  # YYYY-MM-DD
            if date not in time_groups:
                time_groups[date] = []
            time_groups[date].append(item)
        
        # 计算每日平均分
        daily_averages = []
        for date in sorted(time_groups.keys()):
            items = time_groups[date]
            avg_score = sum(item['total_score'] for item in items) / len(items)
            daily_averages.append({
                'date': date,
                'avg_score': avg_score,
                'skill_count': len(items),
            })
        
        return {
            'daily_averages': daily_averages,
            'total_days': len(daily_averages),
            'overall_avg': sum(d['avg_score'] for d in daily_averages) / max(len(daily_averages), 1),
            'trend': self.calculate_trend(daily_averages),
        }
    
    def calculate_trend(self, daily_averages: List[dict]) -> str:
        """计算趋势方向"""
        if len(daily_averages) < 2:
            return "稳定"
        
        recent = daily_averages[-3:]
        if len(recent) < 2:
            return "稳定"
        
        first_half = sum(d['avg_score'] for d in recent[:len(recent)//2]) / max(len(recent)//2, 1)
        second_half = sum(d['avg_score'] for d in recent[len(recent)//2:]) / max(len(recent) - len(recent)//2, 1)
        
        if second_half > first_half + 5:
            return "上升 ↑"
        elif second_half < first_half - 5:
            return "下降 ↓"
        else:
            return "稳定 →"
    
    def generate_ascii_chart(self, trend_data: Dict) -> str:
        """生成 ASCII 趋势图"""
        daily_averages = trend_data['daily_averages']
        
        if not daily_averages:
            return "暂无数据"
        
        # 限制显示最近 10 天
        recent = daily_averages[-10:]
        
        # 找到最大值和最小值
        scores = [d['avg_score'] for d in recent]
        min_score = min(scores)
        max_score = max(scores)
        
        # 生成图表
        chart_height = 10
        chart_width = len(recent)
        
        chart_lines = []
        for row in range(chart_height, -1, -1):
            threshold = min_score + (max_score - min_score) * row / chart_height
            line = f"{threshold:5.1f} |"
            for d in recent:
                if d['avg_score'] >= threshold:
                    line += "  ██"
                else:
                    line += "    "
            chart_lines.append(line)
        
        # 添加 X 轴
        chart_lines.append("      +" + "─" * (chart_width * 4))
        
        # 添加日期标签
        date_line = "       "
        for d in recent:
            date_line += f"{d['date'][5:]:4}"
        chart_lines.append(date_line)
        
        return "\n".join(chart_lines)
    
    def generate_report(self) -> Path:
        """生成趋势报告"""
        print("📈 生成经验积累趋势报告...")
        
        trend_data = self.generate_trend_data()
        ascii_chart = self.generate_ascii_chart(trend_data)
        
        report_file = REPORTS_DIR / f"experience-trend-report-{datetime.now().strftime('%Y%m%d')}.md"
        
        content = f"""# 📈 经验积累趋势报告

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **灵感**: Auto Skill Optimizer  
> **总天数**: {trend_data['total_days']} 天  
> **总体平均**: {trend_data['overall_avg']:.1f}/100  
> **趋势**: {trend_data['trend']}

---

## 📊 经验积累趋势

```
{ascii_chart}
```

**说明**: 每个 █ 代表一天的平均自信度分数

---

## 📈 趋势分析

### 整体趋势

| 指标 | 数值 |
|------|------|
| **总天数** | {trend_data['total_days']} 天 |
| **总体平均** | {trend_data['overall_avg']:.1f}/100 |
| **趋势方向** | {trend_data['trend']} |

### 每日详情

| 日期 | 平均分数 | Skills 数量 |
|------|---------|------------|
"""
        
        for d in trend_data['daily_averages'][-10:]:  # 最近 10 天
            content += f"| {d['date']} | {d['avg_score']:.1f} | {d['skill_count']} |\n"
        
        content += f"""
---

## 🎯 参考 Auto Skill Optimizer

### 经验积累曲线

```
73 → 79 → 70 → 84 → 87 (上升趋势)
```

**说明**:
- 初始阶段：73 分 (基础评估)
- 第一次优化：79 分 (+6 分)
- 调整阶段：70 分 (-9 分，正常波动)
- 第二次优化：84 分 (+14 分)
- 持续优化：87 分 (+3 分)

**总提升**: 73 → 87 (+14 分，+19.2%)

---

## 🚀 优化建议

### P0 - 立即实施
- [ ] 针对低分 Skills 进行优化
- [ ] 建立优化循环机制
- [ ] 记录每次优化效果

### P1 - 本周实施
- [ ] 实施 A/B Testing 验证
- [ ] 建立反馈循环
- [ ] 持续跟踪趋势

### P2 - 按需实施
- [ ] 自动化优化流程
- [ ] 智能优化建议
- [ ] 优化效果预测

---

## 📋 优化循环阶段

| 阶段 | 说明 | 目标分数 |
|------|------|---------|
| **0** | 智能分析准备 | 0-20 |
| **0.5** | 自动执行优化 | 20-40 |
| **1** | 自我评估 | 40-60 |
| **2** | A/B Testing 验证 | 60-80 |
| **3** | 反馈循环 | 80-100 |

---

*经验积累趋势报告 · 太一 AGI · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ 趋势报告已保存：{report_file}")
        return report_file


def main():
    """主函数"""
    generator = ExperienceTrendGenerator()
    
    # 生成趋势数据
    trend_data = generator.generate_trend_data()
    
    # 生成报告
    report = generator.generate_report()
    
    # 打印摘要
    print("\n" + "=" * 60)
    print("📈 经验积累趋势摘要")
    print("=" * 60)
    print(f"总天数：{trend_data['total_days']} 天")
    print(f"总体平均：{trend_data['overall_avg']:.1f}/100")
    print(f"趋势：{trend_data['trend']}")
    print(f"趋势报告：{report}")
    print("=" * 60)


if __name__ == "__main__":
    main()

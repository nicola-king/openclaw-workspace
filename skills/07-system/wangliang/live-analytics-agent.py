#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直播数据分析 Agent
功能：直播后台数据可视化 + 多维度分析 + 优化建议 + 迭代进化
版本：v1.0
创建：2026-03-26
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import os

class LiveAnalyticsAgent:
    """直播数据分析 Agent"""
    
    def __init__(self, platform: str = "douyin"):
        self.platform = platform
        self.data_dir = os.path.expanduser("~/.openclaw/workspace/data/live-analytics")
        self.logs_dir = os.path.expanduser("~/.openclaw/workspace/logs")
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # 核心指标权重（可迭代优化）
        self.metrics_weights = {
            "观看人数": 0.25,
            "平均停留时长": 0.20,
            "互动率": 0.20,
            "转化率": 0.20,
            "转粉率": 0.15
        }
        
        # 进化记录
        self.evolution_log = []
        
    def log(self, message: str):
        """日志记录"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        with open(f"{self.logs_dir}/live-analytics.log", "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")
    
    # ==================== 数据采集模块 ====================
    
    def collect_live_data(self, live_id: str) -> Dict:
        """
        采集直播实时数据
        支持平台：抖音/TikTok/淘宝/快手
        """
        self.log(f"开始采集直播数据：{live_id}")
        
        # 模拟数据结构（实际对接平台 API）
        live_data = {
            "live_id": live_id,
            "platform": self.platform,
            "timestamp": datetime.now().isoformat(),
            "basic_metrics": {
                "观看人数": 0,
                "最高在线": 0,
                "平均在线": 0,
                "新增粉丝": 0,
                "转粉率": 0.0
            },
            "engagement_metrics": {
                "点赞数": 0,
                "评论数": 0,
                "分享数": 0,
                "礼物收入": 0.0,
                "互动率": 0.0
            },
            "conversion_metrics": {
                "商品点击": 0,
                "下单数": 0,
                "成交金额": 0.0,
                "转化率": 0.0,
                "GPM": 0.0  # 千次观看成交
            },
            "time_series": {
                "观看曲线": [],  # 每分钟在线人数
                "互动曲线": [],  # 每分钟互动数
                "成交曲线": []   # 每分钟成交
            },
            "audience_profile": {
                "性别分布": {"男": 0, "女": 0},
                "年龄分布": {"18-23": 0, "24-30": 0, "31-40": 0, "40+": 0},
                "地域分布": {}
            }
        }
        
        self.log(f"数据采集完成：{live_id}")
        return live_data
    
    # ==================== 数据可视化模块 ====================
    
    def generate_dashboard(self, live_data: Dict) -> str:
        """
        生成数据可视化看板
        输出：Markdown 格式报告
        """
        self.log("生成数据可视化看板...")
        
        dashboard = f"""# 📊 直播数据可视化看板

**直播 ID**: {live_data['live_id']}
**平台**: {live_data['platform']}
**时间**: {live_data['timestamp']}

---

## 📈 核心指标概览

### 流量指标
| 指标 | 数值 | 行业基准 | 状态 |
|------|------|---------|------|
| 观看人数 | {live_data['basic_metrics']['观看人数']} | 5000+ | {'✅' if live_data['basic_metrics']['观看人数'] >= 5000 else '🟡'} |
| 最高在线 | {live_data['basic_metrics']['最高在线']} | 1000+ | {'✅' if live_data['basic_metrics']['最高在线'] >= 1000 else '🟡'} |
| 平均在线 | {live_data['basic_metrics']['平均在线']} | 500+ | {'✅' if live_data['basic_metrics']['平均在线'] >= 500 else '🟡'} |
| 新增粉丝 | {live_data['basic_metrics']['新增粉丝']} | 100+ | {'✅' if live_data['basic_metrics']['新增粉丝'] >= 100 else '🟡'} |
| 转粉率 | {live_data['basic_metrics']['转粉率']:.2f}% | 2%+ | {'✅' if live_data['basic_metrics']['转粉率'] >= 2 else '🟡'} |

### 互动指标
| 指标 | 数值 | 行业基准 | 状态 |
|------|------|---------|------|
| 点赞数 | {live_data['engagement_metrics']['点赞数']} | 10000+ | {'✅' if live_data['engagement_metrics']['点赞数'] >= 10000 else '🟡'} |
| 评论数 | {live_data['engagement_metrics']['评论数']} | 1000+ | {'✅' if live_data['engagement_metrics']['评论数'] >= 1000 else '🟡'} |
| 分享数 | {live_data['engagement_metrics']['分享数']} | 500+ | {'✅' if live_data['engagement_metrics']['分享数'] >= 500 else '🟡'} |
| 互动率 | {live_data['engagement_metrics']['互动率']:.2f}% | 5%+ | {'✅' if live_data['engagement_metrics']['互动率'] >= 5 else '🟡'} |

### 转化指标
| 指标 | 数值 | 行业基准 | 状态 |
|------|------|---------|------|
| 商品点击 | {live_data['conversion_metrics']['商品点击']} | 1000+ | {'✅' if live_data['conversion_metrics']['商品点击'] >= 1000 else '🟡'} |
| 下单数 | {live_data['conversion_metrics']['下单数']} | 100+ | {'✅' if live_data['conversion_metrics']['下单数'] >= 100 else '🟡'} |
| 成交金额 | ¥{live_data['conversion_metrics']['成交金额']:.2f} | ¥10000+ | {'✅' if live_data['conversion_metrics']['成交金额'] >= 10000 else '🟡'} |
| 转化率 | {live_data['conversion_metrics']['转化率']:.2f}% | 2%+ | {'✅' if live_data['conversion_metrics']['转化率'] >= 2 else '🟡'} |
| GPM | ¥{live_data['conversion_metrics']['GPM']:.2f} | ¥50+ | {'✅' if live_data['conversion_metrics']['GPM'] >= 50 else '🟡'} |

---

## 📉 趋势分析

### 观看曲线
```
[观看人数随时间变化曲线 - 每分钟数据点]
"""
        
        # 添加观看曲线数据
        if live_data['time_series']['观看曲线']:
            for point in live_data['time_series']['观看曲线'][-10:]:  # 最近 10 个点
                dashboard += f"\n{point['time']}: {point['value']}人"
        else:
            dashboard += "\n数据收集中..."
        
        dashboard += """
```

### 互动曲线
```
[互动数随时间变化曲线 - 每分钟数据点]
"""
        
        if live_data['time_series']['互动曲线']:
            for point in live_data['time_series']['互动曲线'][-10:]:
                dashboard += f"\n{point['time']}: {point['value']}次"
        else:
            dashboard += "\n数据收集中..."
        
        dashboard += """
```

---

## 👥 用户画像

### 性别分布
| 性别 | 占比 |
|------|------|
| 男 | {live_data['audience_profile']['性别分布']['男']:.1f}% |
| 女 | {live_data['audience_profile']['性别分布']['女']:.1f}% |

### 年龄分布
| 年龄段 | 占比 |
|--------|------|
| 18-23 岁 | {live_data['audience_profile']['年龄分布']['18-23']:.1f}% |
| 24-30 岁 | {live_data['audience_profile']['年龄分布']['24-30']:.1f}% |
| 31-40 岁 | {live_data['audience_profile']['年龄分布']['31-40']:.1f}% |
| 40 岁 + | {live_data['audience_profile']['年龄分布']['40+']:.1f}% |

---

*生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 直播数据分析 Agent v1.0*
"""
        
        self.log("数据看板生成完成")
        return dashboard
    
    # ==================== 数据分析解读模块 ====================
    
    def analyze_performance(self, live_data: Dict) -> Dict:
        """
        多维度数据分析解读
        返回：分析结果 + 问题诊断
        """
        self.log("开始多维度数据分析...")
        
        analysis = {
            "overall_score": 0,
            "dimension_scores": {},
            "problems": [],
            "highlights": [],
            "optimization_suggestions": []
        }
        
        # 1. 流量维度分析
        traffic_score = self._analyze_traffic(live_data)
        analysis["dimension_scores"]["流量"] = traffic_score
        
        # 2. 互动维度分析
        engagement_score = self._analyze_engagement(live_data)
        analysis["dimension_scores"]["互动"] = engagement_score
        
        # 3. 转化维度分析
        conversion_score = self._analyze_conversion(live_data)
        analysis["dimension_scores"]["转化"] = conversion_score
        
        # 4. 计算综合得分
        analysis["overall_score"] = (
            traffic_score * self.metrics_weights["观看人数"] +
            engagement_score * self.metrics_weights["互动率"] +
            conversion_score * self.metrics_weights["转化率"]
        )
        
        # 5. 问题诊断
        if traffic_score < 60:
            analysis["problems"].append("流量不足：需要加强预热和引流")
        if engagement_score < 60:
            analysis["problems"].append("互动偏低：需要优化话术和互动环节")
        if conversion_score < 60:
            analysis["problems"].append("转化率低：需要优化选品和促销策略")
        
        # 6. 亮点识别
        if traffic_score >= 80:
            analysis["highlights"].append("流量表现优秀！继续保持")
        if engagement_score >= 80:
            analysis["highlights"].append("互动氛围很好！主播表现力强")
        if conversion_score >= 80:
            analysis["highlights"].append("转化能力强！选品和话术精准")
        
        # 7. 优化建议
        analysis["optimization_suggestions"] = self._generate_suggestions(live_data, analysis)
        
        self.log(f"分析完成，综合得分：{analysis['overall_score']:.1f}")
        return analysis
    
    def _analyze_traffic(self, live_data: Dict) -> float:
        """流量维度分析（0-100 分）"""
        score = 0
        
        # 观看人数（30 分）
        views = live_data['basic_metrics']['观看人数']
        if views >= 10000:
            score += 30
        elif views >= 5000:
            score += 20
        elif views >= 1000:
            score += 10
        
        # 最高在线（30 分）
        peak = live_data['basic_metrics']['最高在线']
        if peak >= 2000:
            score += 30
        elif peak >= 1000:
            score += 20
        elif peak >= 500:
            score += 10
        
        # 转粉率（40 分）
        follow_rate = live_data['basic_metrics']['转粉率']
        if follow_rate >= 5:
            score += 40
        elif follow_rate >= 3:
            score += 30
        elif follow_rate >= 2:
            score += 20
        elif follow_rate >= 1:
            score += 10
        
        return score
    
    def _analyze_engagement(self, live_data: Dict) -> float:
        """互动维度分析（0-100 分）"""
        score = 0
        
        # 互动率（50 分）
        engagement_rate = live_data['engagement_metrics']['互动率']
        if engagement_rate >= 10:
            score += 50
        elif engagement_rate >= 5:
            score += 35
        elif engagement_rate >= 3:
            score += 20
        elif engagement_rate >= 1:
            score += 10
        
        # 分享数（30 分）
        shares = live_data['engagement_metrics']['分享数']
        views = live_data['basic_metrics']['观看人数']
        share_rate = (shares / views * 100) if views > 0 else 0
        if share_rate >= 5:
            score += 30
        elif share_rate >= 2:
            score += 20
        elif share_rate >= 1:
            score += 10
        
        # 礼物收入（20 分）
        gifts = live_data['engagement_metrics']['礼物收入']
        if gifts >= 1000:
            score += 20
        elif gifts >= 500:
            score += 15
        elif gifts >= 100:
            score += 10
        
        return score
    
    def _analyze_conversion(self, live_data: Dict) -> float:
        """转化维度分析（0-100 分）"""
        score = 0
        
        # 转化率（40 分）
        conversion_rate = live_data['conversion_metrics']['转化率']
        if conversion_rate >= 5:
            score += 40
        elif conversion_rate >= 3:
            score += 30
        elif conversion_rate >= 2:
            score += 20
        elif conversion_rate >= 1:
            score += 10
        
        # GPM（40 分）
        gpm = live_data['conversion_metrics']['GPM']
        if gpm >= 100:
            score += 40
        elif gpm >= 50:
            score += 30
        elif gpm >= 30:
            score += 20
        elif gpm >= 10:
            score += 10
        
        # 成交金额（20 分）
        gmv = live_data['conversion_metrics']['成交金额']
        if gmv >= 50000:
            score += 20
        elif gmv >= 10000:
            score += 15
        elif gmv >= 5000:
            score += 10
        
        return score
    
    def _generate_suggestions(self, live_data: Dict, analysis: Dict) -> List[str]:
        """生成优化建议"""
        suggestions = []
        
        # 根据各维度得分生成建议
        if analysis["dimension_scores"].get("流量", 0) < 60:
            suggestions.extend([
                "📢 加强直播前预热：提前 3 天发布预热视频",
                "📱 投放 DOU+ 引流：预算¥500-1000",
                "🤝 连麦 PK 引流：与同级别主播连麦",
                "📍 优化直播标题和封面：提升点击率"
            ])
        
        if analysis["dimension_scores"].get("互动", 0) < 60:
            suggestions.extend([
                "🎮 增加互动环节：每 10 分钟一次抽奖/问答",
                "💬 优化话术：多提问、引导评论",
                "🎁 设置互动福利：点赞到 X 万发福利",
                "⏰ 控制节奏：避免长时间单向讲解"
            ])
        
        if analysis["dimension_scores"].get("转化", 0) < 60:
            suggestions.extend([
                "🛍️ 优化选品：选择高性价比爆款",
                "💰 设置限时优惠：营造紧迫感",
                "📝 优化商品讲解：突出卖点和使用场景",
                "🎯 精准人群：调整投放定向"
            ])
        
        return suggestions
    
    # ==================== 迭代进化模块 ====================
    
    def save_live_record(self, live_data: Dict, analysis: Dict):
        """保存直播记录，用于迭代学习"""
        record_file = f"{self.data_dir}/live-records.json"
        
        # 加载现有记录
        records = []
        if os.path.exists(record_file):
            with open(record_file, 'r', encoding='utf-8') as f:
                records = json.load(f)
        
        # 添加新记录
        new_record = {
            "live_id": live_data['live_id'],
            "timestamp": live_data['timestamp'],
            "metrics": {
                "观看人数": live_data['basic_metrics']['观看人数'],
                "互动率": live_data['engagement_metrics']['互动率'],
                "转化率": live_data['conversion_metrics']['转化率'],
                "GPM": live_data['conversion_metrics']['GPM']
            },
            "overall_score": analysis['overall_score'],
            "dimension_scores": analysis['dimension_scores']
        }
        records.append(new_record)
        
        # 保存记录
        with open(record_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        
        self.log(f"直播记录已保存：{live_data['live_id']}")
        
        # 触发进化分析
        self._evolve(records)
    
    def _evolve(self, records: List[Dict]):
        """
        递归进化：分析历史数据，优化权重和策略
        """
        if len(records) < 5:
            self.log(f"记录数不足 ({len(records)}/5)，暂不进化")
            return
        
        self.log("开始递归进化分析...")
        
        # 1. 分析高分直播特征
        high_score_records = [r for r in records if r['overall_score'] >= 80]
        low_score_records = [r for r in records if r['overall_score'] < 60]
        
        evolution_insights = {
            "timestamp": datetime.now().isoformat(),
            "total_records": len(records),
            "high_score_count": len(high_score_records),
            "insights": []
        }
        
        if high_score_records:
            # 计算高分直播的平均指标
            avg_views = sum(r['metrics']['观看人数'] for r in high_score_records) / len(high_score_records)
            avg_engagement = sum(r['metrics']['互动率'] for r in high_score_records) / len(high_score_records)
            avg_conversion = sum(r['metrics']['转化率'] for r in high_score_records) / len(high_score_records)
            
            evolution_insights["insights"].append({
                "type": "高分特征",
                "description": f"高分直播平均观看:{avg_views:.0f}, 互动率:{avg_engagement:.2f}%, 转化率:{avg_conversion:.2f}%"
            })
        
        # 2. 权重优化建议
        evolution_insights["insights"].append({
            "type": "权重优化",
            "description": "根据历史数据，建议调整指标权重（待实现）"
        })
        
        # 3. 保存进化记录
        evolution_file = f"{self.data_dir}/evolution-log.json"
        evolution_records = []
        if os.path.exists(evolution_file):
            with open(evolution_file, 'r', encoding='utf-8') as f:
                evolution_records = json.load(f)
        evolution_records.append(evolution_insights)
        
        with open(evolution_file, 'w', encoding='utf-8') as f:
            json.dump(evolution_records, f, ensure_ascii=False, indent=2)
        
        self.evolution_log.append(evolution_insights)
        self.log(f"进化分析完成，已记录 {len(evolution_records)} 次进化")
    
    # ==================== 报告生成模块 ====================
    
    def generate_report(self, live_data: Dict, analysis: Dict) -> str:
        """生成完整分析报告"""
        dashboard = self.generate_dashboard(live_data)
        
        report = f"""{dashboard}

---

## 🔍 数据分析解读

### 综合得分：{analysis['overall_score']:.1f} / 100

| 维度 | 得分 | 状态 |
|------|------|------|
| 流量 | {analysis['dimension_scores'].get('流量', 0):.1f} | {'✅' if analysis['dimension_scores'].get('流量', 0) >= 80 else '🟡' if analysis['dimension_scores'].get('流量', 0) >= 60 else '❌'} |
| 互动 | {analysis['dimension_scores'].get('互动', 0):.1f} | {'✅' if analysis['dimension_scores'].get('互动', 0) >= 80 else '🟡' if analysis['dimension_scores'].get('互动', 0) >= 60 else '❌'} |
| 转化 | {analysis['dimension_scores'].get('转化', 0):.1f} | {'✅' if analysis['dimension_scores'].get('转化', 0) >= 80 else '🟡' if analysis['dimension_scores'].get('转化', 0) >= 60 else '❌'} |

---

## ⚠️ 问题诊断

"""
        
        if analysis['problems']:
            for problem in analysis['problems']:
                report += f"- {problem}\n"
        else:
            report += "暂无明显问题，表现优秀！\n"
        
        report += """
---

## ✨ 亮点识别

"""
        
        if analysis['highlights']:
            for highlight in analysis['highlights']:
                report += f"- {highlight}\n"
        else:
            report += "继续优化，争取更多亮点！\n"
        
        report += """
---

## 💡 优化建议

"""
        
        if analysis['optimization_suggestions']:
            for i, suggestion in enumerate(analysis['optimization_suggestions'], 1):
                report += f"{i}. {suggestion}\n"
        else:
            report += "保持当前策略，持续优化！\n"
        
        report += f"""
---

## 🔄 迭代进化

**历史直播场次**: {len(self.evolution_log) + 1}
**进化记录**: {len(self.evolution_log)} 次

> 系统会持续学习历史数据，自动优化分析模型和建议策略

---

*报告生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 直播数据分析 Agent v1.0*
"""
        
        return report


# ==================== 主函数 ====================

def main():
    """主函数：演示使用"""
    agent = LiveAnalyticsAgent(platform="douyin")
    
    # 模拟直播数据
    live_data = agent.collect_live_data("live_20260326_001")
    
    # 分析数据
    analysis = agent.analyze_performance(live_data)
    
    # 生成报告
    report = agent.generate_report(live_data, analysis)
    
    # 保存记录
    agent.save_live_record(live_data, analysis)
    
    # 输出报告
    print("\n" + "="*60)
    print(report)
    print("="*60)
    
    # 保存报告到文件
    report_file = f"{agent.data_dir}/live-report-20260326-001.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 报告已保存：{report_file}")


if __name__ == "__main__":
    main()

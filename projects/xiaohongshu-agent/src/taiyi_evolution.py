#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一进化引擎 - 小红书智能自进化核心

太一 v1.0 - Phase 2
功能：反馈收集 | 学习分析 | 策略优化 | 自主进化
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class TaiyiEvolutionEngine:
    """太一进化引擎"""
    
    def __init__(self, workspace: str = "~/.openclaw/workspace"):
        self.workspace = Path(workspace).expanduser()
        self.data_dir = self.workspace / "projects" / "xiaohongshu-agent" / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 进化状态
        self.evolution_state = {
            "version": "0.1.0",
            "created_at": datetime.now().isoformat(),
            "total_notes": 0,
            "viral_notes": 0,
            "avg_engagement": 0,
            "strategies": [],
            "learnings": []
        }
        
        # 策略库
        self.strategy_db = self._load_strategies()
        
        # 反馈日志
        self.feedback_log = []
    
    def _load_strategies(self) -> Dict[str, Any]:
        """加载策略库"""
        default_strategies = {
            "title_templates": [
                "数字 + 情绪 + 关键词",
                "痛点 + 解决方案",
                "场景 + 情感共鸣",
                "反差 + 好奇",
                "教程 + 价值"
            ],
            "content_styles": {
                "治愈系": {"engagement_rate": 8.5, "save_rate": 15.2},
                "教程类": {"engagement_rate": 9.2, "save_rate": 22.5},
                "分享类": {"engagement_rate": 7.8, "save_rate": 12.3},
                "故事类": {"engagement_rate": 10.1, "save_rate": 18.7}
            },
            "publish_times": {
                "07:00-09:00": {"label": "早高峰", "score": 7.5},
                "12:00-14:00": {"label": "午休", "score": 8.0},
                "19:00-21:00": {"label": "晚高峰", "score": 9.5},
                "21:00-23:00": {"label": "睡前", "score": 9.0}
            },
            "hot_topics": []
        }
        
        # 尝试加载已有策略
        strategy_file = self.data_dir / "strategy_db.json"
        if strategy_file.exists():
            try:
                return json.loads(strategy_file.read_text(encoding='utf-8'))
            except:
                pass
        
        return default_strategies
    
    def collect_feedback(self, note_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        收集笔记反馈
        
        参数:
            note_data: 笔记数据 (包含实际表现数据)
        
        返回:
            反馈分析报告
        """
        print("📝 收集笔记反馈...")
        
        feedback = {
            "note_id": note_data.get("id", datetime.now().timestamp()),
            "topic": note_data.get("topic", ""),
            "title": note_data.get("title", ""),
            "style": note_data.get("style", ""),
            "publish_time": note_data.get("publish_time", ""),
            "metrics": {
                "views": note_data.get("views", 0),
                "likes": note_data.get("likes", 0),
                "comments": note_data.get("comments", 0),
                "saves": note_data.get("saves", 0),
                "shares": note_data.get("shares", 0)
            },
            "calculated_metrics": {},
            "performance_level": "",
            "success_factors": [],
            "improvement_areas": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # 计算关键指标
        metrics = feedback["metrics"]
        if metrics["views"] > 0:
            feedback["calculated_metrics"] = {
                "engagement_rate": f"{(metrics['likes'] + metrics['comments']) / metrics['views'] * 100:.2f}%",
                "save_rate": f"{metrics['saves'] / metrics['views'] * 100:.2f}%",
                "share_rate": f"{metrics['shares'] / metrics['views'] * 100:.2f}%",
                "click_through_rate": note_data.get("predicted_ctr", 0)
            }
        
        # 评估表现等级
        feedback["performance_level"] = self._evaluate_performance(metrics)
        
        # 分析成功因素
        feedback["success_factors"] = self._analyze_success(note_data, metrics)
        
        # 识别改进点
        feedback["improvement_areas"] = self._identify_improvements(note_data, metrics)
        
        # 记录反馈
        self.feedback_log.append(feedback)
        
        # 更新进化状态
        self._update_evolution_state(feedback)
        
        # 保存反馈日志
        self._save_feedback_log()
        
        return feedback
    
    def _evaluate_performance(self, metrics: Dict[str, int]) -> str:
        """评估笔记表现等级"""
        views = metrics.get("views", 0)
        likes = metrics.get("likes", 0)
        
        if views > 100000 or likes > 10000:
            return "爆款 (10W+)"
        elif views > 10000 or likes > 1000:
            return "优秀 (1W+)"
        elif views > 1000 or likes > 100:
            return "良好 (1K+)"
        elif views > 100 or likes > 10:
            return "普通"
        else:
            return "待优化"
    
    def _analyze_success(self, note_data: Dict, metrics: Dict) -> List[str]:
        """分析成功因素"""
        factors = []
        
        # 标题分析
        title = note_data.get("title", "")
        if any(char.isdigit() for char in title):
            factors.append("✓ 标题包含数字，吸引点击")
        
        if any(e in title for e in ["绝了", "吹爆", "必入", "爱了"]):
            factors.append("✓ 标题包含情绪词，引发共鸣")
        
        # 风格分析
        style = note_data.get("style", "")
        if style == "教程类" and metrics.get("saves", 0) > 100:
            factors.append("✓ 教程类内容收藏率高")
        elif style == "治愈系" and metrics.get("likes", 0) > 500:
            factors.append("✓ 治愈系内容点赞率高")
        
        # 时间分析
        publish_time = note_data.get("publish_time", "")
        if "19:00" in publish_time or "21:00" in publish_time:
            factors.append("✓ 发布时间在黄金时段")
        
        # 热度分析
        if metrics.get("views", 0) > 5000:
            factors.append("✓ 话题热度高，流量大")
        
        return factors
    
    def _identify_improvements(self, note_data: Dict, metrics: Dict) -> List[str]:
        """识别改进点"""
        improvements = []
        
        views = metrics.get("views", 0)
        likes = metrics.get("likes", 0)
        saves = metrics.get("saves", 0)
        
        # 点击率低
        if views < 500:
            improvements.append("⚠ 优化标题和封面，提高点击率")
        
        # 互动率低
        if views > 1000 and likes / views < 0.03:
            improvements.append("⚠ 增强内容情感共鸣，提高互动率")
        
        # 收藏率低
        if views > 1000 and saves / views < 0.05:
            improvements.append("⚠ 增加实用价值，提高收藏率")
        
        # 发布时间
        if "03:00" in note_data.get("publish_time", "") or "04:00" in note_data.get("publish_time", ""):
            improvements.append("⚠ 调整发布时间到黄金时段")
        
        return improvements
    
    def _update_evolution_state(self, feedback: Dict):
        """更新进化状态"""
        self.evolution_state["total_notes"] += 1
        
        if feedback["performance_level"] in ["爆款 (10W+)", "优秀 (1W+)"]:
            self.evolution_state["viral_notes"] += 1
        
        # 更新策略库
        if feedback["success_factors"]:
            self._learn_from_success(feedback)
        
        if feedback["improvement_areas"]:
            self._learn_from_improvements(feedback)
    
    def _learn_from_success(self, feedback: Dict):
        """从成功中学习"""
        learning = {
            "type": "success",
            "topic": feedback["topic"],
            "style": feedback["style"],
            "factors": feedback["success_factors"],
            "metrics": feedback["metrics"],
            "timestamp": feedback["timestamp"]
        }
        
        self.evolution_state["learnings"].append(learning)
        
        # 更新策略库
        if feedback["style"] in self.strategy_db["content_styles"]:
            # 提高该风格的评分
            current = self.strategy_db["content_styles"][feedback["style"]]
            current["engagement_rate"] = min(15, current["engagement_rate"] + 0.5)
    
    def _learn_from_improvements(self, feedback: Dict):
        """从改进点中学习"""
        learning = {
            "type": "improvement",
            "topic": feedback["topic"],
            "issues": feedback["improvement_areas"],
            "timestamp": feedback["timestamp"]
        }
        
        self.evolution_state["learnings"].append(learning)
    
    def _save_feedback_log(self):
        """保存反馈日志"""
        log_file = self.data_dir / "feedback_log.json"
        
        # 读取现有日志
        existing_log = []
        if log_file.exists():
            try:
                existing_log = json.loads(log_file.read_text(encoding='utf-8'))
            except:
                pass
        
        # 追加新反馈
        existing_log.extend(self.feedback_log[-100:])  # 保留最近 100 条
        
        log_file.write_text(json.dumps(existing_log, ensure_ascii=False, indent=2), encoding='utf-8')
    
    def optimize_strategy(self) -> Dict[str, Any]:
        """优化策略库"""
        print("🚀 优化策略库...")
        
        # 分析反馈数据
        if len(self.feedback_log) < 3:
            return {"status": "数据不足，需要更多反馈"}
        
        # 统计各风格表现
        style_stats = {}
        for feedback in self.feedback_log:
            style = feedback.get("style", "未知")
            if style not in style_stats:
                style_stats[style] = {"count": 0, "viral": 0, "avg_views": 0}
            
            style_stats[style]["count"] += 1
            if feedback["performance_level"] in ["爆款 (10W+)", "优秀 (1W+)"]:
                style_stats[style]["viral"] += 1
            style_stats[style]["avg_views"] += feedback["metrics"].get("views", 0)
        
        # 计算平均
        for style in style_stats:
            style_stats[style]["avg_views"] /= style_stats[style]["count"]
            style_stats[style]["viral_rate"] = style_stats[style]["viral"] / style_stats[style]["count"] * 100
        
        # 生成优化建议
        optimization = {
            "timestamp": datetime.now().isoformat(),
            "total_feedback": len(self.feedback_log),
            "style_performance": style_stats,
            "best_style": max(style_stats.items(), key=lambda x: x[1]["viral_rate"])[0] if style_stats else "未知",
            "recommendations": self._generate_recommendations(style_stats)
        }
        
        # 保存优化结果
        opt_file = self.data_dir / "strategy_optimization.json"
        opt_file.write_text(json.dumps(optimization, ensure_ascii=False, indent=2), encoding='utf-8')
        
        return optimization
    
    def _generate_recommendations(self, style_stats: Dict) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        if not style_stats:
            return ["继续创作，积累更多数据"]
        
        # 最佳风格建议
        best_style = max(style_stats.items(), key=lambda x: x[1]["viral_rate"])
        recommendations.append(f"✓ 重点发展 {best_style[0]} 风格 (爆款率 {best_style[1]['viral_rate']:.1f}%)")
        
        # 待改进风格
        worst_style = min(style_stats.items(), key=lambda x: x[1]["viral_rate"])
        if worst_style[1]["viral_rate"] < 20:
            recommendations.append(f"⚠ {worst_style[0]} 风格需要优化 (爆款率仅 {worst_style[1]['viral_rate']:.1f}%)")
        
        # 通用建议
        recommendations.extend([
            "✓ 保持日更频率，持续输出",
            "✓ 蹭热搜话题，获取流量红利",
            "✓ 优化封面设计，提高点击率",
            "✓ 增加互动引导，提高评论率"
        ])
        
        return recommendations
    
    def generate_evolution_report(self) -> str:
        """生成进化报告"""
        print("📊 生成进化报告...")
        
        # 获取优化结果
        optimization = self.optimize_strategy()
        
        report = f"""# 太一进化引擎 · 自进化报告

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
> **版本**: {self.evolution_state['version']}  
> **状态**: 自进化中

---

## 📊 一、进化状态

| 指标 | 数值 |
|------|------|
| 总笔记数 | {self.evolution_state['total_notes']} |
| 爆款笔记 | {self.evolution_state['viral_notes']} |
| 爆款率 | {self.evolution_state['viral_notes'] / max(1, self.evolution_state['total_notes']) * 100:.1f}% |
| 反馈记录 | {len(self.feedback_log)} |
| 学习洞察 | {len(self.evolution_state['learnings'])} |

---

## 🎨 二、风格表现分析

"""
        
        if "style_performance" in optimization:
            report += "| 风格 | 数量 | 爆款数 | 爆款率 | 平均浏览 |\n"
            report += "|------|------|--------|--------|----------|\n"
            for style, stats in optimization.get("style_performance", {}).items():
                report += f"| {style} | {stats['count']} | {stats['viral']} | {stats['viral_rate']:.1f}% | {stats['avg_views']:.0f} |\n"
        
        report += f"""
**最佳风格**: {optimization.get('best_style', '数据不足')}

---

## 💡 三、优化建议

"""
        for i, rec in enumerate(optimization.get("recommendations", []), 1):
            report += f"{i}. {rec}\n"
        
        report += f"""
---

## 📈 四、学习洞察

"""
        # 最近 5 条学习
        recent_learnings = self.evolution_state['learnings'][-5:]
        for learning in recent_learnings:
            if learning["type"] == "success":
                report += f"✅ 成功：{learning['topic']} ({learning['style']})\n"
                for factor in learning.get("factors", [])[:2]:
                    report += f"   - {factor}\n"
            else:
                report += f"⚠ 改进：{learning['topic']}\n"
                for issue in learning.get("issues", [])[:2]:
                    report += f"   - {issue}\n"
        
        report += f"""
---

## 🎯 五、下一步计划

- [ ] 继续收集反馈数据
- [ ] 优化标题模板库
- [ ] 测试新的内容风格
- [ ] 分析竞品爆款笔记
- [ ] 调整发布策略

---

*报告生成：太一进化引擎 · 小红书智能自进化系统*
*版本：v{self.evolution_state['version']} | {datetime.now().strftime('%Y-%m-%d')}*

**让系统持续进化，让每个小白都能成为小红书达人。**
"""
        
        # 保存报告
        report_file = self.data_dir / f"evolution_report_{datetime.now().strftime('%Y%m%d')}.md"
        report_file.write_text(report, encoding='utf-8')
        
        return report
    
    def save_state(self):
        """保存进化状态"""
        state_file = self.data_dir / "evolution_state.json"
        state_file.write_text(json.dumps(self.evolution_state, ensure_ascii=False, indent=2), encoding='utf-8')
    
    def simulate_feedback(self, note: Dict) -> Dict:
        """模拟反馈数据 (用于测试)"""
        base_views = random.randint(500, 10000)
        
        # 根据风格调整
        style_multipliers = {
            "治愈系": 1.2,
            "教程类": 1.5,
            "分享类": 1.0,
            "故事类": 1.3
        }
        multiplier = style_multipliers.get(note.get("style", "治愈系"), 1.0)
        
        views = int(base_views * multiplier)
        likes = int(views * random.uniform(0.03, 0.15))
        comments = int(views * random.uniform(0.005, 0.03))
        saves = int(views * random.uniform(0.05, 0.25))
        shares = int(views * random.uniform(0.01, 0.05))
        
        return {
            "id": datetime.now().timestamp(),
            "topic": note.get("topic", ""),
            "title": note.get("title", ""),
            "style": note.get("style", ""),
            "publish_time": note.get("best_publish_time", ""),
            "views": views,
            "likes": likes,
            "comments": comments,
            "saves": saves,
            "shares": shares
        }


def main():
    """测试太一进化引擎"""
    print("=" * 60)
    print("🔄 太一进化引擎 - 自进化核心")
    print("=" * 60)
    
    engine = TaiyiEvolutionEngine()
    
    # 模拟收集反馈
    print("\n📝 模拟收集反馈...")
    test_notes = [
        {"topic": "春日壁纸", "style": "治愈系", "title": "这组春日壁纸绝了"},
        {"topic": "AI 教程", "style": "教程类", "title": "0 基础学会 AI 绘画"},
        {"topic": "副业分享", "style": "分享类", "title": "我的副业收入公开"},
    ]
    
    for note in test_notes:
        simulated = engine.simulate_feedback(note)
        feedback = engine.collect_feedback(simulated)
        print(f"  ✅ {note['topic']}: {feedback['performance_level']}")
    
    # 生成进化报告
    print("\n📊 生成进化报告...")
    report = engine.generate_evolution_report()
    print(f"✅ 报告已生成")
    
    # 保存状态
    engine.save_state()
    print("💾 状态已保存")
    
    print("\n" + "=" * 60)
    print("✅ 太一进化引擎测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
总 Agent 协调器 - 小红书智能自进化系统大脑

太一 v2.0 - Phase 2
功能：任务调度 | Agent 协调 | 决策审批 | 进化方向
"""

import asyncio
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.shanmu_agent import ShanmuAgent
from src.zhiji_agent import ZhijiAgent
from src.taiyi_evolution import TaiyiEvolutionEngine


class XiaohongshuMasterAgent:
    """总 Agent 协调器"""
    
    def __init__(self, workspace: str = "~/.openclaw/workspace"):
        self.workspace = Path(workspace).expanduser()
        self.output_dir = self.workspace / "projects" / "xiaohongshu-agent" / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化子 Agent
        self.shanmu = ShanmuAgent(workspace)    # 山木 (创作)
        self.zhiji = ZhijiAgent(workspace)      # 知几 (分析)
        self.taiyi = TaiyiEvolutionEngine(workspace)  # 太一 (进化)
        
        # 系统状态
        self.system_state = {
            "version": "2.0.0",
            "phase": "Phase 2 - 多 Agent 协作",
            "status": "active",
            "last_run": None,
            "total_runs": 0,
            "notes_created": 0,
            "feedback_collected": 0
        }
        
        # 加载状态
        self._load_state()
    
    def _load_state(self):
        """加载系统状态"""
        state_file = self.output_dir.parent / "data" / "master_state.json"
        if state_file.exists():
            try:
                saved_state = json.loads(state_file.read_text(encoding='utf-8'))
                self.system_state.update(saved_state)
            except:
                pass
    
    def _save_state(self):
        """保存系统状态"""
        state_file = self.output_dir.parent / "data" / "master_state.json"
        state_file.write_text(json.dumps(self.system_state, ensure_ascii=False, indent=2), encoding='utf-8')
    
    def daily_automation(self, auto_publish: bool = False) -> Dict[str, Any]:
        """
        每日自动化工作流 (完整版)
        
        流程:
        1. 知几分析热搜和趋势
        2. 生成选题建议
        3. 山木创作笔记内容
        4. 太一收集反馈并进化
        5. 生成完整日报
        
        参数:
            auto_publish: 是否自动发布 (默认 False，需人工确认)
        """
        print("=" * 80)
        print("🧠 小红书智能自进化系统 · 每日自动化工作流")
        print("=" * 80)
        print(f"📅 日期：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"🚀 版本：{self.system_state['version']}")
        print(f"📊 状态：{self.system_state['phase']}")
        print("=" * 80)
        
        # Step 1: 知几分析
        print("\n📊 Step 1: 知几分析热搜和趋势...")
        hot_search = self.zhiji.fetch_hot_search()
        trends = self.zhiji.predict_trends(7)
        print(f"✅ 获取 {len(hot_search['trending_topics'])} 个热搜话题")
        print(f"✅ 获取 {len(trends['hot_topics'])} 个趋势预测")
        
        # Step 2: 生成选题
        print("\n💡 Step 2: 生成选题建议...")
        topics = self._generate_smart_topics(hot_search, trends)
        print(f"✅ 生成 {len(topics)} 个智能选题")
        
        # Step 3: 山木创作
        print("\n✍️ Step 3: 山木创作笔记...")
        notes = []
        for i, topic in enumerate(topics[:5], 1):  # 创作前 5 个选题
            print(f"  📝 创作 #{i}: {topic['topic']}")
            note = self.shanmu.create_complete_note(
                topic=topic["topic"],
                style=topic["style"],
                target_audience=topic["audience"]
            )
            note["topic_data"] = topic
            notes.append(note)
            print(f"     ✅ {note['title'][:40]}...")
        
        # Step 4: 保存笔记
        print("\n💾 Step 4: 保存笔记...")
        saved_files = []
        for i, note in enumerate(notes, 1):
            filepath = self.shanmu.save_note(note, f"note_{datetime.now().strftime('%Y%m%d')}_{i}.md")
            saved_files.append(str(filepath))
            print(f"  ✅ {filepath.name}")
            self.system_state["notes_created"] += 1
        
        # Step 5: 模拟反馈收集 (实际运行时需要有真实数据)
        print("\n📝 Step 5: 太一收集反馈...")
        feedbacks = []
        for note in notes:
            simulated = self.taiyi.simulate_feedback(note)
            feedback = self.taiyi.collect_feedback(simulated)
            feedbacks.append(feedback)
            print(f"  ✅ {note['topic']}: {feedback['performance_level']}")
            self.system_state["feedback_collected"] += 1
        
        # Step 6: 策略优化
        print("\n🚀 Step 6: 太一优化策略...")
        optimization = self.taiyi.optimize_strategy()
        print(f"✅ 最佳风格：{optimization.get('best_style', '数据不足')}")
        
        # Step 7: 生成日报
        print("\n📝 Step 7: 生成完整日报...")
        daily_report = self._generate_comprehensive_report(
            hot_search, trends, topics, notes, feedbacks, optimization
        )
        
        report_path = self.output_dir / f"daily_full_{datetime.now().strftime('%Y%m%d')}.md"
        report_path.write_text(daily_report, encoding='utf-8')
        print(f"✅ 日报已保存：{report_path}")
        
        # Step 8: 生成进化报告
        print("\n📊 Step 8: 生成进化报告...")
        evolution_report = self.taiyi.generate_evolution_report()
        print(f"✅ 进化报告已生成")
        
        # 更新系统状态
        self.system_state["last_run"] = datetime.now().isoformat()
        self.system_state["total_runs"] += 1
        self._save_state()
        
        print("\n" + "=" * 80)
        print("✅ 每日自动化工作流完成！")
        print("=" * 80)
        print(f"📊 本次创作：{len(notes)} 篇笔记")
        print(f"📝 反馈收集：{len(feedbacks)} 条")
        print(f"📈 累计笔记：{self.system_state['notes_created']} 篇")
        print(f"🔄 累计运行：{self.system_state['total_runs']} 次")
        print("=" * 80)
        
        return {
            "hot_search": hot_search,
            "trends": trends,
            "topics": topics,
            "notes": notes,
            "feedbacks": feedbacks,
            "optimization": optimization,
            "report_path": str(report_path),
            "saved_files": saved_files
        }
    
    def _generate_smart_topics(self, hot_search: Dict, trends: Dict) -> List[Dict[str, str]]:
        """智能生成选题 (结合热搜和趋势)"""
        topics = []
        
        # 热搜 TOP5
        for topic in hot_search["trending_topics"][:5]:
            topic_name = topic["topic"].split("/")[0]
            
            # 智能匹配风格
            style = self._match_style_by_topic(topic_name, topic["category"])
            
            # 智能匹配受众
            audience = self._match_audience(topic["heat"], topic["category"])
            
            topics.append({
                "topic": topic_name,
                "style": style,
                "audience": audience,
                "heat": topic["heat"],
                "category": topic["category"],
                "rank": topic["rank"],
                "reason": f"热搜#{topic['rank']}，{topic['category']}类，{topic['heat']}",
                "source": "热搜"
            })
        
        # 趋势预测 TOP3
        for trend in trends["hot_topics"][:3]:
            topic_name = trend["topic"]
            
            # 避免重复
            if any(t["topic"] == topic_name for t in topics):
                continue
            
            style = self._match_style_by_topic(topic_name, "趋势")
            audience = "18-35 岁全人群"
            
            topics.append({
                "topic": topic_name,
                "style": style,
                "audience": audience,
                "heat": "🔥🔥🔥🔥",
                "category": "趋势",
                "rank": f"预测",
                "reason": f"趋势预测 ({trend['confidence']}): {trend['reason']}",
                "source": "趋势"
            })
        
        return topics
    
    def _match_style_by_topic(self, topic: str, category: str) -> str:
        """根据话题智能匹配风格"""
        style_keywords = {
            "壁纸": "治愈系",
            "教程": "教程类",
            "AI": "教程类",
            "技术": "教程类",
            "分享": "分享类",
            "推荐": "分享类",
            "故事": "故事类",
            "情感": "治愈系",
            "治愈": "治愈系",
            "美食": "分享类",
            "穿搭": "分享类",
            "旅行": "治愈系",
        }
        
        for keyword, style in style_keywords.items():
            if keyword in topic:
                return style
        
        # 默认根据分类
        category_style = {
            "科技": "教程类",
            "情感": "治愈系",
            "旅行": "治愈系",
            "美食": "分享类",
            "财经": "分享类",
        }
        
        return category_style.get(category, "治愈系")
    
    def _match_audience(self, heat: str, category: str) -> str:
        """根据热度和分类智能匹配受众"""
        if heat == "🔥🔥🔥🔥🔥":
            return "18-35 岁全人群"
        elif heat == "🔥🔥🔥🔥":
            return "20-35 岁年轻人"
        else:
            return "精准人群"
    
    def _generate_comprehensive_report(self, hot_search, trends, topics, notes, feedbacks, optimization) -> str:
        """生成完整日报"""
        report = f"""# 小红书智能自进化系统 · 每日完整日报

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
> **系统版本**: {self.system_state['version']}  
> **运行阶段**: {self.system_state['phase']}  
> **今日运行**: 第 {self.system_state['total_runs']} 次

---

## 🔥 一、热搜榜单 TOP5

| 排名 | 话题 | 热度 | 分类 | 增长 |
|------|------|------|------|------|
"""
        for topic in hot_search["trending_topics"][:5]:
            report += f"| {topic['rank']} | {topic['topic']} | {topic['heat']} | {topic['category']} | {topic['growth']} |\n"
        
        report += f"""
## 🔮 二、趋势预测

"""
        for trend in trends["hot_topics"][:3]:
            report += f"**{trend['topic']}** (置信度：{trend['confidence']})\n"
            report += f"- 原因：{trend['reason']}\n"
            report += f"- 建议：{', '.join(trend['suggested_content'])}\n\n"
        
        report += f"""
## 💡 三、智能选题

今日生成 {len(topics)} 个选题：

"""
        for i, topic in enumerate(topics, 1):
            report += f"**{i}. {topic['topic']}** ({topic['style']})\n"
            report += f"- 来源：{topic['source']}\n"
            report += f"- 热度：{topic['heat']}\n"
            report += f"- 受众：{topic['audience']}\n"
            report += f"- 理由：{topic['reason']}\n\n"
        
        report += f"""
## ✍️ 四、创作笔记

今日创作 {len(notes)} 篇笔记：

"""
        for i, note in enumerate(notes, 1):
            report += f"**{i}. {note['topic']}**\n"
            report += f"- 标题：{note['title']}\n"
            report += f"- 风格：{note['style']}\n"
            report += f"- 预测点击率：{note['predicted_ctr']}%\n"
            report += f"- 最佳发布：{note['best_publish_time']}\n\n"
        
        report += f"""
## 📊 五、反馈分析

"""
        viral_count = sum(1 for f in feedbacks if f["performance_level"] in ["爆款 (10W+)", "优秀 (1W+)"])
        report += f"- 总笔记数：{len(feedbacks)}\n"
        report += f"- 爆款/优秀：{viral_count} 篇 ({viral_count/len(feedbacks)*100:.0f}%)\n"
        report += f"- 普通/待优化：{len(feedbacks) - viral_count} 篇\n\n"
        
        for feedback in feedbacks:
            report += f"**{feedback['topic']}**: {feedback['performance_level']}\n"
            if feedback["success_factors"]:
                report += f"- ✅ {feedback['success_factors'][0]}\n"
        
        report += f"""
## 🚀 六、策略优化

"""
        report += f"**最佳风格**: {optimization.get('best_style', '数据不足')}\n\n"
        
        for i, rec in enumerate(optimization.get("recommendations", [])[:5], 1):
            report += f"{i}. {rec}\n"
        
        report += f"""
## 📈 七、系统状态

| 指标 | 数值 |
|------|------|
| 系统版本 | {self.system_state['version']} |
| 运行阶段 | {self.system_state['phase']} |
| 累计运行 | {self.system_state['total_runs']} 次 |
| 累计创作 | {self.system_state['notes_created']} 篇 |
| 累计反馈 | {self.system_state['feedback_collected']} 条 |

---

## 🎯 八、明日计划

- [ ] 监控今日笔记数据表现
- [ ] 根据反馈优化创作策略
- [ ] 继续跟进热点话题
- [ ] 测试新的内容形式
- [ ] 分析竞品爆款笔记

---

*日报生成：太一 AGI · 小红书智能自进化系统*
*总 Agent 协调器 · 多 Agent 协作*
*版本：v{self.system_state['version']} | {datetime.now().strftime('%Y-%m-%d')}*

---

**让每个小白都能掌握流量密码，递归进化成为小红书达人。**
"""
        return report
    
    def quick_create(self, topic: str, style: str = "治愈系") -> Dict[str, Any]:
        """快速创建单篇笔记"""
        print(f"📝 快速创作：{topic} ({style})")
        
        note = self.shanmu.create_complete_note(topic, style)
        filepath = self.shanmu.save_note(note)
        
        # 模拟反馈
        simulated = self.taiyi.simulate_feedback(note)
        feedback = self.taiyi.collect_feedback(simulated)
        
        self.system_state["notes_created"] += 1
        self.system_state["feedback_collected"] += 1
        self._save_state()
        
        return {
            "note": note,
            "filepath": str(filepath),
            "feedback": feedback
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "version": self.system_state["version"],
            "phase": self.system_state["phase"],
            "status": self.system_state["status"],
            "last_run": self.system_state["last_run"],
            "total_runs": self.system_state["total_runs"],
            "notes_created": self.system_state["notes_created"],
            "feedback_collected": self.system_state["feedback_collected"]
        }


def main():
    """测试总 Agent"""
    master = XiaohongshuMasterAgent()
    
    # 运行每日自动化
    result = master.daily_automation()
    
    print(f"\n📊 系统状态:")
    status = master.get_system_status()
    for key, value in status.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    master = XiaohongshuMasterAgent()
    master.daily_automation()

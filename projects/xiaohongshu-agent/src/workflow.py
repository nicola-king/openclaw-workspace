#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书 Agent 工作流编排器

太一 v1.0 - Phase 1 MVP
功能：知几 + 山木协作 | 自动化工作流 | 日报生成
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.shanmu_agent import ShanmuAgent
from src.zhiji_agent import ZhijiAgent


class XiaohongshuWorkflow:
    """小红书 Agent 工作流编排器"""
    
    def __init__(self, workspace: str = "~/.openclaw/workspace"):
        self.workspace = Path(workspace).expanduser()
        self.output_dir = self.workspace / "projects" / "xiaohongshu-agent" / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化 Agent
        self.shanmu = ShanmuAgent(workspace)  # 山木 (创作)
        self.zhiji = ZhijiAgent(workspace)    # 知几 (分析)
    
    def daily_workflow(self) -> Dict[str, Any]:
        """
        每日自动化工作流
        
        流程:
        1. 知几获取热搜和趋势
        2. 生成选题建议
        3. 山木创作笔记内容
        4. 输出完整方案
        """
        print("=" * 60)
        print("🤖 小红书每日工作流")
        print("=" * 60)
        
        # Step 1: 获取热搜数据
        print("\n📊 Step 1: 知几分析热搜...")
        hot_search = self.zhiji.fetch_hot_search()
        print(f"✅ 获取到 {len(hot_search['trending_topics'])} 个热搜话题")
        
        # Step 2: 生成选题建议
        print("\n💡 Step 2: 生成选题建议...")
        topics = self._generate_topic_suggestions(hot_search)
        print(f"✅ 生成 {len(topics)} 个选题建议")
        
        # Step 3: 创作笔记内容
        print("\n✍️ Step 3: 山木创作笔记...")
        notes = []
        for topic in topics[:3]:  # 创作前 3 个选题
            note = self.shanmu.create_complete_note(
                topic=topic["topic"],
                style=topic["style"],
                target_audience=topic["audience"]
            )
            notes.append(note)
            print(f"  ✅ {topic['topic']}: {note['title']}")
        
        # Step 4: 生成日报
        print("\n📝 Step 4: 生成每日创作日报...")
        daily_report = self._generate_daily_report(hot_search, topics, notes)
        
        # 保存日报
        report_path = self.output_dir / f"daily_{datetime.now().strftime('%Y%m%d')}.md"
        report_path.write_text(daily_report, encoding='utf-8')
        print(f"✅ 日报已保存：{report_path}")
        
        # Step 5: 保存笔记
        print("\n💾 Step 5: 保存笔记...")
        saved_files = []
        for i, note in enumerate(notes, 1):
            filepath = self.shanmu.save_note(note, f"note_{datetime.now().strftime('%Y%m%d')}_{i}.md")
            saved_files.append(str(filepath))
            print(f"  ✅ {filepath.name}")
        
        print("\n" + "=" * 60)
        print("✅ 每日工作流完成！")
        print("=" * 60)
        
        return {
            "hot_search": hot_search,
            "topics": topics,
            "notes": notes,
            "report_path": str(report_path),
            "saved_files": saved_files
        }
    
    def _generate_topic_suggestions(self, hot_search: Dict[str, Any]) -> List[Dict[str, str]]:
        """根据热搜生成选题建议"""
        suggestions = []
        
        for topic in hot_search["trending_topics"][:5]:
            topic_name = topic["topic"]
            heat = topic["heat"]
            category = topic["category"]
            
            # 根据分类推荐风格
            style_map = {
                "旅行": "治愈系",
                "科技": "教程类",
                "财经": "分享类",
                "美食": "分享类",
                "情感": "治愈系",
                "健身": "教程类",
                "穿搭": "分享类",
                "美妆": "分享类",
                "家居": "分享类",
                "职场": "教程类",
            }
            
            # 根据热度决定受众
            if heat == "🔥🔥🔥🔥🔥":
                audience = "18-35 岁全人群"
            elif heat == "🔥🔥🔥🔥":
                audience = "20-35 岁年轻人"
            else:
                audience = "精准人群"
            
            suggestions.append({
                "topic": topic_name.split("/")[0],  # 取主关键词
                "style": style_map.get(category, "治愈系"),
                "audience": audience,
                "heat": heat,
                "category": category,
                "reason": f"热搜#{topic['rank']}，{category}类，热度{heat}"
            })
        
        return suggestions
    
    def _generate_daily_report(self, hot_search: Dict, topics: List, notes: List) -> str:
        """生成每日创作日报"""
        report = f"""# 小红书每日创作日报

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
> **工作流**: 知几分析 + 山木创作  
> **版本**: Phase 1 MVP

---

## 🔥 一、今日热搜 TOP5

| 排名 | 话题 | 热度 | 分类 | 增长 |
|------|------|------|------|------|
"""
        for topic in hot_search["trending_topics"][:5]:
            report += f"| {topic['rank']} | {topic['topic']} | {topic['heat']} | {topic['category']} | {topic['growth']} |\n"
        
        report += f"""
## 💡 二、选题建议

今日推荐 {len(topics)} 个选题方向：

"""
        for i, topic in enumerate(topics, 1):
            report += f"**{i}. {topic['topic']}** ({topic['style']})\n"
            report += f"- 热度：{topic['heat']}\n"
            report += f"- 受众：{topic['audience']}\n"
            report += f"- 理由：{topic['reason']}\n\n"
        
        report += f"""
## ✍️ 三、已创作笔记

今日生成 {len(notes)} 篇笔记：

"""
        for i, note in enumerate(notes, 1):
            report += f"**{i}. {note['topic']}**\n"
            report += f"- 标题：{note['title']}\n"
            report += f"- 预测点击率：{note['predicted_ctr']}%\n"
            report += f"- 最佳发布：{note['best_publish_time']}\n\n"
        
        report += f"""
## 📊 四、创作建议

### 发布时间建议
- **最佳时间**: 19:00-21:00 (晚高峰)
- **次优时间**: 12:00-14:00 (午休)
- **情感内容**: 21:00-23:00 (睡前)

### 内容优化建议
1. 蹭热点：结合今日热搜 TOP3
2. 差异化：在热门话题中加入独特视角
3. 互动引导：结尾设置互动问题
4. 标签优化：使用 8-10 个精准标签

### 注意事项
- ⚠️ 避免硬广，保持内容真实
- ⚠️ 封面要清晰美观，信息量适中
- ⚠️ 及时回复评论，提高互动率

---

## 📁 五、输出文件

| 文件 | 用途 |
|------|------|
| `daily_{datetime.now().strftime('%Y%m%d')}.md` | 本日报 |
| `note_{datetime.now().strftime('%Y%m%d')}_1.md` | 笔记 1 |
| `note_{datetime.now().strftime('%Y%m%d')}_2.md` | 笔记 2 |
| `note_{datetime.now().strftime('%Y%m%d')}_3.md` | 笔记 3 |

---

## 🎯 六、明日计划

- [ ] 监控今日笔记数据
- [ ] 根据反馈优化创作策略
- [ ] 继续跟进热点话题
- [ ] 测试新的内容形式

---

*日报生成：太一 AGI · 小红书智能自进化系统*
*工作流：知几 (分析) + 山木 (创作)*
*版本：v0.1.0 | {datetime.now().strftime('%Y-%m-%d')}*

---

**让每个小白都能掌握流量密码，递归进化成为小红书达人。**
"""
        return report
    
    def create_single_note(self, topic: str, style: str = "治愈系") -> Dict[str, Any]:
        """
        快速创建单篇笔记
        
        参数:
            topic: 主题
            style: 风格
        """
        print(f"📝 创建笔记：{topic} ({style})")
        
        # 创作笔记
        note = self.shanmu.create_complete_note(topic, style)
        
        # 保存
        filepath = self.shanmu.save_note(note)
        
        print(f"✅ 标题：{note['title']}")
        print(f"📊 预测点击率：{note['predicted_ctr']}%")
        print(f"💾 已保存：{filepath}")
        
        return {
            "note": note,
            "filepath": str(filepath)
        }


def main():
    """测试工作流"""
    workflow = XiaohongshuWorkflow()
    
    # 运行每日工作流
    result = workflow.daily_workflow()
    
    print(f"\n📊 汇总:")
    print(f"- 热搜话题：{len(result['hot_search']['trending_topics'])} 个")
    print(f"- 选题建议：{len(result['topics'])} 个")
    print(f"- 创作笔记：{len(result['notes'])} 篇")
    print(f"- 日报路径：{result['report_path']}")


if __name__ == "__main__":
    workflow = XiaohongshuWorkflow()
    workflow.daily_workflow()

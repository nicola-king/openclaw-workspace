#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一旅行探路者自进化 Agent - Self-Evolving Travel Agent

功能:
1. 自动学习旅行数据
2. 自我优化推荐算法
3. 能力涌现检测
4. 技能自动创建
5. 经验积累与分享

集成:
- 太一旅行探路者 Agent
- 自进化触发器
- 智能调度中心
- 记忆系统

作者：太一 AGI
创建：2026-04-14
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
AGENT_DIR = Path(__file__).parent
DATA_DIR = AGENT_DIR / "data" / "evolution"
SKILLS_DIR = AGENT_DIR / "emerged-skills"
REPORTS_DIR = AGENT_DIR / "reports"

# 确保目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)
SKILLS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


class SelfEvolvingTravelAgent:
    """旅行探路者自进化 Agent"""
    
    def __init__(self):
        self.evolution_log: List[Dict] = []
        self.skills_created: List[str] = []
        self.learning_data: Dict = {
            "user_preferences": {},
            "popular_destinations": [],
            "seasonal_trends": {},
            "cost_patterns": {},
        }
        
        print(f"🌍 太一旅行探路者自进化 Agent 启动")
        print(f"  数据目录：{DATA_DIR}")
        print(f"  技能目录：{SKILLS_DIR}")
        print(f"  报告目录：{REPORTS_DIR}")
    
    # ========== 自进化核心功能 ==========
    
    def learn_from_trip(self, trip_plan: Dict, feedback: Optional[Dict] = None) -> Dict:
        """
        从旅行计划中学习
        
        Args:
            trip_plan: 旅行计划
            feedback: 用户反馈 (可选)
        
        Returns:
            学习结果
        """
        print(f"\n🧠 从旅行计划中学习")
        
        # 提取学习数据
        destination = trip_plan.get("destination", "未知")
        budget = trip_plan.get("budget", {}).get("total", 0)
        travelers = trip_plan.get("travelers", 1)
        
        # 更新目的地热度
        if destination not in self.learning_data["popular_destinations"]:
            self.learning_data["popular_destinations"].append(destination)
        
        # 更新预算模式
        if destination not in self.learning_data["cost_patterns"]:
            self.learning_data["cost_patterns"][destination] = []
        self.learning_data["cost_patterns"][destination].append({
            "budget": budget,
            "travelers": travelers,
            "date": datetime.now().isoformat(),
        })
        
        # 记录反馈
        if feedback:
            self.learning_data["user_preferences"][destination] = feedback
        
        # 保存学习数据
        self._save_learning_data()
        
        # 检测能力涌现
        emergence_signals = self._detect_emergence()
        
        result = {
            "type": "Learning",
            "destination": destination,
            "learned_at": datetime.now().isoformat(),
            "emergence_signals": emergence_signals,
        }
        
        self.evolution_log.append(result)
        
        print(f"  目的地：{destination}")
        print(f"  热门目的地：{len(self.learning_data['popular_destinations'])} 个")
        print(f"  能力涌现信号：{len(emergence_signals)} 个")
        
        return result
    
    def optimize_recommendations(self) -> Dict:
        """
        优化推荐算法
        
        Returns:
            优化结果
        """
        print(f"\n🔄 优化推荐算法")
        
        # 分析热门目的地
        popular = self.learning_data["popular_destinations"]
        
        # 分析预算模式
        cost_patterns = self.learning_data["cost_patterns"]
        
        # 生成优化建议
        recommendations = []
        
        for dest in popular[:5]:  # 前 5 个热门目的地
            if dest in cost_patterns:
                avg_budget = sum(p["budget"] for p in cost_patterns[dest]) / len(cost_patterns[dest])
                recommendations.append({
                    "destination": dest,
                    "avg_budget": avg_budget,
                    "popularity_rank": popular.index(dest) + 1,
                    "recommendation_score": 100 - popular.index(dest) * 10,
                })
        
        # 保存优化结果
        optimization_result = {
            "type": "Optimization",
            "recommendations": recommendations,
            "optimized_at": datetime.now().isoformat(),
        }
        
        self._save_optimization(optimization_result)
        
        print(f"  生成推荐：{len(recommendations)} 个")
        for rec in recommendations[:3]:
            print(f"    - {rec['destination']}: ¥{rec['avg_budget']:.0f} (评分：{rec['recommendation_score']})")
        
        return optimization_result
    
    def detect_emergence(self) -> List[Dict]:
        """
        检测能力涌现
        
        Returns:
            涌现信号列表
        """
        print(f"\n✨ 检测能力涌现")
        
        signals = self._detect_emergence()
        
        for signal in signals:
            print(f"  🚀 涌现信号：{signal['type']}")
            print(f"     原因：{signal['reason']}")
            print(f"     优先级：{signal['priority']}")
        
        return signals
    
    def create_emerged_skill(self, signal: Dict) -> str:
        """
        创建涌现技能
        
        Args:
            signal: 涌现信号
        
        Returns:
            技能名称
        """
        print(f"\n🎨 创建涌现技能")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        skill_name = f"travel-skill-{timestamp}"
        skill_dir = SKILLS_DIR / skill_name
        
        # 创建技能目录
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建 SKILL.md
        skill_md = skill_dir / "SKILL.md"
        with open(skill_md, 'w', encoding='utf-8') as f:
            f.write(f"""# {skill_name}

> **创建时间**: {datetime.now().isoformat()}  
> **来源**: 能力涌现  
> **类型**: {signal['type']}

---

## 🎯 职责域

{signal['reason']}

---

## 📋 功能

自动创建的技能，用于处理：
- {signal['reason']}

---

## 🚀 使用方式

```python
# 自动调用
from skills.emerged-skills.{skill_name} import {skill_name.replace('-', '_')}

skill = {skill_name.replace('-', '_')}()
result = skill.execute()
```

---

*太一旅行探路者自进化 Agent · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
""")
        
        # 创建主程序
        main_py = skill_dir / f"{skill_name.replace('-', '_')}.py"
        with open(main_py, 'w', encoding='utf-8') as f:
            f.write(f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
{skill_name}

自动创建的涌现技能
\"\"\"

from pathlib import Path

class {skill_name.replace('-', '_').replace('_', ' ').title().replace(' ', '')}:
    \"\"\"{skill_name}\"\"\"
    
    def __init__(self):
        self.skill_name = "{skill_name}"
    
    def execute(self):
        \"\"\"执行技能\"\"\"
        print(f"执行技能：{{self.skill_name}}")
        return {{"success": True, "skill": self.skill_name}}

if __name__ == "__main__":
    skill = {skill_name.replace('-', '_').replace('_', ' ').title().replace(' ', '')}()
    result = skill.execute()
    print(f"结果：{{result}}")
""")
        
        self.skills_created.append(skill_name)
        
        print(f"  技能名称：{skill_name}")
        print(f"  技能目录：{skill_dir}")
        print(f"  ✅ 技能已创建")
        
        return skill_name
    
    def share_experience(self) -> Dict:
        """
        分享经验
        
        Returns:
            分享内容
        """
        print(f"\n📢 分享经验")
        
        # 生成经验总结
        experience = {
            "type": "Experience Sharing",
            "popular_destinations": self.learning_data["popular_destinations"][:10],
            "cost_insights": {},
            "tips": [
                "提前 2-3 个月预订机票最便宜",
                "避开旺季可节省 30%+ 费用",
                "多城市路线优化可节省 15%+",
                "使用促销码可额外节省 10-20%",
            ],
            "shared_at": datetime.now().isoformat(),
        }
        
        # 分析成本洞察
        for dest, patterns in self.learning_data["cost_patterns"].items():
            if patterns:
                avg = sum(p["budget"] for p in patterns) / len(patterns)
                experience["cost_insights"][dest] = {
                    "avg_budget": avg,
                    "min_budget": min(p["budget"] for p in patterns),
                    "max_budget": max(p["budget"] for p in patterns),
                }
        
        # 保存经验分享
        self._save_experience(experience)
        
        print(f"  热门目的地：{len(experience['popular_destinations'])} 个")
        print(f"  成本洞察：{len(experience['cost_insights'])} 个")
        print(f"  旅行贴士：{len(experience['tips'])} 个")
        
        return experience
    
    # ========== 辅助方法 ==========
    
    def _detect_emergence(self) -> List[Dict]:
        """检测能力涌现"""
        signals = []
        
        # 检测 1: 同类目的地重复出现 ≥3 次
        dest_counts = {}
        for dest in self.learning_data["popular_destinations"]:
            dest_counts[dest] = dest_counts.get(dest, 0) + 1
        
        for dest, count in dest_counts.items():
            if count >= 3:
                signals.append({
                    "type": "Repeated Destination",
                    "reason": f"{dest} 出现 {count} 次，建议创建专门技能",
                    "priority": "P1",
                    "data": {"destination": dest, "count": count},
                })
        
        # 检测 2: 预算模式异常
        for dest, patterns in self.learning_data["cost_patterns"].items():
            if len(patterns) >= 5:
                budgets = [p["budget"] for p in patterns]
                avg = sum(budgets) / len(budgets)
                variance = sum((b - avg) ** 2 for b in budgets) / len(budgets)
                
                if variance > avg * 0.5:  # 方差过大
                    signals.append({
                        "type": "Budget Pattern Anomaly",
                        "reason": f"{dest} 预算波动大，建议创建预算优化技能",
                        "priority": "P2",
                        "data": {"destination": dest, "avg_budget": avg, "variance": variance},
                    })
        
        # 检测 3: 用户反馈集中
        for dest, feedback in self.learning_data["user_preferences"].items():
            if isinstance(feedback, dict) and feedback.get("rating", 0) >= 4.5:
                signals.append({
                    "type": "High Rating Destination",
                    "reason": f"{dest} 评分高 ({feedback.get('rating')})，建议创建推荐技能",
                    "priority": "P2",
                    "data": {"destination": dest, "rating": feedback.get("rating")},
                })
        
        return signals
    
    def _save_learning_data(self):
        """保存学习数据"""
        import json
        output_file = DATA_DIR / f"learning_data_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.learning_data, f, indent=2, ensure_ascii=False)
    
    def _save_optimization(self, result: Dict):
        """保存优化结果"""
        import json
        output_file = DATA_DIR / f"optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    
    def _save_experience(self, experience: Dict):
        """保存经验分享"""
        import json
        output_file = DATA_DIR / f"experience_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(experience, f, indent=2, ensure_ascii=False)
    
    def generate_evolution_report(self) -> Path:
        """生成进化报告"""
        report_file = REPORTS_DIR / f"evolution_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        content = f"""# 🌍 太一旅行探路者自进化报告

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **学习次数**: {len(self.evolution_log)}  
> **创建技能**: {len(self.skills_created)} 个

---

## 📊 进化统计

| 指标 | 数值 |
|------|------|
| **学习次数** | {len(self.evolution_log)} |
| **创建技能** | {len(self.skills_created)} |
| **热门目的地** | {len(self.learning_data['popular_destinations'])} |
| **预算模式** | {len(self.learning_data['cost_patterns'])} |
| **用户偏好** | {len(self.learning_data['user_preferences'])} |

---

## 🚀 能力涌现

"""
        
        # 汇总所有涌现信号
        all_signals = []
        for log in self.evolution_log:
            if "emergence_signals" in log:
                all_signals.extend(log["emergence_signals"])
        
        if all_signals:
            content += f"""
| 类型 | 原因 | 优先级 |
|------|------|--------|
"""
            for signal in all_signals[:10]:
                content += f"| {signal['type']} | {signal['reason'][:50]} | {signal['priority']} |\n"
        
        content += f"""
---

## 🎨 已创建技能

"""
        
        for skill in self.skills_created[:10]:
            content += f"- ✅ {skill}\n"
        
        content += f"""
---

## 📢 经验分享

热门目的地 Top 10:
"""
        
        for i, dest in enumerate(self.learning_data["popular_destinations"][:10], 1):
            content += f"{i}. {dest}\n"
        
        content += f"""
---

*太一旅行探路者自进化 Agent · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 进化报告已生成：{report_file}")
        return report_file


def main():
    """测试"""
    print("=" * 60)
    print("🌍 太一旅行探路者自进化 Agent 测试")
    print("=" * 60)
    
    agent = SelfEvolvingTravelAgent()
    
    # 测试 1: 从旅行计划中学习
    print("\n🧠 测试 1: 从旅行计划中学习")
    trip_plan = {
        "destination": "东京",
        "budget": {"total": 15000},
        "travelers": 2,
    }
    feedback = {"rating": 4.8, "comments": "非常好"}
    result = agent.learn_from_trip(trip_plan, feedback)
    
    # 重复学习多次以触发能力涌现
    for i in range(3):
        agent.learn_from_trip({"destination": "东京", "budget": {"total": 15000 + i * 1000}, "travelers": 2})
    
    # 测试 2: 优化推荐算法
    print("\n🔄 测试 2: 优化推荐算法")
    optimization = agent.optimize_recommendations()
    
    # 测试 3: 检测能力涌现
    print("\n✨ 测试 3: 检测能力涌现")
    signals = agent.detect_emergence()
    
    # 测试 4: 创建涌现技能
    if signals:
        print("\n🎨 测试 4: 创建涌现技能")
        skill_name = agent.create_emerged_skill(signals[0])
    
    # 测试 5: 分享经验
    print("\n📢 测试 5: 分享经验")
    experience = agent.share_experience()
    
    # 测试 6: 生成进化报告
    print("\n📊 测试 6: 生成进化报告")
    report = agent.generate_evolution_report()
    
    print("\n" + "=" * 60)
    print("✅ 太一旅行探路者自进化 Agent 测试完成")
    print("=" * 60)
    
    print(f"\n📁 输出文件:")
    print(f"  数据目录：{DATA_DIR}")
    print(f"  技能目录：{SKILLS_DIR}")
    print(f"  报告目录：{REPORTS_DIR}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Learning Orchestrator - 学习循环编排器

核心职责:
- 协调任务追踪 → 模式识别 → 技能创建 → 知识持久化
- 管理学习循环状态
- 生成学习报告
- 触发 Nudge 提醒

作者：太一 AGI
创建：2026-04-09
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# 导入子模块
from task_tracker import TaskTracker, TaskRecord
from skill_creator import SkillCreator, SkillProposal
from nudge_manager import NudgeManager

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
LOOP_DIR = WORKSPACE / "skills/hermes-learning-loop/loop"
STATE_FILE = LOOP_DIR / "learning_state.json"
REPORT_DIR = WORKSPACE / "reports"


@dataclass
class LearningCycle:
    """学习周期"""
    cycle_id: str
    start_time: str
    end_time: Optional[str]
    tasks_analyzed: int
    patterns_detected: int
    skills_created: int
    nudges_triggered: int
    insights_persisted: int
    status: str  # running/completed


class LearningOrchestrator:
    """学习循环编排器"""
    
    def __init__(self):
        self.tracker = TaskTracker()
        self.creator = SkillCreator()
        self.nudge_mgr = NudgeManager()
        self.state = self.load_state()
        self.current_cycle = self.get_or_create_cycle()
    
    def load_state(self) -> Dict:
        """加载学习状态"""
        if STATE_FILE.exists():
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "cycles": [],
            "total_skills_created": 0,
            "total_nudges": 0,
            "last_run": None
        }
    
    def save_state(self):
        """保存学习状态"""
        STATE_FILE.parent.mkdir(exist_ok=True)
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
    
    def get_or_create_cycle(self) -> LearningCycle:
        """获取或创建当前学习周期"""
        # 检查是否有运行中的周期
        for cycle_data in self.state["cycles"]:
            if cycle_data["status"] == "running":
                return LearningCycle(**cycle_data)
        
        # 创建新周期
        cycle = LearningCycle(
            cycle_id=f"cycle-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            start_time=datetime.now().isoformat(),
            end_time=None,
            tasks_analyzed=0,
            patterns_detected=0,
            skills_created=0,
            nudges_triggered=0,
            insights_persisted=0,
            status="running"
        )
        
        self.state["cycles"].append(asdict(cycle))
        self.save_state()
        return cycle
    
    def run_learning_cycle(self) -> Dict:
        """
        执行完整学习循环
        
        流程:
        1. 任务追踪 → 加载并分析任务
        2. 模式识别 → 检测重复/复杂度
        3. 技能创建 → 生成技能提议
        4. 知识持久化 → 更新记忆
        5. Nudge 触发 → 提醒用户
        
        Returns:
            学习循环报告
        """
        print("🧠 太一学习循环 v1.0")
        print("=" * 60)
        print(f"周期 ID: {self.current_cycle.cycle_id}")
        print(f"开始时间：{self.current_cycle.start_time}")
        print("")
        
        report = {
            "cycle_id": self.current_cycle.cycle_id,
            "start_time": self.current_cycle.start_time,
            "steps": []
        }
        
        # 步骤 1: 任务追踪
        print("📋 [1/5] 任务追踪...")
        tasks = self.tracker.parse_heartbeat()
        self.tracker.update_history(tasks)
        self.current_cycle.tasks_analyzed = len(tasks)
        print(f"  ✅ 加载任务：{len(tasks)} 个")
        report["steps"].append({
            "name": "任务追踪",
            "status": "success",
            "count": len(tasks)
        })
        
        # 步骤 2: 模式识别
        print("\n🔍 [2/5] 模式识别...")
        patterns = self.tracker.detect_patterns()
        self.current_cycle.patterns_detected = len(patterns)
        print(f"  ✅ 检测模式：{len(patterns)} 个")
        for pattern_name, pattern in patterns.items():
            print(f"    - {pattern_name}: 频率 {pattern.frequency}, 成功率 {pattern.success_rate:.0%}")
        report["steps"].append({
            "name": "模式识别",
            "status": "success",
            "count": len(patterns)
        })
        
        # 步骤 3: 技能创建检测
        print("\n🛠️ [3/5] 技能创建检测...")
        alerts = self.tracker.get_repetition_alerts(threshold=3)
        skills_to_create = []
        
        for alert in alerts:
            print(f"  ⚠️  检测到重复任务：{alert['task_type']} ({alert['count']}次)")
            print(f"      建议：{alert['recommendation']}")
            skills_to_create.append(alert)
        
        if skills_to_create:
            self.current_cycle.skills_created = len(skills_to_create)
            # 添加到待处理列表
            for skill_info in skills_to_create:
                proposal = SkillProposal(
                    name=f"{skill_info['task_type']}-automation",
                    reason=skill_info['recommendation'],
                    trigger_type="repetition",
                    task_ids=skill_info['task_ids'],
                    responsibilities=[f"自动化处理{skill_info['task_type']}任务"],
                    estimated_commands=[f"{skill_info['task_type']} execute"],
                    priority=skill_info['priority'],
                    created_at=datetime.now().isoformat()
                )
                self.creator.pending.append(asdict(proposal))
            
            self.creator.save_pending()
            print(f"  ✅ 已生成 {len(skills_to_create)} 个技能提议")
        else:
            print(f"  ✅ 无需创建新技能")
        
        report["steps"].append({
            "name": "技能创建检测",
            "status": "success",
            "count": len(skills_to_create)
        })
        
        # 步骤 4: 知识持久化
        print("\n💾 [4/5] 知识持久化...")
        insights_count = self.persist_insights()
        self.current_cycle.insights_persisted = insights_count
        print(f"  ✅ 持久化洞察：{insights_count} 条")
        report["steps"].append({
            "name": "知识持久化",
            "status": "success",
            "count": insights_count
        })
        
        # 步骤 5: Nudge 触发
        print("\n🔔 [5/5] Nudge 触发...")
        nudges = self.nudge_mgr.check_nudges() or []
        if nudges:
            print(f"  ⚠️  触发 {len(nudges)} 个 Nudge 提醒")
            for nudge in nudges:
                print(f"    - {nudge.get('message', '未知')}")
            self.current_cycle.nudges_triggered = len(nudges)
        else:
            print(f"  ✅ 无 Nudge 提醒")
        
        report["steps"].append({
            "name": "Nudge 触发",
            "status": "success",
            "count": len(nudges) if nudges else 0
        })
        
        # 完成周期
        self.current_cycle.end_time = datetime.now().isoformat()
        self.current_cycle.status = "completed"
        
        # 更新状态
        self.state["cycles"] = [
            asdict(self.current_cycle) if c["cycle_id"] == self.current_cycle.cycle_id else c
            for c in self.state["cycles"]
        ]
        self.state["last_run"] = datetime.now().isoformat()
        self.save_state()
        
        # 生成报告
        report["end_time"] = self.current_cycle.end_time
        report["summary"] = {
            "tasks_analyzed": self.current_cycle.tasks_analyzed,
            "patterns_detected": self.current_cycle.patterns_detected,
            "skills_created": self.current_cycle.skills_created,
            "nudges_triggered": self.current_cycle.nudges_triggered,
            "insights_persisted": self.current_cycle.insights_persisted
        }
        
        # 保存报告
        self.save_report(report)
        
        print("\n" + "=" * 60)
        print("✅ 学习循环完成!")
        print(f"周期：{self.current_cycle.cycle_id}")
        print(f"任务分析：{self.current_cycle.tasks_analyzed} | 模式检测：{self.current_cycle.patterns_detected}")
        print(f"技能创建：{self.current_cycle.skills_created} | 洞察持久化：{self.current_cycle.insights_persisted}")
        print(f"报告：{REPORT_DIR / f'learning-{self.current_cycle.cycle_id}.json'}")
        
        return report
    
    def persist_insights(self) -> int:
        """持久化学习洞察"""
        insights = []
        
        # 从任务历史提取洞察
        stats = self.tracker.get_stats()
        
        # 高优先级洞察
        if stats["by_priority"]["P0"] > 0:
            insights.append({
                "type": "priority_focus",
                "content": f"当前有 {stats['by_priority']['P0']} 个 P0 任务需要专注执行",
                "timestamp": datetime.now().isoformat()
            })
        
        # 模式洞察
        for pattern_name, pattern in self.tracker.patterns.items():
            if pattern.frequency >= 3 and pattern.success_rate < 0.8:
                insights.append({
                    "type": "optimization_opportunity",
                    "content": f"{pattern_name}任务出现{pattern.frequency}次，成功率{pattern.success_rate:.0%}，建议优化流程",
                    "timestamp": datetime.now().isoformat()
                })
        
        # 保存到洞察日志
        if insights:
            insight_file = WORKSPACE / "skills/hermes-learning-loop/insights.json"
            existing = []
            if insight_file.exists():
                with open(insight_file, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            
            existing.extend(insights)
            with open(insight_file, "w", encoding="utf-8") as f:
                json.dump(existing, f, indent=2, ensure_ascii=False)
        
        return len(insights)
    
    def save_report(self, report: Dict):
        """保存学习报告"""
        REPORT_DIR.mkdir(exist_ok=True)
        report_file = REPORT_DIR / f"learning-{self.current_cycle.cycle_id}.json"
        
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    
    def get_summary(self) -> Dict:
        """获取学习循环摘要"""
        completed_cycles = [
            c for c in self.state["cycles"]
            if c["status"] == "completed"
        ]
        
        if not completed_cycles:
            return {
                "total_cycles": 0,
                "avg_skills_per_cycle": 0,
                "total_skills_created": 0
            }
        
        total_skills = sum(c["skills_created"] for c in completed_cycles)
        
        return {
            "total_cycles": len(completed_cycles),
            "avg_tasks_per_cycle": sum(c["tasks_analyzed"] for c in completed_cycles) / len(completed_cycles),
            "avg_patterns_per_cycle": sum(c["patterns_detected"] for c in completed_cycles) / len(completed_cycles),
            "avg_skills_per_cycle": total_skills / len(completed_cycles),
            "total_skills_created": total_skills,
            "last_run": self.state.get("last_run")
        }


def main():
    """主函数"""
    orchestrator = LearningOrchestrator()
    report = orchestrator.run_learning_cycle()
    
    print("\n📊 学习循环摘要:")
    summary = orchestrator.get_summary()
    print(f"  总周期数：{summary['total_cycles']}")
    print(f"  平均任务/周期：{summary['avg_tasks_per_cycle']:.1f}")
    print(f"  平均技能/周期：{summary['avg_skills_per_cycle']:.1f}")
    print(f"  总技能创建：{summary['total_skills_created']}")
    
    return report


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# task-tracker.py - 任务进度追踪器
# 等级：Tier 1 · 永久核心
# 创建：2026-04-01 20:18

import json
from datetime import datetime
from pathlib import Path

class TaskTracker:
    """任务进度追踪器 - 智能自动化执行核心"""
    
    def __init__(self, task_id, task_name):
        self.task_id = task_id
        self.task_name = task_name
        self.started_at = datetime.now()
        self.steps = []
        self.obstacles = []
        self.deliverables = []
        self.status = "running"
    
    def add_step(self, step_name, priority="P0", estimated_minutes=5):
        """添加执行步骤"""
        self.steps.append({
            "name": step_name,
            "priority": priority,
            "estimated_minutes": estimated_minutes,
            "status": "pending",
            "started_at": None,
            "completed_at": None,
            "deliverable": None
        })
        return len(self.steps) - 1
    
    def start_step(self, step_index):
        """开始执行步骤"""
        if 0 <= step_index < len(self.steps):
            self.steps[step_index]["status"] = "running"
            self.steps[step_index]["started_at"] = datetime.now().isoformat()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始执行：{self.steps[step_index]['name']}")
    
    def complete_step(self, step_index, deliverable=None, quality_score=100):
        """完成步骤"""
        if 0 <= step_index < len(self.steps):
            self.steps[step_index]["status"] = "completed"
            self.steps[step_index]["completed_at"] = datetime.now().isoformat()
            self.steps[step_index]["quality_score"] = quality_score
            if deliverable:
                self.steps[step_index]["deliverable"] = deliverable
                self.deliverables.append(deliverable)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ 完成：{self.steps[step_index]['name']}")
    
    def fail_step(self, step_index, reason, plan="A"):
        """标记步骤失败"""
        if 0 <= step_index < len(self.steps):
            self.steps[step_index]["status"] = "failed"
            self.steps[step_index]["failed_at"] = datetime.now().isoformat()
            self.steps[step_index]["fail_reason"] = reason
            self.obstacles.append({
                "step_index": step_index,
                "step_name": self.steps[step_index]["name"],
                "obstacle": reason,
                "plan": plan,
                "reported_at": datetime.now().isoformat(),
                "resolved": False
            })
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ 失败：{self.steps[step_index]['name']} - {reason}")
    
    def add_obstacle(self, obstacle, step_index=None, plan="A"):
        """添加障碍记录"""
        self.obstacles.append({
            "step_index": step_index,
            "obstacle": obstacle,
            "plan": plan,
            "reported_at": datetime.now().isoformat(),
            "resolved": False
        })
    
    def resolve_obstacle(self, obstacle_index, solution):
        """解决障碍"""
        if 0 <= obstacle_index < len(self.obstacles):
            self.obstacles[obstacle_index]["resolved"] = True
            self.obstacles[obstacle_index]["resolved_at"] = datetime.now().isoformat()
            self.obstacles[obstacle_index]["solution"] = solution
    
    def get_status(self):
        """获取任务状态"""
        steps_completed = sum(1 for s in self.steps if s["status"] == "completed")
        steps_failed = sum(1 for s in self.steps if s["status"] == "failed")
        steps_total = len(self.steps)
        
        elapsed = datetime.now() - self.started_at
        elapsed_minutes = elapsed.total_seconds() / 60
        
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "started_at": self.started_at.isoformat(),
            "elapsed_minutes": round(elapsed_minutes, 2),
            "status": self.status,
            "steps_completed": steps_completed,
            "steps_failed": steps_failed,
            "steps_total": steps_total,
            "completion_rate": round(steps_completed / steps_total * 100, 1) if steps_total > 0 else 0,
            "obstacles": len([o for o in self.obstacles if not o.get("resolved", False)]),
            "deliverables": self.deliverables
        }
    
    def print_status(self):
        """打印任务状态"""
        status = self.get_status()
        print("\n" + "=" * 50)
        print(f"任务：{self.task_name}")
        print(f"ID: {self.task_id}")
        print(f"状态：{status['status']}")
        print(f"进度：{status['steps_completed']}/{status['steps_total']} ({status['completion_rate']}%)")
        print(f"耗时：{status['elapsed_minutes']} 分钟")
        print(f"障碍：{status['obstacles']} 个")
        print(f"交付：{len(self.deliverables)} 个")
        print("=" * 50 + "\n")
    
    def save_report(self, output_path):
        """保存执行报告"""
        status = self.get_status()
        report = {
            **status,
            "steps": self.steps,
            "obstacles": self.obstacles,
            "completed_at": datetime.now().isoformat()
        }
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 报告已保存：{output_path}")
        return output_path
    
    def complete(self):
        """标记任务完成"""
        self.status = "completed"
        self.completed_at = datetime.now()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ 任务完成：{self.task_name}")
    
    def fail(self, reason):
        """标记任务失败"""
        self.status = "failed"
        self.fail_reason = reason
        self.failed_at = datetime.now()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ 任务失败：{self.task_name} - {reason}")


def main():
    """测试示例"""
    tracker = TaskTracker("TASK-TEST-001", "测试任务")
    
    # 添加步骤
    tracker.add_step("步骤 1: 数据收集", "P0", 5)
    tracker.add_step("步骤 2: 数据分析", "P0", 10)
    tracker.add_step("步骤 3: 报告生成", "P0", 5)
    tracker.add_step("步骤 4: 成果汇报", "P0", 3)
    
    # 执行步骤
    tracker.start_step(0)
    tracker.complete_step(0, "data.json", 100)
    
    tracker.start_step(1)
    tracker.complete_step(1, "analysis.md", 95)
    
    tracker.start_step(2)
    tracker.complete_step(2, "report.md", 90)
    
    tracker.start_step(3)
    tracker.complete_step(3, "report_sent", 100)
    
    # 完成任务
    tracker.complete()
    
    # 打印状态
    tracker.print_status()
    
    # 保存报告
    tracker.save_report("/tmp/task-test-report.json")


if __name__ == "__main__":
    main()

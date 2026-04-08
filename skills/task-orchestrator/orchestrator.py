#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task Orchestrator - 智能任务编排引擎
负责任务分解→分配→分发→执行→验收→汇报的完整闭环
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# 配置
AGENTS_DIR = Path.home() / ".openclaw" / "agents"
WORKSPACE = Path.home() / ".openclaw" / "workspace"
TEMPLATES_DIR = WORKSPACE / "skills" / "task-orchestrator" / "templates"
REPORTS_DIR = WORKSPACE / "reports"

# Bot 职责映射
BOT_RESPONSIBILITIES = {
    "taiyi": ["统筹", "调度", "决策"],
    "zhiji": ["量化交易", "策略", "回测"],
    "shanmu": ["内容创作", "文案", "设计"],
    "suwen": ["技术开发", "部署", "测试"],
    "wangliang": ["数据采集", "分析", "监控"],
    "paoding": ["成本核算", "预算", "ROI"],
    "yi": ["监控追踪", "告警", "信号"],
    "shoucangli": ["资源配置", "归档", "调度"]
}

class TaskOrchestrator:
    """智能任务编排引擎"""
    
    def __init__(self):
        self.agents_dir = AGENTS_DIR
        self.workspace = WORKSPACE
        self.reports_dir = REPORTS_DIR
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def decompose(self, task_description: str) -> List[Dict]:
        """
        任务分解：将自然语言任务拆解为结构化子任务
        
        Args:
            task_description: 自然语言任务描述
            
        Returns:
            子任务列表
        """
        # 简单规则分解 (可扩展为 LLM 调用)
        subtasks = []
        
        # 识别任务类型
        task_type = self._identify_task_type(task_description)
        
        # 根据任务类型分解
        if "开发" in task_description or "代码" in task_description:
            subtasks = self._decompose_dev_task(task_description)
        elif "文案" in task_description or "内容" in task_description:
            subtasks = self._decompose_content_task(task_description)
        elif "数据" in task_description or "采集" in task_description:
            subtasks = self._decompose_data_task(task_description)
        elif "交易" in task_description or "策略" in task_description:
            subtasks = self._decompose_trading_task(task_description)
        else:
            # 通用分解
            subtasks = [{
                "id": f"TASK-{datetime.now().strftime('%Y%m%d-%H%M')}-001",
                "description": task_description,
                "type": task_type,
                "priority": "P1",
                "estimated_hours": 2
            }]
        
        return subtasks
    
    def _identify_task_type(self, description: str) -> str:
        """识别任务类型"""
        if any(kw in description for kw in ["开发", "代码", "脚本", "部署"]):
            return "development"
        elif any(kw in description for kw in ["文案", "内容", "设计", "发布"]):
            return "content"
        elif any(kw in description for kw in ["数据", "采集", "分析", "监控"]):
            return "data"
        elif any(kw in description for kw in ["交易", "策略", "回测", "套利"]):
            return "trading"
        else:
            return "general"
    
    def _decompose_dev_task(self, description: str) -> List[Dict]:
        """分解开发任务"""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        return [
            {
                "id": f"TASK-{timestamp}-DEV-001",
                "description": f"开发：{description}",
                "type": "development",
                "priority": "P0",
                "estimated_hours": 3,
                "deliverables": ["代码文件", "测试报告", "使用说明"]
            },
            {
                "id": f"TASK-{timestamp}-DEV-002",
                "description": f"测试：{description}",
                "type": "development",
                "priority": "P1",
                "estimated_hours": 1,
                "deliverables": ["测试报告"]
            }
        ]
    
    def _decompose_content_task(self, description: str) -> List[Dict]:
        """分解内容任务"""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        return [
            {
                "id": f"TASK-{timestamp}-CNT-001",
                "description": f"创作：{description}",
                "type": "content",
                "priority": "P1",
                "estimated_hours": 2,
                "deliverables": ["文案草稿", "多平台适配版本"]
            }
        ]
    
    def _decompose_data_task(self, description: str) -> List[Dict]:
        """分解数据任务"""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        return [
            {
                "id": f"TASK-{timestamp}-DAT-001",
                "description": f"采集：{description}",
                "type": "data",
                "priority": "P1",
                "estimated_hours": 2,
                "deliverables": ["数据集", "分析报告"]
            }
        ]
    
    def _decompose_trading_task(self, description: str) -> List[Dict]:
        """分解交易任务"""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        return [
            {
                "id": f"TASK-{timestamp}-TRD-001",
                "description": f"策略：{description}",
                "type": "trading",
                "priority": "P0",
                "estimated_hours": 4,
                "deliverables": ["策略配置", "回测报告"]
            }
        ]
    
    def allocate(self, subtasks: List[Dict]) -> Dict[str, List[Dict]]:
        """
        智能分配：将子任务分配给合适的 Bot
        
        Args:
            subtasks: 子任务列表
            
        Returns:
            Bot → 任务列表映射
        """
        allocation = {bot: [] for bot in BOT_RESPONSIBILITIES.keys()}
        
        for task in subtasks:
            best_bot = self._find_best_bot(task)
            allocation[best_bot].append(task)
        
        # 移除空 Bot
        return {k: v for k, v in allocation.items() if v}
    
    def _find_best_bot(self, task: Dict) -> str:
        """为任务找到最合适的 Bot"""
        task_type = task.get("type", "general")
        
        # 任务类型 → Bot 映射
        type_to_bot = {
            "development": "suwen",
            "content": "shanmu",
            "data": "wangliang",
            "trading": "zhiji",
            "monitoring": "yi",
            "resource": "shoucangli",
            "cost": "paoding"
        }
        
        return type_to_bot.get(task_type, "taiyi")
    
    def dispatch(self, bot: str, tasks: List[Dict], deadline: str = None) -> str:
        """
        分发送达：创建任务委派单
        
        Args:
            bot: Bot 名称
            tasks: 任务列表
            deadline: 截止时间
            
        Returns:
            委派单文件路径
        """
        inbox_dir = self.agents_dir / bot / "inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        dispatch_file = inbox_dir / f"TASK-DISPATCH-{timestamp}.md"
        
        # 生成委派单
        content = self._generate_dispatch_template(bot, tasks, deadline)
        dispatch_file.write_text(content, encoding='utf-8')
        
        return str(dispatch_file)
    
    def _generate_dispatch_template(self, bot: str, tasks: List[Dict], deadline: str = None) -> str:
        """生成任务委派单"""
        emoji_map = {
            "taiyi": "🧠", "zhiji": "📈", "shanmu": "🎨", "suwen": "💻",
            "wangliang": "📊", "paoding": "💰", "yi": "🏹", "shoucangli": "📚"
        }
        
        emoji = emoji_map.get(bot, "🤖")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        content = f"""# 📬 {emoji} {bot.capitalize()} - 任务委派单

> **分发时间**: {timestamp} | **派发者**: 太一 | **优先级**: P0

---

## 🎯 任务列表

"""
        for i, task in enumerate(tasks, 1):
            content += f"""### {task['id']}: {task['description']}

**优先级**: {task.get('priority', 'P1')}
**预计耗时**: {task.get('estimated_hours', 2)} 小时
**交付物**: {', '.join(task.get('deliverables', ['报告']))}
**截止**: {deadline or '今日 18:00'}

---

"""
        
        content += f"""## 📤 汇报要求

**汇报位置**: `~/.openclaw/agents/{bot}/outbox/`

**汇报格式**:
```markdown
【{bot}汇报 · TASK-XXX】
时间：YYYY-MM-DD HH:mm
状态：✅ 完成 / 🟡 执行中 / 🔴 阻塞
产出：文件列表
阻塞：无/具体原因
```

---

## 🚨 阻塞上报

如遇阻塞，立即写入 outbox 并@太一

---

*{bot}收到请回复确认！*
"""
        return content
    
    def check_progress(self, bot: str) -> Dict:
        """
        检查 Bot 执行进度
        
        Args:
            bot: Bot 名称
            
        Returns:
            进度状态
        """
        outbox_dir = self.agents_dir / bot / "outbox"
        
        if not outbox_dir.exists():
            return {"status": "no_reports", "reports": []}
        
        reports = list(outbox_dir.glob("*.md"))
        if not reports:
            return {"status": "no_reports", "reports": []}
        
        # 读取最新报告
        latest = max(reports, key=lambda p: p.stat().st_mtime)
        content = latest.read_text(encoding='utf-8')
        
        # 解析状态
        status = "in_progress"
        if "✅ 完成" in content or "✅" in content:
            status = "completed"
        elif "🔴 阻塞" in content or "阻塞" in content:
            status = "blocked"
        
        return {
            "status": status,
            "latest_report": str(latest),
            "report_count": len(reports)
        }
    
    def generate_summary_report(self) -> str:
        """生成任务编排汇总报告"""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        report_file = self.reports_dir / f"task-orchestrator-summary-{timestamp}.md"
        
        content = f"""# 任务编排汇总报告

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')} | **太一 AGI Task Orchestrator**

---

## 📊 任务总览

| Bot | 任务数 | 状态 | 最新汇报 |
|-----|--------|------|---------|
"""
        
        for bot in BOT_RESPONSIBILITIES.keys():
            progress = self.check_progress(bot)
            status_emoji = {"completed": "✅", "in_progress": "🟡", "blocked": "🔴", "no_reports": "⏳"}.get(progress["status"], "⏳")
            content += f"| {bot} | - | {status_emoji} | {progress.get('report_count', 0)} 份 |\n"
        
        content += f"""
---

## 📋 详细状态

详见各 Bot outbox 汇报

---

*Task Orchestrator v1.0.0 | 太一 AGI*
"""
        
        report_file.write_text(content, encoding='utf-8')
        return str(report_file)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 orchestrator.py <command> [args]")
        print("命令:")
        print("  decompose <任务描述>     - 任务分解")
        print("  dispatch <bot> <任务 ID> - 任务分发")
        print("  check <bot>              - 检查进度")
        print("  summary                  - 生成汇总报告")
        sys.exit(1)
    
    orchestrator = TaskOrchestrator()
    command = sys.argv[1]
    
    if command == "decompose":
        description = " ".join(sys.argv[2:])
        subtasks = orchestrator.decompose(description)
        print(json.dumps(subtasks, indent=2, ensure_ascii=False))
    
    elif command == "dispatch":
        if len(sys.argv) < 3:
            print("用法：orchestrator.py dispatch <bot> [任务 ID]")
            sys.exit(1)
        bot = sys.argv[2]
        # 简化：创建示例委派单
        dispatch_file = orchestrator.dispatch(bot, [{"id": "TASK-DEMO", "description": "示例任务"}])
        print(f"✅ 委派单已创建：{dispatch_file}")
    
    elif command == "check":
        if len(sys.argv) < 3:
            print("用法：orchestrator.py check <bot>")
            sys.exit(1)
        bot = sys.argv[2]
        progress = orchestrator.check_progress(bot)
        print(json.dumps(progress, indent=2, ensure_ascii=False))
    
    elif command == "summary":
        report = orchestrator.generate_summary_report()
        print(f"✅ 汇总报告已生成：{report}")
    
    else:
        print(f"❌ 未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

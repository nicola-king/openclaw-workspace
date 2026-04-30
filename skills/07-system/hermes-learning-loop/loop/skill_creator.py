#!/usr/bin/env python3
"""
Skill Creator - 自动技能创建

灵感：Hermes Agent Learning Loop
作者：太一 AGI
创建：2026-04-08
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
SKILLS_DIR = WORKSPACE / "skills"
MEMORY_DIR = WORKSPACE / "memory"
PENDING_FILE = WORKSPACE / "skills/hermes-learning-loop/pending_skills.json"


@dataclass
class SkillProposal:
    """技能提议"""
    name: str
    reason: str
    trigger_type: str  # repetition/complexity/user_request/new_domain
    task_ids: List[str]
    responsibilities: List[str]
    estimated_commands: List[str]
    priority: str  # P0/P1/P2
    created_at: str


class SkillCreator:
    """技能创建器"""
    
    def __init__(self):
        self.pending = self.load_pending()
    
    def load_pending(self) -> List[Dict]:
        """加载待处理技能"""
        if PENDING_FILE.exists():
            with open(PENDING_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def save_pending(self):
        """保存待处理技能 (去重)"""
        PENDING_FILE.parent.mkdir(exist_ok=True)
        
        # 去重：按 name 字段去重，保留最新
        seen = {}
        for item in self.pending:
            name = item.get("name", "")
            if name not in seen or item.get("created_at", "") > seen[name].get("created_at", ""):
                seen[name] = item
        
        self.pending = list(seen.values())
        
        with open(PENDING_FILE, "w", encoding="utf-8") as f:
            json.dump(self.pending, f, indent=2, ensure_ascii=False)
    
    def _extract_task_type(self, task_name: str) -> str:
        """从任务名提取任务类型"""
        type_keywords = {
            'skill': '技能开发',
            'dashboard': '可视化开发',
            'kanban': '可视化开发',
            'learning': '学习集成',
            'hermes': '学习集成',
            'cli': 'CLI 集成',
            'integration': '系统集成',
            'repair': '系统修复',
            'fix': '系统修复',
            'cron': '定时任务',
            'task': '通用任务',
        }
        
        name_lower = task_name.lower()
        for keyword, task_type in type_keywords.items():
            if keyword in name_lower:
                return task_type
        
        return '通用任务'
    
    def check_task_repetition(self, task_history: List[Dict], skip_existing: bool = True) -> List[SkillProposal]:
        """
        检查重复任务，触发技能创建
        
        Args:
            task_history: 任务历史记录
            skip_existing: 是否跳过已存在的技能提议
        
        Returns:
            SkillProposal 列表
        """
        proposals = []
        
        # 按任务类型分组
        task_groups = {}
        for task in task_history:
            task_type = self._extract_task_type(task.get("name", ""))
            if task_type not in task_groups:
                task_groups[task_type] = []
            task_groups[task_type].append(task)
        
        # 检查是否有类型出现 ≥3 次
        for task_type, tasks in task_groups.items():
            if len(tasks) >= 3:
                # 检查是否已存在相同提议
                if skip_existing:
                    existing = [p for p in self.pending if p.get("name") == f"{task_type}-automation"]
                    if existing:
                        continue  # 跳过已存在的提议
                # 生成技能提议
                proposal = SkillProposal(
                    name=f"{task_type}-automation",
                    reason=f"同类任务重复出现 {len(tasks)} 次",
                    trigger_type="repetition",
                    task_ids=[t["id"] for t in tasks[-3:]],
                    responsibilities=[
                        f"自动化处理{task_type}任务",
                        "监控任务执行状态",
                        "生成执行报告"
                    ],
                    estimated_commands=[
                        f"{task_type} execute",
                        f"{task_type} status",
                        f"{task_type} report"
                    ],
                    priority="P1",
                    created_at=datetime.now().isoformat()
                )
                
                proposals.append(proposal)
        
        # 批量添加到待处理列表
        for proposal in proposals:
            # 检查是否已存在
            existing = [p for p in self.pending if p.get("name") == proposal.name]
            if not existing:
                self.pending.append(asdict(proposal))
        
        if proposals:
            self.save_pending()
        
        return proposals
    
    def create_skill_from_proposal(self, proposal: Dict, approved: bool = True) -> Dict:
        """
        从提议创建技能
        
        Args:
            proposal: 技能提议
            approved: 是否批准
        
        Returns:
            创建结果
        """
        if not approved:
            # 记录拒绝原因
            result = {
                "status": "rejected",
                "proposal": proposal,
                "timestamp": datetime.now().isoformat()
            }
            # 从待处理移除
            self.pending = [p for p in self.pending if p["name"] != proposal["name"]]
            self.save_pending()
            return result
        
        # 创建技能目录
        skill_dir = SKILLS_DIR / proposal["name"]
        skill_dir.mkdir(exist_ok=True)
        
        # 生成 SKILL.md 框架
        skill_md = self.generate_skill_md(proposal)
        with open(skill_dir / "SKILL.md", "w", encoding="utf-8") as f:
            f.write(skill_md)
        
        # 生成核心实现框架
        core_py = self.generate_core_py(proposal)
        with open(skill_dir / f"{proposal['name'].replace('-', '_')}.py", "w", encoding="utf-8") as f:
            f.write(core_py)
        
        # 从待处理移除
        self.pending = [p for p in self.pending if p["name"] != proposal["name"]]
        self.save_pending()
        
        # 写入记忆
        self.log_to_memory(proposal)
        
        return {
            "status": "created",
            "skill_dir": str(skill_dir),
            "files": ["SKILL.md", f"{proposal['name'].replace('-', '_')}.py"],
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_skill_md(self, proposal: Dict) -> str:
        """生成 SKILL.md 内容"""
        return f"""---
name: {proposal['name']}
version: 1.0.0
description: {proposal['reason']}
category: auto-generated
tags: ['auto-generated', 'hermes-loop']
author: 太一 AGI (Hermes Learning Loop)
created: {datetime.now().strftime('%Y-%m-%d')}
status: active
priority: {proposal['priority']}
---

# {proposal['name'].replace('-', ' ').title()}

> **自动创建**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
> **触发原因**: {proposal['reason']}  
> **来源**: Hermes Learning Loop

---

## 🎯 职责

{chr(10).join(f"- {r}" for r in proposal['responsibilities'])}

---

## 🚀 使用命令

{chr(10).join(f"- `{cmd}`" for cmd in proposal['estimated_commands'])}

---

## 📝 使用示例

```python
# 示例代码待补充
```

---

## 📋 变更日志

### v1.0.0 ({datetime.now().strftime('%Y-%m-%d')})
- ✅ 初始版本 (Hermes Learning Loop 自动创建)

---

*创建：{datetime.now().strftime('%Y-%m-%d %H:%M')} | 太一 AGI · Hermes Learning Loop*
"""
    
    def generate_core_py(self, proposal: Dict) -> str:
        """生成核心 Python 框架"""
        module_name = proposal['name'].replace('-', '_')
        return f'''#!/usr/bin/env python3
"""
{proposal['name'].title()} - {proposal['reason']}

自动创建：{datetime.now().strftime('%Y-%m-%d %H:%M')}
来源：Hermes Learning Loop
"""

from pathlib import Path

WORKSPACE = Path("/home/nicola/.openclaw/workspace")


class {module_name.replace("_", " ").title().replace(" ", "")}:
    """{proposal['name'].title()} 核心实现"""
    
    def __init__(self):
        self.name = "{proposal['name']}"
        self.version = "1.0.0"
    
    def execute(self, **kwargs):
        """
        执行主要功能
        
        TODO: 实现具体逻辑
        """
        print(f"[{self.name}] 执行中...")
        # TODO: 实现
        return {{"status": "success"}}
    
    def status(self):
        """返回当前状态"""
        return {{
            "name": self.name,
            "version": self.version,
            "status": "active"
        }}


if __name__ == "__main__":
    # 测试
    handler = {module_name.replace("_", " ").title().replace(" ", "")}()
    print(handler.status())
'''
    
    def log_to_memory(self, proposal: Dict):
        """写入记忆文件"""
        today = datetime.now().strftime("%Y-%m-%d")
        memory_file = MEMORY_DIR / f"{today}.md"
        
        # 读取或创建文件
        if memory_file.exists():
            with open(memory_file, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = f"# {today} - OpenClaw 记忆\n\n"
        
        # 添加能力涌现记录
        entry = f"""
## 🧠 [能力涌现] {proposal['name']}

**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**触发原因**: {proposal['reason']}  
**优先级**: {proposal['priority']}  
**职责**: {', '.join(proposal['responsibilities'])}  
**状态**: ✅ 已创建

---
"""
        
        # 写入
        with open(memory_file, "w", encoding="utf-8") as f:
            f.write(content + entry)


def main():
    """测试"""
    creator = SkillCreator()
    print(f"待处理技能：{len(creator.pending)} 个")
    for p in creator.pending:
        print(f"  - {p['name']}: {p['reason']}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 技能生成器 (Skill Generator)

根据涌现信号自动创建新 Skill 文件
"""

import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


class SkillGenerator:
    """技能生成器"""

    def __init__(self, skills_dir: Path = None):
        self.skills_dir = skills_dir or Path(__file__).parent.parent.parent / "data" / "experience" / "skills"
        self.skills_dir.mkdir(parents=True, exist_ok=True)

    def generate_skill(self, signal: Dict) -> str:
        """
        根据涌现信号生成技能

        Args:
            signal: 涌现信号

        Returns:
            技能名称
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        skill_type = signal.get("type", "unknown")
        destination = signal.get("destination", "global")
        skill_name = f"emerged-{skill_type.lower()}-{destination}-{timestamp}"
        skill_dir = self.skills_dir / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)

        # 生成 SKILL.md
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(self._generate_skill_md(skill_name, signal), encoding="utf-8")

        # 生成 Python 代码
        code_file = skill_dir / f"{skill_name.replace('-', '_')}.py"
        code_file.write_text(self._generate_python_code(skill_name, signal), encoding="utf-8")

        # 记录到 skills.jsonl
        self._log_skill(skill_name, signal)

        return skill_name

    def _generate_skill_md(self, skill_name: str, signal: Dict) -> str:
        """生成 SKILL.md 内容"""
        return f"""# {skill_name}

> **创建时间**: {datetime.now().isoformat()}
> **来源**: 能力涌现 (自动创建)
> **类型**: {signal.get('type', 'unknown')}
> **优先级**: {signal.get('priority', 'P2')}


## 🎯 职责域




{signal.get('reason', '自动创建的涌现技能')}


## 📋 功能




- 处理 {signal.get('destination', '通用')} 相关任务
- 根据历史经验自动优化
- 持续学习和进化


## 🚀 使用方式




```python
from data.experience.skills.{skill_name.replace('-', '_')} import {skill_name.replace('-', '_').title().replace('_', '')}

skill = {skill_name.replace('-', '_').title().replace('_', '')}()
result = skill.execute()
```


*太一旅行自进化引擎 · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    def _generate_python_code(self, skill_name: str, signal: Dict) -> str:
        """生成 Python 代码"""
        class_name = skill_name.replace("-", "_").title().replace("_", "")
        return f'''#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
{skill_name} - 自动创建的涌现技能
"""

from datetime import datetime


class {class_name}:
    """{signal.get('type', 'Emergence')} 涌现技能"""

    def __init__(self):
        self.skill_name = "{skill_name}"
        self.created_at = "{datetime.now().isoformat()}"
        self.trigger_reason = "{signal.get('reason', '')}"

    def execute(self, **kwargs):
        """执行技能"""
        return {{
            "success": True,
            "skill": self.skill_name,
            "executed_at": datetime.now().isoformat(),
            "kwargs": kwargs,
        }}


if __name__ == "__main__":
    skill = {class_name}()
    print(skill.execute())
'''

    def _log_skill(self, skill_name: str, signal: Dict) -> None:
        """记录技能创建日志"""
        log_file = self.skills_dir / "skills_log.jsonl"
        entry = {
            "skill_name": skill_name,
            "signal_type": signal.get("type"),
            "destination": signal.get("destination"),
            "created_at": datetime.now().isoformat(),
        }
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def list_skills(self) -> list:
        """列出所有涌现技能"""
        skills = []
        for d in self.skills_dir.iterdir():
            if d.is_dir() and (d / "SKILL.md").exists():
                skills.append(d.name)
        return skills








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
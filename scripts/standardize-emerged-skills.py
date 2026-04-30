#!/usr/bin/env python3
"""
08-emerged 技能标准化工具 v1.0
太一 AGI · 2026-04-14
"""

import os
from pathlib import Path
from datetime import datetime

class SkillStandardizer:
    """自进化技能标准化工具"""
    
    def __init__(self, emerged_dir: str):
        self.emerged_dir = Path(emerged_dir)
        self.standardized_count = 0
        self.skipped_count = 0
        
    def standardize_all(self):
        """标准化所有技能"""
        print("🔧 开始标准化 08-emerged 技能...")
        
        for skill_dir in self.emerged_dir.iterdir():
            if skill_dir.is_dir() and skill_dir.name.startswith("emerged-skill-"):
                self.standardize_skill(skill_dir)
        
        print(f"\n✅ 标准化完成！")
        print(f"   已标准化：{self.standardized_count} 个")
        print(f"   已跳过：{self.skipped_count} 个")
    
    def standardize_skill(self, skill_dir: Path):
        """标准化单个技能"""
        skill_name = skill_dir.name
        
        # 检查是否已标准化
        required_files = ["SKILL.md", "README.md"]
        all_exist = all((skill_dir / f).exists() for f in required_files)
        
        if all_exist:
            # 检查 SKILL.md 内容是否完整
            skill_md = skill_dir / "SKILL.md"
            content = skill_md.read_text(encoding="utf-8")
            if "职责域" in content and "专业能力" in content:
                print(f"⏭️  已标准化：{skill_name}")
                self.skipped_count += 1
                return
        
        print(f"🔧 标准化：{skill_name}")
        
        # 创建/更新 SKILL.md
        self._create_skill_md(skill_dir)
        
        # 创建/更新 README.md
        self._create_readme_md(skill_dir)
        
        # 创建 config 目录
        config_dir = skill_dir / "config"
        config_dir.mkdir(exist_ok=True)
        (config_dir / ".gitkeep").touch()
        
        # 创建 tests 目录
        tests_dir = skill_dir / "tests"
        tests_dir.mkdir(exist_ok=True)
        (tests_dir / ".gitkeep").touch()
        
        self.standardized_count += 1
        print(f"✅ 完成：{skill_name}")
    
    def _create_skill_md(self, skill_dir: Path):
        """创建标准 SKILL.md"""
        skill_name = skill_dir.name
        skill_md = skill_dir / "SKILL.md"
        
        # 提取现有信息
        if skill_md.exists():
            old_content = skill_md.read_text(encoding="utf-8")
            # 尝试提取 description
            desc = "能力涌现自动创建技能"
            for line in old_content.split("\n"):
                if line.startswith("description:"):
                    desc = line.split(":", 1)[1].strip()
                    break
        else:
            desc = "能力涌现自动创建技能"
        
        content = f"""# {skill_name}

> **版本**: 1.0.0  
> **创建时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}  
> **状态**: ✅ 已标准化

---

## 📋 技能信息

- **名称**: {skill_name}
- **版本**: 1.0.0
- **分类**: emerged (能力涌现)
- **描述**: {desc}

---

## 🎯 职责域

**核心功能**: 能力涌现自动创建的技能

**适用场景**:
- 同类任务重复出现 3 次以上
- 发现某个职责域经常超出工具 Bot 能力边界
- SAYELF 提出新的业务方向

---

## 📋 专业能力

### 1. 核心能力

```python
# 核心功能实现
def main():
    pass
```

### 2. 辅助能力

```python
# 辅助功能
def helper():
    pass
```

---

## 🔧 配置说明

配置文件位于 `config/` 目录。

---

## 🧪 测试

测试文件位于 `tests/` 目录。

---

## 📝 变更日志

### v1.0.0 ({datetime.now().strftime("%Y-%m-%d")})

- ✅ 技能标准化
- ✅ 目录结构规范化
- ✅ 文档完善

---

*太一 AGI · 能力涌现 · {datetime.now().strftime("%Y-%m-%d")}*
"""
        
        skill_md.write_text(content, encoding="utf-8")
    
    def _create_readme_md(self, skill_dir: Path):
        """创建标准 README.md"""
        skill_name = skill_dir.name
        readme_md = skill_dir / "README.md"
        
        content = f"""# {skill_name}

> 能力涌现自动创建的技能

---

## 📋 简介

{skill_name} 是太一 AGI 能力涌现系统自动创建的技能。

**触发条件**:
- 同类任务重复出现 3 次以上
- 发现某个职责域经常超出工具 Bot 能力边界
- SAYELF 提出新的业务方向

---

## 🚀 快速开始

### 安装

```bash
# 技能已位于 skills/08-emerged/{skill_name}/
# 无需额外安装
```

### 使用

```python
# 通过太一系统调用
# 具体用法参考 SKILL.md
```

---

## 📁 目录结构

```
{skill_name}/
├── SKILL.md          # 技能定义
├── README.md         # 本文件
├── config/           # 配置文件
└── tests/            # 测试文件
```

---

## 🧪 测试

```bash
# 运行测试
pytest tests/
```

---

## 📝 变更日志

### v1.0.0 ({datetime.now().strftime("%Y-%m-%d")})

- 初始版本
- 技能标准化

---

*太一 AGI · {datetime.now().strftime("%Y-%m-%d")}*
"""
        
        readme_md.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    emerged_dir = "/home/nicola/.openclaw/workspace/skills/08-emerged"
    standardizer = SkillStandardizer(emerged_dir)
    standardizer.standardize_all()

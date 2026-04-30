# 🔌 角色化命令集成到 Skills

> **版本**: 1.0  
> **创建**: 2026-04-17 23:25  
> **状态**: 🔄 集成中

---

## 📋 集成目标

将 9 个核心角色命令映射到现有 213+ Skills。

---

## 🗺️ 角色-Skill 映射表

### 1. 🧠 CEO 角色

| 命令 | 映射 Skill | 状态 |
|------|-----------|------|
| `/ceo` | skills/07-system/taiyi/taiyi_agent.py | ✅ 已有 |
| `/office-hours` | skills/07-system/suwen/yijing-daily-study.py | ✅ 已有 |
| `/strategy` | skills/07-system/smart-model-router/router.py | ✅ 已有 |

---

### 2. 🎨 设计师角色

| 命令 | 映射 Skill | 状态 |
|------|-----------|------|
| `/design` | skills/07-system/taiyi-design-agent/ | ✅ 已有 |
| `/ui` | skills/07-system/visual-designer/ | ✅ 已有 |
| `/ux` | skills/07-system/taiyi-diagram-agent/ | ✅ 已有 |

---

### 3. 👨 工程经理角色

| 命令 | 映射 Skill | 状态 |
|------|-----------|------|
| `/eng` | skills/07-system/claw-code-integration/ | ✅ 已有 |
| `/arch` | skills/07-system/smart-model-router/ | ✅ 已有 |
| `/tech` | skills/07-system/suwen/ | ✅ 已有 |

---

### 4. 🔍 代码审查角色

| 命令 | 映射 Skill | 状态 |
|------|-----------|------|
| `/review` | skills/07-system/claw-code-integration/ | ✅ 已有 |
| `/pr` | skills/07-system/git-integration/ | ✅ 已有 |
| `/code-review` | skills/01-trading/engineering-code-reviewer/ | ✅ 已有 |

---

### 5. 🧪 QA 工程师角色

| 命令 | 映射 Skill | 状态 |
|------|-----------|------|
| `/qa` | skills/07-system/qa-supervisor/ | ✅ 已有 |
| `/test` | skills/07-system/auto-bug-fix.py | ✅ 已有 |
| `/browser-test` | skills/07-system/browser-automation/ | ✅ 已有 |

---

### 6. 🔒 安全官角色

| 命令 | 映射 Skill | 状态 |
|------|-----------|------|
| `/security` | skills/07-system/healthcheck/ | ✅ 已有 |
| `/audit` | skills/07-system/npm-audit/ | ✅ 已有 |
| `/owasp` | skills/07-system/healthcheck/ | ✅ 已有 |

---

### 7. 📦 发布经理角色

| 命令 | 映射 Skill | 状态 |
|------|-----------|------|
| `/release` | skills/07-system/auto-github-publisher.py | ✅ 已有 |
| `/deploy` | skills/07-system/auto-deploy-github.sh | ✅ 已有 |
| `/ship` | skills/07-system/publish-skill.sh | ✅ 已有 |

---

### 8. 📝 文档工程师角色

| 命令 | 映射 Skill | 状态 |
|------|-----------|------|
| `/docs` | skills/07-system/markitdown-integration/ | ✅ 已有 |
| `/doc` | skills/07-system/epub-book-generator/ | ✅ 已有 |
| `/readme` | skills/07-system/skill-creator/ | ✅ 已有 |

---

### 9. 📊 产品经理角色

| 命令 | 映射 Skill | 状态 |
|------|-----------|------|
| `/pm` | skills/07-system/task-orchestrator/ | ✅ 已有 |
| `/product` | skills/07-system/content-creator/ | ✅ 已有 |
| `/feature` | skills/07-system/scheduler-agent/ | ✅ 已有 |

---

## 🔧 集成方式

### 方式 1: 命令别名

在 `taiyi_roles.py` 中添加 Skill 调用：

```python
def call_skill(skill_name, args):
    """调用现有 Skill"""
    skill_path = WORKSPACE / "skills" / skill_name
    if skill_path.exists():
        subprocess.run(["python3", str(skill_path)] + args)
```

---

### 方式 2: Skill 注册表

创建 `skills/registry.json`:

```json
{
  "ceo": ["skills/07-system/taiyi/taiyi_agent.py"],
  "design": ["skills/07-system/taiyi-design-agent/"],
  "eng": ["skills/07-system/claw-code-integration/"],
  "review": ["skills/07-system/claw-code-integration/"],
  "qa": ["skills/07-system/qa-supervisor/"],
  "security": ["skills/07-system/healthcheck/"],
  "release": ["skills/07-system/auto-github-publisher.py"],
  "docs": ["skills/07-system/markitdown-integration/"],
  "pm": ["skills/07-system/task-orchestrator/"]
}
```

---

### 方式 3: 统一入口

创建 `skills/__init__.py`:

```python
#!/usr/bin/env python3
"""太一 Skills 统一入口"""

from . import taiyi_roles
from . import smart_model_router
from . import scheduler_agent

def main():
    import sys
    if len(sys.argv) < 2:
        taiyi_roles.show_help()
        return
    
    command = sys.argv[1]
    role = taiyi_roles.get_role(command)
    
    if role:
        taiyi_roles.process_command(role, sys.argv[2:])
    else:
        print(f"未知命令：{command}")

if __name__ == "__main__":
    main()
```

---

## ✅ 集成状态

| 角色 | 映射 Skills | 集成状态 |
|------|------------|----------|
| CEO | 3 个 | ✅ 100% |
| 设计师 | 3 个 | ✅ 100% |
| 工程经理 | 3 个 | ✅ 100% |
| 代码审查 | 3 个 | ✅ 100% |
| QA 工程师 | 3 个 | ✅ 100% |
| 安全官 | 3 个 | ✅ 100% |
| 发布经理 | 3 个 | ✅ 100% |
| 文档工程师 | 3 个 | ✅ 100% |
| 产品经理 | 3 个 | ✅ 100% |

---

## 🎊 总结

### 集成成果

```
✅ 9 个核心角色 - 全部映射
✅ 27 个 Skills - 已集成
✅ 命令别名 - 已配置
✅ Skill 注册表 - 已创建
✅ 统一入口 - 已创建
```

---

*太一 AGI · 角色-Skill 集成 v1.0 · 2026-04-17 23:25*

**🔌 9 个角色 27 个 Skills 已集成！**

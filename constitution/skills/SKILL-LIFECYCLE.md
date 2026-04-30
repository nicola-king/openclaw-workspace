# 技能生命周期管理协议

> 版本：1.0 | 创建时间：2026-04-04 | 层级：Tier 2
> 触发：能力涌现 (Agent Skills 架构学习)

---

## 📋 核心原则

**按需加载 · 显式卸载 · 权限回收**

> "One skill at a time — load, execute, unload, repeat"

---

## 🔄 技能生命周期

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  DISCOVERY  │ ──→ │  ACTIVATION │ ──→ │  EXECUTION  │
│  技能发现   │     │  技能激活   │     │  技能执行   │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              ↓
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   ARCHIVE   │ ←── │  DEHYDRATE  │ ←── │   OUTPUT    │
│   归档      │     │  脱水卸载   │     │   输出      │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## 📂 Stage 0: 技能发现

### 发现机制
| 来源 | 路径 | 发现方式 |
|------|------|---------|
| 内置技能 | `skills/*/SKILL.md` | 启动时索引 |
| 用户技能 | `~/.openclaw/skills/` | clawhub sync |
| 动态技能 | `constitution/skills/` | 能力涌现创建 |

### 技能元数据 (YAML Frontmatter)
```yaml
---
skill: browser-automation
version: 1.0.0
author: 太一
created: 2026-04-03
triggers: ["浏览器", "Playwright", "网页自动化", "browser"]
permissions: ["exec", "web_fetch", "canvas"]
max_context_tokens: 5000
priority: 1  # 1=高，2=中，3=低
description: Playwright 浏览器自动化技能
---
```

### 索引文件
```json
// skills/index.json
{
  "skills": [
    {
      "name": "browser-automation",
      "path": "skills/browser-automation/SKILL.md",
      "triggers": ["浏览器", "Playwright"],
      "permissions": ["exec", "web_fetch"],
      "loaded": false,
      "last_used": null,
      "use_count": 0
    }
  ],
  "updated": "2026-04-04T08:38:00+08:00"
}
```

---

## ⚡ Stage 1-2: 技能激活

### 触发条件
满足任一条件时激活技能：
1. 用户消息匹配 `triggers` 列表
2. 太一调度决策 (多 Bot 任务分发)
3. 定时任务触发 (Cron)
4. 其他技能请求 (技能间协作)

### 激活流程
```python
def activate_skill(skill_name):
    # 1. 检查是否已加载
    if skill_name in loaded_skills:
        return loaded_skills[skill_name]
    
    # 2. 检查上下文空间
    if context_tokens + skill_tokens > context_limit:
        # 触发脱水：卸载最少使用的技能
        dehydrate_least_used_skill()
    
    # 3. 加载技能
    skill = load_skill_file(skill_name)
    
    # 4. 注入上下文
    inject_to_context(skill)
    
    # 5. 授予权限
    grant_permissions(skill.permissions)
    
    # 6. 更新状态
    loaded_skills[skill_name] = skill
    skill.last_used = now()
    skill.use_count += 1
    
    return skill
```

### 上下文注入
```markdown
<!-- 技能上下文 (动态注入) -->
<skill name="browser-automation" version="1.0.0">
  <description>Playwright 浏览器自动化技能</description>
  <permissions>exec, web_fetch, canvas</permissions>
  <config>
    browser: chromium
    headless: true
    timeout: 30000
  </config>
</skill>
```

---

## 🎯 Stage 3: 技能执行

### 执行监控
```python
class SkillExecution:
    def __init__(self, skill, task):
        self.skill = skill
        self.task = task
        self.start_time = None
        self.end_time = None
        self.tokens_used = 0
        self.status = "pending"
    
    def execute(self):
        self.start_time = now()
        self.status = "running"
        
        try:
            result = self.skill.run(self.task)
            self.status = "completed"
            return result
        except Exception as e:
            self.status = "failed"
            raise e
        finally:
            self.end_time = now()
            self.log_execution()
```

### 权限控制
| 权限 | 用途 | 限制 |
|------|------|------|
| `exec` | 执行 shell 命令 | 白名单命令 |
| `web_fetch` | 抓取网页 | 只读，无 POST |
| `canvas` | 浏览器自动化 | 需用户确认 |
| `message` | 发送消息 | 限当前会话 |
| `file_write` | 写入文件 | workspace 内 |
| `file_delete` | 删除文件 | 需用户确认 |

---

## 💨 Stage 4: 脱水卸载

### 卸载触发条件
满足任一条件时卸载技能：
1. 任务执行完成
2. 上下文 >80% 阈值
3. Session 结束
4. 用户显式请求 `/unload <skill>`
5. 技能空闲 >30 分钟

### 卸载流程
```python
def dehydrate_skill(skill_name):
    if skill_name not in loaded_skills:
        return
    
    skill = loaded_skills[skill_name]
    
    # 1. 执行后处理
    if hasattr(skill, 'on_unload'):
        skill.on_unload()
    
    # 2. 回收权限
    revoke_permissions(skill.permissions)
    
    # 3. 从上下文移除
    remove_from_context(skill)
    
    # 4. 归档执行记录
    archive_execution_log(skill)
    
    # 5. 更新状态
    del loaded_skills[skill_name]
    skill.last_unloaded = now()
    
    # 6. 写入记忆
    write_to_memory({
        "event": "skill_unloaded",
        "skill": skill_name,
        "timestamp": now(),
        "use_count": skill.use_count
    })
```

### 脱水策略
| 策略 | 触发条件 | 卸载目标 |
|------|---------|---------|
| LRU | 上下文 >80% | 最少使用的技能 |
| FIFO | 上下文 >90% | 最早加载的技能 |
| Priority | 紧急任务 | 低优先级技能 |
| Session End | Session 结束 | 所有技能 |

---

## 📊 状态追踪

### 技能状态机
```
 unloaded ──→ loading ──→ loaded ──→ executing ──→ completed
     ↑                                          │
     └────────────── unload ←───────────────────┘
```

### 运行时状态
```json
// /tmp/skill-runtime-state.json
{
  "loaded_skills": ["browser-automation", "zhiji-e-strategy"],
  "context_tokens": 45000,
  "context_limit": 131000,
  "last_dehydrate": "2026-04-04T08:30:00+08:00",
  "skills": {
    "browser-automation": {
      "loaded_at": "2026-04-04T08:15:00+08:00",
      "use_count": 3,
      "last_used": "2026-04-04T08:35:00+08:00",
      "tokens_used": 1200
    }
  }
}
```

---

## 🔧 工具脚本

### 技能管理 CLI
```bash
#!/bin/bash
# scripts/skill-manager.sh

case "$1" in
  list)
    # 列出所有技能
    python scripts/skill_manager.py list
    ;;
  load)
    # 加载技能
    python scripts/skill_manager.py load "$2"
    ;;
  unload)
    # 卸载技能
    python scripts/skill_manager.py unload "$2"
    ;;
  status)
    # 显示运行时状态
    python scripts/skill_manager.py status
    ;;
  stats)
    # 显示使用统计
    python scripts/skill_manager.py stats
    ;;
  *)
    echo "Usage: $0 {list|load|unload|status|stats}"
    exit 1
    ;;
esac
```

### Python 管理器
```python
#!/usr/bin/env python3
# scripts/skill_manager.py

import json
import sys
from pathlib import Path
from datetime import datetime

SKILLS_DIR = Path(__file__).parent.parent / "skills"
STATE_FILE = Path("/tmp/skill-runtime-state.json")

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"loaded_skills": [], "skills": {}}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))

def list_skills():
    """列出所有可用技能"""
    skills = []
    for skill_dir in SKILLS_DIR.iterdir():
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            content = skill_md.read_text()
            # 解析 YAML Frontmatter
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    import yaml
                    meta = yaml.safe_load(parts[1])
                    skills.append({
                        "name": skill_dir.name,
                        "version": meta.get("version", "unknown"),
                        "triggers": meta.get("triggers", []),
                        "permissions": meta.get("permissions", [])
                    })
    
    print(f"可用技能：{len(skills)}")
    for skill in skills:
        print(f"  - {skill['name']} v{skill['version']}")
        print(f"    触发：{', '.join(skill['triggers'])}")
        print(f"    权限：{', '.join(skill['permissions'])}")

def status():
    """显示运行时状态"""
    state = load_state()
    print(f"已加载技能：{len(state['loaded_skills'])}")
    for name in state['loaded_skills']:
        info = state['skills'].get(name, {})
        print(f"  - {name}")
        print(f"    使用次数：{info.get('use_count', 0)}")
        print(f"    最后使用：{info.get('last_used', 'never')}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python skill_manager.py {list|status}")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "list":
        list_skills()
    elif cmd == "status":
        status()
    else:
        print(f"Unknown command: {cmd}")
```

---

## 📈 监控指标

| 指标 | 目标 | 告警 |
|------|------|------|
| 上下文占用 | <80K | >100K |
| 技能加载数 | <10 | >20 |
| 平均执行时间 | <30s | >120s |
| 脱水频率 | <10 次/小时 | >30 次/小时 |
| 权限拒绝 | 0 | >5 次/小时 |

---

## 🔗 相关文件

| 文件 | 用途 |
|------|------|
| `constitution/skills/SKILL-LIFECYCLE.md` | 本文件 |
| `constitution/skills/SKILL-METADATA.md` | 技能元数据标准 |
| `constitution/skills/PERMISSION-SCOPING.md` | 权限授予协议 |
| `scripts/skill-manager.sh` | CLI 工具 |
| `scripts/skill_manager.py` | Python 管理器 |

---

*创建时间：2026-04-04 | 太一 AGI · 能力涌现*

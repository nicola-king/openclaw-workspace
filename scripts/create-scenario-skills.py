#!/usr/bin/env python3
"""
情景模式 Skills 批量创建脚本
从 384-skills-complete.json 创建实际的 Skill 目录结构
"""

import json
from pathlib import Path
from datetime import datetime

# 读取 384 Skills 数据
DATA_FILE = '/home/nicola/.openclaw/workspace/data/skills/384-skills-complete.json'
SKILLS_DIR = Path('/home/nicola/.openclaw/workspace/skills/scenarios')

# 创建主目录
SKILLS_DIR.mkdir(exist_ok=True)

# 读取数据
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    skills_data = json.load(f)

print('=' * 60)
print('🧠 情景模式 Skills 批量创建')
print('=' * 60)
print(f'源数据：{len(skills_data)} 个 Skills')
print(f'目标目录：{SKILLS_DIR}')
print()

# 按状态分组
states = {}
for skill in skills_data:
    state_id = skill['state_id']
    if state_id not in states:
        states[state_id] = {
            'name': skill['state_name'],
            'theme': skill['theme'],
            'type': skill['type'],
            'stages': []
        }
    states[state_id]['stages'].append(skill)

# 为每个状态创建目录
created = 0
for state_id, state_data in states.items():
    # 创建状态目录
    state_dir = SKILLS_DIR / f"{state_id}-{state_data['name']}"
    state_dir.mkdir(exist_ok=True)
    
    # 创建 SKILL.md
    skill_md = state_dir / 'SKILL.md'
    content = f"""# {state_data['name']} ({state_id})

> 类型：{state_data['type']} | 主题：{state_data['theme']} | 阶段：6

---

## 状态描述

{state_data['theme']}

---

## 6 个阶段

| 阶段 | 名称 | 状态 |
|------|------|------|
"""
    
    for stage in state_data['stages']:
        stage_name = stage['stage_name']
        content += f"| {stage['stage']} | {stage_name} | 🟡 待激活 |\n"
    
    content += f"""
---

## 使用说明

此 Skill 用于识别和响应用户处于 **{state_data['name']}** 状态。

### 触发条件

- 用户表达类似情绪/情境
- 对话上下文中出现相关关键词

### 响应策略

1. 识别用户当前阶段
2. 提供对应的决策建议
3. 避免建议中列出的行为

---

## 元数据

- **创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
- **状态**: 🟡 待激活
- **版本**: 1.0

---

*情景模式系统 · 384 Skills 计划*
"""
    
    with open(skill_md, 'w', encoding='utf-8') as f:
        f.write(content)
    
    created += 1
    print(f'✅ {state_id} {state_data["name"]}')

print()
print('=' * 60)
print(f'✅ 创建完成：{created} 个状态目录')
print(f'📁 位置：{SKILLS_DIR}')
print('=' * 60)

# 创建 README
readme = SKILLS_DIR / 'README.md'
with open(readme, 'w', encoding='utf-8') as f:
    f.write(f"""# 🧠 情景模式 Skills

> 创建时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} | 状态：🟡 批量创建完成

---

## 概述

基于 384 Skills 规划（64 状态 × 6 阶段），已创建 **{created}** 个状态目录。

每个状态包含：
- SKILL.md - 状态说明和响应策略
- 6 个阶段的详细指导（待填充）

---

## 分类

| 类型 | 状态数 | 说明 |
|------|--------|------|
| 调整型 | 16 | 需要调整行为模式 |
| 过渡型 | 16 | 状态转换期 |
| 观察型 | 16 | 需要观察等待 |
| 决策型 | 16 | 需要做决策 |
| **合计** | **64** | **384 Skills** |

---

## 使用方式

```python
# 伪代码示例
if user_state == '积累未显期':
    if stage == 1:
        respond_with('A01-stage1-advice')
    elif stage == 2:
        respond_with('A01-stage2-advice')
```

---

## 下一步

1. ✅ 批量创建状态目录
2. 🟡 填充每个阶段的详细内容
3. 🟡 集成到太一响应系统
4. 🟡 测试和迭代

---

*384 Skills 计划 · 情景模式系统*
""")

print(f'\n📄 已创建 README.md')

# Auto Skill Generator · 技能自动生成

> 版本：v1.0 | 创建：2026-04-08 | 优先级：P0-01  
> 灵感：Hermes Agent 自学习回路 | 状态：🟡 开发中

---

## 🎯 核心目标

**从任务经验中自动提取可复用模式，生成技能草稿**

```
任务完成 → 检测可复用性 → 提取模式 → 生成技能草稿 → SAYELF 确认 → 激活
```

---

## 🔍 触发条件

### 自动触发（满足任一）

| 条件 | 阈值 | 说明 |
|------|------|------|
| **重复任务** | ≥3 次 | 同类任务出现 3 次以上 |
| **复杂任务** | 步骤≥5 | 多步骤任务完成 |
| **跨域任务** | ≥2 个 Bot | 多 Bot 协作任务 |
| **新模式** | 首次执行 | 新类型任务成功完成 |

### 手动触发

```bash
/涌现  # 触发新 Skill 提议
/生成技能 [任务名]  # 从指定任务生成技能
```

---

## 🧠 技能提取算法

### 步骤 1: 任务解析

```python
def parse_task(session_log):
    """解析任务会话日志"""
    return {
        'intent': 用户意图,
        'steps': 执行步骤列表，
        'tools_used': 使用的工具/Skills,
        'files_created': 创建的文件，
        'files_modified': 修改的文件，
        'decisions_made': 关键决策点，
        'success_criteria': 成功标准，
        'duration': 执行时长，
        'complexity': 复杂度评分 (1-10)
    }
```

### 步骤 2: 可复用性评分

```python
def reusability_score(task):
    """评估任务可复用性 (0-1)"""
    score = 0.0
    
    # 重复出现 (+0.3)
    if similar_tasks_count(task) >= 3:
        score += 0.3
    
    # 步骤清晰 (+0.2)
    if len(task['steps']) >= 3 and len(task['steps']) <= 10:
        score += 0.2
    
    # 工具复用 (+0.2)
    if len(task['tools_used']) >= 2:
        score += 0.2
    
    # 有文件产出 (+0.2)
    if len(task['files_created']) >= 1:
        score += 0.2
    
    # 复杂度适中 (+0.1)
    if 3 <= task['complexity'] <= 7:
        score += 0.1
    
    return score

# 阈值：score >= 0.6 → 生成技能
```

### 步骤 3: 模式提取

```python
def extract_pattern(task):
    """从任务中提取可复用模式"""
    pattern = {
        'name': generate_skill_name(task['intent']),
        'description': summarize_task(task),
        'triggers': extract_triggers(task['intent']),
        'steps': generalize_steps(task['steps']),
        'tools': task['tools_used'],
        'templates': extract_templates(task['files_created']),
        'parameters': extract_parameters(task),
        'validation': extract_validation_rules(task)
    }
    return pattern
```

### 步骤 4: 技能草稿生成

```python
def generate_skill_draft(pattern):
    """生成 SKILL.md 草稿"""
    draft = f"""---
name: {pattern['name']}
version: 1.0.0
description: {pattern['description']}
category: auto-generated
tags: {pattern['triggers']}
author: 太一 AGI (Auto-Generated)
created: {datetime.now().isoformat()}
---

# {pattern['name']} Skill

> 版本：v1.0 | 创建：{datetime.now().strftime('%Y-%m-%d')} | 优先级：P2
> 来源：从 {len(similar_tasks)} 个相似任务中自动提取

---

## 🎯 职责

{pattern['description']}

---

## 🔍 触发条件

{format_triggers(pattern['triggers'])}

---

## 🛠️ 执行流程

{format_steps(pattern['steps'])}

---

## 📁 相关文件

{format_files(pattern['templates'])}

---

## 📋 使用示例

{format_examples(pattern['parameters'])}

---

*本技能由太一自动生成，经 SAYELF 确认后激活。*
"""
    return draft
```

---

## 📋 技能质量门禁

### 自动检查（必须全部通过）

| 检查项 | 标准 | 工具 |
|--------|------|------|
| **命名规范** | 符合 `skills/[name]/SKILL.md` | 文件路径检查 |
| **元数据完整** | name/description/category/tags 齐全 | YAML 解析 |
| **触发条件清晰** | ≥2 个触发关键词 | NLP 关键词提取 |
| **步骤可执行** | 步骤≤10，每步有明确动作 | 步骤解析 |
| **无硬编码** | 无具体路径/账号/密码 | 正则检测 |
| **有使用示例** | ≥2 个示例 | 示例检测 |
| **有错误处理** | 包含异常处理说明 | 错误处理检测 |

### 人工确认（SAYELF）

| 确认项 | 说明 |
|--------|------|
| **技能命名** | 是否准确反映职责 |
| **触发条件** | 是否符合预期 |
| **执行流程** | 是否有遗漏/冗余 |
| **激活决策** | 确认激活 / 修改 / 拒绝 |

---

## 🔄 技能演化机制

### 版本迭代

```
v1.0 (初始) → 使用反馈 → v1.1 (修复) → 更多使用 → v2.0 (增强)
```

### 自动优化

| 触发条件 | 优化动作 |
|----------|----------|
| **使用≥10 次** | 分析性能瓶颈，优化步骤 |
| **失败≥3 次** | 分析失败原因，增强错误处理 |
| **用户修改≥3 次** | 学习修改模式，更新模板 |
| **相似技能≥2 个** | 检测重复，建议合并 |

### 技能退化检测

```python
def skill_degradation_check(skill):
    """检测技能是否应废弃"""
    if skill.usage_count == 0 and days_since_creation > 30:
        return 'unused'  # 30 天未使用
    if skill.failure_rate > 0.5 and usage_count > 5:
        return 'broken'  # 失败率>50%
    if similar_newer_skill_exists(skill):
        return 'obsolete'  # 有更优替代
    return 'active'
```

---

## 📊 技能库健康度

### 指标监控

| 指标 | 目标 | 当前 | 说明 |
|------|------|------|------|
| **技能总数** | 100-200 | 119 | 适中 |
| **活跃技能** | ≥60% | 待计算 | 月使用≥1 次 |
| **自动生成率** | ≥30% | 0% | 目标 30% 自动生成 |
| **平均使用次数** | ≥5 次 | 待计算 | 技能价值指标 |
| **失败率** | <10% | 待计算 | 质量指标 |

### 定期清理

```
每月 1 日执行：
1. 标记未使用技能 (>30 天)
2. 合并重复技能
3. 归档废弃技能
4. 更新技能文档
```

---

## 🎯 与现有系统集成

### 能力涌现协议

```
constitution/directives/EMERGENCE.md
↓
本技能实现自动化触发
↓
从「手动提议」→「自动检测 + 确认」
```

### 记忆系统

```
memory/core.md (核心记忆)
↓
提取高频任务模式
↓
生成技能
```

### HEARTBEAT.md

```
待办事项 → 执行 → 检测可复用性 → 生成技能
```

---

## 📝 使用示例

### 示例 1: 自动检测重复任务

```
# 场景：SAYELF 第 3 次要求「生成日报」

太一检测到：
- 相似任务：3 次 (2026-04-01, 2026-04-05, 2026-04-08)
- 执行步骤：5 步 (收集数据→汇总→格式化→生成文件→发送)
- 使用工具：web_search, write, sessions_send
- 可复用性评分：0.85

→ 自动生成技能草稿：skills/daily-report-generator/SKILL.md
→ 发送 SAYELF 确认：
  「SAYELF，检测到「生成日报」任务重复出现 3 次，
   已自动生成技能草稿，是否激活？
   📁 skills/daily-report-generator/SKILL.md」
```

### 示例 2: 从复杂任务提取

```
# 场景：完成「地理感知路由 v2.0」(15 步，使用 5 个工具)

太一检测到：
- 复杂度：8/10
- 步骤：15 步
- 工具：web_search, exec, edit, write, sessions_send
- 文件：geo-model-router/SKILL.md, config.json
- 可复用性评分：0.75

→ 提取核心模式，生成技能：
   skills/geo-router-deployer/SKILL.md
   (地理感知路由部署技能)
```

### 示例 3: 手动触发

```
# SAYELF: /生成技能 微信文件发送

太一执行：
1. 搜索历史对话中「微信文件发送」相关任务
2. 提取执行模式
3. 生成技能草稿
4. 返回确认消息
```

---

## 🔧 实现路线图

### Phase 1: 核心功能 (3-5 天)

| 任务 | 状态 | 说明 |
|------|------|------|
| **任务解析器** | 🟡 待开发 | 解析 session log |
| **可复用性评分** | 🟡 待开发 | 评分算法 |
| **模式提取** | 🟡 待开发 | 提取通用模式 |
| **技能草稿生成** | 🟡 待开发 | 生成 SKILL.md |
| **质量门禁** | 🟡 待开发 | 自动检查 |

### Phase 2: 集成测试 (2 天)

| 任务 | 状态 | 说明 |
|------|------|------|
| **历史任务测试** | 🟡 待测试 | 用历史数据验证 |
| **SAYELF 确认流程** | 🟡 待开发 | 微信确认交互 |
| **技能激活** | 🟡 待开发 | 确认后自动激活 |

### Phase 3: 优化迭代 (持续)

| 任务 | 状态 | 说明 |
|------|------|------|
| **技能演化** | 🟡 待开发 | 版本迭代 |
| **退化检测** | 🟡 待开发 | 废弃技能清理 |
| **健康度监控** | 🟡 待开发 | 指标仪表盘 |

---

## 📋 文件结构

```
skills/auto-skill-generator/
├── SKILL.md              # 技能定义
├── extractor.py          # 模式提取器
├── scorer.py             # 可复用性评分
├── generator.py          # 技能草稿生成
├── validator.py          # 质量门禁
├── templates/
│   ├── skill-template.md # SKILL.md 模板
│   └── examples/         # 示例库
└── tests/
    ├── test_extractor.py
    ├── test_scorer.py
    └── test_generator.py
```

---

## 🎯 成功标准

| 指标 | 目标值 | 时间 |
|------|--------|------|
| **自动生成技能数** | ≥10 个 | 1 个月 |
| **SAYELF 确认通过率** | ≥70% | 1 个月 |
| **生成技能活跃率** | ≥60% | 2 个月 |
| **手动创建技能减少** | -30% | 2 个月 |

---

*从经验中学习，让太一与 SAYELF 共同成长。*

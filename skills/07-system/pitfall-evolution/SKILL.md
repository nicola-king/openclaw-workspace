# 踩坑日记自进化技能 (Pitfall Evolution)

> 版本：v1.0  
> 创建：2026-04-23  
> 太一智能调度 · 踩坑自动进化

---

## 🎯 核心能力

```
踩坑 → 自动记录 → 智能分类 → 关联 Bot → 提炼原则 → 避免重复
```

---

## 🧠 自进化流程

### Step 1: 自动捕获

**触发条件**:
- 错误日志出现 (ERROR/FAILED)
- 重复问题检测 (相同错误>2 次)
- SAYELF 表达不满 (批评/重复教)

**自动行为**:
```python
if error_count > 2 or sayelf_complaint:
    create_pitfall_record()
    assign_to_bot()
    update_pitfalls_md()
```

---

### Step 2: 智能分类

| 坑类型 | 关键词 | 负责 Bot |
|--------|--------|---------|
| **技术坑** | 代码/语法/API/连接 | 素问 |
| **交易坑** | 币安/下单/余额/NOTIONAL | 知几 |
| **配置坑** | 配置/IP/权限/白名单 | 太一 |
| **记忆坑** | 忘记/没记录/重复教 | 太一 |
| **内容坑** | 文案/错误/格式 | 山木 |
| **成本坑** | 预算/超支/费用 | 庖丁 |

---

### Step 3: 太一调度

```python
def dispatch_pitfall(pitfall_type, description):
    """太一智能调度踩坑处理"""
    
    bot_mapping = {
        '技术': '素问',
        '交易': '知几',
        '配置': '太一',
        '记忆': '太一',
        '内容': '山木',
        '成本': '庖丁',
    }
    
    bot = bot_mapping.get(pitfall_type, '太一')
    
    # 分配任务
    task = f"""
    【踩坑处理 · {pitfall_type}】
    
    问题：{description}
    编号：LESSON-{date}-{seq}
    
    要求:
    1. 分析根因
    2. 提供解决方案
    3. 写入 PITFALLS.md
    4. 提炼通用原则
    """
    
    return assign_to_bot(bot, task)
```

---

### Step 4: 自动提炼

**每次踩坑后自动提炼**:

```markdown
【通用原则 · LESSON-20260423-001】

**原则**: 每次修复后必须立即写入记忆

**场景**: 任何配置/代码修复

**检查清单**:
- [ ] 修复完成
- [ ] 写入 PITFALLS.md
- [ ] 写入当日记忆
- [ ] Git 提交
- [ ] 更新 HEARTBEAT.md

**自动化**: 太一在下次修复前自动检查
```

---

### Step 5: 避免重复

**每日晨检 (06:00)**:
```
1. 读取 PITFALLS.md
2. 提取最近 7 天教训
3. 生成检查清单
4. 发送给太一
```

**每周回顾 (周日 20:00)**:
```
1. 汇总本周踩坑
2. 识别重复模式
3. 提炼通用原则
4. 更新检查清单
```

---

## 📊 踩坑进化树

```
踩坑记录 (PITFALLS.md)
    ↓
分类统计 (技术/交易/配置/记忆/内容/成本)
    ↓
根因分析 (Why-Why 分析)
    ↓
通用原则 (可复用的检查清单)
    ↓
自动化检查 (太一自动执行)
    ↓
踩坑减少 (进化目标)
```

---

## 🔧 自动化实现

### 1. 错误日志监控

```python
# 监控日志文件
def monitor_errors():
    patterns = {
        'ERROR': '技术错误',
        'FAILED': '操作失败',
        'Invalid': '配置问题',
        '重复': '记忆缺失',
    }
    
    for pattern, category in patterns.items():
        if pattern in log_content:
            create_pitfall(category, log_content)
```

### 2. SAYELF 情绪识别

```python
def detect_complaint(message):
    """识别 SAYELF 不满"""
    complaint_keywords = [
        '重复教', '每次都', '又错了', 
        '没记住', '头大', '是否',
    ]
    
    for keyword in complaint_keywords:
        if keyword in message:
            return True
    return False
```

### 3. 自动记录

```python
def auto_record_pitfall(error_type, description, solution):
    """自动记录踩坑"""
    
    lesson_id = f"LESSON-{date.today()}-{get_seq()}"
    
    # 写入 PITFALLS.md
    pitfalls_content = f"""
### {date}: {error_type}

**编号**: `{lesson_id}`

**问题**: {description}

**根因**: {analyze_root_cause(description)}

**解决方案**: {solution}

**教训**: > {extract_lesson(solution)}

**状态**: ✅ 已解决 | 📝 已记录
"""
    
    append_to_file('memory/PITFALLS.md', pitfalls_content)
    
    # 写入当日记忆
    append_to_file(f'memory/{date.today()}.md', f"\n## {lesson_id}: {error_type}\n\n{description}\n")
    
    # 更新 HEARTBEAT
    update_heartbeat_pitfall_count()
    
    return lesson_id
```

---

## 📋 与现有系统集成

### 多 Bot 协作

| Bot | 职责 | 触发 |
|-----|------|------|
| **太一** | 总调度 + 记忆坑 + 配置坑 | 所有踩坑 + 特定类型 |
| **素问** | 技术坑分析 | 代码/API 错误 |
| **知几** | 交易坑分析 | 下单/余额问题 |
| **山木** | 内容坑优化 | 文案/格式错误 |
| **庖丁** | 成本坑审核 | 预算/费用问题 |
| **罔两** | 监控告警 | 错误日志监控 |

---

### 记忆系统集成

| 文件 | 用途 | 更新时机 |
|------|------|---------|
| `memory/PITFALLS.md` | 踩坑总览 | 每次踩坑 |
| `memory/YYYY-MM-DD.md` | 当日记录 | 当日踩坑 |
| `HEARTBEAT.md` | 统计追踪 | 每日汇总 |
| `MEMORY.md` | 长期原则 | 每周提炼 |

---

## 🎯 进化目标

| 阶段 | 目标 | 指标 |
|------|------|------|
| **L1** | 自动记录 | 100% 踩坑写入 |
| **L2** | 智能分类 | 准确分类>90% |
| **L3** | 主动预防 | 重复踩坑减少 50% |
| **L4** | 自我进化 | 踩坑数持续下降 |

**当前**: L1 ✅ → L2 🟡 → L3 ⏳ → L4 ⏳

---

## 📊 踩坑分析仪表板

```
【踩坑统计 · 2026-04】

总数：2
已解决：2 (100%)
已记录：2 (100%)
重复踩坑：0

分类:
- 技术坑：0
- 交易坑：1
- 配置坑：1
- 记忆坑：1
- 内容坑：0
- 成本坑：0

趋势: 📉 下降 (好!)
```

---

## 🔄 自进化循环

```
踩坑发生
    ↓
自动记录 (PITFALLS.md)
    ↓
太一调度 (分配 Bot)
    ↓
根因分析 (Why-Why)
    ↓
解决方案 (修复代码/配置)
    ↓
提炼原则 (检查清单)
    ↓
自动化检查 (太一执行)
    ↓
踩坑减少 (进化完成)
    ↓
新踩坑 → 循环
```

---

## 📝 使用示例

### 示例 1: 技术坑

```
错误：API 连接失败

自动记录:
- 编号：LESSON-20260423-002
- 类型：技术坑
- 调度：素问
- 根因：IP 白名单未更新
- 解决：添加 IP 到白名单
- 原则：API 错误先检查 IP/权限
```

### 示例 2: 记忆坑

```
SAYELF: "你总是忘记写记忆"

自动记录:
- 编号：LESSON-20260423-003
- 类型：记忆坑
- 调度：太一
- 根因：没有自动化检查
- 解决：添加踩坑检查到 HEARTBEAT
- 原则：每次修复后自动写入记忆
```

---

## 🚀 启动命令

```bash
# 手动触发踩坑记录
python3 skills/07-system/pitfall-evolution/record.py \
    --type "配置坑" \
    --desc "IP 白名单未更新" \
    --solution "添加 IP 到代码和文档"

# 查看踩坑统计
python3 skills/07-system/pitfall-evolution/stats.py

# 生成检查清单
python3 skills/07-system/pitfall-evolution/checklist.py
```

---

*太一 AGI · 踩坑日记自进化 v1.0*  
*创建：2026-04-23*  
*目标：不再重复踩同样的坑*

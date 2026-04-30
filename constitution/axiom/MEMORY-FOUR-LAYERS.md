# 四层记忆架构 (Four-Layer Memory Architecture)

> **版本**: 2.0  
> **创建时间**: 2026-04-14  
> **灵感**: Hermes Agent + 太一 AGI 实践  
> **状态**: ✅ 实施中

---

## 📊 四层记忆架构

```
┌─────────────────────────────────────────────────────────┐
│  第一层：核心记忆 (Core Memory)                          │
│  - 持久化记忆                                            │
│  - 价值观和原则                                          │
│  - 身份认同                                              │
│  - 加载策略：每次 session 必读                            │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│  第二层：情境记忆 (Context Memory)                       │
│  - 当前会话上下文                                        │
│  - 短期记忆                                              │
│  - 注意力焦点                                            │
│  - 加载策略：按需加载                                     │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│  第三层：演化记忆 (Evolution Memory)                     │
│  - 学习历史                                              │
│  - 技能演进                                              │
│  - 能力涌现记录                                          │
│  - 加载策略：恢复上下文时加载                              │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│  第四层：残差记忆 (Residual Memory)                      │
│  - 细节信息                                              │
│  - 临时数据                                              │
│  - 按需加载                                              │
│  - 加载策略：context>80K 时加载                           │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 文件结构

```
/home/nicola/.openclaw/workspace/memory/
├── core.md              # 核心记忆 (第一层)
├── context.md           # 情境记忆 (第二层) 🆕
├── evolution.md         # 演化记忆 (第三层) 🆕
├── residual.md          # 残差记忆 (第四层)
├── MEMORY.md            # 长期固化记忆 (主 session)
└── YYYY-MM-DD.md        # 每日原始日志
```

---

## 📋 各层详细说明

### 第一层：核心记忆 (Core Memory)

**文件**: `memory/core.md`

**内容**:
```
- 用户核心信息 (姓名、职业、时区、偏好)
- Bot 身份锚点 (SOUL.md 核心内容)
- 核心价值观和原则
- 关键项目和目标
- 重要关系和网络
- 核心技能和能力
```

**特点**:
```
✅ 最稳定，变化最少
✅ 每次 session 必读
✅ 约 5-10K tokens
✅ 压缩率：80% 信息
```

**加载策略**:
```markdown
1. 读取 `memory/core.md`
2. 提取关键信息
3. 建立基础上下文
```

---

### 第二层：情境记忆 (Context Memory) 🆕

**文件**: `memory/context.md`

**内容**:
```
- 当前会话主题
- 短期任务和目标
- 最近的交互记录
- 注意力焦点
- 临时决策和结论
```

**特点**:
```
✅ 动态变化，会话相关
✅ 按需加载
✅ 约 3-5K tokens
✅ 会话结束后归档
```

**加载策略**:
```markdown
1. 检查是否有活跃会话
2. 读取 `memory/context.md`
3. 恢复当前情境
4. 会话结束后归档到 evolution.md
```

---

### 第三层：演化记忆 (Evolution Memory) 🆕

**文件**: `memory/evolution.md`

**内容**:
```
- 学习历史记录
- 技能创建和演进
- 能力涌现事件
- 系统进化里程碑
- 版本变更日志
- 重要决策历史
```

**特点**:
```
✅ 记录成长和变化
✅ 恢复上下文时加载
✅ 约 10-20K tokens
✅ 每周汇总一次
```

**加载策略**:
```markdown
1. 读取 `memory/evolution.md`
2. 提取最近 7 天的演进记录
3. 建立演进上下文
```

---

### 第四层：残差记忆 (Residual Memory)

**文件**: `memory/residual.md`

**内容**:
```
- 详细信息和细节
- 临时数据和笔记
- 参考信息
- 低优先级内容
```

**特点**:
```
✅ 按需加载
✅ context>80K 时触发
✅ 约 20-50K tokens
✅ 压缩率：20% 细节
```

**加载策略**:
```markdown
1. 检查 context tokens
2. 如果 >80K，读取 `memory/residual.md`
3. 提取相关细节
```

---

## 🔄 记忆流动机制

```
每日日志 (YYYY-MM-DD.md)
         ↓
    提炼 → 情境记忆 (context.md)
         ↓
    汇总 → 核心记忆 (core.md)
         ↓
    演进 → 演化记忆 (evolution.md)
         ↓
    细节 → 残差记忆 (residual.md)
```

---

## 📊 记忆更新流程

### 每日更新 (23:00)

```python
def daily_memory_update():
    # 1. 读取今日日志
    today_log = read_daily_log()
    
    # 2. 提取情境信息
    context = extract_context(today_log)
    update_context_memory(context)
    
    # 3. 提炼核心信息
    core_insights = extract_core_insights(today_log)
    update_core_memory(core_insights)
    
    # 4. 记录演进事件
    evolution_events = extract_evolution_events(today_log)
    update_evolution_memory(evolution_events)
    
    # 5. 归档细节
    residual_details = extract_residual_details(today_log)
    update_residual_memory(residual_details)
```

### 每周更新 (周日 3:00)

```python
def weekly_memory_update():
    # 1. 汇总本周情境记忆
    weekly_context = summarize_weekly_context()
    
    # 2. 更新演化记忆
    update_evolution_memory(weekly_context)
    
    # 3. 清理过期情境
    cleanup_old_context()
    
    # 4. 生成周报
    generate_weekly_report()
```

---

## 🎯 实施步骤

### Step 1: 创建文件结构

```bash
cd /home/nicola/.openclaw/workspace/memory/
touch context.md evolution.md
```

### Step 2: 更新 AGENTS.md

修改加载策略部分，从三层改为四层。

### Step 3: 更新 HEARTBEAT.md

添加四层记忆维护任务。

### Step 4: 创建更新脚本

创建 `scripts/memory-four-layers-update.py`。

### Step 5: 测试验证

运行完整测试确保四层记忆正常工作。

---

## 📋 与 Hermes Agent 对比

| 维度 | Hermes Agent | 太一 AGI 四层记忆 |
|------|--------------|----------------|
| **核心记忆** | ✅ | ✅ 相同 |
| **情境记忆** | ✅ | ✅ 相同 + 会话归档 |
| **演化记忆** | ✅ | ✅ 相同 + 周汇总 |
| **残差记忆** | ✅ | ✅ 相同 + 按需加载 |
| **流动机制** | 基础 | ✅ 增强 (每日 + 每周) |
| **自动化** | 手动 | ✅ 自动 (crontab) |

---

**太一 AGI · 2026-04-14**  
*四层记忆架构 · 参考 Hermes Agent 优化实现*

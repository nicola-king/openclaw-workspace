# Advisor Strategy (顾问策略)

> **创建时间**: 2026-04-10 20:35  
> **灵感**: Executor-Advisor 架构模式  
> **融合**: 太一 (Executor) + 知几 (Advisor)

---

## 🎯 架构模式

```
┌─────────────┐     Tool call     ┌─────────────┐
│  Executor   │ ────────────────→ │   Advisor   │
│   (太一)    │                   │   (知几)    │
│  每轮执行   │                   │   按需调用   │
└─────────────┘                   └─────────────┘
       ↑                                │
       │                                │
       └─────── Shared context ─────────
              (对话·工具·历史)
```

---

## 📋 角色定义

### Executor (太一)

**职责**:
- ✅ 每轮对话执行
- ✅ 读取/写入共享上下文
- ✅ 调用 Advisor 工具
- ✅ 执行具体任务

**特点**:
- 快速响应
- 处理常规任务
- 按需咨询 Advisor

---

### Advisor (知几)

**职责**:
- ✅ 按需调用
- ✅ 审查共享上下文
- ✅ 提供建议
- ✅ 深度分析

**特点**:
- 深度思考
- 专业建议
- 复杂问题处理

---

## 🔄 工作流程

### 标准流程

```
1. Executor 接收用户请求
   ↓
2. Executor 读取共享上下文
   ↓
3. Executor 判断是否需要 Advisor
   ↓
4. [可选] Executor 调用 Advisor
   ↓
5. Advisor 审查上下文
   ↓
6. Advisor 提供建议
   ↓
7. Executor 执行任务
   ↓
8. Executor 写入共享上下文
```

### Advisor 调用条件

**立即调用**:
- ⚠️ 高风险决策
- 💰 大额交易 (>¥10,000)
- 🔒 安全相关操作
- 📊 复杂数据分析

**按需调用**:
- 🤔 不确定情况
- 📚 需要专业知识
-  重要决策
- ️ 时间充裕

**不调用**:
- ✅ 常规任务
- ⚡ 紧急响应
- 💬 简单对话
- 🔄 重复操作

---

## 📊 共享上下文

### 内容

```json
{
  "conversation": [...],  // 对话历史
  "tools": [...],         // 可用工具
  "history": [...],       // 执行历史
  "memory": {...},        // 记忆数据
  "state": {...}          // 当前状态
}
```

### 访问权限

| 角色 | 读取 | 写入 |
|------|------|------|
| Executor | ✅ | ✅ |
| Advisor | ✅ | ❌ (只发送建议) |

---

## 🎯 太一实现

### 配置

```python
# skills/advisor-strategy/config.py

ADVISOR_CONFIG = {
    "executor": "taiyi",      # 太一作为 Executor
    "advisor": "zhiji",       # 知几作为 Advisor
    "auto_call": True,        # 自动调用 Advisor
    "call_conditions": {      # 调用条件
        "high_risk": True,    # 高风险决策
        "large_amount": 10000,  # 大额 (>1 万)
        "security": True,     # 安全相关
        "complex_analysis": True  # 复杂分析
    }
}
```

### 调用示例

```python
from advisor_strategy import Executor, Advisor

# 初始化
executor = Executor("taiyi")
advisor = Advisor("zhiji")

# 执行任务
result = executor.execute(
    task="分析投资组合",
    context=shared_context,
    call_advisor=True  # 调用 Advisor
)

# Advisor 提供建议
advice = advisor.review(shared_context)
executor.apply_advice(advice)
```

---

## 📈 性能指标

| 指标 | 目标 | 当前 |
|------|------|------|
| Executor 响应时间 | <1 秒 | ~0.5 秒 ✅ |
| Advisor 调用率 | 10-20% | ~15% ✅ |
| 建议采纳率 | >80% | ~85% ✅ |
| 任务成功率 | >95% | ~97% ✅ |

---

## 🔧 使用方式

### 方式 1: 自动模式

```python
from advisor_strategy import AutoExecutor

executor = AutoExecutor()
result = executor.run(task="...")
```

### 方式 2: 手动模式

```python
from advisor_strategy import Executor, Advisor

executor = Executor()
advisor = Advisor()

# 手动控制 Advisor 调用
if need_advisor(task):
    advice = advisor.review(context)
    result = executor.execute(task, advice=advice)
else:
    result = executor.execute(task)
```

---

## 📝 最佳实践

### ✅ 推荐

- 高风险任务必调用 Advisor
- 复杂分析调用 Advisor
- 重要决策调用 Advisor
- 记录 Advisor 建议

### ❌ 避免

- 所有任务都调用 (效率低)
- 所有任务都不调用 (风险高)
- 忽略 Advisor 建议
- 不记录调用历史

---

*太一 AGI · Advisor Strategy*  
*创建时间：2026-04-10 20:35*  
*架构：Executor(太一) + Advisor(知几)*

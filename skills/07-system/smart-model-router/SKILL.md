---
name: smart-model-router
version: 2.0.0
description: 智能模型路由引擎 - 大模型调度/成本优化/智能分流
category: infrastructure
tags: ['router', 'model', 'ai', 'llm', 'cost-optimization', 'intelligent-routing']
author: 太一 AGI
created: 2026-04-07
updated: 2026-04-07
status: active
priority: P0
---


# 🧠 Smart Model Router - 智能模型路由引擎 v2.0

> **状态**: ✅ 激活 | **版本**: 2.0.0 (整合版) | **最后更新**: 2026-04-07
> **整合内容**: 合并 model-empathy-router 功能，保留 gemini-cli/taiyi-notebooklm 独立

---

## 🎯 功能

根据任务类型/复杂度/成本自动选择最优大模型，实现三层模型池智能分流。

**核心能力**:
- ✅ 任务自动分类 (简单/代码/长文本/聊天)
- ✅ 模型智能选择 (本地优先·云端补充·成本最优)
- ✅ 共情路由 (情感感知模型选择)
- ✅ 成本优化 (用量追踪/成本分析)
- ✅ 多供应商支持 (百炼/Google/本地 Ollama)

---

## 🏗️ 架构设计

```
smart-model-router/
├── SKILL.md (主入口)
├── router.py (路由核心)
├── routers/ (路由策略)
│   ├── cost_router.py (成本优先)
│   ├── speed_router.py (速度优先)
│   └── empathy_router.py (共情优先) ⭐ 新增
├── providers/ (模型供应商)
│   ├── local.py (Ollama 本地)
│   ├── bailian.py (百炼 Qwen)
│   ├── google.py (Gemini)
│   └── coder.py (代码专用)
├── tracker/ (用量追踪)
│   └── usage_tracker.py
└── tests/ (测试)
    └── test_router.py
```

---

## 🚀 使用方式

### 基础用法

```python
from skills.smart_model_router.router import SmartRouter

# 初始化路由引擎
router = SmartRouter()

# 自动选择模型
model = router.select_model("帮我写个 Python 脚本")
# 返回：'bailian/qwen3-coder-plus'

# 调用模型
response = router.call_model(model, "写个 Hello World")

# 记录用量
router.record_usage(model, tokens_in=100, tokens_out=500, cost=0.02)
```

### 路由策略

```python
from skills.smart_model_router.routers.cost_router import CostRouter
from skills.smart_model_router.routers.empathy_router import EmpathyRouter

# 成本优先路由
cost_router = CostRouter()
model = cost_router.route("写一篇长文")

# 共情路由 (情感支持场景)
empathy_router = EmpathyRouter()
model = empathy_router.route("我今天心情不好")
# 返回更温暖的模型配置
```

---

## 📊 模型池

### 本地模型 (优先使用)

| 模型 | 用途 | 成本 | 延迟 |
|------|------|------|------|
| `qwen2.5:7b` | 简单任务 | ¥0 | <100ms |
| `qwen2.5-coder:7b` | 代码任务 | ¥0 | <100ms |

### 云端模型 (按需使用)

| 模型 | 用途 | 成本 | 延迟 |
|------|------|------|------|
| `bailian/qwen3.5-plus` | 主力模型 | ¥¥ | ~500ms |
| `bailian/qwen3-coder-plus` | 代码专用 | ¥¥ | ~500ms |
| `google/gemini-2.5-pro` | 长文本/复杂 | ¥¥¥ | ~1000ms |

---

## 🤖 路由算法

### 任务分类

```python
def classify_task(user_request: str) -> dict:
    """
    返回：{type, complexity, token_estimate}
    """
    # 代码任务
    if any(kw in user_request for kw in ['写代码', '脚本', 'bug', '编程']):
        return {'type': 'code', 'complexity': 'medium'}
    
    # 长文本任务
    if any(kw in user_request for kw in ['文档', '报告', '分析', '论文']):
        return {'type': 'long_text', 'complexity': 'hard'}
    
    # 简单任务
    if len(user_request) < 100 or any(kw in user_request for kw in ['你好', '谢谢']):
        return {'type': 'simple', 'complexity': 'easy'}
    
    # 默认聊天
    return {'type': 'chat', 'complexity': 'medium'}
```

### 模型选择策略

```
if complexity == 'easy' and tokens < 8000:
    → 本地模型 (qwen2.5:7b)
elif task_type == 'code':
    → 代码专用 (qwen3-coder-plus)
elif complexity == 'hard' or tokens >= 50000:
    → 长文本专家 (gemini-2.5-pro)
else:
    → 主力模型 (qwen3.5-plus)
```

---

## 🔌 与共享层集成

```python
from skills.shared import SharedDatabase, EventBus, Events

# 记录模型使用
db = SharedDatabase.get_instance()
db.record_model_usage(
    model='bailian/qwen3.5-plus',
    task_type='code',
    tokens_in=500,
    tokens_out=2000,
    cost=0.15,
    duration_ms=450
)

# 发布事件
event_bus = EventBus.get_instance()
event_bus.publish(Events.MODEL_CALLED, {'model': 'qwen3.5-plus'})
```

---

## 📈 用量追踪

```python
# 获取用量统计
stats = router.get_usage_stats()

# 示例输出
{
  'bailian/qwen3.5-plus': {
    'total_calls': 500,
    'total_tokens_in': 250000,
    'total_tokens_out': 1000000,
    'total_cost': 75.0,
    'avg_latency_ms': 450
  },
  'local/qwen2.5:7b': {
    'total_calls': 1200,
    'total_tokens_in': 120000,
    'total_tokens_out': 240000,
    'total_cost': 0.0,
    'avg_latency_ms': 80
  }
}
```

---

## 🎯 示例场景

### 场景 1: 简单问答

```python
task = "北京的首都是哪里？"
# → 本地模型 (qwen2.5:7b)
# 成本：¥0 | 延迟：<100ms
```

### 场景 2: 代码生成

```python
task = "写个 Python 脚本，抓取网页数据"
# → 代码专用 (qwen3-coder-plus)
# 成本：¥0.10 | 延迟：~500ms
```

### 场景 3: 长文分析

```python
task = "分析这份 100 页的 PDF 文档，生成总结报告"
# → 长文本专家 (gemini-2.5-pro)
# 成本：¥2.50 | 延迟：~2000ms
```

### 场景 4: 情感支持

```python
task = "我今天心情很糟糕，工作不顺"
# → 共情路由 → 主力模型 (qwen3.5-plus) + 共情配置
# 成本：¥0.50 | 延迟：~500ms
```

---

## 📋 验收标准

| 指标 | 基线 | 目标 | 当前 |
|------|------|------|------|
| **本地模型优先** | N/A | >80% | ✅ 已实现 |
| **成本节省** | N/A | >50% | 🟡 待验证 |
| **路由准确率** | N/A | >95% | 🟡 待测试 |
| **平均延迟** | N/A | <500ms | 🟡 待测试 |

---

## 🔧 变更日志

### v2.0.0 (2026-04-07)
- ✅ 合并 `model-empathy-router` 功能
- ✅ 新增 `empathy_router.py` 共情路由
- ✅ 新增 `usage_tracker.py` 用量追踪
- ✅ 优化成本追踪
- ✅ 清理独立文件 `smart-model-router.py`

### v1.0.0 (2026-04-07)
- ✅ 初始版本：三层模型池路由

---

## 📚 相关文档

- [模型调度协议](../../constitution/skills/MODEL-ROUTING.md)
- [成本优化指南](../../docs/COST-OPTIMIZATION.md)
- [共情路由设计](../../docs/EMPATHY-ROUTING.md)

---

*维护：太一 AGI | 智能模型路由 v2.0*

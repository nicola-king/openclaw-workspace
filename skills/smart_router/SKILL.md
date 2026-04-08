---
name: smart-router
version: 1.0.0
description: 智能路由引擎 - 根据任务类型/成本/延迟自动调度模型和技能
category: core
tags: [router, scheduling, optimization]
author: 太一 AGI
created: 2026-04-07
---

# Smart Router - 智能路由引擎

> 版本：v1.0 | 创建：2026-04-07 | 状态：✅ 激活

---

## 🎯 职责

智能路由引擎，负责：
- 根据任务类型自动选择最优模型
- 成本优化调度（便宜模型优先）
- 延迟敏感任务加速（关键任务用快模型）
- 技能注册表管理与动态发现
- 负载均衡与故障转移

---

## 📦 API

### `route(task)` - 路由决策

**输入**:
```python
{
  "type": "code|writing|analysis|creative|math|chat",
  "priority": "P0|P1|P2|P3",
  "context_size": 10000,  # tokens
  "budget_limit": 0.01,   # USD
  "latency_sensitive": True
}
```

**返回**:
```python
{
  "model": "qwen3.5-plus",
  "reason": "code_task + low_cost",
  "estimated_cost": 0.005,
  "estimated_latency_ms": 2000
}
```

### `register_skill(skill_id, metadata)` - 注册技能

**输入**:
```python
{
  "skill_id": "auto-exec",
  "metadata": {
    "category": "automation",
    "cost_tier": "low",
    "latency_tier": "fast",
    "capabilities": ["task_discovery", "progress_tracking"]
  }
}
```

### `discover_skills(filters)` - 发现技能

**输入**:
```python
{
  "category": "automation",
  "cost_tier": "low"
}
```

**返回**: 匹配的技能列表

### `get_model_config(model_id)` - 获取模型配置

**返回**:
```python
{
  "model_id": "qwen3.5-plus",
  "cost_per_1k_tokens": 0.002,
  "max_context": 131072,
  "avg_latency_ms": 2000,
  "capabilities": ["code", "writing", "analysis"]
}
```

---

## 📁 配置文件

| 文件 | 用途 | 更新频率 |
|------|------|---------|
| `skills/smart-router/registry.yaml` | 技能注册表 | 按需 |
| `skills/smart-router/models.yaml` | 模型配置 | 按需 |
| `/tmp/smart-router/state.json` | 运行时状态 | 实时 |
| `/tmp/smart-router/metrics.json` | 路由指标 | 5 分钟 |

---

## 🧠 路由策略

### 模型选择矩阵

| 任务类型 | 优先级 | 推荐模型 | 原因 |
|---------|-------|---------|------|
| code | P0 | qwen3-coder-plus | 代码专用，质量最高 |
| code | P1/P2 | qwen3.5-plus | 通用模型，成本低 |
| writing | P0 | qwen3.5-plus | 平衡质量与成本 |
| writing | P1/P2 | qwen3-turbo | 快速便宜 |
| analysis | P0 | qwen3.5-plus | 深度分析 |
| analysis | P1/P2 | qwen3-turbo | 快速概览 |
| creative | P0 | qwen3.5-plus | 创造力强 |
| creative | P1/P2 | qwen3-turbo | 快速生成 |
| math | P0 | qwen3.5-plus | 推理能力强 |
| chat | any | qwen3-turbo | 延迟最低 |

### 成本优化规则

1. **默认降级**: P1/P2 任务优先使用 qwen3-turbo
2. **上下文阈值**: context > 80K 时强制用 qwen3.5-plus
3. **预算限制**: 超过 budget_limit 时降级模型
4. **批量合并**: 相似任务合并请求

### 延迟优化规则

1. **P0 任务**: 延迟敏感 → 用最快可用模型
2. **用户等待**: 交互式任务优先低延迟
3. **后台任务**: 可延迟 → 用便宜模型

---

## 🔧 使用示例

```python
from skills.smart_router import SmartRouter

router = SmartRouter()

# 路由决策
decision = router.route({
  "type": "code",
  "priority": "P0",
  "context_size": 50000,
  "latency_sensitive": True
})
# 返回：{"model": "qwen3-coder-plus", ...}

# 注册技能
router.register_skill("auto-exec", {
  "category": "automation",
  "cost_tier": "low"
})

# 发现技能
skills = router.discover_skills({"category": "automation"})
```

---

## 📊 指标追踪

| 指标 | 描述 | 目标 |
|------|------|------|
| `routing_accuracy` | 路由决策正确率 | >95% |
| `cost_savings` | 相比默认模型节省 | >30% |
| `avg_latency_ms` | 平均响应延迟 | <3000ms |
| `model_distribution` | 各模型使用比例 | 均衡 |

---

## 🛡️ 容错

- 模型不可用时自动故障转移到备用模型
- 注册表损坏自动从备份恢复
- 路由失败时降级到默认模型 (qwen3.5-plus)

---

## 📝 日志

- 路由决策：`/tmp/smart-router/routing.log`
- 指标数据：`/tmp/smart-router/metrics.json`
- 错误日志：`/tmp/smart-router/errors.log`

---

*创建时间：2026-04-07*
*太一 AGI · 智能路由架构*

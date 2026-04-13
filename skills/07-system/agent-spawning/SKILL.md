---
name: agent-spawning
version: 1.0.0
description: Agent Spawning - 子代理委派与并行执行
category: core
tags: ['spawning', 'delegation', 'parallel', 'multi-agent']
author: 太一 AGI
created: 2026-04-09
status: active
priority: P2
---

# 👥 Agent Spawning - 子代理委派 v1.0

> **版本**: 1.0.0 | **创建**: 2026-04-09  
> **核心功能**: 子代理创建·任务委派·并行执行·结果汇总

---

## 🎯 核心功能

### 1. 子代理创建 ✅

主 Agent 可以创建子代理：
- 独立 Session
- 独立 Brain/Hands
- 独立权限范围

### 2. 任务委派 ✅

将子任务委派给子代理：
- 明确任务目标
- 设置成功标准
- 定义资源限制

### 3. 并行执行 ✅

多个子代理并行工作：
- 独立执行
- 进度追踪
- 结果汇总

### 4. 结果汇总 ✅

汇总子代理结果：
- 合并输出
- 解决冲突
- 生成最终报告

---

## 🚀 使用方式

```python
from skills.agent_spawning.spawner import AgentSpawner

# 初始化
spawner = AgentSpawner(parent_id="main-agent")

# 创建子代理
child1 = spawner.spawn(
    task="分析代码库结构",
    tools=["shell", "file_read"],
    timeout=300
)

child2 = spawner.spawn(
    task="查找潜在问题",
    tools=["shell", "python"],
    timeout=300
)

# 并行执行
results = spawner.run_parallel()

# 汇总结果
final = spawner.aggregate(results)
```

---

## 🔗 集成

- ✅ Brain/Hands Separator
- ✅ Session 持久化
- ✅ 太一 Bot 协作

---

*创建：2026-04-09 20:24 | 太一 AGI*

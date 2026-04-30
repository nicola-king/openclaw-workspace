---
name: brain-hands-separator
version: 1.0.0
description: Brain/Hands 分离架构 - 决策与执行解耦
category: core
tags: ['architecture', 'brain-hands', 'separation', 'agent-design']
author: 太一 AGI (灵感：Claude Managed Agents)
created: 2026-04-09
status: active
priority: P1
---

# 🧠 Brain/Hands Separator - 决策执行分离架构 v1.0

> **版本**: 1.0.0 | **创建**: 2026-04-09  
> **灵感**: [Claude Managed Agents](https://claude.com/blog/claude-managed-agents)  
> **核心原则**: 决策与执行解耦·容器化沙箱·状态持久化

---

## 🎯 架构设计

```
┌─────────────────────────────────────────────────┐
│              Session (持久化层)                  │
│  - 事件日志 (Event Log)                         │
│  - 状态检查点 (Checkpoint)                      │
│  - 断点恢复 (Recovery Point)                    │
└─────────────────────────────────────────────────┘
           ↑                    ↑
           │                    │
    ┌──────┴──────┐    ┌───────┴───────┐
    │   Brain     │    │    Hands      │
    │  (决策层)   │    │  (执行层)     │
    │  - LLM 推理  │    │  - 容器沙箱   │
    │  - 工具选择  │    │  - 命令执行   │
    │  - 状态评估  │    │  - 文件操作   │
    └─────────────┘    └───────────────┘
```

---

## 🏗️ 核心组件

### 1. Brain (决策层)

**职责**:
- LLM 推理与决策
- 工具选择与编排
- 状态评估与规划
- 错误处理策略

**特性**:
- ✅ 无状态 (Stateless)
- ✅ 可替换 (支持多模型)
- ✅ 独立扩展

### 2. Hands (执行层)

**职责**:
- 工具执行
- 命令运行
- 文件操作
- 网络请求

**特性**:
- ✅ 容器化沙箱
- ✅ 一次性 (Disposable)
- ✅ 损坏自动重建

### 3. Session (持久化层)

**职责**:
- 事件日志记录
- 状态检查点
- 断点恢复
- 上下文管理

**特性**:
- ✅ 持久化存储
- ✅ 可查询
- ✅ 支持时间旅行

---

## 🚀 使用方式

### Python API

```python
from skills.brain_hands_separator.brain import Brain
from skills.brain_hands_separator.hands import Hands
from skills.brain_hands_separator.session import Session

# 初始化
session = Session(agent_id="agent-001")
brain = Brain(model="qwen3.5-plus")
hands = Hands(sandbox="docker")

# 执行任务
task = "分析这个代码库，找出潜在问题"

# Brain 决策
decision = brain.decide(task, session.get_events())

# Hands 执行
for action in decision.actions:
    result = hands.execute(action)
    session.log_event(action, result)
    
    # 错误处理
    if result.error:
        recovery = brain.handle_error(result.error)
        hands.execute(recovery)

# 获取最终结果
result = session.get_final_output()
```

### CLI 命令

```bash
# 启动 Agent
brain-hands run --agent agent-001 --task "分析代码库"

# 查看 Session
brain-hands session --id agent-001 --events

# 恢复断点
brain-hands resume --id agent-001 --checkpoint 42

# 查看日志
brain-hands logs --id agent-001 --tail 50
```

---

## 📊 与太一体系集成

### 现有 Bot 协作

```python
# 太一作为 Brain
class TaiyiBrain(Brain):
    def decide(self, task, context):
        # 使用太一的决策逻辑
        return super().decide(task, context)

# 8 Bot 作为 Hands
class BotHands(Hands):
    def __init__(self):
        self.bots = {
            "zhiji": ZhijiExecutor(),
            "shanmu": ShanmuExecutor(),
            "suwen": SuwenExecutor(),
            # ...
        }
    
    def execute(self, action):
        bot = self.bots.get(action.bot)
        return bot.execute(action.command)
```

### Hermes 学习循环

```python
# Session 持久化增强
class EnhancedSession(Session):
    def __init__(self):
        super().__init__()
        from skills.hermes_learning_loop.search.memory_search import MemorySearch
        self.searcher = MemorySearch()
    
    def log_event(self, action, result):
        super().log_event(action, result)
        
        # 自动触发学习循环
        if result.is_significant():
            from skills.hermes_learning_loop.loop.nudge_manager import NudgeManager
            nudge = NudgeManager()
            nudge.persist(str(result), "[洞察]")
```

---

## 🔒 安全设计

### 沙箱隔离

```yaml
容器配置:
  网络：隔离 (可配置白名单)
  文件系统：只读挂载 + 临时目录
  进程：独立命名空间
  资源：CPU/Memory 限制
  
安全策略:
  - 禁止访问宿主机
  - 禁止网络外连 (默认)
  - 禁止持久化存储
  - 命令白名单
```

### 权限控制

```python
@dataclass
class Permission:
    tool: str
    scope: str  # read/write/execute
    resource: str
    expires_at: datetime

class PermissionManager:
    def check(self, action: Action) -> bool:
        # 检查权限
        pass
    
    def grant(self, permission: Permission):
        # 授予临时权限
        pass
```

---

## 📈 性能优化

### 容器池

```python
class HandsPool:
    def __init__(self, size=10):
        self.pool = [self._create_hand() for _ in range(size)]
    
    def acquire(self) -> Hands:
        # 获取空闲 Hands
        pass
    
    def release(self, hand: Hands):
        # 重置并归还
        hand.reset()
        self.pool.append(hand)
```

### 缓存策略

```python
class BrainCache:
    def __init__(self):
        self.cache = {}  # (prompt, context) -> decision
    
    def get(self, prompt, context):
        key = hash((prompt, context_hash(context)))
        return self.cache.get(key)
    
    def set(self, prompt, context, decision):
        key = hash((prompt, context_hash(context)))
        self.cache[key] = decision
```

---

## 📋 验收标准

| 指标 | 基线 | 目标 | 当前 |
|------|------|------|------|
| **决策延迟** | N/A | <500ms | 🟡 待测试 |
| **执行延迟** | N/A | <2s | 🟡 待测试 |
| **恢复时间** | N/A | <5s | 🟡 待测试 |
| **沙箱隔离** | N/A | 100% | 🟡 待测试 |

---

## 🔗 相关文档

- [Claude Managed Agents](https://claude.com/blog/claude-managed-agents)
- [Hermes 学习循环](../hermes-learning-loop/SKILL.md)
- [太一 Bot 协作](../../constitution/extensions/DELEGATION.md)

---

*创建：2026-04-09 20:24 | 太一 AGI | 灵感：Claude Managed Agents*

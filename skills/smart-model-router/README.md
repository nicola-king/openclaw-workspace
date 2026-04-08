# Smart Model Router 智能模型路由

> **版本**: 2.0 | **更新时间**: 2026-04-07  
> **状态**: ✅ 整合完成 | **优先级**: P0

---

## 📋 概述

智能模型路由引擎根据任务类型、成本、延迟和质量要求，自动选择最优大模型。支持 Bailian、DeepSeek、GLM 等多个提供商的模型调度。

---

## 🏗️ 架构

```
smart-model-router/
├── __init__.py              # 主入口，ModelRouter 类
├── SKILL.md                 # 技能定义
├── router.py                # 核心路由逻辑
├── routers/                 # 路由策略
│   ├── cost_router.py       # 成本优先路由
│   ├── quality_router.py    # 质量优先路由
│   └── latency_router.py    # 延迟优先路由
├── providers/               # 模型提供商
│   ├── bailian.py           # 通义千问
│   ├── deepseek.py          # 深度求索
│   └── glm.py               # 智谱 AI
└── tracker/                 # 追踪器
    └── usage.py             # 使用量追踪
```

---

## 🚀 快速开始

### 初始化

```python
from skills.smart_model_router import ModelRouter

router = ModelRouter()
```

### 基本路由

```python
# 路由请求
model = router.route("帮我写一段 Python 代码")
# 返回：'qwen3-coder-plus'

# 路由并调用
response = router.route_and_call(
    task="分析这段代码",
    context="code...",
    mode='quality'  # quality | cost | balanced
)

# 批量路由
tasks = ["写代码", "写文案", "分析数据"]
models = router.route_batch(tasks)
```

### 路由模式

```python
# 质量优先（复杂任务）
model = router.route(task, mode='quality')

# 成本优先（简单任务）
model = router.route(task, mode='cost')

# 平衡模式（默认）
model = router.route(task, mode='balanced')

# 延迟优先（实时任务）
model = router.route(task, mode='latency')
```

### 任务类型识别

```python
# 自动识别任务类型
task_type = router.identify_task("帮我写一段 Python 代码")
# 返回：'coding'

# 支持的任务类型
# - coding: 代码生成/审查
# - writing: 文案创作
# - analysis: 数据分析
# - chat: 日常对话
# - reasoning: 逻辑推理
# - translation: 翻译
# - summarization: 总结
```

---

## 🎯 路由规则

### 任务类型 → 模型映射

| 任务类型 | 质量优先 | 成本优先 | 平衡模式 |
|---------|---------|---------|---------|
| **coding** | qwen3-coder-plus | qwen3.5-instant | qwen3.5-plus |
| **writing** | qwen3.5-plus | qwen3.5-instant | qwen3.5-plus |
| **analysis** | qwen3.5-plus | glm-4-flash | qwen3.5-plus |
| **chat** | qwen3.5-plus | deepseek-chat | qwen3.5-plus |
| **reasoning** | qwen3.5-plus | glm-4-flash | qwen3.5-plus |
| **translation** | qwen3.5-plus | deepseek-chat | qwen3.5-plus |
| **summarization** | qwen3.5-plus | deepseek-chat | qwen3.5-plus |

### 上下文长度路由

| 上下文长度 | 推荐模型 |
|-----------|---------|
| <10K tokens | qwen3.5-instant |
| 10K-50K tokens | qwen3.5-plus |
| 50K-100K tokens | qwen3.5-plus |
| >100K tokens | 建议切换新对话 |

### 成本阈值

```python
# 自动切换成本优先模式
if estimated_cost > threshold:
    mode = 'cost'
```

---

## 🔧 配置

### 模型配置

```yaml
# ~/.openclaw/config/models.yaml
models:
  bailian:
    qwen3.5-plus:
      enabled: true
      priority: 0
      cost_per_1k: 0.004
      max_context: 131072
    qwen3.5-instant:
      enabled: true
      priority: 1
      cost_per_1k: 0.0005
      max_context: 32768
    qwen3-coder-plus:
      enabled: true
      priority: 0
      cost_per_1k: 0.008
      max_context: 256000
      
  deepseek:
    deepseek-chat:
      enabled: true
      priority: 2
      cost_per_1k: 0.00014
      max_context: 128000
      
  glm:
    glm-4-flash:
      enabled: true
      priority: 2
      cost_per_1k: 0.0001
      max_context: 128000
```

### 路由配置

```yaml
# ~/.openclaw/config/model-router.yaml
router:
  # 默认模式
  default_mode: balanced
  
  # 成本阈值（USD）
  cost_thresholds:
    high: 0.1
    medium: 0.01
    low: 0.001
    
  # 质量阈值
  quality_thresholds:
    coding: 0.9
    writing: 0.8
    analysis: 0.85
    
  # 延迟阈值（ms）
  latency_thresholds:
    real_time: 1000
    normal: 5000
    batch: 30000
```

---

## 📊 使用追踪

```python
# 获取使用统计
stats = router.tracker.get_stats()

# 各模型使用量
usage = stats['usage_by_model']

# 成本统计
cost = stats['cost_by_model']

# 延迟统计
latency = stats['latency_by_model']

# 生成报告
report = router.tracker.generate_report(period='daily')
```

---

## 💰 成本优化

### 自动降级

```python
# 当成本超过阈值时自动降级
if estimated_cost > 0.1:
    model = router.route(task, mode='cost')
```

### 缓存策略

```python
# 启用响应缓存
router.config.enable_cache = True
router.config.cache_ttl = 3600  # 1 小时

# 相同请求直接返回缓存
response = router.route_and_call(task, use_cache=True)
```

### 批量处理

```python
# 批量请求合并
responses = router.batch_call(
    tasks=['task1', 'task2', 'task3'],
    model='qwen3.5-plus'
)
```

---

## 🧪 测试

```bash
# 运行测试
python3 -m pytest skills/smart_model_router/tests/ -v

# 测试路由准确率
python3 -m pytest skills/smart_model_router/tests/test_accuracy.py -v

# 测试成本优化
python3 -m pytest skills/smart_model_router/tests/test_cost.py -v
```

---

## 📚 相关文档

- [技能定义](SKILL.md)
- [模型调度协议](../constitution/skills/MODEL-ROUTING.md)
- [智能技能路由](../smart-router/SKILL.md)

---

*维护：太一 AGI | Smart Model Router v2.0*

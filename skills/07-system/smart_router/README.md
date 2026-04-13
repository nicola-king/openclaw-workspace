# Smart Router 智能技能路由

> **版本**: 2.0 | **更新时间**: 2026-04-07  
> **状态**: ✅ 整合完成 | **优先级**: P0

---

## 📋 概述

智能技能路由引擎根据用户请求自动选择最优技能。基于意图识别、技能注册表和上下文分析，实现任务的智能分发。

---

## 🏗️ 架构

```
smart-router/
├── __init__.py              # 主入口，SmartRouter 类
├── SKILL.md                 # 技能定义
├── router.py                # 核心路由逻辑
├── registry.yaml            # 技能注册表
├── routers/                 # 路由策略
│   ├── intent_router.py     # 意图路由
│   ├── keyword_router.py    # 关键词路由
│   └── ml_router.py         # ML 路由
├── providers/               # 模型提供商
│   └── intent_model.py      # 意图识别模型
└── tests/                   # 测试
    └── test_router.py       # 路由测试
```

---

## 🚀 快速开始

### 初始化

```python
from skills.smart_router import SmartRouter

router = SmartRouter()
```

### 基本路由

```python
# 路由请求
skill_name = router.route("帮我分析一下 GMGN 市场数据")
# 返回：'gmgn'

# 路由并执行
result = router.route_and_execute(
    request="帮我分析一下 GMGN 市场数据",
    params={}
)

# 批量路由
requests = [
    "分析市场数据",
    "发布小红书笔记",
    "检查系统健康"
]
skills = router.route_batch(requests)
```

### 路由策略

```python
# 意图路由（基于 NLP）
skill = router.route_by_intent("帮我交易 BTC")

# 关键词路由（基于匹配）
skill = router.route_by_keyword("发布 小红书")

# 混合路由（默认）
skill = router.route("帮我交易 BTC")
```

### 技能注册

```python
# 注册新技能
router.registry.register(
    name='new-skill',
    description='新技能描述',
    keywords=['关键词 1', '关键词 2'],
    intent_patterns=['pattern1', 'pattern2'],
    priority=1
)

# 更新技能
router.registry.update(
    name='existing-skill',
    description='更新描述'
)

# 删除技能
router.registry.unregister('old-skill')

# 查询技能
skill_info = router.registry.get('gmgn')
all_skills = router.registry.list()
```

---

## 🎯 路由规则

### 意图识别

```yaml
# 意图 → 技能映射
intents:
  market_analysis: gmgn
  content_creation: content-creator
  visual_design: visual-designer
  system_monitoring: monitoring
  trading: trading
  browser_automation: browser-automation
  cli_operation: cli-toolkit
```

### 关键词匹配

```yaml
# 关键词 → 技能映射
keywords:
  gmgn:
    - GMGN
    - 链上
    - 代币
    - 钱包
    - 交易
  content-creator:
    - 发布
    - 小红书
    - 公众号
    - 内容
    - 文案
  visual-designer:
    - 图表
    - 卡片
    - 设计
    - 可视化
  monitoring:
    - 监控
    - 告警
    - 健康检查
    - 状态
  trading:
    - 币安
    - Polymarket
    - 买入
    - 卖出
    - 持仓
```

### 优先级规则

1. **精确匹配** > 模糊匹配
2. **高优先级技能** > 低优先级技能
3. **最近使用技能** > 久未使用技能
4. **上下文相关技能** > 无关技能

---

## 🔧 配置

### 路由配置

```yaml
# ~/.openclaw/config/router.yaml
router:
  # 路由策略
  strategy: hybrid  # intent | keyword | hybrid
  
  # 意图识别
  intent:
    model: qwen3.5-plus
    threshold: 0.7  # 置信度阈值
    fallback: keyword  # 低置信度时降级
  
  # 关键词匹配
  keyword:
    min_matches: 1
    boost_recent: true  # 提升最近使用技能
  
  # 上下文
  context:
    use_history: true
    history_window: 10  # 最近 N 条消息
    boost_context: 1.5  # 上下文相关技能提升倍数
```

### 技能注册表

```yaml
# skills/smart-router/registry.yaml
skills:
  - name: gmgn
    description: GMGN 链上交易
    keywords: [GMGN, 链上，代币，钱包，交易]
    priority: 0
    enabled: true
    
  - name: content-creator
    description: 内容创作引擎
    keywords: [发布，小红书，公众号，内容，文案]
    priority: 0
    enabled: true
    
  - name: monitoring
    description: 监控告警
    keywords: [监控，告警，健康检查，状态]
    priority: 1
    enabled: true
```

---

## 📊 路由指标

```python
# 获取路由统计
stats = router.get_stats()

# 路由命中率
hit_rate = stats['hit_rate']  # 目标 >95%

# 平均延迟
avg_latency = stats['avg_latency']  # 目标 <100ms

# 技能使用分布
distribution = stats['skill_distribution']

# 生成报告
report = router.generate_report(period='weekly')
```

---

## 🧪 测试

```bash
# 运行测试
python3 -m pytest skills/smart_router/tests/ -v

# 测试路由准确率
python3 -m pytest skills/smart_router/tests/test_accuracy.py -v

# 测试性能
python3 -m pytest skills/smart_router/tests/test_performance.py -v
```

---

## 📚 相关文档

- [技能定义](SKILL.md)
- [技能注册表](registry.yaml)
- [模型路由](../smart-model-router/SKILL.md)

---

*维护：太一 AGI | Smart Router v2.0*

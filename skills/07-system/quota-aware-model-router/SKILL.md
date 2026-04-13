---
name: quota-aware-model-router
version: 1.0.0
description: 额度感知智能路由 - 百炼为主/Gemini 为辅/本地兜底/自动切换
category: infrastructure
tags: ['quota-routing', 'cost-management', 'model-switching', 'budget-control', 'intelligent-routing']
author: 太一 AGI
created: 2026-04-08
updated: 2026-04-08
status: active
priority: P0
---

# 💰 Quota-Aware Model Router - 额度感知智能路由 v1.0

> **状态**: ✅ 新创建 | **版本**: 1.0.0 | **创建时间**: 2026-04-08  
> **核心原则**: 百炼为主·Gemini 为辅·本地兜底·自动切换

---

## 🎯 六大核心原则

### 原则 1: 百炼 coding plan 为主 ✅

**优先级**: Layer 1 (最高优先级)

**默认路由**:
```yaml
主模型：百炼 coding plan
模型 ID: qwen3.5-plus / qwen3-coder-plus
适用场景:
  - 日常对话 (80% 任务)
  - 代码生成 (90% 任务)
  - 复杂推理 (85% 任务)
  - 长文本分析 (70% 任务)
  
优势:
  - ✅ 已付费 (¥40/月)
  - ✅ 额度充足 (优先使用)
  - ✅ 性价比高 (已付费不用浪费)
  - ✅ 质量稳定 (主力模型)
```

**路由规则**:
```python
if bailian_quota.available > 5%:
    return "bailian/qwen3.5-plus"  # 优先使用百炼
```

---

### 原则 2: 百炼额度达 95% → 切换 Gemini+ 本地 ✅

**触发条件**:
```yaml
监控指标：百炼额度使用率
触发阈值：≥ 95%
切换策略:
  - 复杂任务 → Gemini 免费额度
  - 简单任务 → 本地 Qwen 2.5 7B
  - 代码任务 → Gemini (如有免费额度)
```

**自动切换逻辑**:
```python
if bailian_quota.usage_rate >= 95%:
    if gemini_free_quota.available > 5%:
        return "gemini/gemini-2.5-flash"  # 切换到 Gemini 免费
    else:
        return "local/qwen2.5-7b"  # 切换到本地
```

**通知机制**:
```yaml
触发通知：true
通知渠道:
  - Telegram (主)
  - 飞书 (备)
通知内容:
  - "⚠️ 百炼额度已达 95%"
  - "已自动切换到 Gemini/本地模型"
  - "剩余额度：X tokens"
```

---

### 原则 3: Gemini 免费额度达 95% → 切换本地 + 百炼 ✅

**触发条件**:
```yaml
监控指标：Gemini 免费额度使用率
触发阈值：≥ 95%
切换策略:
  - 检查百炼额度是否恢复
  - 百炼可用 → 切换回百炼
  - 百炼不可用 → 切换到本地
```

**自动切换逻辑**:
```python
if gemini_quota.usage_rate >= 95%:
    if bailian_quota.available > 5%:
        return "bailian/qwen3.5-plus"  # 切回百炼
    else:
        return "local/qwen2.5-7b"  # 切换到本地
```

**通知机制**:
```yaml
触发通知：true
通知内容:
  - "⚠️ Gemini 免费额度已达 95%"
  - "已自动切换到本地/百炼模型"
```

---

### 原则 4: 百炼额度恢复 → 强制切回百炼 ✅

**优先级规则**:
```yaml
百炼额度恢复检测：每 5 分钟检查一次
切换策略：强制切回百炼 (不管 Gemini 用了多少)
理由：已付费资源优先使用
```

**自动切换逻辑**:
```python
# 每 5 分钟检查一次
if bailian_quota.available > 5% and current_model != "bailian":
    force_switch_to("bailian/qwen3.5-plus")
    log.info("百炼额度恢复，强制切回百炼 (Gemini 已用额度：{gemini_used})")
```

**覆盖规则**:
```
百炼可用 → 百炼 (优先级 1) ✅
百炼不可用 + Gemini 可用 → Gemini (优先级 2)
百炼不可用 + Gemini 不可用 → 本地 (优先级 3)
```

---

### 原则 5: 双额度耗尽 → 强制本地兜底 ✅

**触发条件**:
```yaml
条件 1: 百炼额度使用率 ≥ 100%
条件 2: Gemini 免费额度使用率 ≥ 100%
切换策略：强制使用本地模型 (无退路)
```

**自动切换逻辑**:
```python
if bailian_quota.usage_rate >= 100% and gemini_quota.usage_rate >= 100%:
    force_switch_to("local/qwen2.5-7b")
    send_alert("🚨 双额度耗尽，已强制切换到本地模型")
```

**本地模型降级策略**:
```yaml
本地模型：Qwen 2.5 7B (Ollama)
能力限制:
  - 最大上下文：8K tokens
  - 无联网搜索能力
  - 复杂推理能力有限
  - 代码生成能力中等
  
降级通知:
  - 告知用户当前使用本地模型
  - 建议简化任务复杂度
  - 提示额度重置时间
```

---

### 原则 6: 单独的 Skill ✅

**独立模块设计**:

```
skills/quota-aware-model-router/
├── SKILL.md (本文档)
├── quota_router.py (路由核心)
├── config/ (配置文件)
│   ├── bailian_config.yaml (百炼配置)
│   ├── gemini_config.yaml (Gemini 配置)
│   └── local_config.yaml (本地配置)
├── monitors/ (监控器)
│   ├── bailian_monitor.py (百炼额度监控)
│   ├── gemini_monitor.py (Gemini 额度监控)
│   └── quota_tracker.py (额度追踪器)
├── switchers/ (切换器)
│   ├── auto_switcher.py (自动切换)
│   └── force_switcher.py (强制切换)
├── notifiers/ (通知器)
│   └── quota_notifier.py (额度告警)
├── cache/ (缓存)
│   └── quota_cache.py (额度缓存)
└── tests/ (测试)
    └── test_quota_router.py
```

**独立使用**:
```python
from skills.quota_aware_model_router.quota_router import QuotaRouter

# 初始化
router = QuotaRouter()

# 自动选择模型 (基于额度)
model = router.select_model_by_quota(
    task_type="code_generation",
    complexity="high"
)
# 返回：根据额度自动选择最优模型

# 调用模型
response = router.call_model(
    model=model,
    prompt="写个 Hello World",
    track_quota=True  # 自动记录额度使用
)

# 查询额度状态
status = router.get_quota_status()
print(f"百炼：{status.bailian.usage_rate}%")
print(f"Gemini: {status.gemini.usage_rate}%")
```

---

## 📊 三层模型池架构

```
┌─────────────────────────────────────────┐
│  Layer 1: 百炼 coding plan (主力·已付费)  │
│  - qwen3.5-plus                         │
│  - qwen3-coder-plus                     │
│  优先级：1 (最高)                        │
│  额度：日/周/月                          │
└─────────────────────────────────────────┘
              ↓ (额度≥95% 时切换)
┌─────────────────────────────────────────┐
│  Layer 2: Gemini 免费额度 (辅助·免费)     │
│  - gemini-2.5-flash                     │
│  - gemini-pro                           │
│  优先级：2 (中等)                        │
│  额度：日免费 1000 次                     │
└─────────────────────────────────────────┘
              ↓ (额度≥95% 时切换)
┌─────────────────────────────────────────┐
│  Layer 3: 本地 Qwen 2.5 7B (兜底·免费)    │
│  - qwen2.5-7b (Ollama)                  │
│  优先级：3 (最低)                        │
│  额度：无限制 (本地资源)                 │
└─────────────────────────────────────────┘
```

---

## 📋 额度监控配置

### 百炼额度监控

```yaml
# config/bailian_config.yaml
bailian:
  enabled: true
  api_key: "${BAILIAN_API_KEY}"
  base_url: "https://dashscope.aliyuncs.com/v1"
  
  # 额度配置
  quota:
    daily_limit: 100000  # 日额度 (tokens)
    weekly_limit: 500000  # 周额度 (tokens)
    monthly_limit: 2000000  # 月额度 (tokens)
    
    # 告警阈值
    warning_threshold: 90%  # 90% 时警告
    switch_threshold: 95%   # 95% 时切换
    
  # 监控配置
  monitor:
    enabled: true
    check_interval: 300  # 每 5 分钟检查一次
    auto_switch: true    # 自动切换
    
  # 模型配置
  models:
    primary: "qwen3.5-plus"
    code: "qwen3-coder-plus"
    long_context: "qwen3.5-plus"
```

### Gemini 额度监控

```yaml
# config/gemini_config.yaml
gemini:
  enabled: true
  api_key: "${GEMINI_API_KEY}"
  base_url: "https://generativelanguage.googleapis.com/v1beta"
  
  # 免费额度配置
  free_quota:
    daily_limit: 1000  # 日免费次数
    # Google AI Studio 免费额度
    # https://aistudio.google.com/app/apikey
    
    # 告警阈值
    warning_threshold: 90%
    switch_threshold: 95%
    
  # 监控配置
  monitor:
    enabled: true
    check_interval: 300  # 每 5 分钟检查一次
    auto_switch: true
    
  # 模型配置
  models:
    primary: "gemini-2.5-flash"
    pro: "gemini-pro"
```

### 本地模型配置

```yaml
# config/local_config.yaml
local:
  enabled: true
  provider: "ollama"
  base_url: "http://127.0.0.1:11434"
  
  # 模型配置
  models:
    primary: "qwen2.5:7b"
    code: "qwen2.5-coder:7b"
    
  # 资源配置
  resources:
    max_context: 8192  # 最大上下文 (tokens)
    max_tokens: 4096   # 最大输出 (tokens)
    
  # 降级策略
  fallback:
    enabled: true
    notify_on_fallback: true
    suggest_simplify: true
```

---

## 🔄 智能切换流程

### 完整切换决策树

```
每次请求
    ↓
[1] 检查百炼额度
    ├─ 可用 (>5%) → 使用百炼 ✅
    └─ 不可用 (≤5%) ↓
[2] 检查 Gemini 额度
    ├─ 可用 (>5%) → 使用 Gemini
    └─ 不可用 (≤5%) ↓
[3] 使用本地模型 (兜底)
    ↓
[4] 记录额度使用
    ↓
[5] 更新缓存 (TTL 60 秒)
    ↓
[6] 后台监控 (每 5 分钟)
    ├─ 检查百炼额度是否恢复
    ├─ 恢复 → 强制切回百炼
    └─ 发送告警通知
```

### 状态机

```yaml
状态定义:
  - STATE_BAILIAN_PRIMARY: 百炼主力状态
  - STATE_GEMINI_BACKUP: Gemini 备用状态
  - STATE_LOCAL_FALLBACK: 本地兜底状态

状态转换:
  STATE_BAILIAN_PRIMARY:
    on_quota_95%: → STATE_GEMINI_BACKUP
    
  STATE_GEMINI_BACKUP:
    on_bailian_recovered: → STATE_BAILIAN_PRIMARY (强制)
    on_gemini_quota_95%: → STATE_LOCAL_FALLBACK
    
  STATE_LOCAL_FALLBACK:
    on_bailian_recovered: → STATE_BAILIAN_PRIMARY (强制)
    on_gemini_recovered: → STATE_GEMINI_BACKUP
```

---

## 📈 额度追踪与统计

### 实时追踪

```python
# 每次调用自动记录
router.track_usage(
    model="bailian/qwen3.5-plus",
    tokens_in=1000,
    tokens_out=2000,
    cost=0.00,  # 已付费
    timestamp="2026-04-08T15:32:00+08:00"
)
```

### 统计报表

```yaml
日报 (每日 23:00):
  - 百炼额度使用：X/Y tokens (Z%)
  - Gemini 使用次数：A/B 次 (C%)
  - 本地模型调用：D 次
  - 自动切换次数：E 次
  - 成本统计：¥40/月 (固定)

周报 (每周一 06:00):
  - 周额度使用统计
  - 切换趋势分析
  - 成本效益分析

月报 (每月 1 日 06:00):
  - 月度额度使用统计
  - 模型使用偏好
  - 优化建议
```

---

## 🚨 告警通知配置

### 告警级别

```yaml
级别定义:
  - INFO: 额度使用正常
  - WARNING: 额度使用≥90%
  - CRITICAL: 额度使用≥95% (触发切换)
  - EMERGENCY: 额度耗尽 (强制降级)
```

### 通知渠道

```yaml
渠道配置:
  - Telegram (主渠道)
    - enabled: true
    - bot_token: "${TELEGRAM_BOT_TOKEN}"
    - chat_id: "${TELEGRAM_CHAT_ID}"
    
  - 飞书 (备用渠道)
    - enabled: true
    - app_id: "${FEISHU_APP_ID}"
    - app_secret: "${FEISHU_APP_SECRET}"
    
  - 邮件 (备选渠道)
    - enabled: false
    - smtp_server: "smtp.qq.com"
    - recipient: "285915125@qq.com"
```

### 告警模板

```yaml
WARNING_90%: |
  ⚠️ 额度使用警告
  
  百炼 coding plan: {bailian_usage}%
  Gemini 免费额度：{gemini_usage}%
  
  建议：关注额度使用情况

CRITICAL_95%: |
  🚨 额度使用临界
  
  百炼 coding plan: {bailian_usage}% (已触发切换)
  已自动切换到：{current_model}
  
  剩余额度：{remaining_tokens}

EMERGENCY_100%: |
  🔴 额度耗尽告警
  
  百炼 coding plan: 100% (耗尽)
  Gemini 免费额度：100% (耗尽)
  已强制切换到：本地模型 (Qwen 2.5 7B)
  
  功能限制:
  - 最大上下文：8K tokens
  - 无联网搜索能力
  
  额度重置时间：{reset_time}
```

---

## 🚀 使用方式

### 基础用法

```python
from skills.quota_aware_model_router.quota_router import QuotaRouter

# 初始化
router = QuotaRouter()

# 自动选择模型 (基于额度)
model = router.select_model(
    task_type="conversation",
    complexity="normal"
)
# 返回：根据额度自动选择

# 调用模型
response = router.chat(
    model=model,
    messages=[{"role": "user", "content": "你好"}],
    track_quota=True
)

# 查询额度状态
status = router.get_quota_status()
print(status)
# 输出：
# Bailian: 85% (可用)
# Gemini: 45% (可用)
# Current: bailian/qwen3.5-plus
```

### 高级用法

```python
# 手动切换模型
router.force_switch_to("gemini/gemini-2.5-flash")

# 临时使用本地模型
with router.use_local_temporarily():
    response = router.chat(...)

# 清除额度缓存
router.clear_quota_cache()

# 重置额度统计 (新的一天)
router.reset_daily_quota()
```

### 集成到现有技能

```python
# 集成到 smart-model-router
from skills.quota_aware_model_router.quota_router import QuotaRouter

quota_router = QuotaRouter()

class SmartModelRouter:
    def select_model(self, task):
        # 优先基于额度选择
        model = quota_router.select_model(
            task_type=task.type,
            complexity=task.complexity
        )
        return model
```

---

## 🔧 配置检查清单

### 环境变量

```bash
# 百炼 API Key
export BAILIAN_API_KEY="sk-xxx"

# Gemini API Key
export GEMINI_API_KEY="xxx"

# Telegram 配置
export TELEGRAM_BOT_TOKEN="xxx"
export TELEGRAM_CHAT_ID="xxx"

# 飞书配置
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
```

### 系统检查

```bash
# 1. 检查百炼 API
curl -H "Authorization: Bearer $BAILIAN_API_KEY" \
  https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation

# 2. 检查 Gemini API
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GEMINI_API_KEY"

# 3. 检查本地 Ollama
curl http://127.0.0.1:11434/api/tags

# 4. 检查 Quota Router Skill
cd /home/nicola/.openclaw/workspace
python3 -c "from skills.quota_aware_model_router.quota_router import QuotaRouter; print('✅ QuotaRouter OK')"
```

---

## 📊 监控仪表盘

### 实时状态

```yaml
当前状态:
  主模型：bailian/qwen3.5-plus
  状态：STATE_BAILIAN_PRIMARY
  
额度使用:
  百炼：85/100 (85%) ✅
  Gemini: 450/1000 (45%) ✅
  本地：N/A (无限制)
  
今日统计:
  百炼调用：120 次
  Gemini 调用：35 次
  本地调用：5 次
  自动切换：2 次
```

### 历史趋势

```yaml
近 7 天额度使用趋势:
  - 百炼：日均 80% 使用率
  - Gemini: 日均 30% 使用率
  - 切换次数：平均 2 次/天
  
成本统计:
  - 百炼：¥40/月 (固定)
  - Gemini: ¥0 (免费)
  - 本地：¥0 (电费)
  - 总计：¥40/月
```

---

## ⚠️ 注意事项

### 1. 额度刷新时间

```yaml
百炼 coding plan:
  - 日额度：每日 00:00 刷新
  - 周额度：每周一 00:00 刷新
  - 月额度：每月 1 日 00:00 刷新

Gemini 免费额度:
  - 日免费次数：每日 00:00 (UTC) 刷新
  - 注意时区转换 (UTC+8)
```

### 2. 额度统计准确性

- 使用本地缓存 (TTL 60 秒)
- 每 5 分钟同步一次 API
- 允许±5% 误差

### 3. 切换延迟

- 检测到阈值：即时
- 执行切换：<1 秒
- 通知发送：<5 秒

### 4. 故障降级

```yaml
优先级:
  1. 百炼 API 故障 → 切换到 Gemini
  2. Gemini API 故障 → 切换到本地
  3. 本地模型故障 → 返回错误 (无降级)
```

---

## 📚 相关文件

| 文件 | 用途 | 位置 |
|------|------|------|
| `SKILL.md` | 本文档 | `skills/quota-aware-model-router/` |
| `quota_router.py` | 路由核心 | `skills/quota-aware-model-router/` |
| `bailian_config.yaml` | 百炼配置 | `skills/quota-aware-model-router/config/` |
| `gemini_config.yaml` | Gemini 配置 | `skills/quota-aware-model-router/config/` |
| `local_config.yaml` | 本地配置 | `skills/quota-aware-model-router/config/` |

---

## 🎯 下一步

- [ ] 创建 `quota_router.py` 核心实现
- [ ] 配置百炼 API Key 和额度
- [ ] 配置 Gemini API Key
- [ ] 配置额度监控器
- [ ] 配置自动切换器
- [ ] 配置告警通知
- [ ] 测试额度追踪
- [ ] 测试自动切换
- [ ] 集成到现有路由系统

---

*版本：1.0.0 | 创建时间：2026-04-08 | 状态：✅ 已创建*

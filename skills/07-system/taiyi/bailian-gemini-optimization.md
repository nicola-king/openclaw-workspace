# 百炼 + Gemini 免费额度优化策略

> 版本：v1.0 | 创建：2026-03-28 22:04
> 原则：最大化免费额度，最小化成本

---

## 📊 免费额度规则

### 百炼 Coding Plan Lite

| 项目 | 规则 |
|------|------|
| **费用** | **40 元/月 (已订阅)** |
| **额度使用目标** | **90% (最大化利用)** |
| **适用模型** | Qwen-Coder 系列 |
| **适用场景** | 代码生成/Debug/技术文档 |
| **优先级** | **⭐⭐⭐⭐⭐ (最高，已付费)** |

---

### Claude/OpenAI 免费额度

| 平台 | 免费额度 | 说明 |
|------|---------|------|
| **Claude** | ❌ 无 | 需付费订阅 |
| **OpenAI** | ❌ 无 | 新用户可能有$5 试用金 (需确认) |

**策略**: 无免费额度，仅特殊场景使用

---

### Gemini 免费额度

| 项目 | 规则 |
|------|------|
| **免费额度** | ✅ 1500 次/天 (Gemini 1.5 Flash) |
| **适用模型** | Gemini 1.5 Flash/Pro |
| **速率限制** | 15 次/分钟 (Flash) |
| **上下文长度** | 1M tokens (Flash) |
| **商业用途** | ✅ 允许 |
| **过期时间** | 永久免费 |

---

## 🎯 优化策略

### 策略 1: 额度分配

```
太一 AI 调度 (成本优先):

1. 百炼 Coding (40 元/月) ⭐⭐⭐⭐⭐
   ├── 代码生成：50%
   ├── Debug: 25%
   ├── 技术文档：15%
   └── 备用：10%
   └── 使用目标：90%/月 (已付费优先用)

2. Gemini (1500 次/天) ⭐⭐⭐⭐⭐
   ├── 文档写作：500 次
   ├── 数据分析：500 次
   ├── 翻译/总结：300 次
   └── 备用：200 次
   └── 永久免费

3. 本地 qwen2.5:7b ⭐⭐⭐⭐
   └── 简单任务/离线任务/降级备用
   └── 完全免费

4. Claude/OpenAI ❌
   └── 无免费额度，仅特殊场景使用
   └── 复杂战略决策 (按需付费)
```

---

### 策略 2: 智能路由

```python
def select_model(task):
    """智能选择模型 (考虑付费额度)"""
    
    # 检查 Gemini 剩余额度
    gemini_remaining = get_gemini_remaining_quota()
    
    # 检查百炼剩余额度 (40 元/月，目标 90% 使用率)
    bailian_remaining = get_bailian_remaining_quota()
    bailian_usage_rate = get_bailian_usage_rate()  # 使用率
    
    if task.type == 'code' or task.type == 'technical':
        # 百炼已付费，优先使用 (目标 90% 使用率)
        if bailian_usage_rate < 0.90:
            return 'bailian-coding'  # 优先使用百炼 (已付费)
        elif bailian_remaining > 0:
            return 'bailian-coding'  # 还有额度
        else:
            return 'qwen2.5-7b-local'  # 降级到本地
    
    elif task.type == 'document' or task.type == 'analysis':
        if gemini_remaining > 200:  # 保留 200 次备用
            return 'gemini'  # 使用 Gemini (免费)
        else:
            return 'qwen2.5-7b-local'  # 降级到本地
    
    elif task.type == 'simple' or task.offline:
        return 'qwen2.5-7b-local'  # 本地
    
    elif task.complexity == 'high':
        return 'claude-or-gpt'  # 付费高端
    
    else:
        return 'qwen2.5-7b-local'  # 默认本地
```

---

### 策略 3: 成本监控

**监控指标**:
- 每日 Gemini 使用量
- 每日百炼使用量
- 剩余额度告警 (80% 阈值)
- 月度成本预算

**告警规则**:
```
Gemini 使用量 > 1200 次/天 → 告警
百炼使用量 > 80% → 告警
月度成本 > 预算 → 告警
```

---

### 策略 4: 故障降级

```
降级策略:
├── Gemini 超额 → 本地 qwen2.5:7b
├── 百炼超额 → 本地 qwen2.5:7b
├── 云端不可用 → 本地 qwen2.5:7b
└── 本地不可用 → 错误提示
```

---

## 📋 实施步骤

### Step 1: 配置 API Key

```bash
# Gemini API Key
export GEMINI_API_KEY="你的 Gemini API Key"

# 百炼 API Key
export DASHSCOPE_API_KEY="你的百炼 API Key"
```

---

### Step 2: 实现额度监控

```python
# skills/taiyi/quota-monitor.py

class QuotaMonitor:
    """额度监控器"""
    
    def __init__(self):
        self.gemini_daily_limit = 1500
        self.gemini_used = 0
        self.bailian_used = 0
    
    def get_gemini_remaining(self):
        """获取 Gemini 剩余额度"""
        return self.gemini_daily_limit - self.gemini_used
    
    def should_use_gemini(self):
        """是否应该使用 Gemini"""
        remaining = self.get_gemini_remaining()
        return remaining > 200  # 保留 200 次备用
    
    def alert_if_needed(self):
        """需要时发送告警"""
        if self.gemini_used > 1200:
            send_alert("Gemini 额度即将用完")
```

---

### Step 3: 集成太一

```python
# skills/taiyi/smart-router.py

from local_ai_caller import LocalAICaller
from quota_monitor import QuotaMonitor

class SmartRouter:
    """智能路由器"""
    
    def __init__(self):
        self.local_caller = LocalAICaller()
        self.quota_monitor = QuotaMonitor()
    
    def call(self, task):
        """智能调用"""
        model = self.select_model(task)
        
        if model == 'gemini':
            return self.call_gemini(task)
        elif model == 'bailian':
            return self.call_bailian(task)
        else:
            return self.call_local(task)
```

---

## 📊 预期效果

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| **免费额度利用率** | ?% | >90% | +?% |
| **月度成本** | ?元 | <100 元 | -?% |
| **本地降级率** | ?% | <10% | -?% |

---

## 🚀 快速启动

```bash
# 1. 配置 API Key
echo 'export GEMINI_API_KEY="xxx"' >> ~/.bashrc
echo 'export DASHSCOPE_API_KEY="xxx"' >> ~/.bashrc
source ~/.bashrc

# 2. 测试额度监控
cd ~/.openclaw/workspace/skills/taiyi
python3 quota-monitor.py

# 3. 测试智能路由
python3 smart-router.py
```

---

*版本：v1.0 | 创建时间：2026-03-28 22:04*
*原则：最大化免费额度，最小化成本*
*太一 AGI · 百炼+Gemini 优化策略*

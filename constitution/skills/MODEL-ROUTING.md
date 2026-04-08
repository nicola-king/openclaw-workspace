---
name: model-routing
tier: 1
enabled: true
---
# 模型调度协议 v2.0（智能分流版）

**更新时间**: 2026-03-27 16:30  
**新增**: 本地 Qwen 2.5 7B 智能调度

---

## 🎯 智能分流架构

### 三层模型池

```
┌─────────────────────────────────────────┐
│  Layer 1: 本地模型 (免费·零延迟)          │
│  - Qwen 2.5 7B (Ollama)                 │
│  适用：快速推理·简单任务·高频调用         │
└─────────────────────────────────────────┘
              ↓ (复杂任务上移)
┌─────────────────────────────────────────┐
│  Layer 2: 云端主力 (性价比·通用)          │
│  - qwen3.5-plus (¥40/月)                │
│  适用：日常对话·中等任务·Bot 调度          │
└─────────────────────────────────────────┘
              ↓ (长文本/代码)
┌─────────────────────────────────────────┐
│  Layer 3: 云端专项 (强大·昂贵)            │
│  - Gemini 2.5 Pro (¥145/月)             │
│  - qwen3-coder-plus (代码专项)           │
│  - Claude Pro (战略决策)                 │
│  适用：长文本·复杂推理·代码·战略           │
└─────────────────────────────────────────┘
```

---

## 🤖 本地 Qwen 2.5 7B 调度规则

### 自动使用本地模型的场景

**优先级**: Layer 1 > Layer 2 > Layer 3

**自动触发本地模型**:

| 任务类型 | 示例 | 自动路由 |
|---------|------|---------|
| **简单问答** | "1+1 等于几" | ✅ Qwen 2.5 7B |
| **快速翻译** | "翻译成英文" | ✅ Qwen 2.5 7B |
| **文本润色** | "优化这句话" | ✅ Qwen 2.5 7B |
| **简单摘要** | "总结这段话" | ✅ Qwen 2.5 7B |
| **日常对话** | "你好/谢谢" | ✅ Qwen 2.5 7B |
| **事实查询** | "中国首都是？" | ✅ Qwen 2.5 7B |
| **单位换算** | "1 英里=？公里" | ✅ Qwen 2.5 7B |
| **简单计算** | "25*36=?" | ✅ Qwen 2.5 7B |

---

### 必须使用云端模型的场景

**自动上移到 Layer 2/3**:

| 条件 | 路由 | 理由 |
|------|------|------|
| **context > 10K tokens** | qwen3.5-plus | 本地模型 8K 限制 |
| **需要联网搜索** | qwen3.5-plus | 本地模型无网络 |
| **复杂推理** | qwen3.5-plus | 7B 能力有限 |
| **代码生成** | qwen3-coder-plus | 专业代码模型 |
| **长文档分析** | Gemini 2.5 Pro | 1M 上下文窗口 |
| **多来源汇总** | Gemini 2.5 Pro | 强大多文档处理 |
| **战略规划** | Claude Pro | 高质量决策 |
| **数学证明** | qwen3.5-plus | 7B 数学较弱 |

---

## 📊 智能分流决策树

```
用户请求
  ↓
[1] 是否需要联网搜索？
  ├─ 是 → qwen3.5-plus
  └─ 否 ↓
[2] 是否超过 10K tokens？
  ├─ 是 → qwen3.5-plus / Gemini
  └─ 否 ↓
[3] 是否是代码任务？
  ├─ 是 → qwen3-coder-plus
  └─ 否 ↓
[4] 是否是简单任务？
  ├─ 是 (问答/翻译/润色) → ✅ Qwen 2.5 7B (本地)
  └─ 否 (复杂推理) → qwen3.5-plus
[5] 是否是长文档/多来源？
  ├─ 是 → Gemini 2.5 Pro
  └─ 否 → qwen3.5-plus
```

---

## 🔧 本地模型调用配置

### Ollama API 端点

```json
{
  "local_model": {
    "provider": "ollama",
    "endpoint": "http://localhost:11434",
    "model": "qwen2.5:7b-instruct-q4_K_M",
    "timeout": 30,
    "max_tokens": 2048,
    "context_window": 8192
  }
}
```

---

### 调用示例

**Python 调用**:
```python
import requests

def call_local_model(prompt, max_tokens=2048):
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'qwen2.5:7b-instruct-q4_K_M',
            'prompt': prompt,
            'stream': False,
            'options': {
                'num_predict': max_tokens,
                'temperature': 0.7
            }
        }
    )
    return response.json()['response']

# 使用
result = call_local_model("你好，介绍一下你自己")
print(result)
```

---

**Bash 调用**:
```bash
# 简单调用
ollama run qwen2.5:7b-instruct-q4_K_M "你的问题"

# API 调用
curl http://localhost:11434/api/generate \
  -d '{
    "model": "qwen2.5:7b-instruct-q4_K_M",
    "prompt": "你好",
    "stream": false
  }'
```

---

## 💰 成本优化策略

### 分流比例目标

| 模型层 | 目标比例 | 月成本 | 说明 |
|--------|---------|--------|------|
| **Layer 1 (本地)** | 40% | ¥0 | 简单任务本地化 |
| **Layer 2 (云端主力)** | 40% | ¥40 | 日常对话/执行 |
| **Layer 3 (云端专项)** | 20% | ¥145 | 长文本/代码/战略 |

**预期月成本**: ¥185 (原¥330 → 节省 44%)

---

### 每日额度分配

| 模型 | 每日配额 | 优先级 | 用途 |
|------|---------|--------|------|
| **Qwen 2.5 7B** | 无限 | 最高 | 简单任务首选 |
| **qwen3.5-plus** | 100 次 | 中等 | 日常对话 |
| **Gemini 2.5 Pro** | 45 次 | 低 | 长文本专用 |

**配额耗尽 Fallback**:
```
qwen3.5-plus 耗尽 → Qwen 2.5 7B (降级)
Gemini 耗尽 → qwen3.5-plus (降级)
```

---

## 📈 任务分解与智能分配

### 复杂任务自动拆解

**示例**: "分析这份 100 页报告并生成摘要"

**自动拆解**:
```
1. 读取文档 (本地处理)
2. 分页提取文本 (本地处理)
3. 每 10 页摘要 (Qwen 2.5 7B × 10 次) ✅ 本地
4. 汇总 10 个摘要 (qwen3.5-plus × 1 次)
5. 生成最终报告 (Gemini 2.5 Pro × 1 次)
```

**成本对比**:
- 传统方式：Gemini 1 次 (¥5)
- 智能分流：Qwen 2.5 7B×10 (¥0) + qwen3.5-plus×1 (¥0.1) + Gemini×1 (¥5) = ¥5.1
- **效果**: 质量相同，成本略增但本地化率 91%

---

### Bot 任务智能分配

| Bot | 主要任务 | 默认模型 | 本地化率目标 |
|-----|---------|---------|------------|
| **知几** | 量化交易 | qwen3.5-plus | 30% (简单计算本地) |
| **山木** | 内容创作 | qwen3.5-plus | 50% (润色本地) |
| **素问** | 技术开发 | qwen3-coder-plus | 20% (文档本地) |
| **罔两** | 数据分析 | qwen3.5-plus | 40% (简单分析本地) |
| **庖丁** | 预算成本 | Qwen 2.5 7B | 80% (计算本地) ✅ |

---

## 🎯 智能分流执行流程

### Step 1: 任务分类

```python
def classify_task(user_request):
    """
    自动分类用户请求
    返回：task_type, complexity, token_estimate
    """
    # 关键词匹配
    if any(kw in user_request for kw in ['写代码', '脚本', 'bug']):
        return 'code', 'medium', 5000
    
    if any(kw in user_request for kw in ['总结', '摘要', '翻译']):
        return 'simple', 'easy', 1000
    
    if '文档' in user_request or '报告' in user_request:
        return 'long_text', 'hard', 50000
    
    # 默认
    return 'chat', 'easy', 500
```

---

### Step 2: 模型选择

```python
def select_model(task_type, complexity, token_estimate):
    """
    根据任务类型选择模型
    """
    # 本地模型优先
    if complexity == 'easy' and token_estimate < 8000:
        if task_type in ['simple', 'chat', 'calc']:
            return 'qwen2.5:7b-instruct-q4_K_M'  # ✅ 本地
    
    # 云端主力
    if complexity == 'medium' or token_estimate < 50000:
        return 'qwen3.5-plus'
    
    # 长文本/复杂
    if complexity == 'hard' or token_estimate >= 50000:
        return 'gemini-2.5-pro'
    
    # 代码
    if task_type == 'code':
        return 'qwen3-coder-plus'
    
    return 'qwen3.5-plus'  # 默认
```

---

### Step 3: 执行与监控

```python
def execute_with_monitoring(user_request):
    """
    执行任务并监控成本
    """
    # 分类
    task_type, complexity, tokens = classify_task(user_request)
    
    # 选择模型
    model = select_model(task_type, complexity, tokens)
    
    # 记录
    log_model_usage(model, task_type)
    
    # 执行
    if model == 'qwen2.5:7b-instruct-q4_K_M':
        result = call_local_model(user_request)
    else:
        result = call_cloud_model(model, user_request)
    
    # 成本统计
    update_cost_tracking(model, tokens)
    
    return result
```

---

## 📊 成本追踪与报告

### 实时统计

**文件**: `memory/model-usage-today.md`

```markdown
# 模型使用统计 · 2026-03-27

## 今日使用

| 模型 | 调用次数 | Token 数 | 估算成本 |
|------|---------|---------|---------|
| Qwen 2.5 7B (本地) | 45 | 15K | ¥0 |
| qwen3.5-plus | 28 | 50K | ¥2.5 |
| Gemini 2.5 Pro | 8 | 120K | ¥5.8 |
| qwen3-coder-plus | 3 | 10K | ¥0.5 |

## 本月累计

- 总支出：¥125 / ¥330 (38%)
- 本地化率：42%
- 平均每任务成本：¥0.15

## 告警

- [ ] Gemini 使用不足 (8 次 < 20 次/天目标)
- [ ] 本地化率达标 (42% > 40% 目标) ✅
```

---

### 每周报告

**时间**: 每周一 09:00 自动生成

**模板**:
```markdown
【模型使用统计 · 第 X 周】

## 使用统计

- Qwen 2.5 7B (本地): 315 次 (40%)
- qwen3.5-plus: 280 次 (36%)
- Gemini 2.5 Pro: 126 次 (16%)
- qwen3-coder-plus: 63 次 (8%)

## 成本分析

- 本周估算成本：¥125
- 月度累计：¥125 / ¥330
- 日均成本：¥17.8

## 调度建议

1. ✅ 本地化率 40% 达标
2. ⚠️ Gemini 使用不足 (18 次/天 < 20 次目标)
3. 💡 建议将更多长文档分析交给 Gemini

## 优化措施

- 增加 Gemini 长文本任务分配
- 简单问答优先本地模型
- 代码任务统一使用 qwen3-coder-plus
```

---

## 🚨 智能告警机制

### 成本告警

| 阈值 | 动作 | 话术 |
|------|------|------|
| **月预算 50%** | 提醒 | 「本月已用¥165/¥330，建议增加本地模型使用」 |
| **月预算 80%** | 警告 | 「本月已用¥264/¥330，请严格控制云端调用」 |
| **月预算 90%** | 降级 | 「本月已用¥297/¥330，非必要任务全部本地化」 |

---

### 配额告警

#### 百炼 (qwen3.5-plus) 配额告警 🆕

| 周期 | 阈值 | 动作 | 降级策略 |
|------|------|------|---------|
| **日用量 98%** | ⚠️ 告警 | 启动本地+Gemini 免费额度 | 简单任务→本地，长文本→Gemini |
| **周用量 98%** | ⚠️ 告警 | 启动本地+Gemini 免费额度 | 简单任务→本地，长文本→Gemini |
| **月用量 99%** | 🚨 紧急 | 全力启动本地+Gemini | 非必要任务全部本地化 |

**核心原则**: > 百炼配额告警时，仍按「本地优先·云端补充·成本最优」核心理念分配任务

**降级路由**:
```
百炼配额告警 → 任务重新分类 →
  ├─ 简单任务 → Qwen 2.5 7B (本地) ✅
  ├─ 长文档 → Gemini 2.5 Pro (免费额度)
  ├─ 代码 → qwen3-coder-plus (独立配额)
  └─ 复杂推理 → Gemini 2.5 Pro (免费额度)
```

**告警话术**:
- 98%: 「百炼本周已用 98%，已自动切换本地+Gemini 免费额度」
- 99%: 「百炼本月已用 99%，非必要任务全部本地化」

---

#### 其他模型配额告警

| 模型 | 阈值 | 动作 |
|------|------|------|
| **Gemini** | 45 次/天 | 自动切换到 qwen3.5-plus |
| **qwen3.5-plus** | 100 次/天 | 降级到 Qwen 2.5 7B |

---

## 🎯 验收标准

### 本地化率目标

| 时间 | 目标 | 验收 |
|------|------|------|
| **第 1 周** | 30% | ✅ 简单任务本地化 |
| **第 2 周** | 40% | ✅ 日常对话本地化 |
| **第 1 月** | 50% | ✅ 中等任务本地化 |

---

### 成本节约目标

| 指标 | 基线 | 目标 | 验收 |
|------|------|------|------|
| **月成本** | ¥330 | ¥185 | 节省 44% |
| **本地化率** | 0% | 40% | 简单任务本地 |
| **响应速度** | 2s | 1s | 本地零延迟 |

---

## 📄 相关文件

| 文件 | 用途 |
|------|------|
| `memory/model-usage-today.md` | 今日使用统计 |
| `memory/model-usage-weekly.md` | 本周使用统计 |
| `memory/gemini-quota.md` | Gemini 配额计数 |
| `constitution/skills/MODEL-ROUTING.md` | 本文档 |

---

## 🆕 配额智能监控与自动切换（2026-04-06 新增）

### 核心策略

**三层模型池 + 配额监控 + 自动切换**

```
┌─────────────────────────────────────────────────────────┐
│                    用户请求                              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              智能路由器 (实时检测 + 自动切换)              │
├─────────────────────────────────────────────────────────┤
│  1. 任务分类 → 简单/中等/复杂                            │
│  2. 配额检测 → 百炼状态检查 (每 5 分钟)                      │
│  3. 自动切换 → 限额时切 Gemini，恢复时切回百炼            │
└─────────────────────────────────────────────────────────┘
                          ↓
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│  L1 · 本地层   │ │  L2 · 百炼层   │ │  L3 · Gemini  │
│  Qwen 2.5 7B  │ │ qwen3.5-plus  │ │  2.5 Pro     │
│  简单问题      │ │ 中等/代码任务  │ │  限额备用     │
│  ¥0           │ │ ¥0.05/1K      │ │  免费额度     │
└───────────────┘ └───────────────┘ └───────────────┘
```

---

### 分流规则（优先级排序）

#### 规则 1：简单问题 → 本地 7B（最高优先级）

**触发条件**（满足任一）：
- 问候/寒暄（你好/谢谢/再见）
- 简单问答（几点/天气/定义/是什么）
- Token 估算 < 2000
- 复杂度 = easy

**路由**：
```
本地 Qwen 2.5 7B (qwen2.5:7b-instruct-q4_K_M)
- 端点：http://localhost:11434/api/generate
- 成本：¥0
- 延迟：<3 秒
- 本地化率贡献：+50%
```

---

#### 规则 2：中等任务 → 百炼 Coding Plan（优先）/ Gemini（备用）

**触发条件**：
- 代码任务（写函数/debug/优化）
- 文档/报告/分析
- Token 估算 2000-50000
- 复杂度 = medium

**路由**（百炼正常时）：
```
百炼 qwen3.5-plus
- 端点：https://dashscope.aliyuncs.com/...
- 成本：¥0.05/1K tokens
- 延迟：5-10 秒
```

**路由**（百炼限额时）：
```
Gemini 2.5 Pro（免费额度）
- 端点：https://generativelanguage.googleapis.com/...
- 成本：¥0（免费额度内）
- 延迟：10-20 秒
```

---

#### 规则 3：复杂任务 → Gemini 2.5 Pro（始终）

**触发条件**（满足任一）：
- Token 估算 > 50000
- 复杂度 = hard
- 长文档处理（>50 页）
- 多模态任务

**路由**：
```
Gemini 2.5 Pro
- 端点：https://generativelanguage.googleapis.com/...
- 成本：¥0（免费额度）
- 延迟：15-30 秒
- 上下文：1M+ tokens
```

---

### 百炼配额监控机制

#### 检测频率

**每 5 分钟自动检查**（Cron 定时任务）

```cron
*/5 * * * * python3 /home/nicola/.openclaw/workspace/scripts/check-bailian-quota.py
```

---

#### 检测方法

1. **API 轻量探测**（最小 token 消耗）
2. **响应状态码分析**
3. **错误消息解析**（配额相关关键词）

**配额状态定义**：

| 状态 | 条件 | 动作 |
|------|------|------|
| **normal** | API 调用成功，无配额警告 | 使用百炼 |
| **warning** | 接近配额上限（>90%） | 准备切换，记录日志 |
| **exhausted** | API 返回配额错误 | 立即切换到 Gemini |

---

### 自动切换逻辑

#### 切换触发（百炼 → Gemini）

**条件**（满足任一）：
1. API 返回 `QuotaExceeded` 错误
2. API 返回 `RateLimitExceeded` 错误
3. 连续 3 次调用失败（非网络原因）

**动作**：
```python
1. 记录切换事件（时间/原因/当前任务）
2. 更新状态文件：current_model = "gemini-2.5-pro"
3. 发送通知（可选）：「百炼配额耗尽，已切换到 Gemini」
4. 当前任务重试（使用 Gemini）
5. 后续任务默认使用 Gemini
```

---

#### 切换回切（Gemini → 百炼）

**条件**（全部满足）：
1. 距离上次切换 > 30 分钟（避免频繁切换）
2. 百炼 API 探测成功（连续 3 次）
3. 当前时间非高峰时段（可选，02:00-06:00）

**动作**：
```python
1. 记录回切事件（时间/原因）
2. 更新状态文件：current_model = "qwen3.5-plus"
3. 发送通知（可选）：「百炼配额已恢复，已切换回 Coding Plan」
4. 后续任务默认使用百炼
```

---

### 状态文件

**位置**：`/home/nicola/.openclaw/workspace/data/model-router-status.json`

**格式**：
```json
{
  "current_model": "qwen3.5-plus",
  "bailian_status": "normal",
  "last_check": "2026-04-06T22:28:00+08:00",
  "last_switch_to_gemini": null,
  "last_switch_to_bailian": "2026-04-06T10:00:00+08:00",
  "switch_count_today": 0,
  "consecutive_failures": 0,
  "notes": ""
}
```

---

### 监控脚本

#### check-bailian-quota.py

**功能**：
- 每 5 分钟检查百炼配额状态
- 自动触发切换逻辑
- 记录状态变更

**用法**：
```bash
python3 /home/nicola/.openclaw/workspace/scripts/check-bailian-quota.py
```

---

#### model-router-executor.py（升级 v2.0）

**新增功能**：
1. 读取状态文件，获取当前可用模型
2. 任务分类时考虑配额状态
3. 自动选择最佳可用模型

**路由优先级**：
```
简单任务 → 本地 7B（无论配额状态）
中等任务 → 百炼（normal）/ Gemini（exhausted）
复杂任务 → Gemini（始终）
```

---

### 使用统计与报告

#### 日志格式

```
时间 | 模型 | 任务类型 | Token 数 | 成本 | 状态
```

**文件**：`memory/model-usage-today.md`

---

#### 核心指标

| 指标 | 目标 | 监控 |
|------|------|------|
| 本地模型使用率 | >50%（简单任务） | 每日统计 |
| 百炼配额使用率 | <95% | 每 5 分钟监控 |
| 切换次数/天 | <5 次 | 防止频繁切换 |
| 平均响应延迟 | <10 秒 | 性能监控 |
| 成本/天 | <¥50 | 预算控制 |

---

### 配置项

#### 环境变量

```bash
# 百炼 API Key
export DASHSCOPE_API_KEY="sk-xxx"

# Gemini API Key
export GEMINI_API_KEY="xxx"

# 本地 Ollama 端点
export OLLAMA_ENDPOINT="http://localhost:11434"

# 切换阈值
export BAILIAN_WARNING_THRESHOLD=0.90
export BAILIAN_SWITCH_COOLDOWN=1800  # 30 分钟
```

---

### 快速启动

```bash
# 1. 配置 API Keys
export DASHSCOPE_API_KEY=sk-xxx
export GEMINI_API_KEY=xxx

# 2. 启动监控（Cron 自动）
# */5 * * * * python3 scripts/check-bailian-quota.py

# 3. 测试路由
python3 scripts/model-router-executor.py "你好"  # 应使用本地
python3 scripts/model-router-executor.py "写一个 Python 函数"  # 百炼/Gemini
```

---

### 相关文件

| 文件 | 用途 |
|------|------|
| `constitution/skills/MODEL-ROUTING-QUOTA.md` | 配额分流策略详情 |
| `scripts/check-bailian-quota.py` | 配额监控脚本 |
| `scripts/model-router-executor.py` | 路由执行器（v2.0） |
| `data/model-router-status.json` | 实时状态文件 |
| `memory/model-usage-today.md` | 使用统计日志 |

---

*版本：v3.0 | 更新时间：2026-04-06 22:45 | 状态：✅ 生效中*

*「三层模型池 + 配额监控 + 自动切换：本地优先·云端补充·成本最优·智能分流」*

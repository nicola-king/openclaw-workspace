# 大模型额度智能分流策略 v1.0

> 创建时间：2026-04-06 22:28 | 状态：✅ 激活 | 依据：AUTO-EXEC.md

---

## 🎯 核心策略

### 三层模型池架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户请求                              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              智能路由器 (实时检测 + 自动切换)              │
├─────────────────────────────────────────────────────────┤
│  1. 任务分类 → 简单/中等/复杂                            │
│  2. 配额检测 → 百炼状态检查                              │
│  3. 自动切换 → 限额时切 Gemini，恢复时切回百炼            │
└─────────────────────────────────────────────────────────┘
                          ↓
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│  L1 · 本地层   │ │  L2 · 百炼层   │ │  L3 · Gemini  │
│  Qwen 2.5 7B  │ │ qwen3.5-plus  │ │  2.5 Pro     │
│  简单问题      │ │ 中等/代码任务  │ │  限额备用     │
│  ¥0/1K tokens │ │ ¥0.05/1K      │ │  免费额度     │
└───────────────┘ └───────────────┘ └───────────────┘
```

---

## 📊 分流规则

### 规则 1：简单问题 → 本地 7B

**触发条件**（满足任一）：
- 问候/寒暄（你好/谢谢/再见）
- 简单问答（几点/天气/定义）
- Token 估算 < 2000
- 复杂度 = easy

**路由**：
```
本地 Qwen 2.5 7B (qwen2.5:7b-instruct-q4_K_M)
- 端点：http://localhost:11434/api/generate
- 成本：¥0
- 延迟：<3 秒
```

---

### 规则 2：中等任务 → 百炼 Coding Plan（优先）

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

### 规则 3：复杂任务 → Gemini 2.5 Pro

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

## 🚨 百炼配额监控

### 检测机制

**频率**：每 5 分钟检查一次

**检测方法**：
1. API 调用尝试（轻量探测）
2. 响应状态码分析
3. 错误消息解析（配额相关关键词）

**配额状态**：
```json
{
  "status": "normal|warning|exhausted",
  "last_check": "2026-04-06T22:28:00+08:00",
  "current_model": "qwen3.5-plus|gemini-2.5-pro",
  "switch_count_today": 0,
  "notes": "可选备注"
}
```

---

### 状态定义

| 状态 | 条件 | 动作 |
|------|------|------|
| **normal** | API 调用成功，无配额警告 | 使用百炼 |
| **warning** | 接近配额上限（>90%） | 准备切换，记录日志 |
| **exhausted** | API 返回配额错误 | 立即切换到 Gemini |

---

## 🔄 自动切换逻辑

### 切换触发（百炼 → Gemini）

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

### 切换回切（Gemini → 百炼）

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

## 📁 状态文件

### 位置
```
/home/nicola/.openclaw/workspace/data/model-router-status.json
```

### 格式
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

## 🛠️ 监控脚本

### check-bailian-quota.py

**功能**：
- 每 5 分钟检查百炼配额状态
- 自动触发切换逻辑
- 记录状态变更

**用法**：
```bash
python3 scripts/check-bailian-quota.py
```

**Cron 配置**：
```cron
*/5 * * * * python3 /home/nicola/.openclaw/workspace/scripts/check-bailian-quota.py
```

---

### model-router-executor.py（升级）

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

## 📊 使用统计

### 日志格式
```
时间 | 模型 | 任务类型 | Token 数 | 成本 | 状态
```

### 日报生成
```bash
python3 scripts/generate-model-usage-report.py --date 2026-04-06
```

### 核心指标
| 指标 | 目标 |
|------|------|
| 本地模型使用率 | >50%（简单任务） |
| 百炼配额使用率 | <95% |
| 切换次数/天 | <5 次 |
| 平均响应延迟 | <10 秒 |
| 成本/天 | <¥50 |

---

## 🔧 配置项

### 环境变量
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

### 配置文件
```
~/.openclaw/config/model-router.yaml
```

---

## 🚀 快速启动

### 1. 安装依赖
```bash
pip install dashscope google-generativeai ollama
```

### 2. 配置 API Keys
```bash
echo "export DASHSCOPE_API_KEY=sk-xxx" >> ~/.bashrc
echo "export GEMINI_API_KEY=xxx" >> ~/.bashrc
source ~/.bashrc
```

### 3. 启动监控
```bash
# 手动运行
python3 scripts/check-bailian-quota.py

# 或配置 Cron
crontab -e
# 添加：*/5 * * * * python3 /home/nicola/.openclaw/workspace/scripts/check-bailian-quota.py
```

### 4. 测试路由
```bash
# 简单任务（应使用本地）
python3 scripts/model-router-executor.py "你好，介绍一下你自己"

# 中等任务（应使用百炼或 Gemini）
python3 scripts/model-router-executor.py "写一个 Python 函数，计算斐波那契数列"

# 复杂任务（应使用 Gemini）
python3 scripts/model-router-executor.py "分析这份 100 页的 PDF 文档，总结核心观点"
```

---

## 📝 实施清单

- [ ] 创建状态文件 `data/model-router-status.json`
- [ ] 实现 `check-bailian-quota.py` 监控脚本
- [ ] 升级 `model-router-executor.py` 支持自动切换
- [ ] 配置 Cron 定时任务（每 5 分钟检查）
- [ ] 测试百炼限额模拟切换
- [ ] 测试百炼恢复模拟回切
- [ ] 生成使用统计报表
- [ ] 文档化到 `MODEL-ROUTING.md`

---

## 🔮 未来扩展

- [ ] 多云备份（阿里云 + 腾讯云 + 火山引擎）
- [ ] 动态负载均衡（基于延迟/成本实时优化）
- [ ] 预测性切换（基于使用趋势预测配额耗尽时间）
- [ ] 成本优化建议（周报/月报）
- [ ] 模型性能基准测试（自动选择最优模型）

---

*创建时间：2026-04-06 22:28 | 版本：v1.0 | 状态：✅ 激活*
*依据：AUTO-EXEC.md · 智能自动化立即执行*

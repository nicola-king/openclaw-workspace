# 分级模型调度方案

**评估时间**: 2026-03-30 21:05
**评估人**: 太一

---

## 🎯 核心思想

**简单任务用小模型，复杂任务用大模型**

类似 MemOS 的分级模型策略，实现 Token 节省 + 响应速度优化。

---

## 📊 模型分级

| 级别 | 模型 | 场景 | Token 成本 | 响应速度 |
|------|------|------|-----------|---------|
| **L1 轻量** | qwen2.5-1.5B (本地) | 简单查询、分类、摘要 | ~0 (本地) | <1s |
| **L2 主力** | qwen3.5-plus (百炼) | 常规对话、任务执行 | 中 | 5-10s |
| **L3 增强** | Gemini 2.5 Pro | 复杂推理、长文本 | 高 | 10-30s |

---

## 🔧 路由策略

### 规则引擎

```python
def route_model(query: str, context: dict) -> str:
    """
    模型路由决策
    """
    # L1: 简单查询
    if len(query) < 50 and '?' in query:
        return "qwen2.5-1.5B"
    
    # L3: 复杂推理
    if any(kw in query.lower() for kw in ['分析', '对比', '评估', '为什么', '如何']):
        if len(query) > 500 or context['complexity'] > 0.7:
            return "gemini-2.5-pro"
    
    # L2: 默认主力
    return "qwen3.5-plus"
```

### 触发条件

| 条件 | 模型 | 示例 |
|------|------|------|
| **查询长度 <50 字** | L1 轻量 | "现在几点？" |
| **事实性查询** | L1 轻量 | "币安 API 端口是多少？" |
| **常规对话** | L2 主力 | "帮我分析这个任务" |
| **复杂推理** | L3 增强 | "对比 MemOS 和 TurboQuant 的优劣" |
| **长文本处理** | L3 增强 | ">50 页文档分析" |

---

## 📊 预期收益

### Token 节省估算

**当前**: 100% 使用 qwen3.5-plus

**分级后**:
- L1 轻量：20% 查询 (本地，~0 Token)
- L2 主力：60% 查询 (qwen3.5-plus)
- L3 增强：20% 查询 (Gemini 2.5 Pro)

**节省计算**:
```
原成本：100% × qwen3.5-plus = 100%
新成本：20% × 0 + 60% × 100% + 20% × 150% = 90%
节省率：(100% - 90%) / 100% = 10%
```

### 响应速度优化

| 场景 | 当前 | 分级后 | 提升 |
|------|------|--------|------|
| 简单查询 | 5-10s | <1s | **5-10x** |
| 常规对话 | 5-10s | 5-10s | - |
| 复杂推理 | 5-10s | 10-30s | -1x (但更准确) |

---

## 🔧 实现方案

### 方案 A: 本地模型 (Ollama)

**安装**:
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:1.5b
```

**调用**:
```python
import requests

def query_local(prompt: str) -> str:
    response = requests.post('http://localhost:11434/api/generate', json={
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": False
    })
    return response.json()['response']
```

### 方案 B: 百炼 API 多模型

**配置**:
```json
{
  "models": {
    "light": "qwen2.5-1.5b-instruct",
    "standard": "qwen3.5-plus",
    "advanced": "gemini-2.5-pro"
  }
}
```

### 方案 C: 宪法路由 (太一自主)

**实现**:
```python
# constitution/skills/MODEL-ROUTING.md 规则
# 太一根据任务复杂度自主决策

if task.type == "simple_query":
    use_model("qwen2.5-1.5B")
elif task.type == "complex_analysis":
    use_model("gemini-2.5-pro")
else:
    use_model("qwen3.5-plus")  # default
```

---

## 📋 推荐方案

**太一推荐**: 方案 C (宪法路由) + 方案 A (本地 Ollama)

**理由**:
- ✅ 太一自主决策 (符合宪法)
- ✅ 本地模型零成本 (20% 查询免费)
- ✅ 灵活扩展 (按需添加模型)

**实施步骤**:
1. 安装 Ollama + qwen2.5:1.5b
2. 更新 MODEL-ROUTING.md 宪法
3. 太一根据任务自主路由
4. 监控 Token 使用，优化路由规则

---

## 📊 验收标准

| 检查项 | 目标 | 状态 |
|--------|------|------|
| Ollama 安装 | ✅ 运行正常 | 🔴 待执行 |
| 模型路由规则 | ✅ 宪法更新 | 🔴 待执行 |
| Token 节省测量 | +10% | 🔴 待验证 |
| 响应速度 | 简单查询 <1s | 🔴 待验证 |

---

## 🎯 决策

**阶段 3 实施**:
- ✅ FTS5 全文检索 (立即实施，+10% 节省)
- 🟡 分级模型调度 (本周实施，+10% 节省)
- ❌ 向量检索 (暂缓，收益有限)

**阶段 3 预期总节省**: 10% + 10% = **20%**

**累计节省**: 阶段 2 (52%) + 阶段 3 (20%) = **72%** (达到 MemOS 水平)

---

*评估人：太一 | 时间：2026-03-30 21:05*

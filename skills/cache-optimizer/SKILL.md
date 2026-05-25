# 大模型缓存命中优化层 v1.0

> **宪法级**: 所有 Agent 经此层调用 LLM，不得直接调用 SDK
> **目标**: 命中率 ≥ 70%，连续 miss ≤ 5 次

---

## 10 条宪法铁律

| # | 铁律 | 违规后果 |
|---|------|---------|
| 1 | 静态内容前置，动态内容后置 | 缓存永远miss |
| 2 | System Prompt 开头绝不插入时间戳/用户ID/UUID | 每次miss |
| 3 | 静态部分不足阈值自动填充 | 短prompt不缓存 |
| 4 | 对话历史只追加，不修改 | 已缓存前缀失效 |
| 5 | 工具定义顺序固定 | 排列变化=缓存失效 |
| 6 | 禁用实时搜索(enable_search=False) | 实时内容破坏前缀 |
| 7 | seed 参数固定(支持的模型必传) | 输出不可复现 |
| 8 | temperature=0.1(不影响缓存) | 输出不稳定 |
| 9 | 连续5次miss自动告警 | 及时发现问题 |
| 10 | 总命中率<70%触发宪法违规 | 系统需要审查 |

---

## 支持模型

| 模型 | 缓存类型 | 命中费用 | 最小阈值 | 策略 |
|------|---------|:--------:|:--------:|------|
| **DeepSeek** | 自动前缀 | 免费 🆓 | 1024 tok | seed=42, temp=0.1 |
| **Qwen** | 自动前缀 | 50%折扣 | 1024 tok | enable_search=False |
| **Claude** | 显式标记 | 10%费用 | 1024 tok | 4个cache_control断点 |
| **OpenAI** | 自动前缀 | 50%折扣 | 1024 tok | seed=42 |

---

## 使用

```python
from skills.cache-optimizer.core import (
    build_cached_prompt,
    prefix_hash,
    check_cache_killers,
    CacheMonitor,
    constitution_check,
)

# 构建缓存优化 prompt
system = build_cached_prompt(
    role_def=ROLE,              # 永不变化
    knowledge=DOCS,             # 会话级不变
    tools=TOOLS,                # 功能模块固定
    dynamic_ctx=f"用户: {name}", # 放最后
    provider="deepseek",
)

# 监控
monitor = CacheMonitor()
monitor.record("deepseek", hit_tokens=123, total_tokens=1000)
monitor.report()
```

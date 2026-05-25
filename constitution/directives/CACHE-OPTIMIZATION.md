---
name: cache-optimization
tier: 1
enabled: true
---
# 大模型缓存命中优化宪章

## 核心原则

大模型调用是太一系统的核心成本。缓存命中率直接决定系统运行成本和响应速度。
本宪章定义 10 条不可违反的铁律，确保每次 LLM 调用都以最高缓存命中率为目标。

每条铁律都对应 `skills/cache-optimizer/core.py` 中的具体实现。

---

## 10 条宪法铁律

### 铁律 1：静态前置，动态后置

System Prompt 必须按以下顺序组装：
```
Layer 1（最静）→ 角色定义（100% 相同）
Layer 2（较静）→ 知识库（会话级不变）
Layer 3（半静）→ 工具定义 + 示例（功能模块固定）
Layer 4（动态）→ 用户输入等变化内容
```

### 铁律 2：前缀绝对纯净

System Prompt **开头部分**（Layer 1-3）绝不插入：
- 时间戳（`datetime.now()`、`2026-05-25`）
- 用户 ID / 会话 ID
- UUID / 随机值 / nonce / salt
- `current_time`、`today` 等动态引用

违反后果：每次请求前缀不同 → 缓存永远 miss。

### 铁律 3：不足阈值自动填充

静态部分的总 token 数必须超过各模型的最小缓存阈值：
- DeepSeek ≥ 1024 tokens
- Qwen ≥ 1024 tokens
- Claude ≥ 1024 tokens

不足时使用 `_CACHE_PADDING`（内容恒定，不破坏前缀）自动填充。

### 铁律 4：历史消息只追加，不修改

多轮对话中，已发送的历史消息不得：
- 重新排序
- 编辑内容
- 删除后重发

违反后果：已缓存的前缀 → 之后全部失效。

### 铁律 5：工具定义顺序固定

所有 tools/functions 定义按**功能分组 + 字母排序**，
每次请求保持一致，不随机排列。

### 铁律 6：禁用实时搜索

Qwen 调用时必须设置 `enable_search=False`。
Grok 调用时不传 `search_parameters`。
实时搜索结果会注入动态内容，破坏缓存前缀。

### 铁律 7：seed 参数固定

支持的模型（DeepSeek/Qwen/OpenAI）必须传递固定 seed（默认 42）。
seed 不影响缓存但提高输出可复现性。

### 铁律 8：temperature 固定

`temperature=0.1`（低随机性 → 提高一致性）。
temperature 不影响缓存命中率，但稳定输出有助于调试。

### 铁律 9：连续 miss 自动告警

连续 5 次调用缓存未命中 → 自动触发告警。
可能的原因：
- 缓存被清除（服务器端）
- prompt 结构发生变化
- 模型版本更新

### 铁律 10：总命中率 ≥ 70%

系统整体缓存命中率不得低于 70%。
低于阈值 → 触发宪法违规审查 → 查找根因 → 修复。

---

## 实现

缓存优化层实现见 `skills/cache-optimizer/core.py`。
所有 Agent 必须经此层调用 LLM，不得直接调用 SDK。

监控报告通过 `CacheMonitor.report()` 输出，含：
- 调用次数 / 命中次数 / 未命中次数
- 按模型分类的命中率
- 宪法合规状态
- 总节省 token 数

---

## 扩展：四层文件/数据缓存

> 实现见 `skills/cache-engine/core.py`
> 覆盖范围：文件读取、会话上下文、函数结果、持久化记忆

### 铁律（补充）

| # | 铁律 | 说明 |
|---|------|------|
| 11 | **读文件强制走缓存** | `engine.read_file()` 统一入口，禁止直接 `open()` |
| 12 | **命中率硬指标 > 90%** | 12 小时健康检查自愈，低于阈值触发告警 |
| 13 | **命中时禁止传全文给 LLM** | 只传摘要 `[CACHE:hash] 预览... (N chars)` |
| 14 | **LRU 200 条上限** | result/memory 层自动 LRU 淘汰 |
| 15 | **7 天过期自动清理** | health_check 自动清理过期条目 |

### 架构

```
Layer 1: File Cache    文件内容缓存 → 读一次，永远缓存，直到文件 mtime 变化
Layer 2: Context Cache  上下文缓存 → TTL 可控（默认 1 小时）
Layer 3: Result Cache   结果缓存 → LRU + 摘要提取，命中时用摘要替代全文
Layer 4: Memory Cache   持久化记忆 → LRU 200 + 7 天过期 + 磁盘持久化
```

### 使用

```python
from skills.cache-engine.core import _get_engine

cache = _get_engine("main")

# Layer 1: 读文件
content, from_cache = cache.read_file("data/buyers.md")
digest, _ = cache.read_file_digest("data/buyers.md")  # 命中时只返回摘要

# Layer 2: 上下文
cache.set_context("session:user123", {"product": "折叠房屋"}, ttl=3600)
ctx, hit = cache.get_context("session:user123")

# Layer 3: 结果
cache.cache_result("search:buyers:Australia", results, ttl=300)
res, hit = cache.get_result("search:buyers:Australia")

# Layer 4: 记忆
cache.set_memory("user_profile", {"company": "重庆兴旺"})
profile, hit = cache.get_memory("user_profile")

# 健康检查
health = cache.health_check()
```

### 自检自愈

每 12 小时自动：
1. 检查各层命中率
2. 清理 7 天过期条目
3. 检查 LRU 是否超限
4. 重建持久化索引
5. 命中率 < 90% → 记录问题

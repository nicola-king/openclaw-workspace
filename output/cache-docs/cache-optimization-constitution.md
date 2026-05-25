# 太一 · 大模型缓存命中优化宪章

> 宪法级别：Tier 1 | 生效时间：2026-05-25
> 状态：✅ 已签署生效

---

## 核心原则

大模型调用是太一系统的核心成本。缓存命中率直接决定系统运行成本和响应速度。
本宪章定义不可违反的铁律，确保每次 LLM 调用都以最高缓存命中率为目标。

---

## 第一部分：LLM Prompt 缓存（10 条铁律）

> 实现层：`skills/cache-optimizer/core.py`

### 铁律 1：静态前置，动态后置

System Prompt 必须按以下顺序组装：

```
Layer 1（最静） → 角色定义（100% 相同，必然命中）
Layer 2（较静） → 知识库（会话级不变，首次 miss 后续全 hit）
Layer 3（半静） → 工具定义 + 示例（功能模块固定）
Layer 4（动态） → 用户输入等变化内容（放最后，不污染前缀）
```

### 铁律 2：前缀绝对纯净

System Prompt 开头部分（Layer 1-3）绝不插入：

- ❌ 时间戳（`datetime.now()`、`2026-05-25`）
- ❌ 用户 ID / 会话 ID
- ❌ UUID / 随机值 / nonce / salt
- ❌ `current_time`、`today` 等动态引用

违反后果：每次请求前缀不同 → 缓存永远 miss。

检测函数：`check_cache_killers()`

### 铁律 3：不足阈值自动填充

静态部分的总 token 数必须超过各模型的最小缓存阈值：

| 模型 | 最小阈值 | 填充策略 |
|------|:--------:|---------|
| DeepSeek | 1024 tok | 自动填充恒定内容 |
| Qwen | 1024 tok | 自动填充恒定内容 |
| Claude | 1024 tok | 自动填充恒定内容 |

填充内容恒定不变，不破坏缓存前缀。

### 铁律 4：历史消息只追加，不修改

多轮对话中，已发送的历史消息不得：

- 重新排序
- 编辑内容
- 删除后重发

违反后果：已缓存的前缀 → 之后全部失效。

### 铁律 5：工具定义顺序固定

所有 tools/functions 定义按功能分组 + 字母排序，每次请求保持一致，不随机排列。

### 铁律 6：禁用实时搜索

- Qwen 调用时必须设置 `enable_search=False`
- Grok 调用时不传 `search_parameters`
- 实时搜索结果会注入动态内容，破坏缓存前缀

### 铁律 7：seed 参数固定

支持的模型（DeepSeek / Qwen / OpenAI）必须传递固定 seed（默认 42）。

seed 不影响缓存但提高输出可复现性。

### 铁律 8：temperature 固定

`temperature=0.1`（低随机性 → 提高一致性）。

temperature 不影响缓存命中率，但稳定输出有助于调试。

### 铁律 9：连续 miss 自动告警

连续 5 次调用缓存未命中 → 自动触发告警。

可能的原因：
- 缓存被服务器清除
- prompt 结构发生变化
- 模型版本更新

### 铁律 10：总命中率 ≥ 70%

系统整体缓存命中率不得低于 70%。

低于阈值 → 触发宪法违规审查 → 查找根因 → 修复。

---

## 第二部分：文件/数据四层缓存（补充 5 条铁律）

> 实现层：`skills/cache-engine/core.py`

### 铁律 11：读文件强制走缓存

统一通过 `engine.read_file()` 入口读取文件。

禁止直接 `open()` 读取——除非文件首次加载或 mtime 变化。

### 铁律 12：命中率硬指标 > 90%

每 12 小时自动健康检查，检测各层命中率。

命中率 < 90% → 记录问题 → 触发自愈。

### 铁律 13：命中时禁止传全文给 LLM

命中时只返回摘要，不传全文。

摘要格式：`[CACHE:hash] 预览内容前200字符... (N chars)`

落地函数：`read_file_digest()` / `get_result_digest()`

### 铁律 14：LRU 200 条上限

result 层和 memory 层自动 LRU 淘汰。

超出 200 条时淘汰最久未使用的条目。

### 铁律 15：7 天过期自动清理

health_check 自动清理 7 天前的过期条目。

context 层除 LRU 外还受 TTL（默认 1 小时）约束。

---

## 第三部分：四层缓存架构

```
                   ┌──────────────────────────────────┐
                   │     应用程序 / Agent              │
                   └──────────┬───────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
      Layer 1 File      Layer 2 Context   Layer 3 Result
      ┌──────────┐     ┌──────────┐     ┌──────────┐
      │文件内容   │     │会话上下文 │     │函数结果   │
      │mtime感知  │     │TTL 1小时  │     │LRU + 摘要 │
      │永久有效   │     │会话级    │     │5分钟TTL   │
      └──────────┘     └──────────┘     └──────────┘
                              │
                              ▼
                      Layer 4 Memory
                      ┌──────────────┐
                      │持久化记忆     │
                      │LRU 200 + 7天  │
                      │磁盘持久化     │
                      └──────────────┘
                              │
                              ▼
                      Layer 0 (前置)
                      ┌──────────────┐
                      │LLM Prompt    │
                      │前缀缓存       │
                      │10条宪法铁律   │
                      └──────────────┘
```

---

## 第四部分：自检自愈

每 12 小时自动执行：

| 检查项 | 方法 | 自愈动作 |
|--------|------|---------|
| 各层命中率 | `health_check()` | 命中率 < 90% 记录问题 |
| 过期条目 | `clean_expired()` | 清理 7 天前条目 |
| LRU 超限 | `_enforce_lru()` | 淘汰最久未使用 |
| 持久化索引 | `rebuild_index()` | 扫描磁盘重建索引 |
| 缓存杀手检测 | `check_cache_killers()` | 报告违规模式 |

---

## 使用速查

### LLM Prompt 缓存

```python
from skills.cache-optimizer.core import build_cached_prompt, CacheMonitor

# 构建缓存优化 prompt
system = build_cached_prompt(
    role_def=ROLE,         # Layer 1：永不变化
    knowledge=DOCS,        # Layer 2：会话级不变
    tools=TOOLS,           # Layer 3：功能模块固定
    dynamic_ctx=CTX,       # Layer 4：动态内容放最后
    provider="deepseek",   # 自动适配模型特性
)

# 监控命中率
monitor = CacheMonitor()
monitor.record(provider, hit_tokens=H, total_tokens=T)
monitor.report()
```

### 文件/数据缓存

```python
from skills.cache-engine.core import _get_engine

cache = _get_engine("main")

# 读文件（强制走缓存）
content, from_cache = cache.read_file("data/buyers.md")

# 命中时只取摘要（不传全文给LLM）
digest, _ = cache.read_file_digest("data/buyers.md")

# 缓存函数结果
cache.cache_result("search:buyers:AU", results, ttl=300)
res, hit = cache.get_result("search:buyers:AU")

# 持久化记忆
cache.set_memory("user_profile", {"company": "重庆兴旺"})

# 健康检查
health = cache.health_check()
```

---

**维护：太一 · 2026-05-25**
**文件位置：`skills/cache-optimizer/core.py` + `skills/cache-engine/core.py`**

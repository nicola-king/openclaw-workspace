# Agent 并行化能力演进趋势 · 调研报告

> 生成日期：2026-05-09 | 调研者：太一子Agent
> 目标：为「跨境贸易 Agent」搜索 Agent v4（Scrapling 自适应搜索）提供并行化升级方案

---

## 一、调研摘要

本报告调研了三个领域的最新并行化演进：
1. **Codex/CLI Agent 跨标签并行运行** — codex-yolo、nexus-mcp、golutra 等项目的实践
2. **Agent Workflow 并行化模式** — LangGraph、LangChain Agent 生态的 token 效率与 multi-agent 编排
3. **Web Scraper 层面的并行化** — Scrapling（⭐47.8K）的 Spider 系统、AsyncSession 等原生能力

核心发现：**并行化已从「基础设施层面」进化到「架构模式层面」** — 不再只是 `asyncio.gather`，而是包含智能并发控制、领域敏感度调节、代理自动轮换、多模型协作编排等多个维度。

---

## 二、关键发现

### 2.1 Codex / CLI Agent 并行运行

| 项目 | ⭐Stars | 并行方式 | 能力边界 |
|------|---------|---------|---------|
| **codex-yolo** | 9 | tmux 多窗格并行 + git worktree 隔离 | 每 agent 独立目录，可跑多个 Codex CLI 实例并行，auto-approve 模式 |
| **nexus-mcp** | 2 | MCP Server 用 `asyncio.gather` + semaphore(3) | 将 Codex/Claude/Gemini/OpenCode 等 CLI agent 封装为 MCP 工具，支持并行调用 |
| **golutra** | 3.4K | Rust+Tauri 桌面应用，多 agent 并行编排 | 统一编排 Claude Code/Codex/Gemini/Qwen/OpenClaw，并行执行 + 日志聚合 |

**实现方式对比：**
- codex-yolo 用的是 **OS 级并行**（tmux + git worktree 隔离），每个 agent 在独立终端运行
- nexus-mcp 是 **应用级并行**（Python asyncio + semaphore 限流），MCP 协议跨模型调用
- golutra 是 **桌面级编排**（Rust 调度 + Web 监控），最接近「AI 员工管理」概念

**关键洞察**：Codex CLI 本身不支持跨标签并行，社区通过在外部层用 tmux/MCP 包装来实现并行。这也意味着**并行化不需要 agent 原生支持**，可以在编排层实现。

### 2.2 Agent Workflow 并行化模式

| 模式 | 代表实现 | 适用场景 |
|------|---------|---------|
| **Fan-out 扇出** | LangGraph `send()` API | 同一任务分发给多个子 agent 并行处理 |
| **Parallel branch 并行分支** | LangGraph 状态图的并行边 | 不同工具/路径的并行执行 |
| **Subgraph 子图并行** | LangGraph subgraph 多图独立运行 | 独立子任务隔离执行 |
| **Semaphore 限流** | nexus-mcp concurrency=3 | I/O 密集型并行任务 |
| **Durable execution 持久执行** | LangGraph 检查点 + 容错 | 长周期并行任务 |
| **Human-in-the-loop** | LangGraph interrupt/approval | 需要人工审核的并行节点 |

**Token 效率分析：**
- 串行执行 N 个国家搜索：$O(N)$ token 消耗，$O(N \times T)$ 时间
- 并行执行：$O(N)$ token 消耗（不变），$O(T)$ 时间（N 倍提速）
- 但并行带来新的 token 开销：结果合并/去重/冲突解决的 token

**multi-agent 协作模式：**
- **Orchestrator-Worker**：中心调度器 + 并行 worker（适合搜索 Agent）
- **Debate/Critic**：多 agent 交叉验证（适合合规检查）
- **Pipeline**：串行 + 并行混合（适合翻译→校验→发布流程）

### 2.3 Scrapling 原生并行能力

Scrapling（⭐47.8K，D4Vinci/Scrapling）是目前最活跃的 Python 自适应爬虫框架，作为搜索 Agent v4 的核心依赖，它本身就提供以下并行化基础设施：

**Spider 系统内置：**
```
concurrent_requests = 4          # 全局并发（可调）
concurrent_requests_per_domain   # 单域限流（可调）
download_delay = 0.0             # 请求间隔
```

**AsyncSession 并行请求：**
```python
# 多个 url 并行抓取
async with FetcherSession(impersonate="chrome") as session:
    tasks = [session.get(url) for url in urls]
    pages = await asyncio.gather(*tasks)
```

**StealthySession + Cloudflare 绕过：**
```python
async with AsyncStealthySession(solve_cloudflare=True) as session:
    pages = await asyncio.gather(
        session.fetch(url1),  # 可能有 Cloudflare
        session.fetch(url2),
        session.fetch(url3)
    )
```

**其他并行支持：**
- 自动 Proxy 轮换（`ProxyRotator`）
- 暂停/恢复（checkpoint 持久化）
- uvloop 加速事件循环
- 自适应选择器（页面变化自动重定位元素）

**核心价值**：Scrapling 已经为搜索 Agent v4 提供「开箱即用」的并行抓取能力。我们不需要再实现底层并发，而是把精力放在**智能调度层**。

---

## 三、当前架构瓶颈点（搜索 Agent）

| 瓶颈 | 描述 | 影响 |
|------|------|------|
| **单次串行多国搜索** | 搜索国家序列依次执行，等待前一个完成 | 10 国搜索 ≈ 串行 ×10 耗时 |
| **无并发上限感知** | 固定并发数，不根据目标网站响应动态调整 | 资源浪费或触发限流 |
| **无域级隔离** | 不同站点共享一个 fetcher，互相干扰 | 一个域超时拖慢全部 |
| **无结果合并并行化** | 多源结果回来后再集中分析，无法流式处理 | 增加等待时间 |
| **无状态感知重试** | 失败后简单重试，不区分网络/反爬/超时 | 重试效率低 |

---

## 四、并行化改造路径

### 路径 A：Spider 级并行（推荐 · 2天）

基于 Scrapling 的 Spider 系统，把搜索 Agent 重构为 spider + pipeline 架构。

```
┌─────────────────────────────────────────────────┐
│                   Orchestrator                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Spider 1 │  │ Spider 2 │  │ Spider 3 │  ...  │
│  │ ────CN   │  │ ────US   │  │ ────EU   │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │             │             │             │
│       └─────────────┼─────────────┘             │
│                     ▼                           │
│              Merge Layer (流式合并)              │
│                ↓ filtered results               │
│              AI Synthesis Layer                 │
└─────────────────────────────────────────────────┘
```

**具体改动：**
1. 每个国家生成一个 Spider 实例（共享 task 配置）
2. 使用 `asyncio.gather` 并行启动所有 spider
3. 设置 `concurrent_requests_per_domain=2` + `download_delay` 防限流
4. Merge Layer 用队列模式流式接收结果
5. 结果达到阈值即触发 AI 合成，不等全部完成

### 路径 B：AsyncSession 级并行（快速 · 0.5天）

最小改动：把原 `fetch()` 调用改为 `asyncio.gather` + semaphore。

```python
sem = asyncio.Semaphore(PER_COUNTRY_CONCURRENCY)

async def search_country(country, query):
    async with sem:
        async with AsyncStealthySession(solve_cloudflare=True) as s:
            return await s.fetch(country.search_url(query))

all_tasks = [search_country(c, q) for c in countries]
results = await asyncio.gather(*all_tasks, return_exceptions=True)
```

**优势**：改动最小，0.5天可上线
**劣势**：每个国家开独立 session，资源使用较高

### 路径 C：流式并行（高级 · 3天）

在路径 A 基础上增加：
1. `asyncio.Queue` 流式传递搜索结果
2. AI 合成层在收到 N 个结果后启动增量分析
3. `trio` 或 `uvloop` 提升事件循环性能
4. 失败国家自动补搜（重分配资源）
5. 结果质量实时评估（脏数据直接丢弃，不影响合成）

---

## 五、预期提速

| 搜索国家数 | 当前串联耗时 | Spider 并行 | AsyncSession 并行 | 流式并行 |
|-----------|------------|------------|------------------|---------|
| 3 国 | ~30s | ~10s (3×) | ~10s (3×) | ~8s (3.75×) |
| 5 国 | ~50s | ~12s (4.2×) | ~15s (3.3×) | ~10s (5×) |
| 10 国 | ~100s | ~18s (5.6×) | ~25s (4×) | ~15s (6.7×) |
| 20 国 | ~200s | ~30s (6.7×) | ~45s (4.4×) | ~22s (9×) |

**说明：**
- 预期非严格线性提升，受目标站点响应速度、反爬强度、网络延迟等因素影响
- `concurrent_requests` 建议设置为 min(目标服务器数 × 2, 16)，避免过度并发

---

## 六、风险点与缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| **反爬检测升级** | 中 | 多个 parallel 请求同时来自同 IP 易触发风控 | 1. ProxyRotator 自动轮换 IP；2. 每个国家用不同 IP 池；3. 随机化 User-Agent |
| **内存暴涨** | 低 | 同时加载多个页面响应导致 OOM | 1. Spider 内置流式处理不缓存全量；2. 设置 `max_items`；3. 结果页大小限制 |
| **目标站点限流** | 中 | 多个 parallel 请求导致被封 IP | 1. `concurrent_requests_per_domain` 限制每域并发；2. download_delay 自适应 |
| **结果质量下降** | 低 | 并行场景下结果合并逻辑出错 | 1. 每个结果附带 country+source 元信息；2. 合并层做冲突检测；3. 增量合成而非全量重合成 |
| **编排层复杂度** | 中 | Spider 并行 + AI 合成耦合导致 debug 困难 | 1. 日志结构化（每个 country+spider 独立日志）；2. 可重复执行（幂等设计）；3. checkpoint 持久化 |
| **代理延迟** | 中 | 跨国代理节点延迟不一，FIFO 等待拖慢整体 | 1. 每个 country 绑定不同区域代理；2. 超时快的先返回；3. 不等最慢的 |

---

## 七、推荐方案

### 立即执行（Phase 1 · 0.5天）
- **路径 B**：把 `fetch()` 改为 `asyncio.gather` + semaphore 限流
- 加 `return_exceptions=True` 防止单个失败拖慢整体
- 效果：4-5× 提速，改动量极小

### 短期（Phase 2 · 2天）
- **路径 A**：重构为 Scrapling Spider 架构
- 充分利用 Scrapling 的 `concurrent_requests` / pause-resume / checkpoint
- 增加自适应退避策略
- 效果：5-7× 提速，稳定性大幅提升

### 中期（Phase 3 · 3-5天）
- **路径 C**：流式并行 + AI 增量合成
- 引入 `asyncio.Queue` 或 `tornado.queues`
- AI 合成层支持增量更新
- 失败自动补搜
- 效果：7-9× 提速，首批结果在 3s 内返回

---

## 八、工作量估算

| 阶段 | 复杂度 | 代码量 | 测试量 | 总工时 |
|------|--------|--------|--------|--------|
| Phase 1: AsyncSession 并行 | ★☆☆ | ~50 行 | ~30 行 | 0.5 人天 |
| Phase 2: Spider 架构重构 | ★★☆ | ~300 行 | ~200 行 | 2 人天 |
| Phase 3: 流式并行 + 增量合成 | ★★★ | ~500 行 | ~400 行 | 3-5 人天 |
| **总计** | | **~850 行** | **~630 行** | **5.5-7.5 人天** |

---

## 九、参考资料

1. **codex-yolo** — https://github.com/codex-yolo/codex-yolo（tmux 并行运行 Codex CLI）
2. **nexus-mcp** — https://github.com/j7an/nexus-mcp（MCP 多 agent 并行编排）
3. **golutra** — https://github.com/golutra/golutra（桌面级多 agent 并行）⭐3.4K
4. **Scrapling** — https://github.com/D4Vinci/Scrapling（自适应爬虫）⭐47.8K
5. **LangGraph Advanced** — https://github.com/esurovtsev/langgraph-advanced（并行 agent workflow 教程）
6. **LangGraph 文档** — https://docs.langchain.com（Durable execution + subgraph + parallel branching）

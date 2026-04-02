# OpenClaw Fetch 命令设计规范

> 灵感来源：opencli 项目  
> 版本：v1.0（规划中）  
> 状态：🟡 待实现

---

## 📋 命令格式

```bash
openclaw fetch <平台> <动作> [参数]
```

### 参数规范

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--limit` | 返回数量限制 | 10 |
| `--format` | 输出格式（table/json/csv） | table |
| `--query` | 搜索关键词 | - |
| `--sort` | 排序方式（hot/new/top） | hot |

---

## 🌐 支持平台（20+）

### 国际平台（公开 API，无需登录）

| 平台 | 命令 | 动作 | 示例 |
|------|------|------|------|
| **HackerNews** | `hackernews` | top/new/best | `openclaw fetch hackernews top --limit 5` |
| **GitHub** | `github` | trending/stars | `openclaw fetch github trending --limit 10` |
| **StackOverflow** | `stackoverflow` | hot/unanswered | `openclaw fetch stackoverflow hot --limit 5` |
| **arXiv** | `arxiv` | search/categories | `openclaw fetch arxiv search "large language model"` |
| **BBC** | `bbc` | news/world/tech | `openclaw fetch bbc news` |
| **Wikipedia** | `wikipedia` | random/search | `openclaw fetch wikipedia random` |
| **Twitter** | `twitter` | trending/search | `openclaw fetch twitter trending` |
| **Reddit** | `reddit` | hot/new/top | `openclaw fetch reddit hot --subreddit technology` |
| **ProductHunt** | `producthunt` | top/new | `openclaw fetch producthunt top` |

### 国内平台（需要 Chrome 已登录）

| 平台 | 命令 | 动作 | 示例 |
|------|------|------|------|
| **B 站** | `bilibili` | hot/ranking | `openclaw fetch bilibili hot --limit 10` |
| **知乎** | `zhihu` | hot/search | `openclaw fetch zhihu hot --format json` |
| **小红书** | `xiaohongshu` | search/notes | `openclaw fetch xiaohongshu search "AI 工具"` |
| **微博** | `weibo` | hot/search | `openclaw fetch weibo hot` |
| **豆瓣** | `douban` | top250/search | `openclaw fetch douban top250` |
| **Boss 直聘** | `boss` | search | `openclaw fetch boss search "前端开发"` |
| **V2EX** | `v2ex` | latest/hot | `openclaw fetch v2ex latest --limit 5` |
| **即刻** | `jike` | feed/topic | `openclaw fetch jike feed` |

---

## 💡 使用场景

### 场景 1：每日晨报素材收集

```bash
# 科技新闻
openclaw fetch hackernews top --limit 5
openclaw fetch github trending
openclaw fetch bbc tech

# 国内动态
openclaw fetch zhihu hot
openclaw fetch weibo hot

# 整合输出
openclaw fetch hackernews top --limit 5 --format json | \
  openclaw process --template morning-brief
```

### 场景 2：市场调研

```bash
# 竞品监控
openclaw fetch github trending --query "AI"
openclaw fetch producthunt top --query "AI"
openclaw fetch twitter trending --query "AGI"

# 舆情分析
openclaw fetch weibo hot --query "AI"
openclaw fetch zhihu hot --query "人工智能"
```

### 场景 3：技术学习

```bash
# 论文追踪
openclaw fetch arxiv search "transformer" --limit 10
openclaw fetch arxiv search "reinforcement learning"

# 问题解答
openclaw fetch stackoverflow hot --query "python"
```

### 场景 4：求职招聘

```bash
# 岗位搜索
openclaw fetch boss search "AI 工程师" --city 上海
openclaw fetch boss search "大模型" --salary "30k+"

# 行业趋势
openclaw fetch zhihu hot --query "就业"
openclaw fetch v2ex latest --query "求职"
```

---

## 🛠️ 技术实现

### 架构设计

```
┌─────────────────────────────────────────┐
│  openclaw fetch CLI                     │
├─────────────────────────────────────────┤
│  命令解析层                              │
│  - 平台识别                              │
│  - 动作解析                              │
│  - 参数验证                              │
├─────────────────────────────────────────┤
│  适配器层（Platform Adapters）          │
│  - hackernews_adapter.py               │
│  - github_adapter.py                   │
│  - zhihu_adapter.py                    │
│  - ...                                 │
├─────────────────────────────────────────┤
│  数据层                                  │
│  - API 调用（公开 API）                  │
│  - Web 爬取（需要登录）                  │
│  - 缓存机制（Redis/本地）               │
└─────────────────────────────────────────┘
```

### 实现优先级

**Phase 1（P0，1 周）**：
- 公开 API 平台（HackerNews/GitHub/BBC/Wikipedia）
- 基础命令解析
- JSON/Table 输出格式

**Phase 2（P1，2 周）**：
- 国内平台（知乎/微博/B 站）
- Chrome 登录集成
- 缓存机制

**Phase 3（P2，3 周）**：
- 高级功能（搜索/过滤/排序）
- 自定义模板
- 定时任务集成

---

## 📊 与 opencli 对比

| 维度 | opencli | OpenClaw Fetch |
|------|---------|----------------|
| **平台覆盖** | 15+ | 20+（规划） |
| **输出格式** | table/json | table/json/csv |
| **AI 集成** | ❌ | ✅（可调用太一分析） |
| **工作流** | ❌ | ✅（可集成定时任务） |
| **缓存** | ❌ | ✅（规划中） |

---

## 🎯 验收标准

### 功能验收
- [ ] 支持 10+ 平台（Phase 1）
- [ ] 支持 20+ 平台（Phase 2）
- [ ] 输出格式正确（JSON/Table/CSV）
- [ ] 参数解析正确（limit/format/query）

### 性能验收
- [ ] 单次请求 <3 秒
- [ ] 缓存命中率 >80%
- [ ] 并发请求支持（5+ 平台同时）

### 安全验收
- [ ] 不存储用户凭证
- [ ] 遵守 robots.txt
- [ ] 请求频率限制（<10 次/分钟/平台）

---

## 🔗 参考资源

- opencli 项目：https://github.com/opencli/opencli
- OpenClaw CLI: https://github.com/nicola-king/openclaw-workspace
- 公开 API 列表：https://github.com/public-apis/public-apis

---

*版本：v1.0 | 创建时间：2026-04-02 | 状态：规划中*

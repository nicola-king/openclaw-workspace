# 🤖 AI 搜索 Skill

> **版本**: 1.0.0  
> **创建**: 2026-04-19  
> **灵感**: Crawl4AI (58k+ ⭐) + Firecrawl (70k+ ⭐)  
> **定位**: 太一系统 AI 搜索专用 Skill

---

## 📋 功能说明

### 核心功能

| 功能 | 说明 | 技术来源 |
|------|------|---------|
| **网络搜索** | 搜索网络获取结果 | Firecrawl |
| **网页爬取** | 爬取网页内容 | Crawl4AI |
| **搜索 + 爬取** | 搜索后自动爬取内容 | 融合 |
| **Agent 查询** | 描述需求自主采集 | Firecrawl |
| **页面交互** | 点击/滚动/输入 | Firecrawl |

---

## 🛠️ 安装

```bash
# 安装 Crawl4AI (爬取)
pip install crawl4ai
crawl4ai-setup
crawl4ai-doctor

# 安装 Firecrawl (搜索)
pip install firecrawl-py

# 配置 API Key (可选，仅 Firecrawl 需要)
# 在 skill_config.json 中添加 firecrawl_api_key
```

---

## 📖 使用方法

### 智能自动化调用 (推荐)

```python
from ai_search_skill_evolution import AISearchSkillEvolution

skill = AISearchSkillEvolution()

# 智能调用 - 自动选择最佳方法
result = await skill.smart_call("搜索 AI 爬虫相关信息")
result = await skill.smart_call("分析 2026 年 AI 市场格局")
result = await skill.smart_call("爬取 https://example.com")
```

### 异步调用

```python
from ai_search_skill import AISearchSkill

skill = AISearchSkill()

# 1. 搜索
results = await skill.search("AI 爬虫", limit=10)

# 2. 爬取
content = await skill.crawl("https://example.com")

# 3. 搜索 + 爬取
full_results = await skill.search_and_crawl("AI 爬虫", limit=5)

# 4. Agent 查询
agent_result = await skill.agent_query("查找 Notion 的定价信息")

# 5. 页面交互
await skill.interact("https://amazon.com", [
    {"type": "type", "text": "mechanical keyboard"},
    {"type": "click", "target": "search button"}
])
```

### 同步调用

```python
from ai_search_skill import AISearchSkillSync

skill = AISearchSkillSync()

# 搜索
results = skill.search("AI 爬虫", limit=10)

# 爬取
content = skill.crawl("https://example.com")

# 搜索 + 爬取
full_results = skill.search_and_crawl("AI 爬虫", limit=5)

# Agent 查询
agent_result = skill.agent_query("查找 Notion 的定价信息")
```

---

## 📊 API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/search` | async | 网络搜索 |
| `/crawl` | async | 网页爬取 |
| `/search_and_crawl` | async | 搜索 + 爬取 |
| `/agent_query` | async | Agent 自主查询 |
| `/interact` | async | 页面交互 |

---

## 🔧 配置

### skill_config.json

```json
{
  "crawler": "crawl4ai",
  "search": "firecrawl",
  "local_mode": true,
  "api_mode": false,
  "max_results": 10,
  "timeout": 30,
  "firecrawl_api_key": "fc-YOUR_API_KEY"
}
```

---

## 📈 统计信息

```python
stats = skill.get_stats()

# 输出:
{
  "total_searches": 0,
  "total_crawls": 0,
  "total_interactions": 0,
  "total_agent_queries": 0,
  "skill_name": "ai_search",
  "version": "1.0.0",
  "crawler_status": "ready",
  "search_api_status": "ready"
}
```

---

## 🎯 使用场景

### 1. 市场研究

```python
# 搜索竞品信息
results = await skill.search_and_crawl("竞品分析", limit=10)

# 提取关键信息
for result in results:
    print(f"来源：{result['url']}")
    print(f"内容：{result['content'][:500]}")
```

### 2. 价格监控

```python
# Agent 自主查询价格
price_info = await skill.agent_query("查找 MacBook Pro 16 寸的最新价格")
print(price_info)
```

### 3. 数据采集

```python
# 批量爬取
urls = ["https://site1.com", "https://site2.com", ...]
for url in urls:
    content = await skill.crawl(url)
    # 处理内容
```

### 4. 自动化调研

```python
# 描述需求，Agent 自主完成
report = await skill.agent_query("调研 2026 年 AI 爬虫市场格局，包括主要玩家/价格/功能对比")
print(report)
```

---

## 🔄 与太一系统集成

### Skill 注册

```python
# 在太一系统注册 Skill
from taiyi_skill_registry import register_skill

register_skill(
    name="ai_search",
    version="1.0.0",
    module="ai_search_skill",
    class_name="AISearchSkill"
)
```

### 太一调用

```python
# 太一系统调用
result = await taiyi.call_skill(
    skill="ai_search",
    method="search_and_crawl",
    params={"query": "AI 爬虫", "limit": 5}
)
```

---

## 📊 性能对比

| 功能 | Crawl4AI | Firecrawl | 太一 AI 搜索 |
|------|---------|-----------|------------|
| 搜索 | ❌ | ✅ | ✅ |
| 爬取 | ✅ | ✅ | ✅ |
| 交互 | ❌ | ✅ | ✅ |
| Agent | ❌ | ✅ | ✅ |
| 费用 | 免费 | 付费 | 免费 (本地) |
| 部署 | 本地 | API/本地 | 本地 |

---

## ⚠️ 注意事项

1. **Firecrawl API Key**: 搜索功能需要 API Key (可免费注册获取)
2. **Crawl4AI 安装**: 需要运行 `crawl4ai-setup` 初始化
3. **异步调用**: 主要功能为异步，需使用 `await`
4. **同步包装**: 提供 `AISearchSkillSync` 同步包装器

---

## 🔗 相关链接

- **Crawl4AI**: https://github.com/unclecode/crawl4ai (58k+ ⭐)
- **Firecrawl**: https://github.com/firecrawl/firecrawl (70k+ ⭐)
- **太一 AGI**: https://github.com/nicola-king/openclaw

---

## 📄 许可证

Apache License 2.0 - 免费开源，可商用

---

*太一 AGI · AI 搜索 Skill · 2026-04-19*

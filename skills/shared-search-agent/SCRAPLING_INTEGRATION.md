# Scrapling 集成到共享搜索服务

> **版本**: v1.0
> **时间**: 2026-05-04
> **状态**: ✅ 已集成

---

## 📋 集成概述

Scrapling 已集成到 `shared_search_service.py`，作为新的搜索模式选项。

### 搜索模式优先级

```
AUTO 模式选择逻辑:
1. 高保护网站 (google, bing, linkedin, twitter)
   → 优先 Scrapling → 回退 Browser → 回退 Requests
2. 普通网站
   → Requests (快速)
```

---

## 🔧 集成代码变更

### 1. 新增搜索模式

```python
class SearchMode(Enum):
    REQUESTS = "requests"      # 快速模式
    BROWSER = "browser"        # 浏览器模式
    SCRAPLING = "scrapling"    # Scrapling 抓取模式 ← 新增
    AUTO = "auto"              # 自动选择
```

### 2. 新增 Scrapling 搜索方法

```python
def _scrapling_search(self, request: SearchRequest) -> List[Dict]:
    """使用 Scrapling 搜索"""
    from scrapling import Fetcher
    
    fetcher = Fetcher()
    response = fetcher.get(search_url, timeout=15)
    
    # 解析搜索结果
    results = []
    for item in response.css('div.g')[:request.max_results]:
        title = item.css('h3::text').get('')
        url = item.css('a::attr(href)').get('')
        description = item.css('div.VwiC3b::text').get('')
        
        if title and url:
            results.append({
                "title": title,
                "url": url,
                "description": description or '',
                "source": "scrapling",
            })
    
    return results
```

### 3. 修改搜索模式选择

```python
def _select_search_mode(self, request: SearchRequest) -> SearchMode:
    if request.search_mode == "scrapling":
        return SearchMode.SCRAPLING
    elif request.search_mode == "browser":
        return SearchMode.BROWSER
    # ...
    # 自动选择: 高保护网站优先 Scrapling
    if any(site in request.query.lower() for site in high_protection_sites):
        if self._scrapling_available():
            return SearchMode.SCRAPLING
        return SearchMode.BROWSER
```

---

## 🚀 使用方式

### 显式使用 Scrapling

```python
from skills.shared_search_agent.shared_search_service import SearchRequest

request = SearchRequest(
    query="smart water bottle",
    agent_type="cross_border_trade",
    search_mode="scrapling",  # 显式指定
    max_results=10,
)
```

### 自动选择 (推荐)

```python
request = SearchRequest(
    query="site:google.com product",
    agent_type="cross_border_trade",
    search_mode="auto",  # 自动选择 Scrapling/Browser
)
```

---

## 📊 测试结果

| 测试项目 | 结果 | 说明 |
|---------|------|------|
| Hacker News 抓取 | ✅ | 成功提取 30 个标题 |
| httpbin 抓取 | ✅ | 成功提取内容 |
| Google 搜索 | ⚠️ | 抓取成功但解析需调整 |
| 超时机制 | ✅ | 15秒超时正常 |

---

## 🔗 依赖关系

```
shared-search-agent/
├── shared_search_service.py  ← 集成 Scrapling
└── SCRAPLING_INTEGRATION.md   ← 本文档

scrapling-integration/
├── venv-scrapling/            ← Scrapling 虚拟环境
└── SCRAPLING_INTEGRATION.md   ← Scrapling 文档
```

---

## 🎯 未来优化

- [ ] 优化 Google 搜索结果解析
- [ ] 添加更多网站适配器
- [ ] 集成到跨境贸易 Agent
- [ ] 性能优化 (连接池)

---

*太一 AGI · Scrapling 集成文档*

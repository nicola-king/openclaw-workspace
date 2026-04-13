# 罔两 Bot·全平台搜索增强

> 版本：v1.0 | 创建：2026-03-28 20:02
> 参考：Xcrawl-Skills / last30days-skill

---

## 功能规划

### 1. 集成 Xcrawl-Skills
- xcrawl-scrape: 单页精准抓取
- xcrawl-map: 全站 URL 映射
- xcrawl-crawl: 批量异步爬取
- xcrawl-search: 多引擎 SERP 搜索

### 2. 支持平台
- Reddit
- X (Twitter)
- YouTube
- HackerNews
- Polymarket
- 微博
- 小红书

### 3. 输出格式
- Markdown
- JSON
- 链接列表

---

## 技术实现

```python
from xcrawl import scrape, map, crawl, search

def multi_platform_search_enhanced(query):
    """全平台搜索增强"""
    
    results = {
        'reddit': search(query, platform='reddit'),
        'twitter': search(query, platform='twitter'),
        'youtube': search(query, platform='youtube'),
        'hn': search(query, platform='hackernews'),
        'polymarket': search(query, platform='polymarket')
    }
    
    return results
```

---

## 集成到罔两 Bot

- 增强数据采集能力
- 支持更多数据源
- 提升数据质量

---

*版本：v1.0 | 状态：✅ 已创建*

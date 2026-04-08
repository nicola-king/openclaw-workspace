---
name: news-fetcher
version: 1.0.0
description: "Use when fetching news articles, headlines, and media content from NewsAPI (free tier: 100 requests/day)."
triggers: ['新闻，头条，媒体，NewsAPI', 'news', 'headlines', '实时新闻']
permissions: ['exec', 'web_fetch']
category: data
author: 太一 AGI
tags: ['news', 'media', 'api', '新闻', '获取']
---



# News Fetcher (NewsAPI)

Use this skill when you need real-time news articles, headlines, or media content from NewsAPI.

## Core Truths

- **免费层**: 100 请求/天
- **覆盖广**: 全球 80,000+ 新闻源
- **实时**: 新闻发布后 5-15 分钟可搜索
- **API Key**: 需要注册 (免费)

## What This Tool Is For

`news-fetcher` provides:

1. **Top Headlines** - 头条新闻
2. **Everything** - 全文搜索
3. **Sources** - 新闻源列表

## Authentication

**Get API Key**: https://newsapi.org/register

```bash
# 测试 API Key
curl "https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_API_KEY"
```

**太一配置**: 将 API Key 存入 `.env`
```
NEWS_API_KEY=your_api_key_here
```

## Default Workflow

### 1. Top Headlines (头条新闻)

```bash
# 美国头条
curl "https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_KEY"

# 中国头条
curl "https://newsapi.org/v2/top-headlines?country=cn&apiKey=YOUR_KEY"

# 特定类别 (business, technology, sports, entertainment, health, science)
curl "https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=YOUR_KEY"

# 特定关键词
curl "https://newsapi.org/v2/top-headlines?q=bitcoin&country=us&apiKey=YOUR_KEY"
```

**Parameters**:
- `country`: us, cn, gb, jp, de, fr (ISO 3166-2)
- `category`: business, technology, sports, entertainment, health, science
- `q`: 关键词搜索
- `pageSize`: 1-100 (默认 20)

### 2. Everything (全文搜索)

```bash
# 搜索关键词
curl "https://newsapi.org/v2/everything?q=bitcoin&apiKey=YOUR_KEY"

# 时间范围
curl "https://newsapi.org/v2/everything?q=AI&from=2026-04-01&to=2026-04-04&apiKey=YOUR_KEY"

# 排序 (relevancy, popularity, publishedAt)
curl "https://newsapi.org/v2/everything?q=AI&sortBy=publishedAt&apiKey=YOUR_KEY"
```

**Parameters**:
- `q`: 搜索关键词 (AND, OR, NOT 支持)
- `from`: 起始日期 (YYYY-MM-DD)
- `to`: 结束日期
- `sortBy`: relevancy, popularity, publishedAt
- `language`: en, zh, ja, ko, de, fr, etc.

### 3. Sources (新闻源)

```bash
# 所有新闻源
curl "https://newsapi.org/v2/sources?apiKey=YOUR_KEY"

# 特定国家
curl "https://newsapi.org/v2/sources?country=us&apiKey=YOUR_KEY"

# 特定类别
curl "https://newsapi.org/v2/sources?category=technology&apiKey=YOUR_KEY"
```

## Integration with Taiyi

### 罔两 数据采集

**使用场景**:
- 批量采集新闻数据
- 监控特定主题
- 生成新闻摘要

**示例脚本**:
```python
import requests
import os

def fetch_news(query, days=1, language='en'):
    api_key = os.getenv('NEWS_API_KEY')
    url = "https://newsapi.org/v2/everything"
    
    params = {
        'q': query,
        'from': f'{days}daysAgo',
        'sortBy': 'publishedAt',
        'language': language,
        'apiKey': api_key
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    return {
        'total': data['totalResults'],
        'articles': data['articles'][:10]  # 前 10 条
    }

# 使用
news = fetch_news('cryptocurrency')
print(f"找到 {news['total']} 条新闻")
for article in news['articles']:
    print(f"- {article['title']} ({article['source']['name']})")
```

### 山木 内容创作

**使用场景**:
- 获取热点话题
- 收集创作素材
- 追踪趋势

## Rate Limits

| 层级 | 请求数 | 价格 |
|------|--------|------|
| **免费** | 100/天 | $0 |
| **Developer** | 500/天 | $29/月 |
| **Business** | 2000/天 | $99/月 |

**太一策略**:
- 免费层 100 请求/天 = 每 14 分钟 1 次
- 缓存结果 30 分钟
- 关键新闻实时获取

## Error Handling

### Common Errors

| Error | Code | Solution |
|-------|------|----------|
| Rate Limit | 429 | 等待或升级套餐 |
| Invalid Key | 401 | 检查 API Key |
| Bad Request | 400 | 检查参数格式 |
| Server Error | 500 | 重试 |

### Fallback News APIs

1. **Guardian API**: https://open-platform.theguardian.com/
2. **New York Times API**: https://developer.nytimes.com/
3. **NewsData.io**: https://newsdata.io/
4. **Currents API**: https://currentsapi.services/

## Quick Reference

### Country Codes

| 代码 | 国家 |
|------|------|
| us | 美国 |
| cn | 中国 |
| gb | 英国 |
| jp | 日本 |
| de | 德国 |
| fr | 法国 |
| kr | 韩国 |

### Category List

- business (商业)
- technology (科技)
- sports (体育)
- entertainment (娱乐)
- health (健康)
- science (科学)

### Language Codes

| 代码 | 语言 |
|------|------|
| en | 英语 |
| zh | 中文 |
| ja | 日语 |
| ko | 韩语 |
| de | 德语 |
| fr | 法语 |
| es | 西班牙语 |

## Example Outputs

### Top Headlines Query

**Input**: "美国科技新闻头条"

**Output**:
```markdown
## 📰 美国科技头条

| 标题 | 来源 | 时间 |
|------|------|------|
| [标题 1] | [来源] | [X 小时前] |
| [标题 2] | [来源] | [X 小时前] |
| [标题 3] | [来源] | [X 小时前] |

共 20 条 | 更新于：刚刚
```

### Search Query

**Input**: "搜索 AI 相关新闻 (最近 7 天)"

**Output**:
```markdown
## 🔍 AI 相关新闻 (7 天内)

**找到**: 1,234 条

### Top 10

1. **[标题]** - [来源] ([时间])
   [摘要...]

2. **[标题]** - [来源] ([时间])
   [摘要...]

...
```

## Setup for Taiyi

### 1. Register API Key

Visit: https://newsapi.org/register

### 2. Add to .env

```bash
# /home/nicola/.openclaw/workspace/.env
NEWS_API_KEY=your_api_key_here
```

### 3. Test Connection

```bash
curl "https://newsapi.org/v2/top-headlines?country=us&apiKey=$(grep NEWS_API_KEY .env | cut -d= -f2)"
```

### 4. Create Cron Job (Optional)

```bash
# 每小时采集 (免费层 100 次/天)
0 * * * * cd /home/nicola/.openclaw/workspace && python scripts/news-collector.py
```

## Notes

- Free tier: 100 requests/day (enough for ~4/hour)
- News available 5-15 min after publication
- API Key required (free registration)
- Cache results to reduce API calls
- Use `from` and `to` parameters for historical queries

## References

- **API Docs**: https://newsapi.org/docs
- **Register**: https://newsapi.org/register
- **Pricing**: https://newsapi.org/pricing

---

*Version: 1.0.0 | Created: 2026-04-04 | Taiyi AGI*

---
name: public-apis-index
version: 1.0.0
description: Use when discovering, searching, or integrating public APIs from the public-apis repository (400k+ stars, 1000+ APIs, 54 categories).
triggers: ['API', '数据源，集成，public-apis', '发现 API', 'API 搜索']
permissions: ['web_search', 'web_fetch', 'exec']
category: other
---



# Public APIs Index

Use this skill when you need to discover, search, or integrate free public APIs from the curated public-apis repository.

## Core Truths

- **40 万 + Star**: https://github.com/public-apis/public-apis
- **1000+ API**: 54 大类，社区维护
- **免费优先**: 优先推荐免费/开源 API
- **认证标注**: 每个 API 标注认证方式 (API Key/OAuth/无)

## What This Tool Is For

`public-apis-index` helps you:

1. **Discover APIs** - Find APIs by category or keyword
2. **Evaluate APIs** - Check auth, pricing, features
3. **Integrate APIs** - Get quick start guides
4. **Monitor APIs** - Track status and rate limits

## Default Workflow

### 1. API Discovery (By Category)

When user asks for APIs in a category:

```markdown
**Category**: [名称]
**APIs Found**: [数量]

| API | Auth | HTTPS | Price | Notes |
|-----|------|-------|-------|-------|
| [Name] | [API Key/OAuth/None] | ✅/❌ | Free/Paid | [特色] |
```

**Top Categories**:
- Cryptocurrency (比特币，以太坊)
- Weather (天气预测)
- News (新闻媒体)
- Finance (股票，外汇)
- AI/ML (机器学习)
- Images (图片库)
- Maps (地图地理)

### 2. API Search (By Keyword)

When user has specific needs:

1. Search public-apis README
2. Filter by keywords
3. Return top 5 matches

### 3. API Integration Guide

For selected API:

```markdown
## [API Name] Integration

**Base URL**: `https://api.example.com`
**Auth**: [API Key/OAuth/None]
**Rate Limit**: [请求数/分钟]

### Quick Start

1. **Get API Key**: [注册链接]
2. **Test Endpoint**:
   ```bash
   curl "https://api.example.com/endpoint?key=YOUR_KEY"
   ```
3. **Integrate**: [代码示例]

### Common Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/data` | GET | 获取数据 |
| `/v1/search` | POST | 搜索 |
```

### 4. API Monitoring

Track API status:

- ✅ Available
- ⚠️ Rate limited
- ❌ Down

## Integration Examples

### Cryptocurrency (CoinGecko)

**Use Case**: 获取加密货币价格

```bash
# 免费，无需 API Key
curl "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
```

**太一集成**: 知几-E 策略增强

### News (NewsAPI)

**Use Case**: 实时新闻采集

```bash
# 需要 API Key (免费 100 请求/天)
curl "https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_KEY"
```

**太一集成**: 罔两数据采集

### Weather (Open-Meteo)

**Use Case**: 气象预测

```bash
# 免费，无需 API Key
curl "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true"
```

**太一集成**: 知几-E 气象套利

## High-Value APIs for Taiyi

### P0 (立即集成)

| API | Category | Auth | 用途 | 负责 Bot |
|-----|---------|------|------|---------|
| **CoinGecko** | Cryptocurrency | None | 加密货币价格 | 知几 |
| **NewsAPI** | News | API Key | 新闻采集 | 罔两 |
| **Open-Meteo** | Weather | None | 气象预测 | 知几-E |

### P1 (本周集成)

| API | Category | Auth | 用途 |
|-----|---------|------|------|
| **Alpha Vantage** | Finance | API Key | 股票/外汇 |
| **Unsplash** | Images | API Key | 免费图片 |
| **Guardian API** | News | API Key | 新闻媒体 |

### P2 (下周可选)

| API | Category | 用途 |
|-----|---------|------|
| OpenStreetMap | Maps | 地图地理 |
| Reddit API | Social | 社交舆情 |
| GIPHY | Images | GIF 素材 |

## Error Handling

### Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Missing API Key | 注册获取 Key |
| 429 Too Many Requests | Rate limit | 降级/缓存 |
| 503 Service Unavailable | API down | 切换备用 API |

### Fallback Strategy

1. Primary API fails → Try backup
2. All APIs fail → Cache last known good data
3. Log error to `memory/api-errors.md`

## References

- **public-apis Repo**: https://github.com/public-apis/public-apis
- **DeepWiki Analysis**: https://deepwiki.com/public-apis/public-apis
- **FindFree Directory**: https://findfree.org/resource/public-apis-github-repo

## Notes

- This skill is a **discovery layer**, not an API wrapper
- For specific API integrations, create dedicated skills (e.g., `coingecko-price`)
- Always check API terms of service and rate limits
- Prefer APIs with no auth or simple API Key for quick integration

---

*Version: 1.0.0 | Created: 2026-04-04 | Taiyi AGI*

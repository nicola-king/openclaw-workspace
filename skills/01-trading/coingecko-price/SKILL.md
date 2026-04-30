---
name: coingecko-price
version: 1.0.0
description: Use when fetching cryptocurrency prices, market data, and trends from CoinGecko API (free, no API key required for basic usage).
triggers: ['加密货币，比特币，以太坊，币价，CoinGecko', 'crypto', 'price', 'BTC', 'ETH']
permissions: ['exec', 'web_fetch']
category: trading
tags: ['crypto', 'price', 'market', '币价', '查询']
---



# CoinGecko Price API

Use this skill when you need cryptocurrency prices, market data, or trends from CoinGecko.

## Core Truths

- **免费**: 基础功能无需 API Key
- **覆盖广**: 10,000+ 加密货币
- **实时**: 价格实时更新
- **限流**: 10-50 次/分钟 (免费层)

## What This Tool Is For

`coingecko-price` provides:

1. **Simple Price** - 单个或多个币种价格
2. **Market Data** - 市值，交易量，涨跌幅
3. **Price History** - 历史价格数据
4. **Trending** - 热门币种排行

## Default Workflow

### 1. Get Simple Price

```bash
# 单个币种 (USD)
curl "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

# 多个币种
curl "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd,cny"

# 包含 24h 变化
curl "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
```

**Response**:
```json
{
  "bitcoin": {
    "usd": 67234.50,
    "usd_24h_change": 2.34
  }
}
```

### 2. Get Market Data

```bash
# 币种详情
curl "https://api.coingecko.com/api/v3/coins/bitcoin"

# 市场概览
curl "https://api.coingecko.com/api/v3/global"
```

### 3. Get Price History

```bash
# 历史数据 (天)
curl "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30"

# 历史数据 (小时)
curl "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=1&interval=hourly"
```

### 4. Get Trending

```bash
# 搜索趋势
curl "https://api.coingecko.com/api/v3/search/trending"
```

## Integration with Taiyi

### 知几-E 策略增强

**使用场景**:
- 获取加密货币实时价格
- 计算市场情绪
- 监控交易量变化

**示例**:
```python
import requests

def get_crypto_prices(coins=['bitcoin', 'ethereum']):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': ','.join(coins),
        'vs_currencies': 'usd',
        'include_24hr_change': True
    }
    response = requests.get(url, params=params)
    return response.json()

# 使用
prices = get_crypto_prices()
print(f"BTC: ${prices['bitcoin']['usd']} (+{prices['bitcoin']['usd_24h_change']:.2f}%)")
```

### 罔两 数据采集

**使用场景**:
- 批量采集市场数据
- 监控热门币种
- 生成市场报告

## Rate Limits

| 层级 | 请求数 | 价格 |
|------|--------|------|
| **免费** | 10-50/分钟 | $0 |
| **Bronze** | 1000/分钟 | $29/月 |
| **Silver** | 5000/分钟 | $99/月 |

**太一策略**: 免费层足够，超限缓存 5 分钟

## Error Handling

### Common Errors

| Error | Code | Solution |
|-------|------|----------|
| Rate Limit | 429 | 等待 60 秒或缓存 |
| Not Found | 404 | 检查币种 ID |
| Server Error | 500/503 | 重试或切换备用 API |

### Fallback APIs

1. **CoinCap**: https://api.coincap.io/v2/assets
2. **Binance**: https://api.binance.com/api/v3/ticker/price
3. **CryptoCompare**: https://min-api.cryptocompare.com/data/price

## Quick Reference

### Common Coin IDs

| 中文名 | CoinGecko ID | Symbol |
|--------|-------------|--------|
| 比特币 | bitcoin | BTC |
| 以太坊 | ethereum | ETH |
| 索拉纳 | solana | SOL |
| 瑞波币 | ripple | XRP |
| 卡尔达诺 | cardano | ADA |
| 狗狗币 | dogecoin | DOGE |

### Currency Codes

| 代码 | 货币 |
|------|------|
| usd | 美元 |
| cny | 人民币 |
| eur | 欧元 |
| jpy | 日元 |
| krw | 韩元 |

## Example Outputs

### Simple Price Query

**Input**: "比特币价格"

**Output**:
```markdown
## 📊 比特币价格

| 指标 | 值 |
|------|-----|
| **价格** | $67,234.50 |
| **24h 涨跌** | +2.34% |
| **市值** | $1.32T |
| **24h 交易量** | $28.5B |

数据来源：CoinGecko (实时更新)
```

### Market Overview

**Input**: "加密货币市场概览"

**Output**:
```markdown
## 🌍 加密货币市场概览

| 指标 | 值 |
|------|-----|
| **总市值** | $2.45T |
| **24h 交易量** | $98.2B |
| **BTC 主导率** | 54.2% |
| **活跃币种** | 10,234 |

### Top 5

| 排名 | 币种 | 价格 | 24h |
|------|------|------|-----|
| 1 | BTC | $67,234 | +2.3% |
| 2 | ETH | $3,456 | +1.8% |
| 3 | SOL | $145.67 | +5.2% |
| 4 | XRP | $0.62 | -0.5% |
| 5 | ADA | $0.58 | +3.1% |
```

## References

- **API Docs**: https://www.coingecko.com/en/api/documentation
- **Website**: https://www.coingecko.com
- **Rate Limits**: https://www.coingecko.com/en/api/pricing

## Notes

- No API key required for basic usage
- Rate limit: ~10-50 calls/minute (free tier)
- For production use, consider paid tier or caching
- CoinGecko ID != Symbol (e.g., bitcoin != BTC)

---

*Version: 1.0.0 | Created: 2026-04-04 | Taiyi AGI*

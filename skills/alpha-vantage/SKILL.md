---
name: alpha-vantage
version: 1.0.0
description: "Use when fetching stock prices, forex rates, and financial market data from Alpha Vantage API (free tier: 5 requests/minute)."
triggers: ['股票，外汇，金融数据，Alpha Vantage', 'stock', 'forex', 'finance', 'AAPL', 'GOOGL']
permissions: ['exec', 'web_fetch']
category: trading
author: 太一 AGI
---



# Alpha Vantage API

Use this skill when you need stock prices, forex rates, or financial market data from Alpha Vantage.

## Core Truths

- **免费层**: 5 请求/分钟，500 请求/天
- **覆盖广**: 全球股票，外汇，加密货币，指标
- **实时 + 历史**: 支持实时数据和历史数据
- **API Key**: 需要注册 (免费)

## What This Tool Is For

`alpha-vantage` provides:

1. **Stock Quotes** - 实时股票价格
2. **Time Series** - 历史价格数据
3. **Forex Rates** - 外汇汇率
4. **Technical Indicators** - 技术指标 (SMA, EMA, RSI, MACD)
5. **Company Info** - 公司信息

## Authentication

**Get API Key**: https://www.alphavantage.co/support/#api-key

```bash
# 测试 API Key
curl "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=YOUR_API_KEY"
```

**太一配置**: 将 API Key 存入 `.env`
```
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

## Default Workflow

### 1. Stock Quote (实时股价)

```bash
# 实时股价
curl "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=YOUR_KEY"

# A 股 (需要特殊代码)
curl "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=BABA&apikey=YOUR_KEY"
```

**Response**:
```json
{
  "Global Quote": {
    "01. symbol": "AAPL",
    "02. open": "175.50",
    "03. high": "177.30",
    "04. low": "174.80",
    "05. price": "176.55",
    "06. volume": "52340000",
    "07. latest trading day": "2026-04-04",
    "08. previous close": "174.90",
    "09. change": "1.65",
    "10. change percent": "0.94%"
  }
}
```

### 2. Time Series (历史数据)

```bash
# 日线数据
curl "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=YOUR_KEY"

# 周线数据
curl "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=AAPL&apikey=YOUR_KEY"

# 月线数据
curl "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=AAPL&apikey=YOUR_KEY"
```

### 3. Forex Rates (外汇汇率)

```bash
# 实时汇率
curl "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=CNY&apikey=YOUR_KEY"
```

**Response**:
```json
{
  "Realtime Currency Exchange Rate": {
    "1. From_Currency Code": "USD",
    "2. From_Currency Name": "United States Dollar",
    "3. To_Currency Code": "CNY",
    "4. To_Currency Name": "Chinese Yuan",
    "5. Exchange Rate": "7.2345",
    "6. Last Refreshed": "2026-04-04 15:55:00",
    "7. Time Zone": "UTC"
  }
}
```

### 4. Technical Indicators (技术指标)

```bash
# SMA (简单移动平均)
curl "https://www.alphavantage.co/query?function=SMA&symbol=AAPL&interval=daily&time_period=20&apikey=YOUR_KEY"

# RSI (相对强弱指数)
curl "https://www.alphavantage.co/query?function=RSI&symbol=AAPL&interval=daily&time_period=14&apikey=YOUR_KEY"

# MACD
curl "https://www.alphavantage.co/query?function=MACD&symbol=AAPL&interval=daily&apikey=YOUR_KEY"
```

## Integration with Taiyi

### 知几 (量化交易)

**使用场景**:
- 获取股票价格数据
- 计算技术指标
- 回测策略

**示例**:
```python
import requests
import os

def get_stock_price(symbol):
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    url = "https://www.alphavantage.co/query"
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': symbol,
        'apikey': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    quote = data.get('Global Quote', {})
    return {
        'price': float(quote.get('05. price', 0)),
        'change': float(quote.get('09. change', 0)),
        'change_percent': quote.get('10. change percent', '0%')
    }

# 使用
price = get_stock_price('AAPL')
print(f"AAPL: ${price['price']} ({price['change_percent']})")
```

### 罔两 (数据采集)

**使用场景**:
- 批量采集股票数据
- 监控市场趋势
- 生成金融报告

## Rate Limits

| 层级 | 请求数 | 价格 |
|------|--------|------|
| **免费** | 5/分钟，500/天 | $0 |
| **Premium** | 120/分钟 | $49.99/月 |

**太一策略**:
- 免费层 5 请求/分钟 = 每 12 秒 1 次
- 缓存结果 10 分钟
- 批量请求分散执行

## Error Handling

### Common Errors

| Error | Code | Solution |
|-------|------|----------|
| Rate Limit | 429 | 等待 12 秒或缓存 |
| Invalid Key | 401 | 检查 API Key |
| Invalid Symbol | 400 | 检查股票代码 |
| Server Error | 500 | 重试 |

### Fallback APIs

1. **Yahoo Finance**: https://finance.yahoo.com/
2. **IEX Cloud**: https://iexcloud.io/
3. **Financial Modeling Prep**: https://financialmodelingprep.com/

## Quick Reference

### Common Stock Symbols

| 公司 | 代码 | 市场 |
|------|------|------|
| Apple | AAPL | NASDAQ |
| Microsoft | MSFT | NASDAQ |
| Google | GOOGL | NASDAQ |
| Amazon | AMZN | NASDAQ |
| Tesla | TSLA | NASDAQ |
| 阿里巴巴 | BABA | NYSE |
| 腾讯 | 0700.HK | HKEX |

### Function List

| 功能 | Function 参数 |
|------|-------------|
| 实时股价 | GLOBAL_QUOTE |
| 日线数据 | TIME_SERIES_DAILY |
| 周线数据 | TIME_SERIES_WEEKLY |
| 月线数据 | TIME_SERIES_MONTHLY |
| 外汇汇率 | CURRENCY_EXCHANGE_RATE |
| SMA | SMA |
| RSI | RSI |
| MACD | MACD |

## Example Outputs

### Stock Price Query

**Input**: "苹果股价"

**Output**:
```markdown
## 📊 Apple Inc. (AAPL)

| 指标 | 值 |
|------|-----|
| **价格** | $176.55 |
| **开盘** | $175.50 |
| **最高** | $177.30 |
| **最低** | $174.80 |
| **涨跌** | +$1.65 (+0.94%) |
| **成交量** | 52.3M |

数据来源：Alpha Vantage (实时更新)
```

### Forex Query

**Input**: "美元兑人民币汇率"

**Output**:
```markdown
## 💱 USD/CNY

| 指标 | 值 |
|------|-----|
| **汇率** | 7.2345 |
| **更新时间** | 2026-04-04 15:55:00 |

1 USD = 7.2345 CNY
```

## Setup for Taiyi

### 1. Register API Key

Visit: https://www.alphavantage.co/support/#api-key

### 2. Add to .env

```bash
# /home/nicola/.openclaw/workspace/.env
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

### 3. Test Connection

```bash
curl "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=$(grep ALPHA_VANTAGE_API_KEY .env | cut -d= -f2)"
```

## Notes

- Free tier: 5 requests/minute, 500/day
- API Key required (free registration)
- Cache results to reduce API calls (10 min TTL)
- A-shares use special symbols (e.g., 000001.SZ for 平安银行)

## References

- **API Docs**: https://www.alphavantage.co/documentation/
- **Register**: https://www.alphavantage.co/support/#api-key
- **Pricing**: https://www.alphavantage.co/premium/

---

*Version: 1.0.0 | Created: 2026-04-04 | Taiyi AGI*

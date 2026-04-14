# 🌐 APILayer API 集成指南

> **创建时间**: 2026-04-14  
> **状态**: ✅ 已完成  
> **来源**: APILayer 公共 API 平台

---

## 🚀 快速开始

### 1. 获取 API Keys

访问 https://apilayer.com/marketplace 注册并获取 API Keys:

- IPstack: https://ipstack.com/
- Marketstack: https://marketstack.com/
- Weatherstack: https://weatherstack.com/
- Fixer: https://fixer.io/
- Aviationstack: https://aviationstack.com/

### 2. 配置环境变量

```bash
export APILAYER_IPSTACK_KEY="your_ipstack_key"
export APILAYER_MARKETSTACK_KEY="your_marketstack_key"
export APILAYER_WEATHERSTACK_KEY="your_weatherstack_key"
export APILAYER_FIXER_KEY="your_fixer_key"
export APILAYER_AVIATIONSTACK_KEY="your_aviationstack_key"
```

### 3. 使用示例

```python
from skills.04-integration.apilayer-integration.apilayer_client import APILayerClient

client = APILayerClient()

# IP 定位
result = client.ipstack_lookup("8.8.8.8")

# 股票数据
result = client.marketstack_eod("AAPL", "2024-01-01")

# 天气查询
result = client.weatherstack_current("Beijing")

# 汇率查询
result = client.fixer_latest("USD", "EUR,CNY,JPY")
```

---

## 📋 API 参考

### IPstack - IP 地址定位

**功能**: 定位和识别网站访问者

```python
client.ipstack_lookup(ip: str) -> Dict
```

**返回**:
```json
{
  "success": true,
  "country_name": "United States",
  "city": "Mountain View",
  "time_zone": {"id": "America/Los_Angeles"}
}
```

### Marketstack - 股票市场数据

**功能**: 全球股票市场数据

```python
client.marketstack_eod(symbol: str, date: Optional[str]) -> Dict
```

**返回**:
```json
{
  "data": [{
    "symbol": "AAPL",
    "date": "2024-01-01",
    "open": 185.00,
    "close": 186.50,
    "high": 187.00,
    "low": 184.50
  }]
}
```

### Weatherstack - 天气信息

**功能**: 实时天气数据

```python
client.weatherstack_current(location: str) -> Dict
```

**返回**:
```json
{
  "current": {
    "temperature": 25,
    "weather_descriptions": ["Sunny"],
    "humidity": 60,
    "wind_speed": 10
  }
}
```

### Fixer - 汇率数据

**功能**: 实时和历史汇率

```python
client.fixer_latest(base: str = "USD", symbols: Optional[str]) -> Dict
```

**返回**:
```json
{
  "success": true,
  "date": "2024-01-01",
  "rates": {
    "EUR": 0.85,
    "CNY": 6.45,
    "JPY": 110.00
  }
}
```

### Aviationstack - 航班状态

**功能**: 实时航班状态和全球航空数据

```python
client.aviationstack_flights(access_key: str, params: Optional[Dict]) -> Dict
```

**返回**:
```json
{
  "data": [{
    "flight_iata": "CA123",
    "dep_iata": "PEK",
    "arr_iata": "LAX"
  }]
}
```

---

## 🔧 高级用法

### 批量查询

```python
# 批量 IP 定位
ips = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
for ip in ips:
    result = client.ipstack_lookup(ip)
    client.save_result(result, f"ipstack_{ip.replace('.', '_')}")
```

### 结果保存

```python
# 自动保存到文件
result = client.weatherstack_current("Beijing")
client.save_result(result, "weather_beijing")
# 输出：data/apilayer/weather_beijing_20260414_155500.json
```

### 错误处理

```python
result = client.ipstack_lookup("8.8.8.8")

if result.get("success"):
    # 处理成功结果
    print(f"国家：{result.get('country_name')}")
else:
    # 处理错误
    print(f"错误：{result.get('error', {}).get('info')}")
```

---

## 📊 输出目录

**默认位置**: `/home/nicola/.openclaw/workspace/data/apilayer/`

**文件结构**:
```
data/apilayer/
├── ipstack_test_20260414_155500.json
├── marketstack_test_20260414_155501.json
├── weatherstack_test_20260414_155502.json
├── fixer_test_20260414_155503.json
└── aviationstack_test_20260414_155504.json
```

---

## 💰 商业价值

**应用场景**:
```
✅ IP 定位 - 用户分析/反欺诈
✅ 股票数据 - 金融分析/投资组合
✅ 天气数据 - 农业/物流/旅游
✅ 汇率数据 - 跨境贸易/金融
✅ 航班数据 - 旅行/物流
```

**成本优势**:
```
✅ 免费套餐可用
✅ 按需付费
✅ 无需自建数据源
✅ 实时更新
```

---

## 🔗 相关链接

- **APILayer**: https://apilayer.com/
- **Marketplace**: https://apilayer.com/marketplace
- **IPstack**: https://ipstack.com/
- **Marketstack**: https://marketstack.com/
- **Weatherstack**: https://weatherstack.com/
- **Fixer**: https://fixer.io/
- **Aviationstack**: https://aviationstack.com/

---

*APILayer API 集成指南 · 太一 AGI · 2026-04-14*

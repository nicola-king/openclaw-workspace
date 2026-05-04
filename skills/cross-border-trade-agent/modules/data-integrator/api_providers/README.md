# API Providers v10.0

## 数据源集成

| 提供者 | 数据源 | 免费 | 需 Key |
|--------|--------|------|--------|
| ExchangeRateAPI | Frankfurter / ExchangeRate-API | ✅ | ❌ |
| CustomsDataAPI | UN Comtrade / WTO | ✅ | ❌ |
| RegulationTracker | 各国法规数据库 | ✅ | ❌ |

## 使用示例

```python
from api_gateway import APIGateway

gateway = APIGateway()

# 汇率
rate = gateway.get_exchange_rate("CNY", "AUD")
# {'from': 'CNY', 'to': 'AUD', 'rate': 0.20474, 'source': 'frankfurter'}

# 关税
tariff = gateway.get_tariff_rate("9406.00", "Australia")
# {'hs_code': '9406.00', 'country': 'Australia', 'tariff_rate': 5.0}

# 合规检查
compliance = gateway.check_compliance("Australia", "construction", ["CE", "ISO9001"])
# {'compliant': False, 'compliance_score': 66.7, 'missing': ['Australian Building Code']}
```

## 蒸馏来源

- 金融情报 Agent (OpenBB, ai-hedge-fund, FinGPT)
- 天机系统 (聪明钱追踪)
- 全球海关数据 (9 大机构)
- 太一宪法层 (负熵法则)

## 状态

- ✅ ExchangeRateAPI: 实时汇率，缓存 1h
- ✅ CustomsDataAPI: HS 编码 + 关税 + 贸易数据
- ✅ RegulationTracker: 法规 + 合规检查 + 更新追踪

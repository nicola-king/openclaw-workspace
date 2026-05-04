# GEO 外贸开发 (Geo Outbound) Skill

## 描述
GEO 外贸开发：市场分析 → 潜客名单 → 内容营销 → 监测优化

## 独立运行
```bash
python core.py --hs-code "8507.60"
```

## 依赖
- cross-border-core: ^9.0.0

## API

### 输入
```json
{
  "hs_code": "8507.60",
  "market": "澳大利亚"
}
```

### 输出
```json
{
  "status": "success",
  "market_analysis": {
    "demand": "high",
    "growth_rate": "15%",
    "competitors": 12
  }
}
```

## 配置
```json
{
  "analysis": {
    "hs_codes": ["8507.60", "7308.90"],
    "markets": ["澳大利亚", "新西兰", "中东"]
  },
  "content": {
    "platforms": ["linkedin", "quora", "blog"],
    "frequency": "weekly"
  }
}
```

## 使用示例
```python
from core import GeoOutbound

agent = GeoOutbound(config_path="config.json")
result = agent.execute(hs_code="8507.60", market="澳大利亚")
print(result)
```

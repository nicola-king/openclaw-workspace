# 智能分析中心 (Intelligence Hub) Skill

## 描述
智能分析：竞品分析/选品评分/厂家推荐/趋势预测

## 独立运行
```bash
python core.py --task competitor --product "折叠房屋"
```

## 依赖
- cross-border-core: ^9.0.0
- data-integrator: ^9.0.0

## API

### 输入
```json
{
  "task": "competitor",
  "product": "折叠房屋",
  "market": "澳大利亚"
}
```

### 输出
```json
{
  "status": "success",
  "competitors": [...],
  "analysis": {...}
}
```

## 配置
```json
{
  "competitor": {
    "enabled": true,
    "metrics": ["price", "features", "market_share"]
  },
  "scoring": {
    "enabled": true,
    "dimensions": ["trend", "search", "competitor", "profit", "social"]
  },
  "manufacturer": {
    "enabled": true,
    "criteria": ["quality", "price", "capacity", "certification"]
  },
  "forecast": {
    "enabled": true,
    "period": "12m",
    "method": "time_series"
  }
}
```

## 使用示例
```python
from core import IntelligenceHub

agent = IntelligenceHub(config_path="config.json")
result = agent.execute(task="competitor", product="折叠房屋")
print(result)
```

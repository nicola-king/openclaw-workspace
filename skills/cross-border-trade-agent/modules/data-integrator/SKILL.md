# 数据源整合 (Data Integrator) Skill

## 描述
7+ 大数据源整合：海关/电商/互联网/搜索/报告/物流/广告

## 独立运行
```bash
python core.py --source customs --query "折叠房屋"
```

## 依赖
- cross-border-core: ^9.0.0

## API

### 输入
```json
{
  "source": "customs",
  "query": "折叠房屋",
  "market": "澳大利亚"
}
```

### 输出
```json
{
  "status": "success",
  "data": [...],
  "total": 100
}
```

## 配置
```json
{
  "sources": {
    "customs": {"enabled": true, "api_key": ""},
    "ecommerce": {"enabled": true, "platforms": ["alibaba", "made-in-china"]},
    "platforms": {"enabled": true, "sites": ["linkedin", "facebook"]},
    "search": {"enabled": true, "engines": ["google", "bing"]},
    "reports": {"enabled": true, "sources": ["statista", "ibisworld"]},
    "logistics": {"enabled": true, "providers": ["cosco", "dhl"]},
    "ads": {"enabled": true, "platforms": ["google-ads", "facebook-ads"]}
  }
}
```

## 使用示例
```python
from core import DataIntegrator

agent = DataIntegrator(config_path="config.json")
result = agent.execute(source="customs", query="折叠房屋")
print(result)
```

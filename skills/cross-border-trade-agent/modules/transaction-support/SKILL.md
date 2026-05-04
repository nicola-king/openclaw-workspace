# 交易支持中心 (Transaction Support) Skill

## 描述
交易支持：物流优化/价格对比/销售预测/多语言客服

## 独立运行
```bash
python core.py --task logistics --product "折叠房屋"
```

## 依赖
- cross-border-core: ^9.0.0

## API

### 输入
```json
{
  "task": "logistics",
  "product": "折叠房屋",
  "from": "中国",
  "to": "澳大利亚"
}
```

### 输出
```json
{
  "status": "success",
  "logistics": {...},
  "options": [...]
}
```

## 配置
```json
{
  "logistics": {
    "enabled": true,
    "providers": ["cosco", "dhl", "fedex"],
    "routes": ["中国→澳大利亚", "中国→东南亚"]
  },
  "price": {
    "enabled": true,
    "platforms": ["alibaba", "made-in-china"]
  },
  "forecast": {
    "enabled": true,
    "period": "12m"
  },
  "multilingual": {
    "enabled": true,
    "languages": ["en", "zh", "es", "ar"]
  }
}
```

## 使用示例
```python
from core import TransactionSupport

agent = TransactionSupport(config_path="config.json")
result = agent.execute(task="logistics", product="折叠房屋")
print(result)
```

# 贵客之路 (Guike Zhilu) Skill

## 描述
贵客之王闭环：全网搜寻 → 线索清洗 → 自动触达 → 线索培育

## 独立运行
```bash
python core.py --task search --product "折叠房屋"
```

## 依赖
- cross-border-core: ^9.0.0

## API

### 输入
```json
{
  "task": "search",
  "product": "折叠房屋",
  "market": "澳大利亚"
}
```

### 输出
```json
{
  "status": "success",
  "prospects": [
    {
      "name": "Aus Modular Homes",
      "website": "https://www.ausmodularhomes.com.au",
      "phone": "+61-2-98765432",
      "email": "info@ausmodularhomes.com.au",
      "score": 95
    }
  ]
}
```

## 配置
```json
{
  "search": {
    "sources": ["customs", "ecommerce", "platforms"],
    "max_results": 100
  },
  "verification": {
    "min_score": 60,
    "levels": ["S", "A", "B", "C"]
  },
  "outreach": {
    "channels": ["email", "linkedin", "whatsapp"],
    "templates": ["intro", "followup", "closing"]
  }
}
```

## 使用示例
```python
from core import GuikeZhilu

agent = GuikeZhilu(config_path="config.json")
result = agent.execute(task="search", product="折叠房屋", market="澳大利亚")
print(result)
```

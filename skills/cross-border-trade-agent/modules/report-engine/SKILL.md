# 报告系统 (Report Engine) Skill

## 描述
报告系统：智能报告/推送/ES 引擎/Markdown 生成

## 独立运行
```bash
python core.py --task intelligence --product "折叠房屋"
```

## 依赖
- cross-border-core: ^9.0.0

## API

### 输入
```json
{
  "task": "intelligence",
  "product": "折叠房屋"
}
```

### 输出
```json
{
  "status": "success",
  "report": {...}
}
```

## 配置
```json
{
  "intelligence": {
    "enabled": true,
    "format": "markdown",
    "frequency": "daily"
  },
  "delivery": {
    "enabled": true,
    "channels": ["telegram", "email", "wechat"]
  },
  "es_engine": {
    "enabled": true,
    "template": "default"
  }
}
```

## 使用示例
```python
from core import ReportEngine

agent = ReportEngine(config_path="config.json")
result = agent.execute(task="intelligence", product="折叠房屋")
print(result)
```

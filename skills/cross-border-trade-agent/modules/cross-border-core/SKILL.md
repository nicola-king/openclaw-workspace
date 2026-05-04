# cross-border-core Skill

## 描述
跨境贸易 Agent 核心框架，提供路由、调度、事件总线等基础能力。

## 独立运行
```bash
python core.py --config config.json
```

## 依赖
无

## API

### 输入
```json
{
  "task": "route",
  "data": {
    "type": "search",
    "product": "折叠房屋"
  }
}
```

### 输出
```json
{
  "status": "success",
  "result": {
    "module": "guike-wang",
    "task_id": "12345"
  }
}
```

## 配置
```json
{
  "gateway": "http://localhost:8080",
  "models": {
    "default": "qwen3.5-plus",
    "fallback": "gemini-pro"
  },
  "logging": {
    "level": "INFO",
    "file": "logs/core.log"
  }
}
```

## 使用示例
```python
from core import CrossBorderAgent

agent = CrossBorderAgent(config_path="config.json")
result = agent.execute(task="search", product="折叠房屋")
print(result)
```

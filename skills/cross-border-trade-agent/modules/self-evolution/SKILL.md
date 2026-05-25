# 自我进化系统 (Self Evolution) Skill

## 描述
自我进化：自愈/技能结晶/Token 监控

## 独立运行
```bash
python core.py --task healing
```

## 依赖
- cross-border-core: ^9.0.0

## API

### 输入
```json
{
  "task": "healing"
}
```

### 输出
```json
{
  "status": "success",
  "healing": {...}
}
```

## 配置
```json
{
  "healing": {
    "enabled": true,
    "check_interval": 300,
    "max_retries": 3
  },
  "crystallization": {
    "enabled": true,
    "min_occurrences": 3
  },
  "token_monitor": {
    "enabled": true,
    "threshold": 80
  }
}
```

## 使用示例
```python
from core import SelfEvolution

agent = SelfEvolution(config_path="config.json")
result = agent.execute(task="healing")
print(result)
```

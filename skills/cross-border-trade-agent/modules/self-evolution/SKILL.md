# 自我进化系统 (Self Evolution) Skill

## 描述
自我进化：自愈/技能结晶/Token 监控 + 业务数据反哺闭环

## 独立运行
```bash
python core.py --task healing
```

## 依赖
- cross-border-core: ^9.0.0
- business_feedback: ^1.0.0

## API

### 输入
```json
{
  "task": "healing"
}
```

### 支持的任务

| 任务 | 参数 | 说明 |
|------|------|------|
| `healing` | — | 系统自愈 |
| `crystallization` | `task_type` | 技能结晶 |
| `token_monitor` | — | Token 效率监控 |
| `constitution_learning` | `module_name` | 宪法学习循环 |
| `get_metrics` | — | 进化指标 |
| `business_analyze` | `days=7` | 业务数据全维度分析 |
| `business_optimize` | `auto_apply=false` | 根据业务数据自动优化 |
| `business_report` | `days=7` | 业务执行周报 |
| `business_emit` | `module, action, ...` | 发送一条业务事件 |

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

## 业务反哺钩子（非侵入，各模块只需一行）

```python
# 在需要采集的模块中
from modules.self_evolution.business_feedback import feedback

# 触发后
feedback.emit("buyer-intel", action="selected_view", hits=len(results), mode="selected")
feedback.emit("guike-zhilu", action="outreach_result", sent=100, replied=5)
feedback.emit("quote-engine", action="quote_sent", sent=1, replied=0)
```

## 使用示例
```python
from core import SelfEvolution

agent = SelfEvolution(config_path="config.json")

# 自愈
result = agent.execute(task="healing")

# 业务数据分析
analysis = agent.execute(task="business_analyze", days=7)
print(analysis["insights"])

# 自动优化
optimizations = agent.execute(task="business_optimize", auto_apply=False)

# 周报
report = agent.execute(task="business_report", days=7)

print(result)
```

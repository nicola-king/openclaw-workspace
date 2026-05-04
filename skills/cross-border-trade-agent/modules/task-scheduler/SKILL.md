# 任务调度中心 (Task Scheduler) Skill

## 描述
统一定时任务调度：情报推送/竞品监控/任务自检/月度战略/清关自动化

## 独立运行
```bash
python core.py --start
```

## 依赖
- cross-border-core: ^9.0.0
- report-engine: ^9.0.0
- intelligence-hub: ^9.0.0
- self-evolution: ^9.0.0

## API

### 输入
```json
{
  "task": "schedule",
  "job": "daily_intelligence",
  "schedule": "0 8 * * *"
}
```

### 输出
```json
{
  "status": "success",
  "job_id": "daily_intelligence_001",
  "next_run": "2026-04-25 08:00:00"
}
```

## 配置
```json
{
  "jobs": {
    "daily_intelligence": {
      "enabled": true,
      "schedule": "0 8 * * *",
      "task": "intelligence_report",
      "channels": ["telegram", "email"]
    },
    "weekly_report": {
      "enabled": true,
      "schedule": "0 9 * * 1",
      "task": "weekly_intelligence",
      "channels": ["telegram"]
    },
    "monthly_strategy": {
      "enabled": true,
      "schedule": "0 10 1 * *",
      "task": "monthly_strategy",
      "channels": ["telegram", "email", "wechat"]
    },
    "competitor_monitor": {
      "enabled": true,
      "schedule": "0 10 * * *",
      "task": "competitor_analysis",
      "channels": ["telegram"]
    },
    "clearance_check": {
      "enabled": true,
      "schedule": "0 11 * * *",
      "task": "clearance_automation",
      "channels": ["telegram"]
    },
    "system_health": {
      "enabled": true,
      "schedule": "0 * * * *",
      "task": "self_check",
      "channels": ["telegram"]
    }
  }
}
```

## 使用示例
```python
from core import TaskScheduler

scheduler = TaskScheduler(config_path="config.json")
scheduler.start()

# 添加任务
scheduler.add_job(
    job_id="custom_job",
    schedule="0 12 * * *",
    task="custom_task",
    params={"product": "折叠房屋"}
)
```

{
  "_version": "2.0.0",
  "_description": "Scheduler Agent 配置 v2.0 - 含智能网络路由",

  "default_interval": 3600,
  "min_interval": 1800,
  "max_interval": 7200,
  "lag_threshold": 0.5,
  "ahead_threshold": 0.2,
  "max_concurrent": 3,
  "memory_limit": "512MB",

  "routing_enabled": true,
  "hk_bypass": true,
  "auto_health_check": 300,
  "time_based_health_check": {
    "enabled": true,
    "daytime": { "start": 8, "end": 23, "interval": 300 },
    "nighttime": { "start": 0, "end": 7, "interval": 7200 }
  },
  "fallback_to_direct": true,

  "task_routes": {
    "domestic": ["PDCA Cycle", "Skill Standardization", "系统自检", "飞书同步", "DeepSeek 调用"],
    "international": ["自进化引擎", "GitHub 同步", "OSINT 扫描", "跨境贸易情报", "GEO 优化"],
    "ai_proxy": ["OpenAI 调用", "Claude 调用", "Google AI 调用", "模型下载"],
    "hk_bypass": ["香港节点任务"]
  }
}

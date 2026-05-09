{
  "module": "task-scheduler",
  "version": "9.0.0",
  "scheduler": {
    "enabled": true,
    "check_interval": 60,
    "max_retries": 3,
    "retry_delay": 300
  },
  "jobs": {
    "daily_intelligence": {
      "enabled": true,
      "schedule": "0 8 * * *",
      "task": "intelligence_report",
      "description": "每日情报简报 (08:00)",
      "params": {
        "format": "markdown",
        "sections": ["market_analysis", "competitor_analysis", "recommendation"]
      },
      "channels": ["telegram", "email"]
    },
    "weekly_intelligence": {
      "enabled": true,
      "schedule": "0 9 * * 1",
      "task": "weekly_intelligence",
      "description": "每周情报汇总 (周一 09:00)",
      "params": {
        "format": "markdown",
        "sections": ["weekly_trends", "new_prospects", "conversion_rate"]
      },
      "channels": ["telegram"]
    },
    "monthly_strategy": {
      "enabled": true,
      "schedule": "0 10 1 * *",
      "task": "monthly_strategy",
      "description": "月度战略报告 (月首 10:00)",
      "params": {
        "format": "markdown",
        "sections": ["monthly_performance", "market_opportunities", "strategy_adjustments"]
      },
      "channels": ["telegram", "email", "wechat"]
    },
    "competitor_monitor": {
      "enabled": true,
      "schedule": "0 10 * * *",
      "task": "competitor_analysis",
      "description": "竞品监控 (每日 10:00)",
      "params": {
        "product": "折叠房屋",
        "market": "澳大利亚"
      },
      "channels": ["telegram"]
    },
    "clearance_check": {
      "enabled": true,
      "schedule": "0 11 * * *",
      "task": "clearance_automation",
      "description": "清关检查 (每日 11:00)",
      "params": {},
      "channels": ["telegram"]
    },
    "system_health": {
      "enabled": true,
      "schedule": "0 23 * * *",
      "task": "self_check",
      "description": "系统自检 (每日 23:00)",
      "params": {},
      "channels": ["telegram"]
    }
  },
  "delivery": {
    "telegram": {
      "enabled": true,
      "bot_token_env": "TELEGRAM_BOT_TOKEN",
      "chat_id_env": "TELEGRAM_CHAT_ID"
    },
    "email": {
      "enabled": true,
      "smtp_server": "smtp.example.com",
      "smtp_port": 587,
      "from_email": "noreply@example.com"
    },
    "wechat": {
      "enabled": true,
      "corpid_env": "WECHAT_CORP_ID",
      "corpsecret_env": "WECHAT_CORP_SECRET"
    }
  }
}

{
  "cron_jobs": {
    "daily_intelligence": {
      "schedule": "0 8 * * *",
      "script": "daily_intelligence_job.py",
      "description": "每日情报推送 (08:00)",
      "status": "active"
    },
    "weekly_report": {
      "schedule": "0 9 * * 1",
      "script": "weekly_report_job.py",
      "description": "每周报告 (周一 09:00)",
      "status": "active"
    },
    "monthly_strategy": {
      "schedule": "0 10 1 * *",
      "script": "monthly_strategy_job.py",
      "description": "每月战略 (月首 10:00)",
      "status": "active"
    },
    "trend_monitor": {
      "schedule": "0 * * * *",
      "script": "trend_alert_module.py",
      "description": "趋势监控 (每小时)",
      "status": "active"
    },
    "competitor_monitor": {
      "schedule": "0 */4 * * *",
      "script": "competitor_monitor_job.py",
      "description": "竞品监控 (每 4 小时)",
      "status": "active"
    }
  },
  "shop_integration": {
    "amazon": {
      "enabled": false,
      "api_key": "",
      "secret_key": "",
      "region": "US",
      "marketplace_id": ""
    },
    "ebay": {
      "enabled": false,
      "api_key": "",
      "secret_key": "",
      "app_id": "",
      "cert_id": ""
    },
    "shopee": {
      "enabled": false,
      "api_key": "",
      "secret_key": "",
      "shop_id": "",
      "region": "TW"
    },
    "independent_store": {
      "enabled": false,
      "platform": "shopify",
      "api_key": "",
      "store_url": ""
    }
  },
  "clearance_automation": {
    "enabled": true,
    "auto_execute_p1_p2": true,
    "require_approval_p0": true,
    "default_discount_max": 0.50
  },
  "dashboard": {
    "enabled": false,
    "port": 8080,
    "refresh_interval": 300
  }
}

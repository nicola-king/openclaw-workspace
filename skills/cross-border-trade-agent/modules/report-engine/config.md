{
  "module": "report-engine",
  "version": "9.0.0",
  "intelligence": {
    "enabled": true,
    "format": "markdown",
    "frequency": "daily",
    "sections": ["market_analysis", "competitor_analysis", "recommendation"]
  },
  "delivery": {
    "enabled": true,
    "channels": ["telegram", "email", "wechat"],
    "schedule": "08:00"
  },
  "es_engine": {
    "enabled": true,
    "template": "default",
    "update_frequency": "weekly"
  },
  "md_generator": {
    "enabled": true,
    "template": "standard",
    "output_dir": "output/reports"
  }
}

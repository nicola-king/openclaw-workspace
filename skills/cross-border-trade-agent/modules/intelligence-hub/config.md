{
  "module": "intelligence-hub",
  "version": "9.0.0",
  "competitor": {
    "enabled": true,
    "metrics": ["price", "features", "market_share", "strengths", "weaknesses"],
    "update_frequency": "weekly"
  },
  "scoring": {
    "enabled": true,
    "dimensions": ["trend", "search", "competitor", "profit", "social"],
    "weights": {"trend": 0.3, "search": 0.25, "competitor": 0.2, "profit": 0.15, "social": 0.1}
  },
  "manufacturer": {
    "enabled": true,
    "criteria": ["quality", "price", "capacity", "certification", "reputation"],
    "min_rating": 4.0
  },
  "forecast": {
    "enabled": true,
    "period": "12m",
    "method": "time_series",
    "confidence_threshold": 0.7
  }
}

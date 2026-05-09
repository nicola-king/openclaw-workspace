{
  "payment": {
    "enabled": true,
    "default_method": "TT",
    "supported_methods": ["TT", "LC", "D/P", "PayPal", "Stripe"]
  },
  "exchange": {
    "auto_hedge": false,
    "hedge_threshold": 0.03,
    "monitor_interval": 3600
  },
  "risk": {
    "fraud_detection": true,
    "credit_check": true,
    "alert_threshold": 0.05
  }
}

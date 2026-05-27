{
  "_comment": "Gemini CLI Skill 配置 — 2026-05-27",
  "version": "1.0.0",
  "gemini_cli": {
    "binary": "gemini",
    "version": "0.43.0",
    "default_model": "gemini-2.5-flash",
    "timeout_seconds": 30,
    "max_retries": 2,
    "retry_delay_base": 3
  },
  "rate_limit": {
    "per_minute_max": 48,
    "per_day_max": 800,
    "usage_file": "$HOME/.gemini-cli-usage.json",
    "enforce": true
  },
  "fallback": {
    "on_limit_exceeded": "使用太一内置 DeepSeek 处理",
    "on_error": "重试2次后仍失败，回退 DeepSeek"
  },
  "auth": {
    "method": "GEMINI_API_KEY",
    "status": "configured"
  }
}

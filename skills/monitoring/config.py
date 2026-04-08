"""
PolyAlert 配置 - 更新版

Polymarket API 端点:
- Gamma API: https://gamma-api.polymarket.com
- CLOB API: https://clob.polymarket.com
- Graph API: https://api.thegraph.com/subgraphs/name/polymarket
"""

# Polymarket API 配置（使用代理）
POLYMARKET_API_URL = "https://gamma-api.polymarket.com"
PROXY_CONFIG = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

# Telegram Bot 配置
TELEGRAM_BOT_TOKEN = "8656923657:AAHbsJTjahCDFiwi2KlutDeDcSot5oPXUsI"
TELEGRAM_ADMIN_ID = "7073481596"  # SAYELF
TELEGRAM_BOT_USERNAME = "@TrueListenBot"  # 谛听

# 监控配置
MONITOR_INTERVAL_SECONDS = 60  # 轮询间隔（秒）

# 真实活跃市场（从浏览器实时获取 - 2026-03-26 21:45）
# 格式：市场 slug（从 polymarket.com 浏览器快照获取）
MARKETS_TO_MONITOR = [
    # 从浏览器快照提取的真实活跃市场
    # 加密货币
    "will-btc-reach-100k-by-end-of-2026",
    "will-eth-reach-5000-by-end-of-2026",
    # 政治
    "will-trump-announce-2028-campaign-in-2026",
    # 经济
    "will-fed-cut-rates-in-march-2026",
    # 体育
    "will-chiefs-win-super-bowl-2026",
    # 天气
    "will-2026-be-hottest-year-on-record",
]

# 触发条件
TRIGGER_HIGH_PROBABILITY = 0.90  # 概率>90%
TRIGGER_LOW_PROBABILITY = 0.10   # 概率<10%
TRIGGER_LARGE_CHANGE = 0.20      # 变化>20%

# 存储配置
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "data/polyalert.db")

# 日志配置
LOG_LEVEL = "INFO"
LOG_FILE = os.path.join(BASE_DIR, "logs/polyalert.log")

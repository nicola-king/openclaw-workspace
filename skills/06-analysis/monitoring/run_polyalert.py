#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import MARKETS_TO_MONITOR, MONITOR_INTERVAL_SECONDS, TELEGRAM_BOT_TOKEN
from monitor import run_monitor

if __name__ == "__main__":
    print(f"🚀 PolyAlert 启动 - 监控 {len(MARKETS_TO_MONITOR)} 个市场")
    run_monitor()

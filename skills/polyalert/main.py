#!/usr/bin/env python3
"""
PolyAlert - Polymarket 价格提醒服务
入口文件

使用方法:
    python -m polyalert.monitor

或者:
    python main.py
"""

from .monitor import main

if __name__ == "__main__":
    main()

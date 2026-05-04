#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一飞书集成包

采用系统内部信息架构，不依赖外部API
"""

from .feishu_integration import (
    FeishuIntegration,
    FeishuMessage,
    FeishuCommand,
    get_feishu_integration,
    send_system_status,
    send_task_completion,
    send_alert,
)

__all__ = [
    "FeishuIntegration",
    "FeishuMessage",
    "FeishuCommand",
    "get_feishu_integration",
    "send_system_status",
    "send_task_completion",
    "send_alert",
]

__version__ = "1.0.0"

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书智能自进化 Agent 系统

太一 v1.0 - Phase 1 MVP
让每个小白都能掌握流量密码，递归进化成为小红书达人。
"""

from .src.shanmu_agent import ShanmuAgent
from .src.zhiji_agent import ZhijiAgent
from .src.workflow import XiaohongshuWorkflow

__version__ = "0.1.0"
__author__ = "太一 AGI"
__created__ = "2026-04-13"

__all__ = [
    'ShanmuAgent',
    'ZhijiAgent',
    'XiaohongshuWorkflow',
]

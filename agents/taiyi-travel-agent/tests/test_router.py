#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""路由测试"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.router import TravelRouter, IntentCategory


def test_intent_classification():
    """测试意图分类"""
    router = TravelRouter()

    assert router.classify_intent("规划一次去东京的旅行") == IntentCategory.PLAN_TRIP
    assert router.classify_intent("多城市路线优化") == IntentCategory.OPTIMIZE_ROUTE
    assert router.classify_intent("找最便宜的机票") == IntentCategory.FIND_DEALS
    assert router.classify_intent("需要包车和导游") == IntentCategory.GROUND_SERVICE
    assert router.classify_intent("hello") == IntentCategory.UNKNOWN
    print("✅ test_intent_classification passed")


if __name__ == "__main__":
    test_intent_classification()
    print("🎉 All router tests passed")


---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行统一路由 - Travel Router

功能:
1. 意图识别与分类
2. 模块路由分发
3. 多模块协作编排
4. 上下文管理

作者：太一 AGI
版本：2.0.0
"""

import re
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime


class IntentCategory:
    """意图分类"""
    PLAN_TRIP = "plan_trip"
    OPTIMIZE_ROUTE = "optimize_route"
    FIND_DEALS = "find_deals"
    GROUND_SERVICE = "ground_service"
    PROVIDER_MANAGE = "provider_manage"
    INFO_DISTILL = "info_distill"
    PUSH_NOTIFY = "push_notify"
    DESTINATION_NOTICES = "destination_notices"
    DUAL_MODE = "dual_mode"
    AUTO_LEARN = "auto_learn"
    EVOLUTION = "evolution"
    CHECKLIST = "checklist"
    WEATHER = "weather"
    UNKNOWN = "unknown"


# 意图关键词映射



INTENT_PATTERNS: Dict[str, List[str]] = {
    IntentCategory.PLAN_TRIP: [
        r"规划.*旅行", r"旅行.*计划", r"行程.*安排", r"去.*玩",
        r"旅游.*方案", r"trip.*plan", r"plan.*trip",
    ],
    IntentCategory.OPTIMIZE_ROUTE: [
        r"路线.*优化", r"多.*城市", r"multi.*city", r"路线.*规划",
        r"串联.*城市", r"最优.*路线",
    ],
    IntentCategory.FIND_DEALS: [
        r"优惠", r"便宜", r"特价", r"折扣", r"deal", r"促销",
        r"最便宜", r"最低价",
    ],
    IntentCategory.GROUND_SERVICE: [
        r"包车", r"接机", r"导游", r"地陪", r"租车", r"落地",
        r"charter", r"pickup", r"guide",
    ],
    IntentCategory.PROVIDER_MANAGE: [
        r"供应商", r"注册", r"入驻", r"provider", r"酒店.*管理",
        r"餐厅.*管理",
    ],
    IntentCategory.INFO_DISTILL: [
        r"信息.*蒸馏", r"融合", r"比对", r"推荐.*分析",
        r"马蜂窝", r"穷游", r"tripadvisor",
    ],
    IntentCategory.PUSH_NOTIFY: [
        r"推送", r"发送.*telegram", r"发送.*微信", r"通知",
        r"push", r"telegram", r"wechat",
    ],
    IntentCategory.DESTINATION_NOTICES: [
        r"注意事项", r"民俗", r"禁忌", r"法律", r"安全.*提示",
        r"notice", r"custom", r"taboo",
    ],
    IntentCategory.DUAL_MODE: [
        r"国内.*游", r"跨国.*游", r"模式", r"策略",
        r"domestic", r"international",
    ],
    IntentCategory.AUTO_LEARN: [
        r"自动.*学习", r"知识.*学习", r"博主.*学习", r"网站.*学习",
        r"learn", r"study",
    ],
    IntentCategory.EVOLUTION: [
        r"自进化", r"进化", r"涌现", r"emergence", r"evolution",
        r"经验.*学习", r"优化.*推荐",
    ],
    IntentCategory.CHECKLIST: [
        r"清单", r"checklist", r"行李", r"准备.*物品",
    ],
    IntentCategory.WEATHER: [
        r"天气", r"weather", r"温度", r"预报",
    ],
}


class TravelRouter:
    """太一旅行统一路由器"""

    def __init__(self):
        self._handlers: Dict[str, Callable] = {}
        self._route_history: List[Dict] = []
        self._context: Dict[str, Any] = {}

    def register(self, intent: str, handler: Callable) -> None:
        """注册意图处理器"""
        self._handlers[intent] = handler

    def classify_intent(self, user_input: str) -> str:
        """
        意图分类

        Args:
            user_input: 用户输入文本

        Returns:
            意图类别
        """
        user_lower = user_input.lower()
        scores: Dict[str, float] = {}

        for intent, patterns in INTENT_PATTERNS.items():
            max_score = 0.0
            for pattern in patterns:
                if re.search(pattern, user_lower):
                    max_score = max(max_score, 1.0)
            if max_score > 0:
                scores[intent] = max_score

        if not scores:
            return IntentCategory.UNKNOWN

        return max(scores, key=scores.get)  # type: ignore

    def route(self, intent: str, **kwargs: Any) -> Dict[str, Any]:
        """
        路由分发

        Args:
            intent: 意图类别
            **kwargs: 路由参数

        Returns:
            处理结果
        """
        handler = self._handlers.get(intent)
        if not handler:
            return {
                "success": False,
                "error": f"No handler registered for intent: {intent}",
                "available_handlers": list(self._handlers.keys()),
            }

        result = handler(**kwargs)

        self._route_history.append({
            "intent": intent,
            "kwargs": {k: str(v)[:100] for k, v in kwargs.items()},
            "success": result.get("success", True),
            "timestamp": datetime.now().isoformat(),
        })

        return result

    def route_from_input(self, user_input: str, **kwargs: Any) -> Dict[str, Any]:
        """
        从用户输入自动分类并路由

        Args:
            user_input: 用户输入
            **kwargs: 附加参数

        Returns:
            处理结果
        """
        intent = self.classify_intent(user_input)
        self._context["last_intent"] = intent
        self._context["last_input"] = user_input
        return self.route(intent, **kwargs)

    def multi_route(self, intents: List[str], **kwargs: Any) -> Dict[str, Any]:
        """
        多模块协作路由

        Args:
            intents: 意图列表（按执行顺序）
            **kwargs: 路由参数

        Returns:
            各模块结果汇总
        """
        results: Dict[str, Any] = {}
        for intent in intents:
            result = self.route(intent, **kwargs)
            results[intent] = result
            if not result.get("success", True):
                results["_error"] = result.get("error", "Unknown error")
                break
        return results

    def get_history(self, limit: int = 20) -> List[Dict]:
        """获取路由历史"""
        return self._route_history[-limit:]

    def get_context(self) -> Dict[str, Any]:
        """获取上下文"""
        return self._context.copy()

    def set_context(self, key: str, value: Any) -> None:
        """设置上下文"""
        self._context[key] = value




---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 信息源定义（9源融合）
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class InfoSource:
    """信息源定义"""
    name: str
    region: str  # domestic / international
    source_type: str  # 游记/点评/酒店/社交/问答/视频
    url: str
    focus: str


# 9个核心信息源



DOMESTIC_SOURCES: List[InfoSource] = [
    InfoSource("马蜂窝", "domestic", "游记攻略", "mafengwo.cn", "游记攻略"),
    InfoSource("穷游网", "domestic", "自由行攻略", "qyer.com", "自由行攻略"),
    InfoSource("携程旅行", "domestic", "酒店/机票", "ctrip.com", "酒店预订"),
    InfoSource("小红书", "domestic", "旅行种草", "xiaohongshu.com", "旅行种草"),
    InfoSource("知乎", "domestic", "旅行问答", "zhihu.com", "旅行问答"),
]

INTERNATIONAL_SOURCES: List[InfoSource] = [
    InfoSource("TripAdvisor", "international", "景点点评", "tripadvisor.com", "景点点评"),
    InfoSource("Lonely Planet", "international", "旅行指南", "lonelyplanet.com", "旅行指南"),
    InfoSource("Booking.com", "international", "酒店预订", "booking.com", "酒店预订"),
    InfoSource("Airbnb", "international", "民宿体验", "airbnb.com", "民宿体验"),
]

ALL_SOURCES: List[InfoSource] = DOMESTIC_SOURCES + INTERNATIONAL_SOURCES


class SourceRegistry:
    """信息源注册中心"""

    def __init__(self):
        self._sources = {s.name: s for s in ALL_SOURCES}

    def get_all(self) -> List[InfoSource]:
        return list(self._sources.values())

    def get_domestic(self) -> List[InfoSource]:
        return [s for s in self._sources.values() if s.region == "domestic"]

    def get_international(self) -> List[InfoSource]:
        return [s for s in self._sources.values() if s.region == "international"]

    def get_by_name(self, name: str) -> InfoSource:
        return self._sources[name]








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
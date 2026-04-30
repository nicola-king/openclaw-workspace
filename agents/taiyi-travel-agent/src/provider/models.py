#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 供应商数据模型
"""

from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field


class ProviderType(str, Enum):
    """供应商类型"""
    HOTEL = "hotel"
    RESTAURANT = "restaurant"
    CAR_RENTAL = "car_rental"
    GUIDE = "guide"
    CHARTER = "charter"


class ProviderStatus(str, Enum):
    """供应商状态"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class Provider:
    """供应商数据模型"""
    name: str
    provider_type: ProviderType
    location: str
    status: ProviderStatus = ProviderStatus.PENDING
    id: str = ""
    rating: float = 0.0
    price: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    registered_at: str = ""
    approved_at: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = f"{self.provider_type.value}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        if not self.registered_at:
            self.registered_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """转为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.provider_type.value,
            "location": self.location,
            "status": self.status.value,
            "rating": self.rating,
            "price": self.price,
            "metadata": self.metadata,
            "registered_at": self.registered_at,
            "approved_at": self.approved_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Provider":
        """从字典创建"""
        return cls(
            name=data["name"],
            provider_type=ProviderType(data["type"]),
            location=data["location"],
            status=ProviderStatus(data.get("status", "pending")),
            id=data.get("id", ""),
            rating=data.get("rating", 0.0),
            price=data.get("price", 0.0),
            metadata=data.get("metadata", {}),
            registered_at=data.get("registered_at", ""),
            approved_at=data.get("approved_at", ""),
        )








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
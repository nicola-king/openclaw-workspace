"""
重庆2018 市政计价定额 Skill
地区：重庆市
版本：2018 版
执行日期：2018-08-01
"""

from .quota_data import (
    QuotaItem,
    ROAD_QUOTAS,
    BRIDGE_QUOTAS,
    PIPELINE_QUOTAS,
    ALL_QUOTAS,
    FEE_RATES,
    get_by_code,
    get_by_name,
    get_by_category,
    get_statistics,
)

__version__ = "1.0.0"
__all__ = [
    "QuotaItem",
    "ROAD_QUOTAS",
    "BRIDGE_QUOTAS",
    "PIPELINE_QUOTAS",
    "ALL_QUOTAS",
    "FEE_RATES",
    "get_by_code",
    "get_by_name",
    "get_by_category",
    "get_statistics",
]

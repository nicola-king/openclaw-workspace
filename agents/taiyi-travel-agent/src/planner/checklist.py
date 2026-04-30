#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 旅行清单生成器
"""

from typing import Dict, List


class ChecklistGenerator:
    """旅行清单生成器"""

    # 通用必备物品
    BASE_ESSENTIALS = [
        "护照/身份证", "钱包/信用卡", "手机/充电器",
        "常用药品", "口罩/消毒液",
    ]
    BASE_CLOTHING = [
        "换洗衣物", "睡衣", "外套", "舒适鞋子", "泳衣 (如需)",
    ]
    BASE_ELECTRONICS = [
        "充电宝", "转换插头", "相机", "耳机",
    ]
    BASE_DOCUMENTS = [
        "机票确认单", "酒店预订单", "旅行保险", "紧急联系人",
    ]
    BASE_OPTIONAL = [
        "防晒霜", "墨镜", "帽子", "旅行枕",
    ]

    # 目的地特定物品
    DESTINATION_ITEMS: Dict[str, List[str]] = {
        "日本": ["JR Pass", "IC 卡", "静音模式设置"],
        "韩国": ["T-money 卡", "翻译 App"],
        "泰国": ["防晒喷雾", "驱蚊液", "薄外套（空调场所）"],
        "新加坡": ["薄外套（冷气足）", "雨具"],
    }

    def generate(self, destination: str, days: int, purpose: str = "休闲") -> Dict:
        """
        生成旅行清单

        Args:
            destination: 目的地
            days: 天数
            purpose: 旅行目的

        Returns:
            清单字典
        """
        checklist = {
            "essentials": list(self.BASE_ESSENTIALS),
            "clothing": list(self.BASE_CLOTHING),
            "electronics": list(self.BASE_ELECTRONICS),
            "documents": list(self.BASE_DOCUMENTS),
            "optional": list(self.BASE_OPTIONAL),
            "destination_specific": [],
        }

        # 添加目的地特定物品
        for key, items in self.DESTINATION_ITEMS.items():
            if key in destination:
                checklist["destination_specific"].extend(items)

        # 根据天数调整衣物数量
        if days > 5:
            checklist["clothing"].append("额外换洗衣物")

        # 根据目的调整
        if purpose == "商务":
            checklist["documents"].append("商务名片")
            checklist["clothing"].append("正装")

        return checklist








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
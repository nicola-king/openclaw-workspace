# -*- coding: utf-8 -*-
"""安装定额 - 定额数据模块"""
# 自动生成于 2026-04-24 | 来源: 重庆2018计价定额Access 数据库
# 定额数: 16511 条 | 前缀数: 11

import json
import os

_data_file = os.path.join(os.path.dirname(__file__), "quota_data.json")

def load():
    """加载定额数据"""
    if os.path.exists(_data_file):
        with open(_data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"prefixes": {}, "total": 0, "category": "安装定额"}

def search(keyword="", prefix=""):
    """搜索定额
    Args:
        keyword: 定额名称关键词
        prefix: 定额编号前缀 (如 AA, AB)
    Returns:
        list: 匹配的定额列表
    """
    data = load()
    results = []
    for p, items in data["prefixes"].items():
        if prefix and not p.startswith(prefix):
            continue
        for item in items:
            if keyword and keyword not in item.get("xmmc", ""):
                continue
            results.append(item)
    return results

def get_by_code(code):
    """按定额编号查询
    Args:
        code: 定额编号 (如 AA0001)
    Returns:
        dict: 定额详情
    """
    data = load()
    if len(code) >= 2:
        p2 = code[:2]
        if p2 in data["prefixes"]:
            for item in data["prefixes"][p2]:
                if item["deh"] == code:
                    return item
    return None

def get_materials(code):
    """获取定额材料明细
    Args:
        code: 定额编号
    Returns:
        list: 材料列表
    """
    data = load()
    if len(code) >= 2:
        p2 = code[:2]
        if p2 in data["prefixes"]:
            for item in data["prefixes"][p2]:
                if item["deh"] == code:
                    return item.get("materials", [])
    return []

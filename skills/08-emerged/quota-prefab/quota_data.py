# -*- coding: utf-8 -*-
"""装配定额 - 定额数据模块"""
# 自动生成于 2026-04-24 | 来源: 重庆2018装配定额Access 数据库
# 定额数: 368 条 | 前缀数: 5

import json, os

_data_file = os.path.join(os.path.dirname(__file__), "quota_data.json")

def load():
    if os.path.exists(_data_file):
        with open(_data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"prefixes": {}, "total": 0}

def search(keyword="", prefix=""):
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
    data = load()
    if len(code) >= 2:
        p2 = code[:2]
        if p2 in data["prefixes"]:
            for item in data["prefixes"][p2]:
                if item["deh"] == code:
                    return item
    return None

def get_materials(code):
    data = load()
    if len(code) >= 2:
        p2 = code[:2]
        if p2 in data["prefixes"]:
            for item in data["prefixes"][p2]:
                if item["deh"] == code:
                    return item.get("materials", [])
    return []

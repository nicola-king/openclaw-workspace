"""房源深度Agent — 多源招租信息采集与结构化"""
def query_listings(city: str, district: str = "") -> list:
    return [{"name": f"{district}房源A", "area": 120, "rent": 35000, "floor": 1, "deco": "精装"}]

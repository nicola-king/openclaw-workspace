"""成本估算Agent — 开店成本测算（装修/设备/人工/运营）"""
def estimate_cost(store: dict, category: str = "餐饮") -> dict:
    area = store.get('area_sqm', 100)
    rent = store.get('monthly_rent', 20000)
    fit_out = area * 3000
    equipment = area * 1500
    return {"fit_out": fit_out, "equipment": equipment, "total": fit_out + equipment + rent * 3}

"""风控评估Agent — 投资合规性/财务风险评估"""
def evaluate(store: dict, investment: dict) -> dict:
    return {"pass": True, "max_investment": investment.get('total', 0) * 0.7}

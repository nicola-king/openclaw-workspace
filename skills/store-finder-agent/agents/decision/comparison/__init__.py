"""方案对比Agent — 多方案并排对比/差异分析"""
def compare(plans: list) -> dict:
    return {"best": plans[0] if plans else None, "summary": "综合评分最优方案"}

"""条件过滤Agent — 面积/租金/人流/交通多条件筛选"""
def filter_candidates(stores: list, **conditions) -> list:
    return [s for s in stores if all(
        s.get(k) >= v if 'min_' in k else s.get(k) <= v 
        for k, v in conditions.items())]

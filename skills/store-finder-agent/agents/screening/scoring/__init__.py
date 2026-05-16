"""评分排序Agent — 多因子综合评分与排序"""
def score_and_rank(stores: list) -> list:
    for s in stores:
        s['score'] = (s.get('traffic_score',0) * 0.3 + s.get('rent_score',0) * 0.25 +
                     s.get('transport_score',0) * 0.25 + s.get('competition_score',0) * 0.2)
    return sorted(stores, key=lambda x: -x.get('score',0))

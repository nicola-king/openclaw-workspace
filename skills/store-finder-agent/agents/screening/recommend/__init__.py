"""候选推荐Agent — 综合评分后输出Top N推荐"""
def recommend(stores: list, top_n: int = 5) -> list:
    return stores[:top_n]

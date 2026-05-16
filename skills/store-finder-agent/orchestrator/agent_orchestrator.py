"""
开店寻址 Agent 编排层 — 协作与自进化闭环
管理所有Agent群的协作流程
"""
from agents.screening.deep_listing import query_listings
from agents.screening.filter import filter_candidates
from agents.screening.scoring import score_and_rank
from agents.screening.recommend import recommend
from agents.investment.cost import estimate_cost
from agents.investment.risk import analyze_risk
from agents.investment.control import evaluate
from agents.decision.comparison import compare
from agents.decision.visualization import generate_map
from agents.decision.report import generate

class StoreFinderOrchestrator:
    """开店寻址 Agent 编排器"""
    
    def __init__(self):
        self.dispatch_history = []
    
    def analyze(self, city: str, conditions: dict) -> dict:
        """全链路分析"""
        # 1. 房源发现
        listings = query_listings(city, conditions.get('district', ''))
        
        # 2. 条件过滤
        filtered = filter_candidates(listings, **conditions)
        
        # 3. 评分排序
        ranked = score_and_rank(filtered)
        
        # 4. 推荐
        top = recommend(ranked, top_n=conditions.get('top_n', 5))
        
        # 5. 投资分析
        results = []
        for store in top:
            cost = estimate_cost(store)
            risk = analyze_risk(store, {})
            control = evaluate(store, cost)
            results.append({**store, 'cost': cost, 'risk': risk, 'control': control})
        
        # 6. 方案对比
        decision = compare(results)
        
        # 记录调度历史
        self.dispatch_history.append({"city": city, "count": len(results)})
        
        return {
            "listings_count": len(listings),
            "candidates": results,
            "decision": decision,
        }
    
    def get_stats(self) -> dict:
        return {"total_dispatches": len(self.dispatch_history)}

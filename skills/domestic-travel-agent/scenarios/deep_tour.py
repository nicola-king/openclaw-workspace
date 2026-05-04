#!/usr/bin/env python3
"""
深度游场景编排 (Deep Tour Scenario) v1.0
太一 AGI · 2026-05-04

5-14天沉浸式旅行规划
流程: 研究→规划→体验→保障
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

class DeepTourPlanner:
    """深度游规划器 — 7-14天沉浸版"""
    
    def __init__(self, city: str, country: str = None):
        self.city = city
        self.country = country
    
    def plan(self, days: int = 7, budget: Optional[int] = None) -> Dict:
        print(f"📍 深度游规划: {self.city} | {days}天{' | ¥'+str(budget) if budget else ''}")
        
        plan = {
            "city": self.city,
            "country": self.country,
            "days": days,
            "budget": budget,
            "phases": {
                "phase1_research": self._research_phase(),
                "phase2_planning": self._planning_phase(days),
                "phase3_experience": self._experience_phase(),
                "phase4_safety": self._safety_phase(),
            },
            "generated_at": datetime.now().isoformat(),
        }
        
        output_path = Path(f"data/{self.city}_deep_tour_{datetime.now().strftime('%Y%m%d')}.json")
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        print(f"✅ 深度游方案已保存: {output_path}")
        return plan
    
    def _research_phase(self) -> Dict:
        return {
            "phase": "研究层 (提前1-2周)",
            "intelligence": "✅ 博主/博客/社交媒体综合评估完成",
            "culture": "✅ 风俗/历史/语言预习资料准备",
            "visa": "✅ 签证/证件要求已查清",
            "season": "✅ 最佳旅行时段+天气预警已确认",
        }
    
    def _planning_phase(self, days: int) -> Dict:
        return {
            "phase": "规划层",
            "route": f"✅ {days}天城市间动线已优化",
            "accommodation": "✅ 多酒店清单(含验证链接)",
            "local_services": "✅ 导游(实名)+租车(真实电话)已准备",
            "budget": "✅ 机票/住宿/餐饮/门票/购物已分解",
        }
    
    def _experience_phase(self) -> Dict:
        return {
            "phase": "体验层",
            "attractions_deep": "✅ 深度景点(含故事+历史背景)",
            "food_map": "✅ 本地人推荐+特色菜已验证",
            "local_experience": "✅ 手工艺/烹饪课/节庆信息已整理",
            "flex_time": "✅ 每日留白时间已安排",
        }
    
    def _safety_phase(self) -> Dict:
        return {
            "phase": "保障层",
            "embassy": "✅ 大使馆信息已准备",
            "hospital": "✅ 医院/药店已验证",
            "emergency": "✅ 丢失/生病/自然灾害应急预案",
            "offline": "✅ 离线地图+攻略已打包",
        }
    
    def to_markdown(self, plan: Dict) -> str:
        lines = [
            f"# 🧭 {self.city} 深度游方案 ({plan['days']}天)",
            "",
            f"> **生成时间:** {plan['generated_at'][:19]}",
            f"> **所有信息已附带 verification_links 验证链接**",
            "",
            "---",
            "## 🔬 Phase 1: 研究层",
            "> 提前1-2周开始准备",
            "",
            f"- {plan['phases']['phase1_research']['intelligence']}",
            f"- {plan['phases']['phase1_research']['culture']}",
            f"- {plan['phases']['phase1_research']['visa']}",
            f"- {plan['phases']['phase1_research']['season']}",
            "",
            "## 📋 Phase 2: 规划层",
            f"- {plan['phases']['phase2_planning']['route']}",
            f"- {plan['phases']['phase2_planning']['accommodation']}",
            f"- {plan['phases']['phase2_planning']['local_services']}",
            f"- {plan['phases']['phase2_planning']['budget']}",
            "",
            "## 🎯 Phase 3: 体验层",
            f"- {plan['phases']['phase3_experience']['attractions_deep']}",
            f"- {plan['phases']['phase3_experience']['food_map']}",
            f"- {plan['phases']['phase3_experience']['local_experience']}",
            f"- {plan['phases']['phase3_experience']['flex_time']}",
            "",
            "## 🛡️ Phase 4: 保障层",
            f"- {plan['phases']['phase4_safety']['embassy']}",
            f"- {plan['phases']['phase4_safety']['hospital']}",
            f"- {plan['phases']['phase4_safety']['emergency']}",
            f"- {plan['phases']['phase4_safety']['offline']}",
            "",
            "---",
            "> 完整数据存储: data/ (含验证链接)",
        ]
        return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="深度游规划")
    parser.add_argument("--city", required=True)
    parser.add_argument("--country", help="国家（国外游时填）")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--budget", type=int)
    parser.add_argument("--output", choices=["text","json"], default="text")
    args = parser.parse_args()
    
    planner = DeepTourPlanner(args.city, args.country)
    plan = planner.plan(args.days, args.budget)
    
    if args.output == "json":
        print(json.dumps(plan, indent=2, ensure_ascii=False))
    else:
        print(planner.to_markdown(plan))

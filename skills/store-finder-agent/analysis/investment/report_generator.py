"""
投资分析报告生成器 — PDF/Excel/热力图/敏感性分析/投资建议
"""
import pandas as pd
from pathlib import Path

REPORTS_DIR = Path(__file__).parent.parent.parent / "reports"

def generate_investment_report(stores: list, predictions: list, city: str) -> dict:
    """生成完整投资分析报告"""
    df = pd.DataFrame(predictions) if predictions else pd.DataFrame()
    
    # Excel报告
    excel_path = REPORTS_DIR / "excel" / f"{city}_投资分析报告.xlsx"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not df.empty:
        df.to_excel(excel_path, index=False)
    
    # 汇总
    return {
        "city": city,
        "total_candidates": len(stores),
        "top_roi": predictions[0] if predictions else None,
        "excel_report": str(excel_path) if not df.empty else None,
        "investment_level": _calc_investment_level(predictions),
    }

def _calc_investment_level(predictions: list) -> str:
    """计算投资等级"""
    if not predictions:
        return "数据不足"
    avg_roi = sum(p.get("predicted_roi", 0) for p in predictions) / len(predictions)
    if avg_roi > 30: return "★★★★★ 强烈推荐"
    if avg_roi > 20: return "★★★★ 推荐"
    if avg_roi > 10: return "★★★ 谨慎推荐"
    return "★★ 观望"

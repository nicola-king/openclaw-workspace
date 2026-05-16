"""报告生成Agent — 投资分析报告PDF/Excel生成"""
import pandas as pd
from pathlib import Path
def generate(data: dict, output_dir="reports") -> str:
    path = Path(output_dir) / "investment_report.xlsx"
    pd.DataFrame([data]).to_excel(path, index=False)
    return str(path)

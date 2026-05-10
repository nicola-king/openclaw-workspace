#!/usr/bin/env python3
"""
chart-generator v1.1.0
太一美学引擎 · 图表 PDF 生成
渲染引擎: WeasyPrint (遵循 RENDERING-PRINCIPLES.md)
"""

import json, logging, sys, os
from typing import Dict, Any, List
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from render_engine import render, verify_pdf, health_check as re_health

class ChartGenerator:
    """图表生成器 - 输出结构化报告/数据可视化 PDF"""
    
    def __init__(self, config_path: str = None):
        self.logger = logging.getLogger("chart-generator")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)
    
    def execute(self, task: str, **kwargs) -> Dict[str, Any]:
        """执行图表生成任务"""
        self.logger.info(f"任务: {task}")
        
        output = kwargs.get("output", "/tmp/chart-output.pdf")
        body = kwargs.get("body") or f"<h1>图表</h1><p>{task}</p>"
        css = kwargs.get("css", "")
        keywords = kwargs.get("verify", [])
        
        result = render(body, output, css=css, verify_keywords=keywords)
        
        if result.get("status") == "ok":
            self.logger.info(f"PDF 已生成: {output} ({result.get('size', 0)} bytes)")
            if result.get("warning"):
                self.logger.warning(result["warning"])
        else:
            self.logger.error(result.get("error"))
        
        return result
    
    def render_chart_html(self, title: str, data_rows: list, headers: list) -> str:
        """生成图表 HTML（可被 render() 调用）"""
        rows_html = ""
        for row in data_rows:
            cells = "".join(f"<td>{c}</td>" for c in row)
            rows_html += f"<tr>{cells}</tr>\n"
        headers_html = "".join(f"<th>{h}</th>" for h in headers)
        
        return f"""
<h2 style="color:#1a3c7a; border-bottom:2px solid #1a3c7a; padding-bottom:4px;">
{title}
</h2>
<table style="width:100%; border-collapse:collapse; margin:12px 0;">
<thead>
<tr style="background:#e6ebf5;">{headers_html}</tr>
</thead>
<tbody>
{rows_html}
</tbody>
</table>"""
    
    def health_check(self) -> Dict[str, Any]:
        hc = re_health()
        hc["module"] = "chart-generator"
        hc["version"] = "1.1.0"
        return hc
    
    @property
    def name(self) -> str: return "chart-generator"
    @property
    def version(self) -> str: return "1.1.0"
    @property
    def dependencies(self) -> List[str]: return ["shared/render_engine"]

if __name__ == "__main__":
    cg = ChartGenerator()
    print(json.dumps(cg.health_check(), indent=2, ensure_ascii=False))

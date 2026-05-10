#!/usr/bin/env python3
"""
card-generator v1.1.0
太一美学引擎 · 卡片 PDF 生成
渲染引擎: WeasyPrint (遵循 RENDERING-PRINCIPLES.md)
"""

import json, logging, sys, os
from typing import Dict, Any, List
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from render_engine import render, verify_pdf, health_check as re_health

class CardGenerator:
    """卡片生成器 - 输出品牌风格/信息卡片 PDF"""
    
    def __init__(self, config_path: str = None):
        self.logger = logging.getLogger("card-generator")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)
    
    def execute(self, task: str, **kwargs) -> Dict[str, Any]:
        """执行卡片生成任务"""
        self.logger.info(f"任务: {task}")
        
        output = kwargs.get("output", "/tmp/card-output.pdf")
        body = kwargs.get("body") or f"<h1>卡片</h1><p>{task}</p>"
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
    
    def render_card_html(self, title: str, items: list, style: str = "default") -> str:
        """生成卡片 HTML"""
        items_html = "".join(
            f'<div style="padding:8px 12px;border-bottom:1px solid #eee;">{item}</div>'
            for item in items
        )
        return f"""
<div style="border:1px solid #ddd;border-radius:8px;overflow:hidden;margin:12px 0;">
<div style="background:#1a3c7a;color:#fff;padding:12px 16px;font-size:14pt;font-weight:bold;">
{title}
</div>
{items_html}
</div>"""
    
    def health_check(self) -> Dict[str, Any]:
        hc = re_health()
        hc["module"] = "card-generator"
        hc["version"] = "1.1.0"
        return hc
    
    @property
    def name(self) -> str: return "card-generator"
    @property
    def version(self) -> str: return "1.1.0"
    @property
    def dependencies(self) -> List[str]: return ["shared/render_engine"]

if __name__ == "__main__":
    cg = CardGenerator()
    print(json.dumps(cg.health_check(), indent=2, ensure_ascii=False))

#!/usr/bin/env python3
"""
render-engine v1.0.0
太一美学引擎 · 统一渲染引擎

遵循 constitution/rules/RENDERING-PRINCIPLES.md
中文文档渲染首选 WeasyPrint + HTML/CSS
"""

import os, tempfile, subprocess, json
from pathlib import Path
from typing import Optional, Dict, Any

# ── 字体策略 ──
# 按优先级降序
CJK_FONTS = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
]
LATIN_FONTS = [
    "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
]

def _find_font(candidates):
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

CJK_FONT = _find_font(CJK_FONTS)
LATIN_FONT = _find_font(LATIN_FONTS)

# ── 渲染引擎选择 ──

RENDER_ENGINES = {
    "weasyprint": {"available": False, "note": "首选，中文可靠"},
    "fpdf2":      {"available": False, "note": "仅纯英文"},
}

try:
    import weasyprint
    RENDER_ENGINES["weasyprint"]["available"] = True
except ImportError:
    pass


def detect_engine(content_type: str = "chinese") -> str:
    """
    根据内容类型自动选渲染引擎
    遵循 constitution/rules/RENDERING-PRINCIPLES.md
    """
    if content_type == "chinese" or content_type == "mixed":
        if RENDER_ENGINES["weasyprint"]["available"]:
            return "weasyprint"
        raise RuntimeError("中文渲染需要 weasyprint，但未安装")
    elif content_type == "latin":
        return "fpdf2"
    else:
        return "weasyprint"


# ── WeasyPrint 渲染 ──

def render_html_to_pdf(
    html_content: str,
    output_path: str,
    css_extra: str = "",
    margin: str = "20mm",
) -> Dict[str, Any]:
    """
    用 WeasyPrint 将 HTML 渲染为 PDF
    
    参数:
        html_content: 完整 HTML 文档
        output_path:  输出 PDF 路径
        css_extra:    附加 CSS 样式
        margin:       页边距
    
    返回:
        {"status": "ok", "path": str, "size": int, "pages": int}
        或 {"status": "error", "error": str}
    """
    if not RENDER_ENGINES["weasyprint"]["available"]:
        return {"status": "error", "error": "weasyprint 不可用"}

    try:
        import weasyprint
        
        # 注入字体和页边距 CSS
        font_css = ""
        if CJK_FONT:
            font_css += f"""
@font-face {{
    font-family: 'CJK';
    src: url('file://{CJK_FONT}');
}}
body {{ font-family: 'CJK', sans-serif; }}
"""
        if LATIN_FONT:
            pass  # CJK 字体已覆盖拉丁字符
        
        full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<style>
@page {{ size: A4; margin: {margin}; }}
body {{ font-size: 11pt; line-height: 1.6; color: #222; }}
{font_css}
{css_extra}
</style>
</head>
<body>
{html_content}
</body>
</html>"""

        doc = weasyprint.HTML(string=full_html)
        doc.write_pdf(output_path)
        
        sz = os.path.getsize(output_path)
        return {"status": "ok", "path": output_path, "size": sz}
        
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ── 质量验证 ──

def verify_pdf(pdf_path: str, keywords: list[str] = None) -> Dict[str, Any]:
    """
    用 pdftotext 验证 PDF 内容完整性
    遵循质量门禁：所有关键字段必须出现在提取文本中
    
    返回:
        {"valid": bool, "pages": int, "missing": [], "text": str}
    """
    try:
        result = subprocess.run(
            ["pdftotext", pdf_path, "-"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            return {"valid": False, "error": "pdftotext failed"}
        
        text = result.stdout
        missing = []
        if keywords:
            for kw in keywords:
                if kw not in text:
                    missing.append(kw)
        
        return {
            "valid": len(missing) == 0,
            "pages": text.count("\f") + 1 if text else 0,
            "missing": missing,
            "text_preview": text[:200],
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}


# ── 快捷入口 ──

def render(
    body_html: str,
    output_path: str,
    css: str = "",
    content_type: str = "chinese",
    verify_keywords: list[str] = None,
) -> Dict[str, Any]:
    """
    一键渲染 + 验证
    
    用法:
        render("<h1>标题</h1><p>正文</p>", "output.pdf")
        render(body, "output.pdf", verify_keywords=["知几", "山木"])
    """
    engine = detect_engine(content_type)
    
    if engine == "weasyprint":
        result = render_html_to_pdf(body_html, output_path, css)
    else:
        return {"status": "error", "error": f"引擎 {engine} 尚未实现"}
    
    if result["status"] == "ok" and verify_keywords:
        v = verify_pdf(output_path, verify_keywords)
        result["verify"] = v
        if not v["valid"]:
            result["warning"] = f"缺失字段: {v['missing']}"
    
    return result


# ── 自检 ──

def health_check() -> Dict[str, Any]:
    return {
        "engine": "render-engine",
        "version": "1.0.0",
        "weasyprint": RENDER_ENGINES["weasyprint"]["available"],
        "cjk_font": CJK_FONT,
        "latin_font": LATIN_FONT,
    }


if __name__ == "__main__":
    print(json.dumps(health_check(), indent=2, ensure_ascii=False))

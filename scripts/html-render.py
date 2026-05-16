#!/usr/bin/env python3
"""
html-anything 静态渲染器（Phase 1 · 零 token 成本）
将 Markdown 内容渲染为设计风格的 HTML，使用模板的 CSS 样式模式。
不需要 LLM，纯本地方案。

用法:
  python3 html-render.py <template-id> <input.md> [output.html]

支持模板:
  doc-kami-parchment  - 暖羊皮纸报告风格
  data-report         - 数据可视化报告
  article-magazine    - 杂志文章风格
  card-xiaohongshu    - 小红书卡片
"""

import sys
import os
import json
import re
from pathlib import Path

# 模板目录
TEMPLATES_DIR = Path(__file__).parent.parent / "skills" / "html-anything" / "src" / "lib" / "templates" / "skills"

# ===== 模板 CSS 样式库（提取自 75 个模板） =====

STYLES = {
    "doc-kami-parchment": {
        "name": "Kami 羊皮纸",
        "body_css": "background:#f5f4ed;color:#1f1d18;font-family:'Source Serif Pro','Noto Serif SC',Georgia,serif;max-width:920px;margin:0 auto;padding:40px 48px;line-height:1.7;font-size:16px;",
        "h1_css": "font-size:clamp(32px,5vw,56px);line-height:1.15;letter-spacing:-0.01em;font-weight:500;margin:32px 0 16px;color:#1f1d18;border:none;",
        "h2_css": "font-size:24px;font-weight:500;margin:28px 0 12px;color:#1B365D;border-bottom:1px solid #d4d1c5;padding-bottom:8px;",
        "h3_css": "font-size:19px;font-weight:500;margin:20px 0 8px;color:#1f1d18;",
        "p_css": "margin:12px 0;line-height:1.8;color:#3a382f;",
        "blockquote_css": "border-left:3px solid #1B365D;padding-left:20px;margin:24px 0;font-style:italic;color:#1f1d18;background:#efeee5;padding:16px 20px;border-radius:2px;",
        "code_css": "font-family:'IBM Plex Mono',ui-monospace,monospace;background:#e8e7dd;padding:2px 6px;font-size:13px;border-radius:2px;",
        "pre_css": "background:#e8e7dd;padding:16px;border-radius:4px;overflow-x:auto;font-size:13px;line-height:1.5;border:1px solid #d4d1c5;",
        "table_css": "width:100%;border-collapse:collapse;margin:16px 0;font-size:14px;",
        "th_css": "background:#efeee5;padding:10px 12px;text-align:left;border-bottom:2px solid #d4d1c5;color:#1B365D;font-weight:500;",
        "td_css": "padding:10px 12px;border-bottom:1px solid #d4d1c5;color:#3a382f;",
        "hr_css": "border:none;border-top:1px solid #d4d1c5;margin:32px 0;",
        "ul_css": "padding-left:24px;color:#3a382f;",
        "li_css": "margin:6px 0;",
        "a_css": "color:#1B365D;text-decoration:underline;text-underline-offset:2px;",
        "strong_css": "color:#1f1d18;font-weight:600;",
    },
    "data-report": {
        "name": "数据报告",
        "body_css": "background:#0f1117;color:#e2e8f0;font-family:'Inter','Noto Sans SC',system-ui,sans-serif;max-width:1100px;margin:0 auto;padding:40px 48px;line-height:1.6;",
        "h1_css": "font-size:36px;font-weight:700;margin:32px 0 16px;color:#f8fafc;letter-spacing:-0.02em;border:none;",
        "h2_css": "font-size:22px;font-weight:600;margin:28px 0 12px;color:#60a5fa;border-bottom:1px solid #1e293b;padding-bottom:8px;",
        "h3_css": "font-size:17px;font-weight:600;margin:20px 0 8px;color:#e2e8f0;",
        "p_css": "margin:12px 0;line-height:1.7;color:#94a3b8;",
        "blockquote_css": "border-left:3px solid #3b82f6;padding-left:20px;margin:24px 0;color:#e2e8f0;background:#1a1d2e;padding:16px 20px;border-radius:8px;",
        "code_css": "font-family:'JetBrains Mono',monospace;background:#1e293b;padding:2px 6px;font-size:13px;border-radius:4px;color:#a5b4fc;",
        "pre_css": "background:#1a1d2e;padding:16px;border-radius:8px;overflow-x:auto;font-size:13px;border:1px solid #1e293b;",
        "table_css": "width:100%;border-collapse:collapse;margin:16px 0;font-size:14px;",
        "th_css": "background:#1a1d2e;padding:10px 12px;text-align:left;border-bottom:2px solid #3b82f6;color:#60a5fa;font-weight:500;",
        "td_css": "padding:10px 12px;border-bottom:1px solid #1e293b;color:#94a3b8;",
        "hr_css": "border:none;border-top:1px solid #1e293b;margin:32px 0;",
        "ul_css": "padding-left:24px;color:#94a3b8;",
        "li_css": "margin:6px 0;",
        "strong_css": "color:#f8fafc;font-weight:600;",
    },
    "article-magazine": {
        "name": "杂志文章",
        "body_css": "background:#ffffff;color:#1a1a1a;font-family:'Georgia','Noto Serif SC',serif;max-width:720px;margin:0 auto;padding:48px 24px;line-height:1.8;font-size:18px;",
        "h1_css": "font-size:42px;font-weight:700;margin:40px 0 8px;color:#1a1a1a;line-height:1.15;letter-spacing:-0.02em;border:none;",
        "h2_css": "font-size:28px;font-weight:600;margin:36px 0 12px;color:#1a1a1a;border-bottom:none;",
        "h3_css": "font-size:22px;font-weight:500;margin:24px 0 8px;color:#333;",
        "p_css": "margin:16px 0;line-height:1.8;color:#333;text-indent:0;",
        "blockquote_css": "border-left:4px solid #d4d4d4;padding:12px 24px;margin:24px 0;color:#666;font-style:italic;font-size:19px;background:#fafafa;",
        "code_css": "font-family:'SF Mono','Menlo',monospace;background:#f4f4f4;padding:2px 6px;font-size:15px;border-radius:3px;",
        "pre_css": "background:#f8f8f8;padding:20px;border-radius:4px;overflow-x:auto;font-size:14px;border:1px solid #eee;",
        "table_css": "width:100%;border-collapse:collapse;margin:24px 0;font-size:15px;",
        "th_css": "background:#fafafa;padding:12px;text-align:left;border-bottom:2px solid #333;font-weight:600;",
        "td_css": "padding:12px;border-bottom:1px solid #eee;",
        "hr_css": "border:none;border-top:1px solid #e0e0e0;margin:40px 0;",
        "ul_css": "padding-left:28px;color:#333;",
        "strong_css": "font-weight:600;color:#1a1a1a;",
    },
    "card-xiaohongshu": {
        "name": "小红书卡片",
        "body_css": "background:linear-gradient(135deg,#fef9f0,#fef3e6);color:#3a2a1a;font-family:'PingFang SC','Noto Sans SC','Helvetica Neue',sans-serif;max-width:720px;margin:0 auto;padding:48px 36px;border-radius:24px;line-height:1.6;font-size:16px;box-shadow:0 4px 24px rgba(0,0,0,0.06);",
        "h1_css": "font-size:28px;font-weight:700;margin:24px 0 8px;color:#2a1a0a;line-height:1.3;border:none;",
        "h2_css": "font-size:20px;font-weight:600;margin:20px 0 8px;color:#5a3a1a;border-bottom:none;padding:0 0 8px;",
        "h3_css": "font-size:17px;font-weight:600;margin:16px 0 6px;color:#4a3a2a;",
        "p_css": "margin:10px 0;line-height:1.7;color:#5a4a3a;",
        "blockquote_css": "border-left:3px solid #e8a87c;padding:12px 16px;margin:16px 0;color:#5a4a3a;background:rgba(232,168,124,0.08);border-radius:8px;",
        "code_css": "font-family:'SF Mono',monospace;background:rgba(0,0,0,0.05);padding:2px 6px;font-size:14px;border-radius:4px;",
        "strong_css": "font-weight:700;color:#2a1a0a;",
        "hr_css": "border:none;height:1px;background:linear-gradient(90deg,transparent,#e8d5c0,transparent);margin:24px 0;",
        "ul_css": "padding-left:24px;color:#5a4a3a;",
        "li_css": "margin:6px 0;",
        "a_css": "color:#e07c4f;text-decoration:none;font-weight:500;",
        "th_css": "",
        "td_css": "",
        "pre_css": "",
        "table_css": "",
    }
}

def render_markdown_to_html(md_text: str, template_id: str = "doc-kami-parchment") -> str:
    """将 Markdown 渲染为设计风格的 HTML"""
    style = STYLES.get(template_id, STYLES["doc-kami-parchment"])

    lines = md_text.split("\n")
    html_parts = []
    in_code_block = False
    code_buffer = []
    in_table = False
    table_buffer = []

    def emit(text):
        html_parts.append(text)

    for line in lines:
        # 代码块
        if line.startswith("```"):
            if in_code_block:
                emit(f'<pre><code>{"".join(code_buffer)}</code></pre>\n')
                code_buffer = []
                in_code_block = False
            else:
                in_code_block = True
            continue
        if in_code_block:
            code_buffer.append(line + "\n")
            continue

        # 空行
        if not line.strip():
            emit("\n")
            continue

        # 表格
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not in_table:
                in_table = True
                table_buffer = [cells]
            else:
                table_buffer.append(cells)
            # 分隔行
            if re.match(r'^[\s\|:\-]+$', line):
                continue
            continue
        else:
            if in_table and table_buffer:
                emit("<table>\n")
                for idx, row in enumerate(table_buffer):
                    tag = "th" if idx == 0 else "td"
                    t_style = style["th_css"] if idx == 0 else style["td_css"]
                    emit(f"  <tr>\n")
                    for cell in row:
                        emit(f'    <{tag} style="{t_style}">{cell}</{tag}>\n')
                    emit(f"  </tr>\n")
                emit("</table>\n")
                table_buffer = []
                in_table = False
            if line.startswith("|---"):
                continue

        # 标题
        if line.startswith("###### "):
            emit(f'<h6 style="{style.get("h3_css","")}">{line[7:]}</h6>\n')
        elif line.startswith("##### "):
            emit(f'<h5 style="{style.get("h3_css","")}">{line[6:]}</h5>\n')
        elif line.startswith("#### "):
            emit(f'<h4 style="{style.get("h3_css","")}">{line[5:]}</h4>\n')
        elif line.startswith("### "):
            emit(f'<h3 style="{style["h3_css"]}">{line[4:]}</h3>\n')
        elif line.startswith("## "):
            emit(f'<h2 style="{style["h2_css"]}">{line[3:]}</h2>\n')
        elif line.startswith("# "):
            emit(f'<h1 style="{style["h1_css"]}">{line[2:]}</h1>\n')

        # 引用
        elif line.startswith("> ") or line.startswith(">"):
            text = line.lstrip("> ").strip()
            if text:
                emit(f'<blockquote style="{style["blockquote_css"]}"><p>{text}</p></blockquote>\n')

        # 水平线
        elif line.strip() in ("---", "***", "___"):
            emit(f'<hr style="{style["hr_css"]}" />\n')

        # 列表
        elif re.match(r'^[\-\*]\s', line):
            text = re.sub(r'^[\-\*]\s', '', line)
            # inline formatting
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong style="' + style["strong_css"] + r'">\1</strong>', text)
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            text = re.sub(r'`(.+?)`', r'<code style="' + style["code_css"] + r'">\1</code>', text)
            emit(f'<li style="{style["li_css"]}">{text}</li>\n')

        # 数字列表
        elif re.match(r'^\d+[\.\)]\s', line):
            text = re.sub(r'^\d+[\.\)]\s', '', line)
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong style="' + style["strong_css"] + r'">\1</strong>', text)
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            text = re.sub(r'`(.+?)`', r'<code style="' + style["code_css"] + r'">\1</code>', text)
            emit(f'<li style="{style["li_css"]}">{text}</li>\n')

        # 普通段落
        else:
            text = line
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong style="' + style["strong_css"] + r'">\1</strong>', text)
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            text = re.sub(r'`(.+?)`', r'<code style="' + style["code_css"] + r'">\1</code>', text)
            text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a style="' + style.get("a_css","") + r'" href="\2">\1</a>', text)
            emit(f'<p style="{style["p_css"]}">{text}</p>\n')

    # 处理末尾未关闭的代码块/表格
    if in_code_block and code_buffer:
        emit(f'<pre><code>{"".join(code_buffer)}</code></pre>\n')
    if in_table and table_buffer:
        emit("<table>\n")
        for idx, row in enumerate(table_buffer):
            tag = "th" if idx == 0 else "td"
            t_style = style["th_css"] if idx == 0 else style["td_css"]
            emit(f"  <tr>\n")
            for cell in row:
                emit(f'    <{tag} style="{t_style}">{cell}</{tag}>\n')
            emit(f"  </tr>\n")
        emit("</table>\n")

    content_html = "".join(html_parts)

    # 包裹列表
    content_html = re.sub(r'(<li[^>]*>.*?</li>\n)+', r'<ul style="' + style["ul_css"] + r'">\n\g<0></ul>\n', content_html, flags=re.DOTALL)

    fonts = ""
    if template_id == "doc-kami-parchment":
        fonts = '<link href="https://fonts.googleapis.com/css2?family=Source+Serif+Pro:ital,wght@0,400;0,500;0,600;1,400&family=Noto+Serif+SC:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet" />'
    elif template_id in ("data-report",):
        fonts = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />'
    elif template_id in ("article-magazine",):
        fonts = '<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap" rel="stylesheet" />'

    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{style["name"]} · Taiyi Report</title>
{fonts}
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ {style["body_css"]} }}
  @media (max-width: 640px) {{ body {{ padding:24px 16px; }} }}
</style>
</head>
<body>
{content_html}
</body>
</html>"""

    return full_html


if __name__ == "__main__":
    template_id = sys.argv[1] if len(sys.argv) > 1 else "doc-kami-parchment"
    input_path = sys.argv[2] if len(sys.argv) > 2 else "-"
    output_path = sys.argv[3] if len(sys.argv) > 3 else "-"

    if template_id not in STYLES:
        print(f"❌ 未知模板: {template_id}", file=sys.stderr)
        print(f"   可用: {', '.join(STYLES.keys())}", file=sys.stderr)
        sys.exit(1)

    if input_path == "-":
        md_text = sys.stdin.read()
    else:
        with open(input_path, "r") as f:
            md_text = f.read()

    html = render_markdown_to_html(md_text, template_id)

    if output_path == "-":
        print(html)
    else:
        with open(output_path, "w") as f:
            f.write(html)
        print(f"✅ {template_id} → {output_path}", file=sys.stderr)

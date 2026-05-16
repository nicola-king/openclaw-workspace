#!/usr/bin/env python3
"""
html-anything Agent 驱动渲染（Phase 2）
使用本地 coding agent 将 Markdown 渲染为设计级 HTML。

用法:
  python3 html-agent.py <template-id> [input.md] [output.html]
  python3 html-agent.py <agent> <template-id> [input.md] [output.html]

默认 agent: openclaw
默认模板: doc-kami-parchment
默认输入: stdin
默认输出: stdout
"""

import sys
import json
import urllib.request

AGENT = "openclaw"
TEMPLATE_ID = "doc-kami-parchment"
PORT = 3777
BASE = f"http://localhost:{PORT}"

TEMPLATES_INFO = {
    "article-magazine": "杂志文章排版",
    "blog-post": "博客长文",
    "card-twitter": "Twitter 分享卡",
    "card-xiaohongshu": "小红书图文卡片",
    "data-report": "数据可视化报告",
    "doc-kami-parchment": "Kami 羊皮纸文档",
    "docs-page": "技术文档页",
    "eng-runbook": "工程 Runbook",
    "finance-report": "季度财报",
    "deck-swiss-international": "瑞士国际主义 Deck",
    "deck-guizang-editorial": "贵赞编辑墨水 Deck",
    "deck-pitch": "投资人 Pitch Deck",
    "deck-tech-sharing": "技术分享 Deck",
    "magazine-poster": "杂志海报",
    "saas-landing": "SaaS 落地页",
    "pricing-page": "定价页",
    "waitlist-page": "Waitlist 页",
}

def parse_args():
    args = sys.argv[1:]
    agent = AGENT
    template = TEMPLATE_ID
    input_path = None
    output_path = None

    # 如果第一个参数是已知模板 ID
    if args and args[0] in TEMPLATES_INFO:
        template = args.pop(0)
    elif args and args[0] in ("openclaw", "codex", "claude", "qwen", "gemini", "copilot"):
        agent = args.pop(0)
        if args and args[0] in TEMPLATES_INFO:
            template = args.pop(0)

    if args and args[0] != "-":
        input_path = args.pop(0)
    if args and args[0] != "-":
        output_path = args.pop(0)

    return agent, template, input_path, output_path


def read_content(input_path):
    if input_path:
        with open(input_path, "r") as f:
            return f.read()
    return sys.stdin.read()


def call_convert(agent, template_id, content):
    """调用 convert API 并解析 SSE 流"""
    body = {
        "agent": agent,
        "templateId": template_id,
        "content": content,
        "format": "markdown",
    }

    req = urllib.request.Request(
        f"{BASE}/api/convert",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    html_parts = []
    with urllib.request.urlopen(req, timeout=300) as resp:
        for line_bytes in resp:
            line = line_bytes.decode("utf-8").strip()
            # Read next line which should be data
            if line.startswith("event: delta"):
                data_line = next(resp).decode("utf-8").strip()
                if data_line.startswith("data: "):
                    try:
                        d = json.loads(data_line[6:])
                        if d.get("type") == "delta":
                            html_parts.append(d.get("text", ""))
                    except json.JSONDecodeError:
                        pass
            elif line.startswith('data: {"type":"done"'):
                break

    return "".join(html_parts)


def main():
    agent, template_id, input_path, output_path = parse_args()

    if template_id not in TEMPLATES_INFO:
        print(f"⚠️  未知模板: {template_id}", file=sys.stderr)
        print(f"   可用: {', '.join(TEMPLATES_INFO.keys())}", file=sys.stderr)
        print(f"   使用默认: {TEMPLATE_ID}", file=sys.stderr)
        template_id = TEMPLATE_ID

    content = read_content(input_path)
    if not content.strip():
        print("❌ 输入内容为空", file=sys.stderr)
        sys.exit(1)

    print(f"🎨 Agent: {agent} | 模板: {template_id} ({TEMPLATES_INFO.get(template_id, '?')})", file=sys.stderr)
    print(f"📄 输入: {input_path or 'stdin'} ({len(content)} chars)", file=sys.stderr)
    print(f"⏳ 正在生成...", file=sys.stderr)

    try:
        html = call_convert(agent, template_id, content)
    except Exception as e:
        print(f"❌ 请求失败: {e}", file=sys.stderr)
        sys.exit(1)

    if not html.strip():
        print("❌ 生成失败，无输出", file=sys.stderr)
        sys.exit(1)

    if not html.strip().startswith("<!DOCTYPE html>") and not html.strip().startswith("<html"):
        print(f"⚠️  输出不是标准 HTML (前60字符: {html[:60]})", file=sys.stderr)

    if output_path:
        with open(output_path, "w") as f:
            f.write(html)
        print(f"✅ → {output_path} ({len(html)} bytes)", file=sys.stderr)
    else:
        print(html)


if __name__ == "__main__":
    main()

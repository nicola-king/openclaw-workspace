#!/usr/bin/env python3
"""
太一跨境贸易 · 飞书 Bot 消息处理器
读取 stdin NDJSON 事件流 → 调用买家情报 API → 回复飞书

依赖: lark-cli (IM 回复), curl (买家情报 API)

运行方式（配合 event consume）:
  lark-cli event consume im.message.receive_v1 --as bot | python3 lark-bot-handler.py
"""
import sys
import json
import subprocess
import urllib.request
import urllib.parse
import re
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [handler] %(levelname)s %(message)s",
    stream=sys.stderr,
)

BUYER_API = "http://localhost:8100"
QUERY_ENDPOINT = BUYER_API + "/api/v1/query"
DAILY_ENDPOINT = BUYER_API + "/api/v1/daily"
HEALTH_ENDPOINT = BUYER_API + "/health"

# 国家/品类识别列表
COUNTRIES = [
    "沙特", "阿联酋", "伊拉克", "卡塔尔", "澳大利亚", "新西兰",
    "阿曼", "巴林", "科威特", "土耳其", "埃及", "印度",
]
SECTORS = [
    "钢结构", "变压器", "模块化房屋", "集成房屋", "折叠房屋",
    "光伏", "储能", "摩配", "建材", "建筑",
]


def call_buyer_api(mode, q="", country="", sector="", days=7, tier="pro"):
    """调用买家情报 API"""
    params = {
        "mode": mode,
        "q": q,
        "country": country,
        "sector": sector,
        "days": str(days),
        "tier": tier,
    }
    params = {k: v for k, v in params.items() if v}

    url = QUERY_ENDPOINT + "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.urlopen(url, timeout=15)
        return json.loads(req.read().decode())
    except Exception as e:
        return {"error": str(e), "suggestion": "数据源暂时不可用，稍后再试"}


def process_text_message(text, chat_id):
    """处理文本消息，返回回复内容"""
    text = text.strip()

    # 健康检查
    if text in ("/health", "/状态", "ping"):
        try:
            req = urllib.request.urlopen(HEALTH_ENDPOINT, timeout=5)
            data = json.loads(req.read().decode())
            parts = [
                "✅ 太一跨境贸易 Bot 运行中",
                "模块: " + data.get("module", "?"),
                "版本: " + data.get("version", "?"),
            ]
            return "\n".join(parts)
        except Exception as e:
            return "❌ 健康检查失败: " + str(e)

    # 日报
    if text.startswith("/日报") or text.startswith("/daily"):
        parts = text.split()
        country = parts[1] if len(parts) > 1 else ""
        try:
            req = urllib.request.urlopen(
                DAILY_ENDPOINT + "?country=" + urllib.parse.quote(country), timeout=15
            )
            data = json.loads(req.read().decode())
        except Exception as e:
            return "❌ 获取日报失败: " + str(e)

        return format_result(data)

    # 搜索买家（默认）
    q = text
    country = ""
    sector = ""

    search_match = re.match(r"/(?:搜索|search|find)\s+(.+)", text)
    if search_match:
        q = search_match.group(1)

    # 识别国家
    for c in COUNTRIES:
        if c in q:
            country = c
            q = q.replace(c, "").strip()
            break

    # 识别品类
    for s in SECTORS:
        if s in q:
            sector = s
            if q == s or not q:
                q = ""
            break

    result = call_buyer_api("selected", q=q, country=country, sector=sector)
    return format_result(data)


def format_result(data):
    """格式化 API 结果为可读文本"""
    if "error" in data:
        return "❌ " + data["error"] + "\n💡 " + data.get("suggestion", "稍后再试")

    items = data.get("items", [])
    if not items:
        return "📭 暂无匹配结果\n试试放宽条件：/搜索 [国家] [品类]"

    meta = data.get("_meta", {})
    lines = []

    # 标题行
    mode_label = meta.get("mode", "精选")
    lines.append("**买家情报 · " + mode_label + "**")

    # 元信息行
    time_window = meta.get("time_window", "最近 7 天")
    meta_filter = meta.get("filter", "")
    count_str = "共 " + str(meta.get("count", len(items))) + " 条"
    meta_parts = [p for p in [meta_filter, count_str] if p]
    if meta_parts:
        lines.append("⏱ " + time_window + " | " + " | ".join(meta_parts))
    else:
        lines.append("⏱ " + time_window)
    lines.append("")

    for i, item in enumerate(items[:10], 1):
        name = item.get("project_name") or item.get("title", "项目")
        country = item.get("country", "")
        sector = item.get("sector", "")
        brief = item.get("project_brief") or item.get("summary", "")
        url = item.get("url", "")
        source = item.get("source", "")
        updated = item.get("last_updated") or item.get("date", "")

        item_line = str(i) + ". **" + name + "**"
        if country or sector:
            item_line += " — " + " ".join(filter(None, [country, sector]))
        lines.append(item_line)

        if brief:
            lines.append("   " + brief[:200])
        if url:
            lines.append("   🔗 " + url)
        if source:
            lines.append("   来源: " + source)
        if updated:
            lines.append("   📅 " + updated)
        lines.append("")

    if len(items) > 10:
        lines.append("... 还有 " + str(len(items) - 10) + " 条")

    lines.append("---")
    lines.append("共 " + str(len(items)) + " 条 | 数据：买家情报引擎")
    lines.append("💡 试试：/搜索 澳大利亚 钢结构")
    return "\n".join(lines)


def reply_in_chat(chat_id, message_id, content):
    """通过 lark-cli 回复消息"""
    cmd = [
        "lark-cli", "--as", "bot", "im", "+messages-reply",
        message_id,
        "--markdown", content,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            logging.error("回复失败: %s", result.stderr)
        else:
            logging.info("已回复 %s", message_id)
    except Exception as e:
        logging.error("回复异常: %s", e)


def main():
    logging.info("太一跨境贸易 Bot 处理器启动")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        message_type = event.get("message_type", "")
        chat_id = event.get("chat_id", "")
        message_id = event.get("message_id", "")
        sender_id = event.get("sender_id", "")
        content = event.get("content", "")

        if message_type != "text" or not content:
            continue

        logging.info("收到消息: chat=%s, sender=%s, text=%s", chat_id, sender_id, content[:100])

        reply = process_text_message(content, chat_id)
        if reply:
            reply_in_chat(chat_id, message_id, reply)


if __name__ == "__main__":
    main()

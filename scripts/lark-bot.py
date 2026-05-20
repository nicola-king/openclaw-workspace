#!/usr/bin/env python3
"""
太一跨境贸易 · 飞书 Bot (原生 Python)
直接使用 Feishu OpenAPI，绕过 lark-cli keychain 依赖
"""
import sys
import json
import requests
import websocket
import threading
import time
import logging
import os
import hmac
import hashlib
import base64
import struct
import re

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [bot] %(levelname)s %(message)s",
    stream=sys.stderr,
)

APP_ID = "cli_aa87b4b1f4795cd6"
APP_SECRET = "OlOgWyJlhGw8Zqyt4rp26cxzrNvBoXmn"
BASE_URL = "https://open.feishu.cn/open-apis"
BUYER_API = "http://localhost:8100"

# Token cache
_token = {"access_token": None, "expires_at": 0}


def get_tenant_token():
    """获取 tenant_access_token"""
    if time.time() < _token["expires_at"] - 60:
        return _token["access_token"]

    url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={
        "app_id": APP_ID,
        "app_secret": APP_SECRET,
    }, timeout=10)
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"获取 token 失败: {data}")

    _token["access_token"] = data["tenant_access_token"]
    _token["expires_at"] = time.time() + data.get("expire", 7200)
    logging.info("Token 刷新成功")
    return _token["access_token"]


def api_post(path, data=None):
    """调用飞书 API (POST)"""
    token = get_tenant_token()
    url = f"{BASE_URL}{path}"
    resp = requests.post(url, json=data or {}, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }, timeout=15)
    result = resp.json()
    if result.get("code") != 0:
        logging.error(f"API 错误 {path}: {result}")
    return result


def api_get(path, params=None):
    """调用飞书 API (GET)"""
    token = get_tenant_token()
    url = f"{BASE_URL}{path}"
    resp = requests.get(url, params=params or {}, headers={
        "Authorization": f"Bearer {token}",
    }, timeout=15)
    result = resp.json()
    if result.get("code") != 0:
        logging.error(f"API 错误 {path}: {result}")
    return result


def send_message(chat_id, message_id, content):
    """回复消息"""
    data = {
        "receive_id": chat_id,
        "msg_type": "markdown",
        "content": json.dumps({"text": content}, ensure_ascii=False),
    }
    # 回复到指定消息
    result = requests.post(
        f"{BASE_URL}/im/v1/messages/{message_id}/reply",
        json={"content": json.dumps({"text": content}, ensure_ascii=False), "msg_type": "markdown"},
        headers= {
            "Authorization": f"Bearer {get_tenant_token()}",
            "Content-Type": "application/json; charset=utf-8",
        },
        timeout=10,
    ).json()
    if result.get("code") != 0:
        logging.error(f"回复消息失败: {result}")
    else:
        logging.info(f"已回复 {message_id} in {chat_id}")


def call_buyer_api(q="", country="", sector="", days=7):
    """调用买家情报 API"""
    params = {"mode": "selected", "days": str(days)}
    if q:
        params["q"] = q
    if country:
        params["country"] = country
    if sector:
        params["sector"] = sector

    url = f"{BUYER_API}/api/v1/query"
    try:
        resp = requests.get(url, params=params, timeout=15)
        return resp.json()
    except Exception as e:
        return {"error": str(e), "suggestion": "数据源暂时不可用"}


def format_result(data):
    """格式化结果为可读文本"""
    if "error" in data:
        return f"❌ {data['error']}\n💡 {data.get('suggestion', '稍后再试')}"

    items = data.get("items", [])
    if not items:
        return "📭 暂无匹配结果\n试试：搜索 [国家] [品类]"

    meta = data.get("_meta", {})
    lines = [f"**买家情报 · {meta.get('mode', '精选')}**"]
    time_w = meta.get("time_window", "最近 7 天")
    meta_f = meta.get("filter", "")
    cnt = f"共 {meta.get('count', len(items))} 条"
    parts = [p for p in [meta_f, cnt] if p]
    lines.append(f"⏱ {time_w} | {' | '.join(parts)}" if parts else f"⏱ {time_w}")
    lines.append("")

    for i, item in enumerate(items[:10], 1):
        name = item.get("project_name") or item.get("title", "项目")
        c = item.get("country", "")
        s = item.get("sector", "")
        brief = item.get("project_brief") or item.get("summary", "")
        url = item.get("url", "")
        src = item.get("source", "")
        upd = item.get("last_updated") or item.get("date", "")

        loc = " ".join(filter(None, [c, s]))
        lines.append(f"{i}. **{name}**{' — ' + loc if loc else ''}")
        if brief:
            lines.append(f"   {brief[:200]}")
        if url:
            lines.append(f"   🔗 {url}")
        if src:
            lines.append(f"   来源: {src}")
        if upd:
            lines.append(f"   📅 {upd}")
        lines.append("")

    if len(items) > 10:
        lines.append(f"... 还有 {len(items) - 10} 条")
    lines.append("---")
    lines.append(f"共 {len(items)} 条 | 数据：买家情报引擎")
    lines.append("💡 试试：/搜索 澳大利亚 钢结构")
    return "\n".join(lines)


def process_message(event):
    """处理收到的消息事件"""
    try:
        # 解析事件数据
        if "event" in event:
            ev = event["event"]
        else:
            ev = event

        message = ev.get("message", {})
        msg_type = message.get("message_type", "")
        chat_id = message.get("chat_id", "")
        msg_id = message.get("message_id", "")
        content_raw = message.get("content", "")
        sender = ev.get("sender", {}).get("sender_id", {})

        if msg_type != "text":
            return

        # 解析文本内容
        try:
            content_obj = json.loads(content_raw)
            text = content_obj.get("text", "")
        except (json.JSONDecodeError, TypeError):
            text = str(content_raw)

        if not text:
            return

        text = text.strip()
        logging.info(f"消息: chat={chat_id}, text={text[:80]}")

        # 处理
        reply_text = query_buyer_intel(text)
        if reply_text:
            send_message(chat_id, msg_id, reply_text)
    except Exception as e:
        logging.error(f"处理消息异常: {e}", exc_info=True)


COUNTRIES = ["沙特", "阿联酋", "伊拉克", "卡塔尔", "澳大利亚", "新西兰",
             "阿曼", "巴林", "科威特", "土耳其", "埃及", "印度"]
SECTORS = ["钢结构", "变压器", "模块化房屋", "集成房屋", "折叠房屋",
           "光伏", "储能", "摩配", "建材", "建筑"]


def query_buyer_intel(text):
    """根据用户输入查询买家情报"""
    # 健康检查
    if text in ("/health", "/状态", "ping"):
        try:
            resp = requests.get(f"{BUYER_API}/health", timeout=5)
            data = resp.json()
            return "\n".join([
                "✅ 太一跨境贸易 Bot 运行中",
                f"模块: {data.get('module', '?')}",
                f"版本: {data.get('version', '?')}",
            ])
        except Exception as e:
            return f"❌ 健康检查失败: {e}"

    # 搜索解析
    q = text
    country = ""
    sector = ""

    search_match = re.match(r"/(?:搜索|search|find)\s+(.+)", text)
    if search_match:
        q = search_match.group(1)

    for c in COUNTRIES:
        if c in q:
            country = c
            q = q.replace(c, "").strip()
            break

    for s in SECTORS:
        if s in q:
            sector = s
            if q == s or not q:
                q = ""
            break

    data = call_buyer_api(q=q, country=country, sector=sector)
    return format_result(data)


def start_websocket():
    """连接飞书 WebSocket 事件系统"""
    while True:
        try:
            token = get_tenant_token()
            # 获取 WebSocket URL
            resp = requests.post(
                f"{BASE_URL}/event/v1/ws/connect",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10,
            )
            data = resp.json()
            if data.get("code") != 0:
                logging.error(f"获取 WebSocket URL 失败: {data}")
                time.sleep(30)
                continue

            ws_url = data["data"]["url"]
            logging.info(f"WebSocket URL: {ws_url[:60]}...")

            # 连接 WebSocket
            ws = websocket.WebSocketApp(
                ws_url,
                on_message=on_ws_message,
                on_error=on_ws_error,
                on_close=on_ws_close,
                on_open=on_ws_open,
            )
            ws.run_forever(ping_interval=30, ping_timeout=10)
        except Exception as e:
            logging.error(f"WebSocket 连接异常: {e}")
            time.sleep(30)


def on_ws_open(ws):
    logging.info("WebSocket 已连接 ✅")


def on_ws_close(ws, close_status_code, close_msg):
    logging.info(f"WebSocket 关闭: {close_status_code} {close_msg}")


def on_ws_error(ws, error):
    logging.error(f"WebSocket 错误: {error}")


def on_ws_message(ws, message):
    """处理 WebSocket 消息"""
    try:
        data = json.loads(message)

        # Feishu 事件格式
        if "type" in data:
            if data["type"] == "url_challenge":
                # Challenge 响应
                challenge = data.get("challenge", "")
                ws.send(json.dumps({"challenge": challenge}))
                logging.info("Challenge 响应")
                return

        # 事件处理
        process_message(data)
    except Exception as e:
        logging.error(f"消息处理异常: {e}")


def main():
    logging.info("=" * 50)
    logging.info("太一跨境贸易 Bot (Python) 启动")
    logging.info(f"App ID: {APP_ID}")
    logging.info(f"买家情报 API: {BUYER_API}")
    logging.info("=" * 50)

    start_websocket()


if __name__ == "__main__":
    main()

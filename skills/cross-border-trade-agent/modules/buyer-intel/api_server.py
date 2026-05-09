#!/usr/bin/env python3
"""
买家情报 REST API — 三轨接入 (REST API / RSS / SKILL.md)

借鉴 AI HOT: 匿名开放(限流) + 分层路由 + 人话输出

运行: python3 api_server.py [--port 8080]
"""
import json, os, logging, http.server, urllib.parse, time
from datetime import datetime, timedelta

syspath = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, syspath)
from core import BuyerIntel

HOST = "0.0.0.0"
PORT = 8100
RATE_LIMIT = 60  # req/min/IP
_ratelimit_store = {}

class BuyerIntelAPI(http.server.BaseHTTPRequestHandler):
    """REST API — 三路由 + 正交查询"""

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        params = urllib.parse.parse_qs(parsed.query)

        # --- Rate limit — 必须先于任何 send_header/send_response ---
        client = self.client_address[0]
        if not self._check_rate(client):
            self._send_json(429, {"error": "请求太频繁，等 1 分钟后再试", "suggestion": "限制 60 次/分钟，试试减少请求频率"})
            return

        # --- 路由 ---
        if path == "/health":
            self._send_json(200, {"status": "ok", "module": "buyer-intel-api", "version": "1.0"})
        elif path == "/api/v1/query":
            self._handle_query(params)
        elif path == "/api/v1/daily":
            self._handle_daily(params)
        elif path == "/api/v1/rss":
            self._handle_rss(params)
        else:
            self._send_json(404, {"error": "未知端点", "available": ["/health", "/api/v1/query", "/api/v1/daily", "/api/v1/rss"]})

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    # ════════════════════════════════════════
    # 三层路由 + 正交查询
    # ════════════════════════════════════════

    def _handle_query(self, params):
        """GET /api/v1/query?mode=selected&q=沙特&sector=钢结构&country=沙特&days=7&tier=pro"""
        mode = (params.get("mode") or ["selected"])[0]
        q = (params.get("q") or [""])[0]
        sector = (params.get("sector") or [None])[0]
        country = (params.get("country") or [None])[0]
        days_str = (params.get("days") or ["7"])[0]
        tier = (params.get("tier") or ["pro"])[0]

        # 自然语言时间窗
        days = self._parse_days(days_str)

        bi = BuyerIntel()
        result = bi.query(
            mode=mode,
            q=q,
            country=country,
            sector=sector,
            days=days,
            tier=tier
        )

        # 人话元信息
        result["_meta"] = {
            "time_window": f"最近 {days} 天" if days != 999 else "全部",
            "filter": " | ".join(filter(None, [f"关键词: {q}" if q else "", f"国家: {country}" if country else "", f"品类: {sector}" if sector else "", f"模式: {mode}"])),
            "source": "买家情报引擎·三层路由",
            "count": result.get("count", len(result.get("items", []))),
        }
        self._send_json(200, result)

    def _handle_daily(self, params):
        """GET /api/v1/daily?country=沙特&sector=钢结构&tier=pro"""
        country = (params.get("country") or [None])[0]
        sector = (params.get("sector") or [None])[0]
        tier = (params.get("tier") or ["pro"])[0]

        bi = BuyerIntel()
        result = bi.query("daily", country=country, sector=sector, tier=tier)

        result["_meta"] = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "source": "买家情报日报",
        }
        self._send_json(200, result)

    def _handle_rss(self, params):
        """GET /api/v1/rss — RSS 2.0 feed"""
        mode = (params.get("mode") or ["selected"])[0]
        q = (params.get("q") or [""])[0]
        country = (params.get("country") or [None])[0]

        bi = BuyerIntel()
        items = bi.query(mode=mode, q=q, country=country).get("items", [])

        rss = self._build_rss(items)
        self.send_response(200)
        self._cors_headers()
        self.send_header("Content-Type", "application/rss+xml; charset=utf-8")
        self.end_headers()
        self.wfile.write(rss.encode("utf-8"))

    # ════════════════════════════════════════
    # 工具
    # ════════════════════════════════════════

    def _parse_days(self, raw):
        """自然语言时间→天数: '3d'/'7d'/'30d'/'1m'/'all'/'全部'"""
        raw = str(raw).lower().strip()
        if raw in ("all", "全部", "999", "-1"):
            return 999
        m = {"1d": 1, "3d": 3, "7d": 7, "14d": 14, "30d": 30, "1m": 30, "3m": 90}
        if raw in m:
            return m[raw]
        try:
            return max(1, min(365, int(raw)))
        except:
            return 7

    def _build_rss(self, items):
        """生成 RSS 2.0 XML"""
        now = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0800")
        title = "太一买家情报"
        link = "https://taiyi.trade/buyer-intel/rss"
        desc = "太一跨境贸易 — 买家情报精选"

        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>{title}</title>
<link>{link}</link>
<description>{desc}</description>
<language>zh-cn</language>
<pubDate>{now}</pubDate>
<atom:link href="{link}" rel="self" type="application/rss+xml"/>
"""
        for item in items[:20]:
            title_text = item.get("project_name") or item.get("title", "项目线索")
            desc_text = item.get("project_brief") or item.get("summary", "")
            item_link = item.get("url", link)
            guid = item.get("id", title_text)
            updated = item.get("last_updated") or item.get("date", "")
            pub = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0800")
            if updated:
                try:
                    dt = datetime.strptime(updated[:10], "%Y-%m-%d")
                    pub = dt.strftime("%a, %d %b %Y %H:%M:%S +0800")
                except:
                    pass
            xml += f"""<item>
<title>{self._xml_escape(title_text)}</title>
<description>{self._xml_escape(desc_text)}</description>
<link>{item_link}</link>
<guid isPermaLink="false">{guid}</guid>
<pubDate>{pub}</pubDate>
</item>
"""
        xml += "</channel>\n</rss>"
        return xml

    def _xml_escape(self, s):
        if not s: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def _check_rate(self, client):
        now = time.time()
        if client not in _ratelimit_store:
            _ratelimit_store[client] = []
        ts = _ratelimit_store[client]
        # 清理老记录
        cutoff = now - 60
        ts[:] = [t for t in ts if t > cutoff]
        if len(ts) >= RATE_LIMIT:
            return False
        ts.append(now)
        return True

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _send_json(self, code, data):
        self.send_response(code)
        self._cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(
            data, indent=2, ensure_ascii=False, default=str
        ).encode("utf-8"))

    def log_message(self, fmt, *args):
        logging.info(f"[{self.client_address[0]}] {fmt % args}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="买家情报 REST API")
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--host", default=HOST)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    server = http.server.HTTPServer((args.host, args.port), BuyerIntelAPI)
    logging.info(f"买家情报 API 启动 → http://{args.host}:{args.port}")
    logging.info("端点: /health, /api/v1/query, /api/v1/daily, /api/v1/rss")
    logging.info(f"限流: {RATE_LIMIT} req/min/IP")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()

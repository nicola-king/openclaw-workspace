#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一旅游探路者 v2.0 — 交通票务模块 transport.py

一体化管理机票、火车票、船票、巴士票：
  - 添加、查询、更新票务记录
  - 截图存储与 OCR 文本
  - 验证链接（verification_links）全程附带
  - SQLite 持久化
  - 行程整合集成

CLI 快速用法:
  # 添加票务
  python3 transport.py add --types flight --city 北京 \
    --route "重庆→北京" --provider "中国国航" \
    --departure "2026-05-10 08:00" --arrival "2026-05-10 10:30" \
    --price 1280 --confirmation CA1234
  # 同时添加机票+火车票
  python3 transport.py add --types flight train --city 北京 \
    --route "重庆→北京" --departure "2026-05-10 08:00" \
    --price 1280,540 --confirmation CA1234,G1234
  # 查询票务
  python3 transport.py list --city 北京
  python3 transport.py get --id 1
  # 添加截图
  python3 transport.py screenshot --id 1 --path screenshots/CA1234.png
  # 行程交通概览
  python3 transport.py itinerary --city 北京 --date 2026-05-10

作者：太一 AGI
创建：2026-05-04
"""

import json
import sys
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# ── 路径 ──────────────────────────────────────────────
WORKSPACE = Path("/home/sayelf/.openclaw/workspace")
SKILLS_DIR = WORKSPACE / "skills"
DOMESTIC_DIR = SKILLS_DIR / "domestic-travel-agent"
DATA_DIR = DOMESTIC_DIR / "data"
SCREENSHOTS_DIR = DOMESTIC_DIR / "screenshots"

DATA_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "travel.db"


# ── 验证链接模板 ───────────────────────────────────────
VERIFICATION_PROVIDERS = {
    "flight": {
        "中国国航": "https://www.airchina.com.cn",
        "中国东航": "https://www.ceair.com",
        "中国南航": "https://www.csair.com",
        "海南航空": "https://www.hnair.com",
        "深圳航空": "https://www.shenzhenair.com",
        "厦门航空": "https://www.xiamenair.com",
        "四川航空": "https://www.sichuanair.com",
        "春秋航空": "https://www.ch.com",
        "吉祥航空": "https://www.juneyaoair.com",
        "default": "https://www.flightaware.com",
    },
    "train": {
        "中国铁路": "https://www.12306.cn",
        "default": "https://www.12306.cn",
    },
    "ferry": {
        "default": "https://www.ctrip.com/ferry",
    },
    "bus": {
        "default": "https://www.ctrip.com/bus",
    },
}


def _get_verification_links(ticket_type: str, provider: str, route: str,
                            confirmation_no: str = "") -> List[Dict[str, str]]:
    """根据票务类型和提供商生成验证链接列表"""
    providers = VERIFICATION_PROVIDERS.get(ticket_type, {})
    base_url = providers.get(provider, providers.get("default", ""))

    links = []
    if base_url:
        links.append({
            "label": f"{provider} 官网" if provider != "default" else "票务查询",
            "url": base_url,
            "type": "official",
        })

    # 航班追踪
    if ticket_type == "flight" and confirmation_no:
        links.append({
            "label": "航班追踪",
            "url": f"https://www.flightaware.com/live/flight/{confirmation_no}",
            "type": "tracking",
        })
    # 车票查询
    elif ticket_type == "train":
        links.append({
            "label": "铁路12306 查询",
            "url": "https://www.12306.cn/index/",
            "type": "search",
        })
    # 通用 OTA 查询
    ota_urls = {
        "flight": ("携程机票查询", "https://flights.ctrip.com/"),
        "train": ("携程火车票查询", "https://trains.ctrip.com/"),
        "ferry": ("携程船票查询", "https://www.ctrip.com/ferry"),
        "bus": ("携程汽车票查询", "https://www.ctrip.com/bus"),
    }
    if ticket_type in ota_urls:
        label, url = ota_urls[ticket_type]
        links.append({
            "label": label,
            "url": url,
            "type": "ota",
        })

    return links


# ── SQLite 数据库层 ────────────────────────────────────

class TicketDatabase:
    """交通票务 SQLite 数据库"""

    def __init__(self, db_path: str = str(DB_PATH)):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_db(self):
        conn = self._get_conn()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT,
                    type TEXT NOT NULL,
                    provider TEXT,
                    route TEXT,
                    departure_time TEXT,
                    arrival_time TEXT,
                    price REAL,
                    confirmation_no TEXT,
                    screenshot_path TEXT,
                    ocr_text TEXT,
                    status TEXT DEFAULT 'booked',
                    verification_links TEXT DEFAULT '[]',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_tickets_city
                ON tickets(city)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_tickets_type
                ON tickets(type)
            """)
            conn.commit()
        finally:
            conn.close()

    def add_ticket(self, city: str, ticket_type: str, provider: str,
                   route: str, departure_time: str, arrival_time: str,
                   price: float, confirmation_no: str = "",
                   screenshot_path: str = "", ocr_text: str = "",
                   status: str = "booked") -> int:
        """添加票务记录，自动生成 verification_links"""
        links = _get_verification_links(ticket_type, provider, route, confirmation_no)
        links_json = json.dumps(links, ensure_ascii=False)

        conn = self._get_conn()
        try:
            cursor = conn.execute("""
                INSERT INTO tickets
                    (city, type, provider, route, departure_time, arrival_time,
                     price, confirmation_no, screenshot_path, ocr_text,
                     status, verification_links)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (city, ticket_type, provider, route, departure_time, arrival_time,
                  price, confirmation_no, screenshot_path, ocr_text,
                  status, links_json))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def list_tickets(self, city: str = "", ticket_type: str = "",
                     status: str = "", limit: int = 50) -> List[Dict]:
        """查询票务记录，按出发时间降序"""
        conn = self._get_conn()
        try:
            conditions = []
            params = []
            if city:
                conditions.append("city = ?")
                params.append(city)
            if ticket_type:
                conditions.append("type = ?")
                params.append(ticket_type)
            if status:
                conditions.append("status = ?")
                params.append(status)

            where = " AND ".join(conditions) if conditions else "1=1"
            rows = conn.execute(f"""
                SELECT * FROM tickets
                WHERE {where}
                ORDER BY departure_time DESC
                LIMIT ?
            """, params + [limit]).fetchall()

            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_ticket(self, ticket_id: int) -> Optional[Dict]:
        conn = self._get_conn()
        try:
            row = conn.execute(
                "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def update_ticket(self, ticket_id: int, **kwargs) -> bool:
        """更新票务字段（不更新 verification_links）"""
        allowed = {"provider", "route", "departure_time", "arrival_time",
                   "price", "confirmation_no", "screenshot_path", "ocr_text",
                   "status", "city"}
        updates = {k: v for k, v in kwargs.items() if k in allowed}
        if not updates:
            return False

        conn = self._get_conn()
        try:
            sets = ", ".join(f"{k} = ?" for k in updates)
            values = list(updates.values()) + [ticket_id]
            conn.execute(f"UPDATE tickets SET {sets} WHERE id = ?", values)
            conn.commit()
            return conn.total_changes > 0
        finally:
            conn.close()

    def add_screenshot(self, ticket_id: int, screenshot_path: str,
                       ocr_text: str = "") -> bool:
        """为票务添加截图和 OCR 文本"""
        conn = self._get_conn()
        try:
            conn.execute("""
                UPDATE tickets
                SET screenshot_path = ?, ocr_text = ?
                WHERE id = ?
            """, (screenshot_path, ocr_text, ticket_id))
            conn.commit()
            return conn.total_changes > 0
        finally:
            conn.close()

    def delete_ticket(self, ticket_id: int) -> bool:
        conn = self._get_conn()
        try:
            conn.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
            conn.commit()
            return conn.total_changes > 0
        finally:
            conn.close()

    def get_tickets_for_itinerary(self, city: str, date: str) -> List[Dict]:
        """按城市和日期查询当天所有票务"""
        conn = self._get_conn()
        try:
            rows = conn.execute("""
                SELECT * FROM tickets
                WHERE city = ?
                  AND DATE(departure_time) = DATE(?)
                ORDER BY departure_time ASC
            """, (city, date)).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_statistics(self, city: str = "") -> Dict:
        """获取票务统计"""
        conn = self._get_conn()
        try:
            if city:
                total = conn.execute(
                    "SELECT COUNT(*) FROM tickets WHERE city = ?", (city,)
                ).fetchone()[0]
                type_counts = conn.execute("""
                    SELECT type, COUNT(*) as cnt
                    FROM tickets WHERE city = ?
                    GROUP BY type
                """, (city,)).fetchall()
            else:
                total = conn.execute(
                    "SELECT COUNT(*) FROM tickets"
                ).fetchone()[0]
                type_counts = conn.execute("""
                    SELECT type, COUNT(*) as cnt
                    FROM tickets GROUP BY type
                """).fetchall()

            return {
                "total": total,
                "by_type": {r["type"]: r["cnt"] for r in type_counts},
            }
        finally:
            conn.close()


# ── 交通票务管理器 ──────────────────────────────────────

class TransportManager:
    """高阶交通票务管理：编排票务查询、截图管理、行程整合"""

    TICKET_TYPE_LABELS = {
        "flight": "✈️ 机票",
        "train": "🚄 火车票",
        "ferry": "🚢 船票",
        "bus": "🚌 巴士票",
    }

    def __init__(self, db: Optional[TicketDatabase] = None):
        self.db = db or TicketDatabase()

    @classmethod
    def validate_ticket_type(cls, ticket_type: str) -> bool:
        return ticket_type in cls.TICKET_TYPE_LABELS

    # ── 添加票务 ──

    def add_flight(self, city: str, route: str, provider: str,
                   departure: str, arrival: str, price: float,
                   confirmation: str = "") -> int:
        return self.db.add_ticket(
            city=city, ticket_type="flight", provider=provider,
            route=route, departure_time=departure, arrival_time=arrival,
            price=price, confirmation_no=confirmation,
        )

    def add_train(self, city: str, route: str, provider: str,
                  departure: str, arrival: str, price: float,
                  confirmation: str = "") -> int:
        return self.db.add_ticket(
            city=city, ticket_type="train", provider=provider,
            route=route, departure_time=departure, arrival_time=arrival,
            price=price, confirmation_no=confirmation,
        )

    def add_ferry(self, city: str, route: str, provider: str,
                  departure: str, arrival: str, price: float,
                  confirmation: str = "") -> int:
        return self.db.add_ticket(
            city=city, ticket_type="ferry", provider=provider,
            route=route, departure_time=departure, arrival_time=arrival,
            price=price, confirmation_no=confirmation,
        )

    def add_bus(self, city: str, route: str, provider: str,
                departure: str, arrival: str, price: float,
                confirmation: str = "") -> int:
        return self.db.add_ticket(
            city=city, ticket_type="bus", provider=provider,
            route=route, departure_time=departure, arrival_time=arrival,
            price=price, confirmation_no=confirmation,
        )

    # ── 查询 ──

    def list_tickets(self, city: str = "", ticket_type: str = "",
                     status: str = "", limit: int = 20) -> List[Dict]:
        return self.db.list_tickets(city, ticket_type, status, limit)

    def get_ticket(self, ticket_id: int) -> Optional[Dict]:
        return self.db.get_ticket(ticket_id)

    # ── 截图管理 ──

    def add_screenshot(self, ticket_id: int, image_path: str,
                       ocr_text: str = "") -> bool:
        """为指定票务添加截图"""
        path_obj = Path(image_path)
        if path_obj.is_file():
            # 复制到截图目录
            dest = SCREENSHOTS_DIR / path_obj.name
            import shutil
            shutil.copy2(str(path_obj), str(dest))
            screenshot_rel = str(dest.relative_to(DOMESTIC_DIR))
        else:
            screenshot_rel = image_path

        return self.db.add_screenshot(ticket_id, screenshot_rel, ocr_text)

    # ── 行程整合 ──

    def get_itinerary_transport(self, city: str, date: str) -> Dict:
        """获取指定城市和日期的交通行程"""
        tickets = self.db.get_tickets_for_itinerary(city, date)

        if not tickets:
            return {
                "city": city,
                "date": date,
                "status": "no_tickets",
                "message": f"{city} 在 {date} 没有交通票务记录",
                "tickets": [],
            }

        total_cost = sum(t.get("price", 0) or 0 for t in tickets)
        by_type = {}
        for t in tickets:
            ttype = t.get("type", "unknown")
            if ttype not in by_type:
                by_type[ttype] = []
            by_type[ttype].append(t)

        return {
            "city": city,
            "date": date,
            "status": "success",
            "total_tickets": len(tickets),
            "total_cost": round(total_cost, 2),
            "by_type": {
                tt: {
                    "label": self.TICKET_TYPE_LABELS.get(tt, tt),
                    "count": len(items),
                    "tickets": items,
                }
                for tt, items in by_type.items()
            },
            "tickets": tickets,
        }

    # ── 格式化输出 ──

    def format_ticket(self, ticket: Dict) -> str:
        """格式化单张票务信息"""
        ttype = ticket.get("type", "unknown")
        label = self.TICKET_TYPE_LABELS.get(ttype, "🎫 票务")
        route = ticket.get("route", "")
        dep = ticket.get("departure_time", "")
        arr = ticket.get("arrival_time", "")
        price = ticket.get("price", 0)
        provider = ticket.get("provider", "")
        conf = ticket.get("confirmation_no", "")
        status = ticket.get("status", "booked")
        ticket_id = ticket.get("id", "?")

        # 解析验证链接
        links_json = ticket.get("verification_links", "[]")
        try:
            links = json.loads(links_json) if isinstance(links_json, str) else links_json
        except (json.JSONDecodeError, TypeError):
            links = []

        lines = [
            f"\n{'─'*55}",
            f"  {label} #{ticket_id} | {status}",
            f"  {route}" if route else f"  #{ticket_id}",
            f"  🕐 {dep} → {arr}" if dep and arr else "",
            f"  💰 ¥{price}" if price else "",
            f"  🏢 {provider}" if provider else "",
            f"  🔖 {conf}" if conf else "",
        ]

        # 验证链接
        if links:
            lines.append("  🔗 验证来源:")
            for link in links:
                lines.append(f"     · {link.get('label', '')}: {link.get('url', '')}")

        screenshot = ticket.get("screenshot_path", "")
        if screenshot:
            lines.append(f"  📸 截图: {screenshot}")
            ocr = ticket.get("ocr_text", "")
            if ocr:
                lines.append(f"  📝 OCR: {ocr[:100]}{'...' if len(ocr) > 100 else ''}")

        return "\n".join(line for line in lines if line)

    def format_ticket_list(self, tickets: List[Dict]) -> str:
        """格式化票务列表"""
        if not tickets:
            return "  (无票务记录)"

        lines = [f"共 {len(tickets)} 张票务:"]
        for t in tickets:
            lines.append(self.format_ticket(t))
        return "\n".join(lines)

    def format_itinerary(self, itinerary: Dict) -> str:
        """格式化行程交通信息"""
        if itinerary["status"] == "no_tickets":
            return f"📅 {itinerary['city']} {itinerary['date']}: 无交通票务记录"

        lines = [
            f"\n{'='*55}",
            f"📅 {itinerary['city']} {itinerary['date']} 交通行程",
            f"💵 总交通费: ¥{itinerary['total_cost']}",
            f"{'='*55}",
        ]

        for ttype, group in itinerary["by_type"].items():
            lines.append(f"\n{group['label']} ({group['count']} 张):")
            for t in group["tickets"]:
                lines.append(self.format_ticket(t))

        return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────

def _parse_cli():
    parser = argparse.ArgumentParser(
        description="太一旅游探路者 — 交通票务模块",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    sub = parser.add_subparsers(dest="action", required=True)

    # add
    add_p = sub.add_parser("add", help="添加票务")
    add_p.add_argument("--types", nargs="+",
                       choices=["flight", "train", "ferry", "bus"],
                       required=True, help="票务类型（可多个）")
    add_p.add_argument("--city", required=True, help="目的地城市")
    add_p.add_argument("--route", required=True, help="出发地→目的地")
    add_p.add_argument("--provider", default="", help="提供商")
    add_p.add_argument("--departure", required=True, help="出发时间")
    add_p.add_argument("--arrival", default="", help="到达时间")
    add_p.add_argument("--price", type=float, default=0, help="价格")
    add_p.add_argument("--confirmation", default="", help="订单号/票号")
    add_p.add_argument("--status", default="booked", help="状态")

    # list
    list_p = sub.add_parser("list", help="列出票务")
    list_p.add_argument("--city", default="", help="按城市筛选")
    list_p.add_argument("--type", default="", choices=["flight", "train", "ferry", "bus", ""],
                        help="按类型筛选")
    list_p.add_argument("--status", default="", help="按状态筛选")
    list_p.add_argument("--limit", type=int, default=20, help="最大显示数量")

    # get
    get_p = sub.add_parser("get", help="查看单张票务")
    get_p.add_argument("--id", type=int, required=True, help="票务 ID")

    # screenshot
    ss_p = sub.add_parser("screenshot", help="添加截图")
    ss_p.add_argument("--id", type=int, required=True, help="票务 ID")
    ss_p.add_argument("--path", required=True, help="截图路径")
    ss_p.add_argument("--ocr", default="", help="OCR 文本")

    # itinerary
    it_p = sub.add_parser("itinerary", help="行程交通概览")
    it_p.add_argument("--city", required=True, help="目的地城市")
    it_p.add_argument("--date", default="", help="日期 (YYYY-MM-DD, 默认今天)")
    it_p.add_argument("--format", choices=["text", "json"], default="text")

    # stats
    stats_p = sub.add_parser("stats", help="票务统计")
    stats_p.add_argument("--city", default="", help="按城市统计")

    # delete
    del_p = sub.add_parser("delete", help="删除票务")
    del_p.add_argument("--id", type=int, required=True, help="票务 ID")

    return parser.parse_args()


def _cli_add(args):
    mgr = TransportManager()
    ids = []
    for ttype in args.types:
        ticket_id = mgr.db.add_ticket(
            city=args.city, ticket_type=ttype, provider=args.provider,
            route=args.route, departure_time=args.departure,
            arrival_time=args.arrival, price=args.price,
            confirmation_no=args.confirmation, status=args.status,
        )
        ids.append((ttype, ticket_id))

    print(f"✅ 已添加 {len(ids)} 张票务:")
    for ttype, tid in ids:
        print(f"   {mgr.TICKET_TYPE_LABELS.get(ttype, ttype)} #{tid}")


def _cli_list(args):
    mgr = TransportManager()
    tickets = mgr.list_tickets(args.city, args.type, args.status, args.limit)
    print(mgr.format_ticket_list(tickets))

    # 统计信息
    if tickets:
        total = sum(t.get("price", 0) or 0 for t in tickets)
        print(f"\n💰 合计: ¥{round(total, 2)}")


def _cli_get(args):
    mgr = TransportManager()
    ticket = mgr.get_ticket(args.id)
    if ticket:
        print(mgr.format_ticket(ticket))
        print()
        # 显示验证链接详情
        links_json = ticket.get("verification_links", "[]")
        try:
            links = json.loads(links_json) if isinstance(links_json, str) else links_json
        except (json.JSONDecodeError, TypeError):
            links = []
        if links:
            print("  🔗 验证来源:")
            for i, link in enumerate(links, 1):
                print(f"    {i}. {link.get('label', '')}")
                print(f"       {link.get('url', '')}")
    else:
        print(f"❌ 票务 #{args.id} 不存在")


def _cli_screenshot(args):
    mgr = TransportManager()
    if mgr.add_screenshot(args.id, args.path, args.ocr):
        print(f"✅ 截图已添加到票务 #{args.id}")
    else:
        print(f"❌ 添加截图失败 (票务 #{args.id} 不存在)")


def _cli_itinerary(args):
    mgr = TransportManager()
    date = args.date or datetime.now().strftime("%Y-%m-%d")
    it = mgr.get_itinerary_transport(args.city, date)

    if args.format == "json":
        print(json.dumps(it, indent=2, ensure_ascii=False))
    else:
        print(mgr.format_itinerary(it))


def _cli_stats(args):
    db = TicketDatabase()
    stats = db.get_statistics(args.city)
    if args.city:
        print(f"\n📊 {args.city} 票务统计")
    else:
        print("\n📊 全部票务统计")
    print(f"{'='*40}")
    print(f"  总票数: {stats['total']}")
    for ttype, count in stats["by_type"].items():
        label = TransportManager.TICKET_TYPE_LABELS.get(ttype, ttype)
        print(f"  {label}: {count} 张")


def _cli_delete(args):
    db = TicketDatabase()
    ticket = db.get_ticket(args.id)
    if not ticket:
        print(f"❌ 票务 #{args.id} 不存在")
        return
    label = TransportManager.TICKET_TYPE_LABELS.get(ticket["type"], "票务")
    route = ticket.get("route", "")
    print(f"🗑️  删除 {label}: {route}")
    db.delete_ticket(args.id)
    print(f"✅ 已删除")


def cli_main(argv=None):
    if argv is not None:
        sys.argv = argv
    args = _parse_cli()
    dispatch = {
        "add": _cli_add,
        "list": _cli_list,
        "get": _cli_get,
        "screenshot": _cli_screenshot,
        "itinerary": _cli_itinerary,
        "stats": _cli_stats,
        "delete": _cli_delete,
    }
    fn = dispatch.get(args.action)
    if fn:
        fn(args)
    else:
        _parse_cli().print_help()


if __name__ == "__main__":
    cli_main()

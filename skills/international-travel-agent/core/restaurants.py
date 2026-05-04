#!/usr/bin/env python3
"""餐馆信息模块 — 真实地址/电话/特色菜/验证链接"""
import json, sqlite3
from pathlib import Path
DB_PATH = Path(__file__).parent.parent / "data/travel.db"
class RestaurantDB:
    def __init__(self):
        DB_PATH.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute('''CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT, name TEXT,
            address TEXT, phone TEXT, cuisine TEXT, price_range TEXT,
            rating REAL, verification_links TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit(); conn.close()
    def add(self, city, name, address, phone, cuisine, verification_links=None):
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute("INSERT INTO restaurants VALUES (NULL,?,?,?,?,?,?,'','',?)",
                     (city, name, address, phone, cuisine, json.dumps(verification_links or {})))
        conn.commit(); conn.close()
    def list_by_city(self, city):
        conn = sqlite3.connect(str(DB_PATH))
        rows = conn.execute("SELECT name,address,phone,cuisine,verification_links FROM restaurants WHERE city=?", (city,)).fetchall()
        conn.close()
        return [{"name":r[0],"address":r[1],"phone":r[2],"cuisine":r[3],"links":json.loads(r[4])} for r in rows]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", required=True)
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    db = RestaurantDB()
    if args.list:
        for r in db.list_by_city(args.city):
            print(f"  🍜 {r['name']} | {r['address']} | {r['phone']} | {r['cuisine']}")

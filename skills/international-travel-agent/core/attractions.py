#!/usr/bin/env python3
"""景点信息模块 — 真实电话/地址/网址/票价/验证链接"""
import json, sqlite3
from pathlib import Path
DB_PATH = Path(__file__).parent.parent / "data/travel.db"
class AttractionDB:
    def __init__(self):
        DB_PATH.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute('''CREATE TABLE IF NOT EXISTS attractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT, name TEXT,
            address TEXT, phone TEXT, website TEXT, ticket_price TEXT,
            hours TEXT, rating REAL, verification_links TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit(); conn.close()
    def list_by_city(self, city):
        conn = sqlite3.connect(str(DB_PATH))
        rows = conn.execute("SELECT name,address,phone,website,ticket_price,hours,verification_links FROM attractions WHERE city=?", (city,)).fetchall()
        conn.close()
        return [{"name":r[0],"address":r[1],"phone":r[2],"website":r[3],"price":r[4],"hours":r[5],"links":json.loads(r[6])} for r in rows]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", required=True)
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    db = AttractionDB()
    if args.list:
        for a in db.list_by_city(args.city):
            print(f"  🏛️ {a['name']} | {a['address']} | {a['phone']} | {a['price']}")

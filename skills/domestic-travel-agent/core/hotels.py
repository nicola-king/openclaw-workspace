#!/usr/bin/env python3
"""
酒店信息模块 v1.0 — 真实酒店信息+验证链接
"""
import json, sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "data/travel.db"

class HotelDB:
    def __init__(self):
        self._init_db()
    
    def _init_db(self):
        DB_PATH.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute('''CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT, name TEXT, address TEXT, phone TEXT,
            website TEXT, price_range TEXT, rating REAL,
            verification_links TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()
    
    def add(self, city, name, address, phone, website, verification_links=None):
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute("INSERT INTO hotels (city,name,address,phone,website,verification_links) VALUES (?,?,?,?,?,?)",
                     (city, name, address, phone, website, json.dumps(verification_links or {}, ensure_ascii=False)))
        conn.commit()
        conn.close()
    
    def list_by_city(self, city):
        conn = sqlite3.connect(str(DB_PATH))
        rows = conn.execute("SELECT name,address,phone,website,verification_links FROM hotels WHERE city=?", (city,)).fetchall()
        conn.close()
        return [{"name":r[0],"address":r[1],"phone":r[2],"website":r[3],"links":json.loads(r[4])} for r in rows]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", required=True)
    parser.add_argument("--add", nargs=4, metavar=("name","address","phone","website"))
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    db = HotelDB()
    if args.add:
        db.add(args.city, *args.add)
        print(f"✅ 已添加: {args.add[0]}")
    if args.list:
        for h in db.list_by_city(args.city):
            print(f"  🏨 {h['name']} | {h['address']} | {h['phone']}")
            if h['links']:
                for k,v in h['links'].items():
                    print(f"     🔗 {v['url']}")

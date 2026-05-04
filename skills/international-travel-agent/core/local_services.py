#!/usr/bin/env python3
"""落地服务模块 — 导游实名+租车真实电话+验证链接"""
import json, sqlite3
from pathlib import Path
DB_PATH = Path(__file__).parent.parent / "data/travel.db"
class ServiceDB:
    def __init__(self):
        DB_PATH.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute('''CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT, type TEXT,
            name TEXT, phone TEXT, company TEXT, license_no TEXT,
            rate TEXT, verification_links TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit(); conn.close()
    def add_guide(self, city, name, phone, company, license_no, verification_links=None):
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute("INSERT INTO services VALUES (NULL,?,'guide',?,?,?,?,'',?)",
                     (city, name, phone, company, license_no, json.dumps(verification_links or {})))
        conn.commit(); conn.close()
    def add_car_rental(self, city, company, phone, address, verification_links=None):
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute("INSERT INTO services VALUES (NULL,?,'car_rental',?,?,?,'','',?)",
                     (city, company, phone, address, json.dumps(verification_links or {})))
        conn.commit(); conn.close()
    def list_by_city(self, city, service_type=None):
        conn = sqlite3.connect(str(DB_PATH))
        if service_type:
            rows = conn.execute("SELECT type,name,phone,company,license_no,verification_links FROM services WHERE city=? AND type=?", (city, service_type)).fetchall()
        else:
            rows = conn.execute("SELECT type,name,phone,company,license_no,verification_links FROM services WHERE city=?", (city,)).fetchall()
        conn.close()
        results = []
        for r in rows:
            item = {"type":r[0],"name":r[1],"phone":r[2],"company":r[3],"license":r[4],"links":json.loads(r[5])}
            results.append(item)
        return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", required=True)
    parser.add_argument("--type", choices=["guide","car_rental"])
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    db = ServiceDB()
    if args.list:
        for s in db.list_by_city(args.city, args.type):
            icon = "👤" if s['type']=='guide' else "🚗"
            print(f"  {icon} {s['name']} | {s['phone']} | {s['company']}")

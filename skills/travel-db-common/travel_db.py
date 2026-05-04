#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一旅游探路者 v2.0 - 数据库公共模块

复用 company-enricher 模式，使用 SQLite 存储所有真实信息。
每条记录附带 verification_links 字段以支持验证溯源。

作者：太一 AGI
创建：2026-05-04
"""

import json
import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger('travel-db-common')

WORKSPACE = Path("/home/sayelf/.openclaw/workspace")


class TravelDatabase:
    """旅游数据库 - 使用 SQLite 存储所有真实信息"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        # ==== 酒店表 ====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hotels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                name TEXT NOT NULL,
                name_cn TEXT,
                address TEXT,
                phone TEXT,
                website TEXT,
                email TEXT,
                price_range TEXT,
                rating REAL,
                rating_count INTEGER,
                star_rating INTEGER,
                description TEXT,
                room_types TEXT,
                check_in_time TEXT,
                check_out_time TEXT,
                latitude REAL,
                longitude REAL,
                verification_links TEXT,
                image_urls TEXT,
                tags TEXT,
                data_quality TEXT DEFAULT 'auto',
                enriched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(city, name)
            )
        ''')

        # ==== 餐馆表 ====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                name TEXT NOT NULL,
                name_cn TEXT,
                address TEXT,
                phone TEXT,
                cuisine TEXT,
                price_per_person TEXT,
                rating REAL,
                rating_count INTEGER,
                opening_hours TEXT,
                signature_dishes TEXT,
                reservation_required INTEGER DEFAULT 0,
                website TEXT,
                latitude REAL,
                longitude REAL,
                verification_links TEXT,
                image_urls TEXT,
                tags TEXT,
                data_quality TEXT DEFAULT 'auto',
                enriched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(city, name)
            )
        ''')

        # ==== 景点表 ====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attractions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                name TEXT NOT NULL,
                name_cn TEXT,
                address TEXT,
                phone TEXT,
                website TEXT,
                opening_hours TEXT,
                ticket_price TEXT,
                category TEXT,
                duration TEXT,
                rating REAL,
                rating_count INTEGER,
                latitude REAL,
                longitude REAL,
                verification_links TEXT,
                image_urls TEXT,
                tags TEXT,
                description TEXT,
                data_quality TEXT DEFAULT 'auto',
                enriched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(city, name)
            )
        ''')

        # ==== 本地服务表 ====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS local_services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                service_type TEXT NOT NULL,
                company_name TEXT NOT NULL,
                contact_name TEXT,
                phone TEXT,
                email TEXT,
                website TEXT,
                address TEXT,
                description TEXT,
                price_info TEXT,
                business_hours TEXT,
                verification_links TEXT,
                tags TEXT,
                data_quality TEXT DEFAULT 'auto',
                enriched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(city, company_name, service_type)
            )
        ''')

        # ==== 目的地指南表 ====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS destination_guides (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                category TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                source TEXT,
                language TEXT DEFAULT 'zh',
                verification_links TEXT,
                enriched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(city, category, title)
            )
        ''')

        # ==== 行程计划表 ====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trip_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_name TEXT NOT NULL,
                city TEXT NOT NULL,
                days INTEGER,
                budget REAL,
                preferences TEXT,
                plan_data TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # ==== 综合评估表 ====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS intelligence_ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                source TEXT NOT NULL,
                item_type TEXT NOT NULL,
                item_name TEXT NOT NULL,
                rating REAL,
                review_count INTEGER,
                review_url TEXT,
                summary TEXT,
                enriched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(city, source, item_type, item_name)
            )
        ''')

        # ==== 天气和预防措施表 ====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_safety (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                month INTEGER,
                avg_temp_high REAL,
                avg_temp_low REAL,
                avg_humidity REAL,
                rainfall_mm REAL,
                weather_notes TEXT,
                natural_disaster_risk TEXT,
                health_advisory TEXT,
                safety_tips TEXT,
                enriched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(city, month)
            )
        ''')

        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_hotels_city ON hotels(city)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_restaurants_city ON restaurants(city)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_attractions_city ON attractions(city)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_services_city_type ON local_services(city, service_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_guides_city_cat ON destination_guides(city, category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_intel_city ON intelligence_ratings(city)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_weather_city ON weather_safety(city)')

        conn.commit()
        conn.close()

    def _conn(self):
        return sqlite3.connect(str(self.db_path))

    # ==================== CRUD: Hotels ====================

    def save_hotel(self, city: str, data: Dict[str, Any]) -> int:
        conn = self._conn()
        cursor = conn.cursor()
        verification_links = json.dumps(data.get('verification_links', []), ensure_ascii=False)
        image_urls = json.dumps(data.get('image_urls', []), ensure_ascii=False)
        cursor.execute('''
            INSERT OR REPLACE INTO hotels
            (city, name, name_cn, address, phone, website, email,
             price_range, rating, rating_count, star_rating,
             description, room_types, check_in_time, check_out_time,
             latitude, longitude, verification_links, image_urls, tags, data_quality)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (
            city, data.get('name'), data.get('name_cn'), data.get('address'),
            data.get('phone'), data.get('website'), data.get('email'),
            data.get('price_range'), data.get('rating'), data.get('rating_count'),
            data.get('star_rating'), data.get('description'),
            data.get('room_types'), data.get('check_in_time'), data.get('check_out_time'),
            data.get('latitude'), data.get('longitude'),
            verification_links, image_urls,
            json.dumps(data.get('tags', [])), data.get('data_quality', 'auto')
        ))
        conn.commit()
        hid = cursor.lastrowid
        conn.close()
        return hid

    def get_hotels(self, city: str) -> List[Dict[str, Any]]:
        conn = self._conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM hotels WHERE city=? ORDER BY rating DESC', (city,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        for r in rows:
            r['verification_links'] = json.loads(r.get('verification_links', '[]'))
            r['image_urls'] = json.loads(r.get('image_urls', '[]'))
            r['tags'] = json.loads(r.get('tags', '[]'))
        return rows

    def search_hotels(self, city: str, keyword: str = '') -> List[Dict[str, Any]]:
        conn = self._conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if keyword:
            cursor.execute('''
                SELECT * FROM hotels WHERE city=? AND (name LIKE ? OR name_cn LIKE ? OR address LIKE ?)
                ORDER BY rating DESC
            ''', (city, f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        else:
            cursor.execute('SELECT * FROM hotels WHERE city=? ORDER BY rating DESC', (city,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        for r in rows:
            r['verification_links'] = json.loads(r.get('verification_links', '[]'))
            r['image_urls'] = json.loads(r.get('image_urls', '[]'))
            r['tags'] = json.loads(r.get('tags', '[]'))
        return rows

    # ==================== CRUD: Restaurants ====================

    def save_restaurant(self, city: str, data: Dict[str, Any]) -> int:
        conn = self._conn()
        cursor = conn.cursor()
        verification_links = json.dumps(data.get('verification_links', []), ensure_ascii=False)
        image_urls = json.dumps(data.get('image_urls', []), ensure_ascii=False)
        cursor.execute('''
            INSERT OR REPLACE INTO restaurants
            (city, name, name_cn, address, phone, cuisine, price_per_person,
             rating, rating_count, opening_hours, signature_dishes,
             reservation_required, website, latitude, longitude,
             verification_links, image_urls, tags, data_quality)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (
            city, data.get('name'), data.get('name_cn'), data.get('address'),
            data.get('phone'), data.get('cuisine'), data.get('price_per_person'),
            data.get('rating'), data.get('rating_count'), data.get('opening_hours'),
            data.get('signature_dishes'), 1 if data.get('reservation_required') else 0,
            data.get('website'), data.get('latitude'), data.get('longitude'),
            verification_links, image_urls,
            json.dumps(data.get('tags', [])), data.get('data_quality', 'auto')
        ))
        conn.commit()
        rid = cursor.lastrowid
        conn.close()
        return rid

    def get_restaurants(self, city: str) -> List[Dict[str, Any]]:
        conn = self._conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM restaurants WHERE city=? ORDER BY rating DESC', (city,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        for r in rows:
            r['verification_links'] = json.loads(r.get('verification_links', '[]'))
            r['image_urls'] = json.loads(r.get('image_urls', '[]'))
            r['tags'] = json.loads(r.get('tags', '[]'))
        return rows

    # ==================== CRUD: Attractions ====================

    def save_attraction(self, city: str, data: Dict[str, Any]) -> int:
        conn = self._conn()
        cursor = conn.cursor()
        verification_links = json.dumps(data.get('verification_links', []), ensure_ascii=False)
        image_urls = json.dumps(data.get('image_urls', []), ensure_ascii=False)
        cursor.execute('''
            INSERT OR REPLACE INTO attractions
            (city, name, name_cn, address, phone, website, opening_hours,
             ticket_price, category, duration, rating, rating_count,
             latitude, longitude, verification_links, image_urls, tags, description, data_quality)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (
            city, data.get('name'), data.get('name_cn'), data.get('address'),
            data.get('phone'), data.get('website'), data.get('opening_hours'),
            data.get('ticket_price'), data.get('category'), data.get('duration'),
            data.get('rating'), data.get('rating_count'),
            data.get('latitude'), data.get('longitude'),
            verification_links, image_urls,
            json.dumps(data.get('tags', [])), data.get('description'),
            data.get('data_quality', 'auto')
        ))
        conn.commit()
        aid = cursor.lastrowid
        conn.close()
        return aid

    def get_attractions(self, city: str, category: str = '') -> List[Dict[str, Any]]:
        conn = self._conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if category:
            cursor.execute('SELECT * FROM attractions WHERE city=? AND category=? ORDER BY rating DESC',
                          (city, category))
        else:
            cursor.execute('SELECT * FROM attractions WHERE city=? ORDER BY rating DESC', (city,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        for r in rows:
            r['verification_links'] = json.loads(r.get('verification_links', '[]'))
            r['image_urls'] = json.loads(r.get('image_urls', '[]'))
            r['tags'] = json.loads(r.get('tags', '[]'))
        return rows

    # ==================== CRUD: Local Services ====================

    def save_service(self, city: str, data: Dict[str, Any]) -> int:
        conn = self._conn()
        cursor = conn.cursor()
        verification_links = json.dumps(data.get('verification_links', []), ensure_ascii=False)
        cursor.execute('''
            INSERT OR REPLACE INTO local_services
            (city, service_type, company_name, contact_name, phone, email,
             website, address, description, price_info, business_hours,
             verification_links, tags, data_quality)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (
            city, data.get('service_type'), data.get('company_name'),
            data.get('contact_name'), data.get('phone'), data.get('email'),
            data.get('website'), data.get('address'), data.get('description'),
            data.get('price_info'), data.get('business_hours'),
            verification_links, json.dumps(data.get('tags', [])),
            data.get('data_quality', 'auto')
        ))
        conn.commit()
        sid = cursor.lastrowid
        conn.close()
        return sid

    def get_services(self, city: str, service_type: str = '') -> List[Dict[str, Any]]:
        conn = self._conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if service_type:
            cursor.execute('SELECT * FROM local_services WHERE city=? AND service_type=?',
                          (city, service_type))
        else:
            cursor.execute('SELECT * FROM local_services WHERE city=?', (city,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        for r in rows:
            r['verification_links'] = json.loads(r.get('verification_links', '[]'))
            r['tags'] = json.loads(r.get('tags', '[]'))
        return rows

    # ==================== CRUD: Destination Guides ====================

    def save_guide(self, city: str, category: str, title: str, content: str,
                   source: str = '', verification_links: List[str] = None) -> int:
        conn = self._conn()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO destination_guides
            (city, category, title, content, source, verification_links)
            VALUES (?,?,?,?,?,?)
        ''', (
            city, category, title, content, source,
            json.dumps(verification_links or [], ensure_ascii=False)
        ))
        conn.commit()
        gid = cursor.lastrowid
        conn.close()
        return gid

    def get_guides(self, city: str, category: str = '') -> List[Dict[str, Any]]:
        conn = self._conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if category:
            cursor.execute('SELECT * FROM destination_guides WHERE city=? AND category=?', (city, category))
        else:
            cursor.execute('SELECT * FROM destination_guides WHERE city=?', (city,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        for r in rows:
            r['verification_links'] = json.loads(r.get('verification_links', '[]'))
        return rows

    # ==================== CRUD: Trip Plans ====================

    def save_plan(self, plan_name: str, city: str, days: int, budget: float,
                  preferences: str, plan_data: Dict) -> int:
        conn = self._conn()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO trip_plans (plan_name, city, days, budget, preferences, plan_data)
            VALUES (?,?,?,?,?,?)
        ''', (plan_name, city, days, budget, preferences, json.dumps(plan_data, ensure_ascii=False)))
        conn.commit()
        pid = cursor.lastrowid
        conn.close()
        return pid

    def get_plans(self, city: str = '') -> List[Dict[str, Any]]:
        conn = self._conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if city:
            cursor.execute('SELECT * FROM trip_plans WHERE city=? ORDER BY created_at DESC', (city,))
        else:
            cursor.execute('SELECT * FROM trip_plans ORDER BY created_at DESC')
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        for r in rows:
            r['plan_data'] = json.loads(r.get('plan_data', '{}'))
        return rows

    # ==================== CRUD: Intelligence ====================

    def save_rating(self, city: str, source: str, item_type: str, item_name: str,
                    rating: float, review_count: int, review_url: str = '',
                    summary: str = '') -> int:
        conn = self._conn()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO intelligence_ratings
            (city, source, item_type, item_name, rating, review_count, review_url, summary)
            VALUES (?,?,?,?,?,?,?,?)
        ''', (city, source, item_type, item_name, rating, review_count, review_url, summary))
        conn.commit()
        iid = cursor.lastrowid
        conn.close()
        return iid

    def get_ratings(self, city: str) -> List[Dict[str, Any]]:
        conn = self._conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM intelligence_ratings WHERE city=?', (city,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    # ==================== CRUD: Weather ====================

    def save_weather(self, city: str, month: int, data: Dict[str, Any]) -> int:
        conn = self._conn()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO weather_safety
            (city, month, avg_temp_high, avg_temp_low, avg_humidity, rainfall_mm,
             weather_notes, natural_disaster_risk, health_advisory, safety_tips)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        ''', (
            city, month, data.get('avg_temp_high'), data.get('avg_temp_low'),
            data.get('avg_humidity'), data.get('rainfall_mm'),
            data.get('weather_notes'), data.get('natural_disaster_risk'),
            data.get('health_advisory'), data.get('safety_tips')
        ))
        conn.commit()
        wid = cursor.lastrowid
        conn.close()
        return wid

    def get_weather(self, city: str, month: int = 0) -> List[Dict[str, Any]]:
        conn = self._conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if month:
            cursor.execute('SELECT * FROM weather_safety WHERE city=? AND month=?', (city, month))
        else:
            cursor.execute('SELECT * FROM weather_safety WHERE city=? ORDER BY month', (city,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    # ==================== 通用搜索 ====================

    def search_all(self, city: str, keyword: str) -> Dict[str, List]:
        """跨表搜索"""
        return {
            'hotels': self.search_hotels(city, keyword),
            'restaurants': self.search_hotels(city, keyword),
            'attractions': self.get_attractions(city),
            'services': self.get_services(city),
        }

    def get_statistics(self, city: str) -> Dict[str, int]:
        conn = self._conn()
        cursor = conn.cursor()
        stats = {}
        for table in ['hotels', 'restaurants', 'attractions', 'local_services',
                      'destination_guides', 'intelligence_ratings', 'weather_safety']:
            cursor.execute(f'SELECT COUNT(*) FROM {table} WHERE city=?', (city,))
            stats[table] = cursor.fetchone()[0]
        conn.close()
        return stats

    def export_city_json(self, city: str) -> Dict[str, Any]:
        """导出城市完整数据为 JSON"""
        return {
            'city': city,
            'exported_at': datetime.now().isoformat(),
            'hotels': self.get_hotels(city),
            'restaurants': self.get_restaurants(city),
            'attractions': self.get_attractions(city),
            'services': self.get_services(city),
            'guides': self.get_guides(city),
            'ratings': self.get_ratings(city),
            'weather': self.get_weather(city),
            'plans': self.get_plans(city),
        }

    def import_city_json(self, city: str, data: Dict[str, Any]) -> Dict[str, int]:
        """从 JSON 导入城市数据"""
        counts = {'hotels': 0, 'restaurants': 0, 'attractions': 0, 'services': 0}
        for item in data.get('hotels', []):
            self.save_hotel(city, item)
            counts['hotels'] += 1
        for item in data.get('restaurants', []):
            self.save_restaurant(city, item)
            counts['restaurants'] += 1
        for item in data.get('attractions', []):
            self.save_attraction(city, item)
            counts['attractions'] += 1
        for item in data.get('services', []):
            self.save_service(city, item)
            counts['services'] += 1
        return counts

#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 经验存储 (Experience Store)

持久化旅行经验：决策、结果、用户反馈
支持 JSONL 追加写入和 SQLite 查询
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class ExperienceStore:
    """经验存储引擎"""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).parent.parent.parent / "data" / "experience"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.trips_file = self.data_dir / "trips.jsonl"
        self.patterns_file = self.data_dir / "patterns.json"
        self._init_db()

    def _init_db(self) -> None:
        """初始化 SQLite 数据库"""
        self.db_path = self.data_dir / "experience.db"
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                id TEXT PRIMARY KEY,
                destination TEXT,
                origin TEXT,
                budget REAL,
                travelers INTEGER,
                start_date TEXT,
                end_date TEXT,
                rating REAL,
                feedback TEXT,
                created_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                destination TEXT,
                season TEXT,
                avg_budget REAL,
                confidence REAL,
                created_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill_name TEXT,
                skill_type TEXT,
                trigger_reason TEXT,
                created_at TEXT
            )
        """)
        conn.commit()
        conn.close()

    def record_trip(
        self,
        destination: str,
        origin: str,
        budget: float,
        travelers: int,
        start_date: str,
        end_date: str,
        rating: float = 0.0,
        feedback: str = "",
    ) -> str:
        """
        记录一次旅行经验

        Args:
            destination: 目的地
            origin: 出发地
            budget: 预算
            travelers: 人数
            start_date: 开始日期
            end_date: 结束日期
            rating: 评分 (0-5)
            feedback: 用户反馈

        Returns:
            经验 ID
        """
        trip_id = f"trip_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{destination}"
        record = {
            "id": trip_id,
            "destination": destination,
            "origin": origin,
            "budget": budget,
            "travelers": travelers,
            "start_date": start_date,
            "end_date": end_date,
            "rating": rating,
            "feedback": feedback,
            "created_at": datetime.now().isoformat(),
        }

        # JSONL 追加
        with open(self.trips_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        # SQLite 写入
        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            "INSERT OR REPLACE INTO trips VALUES (?,?,?,?,?,?,?,?,?,?)",
            (trip_id, destination, origin, budget, travelers,
             start_date, end_date, rating, feedback, record["created_at"]),
        )
        conn.commit()
        conn.close()

        return trip_id

    def get_trips(
        self,
        destination: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict]:
        """查询旅行记录"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        if destination:
            rows = conn.execute(
                "SELECT * FROM trips WHERE destination = ? ORDER BY created_at DESC LIMIT ?",
                (destination, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM trips ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_destinations(self) -> List[str]:
        """获取所有去过的目的地"""
        conn = sqlite3.connect(str(self.db_path))
        rows = conn.execute("SELECT DISTINCT destination FROM trips").fetchall()
        conn.close()
        return [r[0] for r in rows]

    def get_destination_count(self, destination: str) -> int:
        """获取某目的地访问次数"""
        conn = sqlite3.connect(str(self.db_path))
        count = conn.execute(
            "SELECT COUNT(*) FROM trips WHERE destination = ?", (destination,)
        ).fetchone()[0]
        conn.close()
        return count

    def get_avg_budget(self, destination: str) -> float:
        """获取某目的地平均预算"""
        conn = sqlite3.connect(str(self.db_path))
        result = conn.execute(
            "SELECT AVG(budget) FROM trips WHERE destination = ?", (destination,)
        ).fetchone()[0]
        conn.close()
        return result or 0.0

    def get_avg_rating(self, destination: str) -> float:
        """获取某目的地平均评分"""
        conn = sqlite3.connect(str(self.db_path))
        result = conn.execute(
            "SELECT AVG(rating) FROM trips WHERE destination = ? AND rating > 0", (destination,)
        ).fetchone()[0]
        conn.close()
        return result or 0.0








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48
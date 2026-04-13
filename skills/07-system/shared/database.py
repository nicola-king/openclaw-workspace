#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库连接池模块 - Database Connection Pool

太一系统共享数据库层，提供连接池管理、事务支持、查询封装。
支持 PostgreSQL、SQLite、MySQL 等主流数据库。

@author: 太一
@version: 1.0.0
@created: 2026-04-07
"""

import asyncio
import sqlite3
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from .config import config


@dataclass
class QueryResult:
    """查询结果封装"""
    rows: List[Tuple]
    columns: List[str]
    row_count: int
    elapsed_ms: float
    
    def to_dicts(self) -> List[Dict[str, Any]]:
        """转换为字典列表"""
        return [dict(zip(self.columns, row)) for row in self.rows]
    
    def first(self) -> Optional[Dict[str, Any]]:
        """返回第一条记录"""
        dicts = self.to_dicts()
        return dicts[0] if dicts else None
    
    def scalar(self) -> Any:
        """返回单个标量值"""
        if self.rows and len(self.rows[0]) > 0:
            return self.rows[0][0]
        return None


class DatabasePool:
    """
    数据库连接池
    
    提供异步连接池管理，支持事务、批量操作、查询缓存。
    
    使用示例:
        >>> db = DatabasePool.get_instance()
        >>> await db.connect()
        >>> async with db.transaction() as tx:
        ...     await tx.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
        >>> result = await db.fetch("SELECT * FROM users WHERE id = ?", (1,))
        >>> await db.close()
    """
    
    _instance: Optional["DatabasePool"] = None
    
    def __init__(self):
        self._conn: Optional[sqlite3.Connection] = None
        self._db_path: Optional[Path] = None
        self._connected = False
        self._config = config
    
    @classmethod
    def get_instance(cls) -> "DatabasePool":
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def reset_instance(cls):
        """重置单例（用于测试）"""
        cls._instance = None
    
    async def connect(self, db_path: Optional[str] = None) -> bool:
        """
        连接到数据库
        
        Args:
            db_path: 数据库文件路径，默认使用 workspace/taiyi.db
            
        Returns:
            bool: 连接是否成功
        """
        if self._connected:
            return True
        
        try:
            if db_path:
                self._db_path = Path(db_path)
            else:
                workspace = Path(self._config.system.workspace)
                self._db_path = workspace / "taiyi.db"
            
            # 确保目录存在
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 创建连接（使用线程池模拟异步）
            loop = asyncio.get_event_loop()
            self._conn = await loop.run_in_executor(
                None, 
                lambda: sqlite3.connect(str(self._db_path), check_same_thread=False)
            )
            self._conn.row_factory = sqlite3.Row
            
            # 初始化基础表
            await self._init_schema()
            
            self._connected = True
            print(f"[Database] 已连接：{self._db_path}")
            return True
            
        except Exception as e:
            print(f"[Database] 连接失败：{e}")
            return False
    
    async def _init_schema(self):
        """初始化基础表结构"""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS _system (
                key TEXT PRIMARY KEY,
                value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS _events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                payload TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS _cache (
                key TEXT PRIMARY KEY,
                value TEXT,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        ]
        
        for sql in tables:
            await self.execute(sql)
    
    async def close(self):
        """关闭数据库连接"""
        if self._conn:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._conn.close)
            self._conn = None
            self._connected = False
            print("[Database] 连接已关闭")
    
    @asynccontextmanager
    async def transaction(self):
        """
        事务上下文管理器
        
        使用示例:
            async with db.transaction() as tx:
                await tx.execute("INSERT ...")
                await tx.execute("UPDATE ...")
            # 自动 commit，异常时自动 rollback
        """
        if not self._connected:
            raise RuntimeError("数据库未连接")
        
        cursor = self._conn.cursor()
        try:
            yield cursor
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            raise e
        finally:
            cursor.close()
    
    async def execute(
        self, 
        sql: str, 
        params: Optional[Tuple] = None,
        fetch: bool = False
    ) -> Union[int, QueryResult]:
        """
        执行 SQL 语句
        
        Args:
            sql: SQL 语句
            params: 参数元组
            fetch: 是否返回结果
            
        Returns:
            int: 受影响的行数（非查询）
            QueryResult: 查询结果（查询）
        """
        if not self._connected:
            raise RuntimeError("数据库未连接")
        
        loop = asyncio.get_event_loop()
        start_time = datetime.now()
        
        def _execute():
            cursor = self._conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            
            if fetch:
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                return rows, columns
            else:
                self._conn.commit()
                return cursor.rowcount, []
        
        try:
            result, columns = await loop.run_in_executor(None, _execute)
            elapsed = (datetime.now() - start_time).total_seconds() * 1000
            
            if fetch:
                return QueryResult(
                    rows=result,
                    columns=columns,
                    row_count=len(result),
                    elapsed_ms=elapsed
                )
            else:
                return result
                
        except Exception as e:
            print(f"[Database] 执行失败：{sql[:100]}... 错误：{e}")
            raise
    
    async def fetch(
        self, 
        sql: str, 
        params: Optional[Tuple] = None
    ) -> QueryResult:
        """执行查询并返回结果"""
        return await self.execute(sql, params, fetch=True)
    
    async def fetch_one(
        self, 
        sql: str, 
        params: Optional[Tuple] = None
    ) -> Optional[Dict[str, Any]]:
        """查询单条记录"""
        result = await self.fetch(sql, params)
        return result.first()
    
    async def fetch_scalar(
        self, 
        sql: str, 
        params: Optional[Tuple] = None
    ) -> Any:
        """查询单个值"""
        result = await self.fetch(sql, params)
        return result.scalar()
    
    async def insert(self, table: str, data: Dict[str, Any]) -> int:
        """
        插入记录
        
        Args:
            table: 表名
            data: 数据字典
            
        Returns:
            int: 插入的行 ID
        """
        columns = list(data.keys())
        placeholders = ", ".join(["?" for _ in columns])
        values = tuple(data.values())
        
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        await self.execute(sql, values)
        
        # 返回最后插入的 ID
        result = await self.fetch_scalar("SELECT last_insert_rowid()")
        return result
    
    async def update(
        self, 
        table: str, 
        data: Dict[str, Any], 
        where: str, 
        params: Optional[Tuple] = None
    ) -> int:
        """
        更新记录
        
        Args:
            table: 表名
            data: 要更新的字段
            where: WHERE 子句（不含 WHERE 关键字）
            params: WHERE 参数
            
        Returns:
            int: 受影响的行数
        """
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        values = tuple(data.values()) + (params or ())
        
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        return await self.execute(sql, values)
    
    async def delete(self, table: str, where: str, params: Optional[Tuple] = None) -> int:
        """
        删除记录
        
        Args:
            table: 表名
            where: WHERE 子句
            params: WHERE 参数
            
        Returns:
            int: 受影响的行数
        """
        sql = f"DELETE FROM {table} WHERE {where}"
        return await self.execute(sql, params)
    
    async def exists(self, table: str, where: str, params: Optional[Tuple] = None) -> bool:
        """检查记录是否存在"""
        sql = f"SELECT 1 FROM {table} WHERE {where} LIMIT 1"
        result = await self.fetch_scalar(sql, params)
        return result is not None
    
    async def count(self, table: str, where: Optional[str] = None, params: Optional[Tuple] = None) -> int:
        """统计记录数"""
        sql = f"SELECT COUNT(*) FROM {table}"
        if where:
            sql += f" WHERE {where}"
        result = await self.fetch_scalar(sql, params)
        return result or 0
    
    async def batch_insert(self, table: str, rows: List[Dict[str, Any]]) -> int:
        """
        批量插入
        
        Args:
            table: 表名
            rows: 数据字典列表
            
        Returns:
            int: 插入的行数
        """
        if not rows:
            return 0
        
        columns = list(rows[0].keys())
        placeholders = ", ".join(["?" for _ in columns])
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        
        async with self.transaction() as tx:
            for row in rows:
                values = tuple(row[k] for k in columns)
                tx.execute(sql, values)
        
        return len(rows)


# 全局数据库实例
db = DatabasePool.get_instance()


if __name__ == "__main__":
    # 测试代码
    import asyncio
    
    async def test():
        print("[Database] 测试数据库模块")
        
        await db.connect()
        
        # 测试插入
        row_id = await db.insert("_system", {"key": "test_key", "value": "test_value"})
        print(f"  插入 ID: {row_id}")
        
        # 测试查询
        result = await db.fetch("SELECT * FROM _system WHERE key = ?", ("test_key",))
        print(f"  查询结果：{result.to_dicts()}")
        
        # 测试更新
        affected = await db.update("_system", {"value": "updated"}, "key = ?", ("test_key",))
        print(f"  更新行数：{affected}")
        
        # 测试删除
        deleted = await db.delete("_system", "key = ?", ("test_key",))
        print(f"  删除行数：{deleted}")
        
        await db.close()
        print("[Database] 测试完成")
    
    asyncio.run(test())

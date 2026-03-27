"""
PolyAlert 数据存储模块
使用 SQLite 存储市场数据、提醒记录、用户订阅
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from .config import DATABASE_PATH

def init_db():
    """初始化数据库"""
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # 监控市场表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS markets (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            category TEXT,
            current_prob REAL,
            last_checked TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 提醒记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            market_id TEXT,
            market_name TEXT,
            trigger_type TEXT,
            old_prob REAL,
            new_prob REAL,
            telegram_user_id TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (market_id) REFERENCES markets(id)
        )
    ''')
    
    # 用户订阅表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_user_id TEXT UNIQUE,
            status TEXT DEFAULT 'trial',
            trial_start TIMESTAMP,
            trial_end TIMESTAMP,
            paid_until TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 价格历史表（用于计算变化）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            market_id TEXT,
            probability REAL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (market_id) REFERENCES markets(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_market(market_id, name, url, category, prob):
    """保存/更新市场数据"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO markets (id, name, url, category, current_prob, last_checked)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (market_id, name, url, category, prob, datetime.now()))
    
    conn.commit()
    conn.close()

def save_price_history(market_id, prob):
    """保存价格历史"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO price_history (market_id, probability)
        VALUES (?, ?)
    ''', (market_id, prob))
    
    conn.commit()
    conn.close()

def get_last_probability(market_id):
    """获取上次记录的概率"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT probability FROM price_history
        WHERE market_id = ?
        ORDER BY recorded_at DESC
        LIMIT 1
    ''', (market_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else None

def save_alert(market_id, market_name, trigger_type, old_prob, new_prob, telegram_user_id=None):
    """保存提醒记录"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO alerts (market_id, market_name, trigger_type, old_prob, new_prob, telegram_user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (market_id, market_name, trigger_type, old_prob, new_prob, telegram_user_id))
    
    conn.commit()
    conn.close()

def get_alert_count(hours=24):
    """获取指定时间内的提醒数量"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*) FROM alerts
        WHERE sent_at > datetime('now', ?)
    ''', (f'-{hours} hours',))
    
    result = cursor.fetchone()
    conn.close()
    
    return result[0]

def get_subscriber(telegram_user_id):
    """获取用户订阅信息"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM subscriptions
        WHERE telegram_user_id = ?
    ''', (telegram_user_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'id': result[0],
            'telegram_user_id': result[1],
            'status': result[2],
            'trial_start': result[3],
            'trial_end': result[4],
            'paid_until': result[5]
        }
    return None

def add_subscriber(telegram_user_id, trial_days=7):
    """添加新订阅用户（7 天试用）"""
    from datetime import timedelta
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    now = datetime.now()
    trial_end = now + timedelta(days=trial_days)
    
    cursor.execute('''
        INSERT OR REPLACE INTO subscriptions (telegram_user_id, status, trial_start, trial_end)
        VALUES (?, 'trial', ?, ?)
    ''', (telegram_user_id, now, trial_end))
    
    conn.commit()
    conn.close()

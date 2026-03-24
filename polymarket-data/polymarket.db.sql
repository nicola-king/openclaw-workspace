-- Polymarket 数据基座数据库结构
-- 创建时间：2026-03-23 23:45

-- 气象预测表
CREATE TABLE IF NOT EXISTS weather_forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    fetched_at TEXT NOT NULL,
    date TEXT NOT NULL,
    temp_max REAL,
    temp_min REAL,
    precip_sum REAL,
    weather_code INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 市场赔率表
CREATE TABLE IF NOT EXISTS market_odds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_id TEXT UNIQUE NOT NULL,
    market_name TEXT,
    odds REAL,
    implied_prob REAL,
    fetched_at TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 套利机会表
CREATE TABLE IF NOT EXISTS arbitrage_opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_id TEXT,
    confidence REAL,
    edge REAL,
    recommended_stake REAL,
    status TEXT DEFAULT 'pending',
    executed_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 策略执行日志
CREATE TABLE IF NOT EXISTS strategy_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_version TEXT,
    opportunities_found INTEGER,
    total_exposure REAL,
    executed_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_weather_city ON weather_forecasts(city);
CREATE INDEX IF NOT EXISTS idx_weather_date ON weather_forecasts(date);
CREATE INDEX IF NOT EXISTS idx_market_fetched ON market_odds(fetched_at);
CREATE INDEX IF NOT EXISTS idx_arb_status ON arbitrage_opportunities(status);

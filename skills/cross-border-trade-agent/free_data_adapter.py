#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
免费开源数据适配器

功能:
- 使用免费 API 和爬虫获取真实数据
- 替代付费数据源
- 缓存机制减少重复请求

作者：太一 AGI
创建：2026-05-04
"""

import json
import logging
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import urllib.request
import urllib.parse

# 日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('FreeDataAdapter')

# 缓存目录
CACHE_DIR = Path("/home/sayelf/.openclaw/workspace/data/cross-border-trade-agent/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# 数据库
DB_PATH = Path("/home/sayelf/.openclaw/workspace/data/cross-border-trade-agent/trade_data.db")


class FreeDataAdapter:
    """免费数据适配器"""
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = 3600  # 缓存 1 小时
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 汇率表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exchange_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                base_currency TEXT,
                target_currency TEXT,
                rate REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 贸易数据表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trade_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                country TEXT,
                product TEXT,
                value REAL,
                year INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 缓存表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_name TEXT,
                params TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ 数据库初始化完成")
    
    def _get_cache(self, api_name: str, params: str) -> Optional[Dict]:
        """获取缓存"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT response, timestamp FROM api_cache
            WHERE api_name = ? AND params = ?
            ORDER BY timestamp DESC LIMIT 1
        ''', (api_name, params))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            response, timestamp = result
            cache_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            if datetime.now() - cache_time < timedelta(seconds=self.cache_duration):
                return json.loads(response)
        
        return None
    
    def _set_cache(self, api_name: str, params: str, response: Dict):
        """设置缓存"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO api_cache (api_name, params, response)
            VALUES (?, ?, ?)
        ''', (api_name, params, json.dumps(response)))
        
        conn.commit()
        conn.close()
    
    def get_exchange_rate(self, base: str = "USD", target: str = "CNY") -> Optional[float]:
        """
        获取汇率 (免费 API)
        
        Args:
            base: 基础货币
            target: 目标货币
            
        Returns:
            汇率数值
        """
        cache_key = f"{base}_{target}"
        cached = self._get_cache("exchange_rate", cache_key)
        if cached:
            logger.info(f"💾 使用缓存汇率: {base}/{target}")
            return cached.get("rate")
        
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{base}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                rate = data['rates'].get(target)
                
                if rate:
                    self._set_cache("exchange_rate", cache_key, {"rate": rate})
                    logger.info(f"✅ 获取汇率: {base}/{target} = {rate}")
                    return rate
        except Exception as e:
            logger.error(f"⚠️ 获取汇率失败: {e}")
        
        return None
    
    def get_world_bank_data(self, country: str, indicator: str, year: int = 2023) -> Optional[Dict]:
        """
        获取世界银行数据
        
        Args:
            country: 国家代码 (如 CHN, USA)
            indicator: 指标代码 (如 NE.EXP.GNFS.CD 出口)
            year: 年份
            
        Returns:
            数据字典
        """
        cache_key = f"{country}_{indicator}_{year}"
        cached = self._get_cache("world_bank", cache_key)
        if cached:
            return cached
        
        try:
            url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&date={year}&per_page=1"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if len(data) > 1 and data[1]:
                    result = {
                        "country": country,
                        "indicator": indicator,
                        "year": year,
                        "value": data[1][0].get("value"),
                        "unit": "USD"
                    }
                    self._set_cache("world_bank", cache_key, result)
                    logger.info(f"✅ 获取世界银行数据: {country}/{indicator}/{year}")
                    return result
        except Exception as e:
            logger.error(f"⚠️ 获取世界银行数据失败: {e}")
        
        return None
    
    def get_trade_summary(self, country: str = "CHN") -> Dict:
        """
        获取贸易摘要
        
        Args:
            country: 国家代码
            
        Returns:
            贸易数据摘要
        """
        logger.info(f"📊 获取 {country} 贸易摘要")
        
        # 出口数据
        export_data = self.get_world_bank_data(country, "NE.EXP.GNFS.CD", 2023)
        # 进口数据
        import_data = self.get_world_bank_data(country, "NE.IMP.GNFS.CD", 2023)
        # GDP
        gdp_data = self.get_world_bank_data(country, "NY.GDP.MKTP.CD", 2023)
        
        summary = {
            "country": country,
            "year": 2023,
            "export_value": export_data.get("value") if export_data else None,
            "import_value": import_data.get("value") if import_data else None,
            "gdp": gdp_data.get("value") if gdp_data else None,
            "timestamp": datetime.now().isoformat()
        }
        
        # 计算贸易依存度
        if summary["export_value"] and summary["gdp"]:
            summary["trade_dependence"] = (summary["export_value"] / summary["gdp"]) * 100
        
        logger.info(f"✅ 贸易摘要生成完成")
        return summary
    
    def get_google_trends(self, keyword: str, geo: str = "US") -> Optional[Dict]:
        """
        获取 Google Trends 数据 (简化版)
        
        Args:
            keyword: 关键词
            geo: 地区
            
        Returns:
            趋势数据
        """
        # 注意：Google Trends 需要复杂处理，这里返回模拟数据
        # 实际使用需要 pytrends 库或爬虫
        logger.info(f"📈 Google Trends: {keyword} ({geo})")
        
        return {
            "keyword": keyword,
            "geo": geo,
            "trend_score": 75,  # 模拟数据
            "note": "需要 pytrends 库获取真实数据",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_all_exchange_rates(self, base: str = "USD") -> Optional[Dict]:
        """
        获取所有汇率
        
        Args:
            base: 基础货币
            
        Returns:
            汇率字典
        """
        cache_key = f"all_{base}"
        cached = self._get_cache("exchange_rates_all", cache_key)
        if cached:
            return cached
        
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{base}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                self._set_cache("exchange_rates_all", cache_key, data)
                logger.info(f"✅ 获取所有汇率: {base}")
                return data
        except Exception as e:
            logger.error(f"⚠️ 获取汇率失败: {e}")
        
        return None


def main():
    """测试"""
    adapter = FreeDataAdapter()
    
    print("=" * 60)
    print("🌐 免费开源数据适配器测试")
    print("=" * 60)
    
    # 测试汇率
    print("\n💱 汇率测试:")
    rate = adapter.get_exchange_rate("USD", "CNY")
    if rate:
        print(f"   USD/CNY: {rate}")
    
    # 测试贸易数据
    print("\n📊 贸易数据测试:")
    summary = adapter.get_trade_summary("CHN")
    print(f"   国家: {summary['country']}")
    print(f"   出口: {summary['export_value']}")
    print(f"   进口: {summary['import_value']}")
    print(f"   GDP: {summary['gdp']}")
    if summary.get('trade_dependence'):
        print(f"   贸易依存度: {summary['trade_dependence']:.2f}%")
    
    # 测试所有汇率
    print("\n💱 所有汇率测试:")
    rates = adapter.get_all_exchange_rates("USD")
    if rates:
        print(f"   基础货币: {rates['base']}")
        print(f"   日期: {rates['date']}")
        print(f"   可用货币数: {len(rates['rates'])}")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
WMO 气象数据采集器
数据源：World Meteorological Organization
更新频率：每日 07:00
"""

import json
import requests
from datetime import datetime
from pathlib import Path

# WMO API 端点 (免费公开数据)
WMO_API_BASE = "https://api.open-meteo.com/v1/forecast"

# 28 个核心城市坐标
CITIES = {
    "beijing": {"lat": 39.9042, "lon": 116.4074},
    "shanghai": {"lat": 31.2304, "lon": 121.4737},
    "chongqing": {"lat": 29.4316, "lon": 106.9123},
    "shenzhen": {"lat": 22.5431, "lon": 114.0579},
    "guangzhou": {"lat": 23.1291, "lon": 113.2644},
    "chengdu": {"lat": 30.5728, "lon": 104.0668},
    "wuhan": {"lat": 30.5928, "lon": 114.3055},
    "xian": {"lat": 34.3416, "lon": 108.9398},
    "hangzhou": {"lat": 30.2741, "lon": 120.1551},
    "nanjing": {"lat": 32.0603, "lon": 118.7969},
    "new_york": {"lat": 40.7128, "lon": -74.0060},
    "london": {"lat": 51.5074, "lon": -0.1278},
    "tokyo": {"lat": 35.6762, "lon": 139.6503},
    "paris": {"lat": 48.8566, "lon": 2.3522},
    "berlin": {"lat": 52.5200, "lon": 13.4050},
    "moscow": {"lat": 55.7558, "lon": 37.6173},
    "sydney": {"lat": -33.8688, "lon": 151.2093},
    "mumbai": {"lat": 19.0760, "lon": 72.8777},
    "singapore": {"lat": 1.3521, "lon": 103.8198},
    "dubai": {"lat": 25.2048, "lon": 55.2708},
    "hong_kong": {"lat": 22.3193, "lon": 114.1694},
    "taipei": {"lat": 25.0330, "lon": 121.5654},
    "seoul": {"lat": 37.5665, "lon": 126.9780},
    "bangkok": {"lat": 13.7563, "lon": 100.5018},
    "jakarta": {"lat": -6.2088, "lon": 106.8456},
    "manila": {"lat": 14.5995, "lon": 120.9842},
    "kuala_lumpur": {"lat": 3.1390, "lon": 101.6869},
    "hanoi": {"lat": 21.0285, "lon": 105.8542},
}

def fetch_forecast(city_name, coords):
    """获取 7 天天气预报"""
    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
        "timezone": "auto",
        "forecast_days": 7
    }
    
    try:
        response = requests.get(WMO_API_BASE, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        return {
            "city": city_name,
            "coords": coords,
            "fetched_at": datetime.utcnow().isoformat(),
            "daily": data.get("daily", {})
        }
    except Exception as e:
        print(f"Error fetching {city_name}: {e}")
        return None

def collect_all():
    """采集所有城市数据"""
    results = []
    for city_name, coords in CITIES.items():
        print(f"Fetching {city_name}...")
        data = fetch_forecast(city_name, coords)
        if data:
            results.append(data)
    
    # 保存到文件
    output_file = Path(f"daily_forecasts_{datetime.now().strftime('%Y%m%d')}.jsonl")
    with open(output_file, "w") as f:
        for record in results:
            f.write(json.dumps(record) + "\n")
    
    print(f"✅ Saved {len(results)} cities to {output_file}")
    return results

if __name__ == "__main__":
    collect_all()

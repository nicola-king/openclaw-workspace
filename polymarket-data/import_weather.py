#!/usr/bin/env python3
"""
导入 JSONL 气象数据到数据库
"""

import json
from pathlib import Path
from db_connector import save_weather_forecast, get_stats

def import_daily_forecasts():
    """导入每日预报数据"""
    data_dir = Path(__file__).parent / "weather-models"
    jsonl_files = list(data_dir.glob("daily_forecasts_*.jsonl"))
    
    total_records = 0
    for jsonl_file in jsonl_files:
        print(f"导入 {jsonl_file.name}...")
        with open(jsonl_file) as f:
            for line in f:
                record = json.loads(line.strip())
                city = record["city"]
                lat = record["coords"]["lat"]
                lon = record["coords"]["lon"]
                
                count = save_weather_forecast(city, lat, lon, record)
                total_records += count
    
    print(f"✅ 导入完成，共 {total_records} 条记录")
    return total_records

if __name__ == "__main__":
    import_daily_forecasts()
    stats = get_stats()
    print("\n数据库统计:")
    print(json.dumps(stats, indent=2))

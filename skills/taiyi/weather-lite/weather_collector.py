#!/usr/bin/env python3
"""
weather-lite - 气象数据采集（免费版）
自动采集单城市气象数据，推送到微信/Telegram

用法：
    python3 weather_collector.py --city Beijing
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path

class WeatherCollector:
    """简易气象数据采集器"""
    
    def __init__(self, city="Beijing"):
        self.city = city
        self.data_dir = Path("~/polymarket-data/weather").expanduser()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Open-Meteo API（免费，无需 key）
        self.api_base = "https://api.open-meteo.com/v1/forecast"
        
    def get_coordinates(self):
        """获取城市坐标（简化版，预定义）"""
        cities = {
            "Beijing": (39.9042, 116.4074),
            "Shanghai": (31.2304, 121.4737),
            "Guangzhou": (23.1291, 113.2644),
            "Shenzhen": (22.5431, 114.0579),
            "Chengdu": (30.5728, 104.0668),
            "Chongqing": (29.4316, 106.9123),
        }
        return cities.get(self.city, (39.9042, 116.4074))
    
    def fetch_weather(self):
        """获取气象数据"""
        lat, lon = self.get_coordinates()
        
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code",
            "hourly": "temperature_2m,precipitation_probability",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "Asia/Shanghai",
            "forecast_days": 7
        }
        
        response = requests.get(self.api_base, params=params)
        data = response.json()
        
        return {
            "city": self.city,
            "timestamp": datetime.now().isoformat(),
            "current": data.get("current", {}),
            "hourly": data.get("hourly", {}),
            "daily": data.get("daily", {}),
            "raw": data
        }
    
    def save_data(self, weather_data):
        """保存数据到本地"""
        date = datetime.now().strftime("%Y-%m-%d")
        file_path = self.data_dir / f"{self.city}_{date}.json"
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(weather_data, f, indent=2, ensure_ascii=False)
        
        return file_path
    
    def generate_report(self, weather_data):
        """生成简易报告"""
        current = weather_data.get("current", {})
        daily = weather_data.get("daily", {})
        
        report = f"""
【气象日报 · {self.city}】{datetime.now().strftime("%Y-%m-%d")}

当前天气：
温度：{current.get("temperature_2m", "N/A")}°C
湿度：{current.get("relative_humidity_2m", "N/A")}%
降水：{current.get("precipitation", "N/A")}mm

今日预报：
最高温：{daily.get("temperature_2m_max", ["N/A"])[0]}°C
最低温：{daily.get("temperature_2m_min", ["N/A"])[0]}°C
降水总量：{daily.get("precipitation_sum", ["N/A"])[0]}mm

数据来源：Open-Meteo（免费 API）
采集时间：{weather_data.get("timestamp", "N/A")}
"""
        return report.strip()
    
    def run(self):
        """主执行流程"""
        print(f"[{datetime.now()}] 开始采集 {self.city} 气象数据...")
        
        # 获取数据
        weather_data = self.fetch_weather()
        
        # 保存数据
        file_path = self.save_data(weather_data)
        print(f"✓ 数据已保存：{file_path}")
        
        # 生成报告
        report = self.generate_report(weather_data)
        print("\n" + report)
        
        return weather_data

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="气象数据采集器")
    parser.add_argument("--city", default="Beijing", help="城市名称")
    
    args = parser.parse_args()
    
    collector = WeatherCollector(args.city)
    collector.run()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
气象数据样本（189 条记录）
用于 TurboQuant v2.0 压缩算法集成测试
"""

import json
from datetime import datetime, timedelta
import random

def generate_meteorological_data(num_records=189):
    """
    生成气象数据样本
    
    字段说明：
    - timestamp: 时间戳
    - temperature: 温度 (°C)
    - humidity: 湿度 (%)
    - pressure: 气压 (hPa)
    - wind_speed: 风速 (m/s)
    - wind_direction: 风向 (度)
    - precipitation: 降水量 (mm)
    - cloud_cover: 云量 (%)
    - visibility: 能见度 (km)
    - uv_index: 紫外线指数
    """
    
    base_time = datetime(2026, 1, 1, 0, 0, 0)
    data = []
    
    # 重庆气象参数范围
    temp_range = (2, 42)  # °C
    humidity_range = (40, 95)  # %
    pressure_range = (980, 1040)  # hPa
    wind_speed_range = (0, 20)  # m/s
    
    for i in range(num_records):
        timestamp = base_time + timedelta(hours=i * 6)  # 每 6 小时一条
        
        # 生成随机但合理的气象数据
        record = {
            'timestamp': timestamp.isoformat(),
            'temperature': round(random.uniform(*temp_range), 1),
            'humidity': round(random.uniform(*humidity_range), 1),
            'pressure': round(random.uniform(*pressure_range), 1),
            'wind_speed': round(random.uniform(*wind_speed_range), 2),
            'wind_direction': round(random.uniform(0, 360), 1),
            'precipitation': round(random.uniform(0, 50), 2),
            'cloud_cover': round(random.uniform(0, 100), 1),
            'visibility': round(random.uniform(1, 20), 2),
            'uv_index': round(random.uniform(0, 11), 1),
        }
        
        data.append(record)
    
    return data


if __name__ == '__main__':
    print("生成 189 条气象数据...")
    data = generate_meteorological_data(189)
    
    # 保存为 JSON
    output_file = 'meteorological_data_189.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 统计信息
    import os
    file_size = os.path.getsize(output_file)
    
    print(f"✅ 生成完成：{output_file}")
    print(f"   记录数：{len(data)}")
    print(f"   文件大小：{file_size:,} 字节 ({file_size/1024:.2f} KB)")
    print(f"   平均每记录：{file_size/len(data):.1f} 字节")
    
    # 显示前 3 条样本
    print(f"\n📊 数据样本:")
    for i, record in enumerate(data[:3]):
        print(f"\n记录 {i+1}:")
        print(f"  时间：{record['timestamp']}")
        print(f"  温度：{record['temperature']}°C")
        print(f"  湿度：{record['humidity']}%")
        print(f"  气压：{record['pressure']} hPa")

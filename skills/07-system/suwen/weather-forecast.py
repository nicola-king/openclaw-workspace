#!/usr/bin/env python3
"""
天气预报
太一 AGI · 2026-04-15

功能：
- 调用 wttr.in 获取天气
- 生成天气预报记录
- 写入报告文件
"""

from pathlib import Path
from datetime import datetime
import subprocess
import json

def get_weather(location="Shanghai"):
    """获取天气数据"""
    try:
        # 使用 wttr.in 获取 JSON 格式天气
        result = subprocess.run(
            ["curl", "-s", f"wttr.in/{location}?format=j1"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"  ⚠️  天气获取失败：{e}")
    return None

def main():
    workspace = Path("/home/nicola/.openclaw/workspace")
    logs_dir = workspace / "logs" / "weather-forecast"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    location = "Shanghai"  # 上海
    
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🌤️ 开始天气预报...")
    print(f"  📍 地点：{location}")
    
    # 获取天气数据
    weather_data = get_weather(location)
    
    if weather_data and "current_condition" in weather_data:
        current = weather_data["current_condition"][0]
        weather_desc = current.get("weatherDesc", [{}])[0].get("value", "未知")
        temp_c = current.get("temp_C", "未知")
        feels_like = current.get("FeelsLikeC", "未知")
        humidity = current.get("humidity", "未知")
        wind_speed = current.get("windspeedKmph", "未知")
        
        print(f"  🌡️  当前温度：{temp_c}°C (体感 {feels_like}°C)")
        print(f"  ☁️  天气：{weather_desc}")
        print(f"  💧  湿度：{humidity}%")
        print(f"  💨  风速：{wind_speed} km/h")
        
        # 生成天气预报
        forecast_content = f"""# 天气预报 · {today}

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📍 地点

{location} (上海)

---

## 🌡️  当前天气

| 指标 | 数值 |
|------|------|
| 温度 | {temp_c}°C |
| 体感 | {feels_like}°C |
| 天气 | {weather_desc} |
| 湿度 | {humidity}% |
| 风速 | {wind_speed} km/h |

---

## 💡 生活建议

"""
        # 根据天气给出建议
        try:
            temp = int(temp_c)
            if temp < 10:
                forecast_content += "- 🧥 天气较冷，注意保暖\n"
            elif temp < 20:
                forecast_content += "- 👕 天气凉爽，建议穿长袖\n"
            elif temp < 30:
                forecast_content += "- 👔 天气舒适，正常着装\n"
            else:
                forecast_content += "- 🌞 天气炎热，注意防暑\n"
            
            if int(humidity) > 80:
                forecast_content += "- ☔ 湿度较高，可能下雨，建议带伞\n"
        except:
            forecast_content += "- 请参考实际天气情况安排出行\n"
        
        forecast_content += f"""
---

*数据来源：wttr.in · 太一 AGI 天气预报*
"""
        
        # 写入预报文件
        reports_dir = workspace / "reports" / "weather"
        reports_dir.mkdir(parents=True, exist_ok=True)
        forecast_file = reports_dir / f"weather-{today}.md"
        forecast_file.write_text(forecast_content, encoding='utf-8')
        print(f"  ✅ 天气预报已创建：{forecast_file}")
    else:
        print(f"  ⚠️  无法获取天气数据，创建空报告")
        # 创建空报告
        reports_dir = workspace / "reports" / "weather"
        reports_dir.mkdir(parents=True, exist_ok=True)
        forecast_file = reports_dir / f"weather-{today}.md"
        forecast_file.write_text(f"# 天气预报 · {today}\n\n⚠️  无法获取天气数据\n", encoding='utf-8')
    
    print(f"\n✅ 天气预报完成！")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

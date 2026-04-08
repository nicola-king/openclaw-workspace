---
name: weather
version: 1.0.0
description: 天气预报 - 实时天气/ forecasts (wttr.in/Open-Meteo)
category: data
tags: ['weather', 'forecast', 'wttr', 'open-meteo']
author: 太一 AGI
created: 2026-04-07
---


# Weather - 天气预测技能

> 版本：v1.0 | 创建：2026-04-03 | 负责 Bot：素问

---

## 🎯 职责

**天气预报采集**，使用 wttr.in 或 Open-Meteo API

---

## 🔧 使用命令

```bash
# 查看天气
python3 weather-forecast.py --location <城市>

# 定时采集 (Cron 每小时)
./skills/suwen/weather-forecast.sh
```

---

## 📁 位置

**系统自带**: `~/.npm-global/lib/node_modules/openclaw/skills/weather/`

---

## 📊 输出格式

天气数据存入 `memory/weather/` 目录

---

## 🔗 相关文档

- `skills/suwen/weather-forecast.sh` - 天气采集脚本
- `constitution/guarantees/CRON-GUARANTEE.md` - Cron 配置

---

*创建：2026-04-03 22:57 | 太一 AGI*

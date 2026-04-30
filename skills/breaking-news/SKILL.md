---
description: 突发新闻实时监测，支持 AI/时事/热点/经济/中国政经等多领域关键词监测，自动推送 P0/P1 级突发新闻到 Telegram
---

# 突发新闻实时监测

## 功能
实时监测全球新闻，自动识别紧急程度（P0-P3），推送重要新闻到 Telegram

## 配置
- 监测脚本: `scripts/breaking-news-monitor.py`
- 触发脚本: `scripts/breaking-news-trigger.sh`
- 输出目录: `news/breaking/`
- 推送目标: Telegram Chat 7073481596
- 监测级别: P0 战争/地震/核爆 → P3 快讯/突发

## 依赖
- Python 3
- requests

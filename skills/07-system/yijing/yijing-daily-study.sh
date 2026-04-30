#!/bin/bash
DATE=$(date "+%Y-%m-%d")
mkdir -p /home/nicola/.openclaw/workspace/content/yijing/daily-notes
echo "# 易经学习笔记 $DATE" > /home/nicola/.openclaw/workspace/content/yijing/daily-notes/$DATE.md
echo "## Day 1/120 乾为天" >> /home/nicola/.openclaw/workspace/content/yijing/daily-notes/$DATE.md
curl -s -X POST "https://api.telegram.org/bot8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY/sendMessage" -d "chat_id=7073481596&text=🔮 易经学习 Day 1

卦象：乾为天

#易经" > /dev/null
echo "✅ 完成"

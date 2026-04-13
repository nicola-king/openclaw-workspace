#!/bin/bash
DATE=$(date "+%Y-%m-%d")
echo "[INFO] 先秦文化学习启动"
mkdir -p /home/nicola/.openclaw/workspace/content/xianqin/daily-notes
cat > "/home/nicola/.openclaw/workspace/content/xianqin/daily-notes/$DATE.md" << NOTE
# 学习笔记 $DATE

## 主题：诸子百家
## 内容：10 家思想概览

### 核心概念
- 儒家：仁义礼智信
- 道家：道法自然
- 法家：以法治国

### 金句
> 己所不欲，勿施于人
> 上善若水

*太一 AGI*
NOTE
curl -s -X POST "https://api.telegram.org/bot8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY/sendMessage" -d "chat_id=7073481596&text=📚 先秦文化学习

主题：诸子百家
内容：10 家思想概览

#先秦文化" > /dev/null
echo "[INFO] ✅ 完成"

#!/bin/bash
# 易经 64 卦每日学习推送

DATE=$(date "+%Y-%m-%d")
DAY_OF_PLAN=1

echo "[INFO] 易经 64 卦学习 Day $DAY_OF_PLAN/120"

mkdir -p /home/nicola/.openclaw/workspace/content/yijing/daily-notes

cat > "/home/nicola/.openclaw/workspace/content/yijing/daily-notes/$DATE.md" << NOTE
# 易经学习笔记 $DATE

## Day $DAY_OF_PLAN/120

### 今日卦象
乾为天 (第 1 卦)

### 卦辞
元亨利贞

### 象传
天行健，君子以自强不息

### 六爻
- 初九：潜龙勿用
- 九二：见龙在田
- 九三：君子终日乾乾
- 九四：或跃在渊
- 九五：飞龙在天
- 上九：亢龙有悔

### 现代解读
现在是积蓄力量的时候，不要急于行动

### 应用建议
1. 职场：努力工作，等待机会
2. 创业：积累资源，不要冒进
3. 感情：真诚相待，顺其自然

*太一 AGI*
NOTE

curl -s -X POST "https://api.telegram.org/bot8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY/sendMessage" \
  -d "chat_id=7073481596" \
  -d "text=🔮 易经 64 卦学习 Day $DAY_OF_PLAN

今日卦象：乾为天

卦辞：元亨利贞

象曰：天行健，君子以自强不息

进度：$DAY_OF_PLAN/120 天

#易经 #学习打卡" > /dev/null

echo "[INFO] ✅ 易经学习推送完成"
echo "[$DATE] Day $DAY_OF_PLAN: 乾为天" >> /home/nicola/.openclaw/workspace/logs/yijing-study.log

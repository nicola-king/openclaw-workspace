# 先秦文化智能自动化学习时间表

> 创建时间：2026-03-29 14:49
> 总周期：90 天
> 自动化：AI 辅助 + 定时任务 + 内容自动生成

---

## 📊 学习时间表 (90 天)

### Phase 1: 基础脉络 (Day 1-30)

| 周数 | 天数 | 主题 | 学习内容 | 产出 |
|------|------|------|---------|------|
| **W1** | D1-7 | 历史分期 | 夏商周春秋战国 | 时间轴图谱 |
| **W2** | D8-14 | 诸子百家概览 | 10 家思想卡片 | 百家思维导图 |
| **W3** | D15-21 | 儒家精读 | 《论语》20 篇 | 20 篇笔记 |
| **W4** | D22-30 | 道家精读 | 《道德经》81 章 | 81 章解读 |

### Phase 2: 经典深入 (Day 31-60)

| 周数 | 天数 | 主题 | 学习内容 | 产出 |
|------|------|------|---------|------|
| **W5** | D31-37 | 兵家精读 | 《孙子兵法》13 篇 | 13 篇案例 |
| **W6** | D38-44 | 法家精读 | 《韩非子》精选 | 法家智慧卡 |
| **W7** | D45-51 | 墨家/纵横家 | 《墨子》《战国策》 | 对比分析 |
| **W8** | D52-60 | 其他百家 | 名家/阴阳家/农家 | 知识补充 |

### Phase 3: 实践应用 (Day 61-90)

| 周数 | 天数 | 主题 | 学习内容 | 产出 |
|------|------|------|---------|------|
| **W9** | D61-67 | 商业案例 | 5 个古代智慧应用 | 案例分析 |
| **W10** | D68-74 | 内容创作 | 10 篇小红书笔记 | 多平台分发 |
| **W11** | D75-81 | 知识图谱 | Neo4j 图谱构建 | 数字化资产 |
| **W12** | D82-90 | 复盘总结 | 90 天学习报告 | 完整体系 |

---

## 🤖 智能自动化学习流程

### 每日自动化任务

```
07:00 → 推送今日学习内容 (Telegram/微信)
09:00 → AI 解读昨日内容 (生成笔记)
12:00 → 推送金句卡片 (小红书/朋友圈)
18:00 → 学习进度检查 (提醒未完成)
23:00 → 内容提炼归档 (知识库更新)
```

### 每周自动化任务

```
周一 09:00 → 本周学习计划生成
周五 18:00 → 本周学习总结
周日 20:00 → 内容创作 (1 篇公众号)
```

---

## 🔧 自动化脚本配置

### 1. 每日学习推送脚本

```bash
# skills/suwen/xianqin-daily-study.sh
# 功能：每日推送学习内容 + AI 解读

#!/bin/bash

DATE=$(date +%Y-%m-%d)
DAY_OF_PLAN=$(( ($(date +%s - "$DATE") - $(date +%s - "2026-03-29") ) / 86400 + 1 ))

# 根据天数确定学习内容
if [ $DAY_OF_PLAN -le 7 ]; then
    TOPIC="历史分期"
    CONTENT="夏商周历史脉络"
elif [ $DAY_OF_PLAN -le 14 ]; then
    TOPIC="诸子百家"
    CONTENT="10 家思想概览"
elif [ $DAY_OF_PLAN -le 21 ]; then
    TOPIC="儒家"
    CONTENT="论语篇"
elif [ $DAY_OF_PLAN -le 30 ]; then
    TOPIC="道家"
    CONTENT="道德经篇"
# ... 继续扩展

# 调用 AI 生成解读
python3 /home/nicola/.openclaw/workspace/skills/suwen/ai-study-interpreter.py \
    --topic "$TOPIC" \
    --content "$CONTENT" \
    --output "/home/nicola/.openclaw/workspace/content/xianqin/daily-notes/$DATE.md"

# 发送 Telegram 通知
curl -X POST "https://api.telegram.org/bot8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY/sendMessage" \
    -d "chat_id=7073481596" \
    -d "text=📚 先秦文化学习 Day $DAY_OF_PLAN

主题：$TOPIC
内容：$CONTENT

进度：$DAY_OF_PLAN/90 天"

echo "[$DATE] 学习推送完成"
```

---

### 2. AI 内容解读脚本

```python
# skills/suwen/ai-study-interpreter.py
# 功能：AI 解读学习内容 + 生成笔记

import sys
import argparse
from datetime import datetime

def interpret_topic(topic, content):
    """AI 解读学习内容"""
    
    # 调用本地 AI 或云端 AI
    prompt = f"""
    请解读先秦文化内容:
    
    主题：{topic}
    内容：{content}
    
    输出格式:
    1. 核心概念 (3-5 个)
    2. 现代解读 (200 字)
    3. 应用建议 (3 条)
    4. 金句摘录 (2-3 句)
    """
    
    # 调用 AI (smart-ai-router)
    # response = call_ai(prompt)
    
    return {
        'concepts': ['概念 1', '概念 2', '概念 3'],
        'interpretation': '现代解读文本...',
        'applications': ['应用 1', '应用 2', '应用 3'],
        'quotes': ['金句 1', '金句 2']
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', required=True)
    parser.add_argument('--content', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    
    result = interpret_topic(args.topic, args.content)
    
    # 保存笔记
    with open(args.output, 'w') as f:
        f.write(f"# 学习笔记 {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(f"## 核心概念\n")
        for c in result['concepts']:
            f.write(f"- {c}\n")
        f.write(f"\n## 现代解读\n{result['interpretation']}\n")
        f.write(f"\n## 应用建议\n")
        for a in result['applications']:
            f.write(f"- {a}\n")
        f.write(f"\n## 金句摘录\n")
        for q in result['quotes']:
            f.write(f"> {q}\n")
    
    print(f"✅ 笔记已保存：{args.output}")

if __name__ == '__main__':
    main()
```

---

### 3. 内容提炼脚本

```python
# skills/shanmu/xianqin-content-generator.py
# 功能：从学习内容提炼小红书/公众号内容

def generate_xiaohongshu_post(note_path):
    """生成小红书笔记"""
    
    # 读取学习笔记
    with open(note_path, 'r') as f:
        content = f.read()
    
    # AI 提炼 (调用 smart-ai-router)
    prompt = f"""
    请将以下学习笔记转化为小红书笔记:
    
    {content}
    
    要求:
    - 标题：吸引眼球 (20 字内)
    - 正文：800-1000 字
    - 标签：5-10 个
    - emoji：适当使用
    """
    
    # 生成内容
    # response = call_ai(prompt)
    
    return {
        'title': '标题',
        'content': '正文',
        'tags': ['#标签 1', '#标签 2'],
        'image_prompt': 'AI 生图提示词'
    }

def generate_wechat_article(note_path):
    """生成公众号文章"""
    
    # 类似小红书生成，但更长 (2000-3000 字)
    pass
```

---

## ⏰ 定时任务配置

### Crontab 配置

```bash
# 编辑 crontab
crontab -e

# 添加以下任务:

# 每日学习推送 (07:00)
0 7 * * * /home/nicola/.openclaw/workspace/skills/suwen/xianqin-daily-study.sh >> /home/nicola/.openclaw/workspace/logs/xianqin-study.log 2>&1

# AI 内容解读 (09:00)
0 9 * * * python3 /home/nicola/.openclaw/workspace/skills/suwen/ai-study-interpreter.py --topic "auto" --content "auto" --output "/home/nicola/.openclaw/workspace/content/xianqin/daily-notes/$(date +\%Y-\%m-\%d).md" >> /home/nicola/.openclaw/workspace/logs/xianqin-ai.log 2>&1

# 金句推送 (12:00)
0 12 * * * python3 /home/nicola/.openclaw/workspace/skills/shanmu/daily-quote-sender.py >> /home/nicola/.openclaw/workspace/logs/xianqin-quote.log 2>&1

# 学习进度检查 (18:00)
0 18 * * * python3 /home/nicola/.openclaw/workspace/skills/suwen/study-progress-check.py >> /home/nicola/.openclaw/workspace/logs/xianqin-progress.log 2>&1

# 内容提炼归档 (23:00)
0 23 * * * python3 /home/nicola/.openclaw/workspace/skills/shanmu/xianqin-content-generator.py >> /home/nicola/.openclaw/workspace/logs/xianqin-content.log 2>&1

# 周一：本周学习计划 (09:00)
0 9 * * 1 python3 /home/nicola/.openclaw/workspace/skills/suwen/weekly-plan-generator.py >> /home/nicola/.openclaw/workspace/logs/xianqin-weekly.log 2>&1

# 周五：本周学习总结 (18:00)
0 18 * * 5 python3 /home/nicola/.openclaw/workspace/skills/suwen/weekly-summary-generator.py >> /home/nicola/.openclaw/workspace/logs/xianqin-weekly.log 2>&1

# 周日：公众号文章生成 (20:00)
0 20 * * 0 python3 /home/nicola/.openclaw/workspace/skills/shanmu/wechat-article-generator.py >> /home/nicola/.openclaw/workspace/logs/xianqin-wechat.log 2>&1
```

---

## 📊 内容融入流程

### 知识库更新流程

```
学习笔记 → AI 提炼 → 标签分类 → 知识图谱 → 多平台分发
    ↓         ↓         ↓         ↓         ↓
daily/   核心概念  儒家/道家  Neo4j   小红书/公众号
```

### 内容创作矩阵

| 平台 | 频率 | 内容类型 | 自动化 |
|------|------|---------|--------|
| **小红书** | 每日 1 篇 | 金句卡片/知识点 | ✅ 自动生成 |
| **公众号** | 每周 1 篇 | 深度解读 | ✅ AI 辅助 |
| **视频号** | 每周 2 条 | 短视频脚本 | ✅ AI 生成 |
| **Telegram** | 每日推送 | 学习进度 | ✅ 自动发送 |

---

## 🎯 预期成果 (90 天)

| 指标 | 目标 | 衡量方式 |
|------|------|---------|
| 学习内容 | 90 天完整覆盖 | 学习笔记 90 篇 |
| AI 解读 | 每日自动 | 解读笔记 90 篇 |
| 小红书 | 每日 1 篇 | 发布 90 篇 |
| 公众号 | 每周 1 篇 | 发布 12 篇 |
| 知识图谱 | 完整构建 | Neo4j 图谱 |
| 粉丝增长 | 10K+ | 全平台统计 |

---

## 📁 文件结构

```
/home/nicola/.openclaw/workspace/content/xianqin/
├── daily-notes/          # 每日学习笔记
│   ├── 2026-03-29.md
│   ├── 2026-03-30.md
│   └── ...
├── weekly-summaries/     # 每周总结
│   ├── week-01.md
│   └── ...
├── content-drafts/       # 内容草稿
│   ├── xiaohongshu/
│   └── wechat/
└── knowledge-graph/      # 知识图谱
    └── xianqin-neo4j.json
```

---

*创建时间：2026-03-29 14:49*
*太一 AGI · 先秦文化智能自动化学习*

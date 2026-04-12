---
name: geo-automation
version: 1.0.0
description: geo-automation skill
category: browser
tags: []
author: 太一 AGI
created: 2026-04-07
---


# GEO 自动化工作流

> 版本：v1.0 | 创建：2026-04-05 | 职责：GEO 内容生成与发布

---

## 🎯 职责

**GEO (Generative Engine Optimization) 内容自动化**

- 问题库生成
- 内容批量创作
- 多平台发布
- SEO 优化集成

---

## 🔧 使用命令

```bash
# 生成问题
python3 /home/nicola/.openclaw/workspace/scripts/geo-question-generator.py

# 生成内容
python3 /home/nicola/.openclaw/workspace/scripts/geo-content-generator.py

# 发布内容
python3 /home/nicola/.openclaw/workspace/scripts/geo-publisher.py
```

---

## 📁 目录结构

| 目录/文件 | 说明 |
|----------|------|
| `geo-questions/` | 问题库（90+ 问题） |
| `geo-content/` | 生成内容（30+ 篇） |
| `geo-published/` | 多平台发布文件 |
| `README.md` | 详细文档 |
| `SKILL.yml` | 技能元数据 |

---

## 📊 输出格式

- 问题库：Markdown 列表
- 内容：多平台格式（知乎/公众号/小红书）
- 发布：自动分发到配置的平台

---

## 🔗 相关 Skills

| Skill | 用途 |
|-------|------|
| geo-seo-optimizer | GEO+SEO 优化 |
| content-scheduler | 内容定时发布 |
| social-publisher | 多平台发布 |
| social-media-scheduler | 社交媒体调度 |

---

## 📋 Cron 配置

| 时间 | 任务 |
|------|------|
| 10:00 | 生成问题 |
| 14:00 | 生成发布文件 |

---

*创建：2026-04-06 09:14 | 素问健康检查自动修复*

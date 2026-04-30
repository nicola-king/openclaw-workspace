---
name: shanmu
version: 1.0.0
description: 山木 - 内容创意与文案生成
category: content
tags: ['shanmu', 'content', 'creative']
author: 太一 AGI
created: 2026-04-07
---


# Shanmu - 山木内容创意 Bot

> 版本：v1.0 | 创建：2026-04-03 | 负责 Bot：山木

---

## 🎯 职责

**内容创意生成**，包括文章/帖子/视频脚本/创意素材

---

## 🔧 使用命令

```bash
# 生成文章
python3 shanmu-generator.py --type article --topic <主题>

# 生成视频脚本
python3 shanmu-generator.py --type video-script --topic <主题>

# 生成小红书帖子
python3 shanmu-generator.py --type xiaohongshu --topic <主题>
```

---

## 📁 目录结构

| 目录/文件 | 说明 |
|----------|------|
| `accounts/` | 账号配置 |
| `ai-drama-workflow.md` | AI 短剧工作流 |
| `generators/` | 内容生成器 |
| `templates/` | 内容模板 |

---

## 📊 输出格式

内容输出到 `memory/shanmu/` 目录

---

## 🔗 相关文档

- `constitution/workflows/CONTENT-CREATION.md` - 内容创作工作流

---

*创建：2026-04-03 22:57 | 太一 AGI*

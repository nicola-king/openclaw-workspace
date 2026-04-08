---
name: web
version: 1.0.0
description: web skill
category: tools
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Web - 网页自动化技能

> 版本：v1.0 | 创建：2026-04-03 | 负责 Bot：素问

---

## 🎯 职责

**网页自动化操作**，使用 Playwright 进行浏览器控制

---

## 🔧 使用命令

```bash
# 网页截图
python3 web-automation.py --screenshot <URL>

# 网页内容提取
python3 web-automation.py --extract <URL>

# 表单填写
python3 web-automation.py --form <URL> --data <JSON>
```

---

## 📁 位置

**系统自带**: `~/.npm-global/lib/node_modules/openclaw/skills/web/`

---

## 🔗 相关文档

- `skills/browser-automation/SKILL.md` - 浏览器自动化技能
- `scripts/playwright-browser.py` - Playwright 脚本

---

*创建：2026-04-03 22:57 | 太一 AGI*

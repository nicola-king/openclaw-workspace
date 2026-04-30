---
title: 微信友好 Markdown 格式规范
author: 太一 AGI
date: 2026-04-18
type: doc
tags: ['规范', '文档', '微信', 'Markdown']
---

# 📱 微信友好 Markdown 格式规范

> **版本**: 1.0  
> **生效时间**: 2026-04-18  
> **适用范围**: 所有发送到微信的 Markdown 文件

---

## 🎯 核心要求

### 1. 必须包含 Front Matter

所有 Markdown 文件必须在开头添加 YAML 格式的元数据：

```yaml
---
title: 文档标题
author: 太一 AGI
date: 2026-04-18
type: report
tags: ['标签 1', '标签 2']
---
```

### 2. 标准字段说明

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `title` | ✅ | 文档标题 | `Telegram 路由修复报告` |
| `author` | ✅ | 作者 | `太一 AGI` |
| `date` | ✅ | 日期 | `2026-04-18` |
| `type` | ✅ | 类型 | `report` / `skill` / `doc` |
| `tags` | ✅ | 标签列表 | `['修复', '路由']` |

### 3. 文档类型 (type)

| 类型 | 用途 | 示例 |
|------|------|------|
| `report` | 各类报告 | 修复报告、检查报告 |
| `skill` | 技能文档 | SKILL.md |
| `doc` | 说明文档 | 规范、指南 |
| `note` | 笔记 | 学习记录、会议纪要 |

---

## 📄 标准模板

### 报告类

```markdown
---
title: 报告标题
author: 太一 AGI
date: 2026-04-18
type: report
tags: ['标签 1', '标签 2']
---

# 📊 报告标题

> **时间**: 2026-04-18  
> **状态**: ✅ 完成

---

## 🎯 核心摘要

简洁的摘要内容

---

## 📋 详细内容

### 小标题

内容...

---

*太一 AGI · 2026-04-18*
```

### Skill 类

```markdown
---
name: skill-name
version: 1.0.0
description: 技能描述
category: 分类
tags: ['标签 1', '标签 2']
author: 太一 AGI
created: 2026-04-18
status: active
---

# 🎯 技能名称

> **状态**: ✅ 活跃 | **版本**: 1.0.0

---

## 功能说明

...

---

*版本：1.0.0 | 创建时间：2026-04-18*
```

---

## 🔧 自动化工具

### 使用脚本添加 Front Matter

```bash
# 基础用法
python3 scripts/add-frontmatter.py <文件路径> [标题] [标签...]

# 示例
python3 scripts/add-frontmatter.py reports/test.md "测试报告" 修复 测试
```

### 脚本自动检测

- 如果文件已有 Front Matter → 跳过
- 如果文件不存在 → 报错
- 成功添加 → 显示确认信息

---

## ✅ 格式检查清单

发布前检查：

- [ ] 包含 YAML 头部 (Front Matter)
- [ ] UTF-8 编码 (无 BOM)
- [ ] 标题简洁 (< 30 字符)
- [ ] 表格适配手机屏幕
- [ ] 代码块 < 20 行
- [ ] 使用 Emoji 增强可读性
- [ ] 文件 < 500 行

---

## 📱 微信优化技巧

### 1. 使用 Emoji

```markdown
✅ 完成  ❌ 失败  ⚠️ 警告  
📊 数据  🔍 检查  🎯 目标
```

### 2. 简洁表格

```markdown
| 项目 | 状态 | 说明 |
|------|------|------|
| 短内容 | ✅ | 简洁描述 |
```

### 3. 短代码块

```markdown
简短的代码示例
```

### 4. 清晰的分隔线

```markdown
---

章节之间用分隔线
```

---

## 🚫 避免的格式

### ❌ 过宽的表格

```markdown
| 非常长的列名 1 | 非常长的列名 2 | 非常长的列名 3 |
|---------------|---------------|---------------|
| 内容... |
```

### ❌ 嵌套过深的列表

```markdown
- 第一层
  - 第二层
    - 第三层
      - 第四层 ❌ 避免
```

### ❌ 超长代码块

```markdown
# 避免超过 20 行的代码块
# 如需展示长代码，建议分段
```

---

## 📚 示例文件

### 已修复的报告

1. `reports/telegram-routing-fix-20260418.md` ✅
2. `reports/communication-channels-check-20260418.md` ✅
3. `reports/timed-tasks-fix-20260418.md` ✅

### 参考 Skill

- `skills/07-system/geo-model-router/SKILL.md` ✅

---

## 🔗 相关文件

| 文件 | 用途 |
|------|------|
| `docs/WECHAT-MD-FORMAT.md` | 详细格式指南 |
| `scripts/add-frontmatter.py` | 自动添加工具 |
| `reports/WECHAT-MD-STANDARD.md` | 本文档 |

---

## 📝 执行记录

| 时间 | 操作 | 状态 |
|------|------|------|
| 2026-04-18 08:11 | 创建规范文档 | ✅ |
| 2026-04-18 08:11 | 修复历史报告 | ✅ |
| 2026-04-18 08:11 | 创建自动化工具 | ✅ |

---

*太一 AGI · 文档规范 v1.0 · 2026-04-18*

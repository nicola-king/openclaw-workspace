---
name: notebooklm-integration
version: 1.0.0
description: Google NotebookLM 集成 - 笔记/研究/知识库自动化
category: integration
tags: ['google', 'notebooklm', 'notes', 'research', 'knowledge', 'ai']
author: 太一 AGI
created: 2026-04-08
updated: 2026-04-08
status: active
priority: P2
---

# NotebookLM 集成技能

> **版本**: 1.0.0 | **创建**: 2026-04-08  
> **负责**: 太一 | **状态**: ✅ 已激活

---

## 🎯 功能

- ✅ 创建知识库 (Notebook)
- ✅ 添加文档源 (Source)
- ✅ 自动生成摘要
- ✅ AI 问答
- ✅ 导出笔记
- ✅ 网页自动化 (主要方案)

---

## 🔧 配置

NotebookLM 目前**无官方 API**，使用网页自动化方案：

### 配置 Google 账号

编辑 `~/.openclaw/workspace-taiyi/config/google-integration.json`:

```json
{
  "notebooklm": {
    "enabled": true,
    "autoImport": true,
    "knowledgeBaseId": "",
    "authMethod": "browser",
    "browserProfile": "~/.config/google-chrome"
  }
}
```

---

## 📋 命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `notebooklm create` | 创建知识库 | `notebooklm create "研究项目"` |
| `notebooklm add-source` | 添加文档 | `notebooklm add-source "笔记内容"` |
| `notebooklm summarize` | 生成摘要 | `notebooklm summarize` |
| `notebooklm ask` | AI 问答 | `notebooklm ask "主要观点是什么"` |
| `notebooklm export` | 导出笔记 | `notebooklm export --format markdown` |

---

## 🚀 使用示例

### 创建知识库
```bash
太一，创建一个 NotebookLM 知识库 "AI 研究笔记"
```

### 添加文档源
```bash
太一，在 NotebookLM 中添加文档：[文档内容]
```

### AI 问答
```bash
太一，问 NotebookLM 这个文档的主要观点是什么
```

### 生成摘要
```bash
太一，总结 NotebookLM 知识库的内容
```

---

## 🔗 相关文件

- `skills/browser-automation/google-services-automation.py` - Google 服务自动化
- `workspace-taiyi/config/google-integration.json` - Google 集成配置

---

*创建：2026-04-08 | 太一 AGI*

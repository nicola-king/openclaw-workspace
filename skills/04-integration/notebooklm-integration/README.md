# NotebookLM 集成 - 快速入门

## 📦 安装完成

✅ 技能文件已创建  
✅ CLI 工具已安装  
✅ 配置已启用

---

## 🌐 使用方式

**NotebookLM 无官方 API**，使用网页自动化方案：

### 前置要求

1. **Google 账号**: 已登录 NotebookLM
2. **Playwright**: 已安装
3. **Chrome 浏览器**: 已安装并登录

---

## 🚀 快速开始

### 方式 1: CLI 命令

```bash
# 创建知识库
python3 skills/notebooklm-integration/notebooklm.py create "AI 研究笔记"

# 添加文档源
python3 skills/notebooklm-integration/notebooklm.py add-source NOTEBOOK_ID \
  --title "文档标题" \
  --content "文档内容..."

# 生成摘要
python3 skills/notebooklm-integration/notebooklm.py summarize NOTEBOOK_ID

# AI 问答
python3 skills/notebooklm-integration/notebooklm.py ask NOTEBOOK_ID \
  --question "主要观点是什么？"

# 导出笔记
python3 skills/notebooklm-integration/notebooklm.py export NOTEBOOK_ID --format markdown
```

### 方式 2: 直接对话

```
太一，在 NotebookLM 创建一个知识库 "项目研究"
太一，添加文档到 NotebookLM
太一，总结 NotebookLM 知识库的内容
太一，问 NotebookLM 这个文档的主要观点
```

---

## 📋 可用功能

| 功能 | 命令 | 说明 |
|------|------|------|
| **创建知识库** | `create` | 新建 Notebook |
| **添加文档** | `add-source` | 添加文本/PDF/链接 |
| **生成摘要** | `summarize` | AI 自动总结 |
| **AI 问答** | `ask` | 基于文档问答 |
| **导出笔记** | `export` | Markdown/PDF/TXT |

---

## 🔧 配置

编辑 `~/.openclaw/workspace-taiyi/config/google-integration.json`:

```json
{
  "notebooklm": {
    "enabled": true,
    "autoImport": true,
    "authMethod": "browser",
    "browserProfile": "~/.config/google-chrome"
  }
}
```

---

## 💡 使用场景

### 1. 研究笔记
- 收集论文/文章
- 自动生成摘要
- AI 辅助分析

### 2. 会议记录
- 上传会议记录
- 提取关键决策
- 生成行动项

### 3. 学习整理
- 整合学习资料
- AI 问答复习
- 导出知识卡片

### 4. 内容创作
- 收集素材
- AI 辅助构思
- 生成大纲

---

## ⚠️ 注意事项

1. **需要登录**: 首次使用需在浏览器登录 Google 账号
2. **网页自动化**: 依赖 Playwright 和 Chrome
3. **无官方 API**: 功能基于网页模拟，可能随界面变化

---

## 🔗 相关链接

- [NotebookLM 官网](https://notebooklm.google.com/)
- [官方文档](https://support.google.com/notebooklm)

---

*创建：2026-04-08 | 太一 AGI*

---
name: notebooklm-cli
version: 1.0.0
description: notebooklm-cli skill
category: cli
tags: []
author: 太一 AGI
created: 2026-04-07
---


# NotebookLM CLI Skill

> **版本**: v1.0 | **创建**: 2026-04-06 12:03  
> **来源**: https://github.com/tmc/nlm  
> **许可证**: MIT (开源)

---

## 🎯 核心功能

**NotebookLM CLI (nlm)** 是 Google NotebookLM 的命令行接口。

| 功能 | 说明 |
|------|------|
| **📖 笔记本管理** | 创建/列出/删除笔记本 |
| **📁 源文件操作** | 上传 PDF/URL/文本/YouTube |
| **📝 笔记管理** | 创建/编辑/组织笔记 |
| **🎧 音频概览** | 生成 AI 音频摘要 |
| **🎬 视频概览** | 生成 AI 视频摘要 |
| **🤖 AI 转换** | 重写/总结/扩展/批评 |
| **💬 交互式对话** | 与笔记内容对话 |
| **🔍 高级生成** | 指南/大纲/时间线/思维导图 |
| **🔌 MCP 集成** | 与 Gemini CLI 联动 |

---

## 📦 安装

### 方式 1: Go install (推荐)

```bash
go install github.com/tmc/nlm/cmd/nlm@latest
```

### 方式 2: 从源码安装

```bash
cd /home/nicola/.openclaw/workspace/nlm
go build -o nlm ./cmd/nlm
sudo cp nlm /usr/local/bin/
```

### 方式 3: 预编译二进制

查看 Releases: https://github.com/tmc/nlm/releases

---

## 🔑 认证配置

### 获取认证

**方式 1: 浏览器自动认证 (推荐)**

```bash
nlm auth
# 会自动打开浏览器登录 Google 账号
```

**方式 2: 手动认证**

```bash
nlm auth --keep-open 60
# 在 60 秒内完成浏览器登录
```

**方式 3: Cookie 认证**

1. 访问：https://notebooklm.google.com
2. 登录 Google 账号
3. F12 → Application → Cookies → 复制 `__Secure-1PSID`
4. 配置：
```bash
nlm config --sid "你的__Secure-1PSID"
```

---

## 💡 使用示例

### 笔记本管理

```bash
# 列出所有笔记本
nlm notebooks list

# 创建新笔记本
nlm notebooks create "我的研究项目"

# 查看笔记本详情
nlm notebooks get --id "notebook_id"

# 删除笔记本
nlm notebooks delete --id "notebook_id"
```

### 源文件操作

```bash
# 上传 PDF 文件
nlm sources upload --notebook "我的研究" document.pdf

# 添加 URL
nlm sources add-url --notebook "我的研究" https://example.com/article

# 添加 YouTube 视频
nlm sources add-youtube --notebook "我的研究" https://youtube.com/watch?v=xxx

# 添加文本
nlm sources add-text --notebook "我的研究" "这是研究内容..."

# 列出源文件
nlm sources list --notebook "我的研究"
```

### 笔记管理

```bash
# 创建笔记
nlm notes create --notebook "我的研究" "关键发现"

# 编辑笔记
nlm notes edit --note "note_id" "更新内容"

# 列出笔记
nlm notes list --notebook "我的研究"

# 删除笔记
nlm notes delete --note "note_id"
```

### 音频/视频概览

```bash
# 生成音频概览
nlm audio generate --notebook "我的研究"

# 下载音频
nlm audio download --notebook "我的研究" --output overview.mp3

# 生成视频概览
nlm video generate --notebook "我的研究"

# 下载视频
nlm video download --notebook "我的研究" --output overview.mp4
```

### AI 内容转换

```bash
# 总结内容
nlm transform --notebook "我的研究" "总结这个研究"

# 重写内容
nlm transform --notebook "我的研究" "用更简单的语言重写"

# 扩展内容
nlm transform --notebook "我的研究" "详细解释这个概念"

# 批评分析
nlm transform --notebook "我的研究" "分析这个研究的局限性"
```

### 交互式对话

```bash
# 开始对话
nlm chat --notebook "我的研究"

# 单次提问
nlm ask --notebook "我的研究" "这个研究的主要发现是什么？"
```

### 高级生成

```bash
# 生成学习指南
nlm generate guide --notebook "我的研究"

# 生成大纲
nlm generate outline --notebook "我的研究"

# 生成时间线
nlm generate timeline --notebook "我的研究"

# 生成思维导图
nlm generate mindmap --notebook "我的研究"
```

---

## 🔌 MCP 集成

### 配置 MCP 服务器

```bash
# 安装 NotebookLM MCP 服务器
npm install -g @tmc/notebooklm-mcp

# 配置到 Gemini CLI
cat >> ~/.gemini/settings.json << 'EOF'
{
  "mcpServers": {
    "notebooklm": {
      "command": "nlm",
      "args": ["mcp", "serve"]
    }
  }
}
EOF
```

### 在 Gemini CLI 中使用

```bash
# 通过 MCP 查询笔记本
gemini "@notebooklm 总结我的所有研究笔记"

# 生成音频概览
gemini "@notebooklm 为我的最新笔记本生成音频"

# 搜索内容
gemini "@notebooklm 找到关于 AI 的所有笔记"
```

---

## 🎯 太一集成

### 1. Python 封装器

```python
# skills/notebooklm-cli/scripts/runner.py
#!/usr/bin/env python3
"""NotebookLM CLI 运行器"""

import subprocess
import os

class NotebookLMRunner:
    """NotebookLM CLI 封装"""
    
    def __init__(self):
        self.env = os.environ.copy()
    
    def list_notebooks(self) -> list:
        """列出所有笔记本"""
        result = subprocess.run(
            ['nlm', 'notebooks', 'list'],
            capture_output=True, text=True
        )
        return result.stdout.strip().split('\n')
    
    def create_notebook(self, title: str) -> str:
        """创建笔记本"""
        result = subprocess.run(
            ['nlm', 'notebooks', 'create', title],
            capture_output=True, text=True
        )
        return result.stdout
    
    def upload_source(self, notebook: str, file_path: str) -> str:
        """上传源文件"""
        result = subprocess.run(
            ['nlm', 'sources', 'upload', '--notebook', notebook, file_path],
            capture_output=True, text=True
        )
        return result.stdout
    
    def generate_audio(self, notebook: str) -> str:
        """生成音频概览"""
        result = subprocess.run(
            ['nlm', 'audio', 'generate', '--notebook', notebook],
            capture_output=True, text=True
        )
        return result.stdout
    
    def chat(self, notebook: str, message: str) -> str:
        """与笔记对话"""
        result = subprocess.run(
            ['nlm', 'ask', '--notebook', notebook, message],
            capture_output=True, text=True
        )
        return result.stdout
```

### 2. 知几-E 集成

```python
# skills/zhiji-e/notebooklm_integration.py

from skills.notebooklm_cli.scripts.runner import NotebookLMRunner

class NotebookLMAssistant:
    """NotebookLM 助手 - 知几-E 集成"""
    
    def __init__(self):
        self.runner = NotebookLMRunner()
    
    def research_summary(self, notebook: str) -> str:
        """研究生成摘要"""
        return self.runner.chat(
            notebook,
            "请用中文总结这个笔记本的核心发现"
        )
    
    def create_learning_material(self, notebook: str) -> str:
        """创建学习材料"""
        return self.runner.run(
            'nlm', 'generate', 'guide', '--notebook', notebook
        ).stdout
    
    def audio_briefing(self, notebook: str) -> str:
        """生成音频简报"""
        return self.runner.generate_audio(notebook)
```

---

## 📊 配额限制

| 操作 | 免费额度 | 说明 |
|------|---------|------|
| **笔记本创建** | 100 个 | 每个 Google 账号 |
| **源文件上传** | 50 个/笔记本 | PDF/URL/文本等 |
| **音频生成** | 不限 | 每个笔记本每天 |
| **视频生成** | 不限 | 每个笔记本每天 |
| **AI 对话** | 不限 | 受 Gemini 配额限制 |

---

## ⚠️  注意事项

### ✅ 推荐做法
- 使用浏览器自动认证
- 定期备份重要笔记
- 使用有意义的笔记本名称
- 利用 MCP 集成提高效率

### ❌ 避免做法
- 不要分享认证 Cookie
- 不要上传敏感/私人信息
- 不要滥用 API（可能被封禁）
- 不要依赖未文档化的 API

---

## 🔗 相关链接

- **GitHub**: https://github.com/tmc/nlm
- **PyPI**: https://pypi.org/project/notebooklm-cli/
- **MCP 服务器**: https://github.com/tmc/notebooklm-mcp
- **官方网站**: https://notebooklm.google/
- **文档**: https://github.com/tmc/nlm/tree/main/docs

---

## 📝 快速参考

```bash
# 安装
go install github.com/tmc/nlm/cmd/nlm@latest

# 认证
nlm auth

# 列出笔记本
nlm notebooks list

# 创建笔记本
nlm notebooks create "项目名称"

# 上传源文件
nlm sources upload --notebook "项目" document.pdf

# 生成音频
nlm audio generate --notebook "项目"

# 对话
nlm ask --notebook "项目" "问题内容"

# MCP 集成
gemini "@notebooklm 总结我的笔记"
```

---

*创建：太一 AGI | 2026-04-06 12:03*  
*状态：✅ 已克隆，待安装配置*

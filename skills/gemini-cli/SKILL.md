---
name: gemini-cli
version: 1.0.0
description: gemini-cli skill
category: cli
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Gemini CLI Skill

> **版本**: v1.0 | **创建**: 2026-04-06 11:47  
> **来源**: Google 官方 Gemini CLI  
> **GitHub**: https://github.com/google-gemini/gemini-cli

---

## 🎯 核心功能

**Gemini CLI** 是 Google 官方的开源 AI 助手，直接在终端使用 Gemini 模型。

| 功能 | 说明 |
|------|------|
| **代码生成** | Python/JS/TS 等任意语言 |
| **代码审查** | Bug 检测 + 优化建议 |
| **文档编写** | 自动生成文档注释 |
| **调试帮助** | 分析错误日志 |
| **文件操作** | 读取/写入/搜索文件 |
| **Shell 命令** | 安全执行终端命令 |
| **网页抓取** | 获取网页内容 |
| **Google Search** | 实时信息检索 |

---

## 📦 安装

### 方式 1: 全局安装 (推荐)

```bash
npm install -g @google/gemini-cli
```

### 方式 2: 即时运行

```bash
npx @google/gemini-cli
```

### 方式 3: Homebrew (macOS/Linux)

```bash
brew install gemini-cli
```

---

## 🔑 认证配置

### 获取 API Key

1. 访问：https://aistudio.google.com/apikey
2. 点击 "Create API Key"
3. 复制 Key

### 配置方式

**方式 1: 环境变量**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

**方式 2: 配置文件**
```bash
mkdir -p ~/.gemini
cat > ~/.gemini/settings.json << 'EOF'
{
  "geminiApiKey": "your_api_key_here",
  "model": "gemini-2.0-flash",
  "theme": "dark"
}
EOF
```

**方式 3: OAuth 登录**
```bash
gemini login
```

---

## 💡 使用示例

### 基础对话

```bash
# 交互模式
gemini

# 单次查询
gemini "Create a Python Fibonacci function"
```

### 代码生成

```bash
gemini "Create a REST API with FastAPI for user management"
```

### 代码审查

```bash
gemini "Review this code for bugs: @file src/main.py"
```

### 文件分析

```bash
gemini "Explain what this code does: @file src/complex_module.py"
```

### 调试帮助

```bash
gemini "Help me fix this error: @file error.log"
```

### 文档生成

```bash
gemini "Generate documentation for: @file src/api.py"
```

### 测试编写

```bash
gemini "Write unit tests for: @file src/utils.py"
```

---

## 🔧 内置工具

### @file - 文件操作

```bash
gemini "Read the contents of: @file config.json"
gemini "Create a new file: @file new_script.py"
```

### @shell - Shell 命令

```bash
gemini "Run tests: @shell npm test"
gemini "List files: @shell ls -la"
```

### @fetch - 网页抓取

```bash
gemini "Get the latest news: @fetch https://example.com"
```

### @google - Google Search

```bash
gemini "Search for Python best practices: @google Python async await"
```

---

## 🔌 MCP 扩展

### 配置 MCP 服务器

编辑 `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"]
    },
    "database": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-database"]
    }
  }
}
```

### 使用示例

```bash
# GitHub 集成
gemini "@github List my open pull requests"

# Slack 集成
gemini "@slack Send summary to #dev channel"

# 数据库集成
gemini "@database Query inactive users"
```

---

## 📊 配额限制

| 账号类型 | 请求/分钟 | 请求/天 | 适用场景 |
|---------|----------|--------|---------|
| **个人 Google** | 60 | 1,000 | 个人开发/学习 ✅ |
| **Google Cloud** | 300 | 10,000 | 团队/企业 |
| **付费版** | 1,000+ | 100,000+ | 生产环境 |

---

## 🎯 太一集成

### 与 OpenClaw 集成

```python
# skills/gemini-cli/scripts/runner.py
#!/usr/bin/env python3
"""Gemini CLI 运行器"""

import subprocess
import os

def gemini_ask(prompt: str, api_key: str = None) -> str:
    """询问 Gemini"""
    env = os.environ.copy()
    if api_key:
        env['GEMINI_API_KEY'] = api_key
    
    result = subprocess.run(
        ['gemini', prompt],
        capture_output=True,
        text=True,
        env=env
    )
    return result.stdout

# 使用示例
if __name__ == '__main__':
    response = gemini_ask("Create a hello world Python script")
    print(response)
```

### 与知几-E 集成

```python
# skills/zhiji-e/gemini_integration.py

from .scripts.runner import gemini_ask

class GeminiAssistant:
    """Gemini 助手 - 知几-E 集成"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def analyze_code(self, file_path: str) -> str:
        """分析代码"""
        return gemini_ask(
            f"Review this code: @file {file_path}",
            self.api_key
        )
    
    def generate_tests(self, file_path: str) -> str:
        """生成测试"""
        return gemini_ask(
            f"Write unit tests for: @file {file_path}",
            self.api_key
        )
    
    def debug_error(self, error_log: str) -> str:
        """调试错误"""
        return gemini_ask(
            f"Help me fix this error: @file {error_log}",
            self.api_key
        )
```

---

## ⚠️  注意事项

### ✅ 推荐做法
- 使用 API Key 进行自动化
- 定期更新到最新版本
- 配置 MCP 服务器扩展功能
- 使用沙箱模式执行未知代码

### ❌ 避免做法
- 不要硬编码 API Key 在代码中
- 不要在生产环境使用免费配额
- 不要执行不可信的 Shell 命令
- 不要忽略安全警告

---

## 🔗 相关链接

- **GitHub**: https://github.com/google-gemini/gemini-cli
- **官方文档**: https://geminicli.com/docs/
- **NPM 包**: https://www.npmjs.com/package/@google/gemini-cli
- **API Key**: https://aistudio.google.com/apikey
- **Roadmap**: https://github.com/orgs/google-gemini/projects/11

---

## 📝 快速参考

```bash
# 安装
npm install -g @google/gemini-cli

# 登录
gemini login

# 交互模式
gemini

# 单次查询
gemini "Create a Python function"

# 文件分析
gemini "Explain: @file src/main.py"

# 代码审查
gemini "Review: @file src/api.py"

# 调试
gemini "Fix: @file error.log"
```

---

*创建：太一 AGI | 2026-04-06 11:47*  
*状态：✅ 已创建，待 API Key 配置*

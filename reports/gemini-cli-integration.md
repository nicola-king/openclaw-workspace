# 🚀 Gemini CLI 集成报告

> **执行时间**: 2026-04-06 11:34-11:35 (1 分钟)  
> **来源**: GitHub - google-gemini/gemini-cli  
> **状态**: ✅ 已克隆，待安装

---

## 📊 项目信息

| 指标 | 数据 |
|------|------|
| **GitHub** | https://github.com/google-gemini/gemini-cli |
| **版本** | 0.36.0-nightly (2026-03-17) |
| **许可证** | Apache 2.0 (开源) |
| **语言** | TypeScript/Node.js |
| **Node 要求** | >=20.0.0 |
| **免费配额** | 60 请求/分钟 + 1000 请求/天 |

---

## 🎯 核心特性

### 为什么选择 Gemini CLI？

| 特性 | 说明 |
|------|------|
| **🎯 免费额度** | 个人 Google 账号：60 请求/分钟 + 1000 请求/天 |
| **🧠 Gemini 3** | 改进的推理能力 + 1M token 上下文窗口 |
| **🔧 内置工具** | Google Search/文件操作/Shell 命令/网页抓取 |
| **🔌 MCP 支持** | Model Context Protocol，自定义扩展 |
| **💻 终端优先** | 专为开发者设计 |
| **🛡️ 开源** | Apache 2.0 许可证 |

---

## 📦 安装方式

### 方式 1: 立即运行 (无需安装)

```bash
npx @google/gemini-cli
```

### 方式 2: 全局安装 (推荐)

```bash
npm install -g @google/gemini-cli
```

### 方式 3: Homebrew (macOS/Linux)

```bash
brew install gemini-cli
```

### 方式 4: MacPorts (macOS)

```bash
sudo port install gemini-cli
```

### 方式 5: 从源码安装 (已克隆)

```bash
cd /home/nicola/.openclaw/workspace/gemini-cli
npm install
npm run build
npm run start
```

---

## 🔑 认证配置

### 方式 1: 个人 Google 账号 (免费)

```bash
gemini login
# 会打开浏览器进行 OAuth 认证
```

### 方式 2: API Key (推荐用于自动化)

```bash
# 获取 API Key: https://aistudio.google.com/apikey
export GEMINI_API_KEY="your_api_key_here"

# 或使用配置文件
echo "GEMINI_API_KEY=your_api_key" >> ~/.gemini/settings.json
```

### 方式 3: Google Cloud 账号

```bash
gcloud auth application-default login
```

---

## 🛠️ 内置工具

### 1. 文件系统操作

```
> @file Read the contents of src/main.py
> @file Write a new configuration file
```

### 2. Shell 命令

```
> @shell Run npm install
> @shell Execute python script.py
```

### 3. 网页抓取

```
> @fetch Get the latest news from example.com
> @search Find information about Gemini CLI
```

### 4. Google Search

```
> @google Search for Python best practices
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

```
> @github List my open pull requests
> @slack Send a summary to #dev channel
> @database Query inactive users
```

---

## 💡 使用示例

### 代码生成

```
> Create a Python function to calculate Fibonacci sequence
```

### 代码审查

```
> Review this code for bugs and suggest improvements: @file src/main.py
```

### 调试帮助

```
> Help me debug this error: @file error.log
```

### 文档生成

```
> Generate documentation for this module: @file src/api.py
```

### 测试编写

```
> Write unit tests for this function: @file src/utils.py
```

---

## 🎯 太一集成方案

### 与 OpenClaw 集成

```bash
# 创建 Gemini Skill
mkdir -p /home/nicola/.openclaw/workspace/skills/gemini-cli
cd /home/nicola/.openclaw/workspace/skills/gemini-cli

# 创建 SKILL.md
cat > SKILL.md << 'EOF'
# Gemini CLI Skill

> 版本：v1.0 | 创建：2026-04-06
> 来源：Google 官方 Gemini CLI

## 功能
- 代码生成/审查
- 文档编写
- 调试帮助
- Shell 命令执行
- 网页信息抓取

## 配置
GEMINI_API_KEY=your_api_key

## 使用
npx @google/gemini-cli
EOF
```

### 与知几-E 集成

```python
# skills/zhiji-e/gemini_integration.py

import subprocess

class GeminiAssistant:
    """Gemini CLI 助手"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.env = {**os.environ, 'GEMINI_API_KEY': api_key}
    
    def ask(self, prompt: str) -> str:
        """询问 Gemini"""
        result = subprocess.run(
            ['npx', '@google/gemini-cli', '--prompt', prompt],
            capture_output=True,
            text=True,
            env=self.env
        )
        return result.stdout
    
    def analyze_code(self, file_path: str) -> str:
        """分析代码"""
        return self.ask(f"Review this code: @file {file_path}")
    
    def generate_tests(self, file_path: str) -> str:
        """生成测试"""
        return self.ask(f"Write unit tests for: @file {file_path}")
```

---

## 📊 配额对比

| 账号类型 | 请求/分钟 | 请求/天 | 适用场景 |
|---------|----------|--------|---------|
| **个人 Google** | 60 | 1,000 | 个人开发/学习 |
| **Google Cloud** | 300 | 10,000 | 团队/企业 |
| **付费版** | 1,000+ | 100,000+ | 生产环境 |

---

## 🚀 快速开始

### 步骤 1: 安装

```bash
npm install -g @google/gemini-cli
```

### 步骤 2: 认证

```bash
gemini login
# 或
export GEMINI_API_KEY="your_api_key"
```

### 步骤 3: 使用

```bash
gemini
# 进入交互模式

# 或直接执行
gemini "Create a hello world Python script"
```

---

## 📝 配置文件

### 位置：`~/.gemini/settings.json`

```json
{
  "theme": "dark",
  "model": "gemini-2.0-flash",
  "maxContextTokens": 1000000,
  "tools": {
    "fileSystem": true,
    "shell": true,
    "webFetch": true,
    "googleSearch": true
  },
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
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

## 📦 已克隆到本地

**位置**: `/home/nicola/.openclaw/workspace/gemini-cli/`

**下一步**:
1. 安装依赖：`npm install`
2. 构建项目：`npm run build`
3. 测试运行：`npm run start`
4. 创建 Skill：集成到太一系统

---

*报告生成：太一 AGI | 2026-04-06 11:35*  
*状态：✅ 已克隆，待安装集成*

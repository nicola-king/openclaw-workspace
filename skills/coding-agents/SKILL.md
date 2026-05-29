---
name: coding-agents
version: 1.0.0
description: 太一编码 Agent 调度引擎 — OpenHands (75K⭐) + Goose (46K⭐) 统一入口
category: development
tags: ['coding-agent', 'openhands', 'goose', 'ai-development', 'mcp', 'acp', 'agent-orchestration']
author: 太一 AGI
created: 2026-05-29
status: active
trigger: 当需要编码/开发/调试/自动化时，自动调度 OpenHands 或 Goose
---

# 🤖 太一编码 Agent 调度引擎

> 统一调度 OpenHands (AI-Driven Development) + Goose (通用 AI Agent)
> 参考架构：OpenHands SDK→CLI→GUI 三层 · Goose MCP+ACP 扩展 · Linux Foundation AAIF

---

## 🧠 智能调度规则

| 任务类型 | 推荐 Agent | 理由 |
|----------|-----------|------|
| **代码开发/调试** | OpenHands | 专注编码，Python SDK 可组合 |
| **自动化工作流** | Goose | 通用 Agent，MCP 扩展生态丰富 |
| **研究/写作/分析** | Goose | 不限代码，多 LLM 后端 |
| **PR Review/CI 集成** | OpenHands | 有 Cloud 集成（Slack/Jira/Linear） |
| **本地文件操作** | Goose | 桌面 App + CLI |
| **云端部署管道** | OpenHands | Cloud 模式支持分布式 |

### 自动识别特征

```
"写代码/改 bug/重构/调试"        → OpenHands
"自动化/批处理/数据清洗/写文档"   → Goose
"开发/PR/部署管道"               → OpenHands
"研究/查询/分析/写作"            → Goose
"编码 Agent/开发 Agent"          → 智能检测已安装的 Agent
```

---

## 🏗 架构对比

| 维度 | OpenHands | Goose |
|------|-----------|-------|
| ⭐ Stars | **75,267** | 46,014 |
| 语言 | **Python** | Rust |
| 许可 | MIT | **Apache 2.0** |
| 核心定位 | AI-Driven Development | 通用 AI Agent |
| 架构 | SDK → CLI → GUI → Cloud | Desktop → CLI → API |
| LLM 后端 | Claude, GPT, 任意 | 15+ 提供商 |
| 扩展协议 | 内置扩展 | **MCP (70+ extensions)** |
| Agent 协议 | CLI 调用 | **ACP (Agent Communication Protocol)** |
| 组织 | OpenHands 社区 | **Linux Foundation AAIF** |
| 安装 | pip install openhands | brew/cargo/curl 安装 |

### OpenHands 三层架构（参考模型）

```
Software Agent SDK (Python 库，可组合)
        ↓
     CLI 模式 (类 Claude Code)
        ↓
GUI / Cloud (REST API + React SPA)
```

### Goose 四层架构（参考模型）

```
 Desktop App (macOS/Linux/Windows)
        ↓
     CLI (终端工作流)
        ↓
     API (嵌入任意系统)
        ↓
 15+ LLM 后端 + 70+ MCP 扩展
```

---

## 🔌 调用方式

```python
from skills.coding_agents.scheduler import (
    schedule,        # 智能调度（自动选 Agent）
    openhands_run,   # 直接调 OpenHands
    goose_run,       # 直接调 Goose
    info,            # Agent 信息
    check,           # 可用性检测
)
```

### 一键命令

```
/agent "写一个 Python 脚本来..."
/agent --openhands "重构这个模块..."
/agent --goose "自动化这个数据管道..."
/agent check        # 检测已安装的 Agent
/agent info         # Agent 版本信息
```

---

## 📁 文件结构

```
skills/coding-agents/
├── SKILL.md          ← 本文档
└── scheduler.py      ← 统一调度引擎
```

## 🔗 相关资源

- OpenHands: https://github.com/OpenHands/OpenHands (75K⭐)
- OpenHands SDK: https://github.com/OpenHands/software-agent-sdk (769⭐)
- OpenHands Docs: https://docs.openhands.dev
- Goose: https://github.com/aaif-goose/goose (46K⭐)
- Goose Docs: https://goose-docs.ai
- AAIF: https://aaif.io (Linux Foundation)
- ACP: https://agentcommunicationprotocol.ai
- MCP: https://modelcontextprotocol.io

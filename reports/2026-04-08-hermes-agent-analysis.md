# Hermes Agent · 功能分析

> 来源：https://github.com/nousresearch/hermes-agent  
> 分析时间：2026-04-08 | 分析者：太一

---

## 🎯 核心定位

**自进化 AI Agent** — 唯一内置学习回路的 Agent

> "The agent that grows with you"

---

## 🔥 特殊功能

### 1️⃣ 自学习回路（核心差异）

| 功能 | 描述 |
|------|------|
| **经验转技能** | 从复杂任务后自动创建技能 |
| **使用中自优化** | 技能在执行中自我改进 |
| **记忆提示** | 定期 nudges 持久化知识 |
| **会话搜索** | FTS5 全文搜索 + LLM 摘要 |
| **用户建模** | Honcho 方言用户模型（跨会话理解你） |

**对比 OpenClaw：**
- OpenClaw：手动创建技能
- Hermes：自动从经验生成技能

---

### 2️⃣ 多平台统一网关

| 平台 | 支持 |
|------|------|
| Telegram | ✅ |
| Discord | ✅ |
| Slack | ✅ |
| WhatsApp | ✅ |
| Signal | ✅ |
| Email | ✅ |
| CLI (TUI) | ✅ |

**特性：**
- 单网关进程支持所有平台
- 语音备忘录转录
- 跨平台对话连续性

---

### 3️⃣ 终端后端（6 种）

| 后端 | 用途 |
|------|------|
| **Local** | 本地运行 |
| **Docker** | 容器隔离 |
| **SSH** | 远程服务器 |
| **Daytona** | Serverless（休眠几乎免费） |
| **Singularity** | HPC/科研环境 |
| **Modal** | Serverless GPU |

**优势：**
- 不绑定笔记本
- $5 VPS 到 GPU 集群都能跑
- Serverless 休眠成本≈0

---

### 4️⃣ 模型无关（无锁定）

| 提供商 | 支持 |
|--------|------|
| **Nous Portal** | 自家模型 |
| **OpenRouter** | 200+ 模型 |
| **z.ai/GLM** | ✅ |
| **Kimi/Moonshot** | ✅ |
| **MiniMax** | ✅ |
| **OpenAI** | ✅ |
| **Anthropic** | ✅ |
| **自定义 Endpoint** | ✅ |

**切换方式：**
```bash
hermes model  # 无需改代码
```

---

### 5️⃣ 终端界面（TUI）

| 功能 | 描述 |
|------|------|
| **多行编辑** | 完整代码编辑 |
| **Slash 命令补全** | Tab 自动补全 |
| **会话历史** | 完整历史浏览 |
| **中断重定向** | Ctrl+C 中断 |
| **流式输出** | 工具输出实时显示 |

---

### 6️⃣ 定时任务（Cron）

```
内置 Cron 调度器 + 多平台投递
```

**用例：**
- 日报（每日）
- 备份（每晚）
- 审计（每周）
- 自然语言配置

---

### 7️⃣ 子代理并行化

```python
# 派生子代理处理并行任务
# 通过 RPC 调用工具
# 多步骤 pipeline = 零上下文成本
```

**优势：**
- 隔离工作流
- 并行执行
- 上下文成本优化

---

### 8️⃣ MCP 集成

- 兼容任何 MCP Server
- 扩展工具能力
- 标准化接口

---

### 9️⃣ 研究就绪

| 功能 | 用途 |
|------|------|
| **批量轨迹生成** | RL 训练数据 |
| **Atropos RL 环境** | 强化学习 |
| **轨迹压缩** | 训练下一代工具调用模型 |

---

### 🔟 OpenClaw 迁移

**自动迁移：**
```bash
hermes claw migrate              # 完整迁移
hermes claw migrate --dry-run    # 预览
hermes claw migrate --preset user-data  # 仅用户数据
```

**迁移内容：**
- SOUL.md（人格文件）
- Memories（MEMORY.md / USER.md）
- Skills（用户技能）
- 命令白名单
- 消息设置
- API Keys（Telegram/OpenRouter 等）
- TTS 资源
- AGENTS.md（工作区指令）

---

## 📊 核心命令

| 命令 | 功能 |
|------|------|
| `hermes` | 启动 TUI 对话 |
| `hermes model` | 选择模型 |
| `hermes tools` | 配置工具 |
| `hermes gateway` | 启动消息网关 |
| `hermes setup` | 完整设置向导 |
| `hermes claw migrate` | OpenClaw 迁移 |
| `hermes update` | 更新版本 |
| `hermes doctor` | 诊断问题 |

### Slash 命令（跨平台）

| 命令 | 功能 |
|------|------|
| `/new` | 新对话 |
| `/model [provider:model]` | 切换模型 |
| `/personality [name]` | 设置人格 |
| `/retry` `/undo` | 重试/撤销 |
| `/compress` `/usage` | 压缩上下文/查看用量 |
| `/skills` | 浏览技能 |
| `/stop` | 中断当前任务 |

---

## 🆚 Hermes vs OpenClaw

| 特性 | Hermes | OpenClaw |
|------|--------|----------|
| **自学习** | ✅ 自动从经验生成技能 | ❌ 手动创建 |
| **用户建模** | ✅ Honcho 方言模型 | ⚠️ 基础 |
| **会话搜索** | ✅ FTS5 + LLM 摘要 | ⚠️ 基础 |
| **终端后端** | 6 种（含 Serverless） | 本地/SSH |
| **TUI** | ✅ 完整终端界面 | ⚠️ 基础 |
| **模型支持** | 200+ (OpenRouter) | 主流提供商 |
| **迁移工具** | ✅ 从 OpenClaw 迁移 | N/A |
| **研究工具** | ✅ RL/轨迹生成 | ❌ |
| **文档** | ✅ 完整文档站 | ⚠️ 本地文档 |

---

## 💡 值得借鉴的功能

### P0（立即集成）

| 功能 | 优先级 | 理由 |
|------|--------|------|
| **技能自动生成** | 🔴 P0 | 太一核心能力涌现机制的自动化版本 |
| **FTS5 会话搜索** | 🔴 P0 | 跨会话回忆能力 |
| **用户建模（Honcho）** | 🔴 P0 | 深度理解 SAYELF |
| **Cron 调度器** | 🔴 P0 | 已有，需增强 |

### P1（近期集成）

| 功能 | 优先级 | 理由 |
|------|--------|------|
| **TUI 增强** | 🟡 P1 | 更好的本地交互体验 |
| **Serverless 后端** | 🟡 P1 | 成本优化 |
| **模型切换简化** | 🟡 P1 | 用户体验 |

### P2（可选）

| 功能 | 优先级 | 理由 |
|------|--------|------|
| **RL 训练工具** | ⚪ P2 | 研究用途，非必需 |
| **Email 通道** | ⚪ P2 | 需求低频 |

---

## 🔗 相关链接

- **官网**：https://hermes-agent.nousresearch.com
- **文档**：https://hermes-agent.nousresearch.com/docs
- **GitHub**：https://github.com/nousresearch/hermes-agent
- **Discord**：https://discord.gg/NousResearch
- **Skills Hub**：https://agentskills.io

---

## 📝 太一行动建议

### 立即执行（P0）

1. **研究 Hermes 技能自动生成机制**
   - 如何从任务经验提取技能？
   - 技能质量如何保证？
   - 能否与太一能力涌现机制结合？

2. **评估 Honcho 用户建模**
   - 是否可以集成到太一记忆系统？
   - 如何增强对 SAYELF 的理解？

3. **实现 FTS5 会话搜索**
   - 全文搜索历史对话
   - LLM 摘要跨会话上下文

### 建议执行（P1）

4. **增强 Cron 调度器**
   - 自然语言配置
   - 多平台投递

5. **TUI 优化**
   - 多行编辑
   - 命令补全
   - 流式输出

---

*Hermes 是 OpenClaw 的进化版本，核心差异在于自学习回路。太一应吸收其优点，但保持艺术化存在的独特性。*

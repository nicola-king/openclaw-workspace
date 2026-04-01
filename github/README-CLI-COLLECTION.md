# OpenClaw CLI 最佳实践与工具集

> 🦞 让 OpenClaw 更强大 - CLI 驱动的自动化工作流

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.3.31-blue)](https://github.com/openclaw/openclaw)
[![太一 AGI](https://img.shields.io/badge/太一-AGI 总管-green)](https://github.com/nicola-king/openclaw-workspace)

---

## 📖 简介

本仓库包含 OpenClaw CLI 的最佳实践文档、自动化工具和工作流案例，帮助你最大化 OpenClaw 的生产力。

**核心内容**：
- 📚 CLI 速查表 - 10 个常用命令快速上手
- 📖 最佳实践 - 命令规范、脚本模板、安全基线
- 🔧 HEARTBEAT CLI - 一键系统检查工具
- 💡 工作流案例 - 晨报自动化/GitHub Issue/Polymarket 交易

---

## 🚀 快速开始

### 1. CLI 速查表

**立即使用**：
```bash
# 查看速查表
cat docs/CLI-CHEATSHEET-README.md

# 或在线阅读
# https://github.com/nicola-king/openclaw-workspace/blob/main/docs/CLI-CHEATSHEET-README.md
```

**10 个核心命令**：
```bash
# 会话管理
openclaw sessions list --limit 10
openclaw sessions spawn --task "分析数据" --runtime subagent

# 记忆操作
openclaw memory search --query "关键词" --limit 5

# 消息发送
openclaw message send --target @user --message "Hello"

# 系统检查
openclaw doctor
openclaw gateway status
```

### 2. HEARTBEAT CLI 工具

**一键检查系统状态**：
```bash
# 添加执行权限
chmod +x scripts/heartbeat-cli.sh

# 执行全部检查
./scripts/heartbeat-cli.sh all

# 单项检查
./scripts/heartbeat-cli.sh gateway    # Gateway 状态
./scripts/heartbeat-cli.sh sessions   # 活跃会话
./scripts/heartbeat-cli.sh tasks      # 待办任务
./scripts/heartbeat-cli.sh send       # 发送心跳消息
```

**输出示例**：
```
================================
  HEARTBEAT CLI 快捷命令
================================

[07:00:00] 开始全面心跳检查...

✓ Gateway 运行中
✓ 活跃会话：2 个
✓ 待办任务：3 个
✓ 微信通道：正常
✓ Telegram 通道：正常
CPU 使用率：12.5%
内存使用率：45.2%
磁盘使用率：67%

✓ 报告已生成：/tmp/heartbeat-report-20260402-070000.md
```

### 3. 工作流案例

**查看完整案例**：
```bash
cat docs/automation-workflow-examples.md
```

**包含案例**：
1. **每日晨报自动化** - 每天 06:00 自动执行宪法学习、记忆提炼、系统自检
2. **GitHub Issue 自动处理** - 自动分类、分配 Bot、跟踪进度
3. **Polymarket 交易监控** - 7x24 小时监控高置信度交易机会

---

## 📚 文档索引

| 文档 | 说明 | 大小 |
|------|------|------|
| [CLI-CHEATSHEET-README.md](docs/CLI-CHEATSHEET-README.md) | CLI 速查表 | 2.5KB |
| [openclaw-cli-best-practices.md](docs/openclaw-cli-best-practices.md) | 最佳实践指南 | 11.5KB |
| [automation-workflow-examples.md](docs/automation-workflow-examples.md) | 工作流案例集 | 11.3KB |
| [CLI 化趋势分析报告](reports/cli-trend-analysis-2026.md) | 行业趋势分析 | 5.1KB |

---

## 🛠️ 工具脚本

| 脚本 | 用途 | 大小 |
|------|------|------|
| [heartbeat-cli.sh](scripts/heartbeat-cli.sh) | 系统检查工具 | 7.3KB |
| [daily-constitution.sh](scripts/daily-constitution.sh) | 每日宪法学习 | 6.6KB |
| [auto-exec-task.sh](scripts/auto-exec-task.sh) | 自动执行任务 | 2.4KB |

---

## 🎯 使用场景

### 场景 1：日常检查
```bash
# 一键检查所有状态
openclaw gateway status && \
openclaw sessions list --limit 5 && \
openclaw memory search --query "待办" --limit 3
```

### 场景 2：任务执行
```bash
# 启动任务并监控
openclaw sessions spawn --task "分析 Polymarket 数据" --timeout 300 && \
openclaw sessions list --active-minutes 5
```

### 场景 3：自动化报告
```bash
# 生成并发送日报
bash /opt/openclaw-report.sh daily && \
openclaw message send --target @SAYELF --media reports/daily-report.md
```

---

## 📊 CLI 化趋势

根据 2026 年最新趋势分析：

- **100% AI Agent 选择 CLI-first**（Codex/Claude Code/Gemini CLI）
- **93% 开发者认为 CLI 是核心生产力工具**
- **CLI 工具组合创新成本比 GUI 低 10x**

**为什么 CLI 赢了？**
1. 可组合性 - 管道连接多个工具
2. 自动化优先 - 脚本可重复执行
3. 远程友好 - SSH/容器/服务器唯一选择
4. 低开销 - 启动<100ms，内存<50MB

---

## 🤝 贡献工作流案例

我们欢迎分享你的 OpenClaw 自动化工作流！

**提交方式**：
1. Fork 本仓库
2. 在 `docs/workflow-examples/` 创建你的案例
3. 提交 Pull Request

**案例模板**：
```markdown
# 你的工作流名称

## 场景描述
（解决什么问题）

## 工作流图
（ASCII 流程图）

## 实现代码
（完整脚本）

## 配置说明
（Cron/GitHub Actions 等）

## 效果说明
（实际运行效果）
```

---

## 📝 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🔗 相关链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [太一 AGI 工作区](https://github.com/nicola-king/openclaw-workspace)
- [Discord 社区](https://discord.gg/clawd)

---

## 📮 联系方式

- GitHub Issues: [提问/建议/Bug 反馈](https://github.com/nicola-king/openclaw-workspace/issues)
- 微信：SAYELF 山野精灵
- Telegram: @taiyi_bot

---

*最后更新：2026-04-02 | 太一 AGI 维护*

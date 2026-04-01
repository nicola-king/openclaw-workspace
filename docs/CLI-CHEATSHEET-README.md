# 📋 OpenClaw CLI 速查表

> 快速上手 OpenClaw 命令行工具 | 版本：v1.0 | 更新时间：2026-04-02

---

## 🚀 10 个常用命令

### 会话管理
```bash
# 查看所有会话
openclaw sessions list --limit 10

# 启动新任务
openclaw sessions spawn --task "分析数据" --runtime subagent --timeout 300

# 查看会话历史
openclaw sessions history --session-key <key> --limit 20
```

### 记忆操作
```bash
# 语义搜索记忆
openclaw memory search --query "Polymarket 策略" --limit 5

# 读取记忆片段
openclaw memory get --path memory/core.md --from 10 --lines 20
```

### 消息发送
```bash
# 发送消息
openclaw message send --target @user --message "Hello"

# 发送文件
openclaw message send --target @user --media /path/to/file.pdf
```

### 文件操作
```bash
# 读取文件
openclaw read --path file.md

# 写入文件
openclaw write --path file.md --content "内容"
```

### 执行命令
```bash
# 执行 shell 命令
openclaw exec "git status"

# 带超时执行
openclaw exec "npm install" --timeout 120
```

### 网络工具
```bash
# 搜索网络
openclaw web_search --query "关键词" --count 10

# 抓取网页
openclaw web_fetch --url https://example.com
```

### 图片生成
```bash
# 生成图片
openclaw image_generate --prompt "赛博朋克城市" --size 1024x1024
```

### Gateway 管理
```bash
# 查看状态
openclaw gateway status

# 重启 Gateway
openclaw gateway restart
```

### Cron 任务
```bash
# 列出定时任务
openclaw cron list

# 添加定时任务
openclaw cron create --schedule "0 6 * * *" --command "daily-constitution.sh"
```

### 健康检查
```bash
# 系统自检
openclaw doctor

# 查看帮助
openclaw --help
```

---

## ⌨️ 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+C` | 中断当前命令 |
| `Ctrl+D` | 结束输入 |
| `Tab` | 命令补全 |
| `Ctrl+R` | 搜索历史（需 fzf） |

---

## 🔧 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENCLAW_MODEL` | 默认模型 | `qwen3.5-plus` |
| `OPENCLAW_TIMEOUT` | 默认超时 | `300` 秒 |
| `OPENCLAW_VERBOSE` | 详细日志 | `false` |

---

## 📁 核心路径

| 文件 | 路径 |
|------|------|
| 主配置 | `~/.openclaw/config.json` |
| 工作区 | `~/.openclaw/workspace/` |
| 记忆 | `~/.openclaw/workspace/MEMORY.md` |
| 脚本 | `~/.openclaw/workspace/scripts/` |

---

## 🎯 场景化组合

### 日常检查
```bash
openclaw gateway status && \
openclaw sessions list --limit 5 && \
openclaw memory search --query "待办" --limit 3
```

### 任务执行
```bash
openclaw sessions spawn --task "分析数据" --timeout 300 && \
openclaw sessions list --active-minutes 5
```

---

## 📚 详细文档

- **最佳实践**: [docs/openclaw-cli-best-practices.md](docs/openclaw-cli-best-practices.md)
- **工作流案例**: [docs/automation-workflow-examples.md](docs/automation-workflow-examples.md)
- **HEARTBEAT CLI**: [scripts/heartbeat-cli.sh](scripts/heartbeat-cli.sh)

---

*太一 AGI 维护 | https://github.com/nicola-king/openclaw-workspace*

# OpenClaw CLI 速查表

> 版本：v1.0 | 更新时间：2026-04-02 07:00 | 太一 AGI

---

## 🚀 10 个常用命令（Top 10）

### 1. 会话管理
```bash
# 查看所有会话
openclaw sessions list --limit 10

# 启动新任务
openclaw sessions spawn --task "分析 Polymarket 数据" --runtime subagent --timeout 300

# 查看会话历史
openclaw sessions history --session-key <key> --limit 20

# 结束会话
openclaw sessions kill <session-id>
```

### 2. 记忆操作
```bash
# 语义搜索记忆
openclaw memory search --query "Polymarket 策略" --limit 5

# 读取记忆片段
openclaw memory get --path memory/core.md --from 10 --lines 20

# 写入记忆
openclaw memory write --path MEMORY.md --content "新内容"
```

### 3. 消息发送
```bash
# 发送消息
openclaw message send --target @user --message "Hello"

# 广播消息
openclaw message broadcast --channel telegram --message "公告内容"

# 发送文件
openclaw message send --target @user --media /path/to/file.pdf
```

### 4. 文件操作
```bash
# 读取文件
openclaw read --path file.md

# 写入文件
openclaw write --path file.md --content "内容"

# 编辑文件
openclaw edit --path file.md --edits '[{"oldText":"旧","newText":"新"}]'
```

### 5. 执行命令
```bash
# 执行 shell 命令
openclaw exec "git status"

# 带超时执行
openclaw exec "npm install" --timeout 120

# 后台执行
openclaw exec "long-task.sh" --background
```

### 6. 网络工具
```bash
# 搜索网络
openclaw web_search --query "关键词" --count 10

# 抓取网页
openclaw web_fetch --url https://example.com --max-chars 5000
```

### 7. 图片生成
```bash
# 生成图片
openclaw image_generate --prompt "赛博朋克城市" --size 1024x1024

# 编辑图片
openclaw image_generate --action edit --image input.jpg --prompt "添加夕阳"
```

### 8. Gateway 管理
```bash
# 查看状态
openclaw gateway status

# 重启 Gateway
openclaw gateway restart

# 查看日志
openclaw logs --follow
```

### 9. Cron 任务
```bash
# 列出定时任务
openclaw cron list

# 添加定时任务
openclaw cron create --schedule "0 6 * * *" --command "daily-constitution.sh"

# 删除定时任务
openclaw cron delete <job-id>
```

### 10. 健康检查
```bash
# 系统自检
openclaw doctor

# 查看配置
openclaw config show

# 查看帮助
openclaw --help
openclaw <command> --help
```

---

## ⌨️ 快捷键

| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `Ctrl+C` | 中断 | 终止当前命令 |
| `Ctrl+D` | EOF | 结束输入 |
| `Ctrl+Z` | 挂起 | 后台运行 |
| `bg` | 恢复后台 | 继续后台执行 |
| `fg` | 恢复前台 | 切回前台执行 |
| `Tab` | 补全 | 命令/参数补全 |
| `Ctrl+R` | 搜索历史 | 需安装 fzf |
| `!!` | 上一条命令 | 快速重复 |
| `!$` | 上个参数 | 引用最后一个参数 |

---

## 🔧 环境变量

| 变量 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `OPENCLAW_HOME` | 主目录 | `~/.openclaw` | `export OPENCLAW_HOME=~/.openclaw` |
| `OPENCLAW_WORKSPACE` | 工作目录 | `~/.openclaw/workspace` | - |
| `OPENCLAW_MODEL` | 默认模型 | `qwen3.5-plus` | `export OPENCLAW_MODEL=gemini-pro` |
| `OPENCLAW_TIMEOUT` | 默认超时 | `300` (秒) | `export OPENCLAW_TIMEOUT=600` |
| `OPENCLAW_VERBOSE` | 详细日志 | `false` | `export OPENCLAW_VERBOSE=true` |
| `OPENCLAW_LOG_LEVEL` | 日志级别 | `info` | `export OPENCLAW_LOG_LEVEL=debug` |

---

## 📁 核心文件路径

| 文件 | 路径 | 用途 |
|------|------|------|
| **主配置** | `~/.openclaw/config.json` | 全局配置 |
| **工作区** | `~/.openclaw/workspace/` | 项目文件 |
| **记忆** | `~/.openclaw/workspace/MEMORY.md` | 长期记忆 |
| **日志** | `~/.openclaw/logs/` | 运行日志 |
| **脚本** | `~/.openclaw/workspace/scripts/` | 自动化脚本 |
| **宪法** | `~/.openclaw/workspace/constitution/` | 规则文件 |
| **报告** | `~/.openclaw/workspace/reports/` | 生成报告 |

---

## 🎯 场景化命令组合

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
openclaw sessions spawn --task "分析数据" --timeout 300 && \
openclaw sessions list --active-minutes 5
```

### 场景 3：记忆整理
```bash
# 搜索 + 读取 + 更新
openclaw memory search --query "任务" && \
openclaw memory get --path memory/core.md && \
openclaw edit --path MEMORY.md --edits '[...]'
```

### 场景 4：消息推送
```bash
# 批量发送
for user in @user1 @user2 @user3; do
  openclaw message send --target $user --message "更新通知"
done
```

### 场景 5：自动化报告
```bash
# 生成并发送日报
bash /opt/openclaw-report.sh daily && \
openclaw message send --target @SAYELF --media reports/daily-report.md
```

---

## 🔐 安全提示

| 风险级别 | 命令类型 | 注意事项 |
|---------|---------|---------|
| 🟢 **LOW** | 只读操作 | `sessions list`, `memory search`, `read` |
| 🟡 **MEDIUM** | 写入操作 | `write`, `edit`, `sessions spawn` |
| 🔴 **HIGH** | 删除/执行 | `exec`, `sessions kill`, `cron delete` |

**安全原则**：
1. 危险命令前先用 `--dry-run` 测试
2. 敏感数据用环境变量，不要硬编码
3. 设置合理超时，避免无限等待
4. 定期备份重要文件

---

## 🆘 故障排查

### 命令找不到
```bash
# 检查 PATH
echo $PATH

# 重新安装
npm install -g openclaw
```

### Gateway 未运行
```bash
# 启动 Gateway
openclaw gateway start

# 查看状态
openclaw gateway status
```

### 认证失败
```bash
# 重新配置
openclaw configure

# 检查配置
openclaw config show
```

### 上下文超限
```bash
# 结束当前会话
openclaw sessions yield

# 压缩记忆
openclaw memory search --query "压缩" --limit 5
```

---

## 📚 学习路径

### 第 1 周：基础命令
- [ ] `sessions list/spawn`
- [ ] `memory search/get`
- [ ] `message send`
- [ ] `read/write`

### 第 2 周：自动化
- [ ] `exec` 执行脚本
- [ ] `cron` 定时任务
- [ ] 管道组合命令

### 第 3 周：高级用法
- [ ] 环境变量配置
- [ ] 自定义脚本
- [ ] 工作流设计

### 第 4 周：贡献
- [ ] 提交命令改进建议
- [ ] 编写新脚本
- [ ] 分享工作流案例

---

*速查表版本：v1.0 | 最后更新：2026-04-02 07:00 | 太一 AGI*

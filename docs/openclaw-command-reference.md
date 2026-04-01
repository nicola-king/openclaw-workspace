# OpenClaw CLI 命令参考手册

> 完整命令列表 | 版本：v1.0 | 更新时间：2026-04-02

---

## 📖 使用说明

本手册列出所有 OpenClaw CLI 命令及其用途，配合 `--help` 使用。

**查看命令帮助**：
```bash
openclaw <command> --help
```

---

## 🎯 核心命令

### sessions - 会话管理

| 子命令 | 用途 | 示例 |
|--------|------|------|
| `list` | 查看所有会话 | `openclaw sessions list --limit 10` |
| `spawn` | 启动新会话 | `openclaw sessions spawn --task "分析数据" --runtime subagent` |
| `kill` | 结束会话 | `openclaw sessions kill <session-id>` |
| `history` | 查看会话历史 | `openclaw sessions history --session-key <key>` |
| `send` | 发送消息到会话 | `openclaw sessions send --session-key <key> --message "Hello"` |

**常用选项**：
- `--limit <n>` - 限制结果数量
- `--active-minutes <n>` - 只显示最近活跃的会话
- `--task <text>` - 任务描述
- `--runtime <subagent|acp>` - 运行时类型
- `--timeout <seconds>` - 超时时间

---

### memory - 记忆操作

| 子命令 | 用途 | 示例 |
|--------|------|------|
| `search` | 语义搜索 | `openclaw memory search --query "Polymarket"` |
| `get` | 读取片段 | `openclaw memory get --path memory/core.md --lines 50` |
| `write` | 写入内容 | `openclaw memory write --path MEMORY.md --content "新内容"` |

**常用选项**：
- `--query <text>` - 搜索关键词
- `--limit <n>` - 最大结果数
- `--path <path>` - 文件路径
- `--from <line>` - 起始行号
- `--lines <n>` - 读取行数

---

### message - 消息发送

| 子命令 | 用途 | 示例 |
|--------|------|------|
| `send` | 发送消息 | `openclaw message send --target @user --message "Hello"` |
| `broadcast` | 广播消息 | `openclaw message broadcast --channel telegram --message "公告"` |
| `react` | 添加反应 | `openclaw message react --emoji 👍` |
| `reply` | 回复消息 | `openclaw message reply --to <msg-id> --message "回复内容"` |

**常用选项**：
- `--target <user>` - 目标用户
- `--message <text>` - 消息内容
- `--channel <name>` - 频道名称
- `--media <path>` - 附件路径
- `--emoji <emoji>` - 表情符号

---

### file - 文件操作

| 子命令 | 用途 | 示例 |
|--------|------|------|
| `read` | 读取文件 | `openclaw read --path file.md` |
| `write` | 写入文件 | `openclaw write --path file.md --content "内容"` |
| `edit` | 编辑文件 | `openclaw edit --path file.md --edits '[...]'` |

**常用选项**：
- `--path <path>` - 文件路径
- `--content <text>` - 文件内容
- `--edits <json>` - 编辑操作（JSON 格式）

---

### exec - 执行命令

| 子命令 | 用途 | 示例 |
|--------|------|------|
| `exec` | 执行 shell 命令 | `openclaw exec "git status"` |

**常用选项**：
- `--timeout <seconds>` - 超时时间
- `--background` - 后台执行
- `--workdir <path>` - 工作目录

---

### web - 网络工具

| 子命令 | 用途 | 示例 |
|--------|------|------|
| `search` | 搜索网络 | `openclaw web_search --query "关键词" --count 10` |
| `fetch` | 抓取网页 | `openclaw web_fetch --url https://example.com` |

**常用选项**：
- `--query <text>` - 搜索词
- `--count <n>` - 结果数量
- `--url <url>` - 网页 URL
- `--max-chars <n>` - 最大字符数

---

### image - 图片生成

| 子命令 | 用途 | 示例 |
|--------|------|------|
| `generate` | 生成图片 | `openclaw image_generate --prompt "描述" --size 1024x1024` |
| `edit` | 编辑图片 | `openclaw image_generate --action edit --image input.jpg --prompt "修改"` |

**常用选项**：
- `--prompt <text>` - 描述词
- `--size <WxH>` - 图片尺寸
- `--count <n>` - 生成数量
- `--image <path>` - 参考图片

---

### gateway - Gateway 管理

| 子命令 | 用途 | 示例 |
|--------|------|------|
| `status` | 查看状态 | `openclaw gateway status` |
| `start` | 启动服务 | `openclaw gateway start` |
| `stop` | 停止服务 | `openclaw gateway stop` |
| `restart` | 重启服务 | `openclaw gateway restart` |

---

### cron - 定时任务

| 子命令 | 用途 | 示例 |
|--------|------|------|
| `list` | 列出任务 | `openclaw cron list` |
| `create` | 创建任务 | `openclaw cron create --schedule "0 6 * * *" --command "script.sh"` |
| `delete` | 删除任务 | `openclaw cron delete <job-id>` |

**常用选项**：
- `--schedule <cron>` - Cron 表达式
- `--command <cmd>` - 执行命令

---

### doctor - 健康检查

| 子命令 | 用途 | 示例 |
|--------|------|------|
| `doctor` | 系统自检 | `openclaw doctor` |

**检查项目**：
- Gateway 状态
- 通道连接
- 配置文件
- 系统资源

---

### config - 配置管理

| 子命令 | 用途 | 示例 |
|--------|------|------|
| `show` | 查看配置 | `openclaw config show` |
| `get` | 获取配置项 | `openclaw config get <key>` |
| `set` | 设置配置项 | `openclaw config set <key> <value>` |
| `unset` | 删除配置项 | `openclaw config unset <key>` |

---

### logs - 日志查看

| 子命令 | 用途 | 示例 |
|--------|------|------|
| `logs` | 查看日志 | `openclaw logs --follow` |

**常用选项**：
- `--follow` - 持续输出
- `--lines <n>` - 显示行数

---

## 🔧 全局选项

| 选项 | 用途 | 示例 |
|------|------|------|
| `--help` | 显示帮助 | `openclaw --help` |
| `--version` | 显示版本 | `openclaw --version` |
| `--profile <name>` | 使用配置档 | `openclaw --profile dev` |
| `--dev` | 开发模式 | `openclaw --dev` |
| `--log-level <level>` | 日志级别 | `openclaw --log-level debug` |
| `--no-color` | 禁用颜色 | `openclaw --no-color` |

---

## 📊 命令分类

### 高频命令（每日使用）
1. `sessions list/spawn`
2. `memory search/get`
3. `message send`
4. `read/write`
5. `gateway status`

### 中频命令（每周使用）
1. `exec`
2. `cron list/create`
3. `web_search/fetch`
4. `config show/set`

### 低频命令（按需使用）
1. `image_generate`
2. `sessions kill/history`
3. `logs`
4. `doctor`

---

## 🎯 场景化命令组合

### 场景 1：日常检查
```bash
openclaw gateway status && \
openclaw sessions list --limit 5 && \
openclaw memory search --query "待办" --limit 3
```

### 场景 2：任务执行
```bash
openclaw sessions spawn --task "分析数据" --timeout 300 && \
openclaw sessions list --active-minutes 5
```

### 场景 3：记忆整理
```bash
openclaw memory search --query "任务" && \
openclaw memory get --path memory/core.md && \
openclaw edit --path MEMORY.md --edits '[...]'
```

### 场景 4：消息推送
```bash
for user in @user1 @user2 @user3; do
  openclaw message send --target $user --message "更新通知"
done
```

### 场景 5：自动化报告
```bash
bash /opt/openclaw-report.sh daily && \
openclaw message send --target @SAYELF --media reports/daily-report.md
```

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
openclaw memory search --query "压缩"
```

---

## 📚 进阶资源

- [CLI 最佳实践](docs/openclaw-cli-best-practices.md)
- [CLI 速查表](docs/CLI-CHEATSHEET-README.md)
- [工作流案例](docs/automation-workflow-examples.md)
- [HEARTBEAT CLI](scripts/heartbeat-cli.sh)

---

*命令参考手册 | 版本：v1.0 | 最后更新：2026-04-02 | 太一 AGI*

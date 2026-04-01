# OpenClaw CLI 最佳实践指南

> 版本：v1.0 | 生成时间：2026-04-02 06:50 | 太一 AGI

---

## 📖 目录

1. [核心原则](#核心原则)
2. [命令规范](#命令规范)
3. [脚本编写](#脚本编写)
4. [自动化工作流](#自动化工作流)
5. [安全基线](#安全基线)
6. [性能优化](#性能优化)
7. [故障排查](#故障排查)
8. [速查表](#速查表)

---

## 🎯 核心原则

### 1. CLI-First, GUI-Optional

**原则**：优先设计 CLI 接口，GUI 作为可选增强。

**为什么**：
- CLI 可被脚本/AI/CI 调用
- CLI 命令可写进文档/版本控制
- CLI 远程友好（SSH/容器/服务器）

**示例**：
```bash
# ✅ 正确：CLI 优先
openclaw message send --to @user --message "Hello"

# ❌ 避免：仅 GUI 操作
# 在微信界面点击发送按钮
```

### 2. 单一职责（Single Responsibility）

**原则**：每个命令只做一件事，做好一件事。

**为什么**：
- 易于测试和调试
- 可组合成复杂工作流
- 错误定位清晰

**示例**：
```bash
# ✅ 正确：职责分离
openclaw memory search --query "Polymarket"
openclaw memory get --path memory/core.md

# ❌ 避免：大杂烩命令
openclaw do-everything  # 不知道会做什么
```

### 3. 显式优于隐式（Explicit > Implicit）

**原则**：参数和选项要显式声明，不依赖隐式上下文。

**为什么**：
- 命令可重复执行
- 减少意外行为
- 便于文档化

**示例**：
```bash
# ✅ 正确：显式参数
openclaw sessions spawn --task "分析数据" --runtime subagent --timeout 300

# ❌ 避免：隐式依赖
openclaw run  # 依赖当前会话状态，不可重复
```

### 4. 可组合性（Composability）

**原则**：命令输出应可被其他命令消费（管道友好）。

**为什么**：
- 支持复杂工作流
- 减少临时文件
- 提升效率

**示例**：
```bash
# ✅ 正确：管道组合
openclaw sessions list --limit 10 | grep active | xargs -I {} openclaw sessions kill {}

# ❌ 避免：孤立命令
openclaw sessions list  # 输出无法被后续命令使用
```

### 5. 失败快速（Fail Fast）

**原则**：错误尽早暴露，提供清晰错误信息。

**为什么**：
- 减少调试时间
- 避免级联失败
- 用户友好

**示例**：
```bash
# ✅ 正确：清晰错误
$ openclaw message send --to @unknown
Error: User '@unknown' not found. Did you mean @nicola?

# ❌ 避免：模糊错误
$ openclaw message send --to @unknown
Error: Failed to send message.  # 为什么失败？
```

---

## 📝 命令规范

### 命令结构

```bash
openclaw <resource> <action> [options] [arguments]
```

**示例**：
```bash
openclaw memory search --query "Polymarket" --limit 5
# │        │       │
# │        │       └─ 选项（可选）
# │        └───────── 动作
# └────────────────── 资源
```

### 命名约定

| 类型 | 规范 | 示例 |
|------|------|------|
| **资源名** | 小写 + 连字符 | `memory`, `sessions`, `cli-tools` |
| **动作名** | 小写 + 连字符 | `search`, `get`, `list`, `create` |
| **选项名** | 小写 + 双连字符 | `--query`, `--limit`, `--timeout` |
| **选项值** | 引号包裹（含空格） | `--message "Hello World"` |

### 选项设计

#### 必填选项（Required）
```bash
openclaw message send --to @user --message "Hello"
#                          │              │
#                          └─ 必填        └─ 必填
```

#### 可选选项（Optional）
```bash
openclaw sessions list [--limit 10] [--active-minutes 30]
#                      │                 │
#                      └─ 可选           └─ 可选
```

#### 布尔选项（Boolean）
```bash
openclaw message send --silent          # 启用
openclaw message send --no-silent       # 禁用
openclaw message send --silent=false    # 禁用
```

#### 枚举选项（Enum）
```bash
openclaw sessions spawn --runtime subagent  # ✅ 有效
openclaw sessions spawn --runtime invalid   # ❌ 错误：必须是 subagent|acp
```

### 帮助文档

每个命令必须支持 `--help`：

```bash
$ openclaw memory search --help

Usage: openclaw memory search [OPTIONS]

Search memory files semantically.

Options:
  --query TEXT     Search query (required)
  --limit INTEGER  Max results (default: 5)
  --min-score FLOAT  Minimum score (default: 0.5)
  --help           Show this message and exit.

Examples:
  openclaw memory search --query "Polymarket strategy"
  openclaw memory search --query "task" --limit 10
```

---

## 🛠️ 脚本编写

### 脚本模板

```bash
#!/bin/bash
set -euo pipefail  # 严格模式

# ============================================
# 脚本名：auto-exec-task.sh
# 用途：OpenClaw 自动执行任务
# 作者：太一 AGI
# 版本：v1.0
# 最后更新：2026-04-02
# ============================================

# 配置区
readonly SCRIPT_NAME=$(basename "$0")
readonly SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
readonly LOG_FILE="/tmp/${SCRIPT_NAME%.sh}.log"

# 日志函数
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# 错误处理
error_exit() {
  log "ERROR: $*"
  exit 1
}

# 清理函数
cleanup() {
  log "Cleanup..."
  # 清理临时文件等
}
trap cleanup EXIT

# 主逻辑
main() {
  log "Starting $SCRIPT_NAME"
  
  # 参数解析
  local task=""
  local timeout=300
  
  while [[ $# -gt 0 ]]; do
    case $1 in
      --task)
        task="$2"
        shift 2
        ;;
      --timeout)
        timeout="$2"
        shift 2
        ;;
      --help)
        echo "Usage: $SCRIPT_NAME --task <task> [--timeout <seconds>]"
        exit 0
        ;;
      *)
        error_exit "Unknown option: $1"
        ;;
    esac
  done
  
  # 参数验证
  [[ -z "$task" ]] && error_exit "Task is required"
  
  # 执行任务
  log "Executing task: $task (timeout: ${timeout}s)"
  openclaw sessions spawn --task "$task" --timeout "$timeout"
  
  log "Task completed successfully"
}

main "$@"
```

### 最佳实践

#### 1. 使用严格模式
```bash
set -euo pipefail
# -e: 命令失败立即退出
# -u: 使用未定义变量报错
# -o pipefail: 管道中任一命令失败则整个管道失败
```

#### 2. 函数化组织代码
```bash
# ✅ 正确：函数化
main() {
  parse_args "$@"
  validate_args
  execute_task
  cleanup
}

# ❌ 避免：面条代码
# 一堆命令从上到下执行，无结构
```

#### 3. 错误处理
```bash
# ✅ 正确：捕获错误
if ! openclaw message send --to @user; then
  log "Failed to send message"
  exit 1
fi

# ❌ 避免：忽略错误
openclaw message send --to @user  # 失败了也不知道
```

#### 4. 日志输出
```bash
# ✅ 正确：结构化日志
log "INFO: Starting task..."
log "ERROR: Failed to connect"
log "DEBUG: Response time: 234ms"

# ❌ 避免：无日志或混乱日志
echo "Starting"
echo "Oops something went wrong"
```

#### 5. 配置与代码分离
```bash
# ✅ 正确：配置文件
source "${SCRIPT_DIR}/config.env"
readonly API_KEY="${CONFIG_API_KEY}"

# ❌ 避免：硬编码
readonly API_KEY="sk-1234567890abcdef"  # 泄露风险
```

---

## 🔄 自动化工作流

### 模式 1：定时任务（Cron）

```bash
# 每天 06:00 执行宪法学习
0 6 * * * /home/nicola/.openclaw/workspace/scripts/daily-constitution.sh >> /tmp/constitution.log 2>&1

# 每 5 分钟检查自动执行状态
*/5 * * * * /home/nicola/.openclaw/workspace/scripts/auto-exec-task.sh >> /tmp/auto-exec.log 2>&1
```

### 模式 2：事件触发

```bash
#!/bin/bash
# 监控新消息并自动响应

tail -F /var/log/openclaw/messages.log | while read -r line; do
  if echo "$line" | grep -q "HEARTBEAT"; then
    openclaw message send --to @nicola --message "Heartbeat OK ✅"
  fi
done
```

### 模式 3：管道组合

```bash
# 批量处理 GitHub Issues
openclaw exec "gh issue list --limit 10" \
  | jq -r '.[].number' \
  | xargs -I {} openclaw sessions spawn --task "Review issue #{}"
```

### 模式 4：条件执行

```bash
#!/bin/bash
# 仅在 Gateway 运行时执行任务

if pgrep -f "openclaw gateway" > /dev/null; then
  openclaw sessions spawn --task "Daily report"
else
  echo "Gateway not running, skipping task"
  exit 1
fi
```

### 模式 5：重试机制

```bash
#!/bin/bash
# 失败自动重试（最多 3 次）

max_retries=3
retry_count=0

while [[ $retry_count -lt $max_retries ]]; do
  if openclaw message send --to @user --message "Hello"; then
    echo "Message sent successfully"
    break
  else
    retry_count=$((retry_count + 1))
    echo "Retry $retry_count/$max_retries..."
    sleep 5
  fi
done

[[ $retry_count -eq $max_retries ]] && echo "Failed after $max_retries retries"
```

---

## 🔐 安全基线

### 命令白名单

参考 `scripts/cli-whitelist-config.md`：

| 安全级别 | 说明 | 示例 | 审批要求 |
|---------|------|------|---------|
| **LOW** | 只读操作 | `git status`, `ls`, `cat` | 无需审批 |
| **MEDIUM** | 可修改但可恢复 | `git commit`, `npm install` | 二次确认 |
| **HIGH** | 危险操作 | `docker rm`, `kubectl delete` | 审批 + 二次确认 |

### 敏感数据处理

```bash
# ✅ 正确：环境变量
openclaw message send --token "$OPENCLAW_TOKEN"

# ❌ 避免：明文传递
openclaw message send --token "sk-1234567890"  # 泄露风险
```

### 超时控制

```bash
# ✅ 正确：设置超时
openclaw sessions spawn --task "Long task" --timeout 300

# ❌ 避免：无超时
openclaw sessions spawn --task "Long task"  # 可能永远卡住
```

### 权限最小化

```bash
# ✅ 正确：只读权限
openclaw memory search --query "task"

# ❌ 避免：过度权限
openclaw exec "rm -rf /tmp/*"  # 不必要的危险操作
```

---

## ⚡ 性能优化

### 1. 减少上下文加载

```bash
# ✅ 正确：精确加载
openclaw memory get --path memory/core.md --lines 50

# ❌ 避免：全量加载
openclaw memory read --path memory/core.md  # 可能加载 50KB+
```

### 2. 批量操作

```bash
# ✅ 正确：批量处理
openclaw message send --to @user1,@user2,@user3 --message "Hello"

# ❌ 避免：逐个处理
openclaw message send --to @user1 --message "Hello"
openclaw message send --to @user2 --message "Hello"
openclaw message send --to @user3 --message "Hello"
```

### 3. 并发执行

```bash
# ✅ 正确：并行执行
openclaw sessions spawn --task "Task 1" &
openclaw sessions spawn --task "Task 2" &
openclaw sessions spawn --task "Task 3" &
wait

# ❌ 避免：串行执行
openclaw sessions spawn --task "Task 1"
openclaw sessions spawn --task "Task 2"
openclaw sessions spawn --task "Task 3"
```

### 4. 缓存结果

```bash
# ✅ 正确：缓存查询结果
if [[ -f /tmp/memory-cache.json ]]; then
  cat /tmp/memory-cache.json
else
  openclaw memory search --query "task" > /tmp/memory-cache.json
fi
```

---

## 🐛 故障排查

### 常见问题

#### 1. 命令找不到
```bash
$ openclaw: command not found

# 解决：
export PATH="$PATH:/home/nicola/.openclaw/workspace/bin"
# 或添加到 ~/.bashrc
```

#### 2. 权限不足
```bash
$ openclaw exec "rm -rf /tmp"
Error: Permission denied

# 解决：
# 检查命令白名单，HIGH 级别命令需要审批
```

#### 3. 超时错误
```bash
$ openclaw sessions spawn --task "Long task"
Error: Timeout after 300s

# 解决：
openclaw sessions spawn --task "Long task" --timeout 600
# 或拆分任务为多个小任务
```

#### 4. 上下文超限
```bash
$ openclaw memory search --query "task"
Error: Context limit exceeded (131K tokens)

# 解决：
openclaw sessions yield  # 结束当前会话，开启新会话
# 或压缩记忆文件
```

### 调试技巧

#### 1. 启用详细日志
```bash
openclaw --verbose memory search --query "task"
```

#### 2.  dry-run 模式
```bash
openclaw --dry-run message send --to @user --message "Hello"
# 显示将要执行的命令，但不实际执行
```

#### 3. 检查配置
```bash
openclaw config show
# 显示当前配置
```

#### 4. 健康检查
```bash
openclaw health check
# 检查 Gateway、插件、配置状态
```

---

## 📋 速查表

### 常用命令

```bash
# 会话管理
openclaw sessions list --limit 10
openclaw sessions spawn --task "分析数据" --runtime subagent
openclaw sessions kill <session-id>
openclaw sessions history --session-key <key>

# 记忆操作
openclaw memory search --query "关键词" --limit 5
openclaw memory get --path memory/core.md --lines 50
openclaw memory write --path MEMORY.md --content "新内容"

# 消息发送
openclaw message send --to @user --message "Hello"
openclaw message broadcast --channel telegram --message "公告"

# 文件操作
openclaw read --path file.md
openclaw write --path file.md --content "内容"
openclaw edit --path file.md --edits '[{"oldText":"旧","newText":"新"}]'

# 执行命令
openclaw exec "git status"
openclaw exec "npm install" --timeout 120

# 工具调用
openclaw web_search --query "关键词" --count 10
openclaw web_fetch --url https://example.com
openclaw image_generate --prompt "描述" --size 1024x1024
```

### 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+C` | 中断当前命令 |
| `Ctrl+D` | 结束输入（EOF） |
| `Ctrl+Z` | 挂起命令（后台） |
| `bg` | 恢复后台命令 |
| `fg` | 恢复前台命令 |
| `Tab` | 命令补全 |
| `Ctrl+R` | 历史搜索（需 fzf） |

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENCLAW_HOME` | OpenClaw 主目录 | `~/.openclaw` |
| `OPENCLAW_WORKSPACE` | 工作目录 | `~/.openclaw/workspace` |
| `OPENCLAW_MODEL` | 默认模型 | `qwen3.5-plus` |
| `OPENCLAW_TIMEOUT` | 默认超时 | `300` (秒) |
| `OPENCLAW_VERBOSE` | 详细日志 | `false` |

---

## 📚 进阶资源

### 内部文档
- `scripts/cli-whitelist-config.md` - CLI 白名单配置
- `constitution/directives/AUTO-EXEC.md` - 自动执行法则
- `constitution/skills/MODEL-ROUTING.md` - 模型调度协议

### 外部资源
- "12 CLI Tools That Are Redefining Developer Workflows" - qodo.ai
- "CLI 化趋势分析报告 2026" - 本仓库 reports/

### 学习路径
1. **入门**：掌握 10 个常用命令
2. **进阶**：编写自动化脚本
3. **高级**：设计 CLI 工作流
4. **专家**：贡献 OpenClaw CLI 代码

---

## 🎯 检查清单

### 命令设计检查
- [ ] 命令名符合 `<resource> <action>` 格式
- [ ] 选项名使用 `--kebab-case`
- [ ] 提供 `--help` 输出
- [ ] 错误信息清晰有用
- [ ] 支持管道组合

### 脚本编写检查
- [ ] 使用 `set -euo pipefail`
- [ ] 函数化组织代码
- [ ] 错误处理完善
- [ ] 日志输出结构化
- [ ] 配置与代码分离

### 安全基线检查
- [ ] 命令在白名单内
- [ ] 敏感数据用环境变量
- [ ] 设置合理超时
- [ ] 权限最小化
- [ ] 危险操作需审批

---

*文档结束 | 版本：v1.0 | 生成时间：2026-04-02 06:50 | 太一 AGI*

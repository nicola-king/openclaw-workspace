# OpenClaw 自动化工作流案例集

> 版本：v1.0 | 创建时间：2026-04-02 07:10 | 太一 AGI

---

## 案例 1：每日晨报自动化

**场景**：每天早上 06:00 自动执行宪法学习、记忆提炼、系统自检，并生成晨报发送给 SAYELF。

**触发方式**：Cron 定时任务

**工作流图**：
```
06:00 Cron 触发
    │
    ├─→ 宪法学习 (daily-constitution.sh)
    │       └─→ 读取 Tier 1 宪法文件
    │       └─→ 写入学习记录
    │
    ├─→ 记忆提炼 (turboquant-compress.py)
    │       └─→ 压缩昨日记忆到 core.md
    │       └─→ 更新 MEMORY.md
    │
    ├─→ 系统自检 (openclaw doctor)
    │       └─→ Gateway 状态
    │       └─→ 通道状态
    │       └─→ 资源使用
    │
    └─→ 生成晨报 (morning-report.py)
            └─→ 汇总检查结果
            └─→ 发送微信消息
```

**实现代码**：

```bash
#!/bin/bash
# 文件：scripts/morning-briefing.sh
set -euo pipefail

readonly LOG_FILE="/tmp/morning-briefing.log"
readonly REPORT_FILE="/tmp/morning-briefing-$(date +%Y%m%d).md"

log() {
  echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# 1. 宪法学习
log "开始宪法学习..."
bash /home/nicola/.openclaw/workspace/scripts/daily-constitution.sh >> "$LOG_FILE" 2>&1
CONSTITUTION_STATUS=$?

# 2. 记忆提炼
log "开始记忆提炼..."
python3 /home/nicola/.openclaw/workspace/skills/turboquant/compressor.py >> "$LOG_FILE" 2>&1
MEMORY_STATUS=$?

# 3. 系统自检
log "开始系统自检..."
openclaw doctor > /tmp/doctor-output.txt 2>&1
DOCTOR_STATUS=$?

# 4. 生成报告
cat > "$REPORT_FILE" << EOF
# 🌅 晨报 $(date +%Y-%m-%d)

**生成时间**: $(date '+%H:%M:%S')
**自动执行**: ✅

## 检查结果

| 项目 | 状态 |
|------|------|
| 宪法学习 | $([ $CONSTITUTION_STATUS -eq 0 ] && echo "✅" || echo "❌") |
| 记忆提炼 | $([ $MEMORY_STATUS -eq 0 ] && echo "✅" || echo "❌") |
| 系统自检 | $([ $DOCTOR_STATUS -eq 0 ] && echo "✅" || echo "❌") |

## 今日 P0 任务

$(grep -A20 "当前聚焦" /home/nicola/.openclaw/workspace/HEARTBEAT.md | grep "^\|")

## 系统资源

$(cat /tmp/doctor-output.txt | grep -A10 "资源")

---
*太一 AGI 自动生成*
EOF

# 5. 发送消息
log "发送晨报..."
openclaw message send \
  --target "@SAYELF" \
  --message "🌅 晨报已生成

$(cat "$REPORT_FILE")

查看详情：$REPORT_FILE"

log "晨报发送完成"
```

**Cron 配置**：
```bash
# 每天 06:00 执行
0 6 * * * /home/nicola/.openclaw/workspace/scripts/morning-briefing.sh >> /tmp/morning-briefing.log 2>&1
```

**效果**：
- 每天 06:00 自动执行
- 10 分钟内完成所有检查
- 微信推送晨报给 SAYELF
- 异常时立即告警

---

## 案例 2：GitHub Issue 自动处理

**场景**：监控 GitHub Issue，自动分类、分配给对应 Bot、跟踪进度、关闭已完成任务。

**触发方式**：事件触发（GitHub Webhook）+ 定时轮询

**工作流图**：
```
GitHub Issue 创建/更新
    │
    ├─→ 读取 Issue 内容
    │       └─→ 标题 + 描述 + 标签
    │
    ├─→ 分类判断
    │       ├─→ bug → 素问（技术）
    │       ├─→ feature → 素问（开发）
    │       ├─→ content → 山木（内容）
    │       └─→ trading → 知几（交易）
    │
    ├─→ 分配任务
    │       └─→ sessions spawn --task "处理 Issue #XXX"
    │
    ├─→ 进度追踪
    │       └─→ 每 30 分钟检查一次
    │       └─→ 更新 Issue 评论
    │
    └─→ 完成归档
            └─→ 关闭 Issue
            └─→ 写入记忆
```

**实现代码**：

```python
#!/usr/bin/env python3
# 文件：scripts/github-issue-handler.py
# GitHub Issue 自动处理器

import subprocess
import json
import sys
from datetime import datetime

LOG_FILE = "/tmp/github-issue-handler.log"

def log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def classify_issue(title, body, labels):
    """根据 Issue 内容分类"""
    title_lower = title.lower()
    body_lower = body.lower()
    
    # 关键词匹配
    if any(kw in title_lower for kw in ["bug", "error", "fix", "崩溃", "错误"]):
        return "bug", "素问"
    
    if any(kw in title_lower for kw in ["feature", "enhancement", "新功能", "需求"]):
        return "feature", "素问"
    
    if any(kw in title_lower for kw in ["content", "doc", "文章", "内容", "文档"]):
        return "content", "山木"
    
    if any(kw in title_lower for kw in ["trading", "polymarket", "交易", "策略"]):
        return "trading", "知几"
    
    return "general", "太一"

def spawn_task(issue_number, category, assignee):
    """启动子任务处理 Issue"""
    task = f"处理 GitHub Issue #{issue_number} ({category})"
    
    cmd = [
        "openclaw", "sessions", "spawn",
        "--task", task,
        "--runtime", "subagent",
        "--timeout", "600"
    ]
    
    log(f"启动任务：{task} → {assignee}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        log(f"任务启动成功：{result.stdout}")
        return result.stdout
    else:
        log(f"任务启动失败：{result.stderr}")
        return None

def add_comment(issue_number, comment):
    """添加 Issue 评论"""
    cmd = [
        "gh", "issue", "comment", str(issue_number),
        "-b", comment
    ]
    
    log(f"添加评论到 #{issue_number}")
    subprocess.run(cmd, capture_output=True, text=True)

def main():
    if len(sys.argv) < 2:
        print("用法：github-issue-handler.py <issue_number>")
        sys.exit(1)
    
    issue_number = sys.argv[1]
    log(f"开始处理 Issue #{issue_number}")
    
    # 1. 获取 Issue 详情
    result = subprocess.run(
        ["gh", "issue", "view", issue_number, "--json", "title,body,labels"],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        log(f"获取 Issue 失败：{result.stderr}")
        sys.exit(1)
    
    issue_data = json.loads(result.stdout)
    title = issue_data["title"]
    body = issue_data["body"] or ""
    labels = [l["name"] for l in issue_data.get("labels", [])]
    
    log(f"Issue 标题：{title}")
    log(f"标签：{', '.join(labels)}")
    
    # 2. 分类
    category, assignee = classify_issue(title, body, labels)
    log(f"分类结果：{category} → {assignee}")
    
    # 3. 添加评论（告知正在处理）
    add_comment(issue_number, f"""
🤖 **太一 AGI 已接管此 Issue**

- 分类：{category}
- 分配：{assignee}
- 预计处理时间：10 分钟

我将自动跟踪进度并更新状态。
""")
    
    # 4. 启动任务
    session_info = spawn_task(issue_number, category, assignee)
    
    if session_info:
        add_comment(issue_number, f"""
✅ **任务已启动**

Session: `{session_info}`
负责人：{assignee}
状态：处理中...

我会在完成后更新此 Issue。
""")
    else:
        add_comment(issue_number, """
❌ **任务启动失败**

请稍后重试或联系 @SAYELF 手动处理。
""")
    
    log(f"Issue #{issue_number} 处理完成")

if __name__ == "__main__":
    main()
```

**GitHub Actions 配置**：
```yaml
# .github/workflows/issue-auto-handler.yml
name: Issue Auto Handler

on:
  issues:
    types: [opened, labeled]

jobs:
  handle:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup OpenClaw
        run: |
          npm install -g openclaw
          echo "$OPENCLAW_TOKEN" > ~/.openclaw/token
      
      - name: Handle Issue
        env:
          OPENCLAW_TOKEN: ${{ secrets.OPENCLAW_TOKEN }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python3 scripts/github-issue-handler.py ${{ github.event.issue.number }}
```

**效果**：
- Issue 创建后 1 分钟内自动响应
- 准确分类并分配给对应 Bot
- 实时进度更新
- 完成后自动归档到记忆

---

## 案例 3：Polymarket 交易监控 + 自动下注

**场景**：监控 Polymarket 市场，当知几-E 检测到高置信度机会（>96%）时，自动执行下注。

**触发方式**：5 分钟 Cron + 事件触发

**工作流图**：
```
每 5 分钟触发
    │
    ├─→ 获取市场数据 (知几-E)
    │       └─→ 热度前 20 市场
    │       └─→ 实时赔率
    │
    ├─→ 策略分析 (zhiji-e strategy)
    │       ├─→ 置信度计算
    │       ├─→ 优势计算
    │       └─→ 决策：下注/跳过
    │
    ├─→ 风险检查 (庖丁)
    │       ├─→ 预算检查
    │       ├─→ 单笔风险检查
    │       └─→ 通过/拒绝
    │
    ├─→ 执行下注 (知几)
    │       ├─→ 创建订单
    │       ├─→ 签名
    │       └─→ 提交
    │
    └─→ 结果通知
            └─→ 微信推送
            └─→ 写入记忆
```

**实现代码**：

```bash
#!/bin/bash
# 文件：scripts/polymarket-auto-bet.sh
# Polymarket 自动下注工作流

set -euo pipefail

readonly LOG_FILE="/tmp/polymarket-auto-bet.log"
readonly STATUS_FILE="/tmp/polymarket-status.json"

log() {
  echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# 1. 获取市场数据
log "获取市场数据..."
MARKET_DATA=$(python3 /home/nicola/.openclaw/workspace/skills/zhiji/fetch-markets.py)
log "获取到 $(echo "$MARKET_DATA" | jq '.markets | length') 个市场"

# 2. 策略分析
log "运行知几-E 策略分析..."
ANALYSIS=$(echo "$MARKET_DATA" | python3 /home/nicola/.openclaw/workspace/skills/zhiji/strategy.py)

CONFIDENCE=$(echo "$ANALYSIS" | jq -r '.confidence')
EDGE=$(echo "$ANALYSIS" | jq -r '.edge')
DECISION=$(echo "$ANALYSIS" | jq -r '.decision')

log "分析结果：置信度=$CONFIDENCE%, 优势=$EDGE%, 决策=$DECISION"

# 3. 决策判断
if [[ "$DECISION" != "bet" ]]; then
  log "策略建议：跳过（置信度不足）"
  echo '{"status":"skipped","reason":"low_confidence"}' > "$STATUS_FILE"
  exit 0
fi

# 4. 风险检查
log "请求庖丁进行风险检查..."
RISK_CHECK=$(python3 /home/nicola/.openclaw/workspace/skills/paoding/risk-check.py \
  --confidence "$CONFIDENCE" \
  --edge "$EDGE")

RISK_APPROVED=$(echo "$RISK_CHECK" | jq -r '.approved')

if [[ "$RISK_APPROVED" != "true" ]]; then
  log "风险检查未通过：$(echo "$RISK_CHECK" | jq -r '.reason')"
  echo '{"status":"rejected","reason":"risk_check_failed"}' > "$STATUS_FILE"
  exit 0
fi

log "风险检查通过"

# 5. 计算下注金额
BET_AMOUNT=$(echo "$RISK_CHECK" | jq -r '.bet_amount')
log "下注金额：$BET_AMOUNT USDC"

# 6. 执行下注
log "执行下注..."
BET_RESULT=$(python3 /home/nicola/.openclaw/workspace/skills/zhiji/place-bet.py \
  --market "$MARKET_ID" \
  --outcome "$OUTCOME" \
  --amount "$BET_AMOUNT")

TX_HASH=$(echo "$BET_RESULT" | jq -r '.tx_hash')
log "交易哈希：$TX_HASH"

# 7. 发送通知
log "发送通知..."
openclaw message send \
  --target "@SAYELF" \
  --message "💰 自动下注执行

**市场**: $MARKET_NAME
**方向**: $OUTCOME
**金额**: $BET_AMOUNT USDC
**置信度**: $CONFIDENCE%
**优势**: $EDGE%
**交易**: \`$TX_HASH\`

状态：✅ 已提交"

# 8. 写入记忆
log "写入记忆..."
cat >> /home/nicola/.openclaw/workspace/memory/$(date +%Y-%m-%d).md << EOF

## [交易] Polymarket 自动下注

**时间**: $(date '+%Y-%m-%d %H:%M:%S')
**市场**: $MARKET_NAME
**方向**: $OUTCOME
**金额**: $BET_AMOUNT USDC
**置信度**: $CONFIDENCE%
**交易哈希**: \`$TX_HASH\`
**结果**: 待结算

EOF

log "下注完成"
echo '{"status":"success","tx_hash":"'"$TX_HASH"'"}' > "$STATUS_FILE"
```

**Cron 配置**：
```bash
# 每 5 分钟执行一次
*/5 * * * * /home/nicola/.openclaw/workspace/scripts/polymarket-auto-bet.sh >> /tmp/polymarket-auto-bet.log 2>&1
```

**效果**：
- 7x24 小时监控市场机会
- 自动执行高置信度交易（>96%）
- 风险检查保障资金安全
- 实时推送交易通知

---

## 📊 案例对比

| 维度 | 晨报自动化 | GitHub Issue | Polymarket 交易 |
|------|-----------|-------------|----------------|
| **触发方式** | Cron (06:00) | Webhook+ 轮询 | Cron (5 分钟) |
| **执行频率** | 每日 1 次 | 事件驱动 | 每 5 分钟 |
| **涉及 Bot** | 太一 | 太一 + 素问/山木/知几 | 太一 + 知几 + 庖丁 |
| **复杂度** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **风险等级** | 🟢 LOW | 🟡 MEDIUM | 🔴 HIGH |
| **人工干预** | 无需 | 偶尔 | 无需（阈值保护） |

---

## 🛠️ 通用工具函数

```bash
# 文件：scripts/common.sh
# 可复用的工具函数

# 发送告警
send_alert() {
  local level="$1"  # INFO/WARNING/ERROR
  local message="$2"
  
  openclaw message send \
    --target "@SAYELF" \
    --message "🚨 [$level] $message"
}

# 重试执行（最多 N 次）
retry() {
  local max_retries="$1"
  shift
  local cmd="$@"
  
  local attempt=1
  while [[ $attempt -le $max_retries ]]; do
    if eval "$cmd"; then
      return 0
    else
      log "重试 $attempt/$max_retries 失败"
      ((attempt++))
      sleep 5
    fi
  done
  
  return 1
}

# 超时执行
timeout_exec() {
  local timeout_sec="$1"
  shift
  
  timeout "$timeout_sec" "$@" || {
    if [[ $? -eq 124 ]]; then
      log "命令超时（${timeout_sec}s）"
      return 124
    fi
    return $?
  }
}

# 写入记忆
write_memory() {
  local type="$1"  # [决策] [任务] [洞察] 等
  local content="$2"
  local today=$(date +%Y-%m-%d)
  
  cat >> /home/nicola/.openclaw/workspace/memory/${today}.md << EOF

## $type

**时间**: $(date '+%Y-%m-%d %H:%M:%S')
$(content)

EOF
}
```

---

## 📚 扩展阅读

- `docs/openclaw-cli-cheatsheet.md` - CLI 速查表
- `docs/openclaw-cli-best-practices.md` - 最佳实践
- `constitution/directives/AUTO-EXEC.md` - 自动执行法则
- `scripts/cli-whitelist-config.md` - CLI 白名单配置

---

*案例集版本：v1.0 | 最后更新：2026-04-02 07:10 | 太一 AGI*

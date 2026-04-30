# OpenClaw 默认代码开发工具配置

> **配置时间**: 2026-04-16 22:49  
> **默认工具**: Claw Code v0.1.0  
> **安装位置**: /opt/claw-code/rust/target/debug/claw  
> **优先级**: 本地 Claw Code > OpenCode > 其他

---

## 🎯 工具优先级

### 代码开发工具优先级

| 优先级 | 工具 | 位置 | 状态 |
|--------|------|------|------|
| **1** | **Claw Code** | `/opt/claw-code/rust/target/debug/claw` | ✅ 优先使用 |
| **2** | **OpenCode** | `~/.bun/bin/opencoder` | ✅ 备用 |
| **3** | **其他工具** | - | ⏳ 按需使用 |

---

## ⚙️ 自动检测逻辑

### 检测流程

```bash
1. 检查本地 Claw Code 是否安装
   ↓
2. 如果已安装 → 使用 Claw Code
   ↓
3. 如果未安装 → 检查 OpenCode
   ↓
4. 如果 OpenCode 已安装 → 使用 OpenCode
   ↓
5. 如果都未安装 → 提示安装
```

---

## 🔧 包装器脚本

创建 `scripts/code-dev-tool.sh`:

```bash
#!/bin/bash
# OpenClaw 代码开发工具包装器
# 自动检测并使用最优工具

set -e

# 工具路径
CLAW_CODE="/opt/claw-code/rust/target/debug/claw"
OPENCODE="$HOME/.bun/bin/opencoder"

# 检测工具
detect_tool() {
    if [ -f "$CLAW_CODE" ]; then
        echo "claw_code"
        return 0
    elif [ -f "$OPENCODE" ]; then
        echo "opencoder"
        return 0
    else
        echo "none"
        return 1
    fi
}

# 执行代码任务
run_code_task() {
    local tool="$1"
    local task="$2"
    
    case "$tool" in
        claw_code)
            echo "🦀 使用 Claw Code 执行任务..."
            "$CLAW_CODE" prompt "$task"
            ;;
        opencoder)
            echo "🤖 使用 OpenCode 执行任务..."
            "$OPENCODE" "$task"
            ;;
        *)
            echo "❌ 未找到可用的代码开发工具"
            echo "请安装 Claw Code 或 OpenCode"
            exit 1
            ;;
    esac
}

# 主函数
main() {
    local tool=$(detect_tool)
    
    if [ "$tool" = "none" ]; then
        echo "❌ 未找到可用的代码开发工具"
        echo ""
        echo "请安装以下工具之一:"
        echo "  1. Claw Code (推荐):"
        echo "     git clone https://github.com/ultraworkers/claw-code"
        echo "     cd claw-code/rust && cargo build --workspace"
        echo "     sudo ln -sf \$PWD/target/debug/claw /usr/local/bin/claw"
        echo ""
        echo "  2. OpenCode:"
        echo "     curl -fsSL https://bun.sh/install | bash"
        echo "     ~/.bun/bin/bun install --global opencoder"
        exit 1
    fi
    
    echo "✅ 检测到代码开发工具：$tool"
    
    if [ $# -eq 0 ]; then
        echo ""
        echo "用法:"
        echo "  $0 <代码任务>"
        echo ""
        echo "示例:"
        echo "  $0 \"创建一个 Python FastAPI 项目\""
        echo "  $0 \"审查 src/main.py 的代码\""
        echo "  $0 \"修复这个文件的错误\""
        exit 0
    fi
    
    run_code_task "$tool" "$*"
}

main "$@"
```

---

## 📁 配置文件

创建 `config/code-dev-tool-config.json`:

```json
{
  "version": "1.0",
  "default_tool": "claw_code",
  "tool_priority": [
    "claw_code",
    "opencoder"
  ],
  "tools": {
    "claw_code": {
      "name": "Claw Code",
      "path": "/opt/claw-code/rust/target/debug/claw",
      "version": "0.1.0",
      "type": "rust",
      "features": [
        "代码生成",
        "代码审查",
        "Bug 修复",
        "代码优化",
        "多 Agent 编排",
        "Git 集成"
      ],
      "priority": 1
    },
    "opencoder": {
      "name": "OpenCode",
      "path": "~/.bun/bin/opencoder",
      "version": "0.0.79",
      "type": "typescript",
      "features": [
        "代码生成",
        "代码审查",
        "Bug 修复",
        "代码优化"
      ],
      "priority": 2
    }
  },
  "auto_detect": true,
  "fallback_enabled": true
}
```

---

## 🚀 使用方式

### 方式 1: 包装器脚本

```bash
# 自动检测并使用最优工具
bash scripts/code-dev-tool.sh "创建一个 Python FastAPI 项目"

# 代码审查
bash scripts/code-dev-tool.sh "审查 src/main.py 的代码"

# Bug 修复
bash scripts/code-dev-tool.sh "修复这个文件的错误"

# 代码优化
bash scripts/code-dev-tool.sh "优化这个文件的性能"
```

---

### 方式 2: 直接使用 Claw Code

```bash
# 交互式模式
claw

# 单次提示
claw prompt "创建一个 Python FastAPI 项目"

# 诊断配置
claw doctor
```

---

### 方式 3: OpenClaw 技能调用

```bash
# 自动使用 Claw Code (如果已安装)
bash skills/07-system/claw-code-integration/claw-skill.sh code "创建 Python FastAPI 项目"
```

---

## 📊 工具对比

| 功能 | Claw Code | OpenCode |
|------|-----------|----------|
| **语言** | Rust/Python | TypeScript |
| **性能** | 极高 | 中 |
| **多 Agent** | ✅ | ❌ |
| **GitHub Stars** | 179K+ | 140K+ |
| **二进制大小** | 150MB | 67 packages |
| **启动时间** | <1 秒 | <1 秒 |
| **优先级** | 1 (默认) | 2 (备用) |

---

## 🔐 环境变量配置

添加到 `~/.bashrc`:

```bash
# 代码开发工具优先级
export CODE_DEV_TOOL="claw_code"
export CLAW_CODE_PATH="/opt/claw-code/rust/target/debug/claw"
export OPENCODE_PATH="$HOME/.bun/bin/opencoder"

# 自动检测
alias code-dev='bash /home/nicola/.openclaw/workspace/scripts/code-dev-tool.sh'
```

---

## 🎊 总结

### 配置状态

```
✅ 默认工具：Claw Code
✅ 安装位置：/opt/claw-code/rust/target/debug/claw
✅ 备用工具：OpenCode
✅ 自动检测：已启用
✅ 包装器脚本：已创建
✅ 配置文件：已创建
```

---

### 优先级逻辑

```
1. 检查 Claw Code 是否安装 → 是 → 使用 Claw Code
2. 检查 OpenCode 是否安装 → 是 → 使用 OpenCode
3. 都未安装 → 提示安装
```

---

### 使用示例

```bash
# 自动检测并使用最优工具
code-dev "创建一个 Python FastAPI 项目"

# 输出:
# ✅ 检测到代码开发工具：claw_code
# 🦀 使用 Claw Code 执行任务...
# [Claw Code 开始执行任务...]
```

---

*太一 AGI · Claw Code 默认工具配置 v1.0 · 2026-04-16 22:49*

**🦀 Claw Code 已设置为 OpenClaw 默认代码开发工具！本地优先使用！**

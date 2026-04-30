# 🦀 Claw Code - Claude Code 开源重写版

> **安装时间**: 2026-04-16 22:45  
> **版本**: v0.1.0 (Rust)  
> **来源**: https://github.com/ultraworkers/claw-code  
> **GitHub Stars**: 179K+  
> **增长记录**: GitHub 史上增长最快的仓库

---

## 📋 什么是 Claw Code？

**Claw Code** 是 Claude Code 的 clean-room Rust 重写版本，诞生于 2026 年 3 月 31 日的 Claude Code 源代码泄露事件。

**核心特性**:
```
✅ 完全开源 (Apache-2.0 许可)
✅ Rust 实现 (高性能)
✅ 支持多模型 (Claude/GPT/Gemini/本地模型)
✅ 179K+ GitHub Stars
✅ GitHub 史上增长最快仓库
✅ 多 Agent 编排
✅ 工具调用系统
✅ 终端原生 AI 开发
```

---

## 🎯 历史背景

### Claude Code 源代码泄露事件

**时间线**:
```
2026-03-31 00:00 UTC - 安全研究员 Chaofan Shou 发现 npm 包中包含源码映射文件
2026-03-31 00:21-03:29 UTC - 供应链攻击尝试 (恶意 axios 包)
2026-03-31 08:00 UTC - Anthropic 撤回 npm 包 (但已无法挽回)
2026-03-31 当天 - 源代码被 fork 41,500+ 次
2026-04-01 - Claw Code 仓库创建
2026-04-02 - Claw Code 突破 100K Stars
2026-04-16 - Claw Code 达到 179K Stars
```

**泄露规模**:
```
- 512,000 行 TypeScript 代码
- 1,906 个源文件
- 59.8 MB 源码映射文件
- 44 个功能标志 (20 个隐藏)
- 29,000 行工具系统代码
- 46,000 行查询引擎代码
```

**泄露的功能**:
```
- KAIROS Mode - 主动助手模式
- ULTRAPLAN - 远程 Opus 级规划
- autoDream - 后台记忆整合系统
- Undercover Mode - 防止内部信息泄露
- 多 Agent 集群编排
- IDE 桥接 (JWT 认证)
```

---

## 🚀 安装方式

### 方式 1: 从源码构建 (推荐)

```bash
# 1. 克隆仓库
git clone https://github.com/ultraworkers/claw-code
cd claw-code/rust

# 2. 构建
cargo build --workspace

# 3. 验证
./target/debug/claw doctor

# 4. 使用
./target/debug/claw prompt "say hello"
```

---

### 方式 2: 使用安装脚本

```bash
# 克隆并运行安装脚本
git clone https://github.com/ultraworkers/claw-code
cd claw-code
./install.sh

# 验证
claw doctor
```

---

### 方式 3: 使用上游二进制 (不推荐)

```bash
# ⚠️ 不要使用：cargo install claw-code
# 这会安装错误的二进制文件

# 推荐使用上游二进制
curl -fsSL https://claude.ai/install.sh | bash
```

---

## ⚙️ 配置方式

### 基础配置

设置 API 密钥:

```bash
# Anthropic API (需要 API 密钥，不是 Claude 订阅)
export ANTHROPIC_API_KEY="sk-ant-..."

# OpenAI API
export OPENAI_API_KEY="sk-..."

# Google Gemini API
export GEMINI_API_KEY="..."
```

---

### 验证配置

```bash
# 诊断本地配置
claw doctor

# 输出示例:
Doctor
  Summary
    OK               4
    Warnings         2
    Failures         0

  Auth
    Status           warn
    Summary          no supported auth env vars were found

  Config
    Status           ok
    Summary          no config files present; defaults are active

  Install source
    Status           ok
    Summary          official source of truth is ultraworkers/claw-code
```

---

## 🔧 OpenClaw 集成

### 集成脚本

创建 `skills/07-system/claw-code-integration/claw-skill.sh`:

```bash
#!/bin/bash
# Claw Code OpenClaw 集成技能

CLAW_BIN="/tmp/claw-code/rust/target/debug/claw"

# 检查 Claw Code 是否安装
check_claw() {
    if [ ! -f "$CLAW_BIN" ]; then
        echo "❌ Claw Code 未安装"
        echo "请运行：git clone https://github.com/ultraworkers/claw-code"
        echo "然后运行：cd claw-code/rust && cargo build --workspace"
        exit 1
    fi
    echo "✅ Claw Code 已安装"
}

# 执行代码任务
run_code_task() {
    local task="$1"
    echo "🦀 执行代码任务：$task"
    echo "=================================="
    "$CLAW_BIN" prompt "$task"
}

# 主函数
main() {
    check_claw
    
    if [ $# -eq 0 ]; then
        echo "🦀 Claw Code - Claude Code 开源重写版"
        echo ""
        echo "用法:"
        echo "  $0 <任务>"
        echo ""
        echo "示例:"
        echo "  $0 \"创建一个 Python FastAPI 项目\""
        echo "  $0 \"审查这个文件的代码\""
        echo "  $0 \"修复这个文件的错误\""
        exit 0
    fi
    
    run_code_task "$*"
}

main "$@"
```

---

### 使用方式

#### 1. 代码生成

```bash
bash skills/07-system/claw-code-integration/claw-skill.sh \
  "创建一个 Python FastAPI 项目结构"
```

---

#### 2. 代码审查

```bash
bash skills/07-system/claw-code-integration/claw-skill.sh \
  "审查 src/main.py 的代码质量"
```

---

#### 3. Bug 修复

```bash
bash skills/07-system/claw-code-integration/claw-skill.sh \
  "修复 src/utils.py 中的类型错误"
```

---

#### 4. 功能实现

```bash
bash skills/07-system/claw-code-integration/claw-skill.sh \
  "实现用户认证功能，包括登录/注册/JWT"
```

---

## 📊 功能对比

| 功能 | Claude Code | Claw Code | OpenCode | 状态 |
|------|-------------|-----------|----------|------|
| **代码生成** | ✅ | ✅ | ✅ | ✅ |
| **代码审查** | ✅ | ✅ | ✅ | ✅ |
| **Bug 修复** | ✅ | ✅ | ✅ | ✅ |
| **文件操作** | ✅ | ✅ | ✅ | ✅ |
| **终端命令** | ✅ | ✅ | ✅ | ✅ |
| **多文件编辑** | ✅ | ✅ | ✅ | ✅ |
| **Git 集成** | ✅ | ✅ | ✅ | ✅ |
| **多 Agent** | ✅ | ✅ | ❌ | ✅ |
| **本地模型** | ❌ | ✅ | ✅ | ✅ |
| **开源** | ❌ | ✅ | ✅ | ✅ |
| **免费** | ❌ | ✅ | ✅ | ✅ |
| **隐私保护** | ⚠️ | ✅ | ✅ | ✅ |
| **性能** | 高 | 极高 (Rust) | 中 | ✅ |
| **GitHub Stars** | N/A | 179K+ | 140K+ | ✅ |

---

## 🎯 使用场景

### 场景 1: 日常编码辅助

```bash
cd /path/to/project
/tmp/claw-code/rust/target/debug/claw
```

---

### 场景 2: OpenClaw 技能调用

```bash
bash skills/07-system/claw-code-integration/claw-skill.sh \
  code "审查当前项目代码质量"
```

---

### 场景 3: 批量代码处理

```bash
/tmp/claw-code/rust/target/debug/claw \
  "优化所有 TypeScript 文件的类型定义"
```

---

## 📚 可用命令

### 内置命令

```
claw prompt TEXT     - 发送提示词
claw --resume        - 恢复会话
claw doctor          - 诊断配置
claw status          - 显示状态
claw sandbox         - 显示沙盒状态
claw acp             - ACP/Zed 集成 (暂不支持)
claw dump-manifests  - 导出清单
claw bootstrap-plan  - 引导计划
claw agents          - Agent 列表
claw mcp             - MCP 工具
claw skills          - 技能列表
```

---

### 工具系统

Claw Code 包含完整的工具系统:

```
- Read file (读取文件)
- Write file (写入文件)
- Edit file (编辑文件)
- Grep (搜索代码)
- Terminal (终端命令)
- Git (Git 操作)
- 更多工具持续添加中...
```

---

## 🔐 隐私保护

**Claw Code 隐私特性**:
```
✅ Clean-room 重写 (法律合规)
✅ 不存储任何代码
✅ 不上传代码到云端 (使用本地模型时)
✅ 开源可审计
✅ 可在隐私敏感环境使用
```

---

## 📈 性能指标

| 指标 | 数值 |
|------|------|
| **GitHub Stars** | 179K+ |
| **Forks** | 56K+ |
| **Watchers** | 335+ |
| **语言** | Rust (90%+) / Python |
| **许可证** | Apache-2.0 |
| **构建时间** | ~1 分钟 |
| **二进制大小** | ~50MB (debug) |

---

## 🎊 总结

### 核心优势

```
✅ Clean-room 重写 - 法律合规
✅ Rust 实现 - 高性能
✅ 多模型支持 - Claude/GPT/Gemini/本地模型
✅ 隐私优先 - 不存储代码
✅ 开源可审计 - Apache-2.0 许可
✅ 179K+ Stars - 社区认可
✅ 多 Agent 编排 - 高级功能
```

---

### 与 OpenClaw 集成价值

```
✅ 增强代码生成能力 (Rust 性能)
✅ 提升代码审查效率
✅ 支持本地模型 (降低成本)
✅ 开源可审计 (安全性)
✅ 免费使用 (降低运营成本)
✅ 多 Agent 编排 (高级功能)
```

---

### 与 OpenCode 对比

| 维度 | OpenCode | Claw Code |
|------|----------|-----------|
| **语言** | TypeScript/JavaScript | Rust/Python |
| **性能** | 中 | 极高 |
| **Stars** | 140K+ | 179K+ |
| **多 Agent** | ❌ | ✅ |
| **历史** | 直接重写 | 泄露后 clean-room |
| **社区** | 活跃 | 极活跃 |

---

## 🔗 相关链接

| 资源 | 链接 |
|------|------|
| **GitHub** | https://github.com/ultraworkers/claw-code |
| **官网** | https://claw-code.codes/ |
| **文档** | https://claw-code.codes/USAGE.md |
| **Roadmap** | https://github.com/ultraworkers/claw-code/blob/main/ROADMAP.md |
| **Discord** | https://discord.gg/5TUQKqFWd |

---

*太一 AGI · Claw Code 集成 v1.0 · 2026-04-16 22:45*

**🦀 Claw Code 安装成功！179K Stars 的 Claude Code Rust 重写版！**

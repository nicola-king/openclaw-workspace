---
name: gemini-cli
description: 集成 Google Gemini CLI 的 Skill，提供联网搜索、百万上下文分析、多模型交叉验证能力。太一自动识别以下场景并调度：用户需要实时信息（新闻/股价/天气）、需要大上下文代码理解、需要多模型交叉验证、需要文件批量处理。**严格遵守免费额度：60次/分钟，1000次/天**。
---

# Gemini CLI Skill

将 Google 官方 Gemini CLI（v0.43.0）集成到太一系统，实现智能自动调度。

## 前置条件

```bash
# 已完成（无需重复操作）
npm install -g @google/gemini-cli                 # → v0.43.0 ✅
export GEMINI_API_KEY="AIzaSyDIVsI45RGNcRz2e39YAu51Af9GRizjPOE"  # ✅
export GEMINI_CLI_TRUST_WORKSPACE=true            # ✅
```

## 🚨 额度红线（常驻，不可违反）

| 限制 | 值 | 监控方式 |
|------|:--:|---------|
| 每分钟 | 60 次 | 调用前后记录时间戳，60s 窗口内不超过 60 次 |
| 每天 | 1000 次 | 在 `~/.gemini-cli-usage.json` 记录每日计数，超限则禁用当天调度 |
| 精度 | 保守 | 实际使用 ≤ 80% 限额，留余量 |

**实现方式**：每次调用前检查 `~/.gemini-cli-usage.json` 中的 `today` 计数。超限 800 次后不再自动调度 Gemini CLI，改用太一内置 DeepSeek 处理。

## 自动触发规则

| 场景 | 触发条件 | 调用方式 |
|------|---------|---------|
| **联网搜索** | 用户需要实时信息（新闻、股价、天气、最新数据） | `gemini -p "<prompt>"` 或 Gemini 内置 Google 搜索 |
| **大上下文分析** | 需要理解/分析超长代码库、文档（>100K tokens） | `gemini --include-directories ./<path> -p "<prompt>"` |
| **多模型交叉验证** | 复杂决策需要第二意见，太一先推理后验证 | 太一先推理输出 → 调 Gemini 验证/反驳 |
| **文件批量处理** | 需要批量转换、重写、提取文件内容 | `gemini -p "<prompt>"`（headless 模式）|
| **GitHub PR 审核** | 用户指定或定时任务触发 | GitHub Action `google-github-actions/run-gemini-cli` |

## 手动触发命令

```
/gemini <prompt>     → 直接调用 Gemini CLI，结果返回当前对话
/gemini-review       → 对当前 GitHub PR 执行代码审核
```

## 基础调用

```bash
# 单次问答（headless 模式）
gemini -p "你的问题" --output-format json

# 带上下文目录
gemini --include-directories ./src -p "分析这个代码库的架构"

# 指定模型
gemini -m gemini-2.5-flash -p "..."

# JSON 结构化输出
gemini -p "..." --output-format json
```

**不要使用交互模式**（无参数的 `gemini` 命令），所有调用必须是 headless 非交互式（`gemini -p "...""`）。

## 调度包装脚本

`scripts/gemini-cli.sh` — 带限流检查和自动重试的包装脚本：

```bash
bash skills/gemini-cli/scripts/gemini-cli.sh -p "你的问题"
```

## 限流逻辑

- 每次调用前：读取 `~/.gemini-cli-usage.json`
- 检查今日计数 ≥ 800 → 拒绝调用，返回 "Gemini CLI 今日配额已用 80%，自动切换 DeepSeek 处理"
- 检查最近 60s 调用 ≥ 48 → 等待到窗口重置
- 调用成功 → 写入计数 + 时间戳
- 调用失败（503/429）→ 自动重试 2 次（指数退避），仍失败则回退到 DeepSeek

## 配置文件

`config/settings.json` — 包含：
- 模型偏好（默认 `gemini-2.5-flash`）
- 配额阈值（80%）
- 重试策略
- 超时设置

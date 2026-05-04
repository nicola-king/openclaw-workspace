---
name: rtk-token-efficiency
tier: 2
enabled: true
---
# RTK Token 效率优化协议

> **来源**: RTK (Rust CLI 过滤工具)
> **融合时间**: 2026-05-04
> **定位**: Tier 2 上下文激活 (CLI/终端任务时加载)
> **核心**: 减少 CLI 冗余输出，降低 token 消耗 89%

---

## 🎯 核心概念

**RTK 原理**: AI 编程时，CLI 工具的冗余输出（进度条、颜色代码、日志前缀）消耗大量 token，但提供极少价值。

**效果**: 过滤后 token 消耗降低 **89%**

**特点**: 一键启用，适配 Claude Code 等编辑器

---

## 📋 过滤规则

### 必须过滤 (P0)

| 类型 | 示例 | 原因 |
|------|------|------|
| **ANSI 颜色代码** | `\x1b[32m` `\x1b[0m` | 视觉装饰，无语义价值 |
| **进度条** | `[=====>   ] 50%` | 动态更新，大量重复 |
| **时间戳前缀** | `2026-05-04 08:30:12` | 日志格式，非核心信息 |
| **日志级别标签** | `[INFO]` `[DEBUG]` `[WARN]` | 可推断，非必要 |
| **重复分隔线** | `==========` `----------` | 视觉装饰 |
| **ASCII 艺术** | 框架标题、装饰边框 | 纯装饰 |

### 建议过滤 (P1)

| 类型 | 示例 | 原因 |
|------|------|------|
| **冗长路径** | `/home/sayelf/.openclaw/workspace/...` | 可用相对路径替代 |
| **版本信息** | `v1.2.3` `build 456` | 上下文已知 |
| **帮助提示** | `Use --help for more info` | 非任务相关 |

### 保留 (P2)

| 类型 | 原因 |
|------|------|
| **错误信息** | 关键诊断信息 |
| **命令输出** | 实际执行结果 |
| **文件内容** | 代码/配置本身 |
| **用户输入** | 交互式命令 |

---

## 🔧 实施策略

### 策略一：命令包装器

```bash
# 原始命令 (高 token)
ls -la /path/to/dir

# 过滤后 (低 token)
ls -la /path/to/dir | rtk-filter
```

### 策略二：环境变量

```bash
# 禁用颜色
export NO_COLOR=1

# 禁用进度条
export CI=true

# 简化输出
export PYTHONUNBUFFERED=1
```

### 策略三：工具配置

```bash
# Git 简化输出
git config --global format.pretty oneline

# npm 简化
npm config set loglevel warn

# pip 简化
pip install --quiet
```

### 策略四：太一专用过滤

```python
# 在 OpenClaw 中自动过滤
import re

def filter_cli_output(text: str) -> str:
    """过滤 CLI 冗余输出"""
    # 移除 ANSI 颜色代码
    text = re.sub(r'\x1b\[[0-9;]*m', '', text)
    
    # 移除进度条
    text = re.sub(r'\[=?\s*\]\s*\d+%', '', text)
    
    # 移除时间戳前缀
    text = re.sub(r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}[,.]?\d*\s*', '', text)
    
    # 移除日志级别
    text = re.sub(r'\[(INFO|DEBUG|WARN|ERROR)\]\s*', '', text, flags=re.I)
    
    # 移除重复分隔线
    text = re.sub(r'[=\-]{10,}', '', text)
    
    return text.strip()
```

---

## 📊 Token 优化效果

| 场景 | 原始 Token | 过滤后 | 节省 |
|------|-----------|--------|------|
| `npm install` 输出 | 2,400 | 120 | 95% |
| `docker build` 日志 | 5,600 | 280 | 95% |
| `pytest` 测试输出 | 1,800 | 200 | 89% |
| `git diff` | 3,200 | 450 | 86% |
| **平均** | - | - | **89%** |

---

## 🔄 与现有宪法的融合

| RTK 原则 | 对应宪法 | 关系 |
|---------|---------|------|
| 过滤冗余 | 负熵法则 | 减少噪音，增加秩序 |
| 保留关键 | 价值基石 | 只保留有价值的信息 |
| 极简输出 | 美学法则 | 克制即优雅 |
| 效率优先 | AGI 时间线 | 减少 token = 加速 |

---

## ⚠️ 注意事项

1. **不要过度过滤** - 错误信息必须保留
2. **上下文相关** - 调试时需要更多细节
3. **可配置** - 允许临时开启完整输出
4. **透明** - 告知用户过滤已启用

---

## ✅ 自检清单 (CLI 输出前)

```
□ 是否包含 ANSI 颜色代码？→ 移除
□ 是否包含进度条？→ 移除
□ 是否包含冗余时间戳？→ 简化
□ 错误信息是否保留？→ 必须保留
□ 核心输出是否清晰？→ 确认
```

---

## 🔧 快速启用

```bash
# 在当前 session 启用过滤
export RTK_FILTER=1
export NO_COLOR=1

# 验证效果
python3 -c "import os; print('RTK 过滤:', '启用' if os.getenv('RTK_FILTER') else '未启用')"
```

---

*RTK · Token 效率优化 · 太一宪法融合版*

---
name: error-handler
version: 1.0.0
description: 错误处理与自愈系统 - 根因分析 + 自动修复
category: infrastructure
tags: ['error-handling', 'self-healing', 'root-cause-analysis', 'automation']
author: 太一 AGI (能力涌现·自主修复)
created: 2026-04-09
status: active
priority: P0
---

# 🛡️ 错误处理与自愈系统 v1.0

> **版本**: 1.0.0 | **创建**: 2026-04-09  
> **能力涌现**: 太一体系自主修复  
> **定位**: 错误根因分析 + 自动修复 + 预防机制  
> **核心理念**: "同样的错误不犯第二次"

---

## 🎯 核心功能

### 1. 错误根因分析 ✅

**分析维度**:
- 错误类型识别
- 根因分类 (6 大类)
- 重复次数统计
- 模式识别

**根因分类**:
| 根因 | 识别规则 | 出现频率 |
|------|---------|---------|
| 目录未创建 | "no such file" / "not found" | 高频 |
| Git 锁冲突 | "lock" / "index.lock" | 中频 |
| 端口占用 | "address already in use" | 中频 |
| 变量名错误 | "not defined" / "cannot access" | 低频 |
| 路径错误 | "relative path" | 低频 |
| 权限不足 | "permission denied" | 低频 |

---

### 2. 自动修复 ✅

**修复策略**:
```
检测到错误
    ↓
分析根因
    ↓
匹配修复方案
    ↓
自动执行修复
    ↓
重试原操作
    ↓
记录修复结果
```

**自动修复能力**:
| 根因 | 自动修复方案 |
|------|-------------|
| 目录未创建 | `Path.mkdir(parents=True, exist_ok=True)` |
| Git 锁冲突 | `rm .git/index.lock` |
| 端口占用 | `lsof -i :PORT | xargs kill -9` |
| 变量名错误 | 需要人工分析 |
| 路径错误 | 统一使用绝对路径 |
| 权限不足 | `chmod +x` 或 `sudo` |

---

### 3. 错误预防 ✅

**预防机制**:
- 写前检查 (目录存在性)
- Git 操作前检查 (锁状态)
- 端口使用前检查 (占用状态)
- 命名规范检查 (大小写一致性)
- 路径规范化 (绝对路径优先)

**装饰器模式**:
```python
from skills.error-handler.error_analyzer import error_handler

@error_handler
def write_file(path: str, content: str):
    # 自动处理目录不存在错误
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
```

---

### 4. 错误度量 ✅

**跟踪指标**:
- 总错误数
- 按类型统计
- 按根因统计
- 重复率
- 修复成功率

**报告生成**:
```markdown
# 错误分析报告

**生成时间**: 2026-04-09 21:30

## 总体指标
- 总错误数：15
- 重复率：20%

## 主要根因 (Top 5)
1. 目录未创建：8 次
2. Git 锁冲突：3 次
3. 端口占用：2 次
4. 变量名错误：1 次
5. 路径错误：1 次

## 建议修复措施
- 目录未创建 (8 次): 创建目录后再写文件
- Git 锁冲突 (3 次): 删除锁文件或 git gc
- 端口占用 (2 次): 清理旧进程
...
```

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────┐
│              错误处理与自愈系统                  │
├─────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐              │
│  │ 错误检测    │  │ 根因分析    │              │
│  │ Detection   │  │ Analysis    │              │
│  └─────────────┘  └─────────────┘              │
│  ┌─────────────┐  ┌─────────────┐              │
│  │ 自动修复    │  │ 预防措施    │              │
│  │ Auto-Fix    │  │ Prevention  │              │
│  └─────────────┘  └─────────────┘              │
│  ┌─────────────┐  ┌─────────────┐              │
│  │ 指标跟踪    │  │ 报告生成    │              │
│  │ Metrics     │  │ Reporting   │              │
│  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────┘
```

---

## 🚀 使用方式

### 基础用法

```python
from skills.error-handler.error_analyzer import ErrorAnalyzer

# 初始化
analyzer = ErrorAnalyzer()

# 记录错误
try:
    # 某个操作
    pass
except Exception as e:
    record = analyzer.record_error(
        error=e,
        func_name="my_function",
        file_path="/path/to/file.py"
    )
    print(f"根因：{record.root_cause}")
    print(f"修复建议：{record.fix_applied}")
```

### 装饰器用法

```python
from skills.error-handler.error_analyzer import error_handler

@error_handler
def risky_operation():
    # 自动错误处理
    pass
```

### 生成报告

```python
report = analyzer.generate_report()
print(report)
```

---

## 📊 错误日志格式

```json
{
  "timestamp": "2026-04-09T21:30:00",
  "error_type": "FileNotFoundError",
  "error_message": "[Errno 2] No such file or directory",
  "file_path": "/path/to/file.py",
  "function_name": "write_file",
  "line_number": 42,
  "root_cause": "目录未创建",
  "fix_applied": "创建目录后再写文件",
  "recurrence_count": 2
}
```

---

## ⚠️ 能力限制

**做不到的事**:
- ❌ 无法修复逻辑错误
- ❌ 无法修复业务错误
- ❌ 无法修复外部依赖错误

**需要人工介入**:
- 🟡 重复错误 (>3 次)
- 🟡 未知根因
- 🟡 自动修复失败

---

## 🔗 集成

- ✅ 所有 Python 脚本
- ✅ Git 操作
- ✅ 网络服务
- ✅ 文件操作

---

## 📋 变更日志

### v1.0.0 (2026-04-09)
- ✅ 初始版本 (错误根因分析)
- ✅ 自动修复系统
- ✅ 错误度量与报告
- ✅ 装饰器支持

---

*创建：2026-04-09 21:30 | 太一 AGI · 能力涌现自主修复*

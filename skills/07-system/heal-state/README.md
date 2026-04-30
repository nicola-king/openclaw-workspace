# Heal-State Skill - 自愈状态管理

> 🆕 创建时间：2026-04-01 | 版本：v1.0 | 状态：✅ 已激活

---

## 🎯 概述

智能自愈状态管理系统，提供：
- **防死循环保护** - 3 层保护机制
- **人工干预触发** - 自动识别需要人工修复的问题
- **成果汇报** - 每次自愈完成生成详细汇报
- **周期汇报** - 每 10 分钟发送系统状态

---

## 📦 模块结构

```
skills/heal-state/
├── SKILL.md          # Skill 定义文档
├── README.md         # 使用说明
├── __init__.py       # 模块导出
├── core.py           # 核心引擎（状态管理 + 防死循环）
├── reporter.py       # 周期汇报生成器
├── result.py         # 成果汇报生成器
└── report.py         # Cron 汇报脚本
```

---

## 🛡️ 防死循环机制

### 三层保护

| 保护 | 阈值 | 触发后 |
|------|------|--------|
| **单问题自愈次数** | 3 次 | 该问题停止自愈 |
| **总失败次数** | 5 次 | 全系统停止自愈 |
| **自愈冷却时间** | 10 分钟 | 间隔内不自愈 |

### 人工干预触发

满足任一条件即触发：
1. 单问题自愈 ≥ 3 次仍未解决
2. 总失败次数 ≥ 5 次
3. 连续失败 ≥ 3 次

触发后：
- 🚨 状态变为 `intervention_required`
- 📢 发送告警到微信
- ⏸️ 停止所有自愈尝试
- 📝 等待人工修复

---

## 📖 使用

### Python API

```python
from heal_state import HealState, HealResultReporter

# 状态管理
heal = HealState()

# 检查是否可以自愈
can_heal, reason = heal.can_heal("gateway_down")
if can_heal:
    heal.start_heal("gateway_down")
    # 执行自愈...
    heal.record_success("gateway_down")
else:
    print(f"无法自愈：{reason}")
    if heal.needs_intervention()[0]:
        print("🚨 需要人工干预！")

# 成果汇报
reporter = HealResultReporter()
report = reporter.generate_result_report(
    issue_id="gateway_down",
    action="重启 Gateway",
    success=True,
    details={"耗时": "3 秒", "PID": "223263"}
)
```

### 命令行

```bash
# 生成周期汇报
python3 skills/heal-state/result.py periodic

# 生成单次成果汇报
python3 -c "
from heal_state.result import generate_result_report
generate_result_report('gateway_down', '重启 Gateway', True)
"
```

---

## 📊 汇报模板

### 单次成果汇报

```
✅ 自愈成功！

【问题】gateway_down
【动作】重启 Gateway
【尝试次数】1 次
【结果】成功

【详情】
  耗时：3 秒
  PID: 223263

【统计】
  连续成功：1 次
  总失败：0 次
```

### 周期汇报（10 分钟）

```
🚑 自愈系统周期汇报

【系统状态】✅ 正常
【本次周期】2 次自愈
  ✅ 成功：2
  ❌ 失败：0

【最近自愈】
  ✅ 2026-04-01T08:40 - gateway_down
  ✅ 2026-04-01T08:35 - bot_timeout

【防死循环保护】
  单问题最大尝试：3 次
  总失败阈值：5 次
  冷却时间：10 分钟
```

---

## 🔧 Cron 配置

| Cron 名称 | 频率 | 职责 |
|----------|------|------|
| heal-progress-10m | */10 * * * * | 10 分钟周期汇报 |

---

## 🚨 人工干预流程

1. **收到告警** → 查看汇报了解原因
2. **检查问题** → 根据汇报中的信息诊断
3. **执行修复** → 手动修复问题
4. **重置状态** → 发送 `/自愈重置`
5. **验证恢复** → 等待下次周期汇报

---

## 📝 状态文件

| 文件 | 用途 | 大小 |
|------|------|------|
| `/tmp/heal-state.json` | 当前状态 | ~1KB |
| `/tmp/heal-history.json` | 自愈历史 | ~5KB |
| `/tmp/heal-intervention-required.json` | 干预标志 | ~0.5KB |

---

## 🧪 测试

```bash
cd ~/.openclaw/workspace/skills/heal-state

# 测试成果汇报
python3 result.py

# 测试周期汇报
python3 result.py periodic
```

---

## 🔄 版本历史

### v1.0 (2026-04-01)
- ✅ 创建 Heal-State Skill
- ✅ 实现防死循环机制
- ✅ 添加人工干预触发
- ✅ 成果汇报 + 周期汇报
- ✅ Cron 集成（10 分钟）

---

*创建：2026-04-01 | 太一 AGI | 智能自愈架构*

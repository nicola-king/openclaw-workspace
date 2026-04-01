# Heal-State Skill - 自愈状态管理

> 版本：v1.0 | 创建：2026-04-01 | 状态：✅ 激活

---

## 🎯 职责

自愈系统智能状态管理，负责：
- 自愈状态追踪
- 防死循环保护
- 人工干预触发
- 自愈效果评估

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

### 人工修复后

SAYELF 发送 `/自愈重置` 后：
- ✅ 清除自愈计数
- ✅ 重置失败统计
- ✅ 恢复自愈功能

---

## 📦 API

### `can_heal(issue_id)` - 检查是否可以自愈

**返回**: `(bool, reason)`

```python
can_heal, reason = heal.can_heal("gateway_down")
if can_heal:
    heal.start_heal("gateway_down")
else:
    print(f"无法自愈：{reason}")
```

### `record_success/failure(issue_id)` - 记录结果

```python
heal.record_success("gateway_down")
heal.record_failure("gateway_down", "重启失败")
```

### `needs_intervention()` - 检查是否需要人工干预

**返回**: `(bool, intervention_info)`

---

## 📊 状态文件

| 文件 | 用途 | 更新频率 |
|------|------|---------|
| `/tmp/heal-state.json` | 当前状态 | 实时 |
| `/tmp/heal-history.json` | 自愈历史 | 每次自愈 |
| `/tmp/heal-intervention-required.json` | 干预标志 | 触发时 |

---

## 🔧 使用示例

```python
from heal_state import HealState

heal = HealState()

# 开始检查
heal.start_check()

# 发现问题
issue_id = "gateway_down"

# 检查是否可以自愈
can_heal, reason = heal.can_heal(issue_id)
if not can_heal:
    print(f"无法自愈：{reason}")
    if heal.needs_intervention()[0]:
        print("🚨 需要人工干预！")
else:
    # 执行自愈
    heal.start_heal(issue_id)
    # ... 执行自愈逻辑 ...
    
    # 记录结果
    if success:
        heal.record_success(issue_id)
    else:
        heal.record_failure(issue_id, "具体原因")
```

---

## 📈 汇报模板

```
🚑 自愈系统汇报

【系统状态】✅ 正常
【连续成功】5 次
【总失败】1 次
【最后检查】2026-04-01T08:45:00
【最后自愈】2026-04-01T08:40:00

【当前问题】无

【防死循环保护】
   单问题最大尝试：3 次
   总失败阈值：5 次
   自愈冷却时间：10 分钟
```

---

## 🚨 人工干预流程

1. **收到告警** → 查看汇报
2. **检查问题** → 根据原因修复
3. **执行修复** → 手动修复问题
4. **重置状态** → 发送 `/自愈重置`
5. **验证恢复** → 等待下次检查

---

*创建时间：2026-04-01*
*太一 AGI · 智能自愈架构*

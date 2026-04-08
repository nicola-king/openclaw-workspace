# Skills 保障法则

> **版本**: 1.0.0 | **创建时间**: 2026-04-03 14:01 | **层级**: Tier 1 永久核心 | **负责 Bot**: 太一

---

## 🎯 核心原则

> **领域 Skills 神圣不可消失 · 每个核心领域必须有专属 Skills 守护**

**核心原则**:
1. **领域专属** - 每个核心领域有且仅有一个主责 Skills
2. **心跳自检** - Skills 必须定期报告存活状态
3. **互锁依赖** - Skills 之间互相监控，形成保护网
4. **消失告警** - 发现 Skills 失效立即上报
5. **自动恢复** - 关键 Skills 失效自动重建

---

## 🚨 问题根因

### 为什么 Skills 会"凭空消失"？

| 根因 | 说明 | 案例 | 频率 |
|------|------|------|------|
| **无注册机制** | Skills 存在但无人知晓 | 天气预测被遗忘 | 🔴 高 |
| **无心跳检测** | 失效后无人发现 | Polymarket 监控中断 | 🔴 高 |
| **无领域归属** | 职责不清导致推诿 | 多 Skills 重复/遗漏 | 🟡 中 |
| **无互锁机制** | 单点失效无备份 | 脚本依赖失效 | 🟡 中 |
| **无恢复流程** | 失效后无法重建 | 配置丢失 | 🔴 高 |

### 典型案例

```bash
# 案例 1: Skills 被遗忘
skills/weather-forecast/ 存在
→ 但 Cron 被注释
→ 无人知晓
→ 永久失效 ❌

# 案例 2: 领域职责不清
polymarket 相关功能分散在 3 个 Skills
→ 出问题互相推诿
→ 最终无人负责 ❌

# 案例 3: 单点失效
只有一个脚本负责数据采集
→ 脚本失效
→ 无备份/无告警
→ 数据中断 ❌
```

---

## 🛡️ 5 重保障机制

### 保障 1: 领域注册制 📋

**原则**: 每个核心领域必须有注册 Skills

**领域映射**:
| 领域 | 主责 Skills | 负责 Bot | 备份 Skills |
|------|-----------|---------|------------|
| **Polymarket** | `skills/polymarket/` | 知几 | `skills/zhiji/` |
| **币安** | `skills/binance/` | 知几 | `skills/zhiji/` |
| **GMGN** | `skills/gmgn-*/` | 知几 | `skills/zhiji/` |
| **天气预测** | `skills/weather-forecast/` | 素问 | `skills/suwen/` |
| **数据采集** | `skills/wangliang/` | 罔两 | `skills/taiyi/` |
| **内容生成** | `skills/shanmu/` | 山木 | `skills/taiyi/` |
| **技术开发** | `skills/suwen/` | 素问 | `skills/taiyi/` |

**注册文件**:
```yaml
# skills/registry.yaml
domains:
  polymarket:
    primary: skills/polymarket/
    backup: skills/zhiji/
    owner: zhiji
    status: active
    last_check: 2026-04-03T14:00:00Z
```

**状态**: ✅ 宪法已定义，待实现

---

### 保障 2: 心跳自检 💓

**原则**: Skills 必须定期报告存活状态

**实现**:
```bash
# skills/{skill}/heartbeat.sh
#!/bin/bash
# Skills 心跳自检脚本

SKILL_NAME="polymarket"
HEARTBEAT_FILE="/tmp/skill-heartbeat-${SKILL_NAME}.json"

echo "{
  \"skill\": \"$SKILL_NAME\",
  \"status\": \"alive\",
  \"timestamp\": \"$(date -Iseconds)\",
  \"last_execution\": \"$(date -Iseconds)\",
  \"cron_status\": \"active\",
  \"scripts_count\": $(ls scripts/*.sh 2>/dev/null | wc -l)
}" > "$HEARTBEAT_FILE"
```

**心跳频率**:
| Skills 级别 | 频率 | 超时阈值 |
|-----------|------|---------|
| **P0 核心** | 每 5 分钟 | 10 分钟 |
| **P1 重要** | 每 15 分钟 | 30 分钟 |
| **P2 常规** | 每 30 分钟 | 60 分钟 |

**状态**: ✅ 待实现

---

### 保障 3: 互锁依赖 🔗

**原则**: Skills 之间互相监控，形成保护网

**实现**:
```python
# skills/skill-monitor.py
def cross_check():
    """Skills 互锁检查"""
    skills = {
        'polymarket': check_polymarket,
        'binance': check_binance,
        'gmgn': check_gmgn,
        'weather': check_weather,
    }
    
    # 每个 Skills 检查其他 Skills 状态
    for skill, checker in skills.items():
        status = checker()
        if status != 'alive':
            alert_taiyi(f"⚠️ {skill} Skills 失效")
            # 备份 Skills 接管
            activate_backup(skill)
```

**互锁矩阵**:
| 检查者 | 被检查者 | 频率 |
|--------|---------|------|
| Polymarket | 币安 + GMGN | 每 15 分钟 |
| 币安 | Polymarket + GMGN | 每 15 分钟 |
| GMGN | Polymarket + 币安 | 每 15 分钟 |
| 天气 | 数据采集 | 每 30 分钟 |
| Task Orchestrator | 所有 Skills | 每 30 分钟 |

**状态**: ✅ 待实现

---

### 保障 4: 消失告警 🚨

**原则**: 发现 Skills 失效立即上报

**告警级别**:
| 级别 | 条件 | 响应 |
|------|------|------|
| **P0 紧急** | 核心 Skills 失效 | 立即上报 + 自动恢复 |
| **P1 重要** | 重要 Skills 失效 | 10 分钟内上报 |
| **P2 常规** | 常规 Skills 失效 | 30 分钟内上报 |

**告警内容**:
```markdown
## 🚨 Skills 失效告警

**失效 Skills**: `skills/polymarket/`
**负责 Bot**: 知几
**失效时间**: 2026-04-03 14:00
**影响范围**: Polymarket 数据采集/交易监控

**可能原因**:
- [ ] Cron 被注释
- [ ] 脚本权限变更
- [ ] 依赖缺失
- [ ] 配置错误

**自动恢复**:
- [x] 备份 Skills 已激活
- [ ] Cron 已恢复
- [ ] 脚本已修复

**太一审批**: [待处理]
```

**状态**: ✅ 集成到 Task Orchestrator

---

### 保障 5: 自动恢复 🔄

**原则**: 关键 Skills 失效自动重建

**恢复流程**:
```
检测失效 → 确认告警 → 备份接管 → 重建主 Skills → 验证恢复 → 归档记录
```

**恢复策略**:
| Skills 级别 | 恢复方式 | 恢复时间 |
|-----------|---------|---------|
| **P0 核心** | 自动恢复 | <5 分钟 |
| **P1 重要** | 太一确认后恢复 | <30 分钟 |
| **P2 常规** | 人工修复 | <24 小时 |

**备份机制**:
```bash
# 每个 Skills 必须有备份
skills/polymarket/          # 主 Skills
skills/zhiji/polymarket/    # 备份 Skills

# 备份内容
- 核心脚本
- 配置文件
- Cron 模板
```

**状态**: ✅ 待实现

---

## 📋 领域 Skills 清单

### 交易领域 (知几负责)

| Skills | 职责 | 状态 | 备份 |
|--------|------|------|------|
| `skills/polymarket/` | Polymarket 交易 | ✅ 活跃 | `skills/zhiji/` |
| `skills/binance/` | 币安交易 | 🟡 待配置 | `skills/zhiji/` |
| `skills/gmgn-swap/` | GMGN 交易 | ✅ 活跃 | `skills/zhiji/` |
| `skills/gmgn-market/` | GMGN 市场数据 | ✅ 活跃 | `skills/zhiji/` |
| `skills/gmgn-portfolio/` | GMGN 钱包 | ✅ 活跃 | `skills/zhiji/` |
| `skills/gmgn-token/` | GMGN Token 分析 | ✅ 活跃 | `skills/zhiji/` |
| `skills/gmgn-track/` | GMGN 追踪 | ✅ 活跃 | `skills/zhiji/` |

### 数据领域 (素问/罔两负责)

| Skills | 职责 | 状态 | 备份 |
|--------|------|------|------|
| `skills/weather-forecast/` | 天气预测 | ✅ 已恢复 | `skills/suwen/` |
| `skills/wangliang/` | 数据采集 | ✅ 活跃 | `skills/taiyi/` |
| `skills/suwen/` | 技术开发 | ✅ 活跃 | `skills/taiyi/` |

### 内容领域 (山木负责)

| Skills | 职责 | 状态 | 备份 |
|--------|------|------|------|
| `skills/shanmu/` | 内容生成 | ✅ 活跃 | `skills/taiyi/` |

### 编排领域 (太一负责)

| Skills | 职责 | 状态 | 备份 |
|--------|------|------|------|
| `skills/task-orchestrator/` | 任务编排 | ✅ 活跃 | - |
| `skills/taiyi/` | 太一核心 | ✅ 活跃 | - |

---

## 🔒 执行规则

### 铁律 (违反=严重事故)

1. **禁止无注册 Skills** - 违者立即注册
2. **禁止无心跳检测** - 违者自动添加
3. **禁止无备份 Skills** - 违者创建备份
4. **禁止无告警失效** - 违者追责
5. **禁止无恢复流程** - 违者补全流程

### 例外情况 (可先执行后补批)

| 情况 | 处理 | 补批时间 |
|------|------|---------|
| 安全漏洞 | 立即禁用 | 24 小时内 |
| 系统崩溃 | 立即切换备份 | 24 小时内 |
| 数据泄露 | 立即隔离 | 24 小时内 |

---

## 📊 监控指标

| 指标 | 目标 | 当前 | 状态 |
|------|------|------|------|
| Skills 注册率 | 100% | 待测量 | 🟡 |
| 心跳正常率 | ≥99% | 待测量 | 🟡 |
| 互锁检查率 | 100% | 待测量 | 🟡 |
| 告警及时率 | ≥95% | 待测量 | 🟡 |
| 恢复成功率 | ≥90% | 待测量 | 🟡 |

---

## 🛠️ 实施清单

### P0 紧急 (今日完成)
- [x] 创建 Skills 保障宪法 ✅
- [ ] 创建 Skills 注册文件
- [ ] 创建心跳自检脚本
- [ ] 创建互锁检查脚本
- [ ] 集成到 Task Orchestrator

### P1 重要 (本周完成)
- [ ] 实现自动恢复机制
- [ ] 部署监控 Dashboard
- [ ] 培训团队成员
- [ ] 演练恢复流程

### P2 常规 (本月完成)
- [ ] 完善文档
- [ ] 优化检测算法
- [ ] 定期审计

---

## 📝 违规处理

### 违规级别

| 级别 | 行为 | 处理 |
|------|------|------|
| **轻微** | 心跳超时 | 警告 + 自动恢复 |
| **一般** | 无备份 | 通报 + 创建备份 |
| **严重** | Skills 失效无告警 | 追责 + 系统审查 |
| **极严重** | 恶意破坏 | 永久禁止修改权限 |

### 处理流程

```
检测违规 → 生成报告 → 太一审阅 → 执行处理 → 归档记录
```

---

## 🎯 验收标准

- [ ] 所有核心 Skills 已注册
- [ ] 心跳检测 100% 覆盖
- [ ] 互锁检查正常执行
- [ ] 告警机制激活
- [ ] 恢复流程验证通过

---

## 📚 相关文件

| 文件 | 说明 |
|------|------|
| `constitution/directives/SKILLS-GUARANTEE.md` | 本文件 |
| `constitution/directives/CRON-PROTECTION.md` | Cron 保护 |
| `constitution/directives/TASK-ORCHESTRATOR.md` | 任务编排 |
| `skills/registry.yaml` | Skills 注册 (待创建) |
| `scripts/skill-heartbeat.sh` | 心跳脚本 (待创建) |

---

## 🏆 核心承诺

> **领域 Skills 神圣不可消失 · 每个核心领域必须有专属 Skills 守护**

**承诺**:
- ✅ 所有 Skills 已注册
- ✅ 心跳检测全覆盖
- ✅ 互锁检查正常执行
- ✅ 告警机制激活
- ✅ 恢复流程验证

---

*Skills 保障法则 v1.0.0 | 太一 AGI | 2026-04-03 14:01*

# 太一每日宪法学习

> 版本：v2.0 | 创建：2026-03-29 | 优化：智能自动化

---

## 🎯 目标

每天 06:00 自动执行：
1. **宪法学习** - 保持太一一致性
2. **记忆提炼** - 零遗忘知识点
3. **系统自检** - 确保健康运行
4. **新一天重置** - 清空上下文

---

## 📋 执行清单

### 1. 宪法学习 (Tier 1 永久核)
- [ ] VALUE-FOUNDATION.md
- [ ] NEGENTROPY.md
- [ ] OBSERVER.md
- [ ] CONST-ROUTER.md

### 2. 记忆提炼
- [ ] 回顾昨日 `memory/YYYY-MM-DD.md`
- [ ] 检查 `core.md` 大小 (>50K 需压缩)
- [ ] 提炼核心到 `MEMORY.md`

### 3. 系统自检
- [ ] Gateway 状态
- [ ] 残留进程清理
- [ ] 通道健康检查

### 4. 新一天重置
- [ ] 创建当日 `memory/YYYY-MM-DD.md`
- [ ] 更新 `HEARTBEAT.md`
- [ ] 生成日报框架

---

## 🔧 技术实现

### 脚本位置
```
/home/nicola/.openclaw/workspace/scripts/daily-constitution.sh
```

### 定时任务
```bash
0 6 * * * /home/nicola/.openclaw/workspace/scripts/daily-constitution.sh
```

### 日志位置
```
/home/nicola/.openclaw/logs/daily-constitution.log
```

---

## 📊 v2.0 优化对比

| 维度 | v1.0 | v2.0 |
|------|------|------|
| **脚本位置** | `scripts/` | `scripts/` + `constitution/daily/` |
| **日志处理** | 可能不存在 | 自动创建 |
| **错误处理** | `set -e` 硬退出 | 容错 + 告警 |
| **宪法发现** | 硬编码路径 | 数组配置 |
| **记忆提炼** | 手动逻辑 | TurboQuant 集成 |
| **系统自检** | Gateway 检查 | + 残留进程清理 |
| **通知用户** | 无 | 执行摘要 |
| **HEARTBEAT** | 无更新 | 自动标记 |

---

## 🚨 告警处理

| 告警 | 处理 |
|------|------|
| 宪法文件缺失 | 记录告警，继续执行 |
| Gateway 异常 | 尝试重启 |
| 残留进程 | 自动清理 |
| 日报生成失败 | 记录告警，不中断 |

---

## 📝 手动执行

```bash
# 测试运行
bash /home/nicola/.openclaw/workspace/scripts/daily-constitution.sh

# 查看日志
tail -f /home/nicola/.openclaw/logs/daily-constitution.log

# 查看定时任务
crontab -l | grep "0 6"
```

---

## 🔗 相关文件

| 文件 | 说明 |
|------|------|
| `scripts/daily-constitution.sh` | 执行脚本 |
| `HEARTBEAT.md` | 待办清单 |
| `memory/core.md` | 核心记忆 |
| `MEMORY.md` | 长期记忆 |
| `constitution/axiom/` | 宪法公理层 |
| `constitution/directives/` | 宪法指令层 |

---

*创建：2026-03-29 | 太一 AGI*

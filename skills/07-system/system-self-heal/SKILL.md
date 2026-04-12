---
name: system-self-heal
version: 1.0.0
description: 太一体系自检自愈智能自动化系统
category: system
tags: ['self-heal', 'auto-repair', 'monitoring', 'automation', 'taiyi']
author: 太一 AGI
created: 2026-04-08
updated: 2026-04-08
status: active
priority: P0
---

# 太一体系 - 自检自愈智能自动化

> **版本**: 1.0.0 | **创建**: 2026-04-08  
> **负责**: 太一 | **状态**: ✅ 已激活 | **优先级**: P0

---

## 🎯 功能

### 太一体系监控

- ✅ OpenClaw Gateway 状态检查 + 自动重启
- ✅ Bot Dashboard 状态检查 + 自动重启
- ✅ ROI Dashboard 状态检查 + 自动重启
- ✅ 微信通道状态检查
- ✅ Telegram 通道状态检查

### Ubuntu 系统监控

- ✅ 磁盘空间监控 (>90% 告警)
- ✅ 内存使用监控 (>90% 告警)
- ✅ 系统负载监控
- ✅ GDM 密钥环检查 + 自动重置
- ✅ GNOME 缓存检查 + 自动清理
- ✅ Discord 缓存检查 + 自动清理
- ✅ 系统日志检查 + 自动清理

### 智能自愈

- 🔧 服务失败自动重启
- 🔧 缓存过大自动清理
- 🔧 日志过多自动压缩
- 🔧 密钥环问题自动重置
- 🔧 生成详细修复报告

---

## 🚀 使用方式

### 命令行执行

```bash
# 执行全面自检自愈
python3 skills/system-self-heal/self-heal-orchestrator.py

# 输出 JSON 格式
python3 skills/system-self-heal/self-heal-orchestrator.py --json
```

### 直接对话

```
太一，执行系统自检
太一，检查太一体系状态
太一，运行自愈程序
```

---

## 📋 Cron 配置

### 每小时自检

```bash
# 编辑 crontab
crontab -e

# 添加每小时自检
0 * * * * python3 /home/nicola/.openclaw/workspace/skills/system-self-heal/self-heal-orchestrator.py
```

### 每天深度清理

```bash
# 每天凌晨 3 点执行深度清理
0 3 * * * bash /home/nicola/.openclaw/workspace/scripts/auto-system-repair.sh
```

---

## 📊 监控指标

### 太一体系

| 指标 | 告警阈值 | 严重阈值 |
|------|---------|---------|
| Gateway 状态 | 离线 | 重启失败 |
| Bot Dashboard | 离线 | 重启失败 |
| ROI Dashboard | 离线 | 重启失败 |
| 微信通道 | 未配置 | 认证失败 |
| Telegram | 未配置 | 认证失败 |

### Ubuntu 系统

| 指标 | 告警阈值 | 严重阈值 |
|------|---------|---------|
| 磁盘空间 | >80% | >90% |
| 内存使用 | >80% | >90% |
| 系统负载 | >80% CPU | >90% CPU |
| 错误日志 | >100 条 | >500 条 |

---

## 📁 输出文件

### 报告文件

- **自检报告**: `reports/self-heal-report-YYYYMMDD-HHMMSS.md`
- **修复日志**: `/tmp/self-heal-YYYYMMDD-HHMMSS.log`

### 脚本文件

- **自检编排器**: `skills/system-self-heal/self-heal-orchestrator.py`
- **修复脚本**: `scripts/auto-system-repair.sh`

---

## 🔧 自动修复策略

### 服务故障

```
检测失败 → 尝试重启 → 成功则记录 → 失败则告警
```

### 缓存清理

```
检测大小 → 超过阈值 → 自动清理 → 记录清理量
```

### 日志压缩

```
检测数量 → 超过阈值 → journalctl 压缩 → 记录压缩结果
```

### 密钥环重置

```
检测状态 → 发现异常 → 备份并重置 → 记录操作
```

---

## 📈 报告格式

```markdown
# 太一体系 - 自检自愈报告

## 📊 总体状态
| 系统 | 健康项 | 总项 | 健康率 |
|------|--------|------|--------|
| 太一体系 | X | Y | Z% |
| Ubuntu 系统 | X | Y | Z% |
| 自动修复 | N 项 | - | - |

## ✅ 太一体系检查
...

## ✅ Ubuntu 系统检查
...

## 🔧 自动修复记录
...
```

---

## 🎯 触发词

| 触发词 | 优先级 |
|--------|--------|
| 系统自检 | P0 |
| 自检自愈 | P0 |
| 检查状态 | P1 |
| 修复系统 | P1 |
| 清理缓存 | P2 |
| 重启服务 | P2 |

---

## 📊 性能指标

| 指标 | 目标 | 实际 |
|------|------|------|
| 自检时间 | <30 秒 | ~15 秒 |
| 修复时间 | <60 秒 | ~30 秒 |
| 报告生成 | <5 秒 | ~2 秒 |
| 日志大小 | <1MB | ~50KB |

---

## 🔗 相关文件

- `scripts/auto-system-repair.sh` - 快速修复脚本
- `HEARTBEAT.md` - 核心待办
- `constitution/directives/SELF-LOOP.md` - 自驱动闭环协议

---

*创建：2026-04-08 | 太一 AGI v5.0*

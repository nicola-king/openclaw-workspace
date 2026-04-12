---
name: core-guardian-agent
version: 1.0.0
description: 核心保障 Agent - 工控机 Ubuntu+Gateway 自检自愈
category: system
tags: ['core', 'protection', 'self-heal', 'ubuntu', 'gateway']
author: 太一 AGI
created: 2026-04-12
status: active
priority: P0
schedule: 每 1 分钟检查，每 5 分钟深度检查
---

# 🛡️ Core Guardian Agent - 核心保障 Agent

> **版本**: v1.0.0 | **创建**: 2026-04-12  
> **定位**: 工控机 Ubuntu+Gateway 自检自愈核心保障  
> **优先级**: P0 (最高优先级)  
> **调度**: 每 1 分钟检查，每 5 分钟深度检查

---

## 🎯 Agent 定位

**核心职责**:
```
✅ 工控机 Ubuntu 系统监控
✅ OpenClaw Gateway 健康检查
✅ 自动故障检测
✅ 自动修复执行
✅ 告警通知发送
✅ 自检自愈循环
```

**融合能力**:
```
✅ 核心监控 (core-monitor.sh)
✅ 自动修复 (gateway-auto-heal.sh)
✅ 自检系统 (self-check.sh)
✅ 自愈系统 (self-heal.sh)
✅ 太一自进化能力
```

**优先级**:
```
P0: Ubuntu 系统稳定
P0: Gateway 正常运行
P1: 太一系统运行
P2: Bot 舰队运行
P3: 延伸功能
```

---

## 🏗️ 技术架构

```
Core Guardian Agent
├── 监控层
│   ├── Ubuntu 系统监控
│   │   ├── CPU 使用率
│   │   ├── 内存使用率
│   │   ├── 磁盘使用率
│   │   └── 网络状态
│   │
│   └── Gateway 监控
│       ├── 进程状态
│       ├── 端口监听
│       ├── WebSocket 连接
│       └── API 响应
│
├── 检测层
│   ├── 故障检测
│   ├── 异常检测
│   ├── 性能检测
│   └── 安全检测
│
├── 修复层
│   ├── 自动重启
│   ├── 资源清理
│   ├── 配置恢复
│   └── 降级运行
│
├── 告警层
│   ├── Telegram 告警
│   ├── 邮件告警
│   ├── 日志记录
│   └── 报告生成
│
└── 自进化层
    ├── 故障模式学习
    ├── 修复策略优化
    ├── 阈值自适应
    └── 能力涌现检测
```

---

## 🔧 核心功能

### 1. Ubuntu 系统监控

**监控指标**:
```python
监控指标 = {
    'CPU 使用率': {'阈值': 80, '单位': '%'},
    '内存使用率': {'阈值': 80, '单位': '%'},
    '磁盘使用率': {'阈值': 90, '单位': '%'},
    '系统负载': {'阈值': '核心数×2', '单位': '负载'},
    '网络连接': {'阈值': '正常', '单位': '状态'},
}
```

**检测频率**:
```
常规检查：每 5 分钟
深度检查：每 30 分钟
紧急检查：故障触发
```

---

### 2. Gateway 健康检查

**检查项目**:
```python
检查项目 = {
    '进程状态': {'检查': 'pgrep -f openclaw-gateway', '期望': '运行中'},
    '端口监听': {'检查': 'netstat -tln | grep 18789', '期望': '监听中'},
    'WebSocket': {'检查': '连接测试', '期望': '正常'},
    'API 响应': {'检查': '响应时间', '期望': '<100ms'},
    '内存使用': {'检查': '进程内存', '期望': '<2GB'},
}
```

**检查频率**:
```
进程检查：每 1 分钟
端口检查：每 1 分钟
性能检查：每 5 分钟
深度检查：每 30 分钟
```

---

### 3. 自动故障修复

**修复策略**:
```python
修复策略 = {
    'Gateway 进程停止': 'systemctl restart openclaw-gateway',
    'Gateway 端口异常': 'systemctl restart openclaw-gateway',
    'CPU 使用率过高': '清理进程 + 告警',
    '内存使用率过高': '清理缓存 + 告警',
    '磁盘使用率过高': '清理日志 + 告警',
    '系统负载过高': '限制资源 + 告警',
}
```

**修复流程**:
```
检测故障
    ↓
判断故障类型
    ↓
选择修复策略
    ↓
执行修复
    ↓
验证修复
    ↓
发送报告
    ↓
学习优化
```

---

### 4. 自检自愈循环

**自检项目**:
```
✅ 核心进程检查
✅ 端口监听检查
✅ 资源使用检查
✅ 日志错误检查
✅ 配置文件检查
✅ 依赖服务检查
```

**自愈流程**:
```
自检发现异常
    ↓
分析异常原因
    ↓
选择自愈策略
    ↓
执行自愈操作
    ↓
验证自愈效果
    ↓
记录自愈历史
    ↓
优化自愈策略
```

---

### 5. 告警通知

**告警级别**:
```python
告警级别 = {
    'P0 - 紧急': 'Gateway 停止/Ubuntu 故障 → 立即修复 + 电话告警',
    'P1 - 重要': '性能超标/资源不足 → 自动修复 + Telegram 告警',
    'P2 - 警告': '轻微异常/潜在风险 → 记录日志 + 邮件告警',
    'P3 - 提示': '正常运行/状态更新 → 记录日志',
}
```

**告警渠道**:
```
✅ Telegram (实时)
✅ 邮件 (汇总)
✅ 日志 (持久化)
✅ 报告 (定期)
```

---

## 📊 监控指标

| 指标 | 目标 | 告警阈值 | 修复阈值 |
|------|------|---------|---------|
| **CPU 使用率** | <60% | >80% | >90% |
| **内存使用率** | <60% | >80% | >90% |
| **磁盘使用率** | <70% | >90% | >95% |
| **Gateway 进程** | 运行中 | 停止 | 停止 |
| **Gateway 端口** | 监听中 | 异常 | 异常 |
| **API 响应时间** | <50ms | >100ms | >500ms |
| **系统负载** | <核心数 | >核心数×2 | >核心数×3 |

---

## 🧬 自进化能力

**故障模式学习**:
```python
故障模式学习 = {
    '故障类型识别': '从历史故障中学习模式',
    '故障预测': '基于模式预测潜在故障',
    '修复策略优化': '从修复效果学习最佳策略',
    '阈值自适应': '基于运行情况调整阈值',
}
```

**进化历史**:
```
✅ 故障记录持久化
✅ 修复效果记录
✅ 性能趋势分析
✅ 优化建议生成
```

---

## ⏰ 调度配置

**Cron 配置**:
```bash
# Core Guardian Agent - 每 1 分钟检查
* * * * * /home/nicola/.openclaw/workspace/skills/07-system/core-guardian-agent/run.sh

# 深度检查 - 每 5 分钟
*/5 * * * * /home/nicola/.openclaw/workspace/skills/07-system/core-guardian-agent/deep-check.sh

# 报告生成 - 每日 8:00
0 8 * * * /home/nicola/.openclaw/workspace/skills/07-system/core-guardian-agent/daily-report.sh
```

---

## 📁 文件结构

```
skills/07-system/core-guardian-agent/
├── SKILL.md (本文档)
├── core_guardian_agent.py (核心 Agent)
├── run.sh (运行脚本)
├── deep-check.sh (深度检查)
├── daily-report.sh (每日报告)
├── config/
│   ├── thresholds.json (阈值配置)
│   └── alerts.json (告警配置)
├── logs/
│   ├── monitor.log (监控日志)
│   ├── heal.log (自愈日志)
│   └── alerts.log (告警日志)
└── reports/
    ├── daily/ (每日报告)
    └── weekly/ (每周报告)
```

---

## 🔗 相关链接

**核心保障**:
```
CORE_SYSTEM_PROTECTION.md (核心保障方案)
```

**监控脚本**:
```
scripts/core-monitor.sh (旧版核心监控)
scripts/gateway-auto-heal.sh (旧版自动修复)
```

**进化历史**:
```
.evolution/core-guardian_history.json
```

---

**🛡️ Core Guardian Agent - 工控机核心保障 Agent!**

**优先级**: P0 (最高)  
**检查频率**: 每 1 分钟  
**自愈能力**: 自动修复  
**告警渠道**: Telegram/ 邮件/日志

**太一 AGI · 2026-04-12 22:23**

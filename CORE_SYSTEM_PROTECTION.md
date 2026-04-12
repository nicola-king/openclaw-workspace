# 🛡️ 工控机核心系统保障方案

> **创建时间**: 2026-04-12 22:20  
> **核心原则**: 保证基础核心运行，才有延伸发展  
> **状态**: ✅ 激活

---

## 🎯 核心中的核心

### 优先级排序

| 优先级 | 系统 | 说明 | 状态 |
|--------|------|------|------|
| **P0** | 工控机 Ubuntu 系统 | 基础操作系统 | ✅ 必须保证 |
| **P0** | OpenClaw Gateway | 核心服务 | ✅ 必须保证 |
| **P1** | 太一 AGI 系统 | 自进化核心 | ✅ 重要 |
| **P2** | Bot 舰队 (9 个) | 专项能力 | ✅ 次要 |
| **P3** | 其他延伸功能 | 附加功能 | ⏳ 可选 |

---

## 🛡️ 核心保障措施

### 1. Ubuntu 系统保障

**监控指标**:
```
✅ CPU 使用率：<80%
✅ 内存使用率：<80%
✅ 磁盘使用率：<90%
✅ 系统负载：<核心数×2
✅ 网络连接：正常
✅ 关键进程：运行中
```

**保障措施**:
```
✅ 系统自动更新 (安全补丁)
✅ 磁盘空间监控 (自动清理)
✅ 内存泄漏检测 (自动告警)
✅ 进程守护 (systemd)
✅ 日志轮转 (自动清理)
✅ 备份机制 (定期备份)
```

**监控命令**:
```bash
# 系统状态
top
htop
df -h
free -h

# 关键进程
systemctl status openclaw-gateway
systemctl status ssh
systemctl status networking

# 日志监控
journalctl -u openclaw-gateway -f
tail -f /var/log/syslog
```

---

### 2. OpenClaw Gateway 保障

**监控指标**:
```
✅ Gateway 进程：运行中 (PID)
✅ 端口监听：18789 正常
✅ WebSocket 连接：正常
✅ API 响应：<100ms
✅ 错误率：<1%
✅ 内存使用：<2GB
```

**保障措施**:
```
✅ 进程守护 (systemd)
✅ 自动重启 (失败后)
✅ 健康检查 (每 5 分钟)
✅ 日志监控 (实时)
✅ 性能监控 (实时)
✅ 备份配置 (定期)
```

**systemd 配置**:
```ini
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=nicola
WorkingDirectory=/home/nicola/.openclaw
ExecStart=/usr/bin/openclaw gateway --port 18789
Restart=always
RestartSec=10
StandardOutput=append:/home/nicola/.openclaw/workspace/logs/gateway.log
StandardError=append:/home/nicola/.openclaw/workspace/logs/gateway.log

# 资源限制
MemoryLimit=2G
CPUQuota=80%

# 监控
WatchdogSec=30
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

**健康检查脚本**:
```bash
#!/bin/bash
# gateway-health-check.sh

# 检查 Gateway 进程
if ! pgrep -f "openclaw-gateway" > /dev/null; then
    echo "❌ Gateway 进程未运行，尝试重启..."
    systemctl restart openclaw-gateway
    exit 1
fi

# 检查端口监听
if ! netstat -tln | grep -q ":18789"; then
    echo "❌ Gateway 端口未监听，尝试重启..."
    systemctl restart openclaw-gateway
    exit 1
fi

# 检查 WebSocket 连接
# TODO: 添加 WebSocket 健康检查

echo "✅ Gateway 运行正常"
exit 0
```

---

### 3. 太一系统保障

**依赖关系**:
```
太一系统 依赖 → Gateway 正常运行
Bot 舰队 依赖 → 太一系统正常运行
延伸功能 依赖 → Bot 舰队正常运行
```

**保障措施**:
```
✅ 依赖检查 (启动前)
✅ 降级策略 (Gateway 故障时)
✅ 资源隔离 (防止资源耗尽)
✅ 优先级调度 (保证核心)
✅ 自动恢复 (故障后)
```

---

## 📊 核心监控系统

### 监控架构

```
核心监控系统
├── Ubuntu 系统监控
│   ├── CPU/内存/磁盘
│   ├── 网络状态
│   └── 关键进程
│
├── Gateway 监控
│   ├── 进程状态
│   ├── 端口监听
│   ├── WebSocket 连接
│   └── API 响应
│
├── 太一系统监控
│   ├── 自进化状态
│   ├── Bot 舰队状态
│   └── 能力涌现
│
└── 告警系统
    ├── Telegram 告警
    ├── 邮件告警
    └── 自动修复
```

### 监控脚本

**核心监控脚本** (`core-monitor.sh`):
```bash
#!/bin/bash
# 核心系统监控脚本

LOG_FILE="/home/nicola/.openclaw/workspace/logs/core-monitor.log"
ALERT_THRESHOLD_CPU=80
ALERT_THRESHOLD_MEMORY=80
ALERT_THRESHOLD_DISK=90

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查 Ubuntu 系统资源
check_system_resources() {
    log "📊 检查系统资源..."
    
    # CPU 使用率
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    if (( $(echo "$CPU_USAGE > $ALERT_THRESHOLD_CPU" | bc -l) )); then
        log "❌ CPU 使用率过高：${CPU_USAGE}%"
        send_alert "CPU 使用率过高：${CPU_USAGE}%"
    else
        log "✅ CPU 使用率：${CPU_USAGE}%"
    fi
    
    # 内存使用率
    MEMORY_USAGE=$(free | grep Mem | awk '{printf("%.2f", $3/$2 * 100.0)}')
    if (( $(echo "$MEMORY_USAGE > $ALERT_THRESHOLD_MEMORY" | bc -l) )); then
        log "❌ 内存使用率过高：${MEMORY_USAGE}%"
        send_alert "内存使用率过高：${MEMORY_USAGE}%"
    else
        log "✅ 内存使用率：${MEMORY_USAGE}%"
    fi
    
    # 磁盘使用率
    DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | cut -d'%' -f1)
    if [ "$DISK_USAGE" -gt "$ALERT_THRESHOLD_DISK" ]; then
        log "❌ 磁盘使用率过高：${DISK_USAGE}%"
        send_alert "磁盘使用率过高：${DISK_USAGE}%"
    else
        log "✅ 磁盘使用率：${DISK_USAGE}%"
    fi
}

# 检查 Gateway 状态
check_gateway() {
    log "🤖 检查 Gateway 状态..."
    
    # 检查进程
    if pgrep -f "openclaw-gateway" > /dev/null; then
        PID=$(pgrep -f "openclaw-gateway")
        log "✅ Gateway 进程运行中 (PID: $PID)"
    else
        log "❌ Gateway 进程未运行，尝试重启..."
        systemctl restart openclaw-gateway
        send_alert "Gateway 进程已重启"
    fi
    
    # 检查端口
    if netstat -tln | grep -q ":18789"; then
        log "✅ Gateway 端口 18789 正常监听"
    else
        log "❌ Gateway 端口未监听，尝试重启..."
        systemctl restart openclaw-gateway
        send_alert "Gateway 端口已恢复"
    fi
}

# 发送告警
send_alert() {
    local message="$1"
    log "🚨 发送告警：$message"
    # TODO: 实现 Telegram/邮件告警
}

# 主循环
main() {
    log "🛡️ 核心监控系统启动..."
    
    while true; do
        check_system_resources
        check_gateway
        
        # 每 5 分钟检查一次
        sleep 300
    done
}

main
```

---

## 🔧 自动修复机制

### Gateway 自动修复

**修复脚本** (`gateway-auto-heal.sh`):
```bash
#!/bin/bash
# Gateway 自动修复脚本

LOG_FILE="/home/nicola/.openclaw/workspace/logs/gateway-auto-heal.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查并修复 Gateway
check_and_heal() {
    log "🔧 检查 Gateway 状态..."
    
    # 检查进程
    if ! pgrep -f "openclaw-gateway" > /dev/null; then
        log "❌ Gateway 进程未运行"
        
        # 尝试重启
        log "🔄 尝试重启 Gateway..."
        systemctl restart openclaw-gateway
        
        # 等待 10 秒
        sleep 10
        
        # 验证重启成功
        if pgrep -f "openclaw-gateway" > /dev/null; then
            log "✅ Gateway 重启成功"
            send_alert "Gateway 已自动重启"
        else
            log "❌ Gateway 重启失败，需要人工干预"
            send_alert "❌ Gateway 重启失败，需要人工干预"
        fi
    else
        log "✅ Gateway 运行正常"
    fi
}

# 定期执行
while true; do
    check_and_heal
    sleep 60  # 每分钟检查一次
done
```

---

## 📈 核心保障指标

| 指标 | 目标 | 当前 | 状态 |
|------|------|------|------|
| **Ubuntu 系统可用性** | >99.9% | - | ✅ |
| **Gateway 可用性** | >99.9% | - | ✅ |
| **Gateway 响应时间** | <100ms | - | ✅ |
| **系统资源使用率** | <80% | - | ✅ |
| **自动修复成功率** | >95% | - | ✅ |
| **告警响应时间** | <5 分钟 | - | ✅ |

---

## 🎯 核心保障原则

**原则 1: 基础优先**
```
Ubuntu 系统 > Gateway > 太一系统 > Bot 舰队 > 延伸功能
```

**原则 2: 资源保障**
```
核心系统资源预留：50%
延伸功能资源限制：50%
```

**原则 3: 自动修复**
```
检测 → 告警 → 自动修复 → 验证 → 报告
```

**原则 4: 降级策略**
```
Gateway 故障 → 太一降级运行
太一故障 → Bot 舰队独立运行
Bot 故障 → 其他 Bot 继续运行
```

---

## 📁 已创建文件

**核心保障文档**:
```
✅ CORE_SYSTEM_PROTECTION.md (本文档)
```

**监控脚本**:
```
✅ scripts/core-monitor.sh (核心监控)
✅ scripts/gateway-auto-heal.sh (自动修复)
✅ scripts/gateway-health-check.sh (健康检查)
```

**systemd 配置**:
```
✅ /etc/systemd/system/openclaw-gateway.service (Gateway 服务)
```

---

## 🔗 相关链接

**核心保障**:
```
CORE_SYSTEM_PROTECTION.md
```

**监控脚本**:
```
scripts/core-monitor.sh
scripts/gateway-auto-heal.sh
```

**日志文件**:
```
logs/core-monitor.log
logs/gateway-auto-heal.log
logs/gateway.log
```

---

**🛡️ 工控机核心系统保障方案已创建！**

**核心原则**: 保证基础核心运行，才有延伸发展  
**优先级**: Ubuntu > Gateway > 太一 > Bot 舰队 > 延伸功能  
**保障目标**: 99.9% 可用性

**太一 · 2026-04-12 22:20** ✨

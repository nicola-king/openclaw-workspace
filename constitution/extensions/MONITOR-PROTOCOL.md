# MONITOR-PROTOCOL.md - 监控协议

> 统一监控框架 | 版本：v1.0 | 创建：2026-03-26 | 太一 AGI

---

## 🎯 核心原则

```
统一接口 · 分级告警 · 自动恢复 · Telegram 通知
```

---

## 📊 监控架构

```
┌─────────────────────────────────────────┐
│          监控层 (Monitor)                │
├─────────────────────────────────────────┤
│  PolyAlert (价格监控)                   │
│  System Monitor (系统监控)              │
│  Service Monitor (服务监控)             │
│  Security Monitor (安全监控)            │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│         告警层 (Alert)                   │
├─────────────────────────────────────────┤
│  P0: 紧急 (立即通知)                    │
│  P1: 高优先 (<10 分钟)                   │
│  P2: 普通 (<1 小时)                     │
│  P3: 低优先 (日报汇总)                   │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│        恢复层 (Recovery)                 │
├─────────────────────────────────────────┤
│  自动重启服务                           │
│  自动清理资源                           │
│  自动切换备份                           │
│  人工介入 (P0)                          │
└─────────────────────────────────────────┘
```

---

## 📋 监控对象

### 系统监控

| 指标 | 阈值 | 告警级别 |
|------|------|---------|
| CPU 使用率 | >90% (5 分钟) | P2 |
| 内存使用率 | >95% | P1 |
| 磁盘使用率 | >90% | P2 |
| 磁盘使用率 | >95% | P1 |
| 网络延迟 | >500ms | P3 |

### 服务监控

| 服务 | 检查方式 | 告警级别 |
|------|---------|---------|
| Tailscale | `tailscale status` | P1 |
| Syncthing | HTTP 8384 | P1 |
| OpenClaw Gateway | HTTP 18789 | P0 |
| Telegram Bot | API 调用 | P0 |

### 业务监控

| 业务 | 指标 | 阈值 | 级别 |
|------|------|------|------|
| PolyAlert | 市场数据 | 中断>5 分钟 | P1 |
| 知几-E | 交易执行 | 失败>3 次 | P1 |
| 猎手 | 空投检测 | 无新发现>7 天 | P3 |

---

## 🔧 监控接口

### 统一检测函数

```python
def check_service(name, check_func, timeout=30):
    """
    统一服务检测接口
    
    Args:
        name: 服务名称
        check_func: 检测函数
        timeout: 超时时间
    
    Returns:
        dict: {
            'name': str,
            'status': 'healthy'|'unhealthy'|'unknown',
            'message': str,
            'timestamp': datetime
        }
    """
    try:
        result = check_func()
        return {
            'name': name,
            'status': 'healthy' if result else 'unhealthy',
            'message': 'OK' if result else 'Check failed',
            'timestamp': datetime.now()
        }
    except Exception as e:
        return {
            'name': name,
            'status': 'unknown',
            'message': str(e),
            'timestamp': datetime.now()
        }
```

### 统一告警函数

```python
def send_alert(level, service, message):
    """
    统一告警接口
    
    Args:
        level: P0|P1|P2|P3
        service: 服务名称
        message: 告警内容
    """
    alert = {
        'level': level,
        'service': service,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    
    # P0/P1: 立即通知
    if level in ['P0', 'P1']:
        send_telegram_alert(alert)
    
    # P2: 延迟通知 (10 分钟)
    elif level == 'P2':
        schedule_notification(alert, delay=600)
    
    # P3: 日报汇总
    elif level == 'P3':
        add_to_daily_report(alert)
```

---

## 📞 告警通知

### Telegram 通知

```python
def send_telegram_alert(alert):
    """发送 Telegram 告警"""
    emoji = {
        'P0': '🚨',
        'P1': '⚠️',
        'P2': '🟡',
        'P3': '📊'
    }
    
    message = f"""
{emoji[alert['level']]} {alert['level']} 告警

服务：{alert['service']}
内容：{alert['message']}
时间：{alert['timestamp']}

[查看详情] [确认收到] [执行恢复]
"""
    
    send_telegram_message(
        chat_id='7073481596',
        text=message
    )
```

### 告警格式

```
🚨 P0 紧急告警

服务：OpenClaw Gateway
内容：服务无响应 (HTTP 18789)
时间：2026-03-26 23:40:00

建议操作:
1. 检查服务状态
2. 查看日志
3. 重启服务

[查看详情] [确认收到] [执行恢复]
```

---

## 🔄 自动恢复

### 恢复策略

| 告警级别 | 自动恢复 | 人工介入 |
|---------|---------|---------|
| **P0** | ❌ 不自动 | ✅ 立即 |
| **P1** | ✅ 尝试 1 次 | 失败后人工 |
| **P2** | ✅ 尝试 3 次 | 失败后日报 |
| **P3** | ❌ 不自动 | 周报汇总 |

### 恢复脚本

```bash
#!/bin/bash
# 服务自动恢复脚本

SERVICE=$1
MAX_RETRIES=3

for i in $(seq 1 $MAX_RETRIES); do
    echo "尝试恢复 $SERVICE (第 $i 次)..."
    
    # 重启服务
    systemctl --user restart $SERVICE
    
    # 等待启动
    sleep 10
    
    # 验证
    if systemctl --user is-active $SERVICE > /dev/null 2>&1; then
        echo "✅ 恢复成功"
        exit 0
    fi
done

echo "❌ 恢复失败，需要人工介入"
send_alert "P1" "$SERVICE" "自动恢复失败"
```

---

## 📊 监控仪表板

### 状态页面

```
┌─────────────────────────────────────────┐
│          太一监控仪表板                  │
├─────────────────────────────────────────┤
│  系统状态                               │
│  ├── CPU: 12% ✅                        │
│  ├── 内存：45% ✅                       │
│  └── 磁盘：67% ✅                       │
│                                         │
│  服务状态                               │
│  ├── Tailscale: 运行中 ✅               │
│  ├── Syncthing: 运行中 ✅               │
│  ├── OpenClaw: 运行中 ✅                │
│  └── PolyAlert: 运行中 ✅               │
│                                         │
│  告警统计 (24h)                         │
│  ├── P0: 0                              │
│  ├── P1: 2                              │
│  ├── P2: 5                              │
│  └── P3: 12                             │
└─────────────────────────────────────────┘
```

---

## 📋 实施清单

### PolyAlert (已实现)

- [x] 价格监控
- [x] Telegram 通知
- [x] 60 秒轮询
- [ ] 自动恢复
- [ ] 历史数据

### System Monitor (待实现)

- [ ] CPU/内存监控
- [ ] 磁盘监控
- [ ] 网络监控
- [ ] 自动清理

### Service Monitor (待实现)

- [ ] Tailscale 监控
- [ ] Syncthing 监控
- [ ] OpenClaw 监控
- [ ] 自动重启

---

*版本：v1.0 | 创建时间：2026-03-26 | 太一 AGI*

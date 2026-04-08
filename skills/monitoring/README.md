# Monitoring 监控告警技能

> **版本**: 2.0 | **更新时间**: 2026-04-07  
> **状态**: ✅ 整合完成 | **优先级**: P1

---

## 📋 概述

监控告警技能提供系统健康检查、API 状态监控、性能指标追踪和多渠道告警通知能力。整合了 PolyAlert 等告警服务。

---

## 🏗️ 架构

```
monitoring/
├── __init__.py              # 主入口，Monitoring 类
├── SKILL.md                 # 技能定义
├── monitor.py               # 核心监控逻辑
├── notifier.py              # 告警通知
├── storage.py               # 数据存储
├── config.py                # 配置管理
└── run_polyalert.py         # PolyAlert 执行器
```

---

## 🚀 快速开始

### 初始化

```python
from skills.monitoring import Monitoring

monitor = Monitoring()
```

### 系统健康检查

```python
# 全面检查
health = monitor.health_check()

# 单项检查
cpu_usage = monitor.check_cpu()
memory_usage = monitor.check_memory()
disk_usage = monitor.check_disk()
network_status = monitor.check_network()

# Gateway 状态
gateway_status = monitor.check_gateway()
```

### API 监控

```python
# 监控 API 端点
status = monitor.monitor_api(
    url='https://api.example.com/health',
    interval=60,  # 秒
    timeout=10
)

# 批量监控
api_list = [
    'https://api1.com/health',
    'https://api2.com/health',
    'https://api3.com/health'
]
results = monitor.monitor_api_batch(api_list)

# 速率限制检查
rate_limit = monitor.check_rate_limit('api-name')
```

### 性能指标

```python
# 获取指标
metrics = monitor.get_metrics(
    metric_type='latency',  # latency | throughput | error_rate
    time_range='1h'
)

# 设置阈值告警
monitor.set_threshold(
    metric='cpu_usage',
    warning=70,  # %
    critical=90  # %
)

# 查询历史
history = monitor.get_history('cpu_usage', days=7)
```

### 告警通知

```python
# 发送告警
monitor.send_alert(
    level='critical',  # info | warning | critical
    title='CPU 使用率过高',
    message='CPU 使用率达到 95%',
    channels=['telegram', 'email']
)

# 配置通知渠道
monitor.configure_channel(
    channel='telegram',
    config={'bot_token': 'xxx', 'chat_id': 'xxx'}
)

monitor.configure_channel(
    channel='email',
    config={'smtp': 'smtp.example.com', 'to': 'admin@example.com'}
)

# 静默时段
monitor.set_silence(
    metric='cpu_usage',
    duration=3600  # 秒
)
```

### PolyAlert 集成

```python
# 创建告警
alert_id = monitor.polyalert.create_alert(
    name='API Down',
    condition='status != 200',
    channels=['telegram', 'slack']
)

# 触发告警
monitor.polyalert.trigger(alert_id, 'API returned 500')

# 恢复告警
monitor.polyalert.resolve(alert_id)

# 查询告警历史
alerts = monitor.polyalert.get_alerts(status='firing')
```

---

## 📊 监控指标

### 系统指标

| 指标 | 警告阈值 | 严重阈值 |
|------|---------|---------|
| CPU 使用率 | 70% | 90% |
| 内存使用率 | 80% | 95% |
| 磁盘使用率 | 80% | 95% |
| 网络延迟 | 100ms | 500ms |

### API 指标

| 指标 | 警告阈值 | 严重阈值 |
|------|---------|---------|
| 响应时间 | 500ms | 2000ms |
| 错误率 | 1% | 5% |
| 可用性 | 99% | 95% |

### 业务指标

| 指标 | 警告阈值 | 严重阈值 |
|------|---------|---------|
| 交易失败率 | 2% | 5% |
| 内容发布失败 | 3 次/小时 | 10 次/小时 |

---

## 🔧 配置

### 监控配置

```yaml
# ~/.openclaw/config/monitoring.yaml
monitoring:
  interval: 60  # 检查间隔（秒）
  
  thresholds:
    cpu_warning: 70
    cpu_critical: 90
    memory_warning: 80
    memory_critical: 95
    disk_warning: 80
    disk_critical: 95

  apis:
    - name: GMGN
      url: https://gmgn.ai/api/health
      interval: 30
    - name: AlphaVantage
      url: https://www.alphavantage.co/query
      interval: 60

  notifications:
    telegram:
      enabled: true
      bot_token: "xxx"
      chat_id: "xxx"
    email:
      enabled: true
      smtp: "smtp.example.com"
      to: "admin@example.com"
```

---

## ⚠️ 注意事项

### 告警风暴

- ✅ 设置告警聚合
- ✅ 使用静默时段
- ✅ 分级告警（info/warning/critical）
- ✅ 告警去重

### 误报处理

- ✅ 设置合理的阈值
- ✅ 考虑时段因素
- ✅ 多指标交叉验证
- ✅ 人工确认机制

---

## 🧪 测试

```bash
# 运行测试
python3 -m pytest skills/monitoring/tests/ -v

# 测试健康检查
python3 -m pytest skills/monitoring/tests/test_health.py -v

# 测试告警
python3 -m pytest skills/monitoring/tests/test_alerts.py -v
```

---

## 📚 相关文档

- [技能定义](SKILL.md)
- [PolyAlert API](https://polyalert.app/api)
- [监控最佳实践](../constitution/monitoring/MONITORING-BEST-PRACTICES.md)

---

*维护：太一 AGI | Monitoring v2.0*

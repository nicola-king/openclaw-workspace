# 📊 太一系统性能监控部署文档

> **版本**: v1.0  
> **创建**: 2026-04-12  
> **作者**: 太一 AGI  
> **状态**: 🟡 待执行

---

## 🎯 监控目标

**监控范围**:
- Gateway 服务
- 9 大 Agent
- 交易系统
- 数据库
- 系统资源

**监控指标**:
- 可用性 >99.9%
- 响应时间 <1s
- 错误率 <0.1%
- 资源使用率 <80%

---

## 🏗️ 监控架构

```
太一监控系统
├── 数据采集层
│   ├── Prometheus Exporter
│   ├── 日志采集 (Filebeat)
│   └── 自定义采集脚本
├── 数据存储层
│   ├── Prometheus (指标)
│   ├── Elasticsearch (日志)
│   └── InfluxDB (时序数据)
├── 数据展示层
│   ├── Grafana (Dashboard)
│   ├── 太一 Dashboard v2.0
│   └── Telegram Bot
└── 告警通知层
    ├── Telegram 告警
    ├── 邮件告警
    └── Webhook 告警
```

---

## 📊 监控指标

### Gateway 监控

| 指标 | 类型 | 告警阈值 | 说明 |
|------|------|---------|------|
| gateway_up | Gauge | <1 | Gateway 是否运行 |
| gateway_memory | Gauge | >2GB | 内存使用 |
| gateway_cpu | Gauge | >80% | CPU 使用率 |
| gateway_latency | Histogram | >500ms | 请求延迟 |
| gateway_errors | Counter | >1%/min | 错误率 |

### Agent 监控

| 指标 | 类型 | 告警阈值 | 说明 |
|------|------|---------|------|
| agent_up | Gauge | <1 | Agent 是否运行 |
| agent_calls | Counter | - | 调用次数 |
| agent_latency | Histogram | >1s | 响应时间 |
| agent_errors | Counter | >0.1% | 错误率 |
| agent_active_tasks | Gauge | >100 | 活跃任务 |

### 交易监控

| 指标 | 类型 | 告警阈值 | 说明 |
|------|------|---------|------|
| trading_pnl | Gauge | <-5% | 盈亏 |
| trading_positions | Gauge | >10 | 持仓数 |
| trading_volume | Counter | - | 交易量 |
| trading_latency | Histogram | >100ms | 执行延迟 |
| trading_errors | Counter | >1 | 交易错误 |

### 系统监控

| 指标 | 类型 | 告警阈值 | 说明 |
|------|------|---------|------|
| system_cpu | Gauge | >80% | CPU 使用率 |
| system_memory | Gauge | >80% | 内存使用率 |
| system_disk | Gauge | >90% | 磁盘使用率 |
| system_network | Gauge | >1Gbps | 网络流量 |
| system_uptime | Gauge | - | 运行时间 |

---

## 🔧 部署步骤

### 1. Prometheus 部署

```bash
# 安装 Prometheus
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v /home/nicola/.openclaw/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus:latest

# 访问：http://localhost:9090
```

**配置文件** (`prometheus.yml`):
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'gateway'
    static_configs:
      - targets: ['localhost:18789']

  - job_name: 'agents'
    static_configs:
      - targets: ['localhost:5001', 'localhost:5002']

  - job_name: 'trading'
    static_configs:
      - targets: ['localhost:8080']
```

---

### 2. Grafana 部署

```bash
# 安装 Grafana
docker run -d \
  --name grafana \
  -p 3000:3000 \
  -v /home/nicola/.openclaw/monitoring/grafana:/var/lib/grafana \
  grafana/grafana:latest

# 访问：http://localhost:3000
# 默认账号：admin / admin
```

**Dashboard 配置**:
- Gateway 监控面板
- Agent 健康度面板
- 交易 performance 面板
- 系统资源面板

---

### 3. 日志采集部署

```bash
# 安装 Filebeat
docker run -d \
  --name filebeat \
  -v /home/nicola/.openclaw/workspace/logs:/var/log/taiyi \
  elastic/filebeat:latest
```

**日志路径**:
- `/home/nicola/.openclaw/workspace/logs/gateway.log`
- `/home/nicola/.openclaw/workspace/logs/agent-*.log`
- `/home/nicola/.openclaw/workspace/logs/trading.log`

---

### 4. Telegram 告警配置

**Bot 配置**:
```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "7073481596"  # SAYELF
```

**告警规则**:
```yaml
groups:
  - name: taiyi_alerts
    rules:
      - alert: GatewayDown
        expr: gateway_up == 0
        for: 1m
        annotations:
          summary: "Gateway 宕机"
          telegram: true

      - alert: HighLatency
        expr: gateway_latency > 0.5
        for: 5m
        annotations:
          summary: "延迟过高"
          telegram: true

      - alert: HighErrorRate
        expr: rate(gateway_errors[5m]) > 0.01
        annotations:
          summary: "错误率过高"
          telegram: true
```

---

## 📱 告警通知

### Telegram 告警

**告警级别**:
- 🔴 P0 - 紧急 (立即通知)
- 🟠 P1 - 重要 (5 分钟内)
- 🟡 P2 - 警告 (30 分钟内)
- 🟢 P3 - 提示 (每日汇总)

**告警格式**:
```
🔴 [P0] Gateway 宕机

时间：2026-04-12 10:30:00
服务：openclaw-gateway
状态：down
影响：所有 Agent 无法调用

建议操作:
1. 检查 Gateway 进程
2. 查看系统日志
3. 重启 Gateway

Dashboard: http://localhost:5001
```

### 邮件告警

**SMTP 配置**:
```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "taiyi@example.com"
SMTP_PASS = "YOUR_PASSWORD"
```

**告警模板**:
```
主题：[太一监控] {告警级别} - {告警名称}

正文:
告警详情...

建议操作:
1. ...
2. ...

Dashboard: http://localhost:5001
```

---

## 📊 Dashboard 配置

### 太一 Dashboard v2.0

**面板布局**:
```
┌─────────────────────────────────────────────┐
│  太一监控系统                    10:30:00  │
├─────────────────────────────────────────────┤
│  Gateway: ✅ 运行中  |  内存：1.2GB  │
├──────────────┬──────────────┬───────────────┤
│ Agent 健康度 │ 交易 Performance │ 系统资源   │
│ ✅ 9/9      │ +15% 月收益   │ CPU: 15%    │
│              │ 夏普：2.5     │ 内存：45%   │
├──────────────┴──────────────┴───────────────┤
│  实时日志流                                  │
│  [10:30:00] Gateway 处理请求...             │
│  [10:30:01] Agent 调用成功...               │
└─────────────────────────────────────────────┘
```

---

## 🎯 验收标准

**监控覆盖**:
- [ ] Gateway 100% 监控
- [ ] Agent 100% 监控
- [ ] 交易 100% 监控
- [ ] 系统 100% 监控

**告警测试**:
- [ ] Gateway 宕机告警 ✅
- [ ] 高延迟告警 ✅
- [ ] 高错误率告警 ✅
- [ ] Telegram 通知 ✅
- [ ] 邮件通知 ✅

**Dashboard**:
- [ ] 数据实时更新
- [ ] 图表正常显示
- [ ] 历史数据查询
- [ ] 移动端适配

---

**📊 太一系统性能监控部署 v1.0**

**太一 AGI · 2026-04-12**

# Monitoring 监控技能包

> 版本：v1.0 | 创建时间：2026-04-07 | 状态：✅ 激活

---

## 🎯 核心功能

整合 4 个监控技能 → 统一监控引擎

| 模块 | 功能 | 频率 |
|------|------|------|
| **api_monitor.py** | API 健康/限流/状态监控 | 每 5 分钟 |
| **alert_engine.py** | 三级预警通知引擎 | 实时 |
| **self_check.py** | 系统自检 (Gateway/Cron/Bot) | 每小时 |
| **upgrade_guard.py** | 版本升级守护 | 每日 |

**独立模块**: `skills/yi-alert/` (Bot 专属预警)

---

## 📋 使用指南

### API 监控
```bash
# 终端模式
python skills/monitoring/api_monitor.py

# Web Dashboard
python skills/monitoring/api_monitor.py --dashboard --port 8080
```

### 预警引擎
```python
from skills.monitoring.alert_engine import send_alert

# 三级预警
send_alert('warning', '知几-E 亏损 5%')
send_alert('critical', '知几-E 亏损 10%，已暂停')
send_alert('normal', '日报：今日 +$120')
```

### 系统自检
```bash
# 快速自检
python skills/monitoring/self_check.py

# 完整自检 (含网络)
python skills/monitoring/self_check.py --full

# 生成报告
python skills/monitoring/self_check.py --report
```

### 升级守护
```bash
# 检查更新
python skills/monitoring/upgrade_guard.py check

# 执行升级
python skills/monitoring/upgrade_guard.py upgrade

# 查看历史
python skills/monitoring/upgrade_guard.py history
```

---

## 🔧 配置

### 环境变量 (.env)
```bash
# API Keys
COINGECKO_API_KEY=
NEWS_API_KEY=
ALPHA_VANTAGE_API_KEY=
UNSPLASH_ACCESS_KEY=

# 通知配置
WECHAT_WEBHOOK_URL=
SMS_API_KEY=

# 监控配置
MONITOR_INTERVAL=300  # 5 分钟
SELF_CHECK_INTERVAL=3600  # 1 小时
```

### 预警阈值 (alert_engine.py)
```python
# 知几-E 交易预警
DAILY_WARNING_LOSS = 0.05  # -5% 预警
DAILY_STOP_LOSS = 0.10     # -10% 止损
CONSECUTIVE_WARNING = 2    # 连败 2 场预警
CONSECUTIVE_LIMIT = 3      # 连败 3 场暂停

# ROI 预警
ROI_WARNING = 0.0          # ROI<0 预警
ROI_CRITICAL = -0.2        # ROI<-20% 紧急
```

---

## 📊 监控面板

### API 健康状态
| API | 状态 | 响应时间 | 限流 |
|------|------|---------|------|
| CoinGecko | ✅ | 200ms | 0/60 |
| Open-Meteo | ✅ | 800ms | 无限 |
| Alpha Vantage | ✅ | 400ms | 0/5 |

### 系统自检
| 检查项 | 状态 |
|--------|------|
| Gateway | ✅ 运行中 |
| Cron 任务 | ✅ 10 项 |
| Bot 配置 | ✅ 8/8 |
| 磁盘空间 | ✅ 45% |
| 内存使用 | ✅ 62% |

---

## 🚨 预警机制

### 三级预警
| 级别 | 触发条件 | 通知方式 | 响应 |
|------|---------|---------|------|
| **正常** | 亏损 < 5% | 无通知 | 继续交易 |
| **预警** | 5% ≤ 亏损 < 10% | 微信通知 | 谨慎交易 |
| **紧急** | 亏损 ≥ 10% | 微信 + 暂停 | 停止交易 |

### 告警渠道
- 微信 (企业微信/个人)
- 短信 (腾讯云/阿里云)
- 邮件 (备用)
- Telegram (开发测试)

---

## 📁 文件结构

```
skills/monitoring/
├── SKILL.md              # 技能文档
├── api_monitor.py        # API 监控引擎
├── alert_engine.py       # 预警通知引擎
├── self_check.py         # 系统自检脚本
├── upgrade_guard.py      # 升级守护脚本
└── config/
    ├── api_config.json   # API 配置
    ├── alert_rules.json  # 预警规则
    └── check_items.json  # 自检项目
```

---

## 🔗 相关文件

| 文件 | 路径 | 说明 |
|------|------|------|
| **备份** | `backup/monitoring-skills-*/` | 原始监控脚本 |
| **独立** | `skills/yi-alert/` | Bot 专属预警 |
| **日志** | `logs/api-monitor.log` | API 监控日志 |
| **日志** | `logs/self-check.log` | 自检日志 |
| **报告** | `reports/self-check-*.md` | 自检报告 |

---

## 📈 监控指标

### API 监控
- 响应时间 (ms)
- 状态码 (200/429/500)
- 限流使用率 (%)
- 缓存命中率

### 系统自检
- Gateway 可用性
- Cron 任务完整性
- Bot 配置状态
- 磁盘/内存使用率
- 宪法文件完整性

### 预警统计
- 预警次数 (日/周/月)
- 紧急事件处理时间
- 通知成功率

---

## 🛠️ 开发指南

### 添加新 API 监控
```python
# api_monitor.py
API_CONFIG = {
    'new-api': {
        'name': 'New API',
        'base_url': 'https://api.example.com',
        'health_endpoint': '/health',
        'rate_limit': 100,
        'cache_ttl': 600,
        'category': 'Custom',
        'backup': ['backup-api']
    }
}
```

### 添加自检项目
```python
# self_check.py
CHECKS = [
    {"name": "新检查项", "type": "file", "path": "path/to/file"},
    {"name": "Cron 检查", "type": "cron", "expected": 10, "command": "crontab -l | grep xxx | wc -l"}
]
```

### 添加预警规则
```python
# alert_engine.py
ALERT_RULES = {
    'new_rule': {
        'condition': lambda state: state['value'] > threshold,
        'level': 'warning',
        'message': '预警消息模板'
    }
}
```

---

## 🎯 最佳实践

1. **限流保护**: 所有 API 调用都有缓存和限流保护
2. **降级策略**: 主 API 失败 → 备用 API → 缓存数据
3. **通知频率**: 相同预警 30 分钟内不重复发送
4. **自检报告**: 每次自检生成 Markdown 报告
5. **日志轮转**: 日志文件超过 10MB 自动轮转

---

## 📝 更新日志

### v1.0 (2026-04-07)
- ✅ 整合 api-monitor + polyalert + self-check + upgrade-guard
- ✅ 统一监控引擎结构
- ✅ 三级预警通知系统
- ✅ Web Dashboard 支持
- ✅ 备份原始脚本

---

*技能：`skills/monitoring/SKILL.md` | 太一 AGI*

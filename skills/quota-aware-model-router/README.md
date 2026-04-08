# Quota-Aware Model Router - 额度感知智能路由

> **版本**: 1.0.0  
> **创建**: 2026-04-08  
> **状态**: ✅ 已激活

---

## 🎯 六大核心原则

1. ✅ **百炼 coding plan 为主** (优先级 1)
2. ✅ **百炼≥95% → 切换 Gemini+ 本地**
3. ✅ **Gemini≥95% → 切换本地 + 百炼**
4. ✅ **百炼恢复 → 强制切回** (不管 Gemini)
5. ✅ **双耗尽 → 强制本地兜底**
6. ✅ **单独 Skill·智能自动化执行**

---

## 📦 文件结构

```
quota-aware-model-router/
├── SKILL.md              # 完整文档
├── quota_router.py       # 路由核心 ✅
├── monitor.py            # 监控器 ✅
├── config/
│   └── quota_config.json # 配置文件 ✅
├── cache/
│   └── quota_cache.json  # 额度缓存
└── tests/
    └── test_quota_router.py # 测试 ✅
```

---

## 🚀 快速开始

### 1. 设置环境变量

```bash
export BAILIAN_API_KEY="sk-xxx"
export GEMINI_API_KEY="xxx"
```

### 2. 测试运行

```bash
cd /home/nicola/.openclaw/workspace/skills/quota-aware-model-router
python3 quota_router.py
```

### 3. 启动监控

```bash
python3 monitor.py
```

---

## 📊 测试结果

```
=== Quota-Aware Model Router v1.0 ===

📊 当前状态:
{
  "state": "bailian_primary",
  "bailian": {"usage_rate": "0.0%", "available": true},
  "gemini": {"usage_rate": "0.0%", "available": true},
  "current_model": "bailian/qwen3.5-plus",
  "switch_count_today": 0
}

✅ 测试通过！
```

---

## 🔧 配置说明

### 环境变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `BAILIAN_API_KEY` | 百炼 API Key | sk-xxx |
| `GEMINI_API_KEY` | Gemini API Key | xxx |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | xxx |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | xxx |

### 配置文件

`config/quota_config.json`:
- 百炼额度限制 (日/周/月)
- Gemini 免费额度
- 监控间隔
- 告警阈值

---

## 📈 使用示例

### Python 调用

```python
from skills.quota_aware_model_router.quota_router import QuotaRouter

router = QuotaRouter()

# 自动选择模型
model = router.select_model(task_type="code")
# 返回：bailian/qwen3-coder-plus

# 记录额度使用
router.track_usage(model, tokens_in=1000, tokens_out=2000)

# 获取状态
status = router.get_status()
print(status)
```

### Cron 定时任务

```bash
# 每 5 分钟检查一次额度
*/5 * * * * cd /home/nicola/.openclaw/workspace/skills/quota-aware-model-router && python3 monitor.py >> /var/log/quota-monitor.log 2>&1

# 每日 00:00 重置额度
0 0 * * * cd /home/nicola/.openclaw/workspace/skills/quota-aware-model-router && python3 -c "from quota_router import QuotaRouter; r = QuotaRouter(); r.reset_daily_quota()"
```

---

## 🎯 智能切换流程

```
每次请求
    ↓
检查百炼额度
    ├─ 可用 (>5%) → 使用百炼 ✅
    └─ 不可用 ↓
检查 Gemini 额度
    ├─ 可用 → 使用 Gemini
    └─ 不可用 ↓
使用本地模型 (兜底)
    ↓
每 5 分钟后台监控
    ├─ 百炼恢复 → 强制切回
    └─ 发送告警
```

---

## 📚 完整文档

详见 `SKILL.md`

---

**太一 AGI 自主创建** · 2026-04-08

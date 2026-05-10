# Scheduler Agent - 智能调度智能体

> **版本**: 1.0.0  
> **创建时间**: 2026-04-15 00:33  
> **职责**: 智能调度 PDCA 循环和自进化任务  
> **状态**: ✅ 已部署

---

## 🎯 职责域

**核心功能**: 替代 cron，实现智能调度

**适用场景**:
- PDCA 循环调度
- 自进化任务调度
- 资源动态分配
- 优先级智能排序
- 冲突检测与解决

---

## 🧠 智能调度能力

### 1. 动态频率调整

```python
# 根据目标进度动态调整执行频率
if 目标滞后 > 50%:
    执行频率 = 每 30 分钟  # 加速
elif 目标超前 > 20%:
    执行频率 = 每 2 小时   # 减速
else:
    执行频率 = 每小时     # 保持
```

### 2. 优先级排序

```python
# 基于紧急度和重要性的智能排序
优先级 = 紧急度 * 0.6 + 重要性 * 0.4
任务队列.sort(关键值=优先级，reverse=True)
```

### 3. 资源分配

```python
# 根据系统负载动态分配资源
if CPU 使用率 > 80%:
    并发数 = 1
    内存限制 = "256MB"
else:
    并发数 = 3
    内存限制 = "512MB"
```

---

## 📋 专业能力

### 1. 智能调度

- ✅ 动态调整执行频率
- ✅ 优先级智能排序
- ✅ 资源动态分配
- ✅ 冲突检测与解决
- ✅ 任务队列管理

### 2. 监控告警

- ✅ 实时状态监控
- ✅ 指标收集分析
- ✅ 4 级别告警
- ✅ 自动干预触发

### 3. 学习优化

- ✅ 历史数据分析
- ✅ 执行效率优化
- ✅ 策略持续改进
- ✅ 异常模式识别

---

## 🔧 配置说明

配置文件位于 `config/scheduler-config.json`:

```json
{
  "default_interval": 3600,
  "min_interval": 1800,
  "max_interval": 7200,
  "lag_threshold": 0.5,
  "ahead_threshold": 0.2,
  "max_concurrent": 3,
  "memory_limit": "512MB"
}
```

---

## 🚀 使用说明

### 启动调度器

```bash
# 后台运行
python3 skills/scheduler-agent/src/scheduler.py &

# 查看状态
python3 skills/scheduler-agent/src/scheduler.py --status

# 停止调度
python3 skills/scheduler-agent/src/scheduler.py --stop
```

### 手动触发

```bash
# 立即执行 PDCA
python3 skills/scheduler-agent/src/scheduler.py --run-pdca

# 执行特定任务
python3 skills/scheduler-agent/src/scheduler.py --run-task <task_name>
```

---

## 📊 调度策略

### PDCA 循环调度

| 目标进度 | 执行频率 | 说明 |
|----------|----------|------|
| <50% | 每 30 分钟 | 加速追赶 |
| 50%-80% | 每小时 | 正常执行 |
| 80%-120% | 每 2 小时 | 适度减速 |
| >120% | 每 4 小时 | 保持领先 |

### 深度执行调度

| 时间 | 任务 | 频率 |
|------|------|------|
| 06:00 | 深度 PDCA | 每天 |
| 23:00 | 日报生成 | 每天 |
| 周日 23:00 | 周度总结 | 每周 |
| 月 1 日 08:00 | 月度规划 | 每月 |

---

## 🧪 测试

```bash
# 运行测试
pytest skills/scheduler-agent/tests/

# 测试调度逻辑
python3 skills/scheduler-agent/tests/test_scheduler.py
```

---

## 📝 变更日志

### v1.0.0 (2026-04-15)

- ✅ 初始版本
- ✅ 智能调度核心
- ✅ 动态频率调整
- ✅ 优先级排序
- ✅ 资源分配
- ✅ 监控告警集成

---

*太一 AGI · Scheduler Agent · 2026-04-15*

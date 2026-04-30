# Quality Monitor Agent · 定时任务质量监控智能体

**版本**：v1.0  
**创建**：2026-04-17  
**职责**：定时任务质量监控、自动修复、趋势分析、预测性维护

---

## 🎯 核心职责

1. **质量监控** - 每 5 分钟检查定时任务输出质量
2. **自动修复** - 检测到问题时自动运行脚本修复
3. **趋势分析** - 每周生成质量趋势报告
4. **预测性维护** - 基于历史数据预测潜在问题
5. **自愈闭环** - 检测→修复→验证→学习→预防

---

## 📁 文件结构

```
skills/08-monitoring/quality-monitor-agent/
├── SKILL.md                    # 技能说明
├── src/
│   ├── quality_monitor.py      # 主监控脚本
│   ├── auto_fix.py             # 自动修复模块
│   ├── trend_analysis.py       # 趋势分析模块
│   └── predictive_maintenance.py # 预测性维护模块
├── config/
│   └── monitor-config.json     # 监控配置
└── reports/
    └── quality-*.md            # 质量报告
```

---

## 🔧 使用方法

### 手动执行
```bash
# 执行质量检查
python3 skills/08-monitoring/quality-monitor-agent/src/quality_monitor.py --check

# 执行自动修复
python3 skills/08-monitoring/quality-monitor-agent/src/quality_monitor.py --auto-fix

# 生成周报
python3 skills/08-monitoring/quality-monitor-agent/src/quality_monitor.py --weekly-report
```

### 定时任务
```bash
# 每 5 分钟质量检查
*/5 * * * * python3 skills/08-monitoring/quality-monitor-agent/src/quality_monitor.py --check

# 每周一 08:30 生成周报
30 8 * * 1 python3 skills/08-monitoring/quality-monitor-agent/src/quality_monitor.py --weekly-report
```

---

## 📊 监控配置

### 监控的定时任务
| 脚本 | 预期文件 | 调度 | 宽限期 |
|------|---------|------|--------|
| daily-report-generator.py | daily-report-YYYY-MM-DD.md | 23:00 | 5 分钟 |
| daily-constitution-study.py | reports/constitution-study-YYYY-MM-DD.md | 06:00 | 10 分钟 |
| hourly-health-check.py | reports/health-check-YYYYMMDD-HHMM.md | 每小时 | 5 分钟 |
| yijing-daily-study.py | reports/yijing/yijing-YYYY-MM-DD.md | 07:00 | 10 分钟 |
| xianqin-daily-study.py | reports/xianqin/xianqin-YYYY-MM-DD.md | 07:30 | 10 分钟 |
| weather-forecast.py | reports/weather/weather-YYYY-MM-DD.md | 07:00 | 10 分钟 |

### 告警阈值
| 级别 | 条件 | 动作 |
|------|------|------|
| **Low** | 单个文件缺失 | 自动修复 |
| **Medium** | 同一脚本连续 2 次问题 | 记录 + 分析 |
| **High** | 同一脚本连续 3 次问题 | Telegram 告警 |
| **Critical** | 自动修复失败 | 立即告警 + 人工干预 |

---

## 🧠 预测性维护

### 风险评分模型
```python
风险评分 = (
    问题频率 × 0.4 +      # 过去 7 天问题次数
    修复失败率 × 0.3 +    # 修复失败占比
    时间规律性 × 0.2 +    # 是否在固定时间出问题
    影响范围 × 0.1        # 影响的任务数量
)
```

### 风险等级
| 评分 | 等级 | 动作 |
|------|------|------|
| 0-20 | 🟢 低风险 | 正常监控 |
| 21-50 | 🟡 中风险 | 增加检查频率 |
| 51-80 | 🟠 高风险 | 提前干预 |
| 81-100 | 🔴 极高风险 | 立即检查 + 告警 |

---

## 📈 自愈闭环流程

```
1. 检测 (Detect)
   ↓
   每 5 分钟检查文件是否存在
   
2. 修复 (Fix)
   ↓
   自动运行对应脚本重新生成
   
3. 验证 (Verify)
   ↓
   检查文件是否已创建且大小正常
   
4. 学习 (Learn)
   ↓
   记录到 task-quality-log.json
   
5. 预防 (Prevent)
   ↓
   分析趋势，预测潜在问题，提前干预
```

---

## 🔗 相关技能

- `skills/scheduler-agent/` - 定时任务调度
- `scripts/scheduler-monitor.py` - 监控脚本（v3.0）
- `scripts/weekly-quality-report.py` - 周报生成

---

## 📝 更新日志

### v1.0 (2026-04-17)
- ✅ 创建独立技能目录
- ✅ 整合 scheduler-monitor.py 功能
- ✅ 整合 weekly-quality-report.py 功能
- ✅ 新增预测性维护模块
- ✅ 完善自愈闭环流程

---

*太一 AGI · 定时任务质量监控智能体 · 2026-04-17*

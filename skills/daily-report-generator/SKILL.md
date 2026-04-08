---
name: daily-report-generator
version: 1.0.0
description: 自动化生成日报，收集任务完成情况并生成报告
category: auto-generated
tags: ['日报', '报告', '自动化']
author: 太一 AGI (Auto-Generated)
created: 2026-04-09
---

# Daily Report Generator Skill

> 版本：v1.0 | 创建：2026-04-09 | 优先级：P2  
> 来源：从 5+ 次日报生成任务中自动提取

---

## 🎯 职责

自动化生成日报，包括：
- 收集当日任务完成情况
- 汇总 memory/ 目录内容
- 生成标准日报格式
- 写入 reports/ 目录
- 发送结果给 SAYELF

---

## 🔍 触发条件

- 用户提及：日报
- 用户提及：生成报告
- 用户提及：今日总结
- 定时触发：每日 23:00

---

## 🛠️ 执行流程

1. **收集数据**
   - 读取 memory/YYYY-MM-DD.md
   - 读取 HEARTBEAT.md
   - 收集 Git 提交记录

2. **汇总任务**
   - 提取 P0/P1/P2 任务完成情况
   - 统计新增文件
   - 统计 Git 提交

3. **生成报告**
   - 使用日报模板
   - 填充数据
   - 格式化输出

4. **写入文件**
   - 保存到 reports/YYYY-MM-DD-daily.md
   - Git add + commit

5. **发送结果**
   - 通过微信/Telegram 发送
   - 附加关键指标

---

## 📁 相关文件

- `reports/YYYY-MM-DD-daily.md` - 日报文件
- `memory/YYYY-MM-DD.md` - 当日记忆
- `HEARTBEAT.md` - 核心待办

---

## 📋 使用示例

```
# 示例 1: 基础使用
太一，生成今日日报

# 示例 2: 指定日期
太一，生成 2026-04-08 的日报

# 示例 3: 定时触发
每天 23:00 自动生成日报
```

---

## 🔧 配置选项

```json
{
  "daily_report": {
    "enabled": true,
    "schedule": "23:00",
    "timezone": "Asia/Shanghai",
    "auto_send": true
  }
}
```

---

## ✅ 质量检查

- [x] 命名规范检查
- [x] 元数据完整检查
- [x] 触发条件清晰检查
- [x] 步骤可执行检查
- [x] 无硬编码检查
- [x] 有使用示例检查
- [ ] 有错误处理检查

---

## 🚨 错误处理

| 错误 | 处理方式 |
|------|----------|
| memory 文件不存在 | 使用 HEARTBEAT.md 替代 |
| Git 提交失败 | 记录日志，继续执行 |
| 发送失败 | 重试 3 次，记录错误 |

---

*本技能由太一自动生成，经 SAYELF 确认后激活。*

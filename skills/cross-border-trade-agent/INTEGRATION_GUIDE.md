# OpenClaw Gateway 集成指南

> **状态**: 🟡 待手动配置
> **时间**: 2026-05-04

---

## 集成方式

### 方式一：Skill 注册（推荐）

将 `cross-border-trade-agent` 注册为 OpenClaw Skill：

```bash
# 1. 确认 Skill 目录结构
ls /home/sayelf/.openclaw/workspace/skills/cross-border-trade-agent/SKILL.md

# 2. 在 OpenClaw 配置中注册 Skill
# 编辑 ~/.openclaw/config.yaml 或 gateway 配置
```

### 方式二：Cron 任务（已配置）

已配置 8 个定时任务：

| 时间 | 任务 | 脚本 |
|------|------|------|
| 08:00 每日 | 晨间新闻推送 | self_media_engine.py |
| 09:00 工作日 | 周度深度分析 | self_media_engine.py |
| 20:00 每日 | 流量数据汇总 | self_media_engine.py |
| 18:00 周五 | 转化漏斗分析 | self_media_engine.py |
| 22:00 周日 | 自进化报告 | self_evolution_engine.py |
| 10:00 周一 | 品牌健康度报告 | brand_building_engine.py |
| 11:00 周一 | 私域运营报告 | private_traffic_engine.py |
| 03:00 每日 | 数据备份 | backup.py |

### 方式三：Telegram Bot 触发

通过太一主 Agent 委派执行：

```
用户: /委派知几 执行跨境贸易市场分析
太一: 启动 cross-border-trade-agent → 执行分析 → 返回结果
```

---

## 配置检查清单

- [ ] OpenClaw Gateway 配置文件中添加 Skill 路径
- [ ] 确认 Python 依赖包已安装 (`pip install -r requirements.txt`)
- [ ] 配置 API Keys（如需外部数据源）
- [ ] 测试 Telegram Bot 触发响应

---

## 快速测试

```bash
cd /home/sayelf/.openclaw/workspace/skills/cross-border-trade-agent

# 测试主 Agent
python3 cross_border_agent.py

# 测试 GEO 模块
python3 geo_auditor.py

# 测试选品模块
python3 smart_product_selector.py
```

---

*太一 AGI · 集成指南*

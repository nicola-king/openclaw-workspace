# MEMORY.md — 太一长期固化记忆

> 更新时间：2026-05-05

---

## 系统架构

### 工作空间
- 根目录：`/home/sayelf/.openclaw/workspace`
- 记忆层：`memory/core.md` → `memory/context.md` → `memory/evolution.md` → `memory/residual.md`

### 技能体系
- **跨境贸易 Agent v10.0**: `skills/cross-border-trade-agent/` — 穿透式蒸馏版，17模块
- **智能代理调度**: `skills/intelligent-agents/` — 自进化/预测/学习/调度
- **MarkItDown**: `~/.local/venvs/markitdown` — 微软开源文件→Markdown 转换器

### 定时任务
14 个 OpenClaw cron jobs，已完全替代旧 crontab：
- 晨间简报 08:00、GEO 优化 14:00、竞品监控 18:00 → 推送 Telegram
- Git 备份 03:00、自进化 06:00、预测 07:00、学习 12:00 → 静默
- 调度 & 健康检查 → 每小时运行
- 周度报告(周一09:00)、自进化报告(周日22:00)、月度报告(每月1日)

### Obsidian 同步
- Vault: `Taiyiopenclaw` → `太一同步/` 目录下符号链接
- 双向打通：workspace 文件通过 symlink 直接映射进 vault
- 同步检活脚本：`scripts/obsidian-sync-check.sh`

## 活跃项目
1. 跨境贸易 Agent（外贸社媒优化）
2. GEO 优化系统（AI 可见度审计）
3. 量化交易（Polymarket / GMGN）
4. 公众号运营（SAYELF 山野精灵）

## 关键配置
- **公网 IP**: 103.172.182.26
- **GMGN Solana**: `5C1bQnC9wSnVUbzUsXPNQ8eB6VvmYPx6DvQrvvbw9zCq` (余额不足)
- **GMGN Base**: `0x73d6a5835ddf6f54480e28c8fdf399f8ec1b1c79` (余额不足)

## 重要决策记录

| 日期 | 决策 | 类型 |
|------|------|------|
| 2026-05-04 | 蒸馏备份融入 OpenClaw workspace | 能力涌现 |
| 2026-05-05 | 系统 crontab 迁移至 OpenClaw cron（14个任务） | 架构升级 |
| 2026-05-05 | Obsidian 双向打通（symlink 方案） | 知识层打通 |

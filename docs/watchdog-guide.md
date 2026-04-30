# 🛡️ 太一系统 Watchdog 使用指南

> **创建时间**: 2026-04-15 15:32  
> **版本**: v1.0  
> **状态**: ✅ 已部署

---

## ⚠️ 重要说明

**不要写入 `/opt/` 目录** (需要 root 权限)。

**正确位置**:
- `/opt/openclaw-watchdog.sh` (✅ **推荐** - 符号链接)
- `/home/nicola/.openclaw/workspace/scripts/openclaw-watchdog.sh` (源文件)
- `/tmp/openclaw-watchdog.sh` (临时备份)

---

## 🚀 快速使用

### 健康检查
```bash
bash /tmp/openclaw-watchdog.sh check
# 或
bash /home/nicola/.openclaw/workspace/scripts/openclaw-watchdog.sh check
```

### 自动修复
```bash
bash /tmp/openclaw-watchdog.sh heal
```

### 快速状态
```bash
bash /tmp/openclaw-watchdog.sh status
```

---

## 📊 检查项目

| 项目 | 说明 | 权重 |
|------|------|------|
| **Gateway** | OpenClaw Gateway 运行状态 (18789) | 12.5% |
| **Dashboard** | 太一 Dashboard 运行状态 (5001) | 12.5% |
| **磁盘空间** | /home 分区使用率 | 12.5% |
| **GitHub 认证** | gh CLI 登录状态 | 12.5% |
| **记忆系统** | core/context/evolution/residual.md | 12.5% |
| **宪法完整性** | constitution/*.md 文件 | 12.5% |
| **技能系统** | skills/ 分类数量 | 12.5% |
| **冗余进程** | dashboard-auto-manager 进程数 | 12.5% |

---

## 🔧 自愈能力

**自动修复项目**:
- ✅ Gateway 重启 (通过 `openclaw gateway restart`)
- ✅ Dashboard 启动 (通过 dashboard-auto-manager.sh)
- ✅ 冗余进程清理 (保留 1 个，清理多余)

**手动修复项目**:
- ⚠️ GitHub 认证 (需手动 `gh auth login`)
- ⚠️ 记忆文件 (需手动创建)
- ⚠️ 宪法文件 (需手动恢复)

---

## 📈 健康度评分

| 分数 | 等级 | 说明 |
|------|------|------|
| 100% | 🟢 优秀 | 所有系统正常 |
| 90-99% | 🟢 良好 |  minor 问题 |
| 70-89% | 🟡 注意 | 需要关注 |
| <70% | 🔴 警告 | 需要立即处理 |

---

## 📝 日志文件

**日志位置**: `/home/nicola/.openclaw/workspace/logs/watchdog-YYYY-MM-DD.log`

**状态文件**: `/tmp/openclaw-watchdog-state.json`

---

## ⏰ 定时任务 (可选)

### 添加到 crontab
```bash
crontab -e
```

**每小时检查**:
```
0 * * * * bash /home/nicola/.openclaw/workspace/scripts/openclaw-watchdog.sh check >> /home/nicola/.openclaw/workspace/logs/watchdog-cron.log 2>&1
```

**每日自检 (06:00)**:
```
0 6 * * * bash /home/nicola/.openclaw/workspace/scripts/openclaw-watchdog.sh heal >> /home/nicola/.openclaw/workspace/logs/watchdog-cron.log 2>&1
```

---

## 🔗 相关脚本

| 脚本 | 功能 | 位置 |
|------|------|------|
| **watchdog** | 系统自检自愈 | `scripts/openclaw-watchdog.sh` |
| **dashboard-auto-manager** | Dashboard 自动管理 | `scripts/dashboard-auto-manager.sh` |
| **openclaw** | Gateway 管理 | CLI 命令 |

---

## 💡 使用示例

### 示例 1: 快速查看状态
```bash
$ bash /tmp/openclaw-watchdog.sh status

==========================================
       太一系统自检报告
==========================================

Gateway:        ✅ 运行中 (18789)
Dashboard:      ✅ 运行中 (5001)
磁盘空间：      5%
GitHub 认证：   ✅ 已登录
记忆文件：      208 个
技能分类：      48 个
宪法文件：      13 个
Dashboard 进程： 1 个

==========================================
```

### 示例 2: 完整健康检查
```bash
$ bash /tmp/openclaw-watchdog.sh check

[2026-04-15 15:32:00] 🛡️  太一系统自检开始...
[2026-04-15 15:32:00] 检查 Gateway 状态...
[2026-04-15 15:32:00] ✅ Gateway 运行正常 (18789)
...
[2026-04-15 15:32:00] 🏥 系统健康度：100%
[2026-04-15 15:32:00] 得分：8 / 8
```

### 示例 3: 自动修复
```bash
$ bash /tmp/openclaw-watchdog.sh heal

[2026-04-15 15:32:00] 🔧 太一系统自愈开始...
[2026-04-15 15:32:00] 检查 Gateway 状态...
[2026-04-15 15:32:00] 🔧 尝试修复 Gateway...
...
[2026-04-15 15:32:30] ✅ 自动修复完成
[2026-04-15 15:32:30] 🏥 系统健康度：100%
```

---

## ⚠️ 注意事项

1. **权限**: 脚本需要普通用户权限，无需 sudo
2. **依赖**: 需要 `curl`, `gh`, `openclaw` CLI 已安装
3. **日志**: 每日自动生成新日志文件
4. **状态**: 状态文件保存在 `/tmp/` (重启后清除)

---

## 🐛 故障排除

### Gateway 无法启动
```bash
openclaw gateway status
openclaw gateway restart
tail -f /tmp/openclaw/openclaw-*.log
```

### Dashboard 无法启动
```bash
bash /home/nicola/.openclaw/workspace/scripts/dashboard-auto-manager.sh status
tail -f /home/nicola/.openclaw/workspace/logs/dashboard-auto-manager.log
```

### GitHub 认证失效
```bash
gh auth logout
gh auth login
```

---

*太一 Watchdog v1.0 · 太一 AGI · 2026-04-15*

**🛡️ 系统自检，自动守护！**

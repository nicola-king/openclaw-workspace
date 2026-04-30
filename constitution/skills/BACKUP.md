---
name: backup
tier: 2
trigger: 备份/恢复/数据/安全
enabled: true
depends: []
---
# 数据备份与恢复技能

## 核心原则

**负熵法则：** 防止数据丢失导致的混乱

**价值基石：** 保护 SAYELF 的数据安全

**简化优先：** 极简备份策略，避免过度复杂

---

## 备份范围

### 核心数据（必须备份）

| 数据类型 | 路径 | 频率 | 保留 |
|----------|------|------|------|
| 宪法文件 | `constitution/` | 每次变更 | 永久 |
| 记忆文件 | `memory/` | 每日 | 永久 |
| 配置文件 | `*.md` (根目录) | 每次变更 | 永久 |
| 会话记录 | `sessions/` | 每周 | 30 天 |

### 可选数据（按需备份）

| 数据类型 | 路径 | 频率 | 保留 |
|----------|------|------|------|
| 技能文件 | `~/.npm-global/skills/` | 每周 | 最新 |
| 日志文件 | `logs/` | 每日 | 7 天 |
| 媒体文件 | `media/` | 每周 | 30 天 |

---

## 备份策略

### 本地备份（即时）

```bash
# 备份到本地备份目录
BACKUP_DIR="/home/nicola/.openclaw/backup"
WORKSPACE="/home/nicola/.openclaw/workspace"

# 创建带时间戳的备份
tar -czf "$BACKUP_DIR/workspace-$(date +%Y%m%d-%H%M).tar.gz" \
  --exclude='node_modules' \
  --exclude='.git' \
  "$WORKSPACE"
```

### 远程备份（可选）

```bash
# 备份到云存储（如 rclone 配置）
rclone copy "$BACKUP_DIR" remote:openclaw-backup/ \
  --backup-dir remote:openclaw-backup/archive/$(date +%Y%m%d)
```

---

## 恢复流程

### 单文件恢复

```bash
# 从备份中提取单个文件
tar -xzf workspace-20260322-0200.tar.gz \
  home/nicola/.openclaw/workspace/memory/2026-03-22.md \
  --strip-components=4
```

### 完整恢复

```bash
# 恢复到新目录
mkdir -p /tmp/openclaw-restore
tar -xzf workspace-20260322-0200.tar.gz -C /tmp/openclaw-restore
```

---

## 自动化备份

### 每日备份（23:00）

**触发：** Session 结束协议执行时

**动作：**
1. 压缩当日 memory 文件
2. 备份宪法文件（如有变更）
3. 写入备份日志

### 每周备份（周日 00:00）

**动作：**
1. 完整 workspace 备份
2. 清理 30 天前备份
3. 远程同步（如配置）

---

## 备份验证

### 月度恢复测试

**每月初执行：**
1. 随机选择一个备份文件
2. 恢复到临时目录
3. 验证文件完整性
4. 写入验证报告

### 验证清单

- [ ] 备份文件可解压
- [ ] 核心文件完整
- [ ] 无数据损坏
- [ ] 恢复时间可接受

---

## 安全注意事项

### 备份加密（可选）

```bash
# 使用 GPG 加密备份
gpg --symmetric --cipher-algo AES256 \
  workspace-20260322-0200.tar.gz
```

### 访问控制

- 备份目录权限：`chmod 700`
- 仅 SAYELF 和太一可访问
- 远程备份使用独立凭证

---

## 快速参考

### 手动备份

```bash
# 立即备份
bash /opt/openclaw-backup.sh

# 查看备份列表
ls -lh /home/nicola/.openclaw/backup/

# 恢复最新备份
bash /opt/openclaw-restore.sh latest
```

### 备份状态检查

```bash
# 检查备份是否最新
ls -lt /home/nicola/.openclaw/backup/ | head -5

# 检查备份大小
du -sh /home/nicola/.openclaw/backup/
```

---

## 与现有技能集成

### Session 结束协议

**集成点：** 23:00 夜间压缩时自动触发备份

**流程：**
```
Session 结束 → 写入 memory → 触发备份 → 验证完成
```

### HEARTBEAT 检查

**集成点：** 每周日检查备份状态

**检查项：**
- [ ] 本周备份已完成
- [ ] 备份大小正常
- [ ] 远程同步成功（如配置）

---

## 故障处理

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 备份失败 | 磁盘空间不足 | 清理旧备份/扩容 |
| 恢复失败 | 备份文件损坏 | 使用更早备份 |
| 加密失败 | GPG 未安装 | `apt install gpg` |

### 紧急恢复

**场景：** 系统故障，需快速恢复

**流程：**
1. 定位最新可用备份
2. 恢复到临时目录
3. 验证核心文件
4. 逐步替换损坏文件

---

## 备份日志模板

```markdown
【备份记录 · YYYY-MM-DD HH:mm】
- 类型：每日/每周/手动
- 备份文件：workspace-YYYYMMDD-HHMM.tar.gz
- 大小：XX MB
- 核心文件：constitution/ memory/ *.md
- 验证：✅ 通过 / ❌ 失败
- 备注：[如有问题]
```

---
*版本：1.0 | 生效日期：2026-03-22 | 最后更新：08:00*

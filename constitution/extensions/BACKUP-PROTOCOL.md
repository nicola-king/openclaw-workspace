# BACKUP-PROTOCOL.md - 备份协议

> 统一备份标准 | 版本：v1.0 | 创建：2026-03-26 | 太一 AGI

---

## 🎯 核心原则

```
自动备份 · 统一目录 · 可恢复 · 30 天保留
```

---

## 📁 备份目录结构

```
/opt/backup/
├── 20260326-233500/          # 时间戳命名
│   ├── syncthing/            # 软件配置
│   │   ├── config.xml
│   │   └── config.xml.v51.backup
│   ├── tailscale/
│   │   └── state.json
│   └── openclaw/
│       └── config.json
├── 20260325-080000/
└── ...
```

---

## 🔧 备份标准

### 命名规范

```
格式：YYYYMMDD-HHMMSS

示例:
20260326-233500  → 2026 年 3 月 26 日 23:35:00
20260325-080000  → 2026 年 3 月 25 日 08:00:00
```

### 备份内容

| 类型 | 路径 | 说明 |
|------|------|------|
| **软件配置** | `~/.config/<app>/` | 用户配置 |
| **系统配置** | `/etc/<app>/` | 系统配置 |
| **数据目录** | `/var/lib/<app>/` | 应用数据 |
| **服务文件** | `/etc/systemd/system/<app>.service` | systemd 配置 |
| **用户服务** | `~/.config/systemd/user/<app>.service` | 用户服务 |

---

## 📋 备份流程

### 安装前备份

```bash
#!/bin/bash
PACKAGE=$1
BACKUP_DIR="/opt/backup/$(date +%Y%m%d-%H%M%S)"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份配置
cp -r ~/.config/$PACKAGE "$BACKUP_DIR/" 2>/dev/null
cp -r /etc/$PACKAGE "$BACKUP_DIR/" 2>/dev/null
cp -r /var/lib/$PACKAGE "$BACKUP_DIR/" 2>/dev/null

# 备份服务
cp /etc/systemd/system/$PACKAGE.service "$BACKUP_DIR/" 2>/dev/null
cp ~/.config/systemd/user/$PACKAGE.service "$BACKUP_DIR/" 2>/dev/null

echo "备份完成：$BACKUP_DIR"
```

### 定期备份

```bash
# 每天 02:00 备份关键配置
0 2 * * * /home/nicola/.openclaw/workspace/skills/suwen/backup-daily.sh
```

---

## 🔄 恢复流程

### 完全恢复

```bash
BACKUP_DIR="/opt/backup/20260326-233500"
PACKAGE="syncthing"

# 停止服务
systemctl stop $PACKAGE
systemctl --user stop $PACKAGE

# 恢复配置
cp -r "$BACKUP_DIR/$PACKAGE/" ~/.config/ 2>/dev/null
cp -r "$BACKUP_DIR/$PACKAGE/" /etc/ 2>/dev/null

# 恢复服务
cp "$BACKUP_DIR/$PACKAGE.service" /etc/systemd/system/ 2>/dev/null
systemctl daemon-reload

# 启动服务
systemctl start $PACKAGE
systemctl --user start $PACKAGE
```

### 部分恢复

```bash
# 仅恢复配置文件
cp /opt/backup/20260326-233500/syncthing/config.xml ~/.config/syncthing/

# 重启服务
systemctl --user restart syncthing
```

---

## 📊 保留策略

| 备份类型 | 保留期 | 清理规则 |
|---------|--------|---------|
| **安装备份** | 30 天 | 自动删除>30 天 |
| **每日备份** | 7 天 | 保留最近 7 份 |
| **每周备份** | 4 周 | 保留最近 4 份 |
| **每月备份** | 12 月 | 保留最近 12 份 |

### 自动清理

```bash
#!/bin/bash
# 删除 30 天前的备份
find /opt/backup -type d -mtime +30 -exec rm -rf {} \;

# 保留最近 N 份备份
ls -dt /opt/backup/* | tail -n +8 | xargs rm -rf
```

---

## 🧪 验证机制

### 备份验证

```bash
# 检查备份完整性
BACKUP_DIR="/opt/backup/20260326-233500"

if [ -d "$BACKUP_DIR" ]; then
    echo "✅ 备份目录存在"
    
    # 检查关键文件
    if [ -f "$BACKUP_DIR/syncthing/config.xml" ]; then
        echo "✅ 配置文件存在"
    else
        echo "❌ 配置文件缺失"
    fi
else
    echo "❌ 备份目录不存在"
fi
```

### 恢复测试

```bash
# 每月执行一次恢复测试
# 1. 创建测试环境
# 2. 恢复备份
# 3. 验证服务
# 4. 清理测试环境
```

---

## 📞 自动化脚本

### backup-daily.sh

```bash
#!/bin/bash
# 每日备份脚本

BACKUP_DIR="/opt/backup/$(date +%Y%m%d-020000)"
mkdir -p "$BACKUP_DIR"

# 备份关键配置
cp -r ~/.config/syncthing "$BACKUP_DIR/" 2>/dev/null
cp -r ~/.config/tailscale "$BACKUP_DIR/" 2>/dev/null
cp -r ~/.openclaw/openclaw.json "$BACKUP_DIR/" 2>/dev/null

# 清理旧备份
find /opt/backup -type d -mtime +30 -exec rm -rf {} \;

echo "每日备份完成：$BACKUP_DIR"
```

---

*版本：v1.0 | 创建时间：2026-03-26 | 太一 AGI*

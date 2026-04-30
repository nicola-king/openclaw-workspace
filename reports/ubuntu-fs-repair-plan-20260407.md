# Ubuntu 文件系统修复方案

**诊断时间**: 2026-04-07 16:10  
**问题**: ext4 文件系统只读错误，导致 snapd 无法启动，系统无法进入 UI

---

## 🔍 问题诊断

### 核心错误

```
snapd[2404]: cannot run daemon: fatal: error opening lock file: 
open /var/lib/snapd/state.lock: read-only file system
```

### 症状

| 组件 | 状态 | 错误 |
|------|------|------|
| **snapd.service** | ❌ 失败 | 无法写入 state.lock |
| **rsyslogd** | ❌ 失败 | 无法写入 /var/log/*.log |
| **cupsd** | ❌ 失败 | 无法写入 /var/log/cups/ |
| **系统日志** | ❌ 失败 | Read-only file system |

### 根本原因

**ext4 文件系统检测到错误，内核自动重新挂载为只读模式**

这是 Linux 的保护机制：当文件系统检测到不一致时，防止进一步损坏。

---

## 🛠️ 修复方案

### 方案 A: 强制 fsck 修复（推荐）

**步骤**:

1. **创建 fsck 强制检查标志**:
```bash
sudo touch /forcefsck
```

2. **重启系统**:
```bash
sudo reboot
```

3. **系统启动时会自动**:
   - 检测到 `/forcefsck` 文件
   - 在挂载根文件系统前运行 `fsck`
   - 修复文件系统错误
   - 自动删除 `/forcefsck`
   - 正常启动

**预计时间**: 5-15 分钟（取决于磁盘大小和错误程度）

---

### 方案 B: 使用 live USB 修复（如方案 A 失败）

**步骤**:

1. 创建 Ubuntu Live USB
2. 从 USB 启动
3. 打开终端，运行:
```bash
# 检查但不修复
sudo fsck -n /dev/nvme0n1p1

# 修复错误
sudo fsck -y /dev/nvme0n1p1
```

4. 重启进入系统

---

### 方案 C: GRUB 强制 fsck（备选）

**步骤**:

1. 重启，在 GRUB 菜单按 `e` 编辑启动项
2. 找到 `ro quiet splash` 行
3. 修改为: `rw fsck.mode=force fsck.fix=yes`
4. 按 `Ctrl+X` 或 `F10` 启动
5. 系统会强制运行 fsck

---

## ⚠️ 注意事项

### 风险提示

- **数据丢失风险**: fsck 可能删除损坏的文件
- **时间成本**: 大磁盘可能需要较长时间
- **不要中断**: fsck 过程中断电可能导致更严重损坏

### 备份建议

如果系统还能部分访问，先备份重要数据:

```bash
# 备份 OpenClaw 工作区
tar -czf /tmp/openclaw-backup.tar.gz ~/.openclaw/workspace

# 备份到其他位置
cp /tmp/openclaw-backup.tar.gz /mnt/external-drive/
```

---

## 📋 执行后验证

系统重启后，检查：

```bash
# 1. 检查 snapd 状态
systemctl status snapd.service

# 2. 测试写入
sudo touch /var/lib/snapd/test.lock && echo "✅ 写入正常" || echo "❌ 仍然只读"

# 3. 检查文件系统
mount | grep "on / "

# 4. 查看系统日志
journalctl -xb -p 3 | tail -20
```

---

## 🔧 预防措施

### 避免再次发生

1. **定期 fsck 检查**:
```bash
# 检查下次挂载时的 fsck 间隔
sudo tune2fs -l /dev/nvme0n1p1 | grep -i "check interval"
```

2. **监控磁盘健康**:
```bash
# 安装 smartmontools
sudo apt install smartmontools

# 检查磁盘健康
sudo smartctl -a /dev/nvme0n1
```

3. **避免强制关机**:
   - 使用 `sudo reboot` 或 `sudo shutdown`
   - 避免直接断电

4. **定期检查系统日志**:
```bash
# 查看文件系统错误
journalctl -xb | grep -i "ext4\|error"
```

---

## 📊 当前系统状态

| 项目 | 状态 |
|------|------|
| **根文件系统** | /dev/nvme0n1p1 (ext4) |
| **挂载状态** | rw (但实际只读) |
| **snapd** | failed (exit-code) |
| **错误日志** | 多个服务报告 Read-only file system |
| **修复方案** | 强制 fsck |

---

## 🎯 建议操作

**立即执行**:

```bash
# 1. 创建 fsck 标志
sudo touch /forcefsck

# 2. 验证文件创建
ls -la /forcefsck

# 3. 重启系统
sudo reboot
```

**重启后验证**:

```bash
# 检查 snapd 是否恢复
systemctl is-active snapd.service

# 检查写入是否正常
touch /var/lib/snapd/test.lock && echo "✅ 修复成功"
```

---

**报告生成**: 太一 AGI  
**时间**: 2026-04-07 16:10  
**状态**: 待执行

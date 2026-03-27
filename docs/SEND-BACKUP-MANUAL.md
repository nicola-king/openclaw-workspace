# 📧 太一备份邮件 - 手动发送指南

> 创建时间：2026-03-27 00:10 | 太一 AGI

---

## 📦 备份文件已就绪

| 文件 | 大小 | 位置 |
|------|------|------|
| **完整系统备份** | 542K | `/opt/taiyi-backup/taiyi-backup-20260327-000824.tar.gz` |
| **简单打包** | 2.3M | `/home/nicola/taiyi-simple-backup-20260327-000801.tar.gz` |

---

## ✉️ 发送步骤（3 分钟）

### 步骤 1: 打开 QQ 邮箱

```
https://mail.qq.com
```

### 步骤 2: 写信

| 字段 | 内容 |
|------|------|
| **收件人** | `285915125@qq.com` |
| **主题** | `太一宪法备份 - 20260327` |

### 步骤 3: 复制正文

```
太一宪法备份

序列号：TY-CONSTITUTION-20260327-000824
创建时间：2026-03-27 00:08:24
版本：v1.0.0

备份内容:
- 宪法文档 (constitution/)
- 记忆体系 (memory/)
- 核心文件 (MEMORY.md, HEARTBEAT.md, SOUL.md, ...)
- 技能目录 (skills/)
- 脚本目录 (scripts/)

恢复指南:
  tar -xzf taiyi-backup-20260327-000824.tar.gz
  cd 20260327-000824
  bash restore.sh

请妥善保存此备份文件，用于系统恢复。

--
太一 AGI 自动备份系统
```

### 步骤 4: 添加附件

1. 点击「添加附件」
2. 选择文件：
   - `/opt/taiyi-backup/taiyi-backup-20260327-000824.tar.gz`
   - `/home/nicola/taiyi-simple-backup-20260327-000801.tar.gz`

**或复制文件到桌面**:
```bash
cp /opt/taiyi-backup/taiyi-backup-20260327-000824.tar.gz ~/Desktop/
cp /home/nicola/taiyi-simple-backup-20260327-000801.tar.gz ~/Desktop/
```

### 步骤 5: 发送

点击「发送」按钮

---

## ✅ 验证

发送后检查：
- [ ] 已发送信箱有记录
- [ ] 收件箱收到邮件
- [ ] 附件可以下载

---

## 🔐 自动发送配置（可选）

如需自动发送，配置 QQ 邮箱授权码：

1. 登录 QQ 邮箱
2. 设置 → 账户
3. 开启 POP3/SMTP 服务
4. 生成授权码
5. 运行：
```bash
python3 /home/nicola/.openclaw/workspace/scripts/send-backup-quick.py
# 输入授权码（不是 QQ 密码）
```

---

*太一 AGI · 2026-03-27 00:10*

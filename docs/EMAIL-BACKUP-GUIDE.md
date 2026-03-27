# 太一备份邮件发送指南

> 版本：v1.0 | 创建：2026-03-27 00:08

---

## ✅ 已完成备份

### 简单打包

| 项目 | 值 |
|------|-----|
| **文件** | `~/taiyi-simple-backup-20260327-000801.tar.gz` |
| **大小** | 2.3M |
| **内容** | 完整工作区 |

### 完整系统备份

| 项目 | 值 |
|------|-----|
| **序列号** | TY-CONSTITUTION-20260327-000824 |
| **文件** | `/opt/taiyi-backup/taiyi-backup-20260327-000824.tar.gz` |
| **大小** | 544K |
| **SHA256** | `51c4a61ff601ff59fe771e6941813d21ec521075c2d74ee18c79a7955cadece8` |

---

## 📧 邮件发送方法

### 方法 1: 手动发送 (推荐)

**步骤**:
1. 打开邮箱客户端 (QQ 邮箱/Outlook 等)
2. 新建邮件
3. 收件人：`285915125@qq.com`
4. 主题：`太一宪法备份 - 20260327`
5. 附件：
   - `/opt/taiyi-backup/taiyi-backup-20260327-000824.tar.gz` (完整系统)
   - `/home/nicola/taiyi-simple-backup-20260327-000801.tar.gz` (简单打包)
6. 发送

**邮件正文**:
```
太一宪法备份

序列号：TY-CONSTITUTION-20260327-000824
创建时间：2026-03-27 00:08:24
版本：v1.0.0

备份内容:
- 宪法文档 (constitution/)
- 记忆体系 (memory/)
- 核心文件 (MEMORY.md, HEARTBEAT.md, ...)
- 技能目录 (skills/)
- 脚本目录 (scripts/)

恢复指南:
  tar -xzf taiyi-backup-20260327-000824.tar.gz
  cd 20260327-000824
  bash restore.sh

请妥善保存！
```

---

### 方法 2: 配置 mutt 自动发送

**步骤 1: 获取 QQ 邮箱授权码**

1. 登录 QQ 邮箱
2. 设置 → 账户
3. 开启 POP3/SMTP 服务
4. 生成授权码 (不是 QQ 密码)

**步骤 2: 配置 mutt**

```bash
# 创建配置文件
cat >> ~/.muttrc << EOF
set from = "285915125@qq.com"
set realname = "太一 AGI"
set imap_user = "285915125@qq.com"
set imap_pass = "授权码"
set smtp_user = "285915125@qq.com"
set smtp_pass = "授权码"
set folder = "imaps://imap.qq.com/"
set spoolfile = "+INBOX"
set mailbox_type = "mbox"
EOF

# 替换授权码
sed -i 's/授权码/YOUR_AUTH_CODE/' ~/.muttrc
```

**步骤 3: 发送**

```bash
bash /home/nicola/.openclaw/workspace/scripts/email-constitution.sh
```

---

### 方法 3: 使用 Python 发送

```python
#!/usr/bin/env python3
# send_backup.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def send_backup(backup_file, to_email, from_email, password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = f"太一宪法备份 - {os.path.basename(backup_file)}"
    
    body = """
    太一宪法备份
    
    请妥善保存此备份文件，用于系统恢复。
    
    恢复指南:
      tar -xzf backup.tar.gz
      cd <timestamp>
      bash restore.sh
    
    --
    太一 AGI
    """
    msg.attach(MIMEBase(body, 'plain'))
    
    # 附加文件
    with open(backup_file, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(backup_file)}')
        msg.attach(part)
    
    # 发送
    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login(from_email, password)
    server.send_message(msg)
    server.quit()
    
    print(f"✅ 邮件已发送到 {to_email}")

# 使用示例
# send_backup('/opt/taiyi-backup/taiyi-backup-20260327-000824.tar.gz', 
#             '285915125@qq.com', 
#             '285915125@qq.com', 
#             'YOUR_AUTH_CODE')
```

---

## ✅ 验证清单

- [x] 简单打包完成 (2.3M)
- [x] 完整系统备份完成 (544K)
- [ ] 邮件发送 (手动/自动)
- [ ] 收到确认
- [ ] 备份验证

---

*创建时间：2026-03-27 00:08 | 太一 AGI*

# 太一记忆体备份机制

> 创建：2026-03-28 23:09
> 执行时间：每周日 24:00
> 接收邮箱：285915125@qq.com

---

## 🎯 备份目的

**场景**:
- OpenClaw 重新安装
- 升级失败
- 系统损坏
- 意外删除

**目标**: 使用该文件夹恢复到备份时的状态

---

## 📦 备份内容

### 1. 宪法文件
- `constitution/` - 全部宪法文件

### 2. 记忆文件
- `memory/` - 核心记忆 + 残差记忆 + 每日日志
- `MEMORY.md` - 长期固化记忆

### 3. 核心配置
- `AGENTS.md` - 工作区配置
- `SOUL.md` - 身份锚点
- `USER.md` - 用户信息
- `TOOLS.md` - 工具配置
- `HEARTBEAT.md` - 核心待办

### 4. Skills (太一核心)
- `skills/taiyi/` - 太一 Skill (含三大智能自动化)
- `skills/zhiji/` - 知几 Bot
- `skills/shanmu/` - 山木 Bot
- `skills/suwen/` - 素问 Bot
- `skills/shoucangli/` - 守藏吏 Bot
- `skills/paoding/` - 庖丁 Bot

### 5. 架构文档
- `TAIYI-ARCHITECTURE.md`
- `EIGHT-BOTS-STATUS.md`
- `SMART-AUTOMATION-ARCHITECTURE.md`
- `TAIYI-MISTAKES-AND-IMPROVEMENTS.md`

### 6. 环境变量配置
- `env_config.txt` - 脱敏后的环境变量

---

## ⏰ 定时任务

### 执行时间
**每周日 24:00** (周一 0:00)

### Cron 配置
```bash
# 编辑 crontab
crontab -e

# 添加定时任务
0 0 * * 0 /home/nicola/.openclaw/workspace/scripts/taiyi-backup.sh
```

---

## 📧 邮件发送

**接收邮箱**: 285915125@qq.com

**邮件内容**:
- 主题：太一记忆体备份 - YYYYMMDD
- 附件：taiyi-backup-YYYYMMDD_HHMMSS.tar.gz

---

## 🔄 恢复步骤

### Step 1: 重新安装 OpenClaw

```bash
npm install -g openclaw
```

### Step 2: 停止 Gateway

```bash
openclaw gateway stop
```

### Step 3: 恢复文件

```bash
# 解压备份文件
tar -xzf taiyi-backup-*.tar.gz

# 复制文件到 workspace
cp -r * /home/nicola/.openclaw/workspace/
```

### Step 4: 恢复环境变量

```bash
# 查看 env_config.txt
cat env_config.txt

# 手动添加到 ~/.bashrc
nano ~/.bashrc

# 应用配置
source ~/.bashrc
```

### Step 5: 启动 Gateway

```bash
openclaw gateway start
```

### Step 6: 验证恢复

```bash
openclaw status
```

---

## ⚠️ 注意事项

### 敏感信息
- API Key 已脱敏处理
- 需手动重新配置敏感信息

### 环境变量
- `env_config.txt` 仅包含配置名，不含具体值
- 需手动从安全来源获取 API Key

### Git 仓库
- 如使用 Git 管理，需单独备份 `.git` 目录
- 或使用 `git push` 同步到远程仓库

---

## 📊 备份管理

### 保留策略
- 保留最近 **4 次** 备份
- 自动删除旧备份

### 备份大小
- 预计：5-10MB
- 压缩格式：tar.gz

### 备份位置
- 临时：`/tmp/taiyi-backup-*.tar.gz`
- 最终：邮件附件

---

## 🚀 手动备份

```bash
# 立即执行备份
/home/nicola/.openclaw/workspace/scripts/taiyi-backup.sh

# 或
cd /home/nicola/.openclaw/workspace/scripts
bash taiyi-backup.sh
```

---

## 📋 检查清单

### 备份前
- [ ] 检查磁盘空间
- [ ] 检查邮件工具
- [ ] 检查网络连接

### 备份后
- [ ] 验证备份文件大小
- [ ] 确认邮件发送成功
- [ ] 检查备份内容完整性

---

## 🔧 故障排查

### 问题 1: 邮件发送失败

**原因**: 未安装 mail 工具

**解决**:
```bash
# Ubuntu/Debian
sudo apt-get install mailutils

# CentOS/RHEL
sudo yum install mailx
```

### 问题 2: 备份文件过大

**原因**: 包含过多文件

**解决**:
- 检查备份脚本排除列表
- 手动清理无用文件

### 问题 3: 恢复后配置不生效

**原因**: 环境变量未恢复

**解决**:
- 手动配置 API Key
- 重新 source ~/.bashrc

---

*创建时间：2026-03-28 23:09*
*太一 AGI · 记忆体备份机制*

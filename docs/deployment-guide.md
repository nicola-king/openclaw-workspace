# OpenClaw 部署指南

> 3 种部署方案，适合不同用户群体  
> 版本：v1.0  
> 状态：🟡 规划中

---

## 🎯 目标

提供 3 种部署方案，满足不同用户需求。

---

## 📋 方案对比

| 方案 | 成本 | 复杂度 | 适用人群 | 状态 |
|------|------|--------|---------|------|
| **托管服务** | ¥100/月 | ⭐ | 非技术用户 | 🟡 规划中 |
| **VPS** | ¥50/月 | ⭐⭐⭐ | 技术用户 | ✅ 可用 |
| **自有设备** | ~¥4000 | ⭐⭐ | 深度体验 | ✅ 可用 |

---

## 方案 A：托管服务（StartClaw/MyClaw）

**适合人群**：非技术用户，不想折腾部署

**成本**：
- 基础版：¥100/月
- 专业版：¥200/月
- 企业版：¥500/月

**包含服务**：
- ✅ 预装 OpenClaw
- ✅ 自动更新
- ✅ 技术支持
- ✅ 备份恢复
- ✅ 监控告警

**部署流程**：
1. 注册账号
2. 选择套餐
3. 配置微信/飞书凭证
4. 导入身份文件（SOUL.md/AGENTS.md）
5. 启动服务

**优点**：
- 零部署成本
- 专业维护
- SLA 保障

**缺点**：
- 月费较高
- 数据在第三方
- 定制能力有限

**状态**：🟡 规划中（预计 2026-05 上线）

---

## 方案 B：VPS 部署

**适合人群**：技术用户，有 Linux 经验

**成本**：
- 阿里云：¥50/月（2 核 4G）
- 腾讯云：¥50/月（2 核 4G）
- 华为云：¥60/月（2 核 4G）

**系统要求**：
- Ubuntu 22.04+ / Debian 11+
- 2 核 CPU
- 4GB 内存
- 50GB 存储
- 公网 IP

**部署流程**：

```bash
# 1. 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# 2. 安装 OpenClaw
npm install -g openclaw

# 3. 配置环境变量
export OPENCLAW_WEIXIN_TOKEN=xxx
export OPENCLAW_FEISHU_APP_ID=xxx
export OPENCLAW_FEISHU_APP_SECRET=xxx

# 4. 启动 Gateway
openclaw gateway start

# 5. 验证状态
openclaw gateway status
```

**定时任务配置**：
```bash
# 编辑 Crontab
crontab -e

# 添加任务
0 6 * * * /usr/local/bin/openclaw memory extract --daily
0 23 * * * /usr/local/bin/openclaw report daily
*/5 * * * * /usr/local/bin/openclaw tasks check
```

**安全配置**：
```bash
# 1. 配置防火墙
sudo ufw allow 22/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# 2. 配置 SSH 密钥
ssh-keygen -t ed25519
sudo mkdir -p /root/.ssh
sudo cp ~/.ssh/id_ed25519.pub /root/.ssh/authorized_keys

# 3. 禁用密码登录
sudo vim /etc/ssh/sshd_config
# PasswordAuthentication no
```

**优点**：
- 成本最低
- 完全控制
- 数据自主

**缺点**：
- 需要技术能力
- 自行维护
- 无 SLA 保障

**状态**：✅ 可用（文档完善中）

---

## 方案 C：自有设备

**适合人群**：深度体验/学习/隐私敏感用户

**设备推荐**：

| 设备 | 成本 | 性能 | 功耗 | 推荐度 |
|------|------|------|------|--------|
| **Mac Mini M1** | ~¥4000 | ⭐⭐⭐⭐ | 低 | ⭐⭐⭐⭐⭐ |
| **旧笔记本** | ~¥0 | ⭐⭐⭐ | 中 | ⭐⭐⭐⭐ |
| **树莓派 5** | ~¥600 | ⭐⭐ | 极低 | ⭐⭐⭐ |
| **N100 小主机** | ~¥1000 | ⭐⭐⭐ | 低 | ⭐⭐⭐⭐ |

**部署流程**（以 Mac Mini 为例）：

```bash
# 1. 安装 Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. 安装 Node.js
brew install node@22

# 3. 安装 OpenClaw
npm install -g openclaw

# 4. 配置环境变量
echo 'export OPENCLAW_WEIXIN_TOKEN=xxx' >> ~/.zshrc
source ~/.zshrc

# 5. 启动 Gateway
openclaw gateway start
```

**优点**：
- 数据完全本地
- 一次性投入
- 学习价值高

**缺点**：
- 前期成本高
- 需要硬件知识
- 自行维护

**状态**：✅ 可用（文档完善中）

---

## ⚠️ 安全警告

**绝不要安装在日常工作/个人电脑上！**

**原因**：
1. **权限风险**：AI 需要较高权限运行
2. **数据泄露**：可能访问本地文件
3. **性能影响**：持续运行影响日常工作
4. **安全边界**：工作/个人数据应隔离

**推荐做法**：
- 使用专用设备
- 或使用虚拟机隔离
- 或使用 Docker 容器

---

## 📋 执行清单

- [ ] 方案 A：托管服务（2026-05 上线）
- [ ] 方案 B：VPS 部署文档完善
- [ ] 方案 C：自有设备文档完善
- [ ] 安全审计脚本开发
- [ ] 一键部署脚本开发

---

## 🔗 参考资源

- OpenClaw 文档：https://docs.openclaw.ai
- GitHub: https://github.com/nicola-king/openclaw-workspace
- Discord: https://discord.gg/clawd

---

*版本：v1.0 | 创建时间：2026-04-02 | 状态：规划中*

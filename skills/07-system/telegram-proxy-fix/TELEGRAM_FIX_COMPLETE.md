# Telegram 问题完整修复方案

> **创建时间**: 2026-04-20 22:48  
> **状态**: ⚠️  需要人工干预  
> **问题等级**: P0 (核心功能)

---

## 🔍 问题诊断

### 症状
Telegram 消息发送失败，无响应

### 日志错误
```
Network request for 'sendMessage' failed!
Network request for 'deleteMyCommands' failed!
Network request for 'deleteWebhook' failed!
Network request for 'setMyCommands' failed!
```

### 根因分析

| 检查项 | 状态 | 说明 |
|--------|------|------|
| Telegram Bot Token | ✅ 已配置 | `8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY` |
| 环境变量 | ✅ 已配置 | `HTTPS_PROXY=http://127.0.0.1:7890` |
| systemd service | ✅ 已配置 | 包含代理环境变量 |
| **代理服务** | ❌ **未运行** | 端口 7890 未监听 |

**结论**: Gateway 配置正确，但**代理服务器 (Clash) 未运行**，导致 Telegram API 请求失败。

---

## 🛠️ 解决方案

### 方案 A: 安装并运行 Clash Meta (推荐)

**步骤**:

```bash
# 1. 下载 Clash Meta (Mihomo)
cd /tmp
wget https://github.com/MetaCubeX/mihomo/releases/download/v1.18.0/mihomo-linux-amd64-v1.18.0.gz

# 2. 解压并安装
gunzip mihomo-linux-amd64-v1.18.0.gz
chmod +x mihomo-linux-amd64-v1.18.0
sudo mv mihomo-linux-amd64-v1.18.0 /usr/local/bin/clash

# 3. 验证安装
clash --version

# 4. 创建配置目录
mkdir -p ~/.config/clash

# 5. 创建基础配置
cat > ~/.config/clash/config.yaml << 'EOF'
mixed-port: 7890
allow-lan: false
mode: rule
log-level: info
external-controller: 127.0.0.1:9090

proxies:
  # TODO: 添加你的代理服务器配置
  # 示例:
  # - name: "My Proxy"
  #   type: vmess
  #   server: proxy.example.com
  #   port: 443
  #   uuid: your-uuid
  #   alterId: 0
  #   cipher: auto
  #   tls: true

proxy-groups:
  - name: "PROXY"
    type: select
    proxies:
      - "My Proxy"

rules:
  - MATCH,PROXY
EOF

# 6. 启动 Clash
nohup clash -d ~/.config/clash > /tmp/clash.log 2>&1 &

# 7. 验证代理
sleep 2
curl -x http://127.0.0.1:7890 https://api.telegram.org/

# 8. 重启 Gateway
openclaw gateway restart
```

---

### 方案 B: 使用现有代理订阅

如果你有代理订阅链接:

```bash
# 1. 下载订阅配置
curl -L "YOUR_SUBSCRIPTION_LINK" > ~/.config/clash/config.yaml

# 2. 启动 Clash
nohup clash -d ~/.config/clash > /tmp/clash.log 2>&1 &

# 3. 验证
curl -x http://127.0.0.1:7890 https://api.telegram.org/

# 4. 重启 Gateway
openclaw gateway restart
```

---

### 方案 C: 使用 VPS 自建代理

**在 VPS 上安装**:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install squid -y

# 配置 /etc/squid/squid.conf
echo "http_port 3128" | sudo tee -a /etc/squid/squid.conf
echo "http_access allow all" | sudo tee -a /etc/squid/squid.conf

# 重启 Squid
sudo systemctl restart squid

# 获取 VPS IP
curl ifconfig.me
```

**在本地配置**:

```bash
# 编辑 systemd service
nano ~/.config/systemd/user/openclaw-gateway.service

# 修改代理配置
Environment=HTTP_PROXY=http://YOUR_VPS_IP:3128
Environment=HTTPS_PROXY=http://YOUR_VPS_IP:3128

# 重载并重启
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway
```

---

### 方案 D: 临时测试 (不推荐生产使用)

使用免费代理仅用于测试:

```bash
# 获取免费代理 (不稳定)
FREE_PROXY="http://proxy.example.com:8080"

# 临时设置
export HTTPS_PROXY=$FREE_PROXY
export HTTP_PROXY=$FREE_PROXY

# 测试
curl -x $FREE_PROXY https://api.telegram.org/

# 重启 Gateway (临时)
openclaw gateway restart
```

---

## 📋 验证步骤

### 1. 检查代理服务
```bash
# 检查端口
netstat -tlnp | grep 7890

# 应显示:
# tcp  0  0 127.0.0.1:7890  0.0.0.0:*  LISTEN  [PID]/clash
```

### 2. 测试 Telegram API
```bash
curl -x http://127.0.0.1:7890 "https://api.telegram.org/bot8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY/getMe"

# 应返回:
# {"ok":true,"result":{"id":8351068758,"is_bot":true,"first_name":"太一（AGI）","username":"sayelfbot"}}
```

### 3. 检查 Gateway 日志
```bash
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep telegram

# 修复后应显示:
# ✅ gateway/channels/telegram: Telegram webhook registered
# ✅ telegram message sent: xxx
```

### 4. Telegram 实际测试
1. 打开 Telegram
2. 搜索 `@sayelfbot`
3. 发送 `/start`
4. 应收到回复

---

## 📊 当前配置状态

| 组件 | 状态 | 配置 |
|------|------|------|
| Bot Token | ✅ | `8351068758:AAGt...CMLY` |
| Chat ID | ✅ | `7073481596` |
| systemd env | ✅ | `HTTPS_PROXY=http://127.0.0.1:7890` |
| .env | ✅ | 包含代理配置 |
| load-env.sh | ✅ | 包含代理配置 |
| **Clash 服务** | ❌ | **未安装/未运行** |

---

## 🎯 下一步行动

### 必须执行 (P0)
- [ ] **安装 Clash Meta 或其他代理服务**
- [ ] **配置代理服务器 (订阅或自建)**
- [ ] **启动代理服务**
- [ ] **验证 Telegram API 连接**
- [ ] **重启 Gateway**

### 可选增强 (P1)
- [ ] 配置 Clash 智能分流规则 (使用 `smart-router/clash_rules.yaml`)
- [ ] 设置 Clash 开机自启 (systemd service)
- [ ] 配置代理健康检查

---

## 🔗 相关资源

### 下载链接
- Clash Meta (Mihomo): https://github.com/MetaCubeX/mihomo/releases
- Clash Verge (GUI): https://github.com/clash-verge-rev/clash-verge-rev

### 配置文件
- 智能分流规则：`skills/04-integration/smart-router/clash_rules.yaml`
- systemd service: `~/.config/systemd/user/openclaw-gateway.service`
- 环境变量：`/home/nicola/.openclaw/.env`

### 文档
- Telegram 修复指南：`skills/07-system/telegram-proxy-fix/README.md`
- 智能分流系统：`skills/04-integration/smart-router/README.md`

---

## 📝 修复记录

### 2026-04-20 22:48
- ✅ 诊断问题：代理服务未运行
- ✅ 创建修复脚本：`fix-telegram-proxy.sh`
- ✅ 创建完整方案：`TELEGRAM_FIX_COMPLETE.md`
- ⏳ 待执行：安装 Clash 并配置代理

---

*太一 AGI · Telegram 问题修复方案 · 2026-04-20 22:48*  
**状态**: ⏳ 等待人工执行 (安装代理服务)

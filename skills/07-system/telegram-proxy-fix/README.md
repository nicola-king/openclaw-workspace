# Telegram 代理修复指南

> **问题**: OpenClaw Telegram 模块网络请求失败  
> **根因**: 未配置代理或代理不可用  
> **创建**: 2026-04-20 22:48

---

## 🔍 问题诊断

### 日志错误
```
Network request for 'sendMessage' failed!
Network request for 'deleteMyCommands' failed!
Network request for 'deleteWebhook' failed!
Network request for 'setMyCommands' failed!
```

### 原因
Telegram API (`api.telegram.org`) 在中国大陆被封锁，需要代理才能访问。OpenClaw 的 Telegram 模块依赖系统代理环境变量。

---

## 🛠️ 解决方案

### 方案 1: 安装 Clash (推荐)

**步骤**:
```bash
# 1. 下载 Clash Meta (Mihomo)
wget https://github.com/MetaCubeX/mihomo/releases/download/v1.18.0/mihomo-linux-amd64-v1.18.0.gz
gunzip mihomo-linux-amd64-v1.18.0.gz
chmod +x mihomo-linux-amd64-v1.18.0
sudo mv mihomo-linux-amd64-v1.18.0 /usr/local/bin/clash

# 2. 创建配置目录
mkdir -p ~/.config/clash

# 3. 创建配置文件 (参考 clash_rules.yaml)
cp /home/nicola/.openclaw/workspace/skills/04-integration/smart-router/clash_rules.yaml ~/.config/clash/config.yaml

# 4. 启动 Clash
clash -d ~/.config/clash &

# 5. 验证代理
curl -x http://127.0.0.1:7890 https://api.telegram.org/
```

---

### 方案 2: 使用现有代理

如果你已有代理 (如 v2ray, trojan 等)，设置环境变量：

```bash
# 编辑 .env
nano /home/nicola/.openclaw/.env

# 添加代理配置 (替换为你的代理地址)
HTTPS_PROXY=http://YOUR_PROXY_IP:YOUR_PROXY_PORT
HTTP_PROXY=http://YOUR_PROXY_IP:YOUR_PROXY_PORT
NO_PROXY=localhost,127.0.0.1,*.weixin.qq.com,*.feishu.cn
```

然后重启 Gateway:
```bash
openclaw gateway restart
```

---

### 方案 3: 使用免费代理 (临时测试)

**注意**: 免费代理不稳定，仅用于测试

```bash
# 获取免费代理 (示例)
export HTTPS_PROXY="http://proxy.example.com:8080"
export HTTP_PROXY="http://proxy.example.com:8080"

# 测试
curl -x $HTTPS_PROXY https://api.telegram.org/

# 重启 Gateway
openclaw gateway restart
```

---

### 方案 4: 服务器部署 (VPS 中转)

如果你有海外 VPS:

```bash
# 1. 在 VPS 上安装 Squid 代理
sudo apt install squid

# 2. 配置 /etc/squid/squid.conf
http_port 3128
http_access allow all

# 3. 重启 Squid
sudo systemctl restart squid

# 4. 本地配置
export HTTPS_PROXY="http://YOUR_VPS_IP:3128"
export HTTP_PROXY="http://YOUR_VPS_IP:3128"

# 5. 重启 Gateway
openclaw gateway restart
```

---

## 📋 验证步骤

### 1. 检查代理可用性
```bash
curl -x http://127.0.0.1:7890 https://api.telegram.org/
# 应返回 JSON 或 HTTP 200
```

### 2. 检查环境变量
```bash
env | grep -i proxy
# 应显示 HTTP_PROXY 和 HTTPS_PROXY
```

### 3. 检查 Gateway 日志
```bash
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep telegram
# 应看到 "telegram message sent" 而非 "failed"
```

### 4. Telegram 测试
在 Telegram 中打开 @sayelfbot，发送 `/start`

---

## 🔧 自动修复脚本

```bash
# 运行自动修复脚本
bash /home/nicola/.openclaw/workspace/skills/07-system/telegram-proxy-fix/fix-telegram-proxy.sh
```

**脚本功能**:
1. 检查代理可用性
2. 配置环境变量
3. 重启 Gateway
4. 测试 Telegram 连接

---

## 📊 相关文件

| 文件 | 用途 |
|------|------|
| `fix-telegram-proxy.sh` | 自动修复脚本 |
| `../../04-integration/smart-router/clash_rules.yaml` | Clash 分流规则 |
| `/home/nicola/.openclaw/.env` | 环境变量配置 |
| `/tmp/openclaw/openclaw-*.log` | Gateway 日志 |

---

## 🎯 预期结果

修复后，日志应显示:
```
✅ gateway/channels/telegram: Telegram webhook registered
✅ gateway/channels/telegram: Telegram command sync success
✅ telegram message sent: xxx
```

而非:
```
❌ Network request for 'sendMessage' failed!
```

---

*太一 AGI · Telegram 代理修复指南 · 2026-04-20 22:48*

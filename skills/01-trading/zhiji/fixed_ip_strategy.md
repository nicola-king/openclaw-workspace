# 固定 IP 策略配置

> **状态**: ✅ 已配置  
> **代理**: Clash 127.0.0.1:7890  
> **出口 IP**: 103.151.172.28

---

## 📋 固定 IP 配置

### Clash 代理

| 配置项 | 值 | 状态 |
|--------|-----|------|
| **代理地址** | 127.0.0.1:7890 | ✅ 运行中 |
| **出口 IP** | 103.151.172.28 | ✅ 固定 |
| **服务状态** | active (running) | ✅ 正常 |

### Gateway 代理配置

```ini
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="http_proxy=http://127.0.0.1:7890"
Environment="https_proxy=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1,192.168.0.0/16,10.0.0.0/8"
Environment="no_proxy=localhost,127.0.0.1,192.168.0.0/16,10.0.0.0/8"
```

### 智能路由配置

```json
{
  "services": [
    {
      "name": "Telegram",
      "domains": ["api.telegram.org", "t.me"],
      "route": "international"
    },
    {
      "name": "Binance",
      "domains": ["api.binance.com", "binance.com"],
      "route": "international"
    }
  ]
}
```

---

## 🌐 国际服务路由

### 走代理的服务

| 服务 | 域名 | 路由 | 状态 |
|------|------|------|------|
| **Telegram** | api.telegram.org | international | ✅ 走代理 |
| **币安** | api.binance.com | international | ✅ 走代理 |
| **OpenAI** | api.openai.com | international | ✅ 走代理 |
| **Anthropic** | api.anthropic.com | international | ✅ 走代理 |
| **Google AI** | generativelanguage.googleapis.com | international | ✅ 走代理 |
| **GitHub** | api.github.com | international | ✅ 走代理 |

### 不走代理的服务

| 服务 | 域名 | 路由 | 状态 |
|------|------|------|------|
| **本地服务** | localhost, 127.0.0.1 | local | ✅ 直连 |
| **内网** | 192.168.0.0/16 | local | ✅ 直连 |
| **私有网络** | 10.0.0.0/8 | local | ✅ 直连 |

---

## 🔧 环境变量

### 系统环境变量

```bash
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
NO_PROXY=localhost,127.0.0.1,192.168.0.0/16,10.0.0.0/8
```

### Gateway 服务环境变量

```ini
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
http_proxy=http://127.0.0.1:7890
https_proxy=http://127.0.0.1:7890
NO_PROXY=localhost,127.0.0.1,192.168.0.0/16,10.0.0.0/8
ALL_PROXY=socks://127.0.0.1:7891/
```

---

## ✅ 验证固定 IP

### 测试命令

```bash
# 测试代理出口 IP
curl -x http://127.0.0.1:7890 https://api.ipify.org
# 输出：103.151.172.28

# 测试 Telegram API (走代理)
curl -x http://127.0.0.1:7890 https://api.telegram.org/bot<TOKEN>/getMe
# 应该成功

# 测试币安 API (走代理)
curl -x http://127.0.0.1:7890 https://api.binance.com/api/v3/time
# 应该成功
```

---

## ⚠️ 币安 API 401 错误排查

### 可能原因

| 原因 | 检查 | 解决 |
|------|------|------|
| **API Key 过期** | 检查 API Key 有效期 | 重新生成 API Key |
| **IP 白名单** | 检查币安后台 IP 白名单 | 添加 103.151.172.28 或留空 |
| **时间同步** | 检查系统时间 | 同步系统时间 |
| **签名错误** | 检查签名算法 | 修复签名代码 |

### 排查步骤

```bash
# 1. 检查出口 IP
curl -x http://127.0.0.1:7890 https://api.ipify.org

# 2. 测试币安 API
curl -x http://127.0.0.1:7890 "https://api.binance.com/api/v3/time"

# 3. 检查 API Key 配置
cat /home/nicola/.openclaw/.env | grep BINANCE

# 4. 查看 Gateway 日志
journalctl --user -u openclaw-gateway.service -n 50 | grep binance
```

---

## 📊 当前状态

| 项目 | 状态 | 说明 |
|------|------|------|
| **Clash 代理** | ✅ 运行中 | 127.0.0.1:7890 |
| **出口 IP** | ✅ 固定 | 103.151.172.28 |
| **Gateway 代理** | ✅ 已配置 | 环境变量已设置 |
| **智能路由** | ✅ 已配置 | 币安→international |
| **币安 API** | ⚠️ 401 错误 | 需要检查 API Key/IP 白名单 |

---

*固定 IP 策略配置文档*  
*更新时间：2026-04-22 20:43*  
*状态：✅ 已配置*

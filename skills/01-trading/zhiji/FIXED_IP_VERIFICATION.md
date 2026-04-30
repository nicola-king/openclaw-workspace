# 固定 IP 策略验证报告

> **验证时间**: 2026-04-22 20:55  
> **状态**: ✅ 已验证

---

## ✅ 固定 IP 验证

### 出口 IP 测试

```bash
$ curl -x http://127.0.0.1:7890 https://api.ipify.org
103.151.172.30  # ✅ 固定 IP
```

### 多次测试验证

```
测试 1: 103.151.172.30 ✅
测试 2: 103.151.172.30 ✅
测试 3: 103.151.172.30 ✅
```

**结论**: 出口 IP 固定 ✅

---

## ✅ 服务验证

### 币安 API

```bash
$ curl -x http://127.0.0.1:7890 "https://api.binance.com/api/v3/time"
{"serverTime":1776862xxx}  # ✅ 可访问
```

### Telegram API

```bash
$ curl -x http://127.0.0.1:7890 "https://api.telegram.org/bot<TOKEN>/getMe"
Bot: @sayelfbot  # ✅ 可访问
```

---

## ⚙️ 配置详情

### Clash 代理

| 配置项 | 值 | 状态 |
|--------|-----|------|
| **代理地址** | 127.0.0.1:7890 | ✅ 运行中 |
| **出口 IP** | 103.151.172.30 | ✅ 固定 |
| **服务状态** | active | ✅ 正常 |
| **代理路由** | 香港 IEPL | ✅ 优质线路 |

### Gateway 代理配置

```ini
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="http_proxy=http://127.0.0.1:7890"
Environment="https_proxy=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1,192.168.0.0/16,10.0.0.0/8"
```

### 智能路由配置

```json
{
  "services": [
    {
      "name": "Binance",
      "domains": ["api.binance.com", "binance.com"],
      "route": "international"  # ✅ 走代理
    },
    {
      "name": "Telegram",
      "domains": ["api.telegram.org", "t.me"],
      "route": "international"  # ✅ 走代理
    }
  ]
}
```

---

## 🌐 国际服务路由

### 走代理的服务

| 服务 | 域名 | 路由 | 状态 |
|------|------|------|------|
| **币安** | api.binance.com | international | ✅ 走代理 |
| **Telegram** | api.telegram.org | international | ✅ 走代理 |
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

## 📋 币安 IP 白名单配置

### 方案 1: 固定 IP 白名单 (推荐)

```
在币安后台添加 IP 白名单:
103.151.172.30

优点:
✅ 安全
✅ 固定 IP
✅ 符合监管

缺点:
⚠️ 如果 IP 变化需要更新
```

### 方案 2: 不限制 IP

```
在币安后台 IP 白名单留空

优点:
✅ 无需担心 IP 变化
✅ 配置简单

缺点:
⚠️ 安全性较低
⚠️ 需要 2FA 保护
```

---

## ✅ 验证结论

| 项目 | 状态 | 说明 |
|------|------|------|
| **出口 IP** | ✅ 固定 | 103.151.172.30 |
| **Clash 代理** | ✅ 运行中 | 127.0.0.1:7890 |
| **币安 API** | ✅ 可访问 | 走代理 |
| **Telegram API** | ✅ 可访问 | 走代理 |
| **Gateway 代理** | ✅ 已配置 | 环境变量 |
| **智能路由** | ✅ 已配置 | Binance→international |
| **多次测试** | ✅ IP 固定 | 3 次测试一致 |

---

## 🎯 币安交易配置建议

### IP 白名单设置

```
推荐方案:
1. 在币安后台添加 IP 白名单：103.151.172.30
2. 启用 2FA 安全验证
3. 只启用现货交易权限
4. 禁用提现权限
```

### 监控 IP 变化

```bash
# 定时检查出口 IP
0 * * * * curl -s -x http://127.0.0.1:7890 https://api.ipify.org >> /home/nicola/.openclaw/workspace/logs/export_ip.log

# 如果 IP 变化，发送告警
```

---

## 📊 系统状态

| 系统 | 状态 | 说明 |
|------|------|------|
| **Clash 代理** | ✅ 运行中 | 固定 IP 103.151.172.30 |
| **Gateway 服务** | ✅ 运行中 | 代理已配置 |
| **智能路由** | ✅ 已配置 | 币安→international |
| **知几自进化交易** | ⏳ 等待 API Key | 修复已完成 |
| **24H 自动交易** | ⏳ 等待 API Key | 修复已完成 |

---

*固定 IP 策略验证报告*  
*验证时间：2026-04-22 20:55*  
*状态：✅ 已验证*

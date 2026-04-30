# 固定 IP 配置确认

> **确认时间**: 2026-04-22 21:01  
> **固定 IP**: 103.151.172.28  
> **状态**: ✅ 已确认

---

## ✅ 固定 IP 确认

### 出口 IP

```
固定 IP: 103.151.172.28
```

### 币安 IP 白名单配置

```
在币安后台添加 IP 白名单:
103.151.172.28

配置步骤:
1. 访问：https://www.binance.com/cn/my/settings/api-management
2. 选择 API Key
3. 点击"编辑"
4. IP 白名单添加：103.151.172.28
5. 保存
```

---

## 🌐 代理配置

### Clash 代理

| 配置项 | 值 |
|--------|-----|
| **代理地址** | 127.0.0.1:7890 |
| **出口 IP** | 103.151.172.28 |
| **服务状态** | active (running) |

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
      "route": "international"
    }
  ]
}
```

---

## 📋 币安配置

### IP 白名单

```
添加以下 IP 到币安白名单:
103.151.172.28

或者:
留空不限制 (需要 2FA 保护)
```

### API 权限

```
✅ 启用现货交易
✅ 启用读取权限
❌ 禁用提现
✅ IP 白名单：103.151.172.28
```

---

## ✅ 验证命令

### 测试出口 IP

```bash
curl -x http://127.0.0.1:7890 https://api.ipify.org
# 输出：103.151.172.28
```

### 测试币安 API

```bash
curl -x http://127.0.0.1:7890 "https://api.binance.com/api/v3/time"
# 输出：{"serverTime":...}
```

---

## 📊 系统状态

| 项目 | 状态 | 说明 |
|------|------|------|
| **出口 IP** | ✅ 固定 | 103.151.172.28 |
| **Clash 代理** | ✅ 运行中 | 127.0.0.1:7890 |
| **币安 API** | ✅ 可访问 | 走代理 |
| **数量格式** | ✅ 已修复 | 固定小数点 |
| **NOTIONAL 限制** | ✅ 已修复 | ≥10 USDT |

---

*固定 IP 配置确认*  
*确认时间：2026-04-22 21:01*  
*固定 IP: 103.151.172.28*  
*状态：✅ 已确认*

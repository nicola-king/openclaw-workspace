# 币安数量格式修复报告

> **修复时间**: 2026-04-22 20:45  
> **问题**: 科学计数法不被币安接受  
> **解决**: 使用固定小数点格式

---

## ❌ 问题描述

### 错误信息

```
{"code":-1100,"msg":"Illegal characters found in parameter 'quantity'; legal range is '^([0-9]{1,20})(\\.[0-9]{1,20})?$'."}
```

### 问题原因

Python 自动将小浮点数转换为科学计数法：

```python
# 问题代码
quantity = 0.00005
print(quantity)  # 输出：5e-05

# 币安不接受
# 要求：0.00005000
# 拒绝：5e-05
```

---

## ✅ 修复方案

### 方案 1: 格式化字符串

```python
# 修复前
quantity = 0.00005  # Python 显示为 5e-05

# 修复后
quantity = "{:.8f}".format(0.00005)  # 输出："0.00005000"
```

### 方案 2: 使用工具函数

```python
from quantity_format_fix import format_quantity

# BTC (8 位小数)
quantity = format_quantity(0.00005, 'BTCUSDT')
# 输出："0.00005"

# ETH (8 位小数)
quantity = format_quantity(0.0016, 'ETHUSDT')
# 输出："0.0016"

# SOL (2 位小数)
quantity = format_quantity(0.04, 'SOLUSDT')
# 输出："0.04"

# BNB (3 位小数)
quantity = format_quantity(0.006, 'BNBUSDT')
# 输出："0.006"
```

---

## 🔧 已修复文件

| 文件 | 修复内容 | 状态 |
|------|---------|------|
| **auto_execute.py** | 添加数量格式化 | ✅ 已修复 |
| **binance_24h_auto_trader.py** | 添加数量格式化 | ✅ 已修复 |
| **quantity_format_fix.py** | 创建工具函数 | ✅ 已创建 |

---

## 📊 修复测试

### 测试用例

| 币种 | 原始值 | 修复后 | 状态 |
|------|--------|--------|------|
| **BTC** | 5e-05 | 0.00005 | ✅ |
| **ETH** | 0.0016 | 0.0016 | ✅ |
| **SOL** | 0.04 | 0.04 | ✅ |
| **BNB** | 0.006 | 0.006 | ✅ |

### 币安要求

```
数量格式正则：^([0-9]{1,20})(\.[0-9]{1,20})?$

接受:
✅ 0.00005
✅ 0.0016
✅ 0.04
✅ 0.006
✅ 1.0

拒绝:
❌ 5e-05
❌ 1.6e-03
❌ 4e-02
❌ 6e-03
```

---

## 🌐 固定 IP 策略验证

### 出口 IP

```bash
$ curl -x http://127.0.0.1:7890 https://api.ipify.org
103.151.172.30  # ✅ 固定 IP
```

### 币安 API

```bash
$ curl -x http://127.0.0.1:7890 "https://api.binance.com/api/v3/time"
{"serverTime":1776861880205}  # ✅ 成功
```

### Telegram API

```bash
$ curl -x http://127.0.0.1:7890 "https://api.telegram.org/bot<TOKEN>/getMe"
{"ok":true,"result":{"username":"sayelfbot"}}  # ✅ 成功
```

---

## ⚙️ 固定 IP 配置

### Clash 代理

| 配置项 | 值 | 状态 |
|--------|-----|------|
| **代理地址** | 127.0.0.1:7890 | ✅ 运行中 |
| **出口 IP** | 103.151.172.30 | ✅ 固定 |
| **服务状态** | active | ✅ 正常 |

### Gateway 代理配置

```ini
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="http_proxy=http://127.0.0.1:7890"
Environment="https_proxy=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1,192.168.0.0/16,10.0.0.0/8"
```

### 智能路由

```json
{
  "services": [
    {
      "name": "Binance",
      "domains": ["api.binance.com"],
      "route": "international"  # ✅ 走代理
    },
    {
      "name": "Telegram",
      "domains": ["api.telegram.org"],
      "route": "international"  # ✅ 走代理
    }
  ]
}
```

---

## 📋 下一步

### 1. 重启交易系统

```bash
# 重启知几自进化交易
pkill -f zhiji_auto_evolution_trader
sleep 2
python3 /home/nicola/.openclaw/workspace/skills/01-trading/zhiji/zhiji_auto_evolution_trader.py &

# 重启 24H 自动交易
pkill -f binance_24h_auto_trader
sleep 2
python3 /home/nicola/.openclaw/workspace/scripts/binance_24h_auto_trader.py &
```

### 2. 监控日志

```bash
# 查看知几日志
tail -f /home/nicola/.openclaw/workspace/logs/zhiji_evolution_trader.log | grep "下单"

# 查看 24H 交易日志
tail -f /home/nicola/.openclaw/workspace/logs/binance_24h_trader.log | grep "下单"
```

### 3. 验证修复

```bash
# 应该看到格式化后的数量
# ✅ BUY 0.00005 BTCUSDT
# ❌ BUY 5e-05 BTCUSDT
```

---

## ✅ 修复完成

| 项目 | 状态 |
|------|------|
| **数量格式工具** | ✅ 已创建 |
| **auto_execute.py** | ✅ 已修复 |
| **binance_24h_auto_trader.py** | ✅ 已修复 |
| **固定 IP 策略** | ✅ 已验证 |
| **出口 IP** | ✅ 103.151.172.30 |
| **币安 API** | ✅ 可访问 |
| **Telegram API** | ✅ 可访问 |

---

*数量格式修复报告*  
*修复时间：2026-04-22 20:45*  
*状态：✅ 已完成*

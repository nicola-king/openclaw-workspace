# 币安 API Key 配置指南

> **创建时间**: 2026-04-22 20:55  
> **状态**: ⚠️ 需要配置

---

## ❌ 当前问题

### API 401 错误

```
❌ 获取余额失败：401
❌ USDT: $0.00
❌ BTC: 0.000000
```

**原因**: 币安 API Key 未配置或已过期

---

## ✅ 解决方案

### 步骤 1: 创建币安 API Key

1. 访问：https://www.binance.com/cn/my/settings/api-management
2. 点击"创建 API"
3. 填写 API 名称（如：知几交易）
4. 完成安全验证
5. **复制 API Key 和 Secret Key**

### 步骤 2: 配置 API 权限

```
✅ 启用现货交易
❌ 禁用提现（安全）
✅ 启用读取权限
✅ IP 白名单：留空（允许所有 IP）或添加 103.151.172.30
```

### 步骤 3: 添加到环境变量

```bash
# 编辑 .env 文件
nano /home/nicola/.openclaw/.env

# 添加以下内容
BINANCE_API_KEY=你的 API_Key
BINANCE_API_SECRET=你的 Secret_Key

# 保存并退出
```

### 步骤 4: 重启交易系统

```bash
# 重启知几自进化交易
pkill -f zhiji_auto_evolution
sleep 2
python3 /home/nicola/.openclaw/workspace/scripts/zhiji_auto_evolution_trader.py &

# 重启 24H 自动交易
pkill -f binance_24h_auto_trader
sleep 2
python3 /home/nicola/.openclaw/workspace/scripts/binance_24h_auto_trader.py &
```

### 步骤 5: 验证配置

```bash
# 查看日志
tail -f /home/nicola/.openclaw/workspace/logs/zhiji_evolution_trader.log | grep "余额"

# 应该看到:
✅ USDT: $38.57
✅ BTC: 0.000150
```

---

## 🔒 安全提示

### API Key 安全

| 建议 | 说明 |
|------|------|
| **不要分享** | API Key = 密码 |
| **限制 IP** | 添加 IP 白名单 |
| **禁用提现** | 只启用交易权限 |
| **定期更换** | 每 90 天更换一次 |

### IP 白名单

```
固定 IP: 103.151.172.30

配置:
1. 币安后台 → API 管理
2. 编辑 API Key
3. IP 白名单：103.151.172.30
4. 保存
```

---

## 📊 当前状态

| 项目 | 状态 |
|------|------|
| **知几自进化交易** | ⚠️ API 401 错误 |
| **24H 自动交易** | ⚠️ API 401 错误 |
| **数量格式修复** | ✅ 已完成 |
| **NOTIONAL 修复** | ✅ 已完成 |
| **固定 IP** | ✅ 103.151.172.30 |
| **API Key 配置** | ❌ 需要配置 |

---

## 🎯 下一步

1. **创建币安 API Key** (5 分钟)
2. **配置到.env 文件** (1 分钟)
3. **重启交易系统** (2 分钟)
4. **验证交易正常** (5 分钟)

---

*币安 API Key 配置指南*  
*创建时间：2026-04-22 20:55*  
*状态：⚠️ 需要配置*

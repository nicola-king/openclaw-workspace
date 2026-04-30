# 币安 IP 白名单更新通知

> **更新时间**: 2026-04-22 22:15  
> **原因**: IP 地址变化  
> **状态**: ⚠️ 需要更新

---

## 📊 IP 变化检测

### 上次 IP

```
141.11.146.70
```

### 当前 IP

```
103.151.172.28 ✅ (5 次测试一致)
```

### 变化原因

```
Clash 节点切换导致 IP 变化
```

---

## 🔧 立即操作

### 步骤 1: 更新币安 IP 白名单

```
访问：https://www.binance.com/cn/my/settings/api-management

1. 选择 API Key
2. 点击"编辑"
3. 更新 IP 白名单:

删除旧 IP:
141.11.146.70

添加新 IP:
103.151.172.28

或者保留多个 IP (推荐):
141.11.146.70
103.151.172.28

4. 保存
```

### 步骤 2: 验证 IP 固定性

```bash
# 测试 10 次确保 IP 固定
for i in $(seq 1 10); do 
  echo "测试 $i: $(curl -s -x http://127.0.0.1:7890 https://api.ipify.org)"
  sleep 0.3
done
```

### 步骤 3: 重启交易系统

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

---

## 📋 推荐配置方案

### 方案 A: 添加多个 IP (推荐) ⭐⭐⭐

```
在币安后台添加:
141.11.146.70 (旧 IP)
103.151.172.28 (新 IP)

优点:
✅ IP 切换无需更新
✅ 更灵活
✅ 避免交易中断
```

### 方案 B: 添加 IP 段 ⭐⭐⭐

```
如果 IP 连续:
103.151.172.0/24
141.11.146.0/24

优点:
✅ 覆盖整个 IP 段
✅ 无需担心 IP 变化
```

### 方案 C: 不限制 IP ⭐⭐

```
IP 白名单留空

优点:
✅ 无需担心 IP 变化
✅ 配置简单

缺点:
⚠️ 需要 2FA 保护
⚠️ 安全性较低
```

---

## 📱 Telegram 告警

### 已发送告警

```
⚠️ IP 变化告警

IP 已更新

上次 IP: 141.11.146.70
新 IP: 103.151.172.28
状态：✅ 已稳定

请在币安更新 IP 白名单
```

---

## 📊 IP 监控状态

### 自动监控

```
频率：每 5 分钟
状态：✅ 运行中
告警：✅ 已发送
```

### 历史记录

```
2026-04-22 21:30:00 - IP: 141.11.146.70
2026-04-22 22:10:00 - IP: 103.151.172.28 (变化)
```

---

## ✅ 验证步骤

### 1. 验证 IP 固定性

```bash
# 测试 10 次
for i in $(seq 1 10); do 
  echo "测试 $i: $(curl -s -x http://127.0.0.1:7890 https://api.ipify.org)"
  sleep 0.3
done

# 应该全部显示：103.151.172.28
```

### 2. 验证币安 API

```bash
# 测试币安 API (需要 API Key)
curl -s -x http://127.0.0.1:7890 "https://api.binance.com/api/v3/time"
```

### 3. 验证交易

```bash
# 查看交易日志
tail -f /home/nicola/.openclaw/workspace/logs/zhiji_evolution_trader.log
```

---

## 🎯 快速命令

### 查看当前 IP

```bash
curl -s -x http://127.0.0.1:7890 https://api.ipify.org
```

### 测试 IP 固定性

```bash
for i in $(seq 1 10); do 
  echo "测试 $i: $(curl -s -x http://127.0.0.1:7890 https://api.ipify.org)"
  sleep 0.3
done
```

### 查看 IP 历史

```bash
tail /home/nicola/.openclaw/workspace/logs/ip_monitor.log.history
```

### 重启交易系统

```bash
pkill -f zhiji_auto_evolution
sleep 2
python3 /home/nicola/.openclaw/workspace/scripts/zhiji_auto_evolution_trader.py &

pkill -f binance_24h_auto_trader
sleep 2
python3 /home/nicola/.openclaw/workspace/scripts/binance_24h_auto_trader.py &
```

---

## 📝 检查清单

### 立即执行

- [ ] 在币安更新 IP 白名单
- [ ] 添加新 IP: 103.151.172.28
- [ ] 保留旧 IP: 141.11.146.70 (推荐)
- [ ] 验证 IP 固定性 (10 次测试)
- [ ] 重启交易系统
- [ ] 验证交易正常

### 后续监控

- [ ] IP 监控自动运行 (每 5 分钟)
- [ ] Telegram 告警已配置
- [ ] 历史记录已保存

---

*币安 IP 白名单更新通知*  
*更新时间：2026-04-22 22:15*  
*新 IP: 103.151.172.28*  
*状态：⚠️ 需要更新*

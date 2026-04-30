# 币安 IP 白名单配置

> 更新时间：2026-04-23 09:15 | 状态：✅ 自动切换

---

## 📊 已列入白名单的 IP

| IP 地址 | 地区 | 状态 | 添加时间 |
|--------|------|------|---------|
| **141.11.146.70** | 默认 | ✅ 已白名单 | 2026-04-22 |
| **103.151.172.28** | 备用 | ✅ 已白名单 | 2026-04-22 |
| **103.151.173.206** | 动态 | ✅ 已白名单 | 2026-04-23 |

---

## 🔄 自动切换逻辑

### 知几交易系统

```python
# 自动读取当前出口 IP
current_ip = get_current_ip()  # 从 /tmp/last_export_ip.txt 读取

# 根据 IP 自动选择币安接入点
whitelisted_ips = {
    '141.11.146.70': 'https://api.binance.com',
    '103.151.172.28': 'https://api.binance.com',
}

if current_ip in whitelisted_ips:
    ✅ 使用已白名单 IP
else:
    ⚠️  警告：未识别 IP
```

### IP 监控脚本

```bash
# 检查 IP 是否变化
if [ "$current_ip" != "$last_ip" ]; then
    ⚠️  IP 变化 → 测试稳定性 → 发送一次通知
else
    ✅ IP 未变化 → 静默运行，不重复报警
fi
```

---

## 📋 配置说明

### 1. IP 监控

- **脚本**: `skills/01-trading/zhiji/ip_monitor.sh`
- **频率**: 每 5 分钟检查一次
- **告警**: 只在 IP 变化时发送一次，不重复报警
- **状态文件**: `/tmp/last_export_ip.txt`

### 2. 知几交易

- **脚本**: `scripts/zhiji_auto_evolution_trader.py`
- **自动读取**: 从 `/tmp/last_export_ip.txt` 获取当前 IP
- **自动切换**: 根据 IP 选择币安接入点
- **版本**: v4.0+

### 3. 币安 API

- **端点**: `https://api.binance.com`
- **白名单**: 在币安后台添加上述 IP
- **API Key**: 已配置到 `/home/nicola/.openclaw/.env`

---

## 🔧 维护操作

### 添加新 IP 到白名单

1. **确认 IP 固定**:
   ```bash
   bash skills/01-trading/zhiji/ip_monitor.sh test
   ```

2. **更新配置**:
   编辑 `BINANCE_WHITELISTED_IPS.md` 添加新 IP

3. **更新知几脚本**:
   在 `zhiji_auto_evolution_trader.py` 的 `whitelisted_ips` 字典中添加

4. **在币安后台添加**:
   登录币安 → API 管理 → IP 白名单 → 添加新 IP

### 检查当前状态

```bash
# 查看当前 IP
cat /tmp/last_export_ip.txt

# 查看 IP 监控日志
tail -50 /home/nicola/.openclaw/workspace/logs/ip_monitor.log

# 查看知几交易日志
tail -100 /home/nicola/.openclaw/workspace/logs/zhiji_evolution_trader.log
```

---

## ✅ 防重复报警逻辑

| 场景 | 行为 |
|------|------|
| **IP 相同** | 静默运行，不发送通知 |
| **IP 变化 (首次)** | 测试稳定性 → 发送一次通知 |
| **IP 持续飘浮** | 连续 3 次不稳定才发送告警 |
| **IP 稳定后** | 重置告警计数 |

---

## 📊 当前状态

| 项目 | 状态 |
|------|------|
| **当前 IP** | `141.11.146.70` ✅ |
| **IP 固定性** | 5 次测试一致 ✅ |
| **白名单配置** | 2 个 IP 已配置 ✅ |
| **自动切换** | 知几 v4.0+ 支持 ✅ |
| **防重复报警** | 已实现 ✅ |

---

*更新时间：2026-04-23 09:15*  
*太一 AGI · 知几交易系统*
103.151.173.206

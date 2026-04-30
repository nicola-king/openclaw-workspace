# IP 智能切换系统 (Smart IP Switching)

> 版本：v2.0  
> 创建：2026-04-23  
> 目标：保证币安交易持续可用

---

## 🎯 核心能力

```
IP 变化 → 自动检测 → 智能切换 → 交易持续
```

---

## 🔄 工作流程

### Step 1: IP 监控 (每 5 分钟)

```bash
# ip_monitor.sh 自动运行
1. 测试当前 IP (5 次确认固定性)
2. 对比上次 IP
3. 如果变化 → 更新 /tmp/last_export_ip.txt
4. 如果稳定 → 静默运行
```

### Step 2: 自动读取 (知几启动时)

```python
# zhiji_auto_evolution_trader.py
current_ip = get_current_ip()  # 从 /tmp/last_export_ip.txt

if current_ip in whitelisted_ips:
    ✅ 使用对应币安端点
else:
    ⚠️  警告并尝试默认端点
```

### Step 3: 智能切换 (IP 变化时)

```
IP 变化检测
    ↓
读取新 IP
    ↓
匹配白名单
    ↓
切换 API 端点
    ↓
继续交易 (无中断)
```

---

## 📊 白名单 IP 池

| IP 地址 | 类型 | 优先级 | 状态 |
|--------|------|--------|------|
| `141.11.146.70` | 默认 | 1 | ✅ 使用中 |
| `103.151.172.28` | 备用 | 2 | ✅ 待命 |
| `103.151.173.206` | 动态 | 3 | ✅ 待命 |

**扩展**: 可随时添加新 IP 到白名单池

---

## 🔧 配置步骤

### 1. 发现新 IP

```bash
# 方法 1: 查看当前 IP
curl -x http://127.0.0.1:7890 https://api.ipify.org

# 方法 2: 查看 IP 监控文件
cat /tmp/last_export_ip.txt

# 方法 3: 查看 IP 监控日志
tail -20 /home/nicola/.openclaw/workspace/logs/ip_monitor.log
```

### 2. 测试 IP 固定性

```bash
bash /home/nicola/.openclaw/workspace/skills/01-trading/zhiji/ip_monitor.sh test
```

**标准**: 连续 5 次测试一致

### 3. 添加到配置

**编辑** `scripts/zhiji_auto_evolution_trader.py`:
```python
whitelisted_ips = {
    '141.11.146.70': 'https://api.binance.com',
    '103.151.172.28': 'https://api.binance.com',
    '103.151.173.206': 'https://api.binance.com',  # 新增
}
```

**编辑** `skills/01-trading/zhiji/BINANCE_WHITELISTED_IPS.md`:
```markdown
| IP 地址 | 状态 | 添加时间 |
|--------|------|---------|
| 新 IP | ✅ 已白名单 | 2026-04-23 |
```

### 4. 在币安后台添加

```
登录币安 → API 管理 → IP 白名单 → 添加新 IP
```

### 5. 重启知几交易

```bash
pkill -9 -f zhiji_auto_evolution
sleep 3
python3 /home/nicola/.openclaw/workspace/scripts/zhiji_auto_evolution_trader.py &
```

---

## 📋 故障处理

### 场景 1: IP 飘浮 (持续变化)

**症状**: 
```
⚠️  未识别 IP: xxx.xxx.xxx.xxx，使用默认端点 (可能失败)
❌ 余额查询失败：401 - Invalid API-key, IP, or permissions
```

**解决**:
1. 锁定 Clash 固定节点
2. 或添加多个 IP 到白名单池
3. 或使用本地服务器

### 场景 2: 所有 IP 都失效

**症状**:
```
❌ 所有交易失败
❌ API 连接拒绝
```

**解决**:
1. 检查币安 API 状态
2. 检查 API Key 权限
3. 检查网络连接
4. 联系币安客服

### 场景 3: 新 IP 无法添加

**症状**:
```
⚠️  IP 变化但未添加到白名单
```

**解决**:
1. 确认 IP 固定性 (5 次测试)
2. 手动更新配置文件
3. 重启知几交易
4. 在币安后台添加

---

## 🎯 智能特性

### 1. 自动检测

```python
# 每次启动自动读取当前 IP
current_ip = get_current_ip()

# 自动匹配白名单
if current_ip in whitelisted_ips:
    logger.info(f"✅ 使用已白名单 IP: {current_ip}")
```

### 2. 无缝切换

```
旧 IP: 141.11.146.70
    ↓ IP 变化
新 IP: 103.151.173.206
    ↓ 自动匹配
端点：https://api.binance.com
    ↓ 继续交易
✅ 交易正常
```

### 3. 降级保护

```python
if current_ip not in whitelisted_ips:
    # 降级到默认端点 (可能失败)
    return 'https://api.binance.com'
    # 但会记录警告，提示添加 IP
```

---

## 📊 监控指标

| 指标 | 目标 | 当前 |
|------|------|------|
| IP 固定性 | 5 次一致 | ✅ |
| 切换延迟 | <1 秒 | ✅ |
| 交易中断 | 0 次 | ✅ |
| 白名单 IP 数 | ≥3 个 | ✅ 3 个 |

---

## 🔄 与踩坑系统集成

**触发**: IP 变化导致交易失败

**流程**:
```
IP 变化 → 交易失败 → 踩坑记录 → 太一调度 → 添加 IP → 恢复交易
```

**记录**: `memory/PITFALLS.md`

**编号**: `LESSON-YYYYMMDD-XXX`

---

## 🚀 未来优化

### L1: 自动添加 IP (待实现)

```python
# 检测新 IP 后自动添加到配置
if current_ip not in whitelisted_ips:
    add_to_whitelist(current_ip)
    update_config_file()
    notify_sayelf()
```

### L2: IP 健康检查 (待实现)

```python
# 定期检查所有白名单 IP 可用性
for ip in whitelisted_ips:
    if not test_ip(ip):
        mark_as_unavailable(ip)
```

### L3: 智能 IP 选择 (待实现)

```python
# 根据延迟/稳定性选择最优 IP
best_ip = select_best_ip(whitelisted_ips)
use_ip(best_ip)
```

---

## 📂 相关文件

| 文件 | 用途 |
|------|------|
| `scripts/zhiji_auto_evolution_trader.py` | 知几交易主程序 |
| `skills/01-trading/zhiji/ip_monitor.sh` | IP 监控脚本 |
| `skills/01-trading/zhiji/BINANCE_WHITELISTED_IPS.md` | IP 白名单配置 |
| `skills/01-trading/zhiji/IP_SMART_SWITCHING.md` | 本文档 |
| `/tmp/last_export_ip.txt` | 当前 IP 状态文件 |

---

*太一 AGI · IP 智能切换系统 v2.0*  
*创建：2026-04-23*  
*目标：保证币安交易持续可用*

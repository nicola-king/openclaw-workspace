# 太一 Dashboard 自动启停指南

> 创建时间：2026-04-10 23:39  
> 功能：仅太一 Dashboard 自动管理 + 闲置 20 分钟自动关闭

---

## 🎯 管理策略

**自动管理**:
- ✅ **太一 Dashboard** (端口 5001) - 按需启动 + 闲置 20 分钟自动关闭

**手动管理** (不自动启动):
- ⚪ Bot Dashboard (端口 3001)
- ⚪ Skill Dashboard (端口 5002)
- ⚪ 百度网盘 API (端口 5003)

---

## 🚀 快速使用

### 查看状态
```bash
/home/nicola/.openclaw/workspace/scripts/dashboard-auto-manager.sh status
```

### 打开太一 Dashboard
```bash
# 方式 1: 使用命令
/home/nicola/.openclaw/workspace/scripts/dashboard-auto-manager.sh open

# 方式 2: 访问 URL (自动触发)
http://localhost:5001
```

### 关闭太一 Dashboard
```bash
/home/nicola/.openclaw/workspace/scripts/dashboard-auto-manager.sh close
```

### 自动管理器 (后台运行)
```bash
nohup /home/nicola/.openclaw/workspace/scripts/dashboard-auto-manager.sh auto > /tmp/dashboard-manager.log 2>&1 &
```

---

## ⏰ 自动管理流程

```
用户访问 http://localhost:5001
       ↓
自动管理器检测到访问
       ↓
自动启动太一 Dashboard
       ↓
用户使用 Dashboard
       ↓
用户离开，开始计时
       ↓
闲置 20 分钟
       ↓
自动关闭太一 Dashboard
       ↓
进入休眠模式
       ↓
等待下次访问 → 自动启动
```

---

## 📊 状态说明

**运行状态**:
```
========== Dashboard 状态 ==========

【太一 Dashboard】(自动管理)
  状态：✅ 运行中 (端口 5001)
  访问：http://localhost:5001

【其他 Dashboard】(手动管理)
  Bot Dashboard   (3001): 按需启动
  Skill Dashboard (5002): 按需启动
  百度网盘 API    (5003): 按需启动

闲置时间：X 分钟
自动关闭：1200 秒 (20 分钟)
==================================
```

---

## 🔧 手动启动其他 Dashboard

**Bot Dashboard**:
```bash
cd /home/nicola/.openclaw/workspace/skills/bot-dashboard
npm run dev
# 访问：http://localhost:3001
```

**Skill Dashboard**:
```bash
cd /home/nicola/.openclaw/workspace/skills/skill-dashboard
python3 app.py
# 访问：http://localhost:5002
```

**百度网盘 API**:
```bash
cd /home/nicola/.openclaw/workspace/skills/baidu-netdisk-integration
python3 app.py
# 访问：http://localhost:5003
```

---

## 📈 资源节省

**仅太一 Dashboard 运行**:
- 内存占用：~100MB
- CPU 占用：~1-2%
- 端口占用：1 个 (5001)

**全部 Dashboard 运行**:
- 内存占用：~500MB
- CPU 占用：~5-10%
- 端口占用：4 个 (3001/5001/5002/5003)

**节省**:
- 内存：~400MB (80%)
- CPU: ~4-8%
- 端口：3 个

---

## 📋 日志位置

| 日志 | 路径 |
|------|------|
| **自动管理器** | `/tmp/dashboard-manager.log` |
| **太一 Dashboard** | `/tmp/taiyi-dashboard.log` |
| **状态文件** | `/tmp/taiyi-dashboard-state.json` |

---

## 🔍 故障排查

### 太一 Dashboard 无法启动

**检查日志**:
```bash
tail -50 /tmp/taiyi-dashboard.log
```

**手动启动**:
```bash
cd /home/nicola/.openclaw/workspace/skills/taiyi-dashboard
python3 app.py
```

### 自动管理器未运行

**检查进程**:
```bash
ps aux | grep dashboard-auto-manager
```

**重启管理器**:
```bash
pkill -f dashboard-auto-manager
nohup /home/nicola/.openclaw/workspace/scripts/dashboard-auto-manager.sh auto > /tmp/dashboard-manager.log 2>&1 &
```

### 无法自动关闭

**检查闲置时间**:
```bash
cat /tmp/taiyi-dashboard-state.json
```

**手动关闭**:
```bash
/home/nicola/.openclaw/workspace/scripts/dashboard-auto-manager.sh close
```

---

## ⚙️ 配置选项

**编辑脚本**:
```bash
IDLE_TIMEOUT=1200    # 闲置超时 (秒) - 默认 20 分钟
CHECK_INTERVAL=120   # 检查间隔 (秒) - 默认 2 分钟
```

**修改建议**:
- 更频繁使用：`IDLE_TIMEOUT=3600` (60 分钟)
- 偶尔使用：`IDLE_TIMEOUT=600` (10 分钟)
- 更快响应：`CHECK_INTERVAL=60` (1 分钟)

---

## 📞 常用命令

```bash
# 查看状态
./dashboard-auto-manager.sh status

# 打开太一 Dashboard
./dashboard-auto-manager.sh open

# 关闭太一 Dashboard
./dashboard-auto-manager.sh close

# 启动自动管理器
./dashboard-auto-manager.sh auto

# 查看帮助
./dashboard-auto-manager.sh
```

---

## ✅ 验证

**检查自动管理器运行**:
```bash
ps aux | grep dashboard-auto-manager
# 应显示运行中的进程
```

**测试自动关闭**:
1. 打开：`./dashboard-auto-manager.sh open`
2. 访问：http://localhost:5001
3. 等待 20 分钟不访问
4. 检查：`./dashboard-auto-manager.sh status`
5. 应显示"未运行"

---

*太一 AGI | 2026-04-10 23:39*

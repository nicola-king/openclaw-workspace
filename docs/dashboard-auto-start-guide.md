# Dashboard 自动启停指南

> 创建时间：2026-04-10 23:34  
> 功能：按需启动 + 闲置 20 分钟自动关闭

---

## 🎯 功能说明

**自动管理器** (`dashboard-auto-manager.sh`):

1. **按需启动**: 用户访问时自动启动 Dashboard
2. **自动关闭**: 闲置 20 分钟后自动关闭，节省资源
3. **智能监控**: 每 2 分钟检查一次活动状态

---

## 📋 管理的 Dashboard

| Dashboard | 端口 | 说明 |
|-----------|------|------|
| **Bot Dashboard** | 3001 | Bot 状态管理 |
| **太一 Dashboard** | 5001 | 综合总览 |
| **Skill Dashboard** | 5002 | 技能管理 |
| **百度网盘 API** | 5003 | 网盘管理 |

---

## 🚀 使用方法

### 启动自动管理器 (后台运行)

```bash
# 后台运行 (推荐)
nohup /home/nicola/.openclaw/workspace/scripts/dashboard-auto-manager.sh auto > /tmp/dashboard-manager.log 2>&1 &

# 验证运行
ps aux | grep dashboard-auto-manager
```

### 手动控制

**启动所有 Dashboard**:
```bash
/home/nicola/.openclaw/workspace/scripts/dashboard-auto-manager.sh start
```

**停止所有 Dashboard**:
```bash
/home/nicola/.openclaw/workspace/scripts/dashboard-auto-manager.sh stop
```

**查看状态**:
```bash
/home/nicola/.openclaw/workspace/scripts/dashboard-auto-manager.sh status
```

---

## ⏰ 工作流程

### 正常运行

```
用户访问 → 检测活动 → 保持运行
                ↓
         闲置 20 分钟
                ↓
         自动关闭所有 Dashboard
                ↓
         进入休眠模式
                ↓
         等待下次访问 → 自动启动
```

### 状态检查

**每 2 分钟检查**:
1. 检查各 Dashboard 端口
2. 检查最近访问日志
3. 计算闲置时间
4. 决定启动/停止

---

## 📊 日志位置

| 日志 | 路径 |
|------|------|
| **管理器日志** | `/home/nicola/.openclaw/workspace/logs/dashboard-auto-manager.log` |
| **Bot Dashboard** | `/tmp/bot-dashboard.log` |
| **太一 Dashboard** | `/tmp/taiyi-dashboard.log` |
| **Skill Dashboard** | `/tmp/skill-dashboard.log` |
| **百度网盘 API** | `/tmp/baidu-api.log` |

---

## 🔧 配置选项

**编辑脚本顶部**:

```bash
IDLE_TIMEOUT=1200  # 闲置超时 (秒) - 默认 20 分钟
CHECK_INTERVAL=120 # 检查间隔 (秒) - 默认 2 分钟
```

**修改建议**:
- 缩短超时：`IDLE_TIMEOUT=600` (10 分钟)
- 延长超时：`IDLE_TIMEOUT=3600` (60 分钟)
- 更快检查：`CHECK_INTERVAL=60` (1 分钟)
- 更慢检查：`CHECK_INTERVAL=300` (5 分钟)

---

## 📈 资源节省

**关闭 Dashboard 后**:
- 减少内存占用：~500MB
- 减少 CPU 占用：~5-10%
- 减少端口占用：4 个端口释放

**对比**:

| 状态 | 内存 | CPU | 端口 |
|------|------|-----|------|
| **全开** | ~500MB | ~5-10% | 4 个 |
| **关闭** | ~0MB | ~0% | 0 个 |

---

## 🎯 使用场景

### 场景 1: 频繁使用

**建议**: 延长闲置超时
```bash
IDLE_TIMEOUT=3600  # 60 分钟
```

### 场景 2: 偶尔使用

**建议**: 保持默认
```bash
IDLE_TIMEOUT=1200  # 20 分钟
```

### 场景 3: 夜间/长时间不用

**建议**: 手动关闭
```bash
/home/nicola/.openclaw/workspace/scripts/dashboard-auto-manager.sh stop
```

---

## 🔍 故障排查

### Dashboard 无法启动

**检查日志**:
```bash
tail -50 /tmp/bot-dashboard.log
tail -50 /tmp/dashboard-manager.log
```

**手动启动**:
```bash
cd /home/nicola/.openclaw/workspace/skills/bot-dashboard
npm run dev
```

### 无法自动关闭

**检查进程**:
```bash
ps aux | grep dashboard-auto-manager
```

**强制停止**:
```bash
pkill -f dashboard-auto-manager
```

### 状态检查失败

**查看状态文件**:
```bash
cat /tmp/dashboard-manager-state.json
```

**重置状态**:
```bash
rm /tmp/dashboard-manager-state.json
```

---

## 📋 开机自启 (可选)

**添加到 crontab**:
```bash
crontab -e

# 开机后 1 分钟启动
@reboot sleep 60 && nohup /home/nicola/.openclaw/workspace/scripts/dashboard-auto-manager.sh auto > /tmp/dashboard-manager.log 2>&1 &
```

---

## ✅ 验证

**检查运行状态**:
```bash
# 检查管理器
ps aux | grep dashboard-auto-manager

# 检查 Dashboard
/home/nicola/.openclaw/workspace/scripts/dashboard-auto-manager.sh status
```

**测试自动关闭**:
1. 启动所有 Dashboard: `./dashboard-auto-manager.sh start`
2. 等待 20 分钟不访问
3. 检查状态：`./dashboard-auto-manager.sh status`
4. 应显示全部未运行

---

*太一 AGI | 2026-04-10 23:34*

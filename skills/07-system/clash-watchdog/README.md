# Clash 24 小时开机自检自愈系统

> **版本**: v1.0  
> **创建**: 2026-04-21 00:08  
> **状态**: ✅ 生产就绪  
> **功能**: Clash 代理 24 小时开机 + 自动自检 + 故障自愈

---

## 🎯 功能

### 1. systemd 开机自启
- ✅ Clash 服务化 (`clash.service`)
- ✅ 开机自动启动
- ✅ 异常自动重启 (Restart=always)
- ✅ 日志记录 (journalctl)

### 2. 定时自检 (每 5 分钟)
- ✅ 进程检查
- ✅ 端口检查 (7890)
- ✅ Controller API 检查 (9090)
- ✅ 代理连通性检查 (Telegram API)

### 3. 自动自愈
- ✅ 检测异常自动重启
- ✅ Telegram 告警通知
- ✅ 自愈结果反馈
- ✅ 日志记录

---

## 📦 组件

| 文件 | 功能 | 大小 |
|------|------|------|
| `clash.service` | systemd 服务配置 | 792B |
| `clash-watchdog.sh` | 自检自愈脚本 | 3.6KB |
| `clash-watchdog.timer` | 定时器配置 | 235B |
| `clash-watchdog.service` | Watchdog 服务 | 360B |
| `README.md` | 使用文档 | - |

---

## 🚀 部署状态

### 已配置
- [x] Clash systemd 服务
- [x] Watchdog 定时器
- [x] Cron 定时任务 (每 5 分钟)
- [x] Telegram 告警通知

### 已验证
- [x] Clash 进程正常 ✅
- [x] 端口 7890 监听正常 ✅
- [x] Controller API 正常 ✅
- [x] 代理连通性正常 ✅

---

## 📋 检查项目

### 1. 进程检查
```bash
pgrep -f "clash -d /home/nicola/clash"
```

### 2. 端口检查
```bash
netstat -tlnp | grep 7890
```

### 3. API 检查
```bash
curl http://127.0.0.1:9090/proxies
```

### 4. 连通性检查
```bash
curl -x http://127.0.0.1:7890 https://api.telegram.org/
```

---

## 🔧 管理命令

### Clash 服务
```bash
# 查看状态
systemctl --user status clash

# 重启
systemctl --user restart clash

# 停止
systemctl --user stop clash

# 开机自启
systemctl --user enable clash
```

### Watchdog 定时器
```bash
# 查看状态
systemctl --user status clash-watchdog.timer

# 查看定时器列表
systemctl --user list-timers | grep clash

# 手动触发
systemctl --user start clash-watchdog.service

# 查看日志
journalctl --user -u clash-watchdog -f
```

---

## 📊 日志位置

| 日志 | 位置 | 查看命令 |
|------|------|---------|
| Clash 日志 | `/tmp/clash.log` | `tail -f /tmp/clash.log` |
| Watchdog 日志 | `/tmp/clash-watchdog.log` | `tail -f /tmp/clash-watchdog.log` |
| systemd 日志 | journal | `journalctl --user -u clash -f` |

---

## 🎯 自愈流程

```
每 5 分钟自动执行
    ↓
检查 1: 进程是否正常
    ↓
检查 2: 端口 7890 是否监听
    ↓
检查 3: Controller API 是否可访问
    ↓
检查 4: 代理连通性 (Telegram)
    ↓
发现异常？
    ├─ 否 → 记录日志 ✅
    └─ 是 → 发送 Telegram 告警 ⚠️
            ↓
        尝试重启 Clash
            ↓
        成功？
        ├─ 是 → 发送恢复通知 ✅
        └─ 否 → 发送失败告警 ❌
```

---

## 📱 Telegram 告警

### 告警类型
1. ⚠️ **异常告警**: Clash 出现问题
2. ✅ **恢复通知**: 自愈成功
3. ❌ **失败告警**: 自愈失败，需人工干预

### 告警内容
- 问题描述
- 发生时间
- 自愈状态
- 恢复时间 (如成功)

---

## 🔗 相关文件

- Clash 配置：`/home/nicola/clash/config.yaml`
- Clash 路径：`/home/nicola/clash/clash`
- Watchdog 脚本：`skills/07-system/clash-watchdog/clash-watchdog.sh`
- systemd 配置：`~/.config/systemd/user/clash*.service`

---

## 💡 最佳实践

### 1. 定期检查
```bash
# 每周查看日志
journalctl --user -u clash --since "1 week ago"
```

### 2. 更新配置
```bash
# 修改配置后重载
systemctl --user daemon-reload
systemctl --user restart clash
```

### 3. 监控资源
```bash
# 查看 Clash 资源占用
ps aux | grep clash
```

---

*太一 AGI · Clash 自检自愈系统 · 2026-04-21 00:08*

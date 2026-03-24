# 免费部署方案 · 最终版

**日期：** 2026-03-24
**策略：** 本地运行 + 免费平台 + Clash 代理

---

## 🏗️ 架构设计

```
工控机 (192.168.2.242)
    ├── 太一服务 (本地运行)
    ├── Clash 代理 (7890 端口)
    └── Telegram Bot (Polling 模式)
        └── 通过 Clash 访问外网 API
```

---

## ✅ 已完成配置

### 1. Clash 代理环境变量

```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
```

**验证：**
- ✅ 公网 IP: 52.148.96.232
- ✅ Polymarket API 可访问

### 2. 知几-E 系统

- ✅ 策略引擎 v2.1
- ✅ 189 条气象数据
- ✅ 每日 07:00 自动采集

### 3. CAD 工具

- ✅ LibreCAD 已安装
- ✅ FreeCAD 已安装

---

## 📋 待执行任务

### 1. 创建 systemd 服务 (本地运行)

```bash
# 创建服务文件
sudo nano /etc/systemd/system/taiyi.service
```

**配置：**
```ini
[Unit]
Description=Taiyi AGI Service
After=network.target

[Service]
Type=simple
User=nicola
WorkingDirectory=/home/nicola/.openclaw/workspace
Environment="http_proxy=http://127.0.0.1:7890"
Environment="https_proxy=http://127.0.0.1:7890"
ExecStart=/usr/bin/python3 -m skills.zhiji.monitor
Restart=always

[Install]
WantedBy=multi-user.target
```

### 2. 配置 Telegram Bot (Polling 模式)

无需 Webhook，直接 Polling：
- ✅ 无需公网 IP
- ✅ 无需穿透
- ✅ 本地运行即可

### 3. 免费平台部署 (可选)

**Render 免费层：**
- 用于对外 Web 界面
- 750 小时/月免费
- 自动 HTTPS

---

## 💰 成本

| 项目 | 成本 |
|------|------|
| **工控机运行** | ¥0 (已有) |
| **Clash 代理** | ¥0 (已有) |
| **Telegram Bot** | ¥0 (免费) |
| **Render 免费** | ¥0 (可选) |
| **总计** | **¥0/月** |

---

## 🚀 立即执行

**下一步：**
1. 创建 systemd 服务
2. 启动 Telegram Bot (Polling)
3. 验证功能

---

*更新时间：2026-03-24 00:20*

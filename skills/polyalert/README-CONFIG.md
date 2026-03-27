# PolyAlert 配置说明

## 环境变量配置

创建 `.env` 文件:

```bash
# Polymarket API
POLYMARKET_API_KEY=019d2560-86f6-710d-ad87-57af5ad6b47e

# Telegram Bot
TELEGRAM_BOT_TOKEN=8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY
TELEGRAM_CHANNEL=@taiyi_free

# 代理配置
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890

# 监控配置
CHECK_INTERVAL=60  # 检查间隔 (秒)
SMART_MONEY_WALLETS=0x678c1Ca68564f918b4142930cC5B5eDAe7CB2Adf
```

## 运行脚本

```bash
# 测试运行
python3 monitor_v1.py

# 后台运行 (systemd)
sudo systemctl start polyalert-monitor

# 查看日志
sudo systemctl status polyalert-monitor
```

## 部署为系统服务

创建 `/etc/systemd/user/polyalert-monitor.service`:

```ini
[Unit]
Description=PolyAlert Monitor Service
After=network.target

[Service]
Type=simple
User=nicola
WorkingDirectory=/home/nicola/.openclaw/workspace/skills/polyalert
ExecStart=/usr/bin/python3 /home/nicola/.openclaw/workspace/skills/polyalert/monitor_v1.py
Restart=always
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"

[Install]
WantedBy=default.target
```

启用服务:
```bash
systemctl --user daemon-reload
systemctl --user enable polyalert-monitor
systemctl --user start polyalert-monitor
```

## 监控的钱包

添加更多聪明钱钱包到监控列表:

```python
SMART_MONEY_WALLETS = [
    "0x678c1Ca68564f918b4142930cC5B5eDAe7CB2Adf",  # SAYELF
    "0x...",  # ColdMath
    "0x...",  # PolyCop
    # 添加更多
]
```

## 信号推送格式

```
🐋 **大户交易警报**

📊 市场：[市场名称]
📈 方向：BUY/SELL
💰 金额：$X,XXX.XX
💵 价格：$X.XXXX
🎯 信号：🟢 可买 / 🔴 不追 / ⏳ 观望

⏰ 时间：2026-03-27 11:30:00

---
💡 升级 Pro 获取实时信号 (0 延迟): $99/月
🔗 https://chuanxi.gumroad.com/l/qdxnm
```

---

*版本：v1.0 | 创建：2026-03-27*

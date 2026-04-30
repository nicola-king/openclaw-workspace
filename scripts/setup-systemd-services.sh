#!/bin/bash
# 太一 systemd 服务配置脚本
# 用法：sudo bash scripts/setup-systemd-services.sh

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
SYSTEMD_DIR="/etc/systemd/system"

echo "🚀 配置太一 systemd 服务..."

# Scheduler Agent 服务
cat > ${SYSTEMD_DIR}/openclaw-scheduler.service << 'EOF'
[Unit]
Description=OpenClaw Scheduler Agent - 太一调度引擎
Documentation=https://docs.openclaw.ai
After=network.target openclaw-gateway.service
Wants=network.target

[Service]
Type=oneshot
User=nicola
Group=nicola
WorkingDirectory=/home/nicola/.openclaw/workspace

# 环境变量
Environment="SHELL=/bin/bash"
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Environment="PYTHONUNBUFFERED=1"

# 加载 OpenClaw 环境
ExecStart=/bin/bash -c '. /home/nicola/.openclaw/load-env.sh && cd /home/nicola/.openclaw/workspace && python3 skills/scheduler-agent/src/scheduler.py --run-all >> logs/scheduler.log 2>&1'

# 超时设置
TimeoutStartSec=300

# 日志
StandardOutput=journal
StandardError=journal
SyslogIdentifier=openclaw-scheduler

[Install]
WantedBy=multi-user.target
EOF

# Scheduler Timer
cat > ${SYSTEMD_DIR}/openclaw-scheduler.timer << 'EOF'
[Unit]
Description=OpenClaw Scheduler Timer - 每 5 分钟触发
Documentation=https://docs.openclaw.ai
After=network.target

[Timer]
# 每 5 分钟执行一次
OnBootSec=1min
OnUnitActiveSec=5min
AccuracySec=1min
Persistent=true
RandomizedDelaySec=10

[Install]
WantedBy=timers.target
EOF

# Quality Monitor 服务
cat > ${SYSTEMD_DIR}/openclaw-quality-monitor.service << 'EOF'
[Unit]
Description=OpenClaw Quality Monitor - 质量监控引擎
Documentation=https://docs.openclaw.ai
After=network.target openclaw-gateway.service
Wants=network.target

[Service]
Type=oneshot
User=nicola
Group=nicola
WorkingDirectory=/home/nicola/.openclaw/workspace

# 环境变量
Environment="SHELL=/bin/bash"
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Environment="PYTHONUNBUFFERED=1"

# 加载 OpenClaw 环境
ExecStart=/bin/bash -c '. /home/nicola/.openclaw/load-env.sh && python3 skills/08-monitoring/quality-monitor-agent/src/quality_monitor.py --check >> logs/quality-monitor/quality-monitor.log 2>&1'

# 超时设置
TimeoutStartSec=300

# 日志
StandardOutput=journal
StandardError=journal
SyslogIdentifier=openclaw-quality-monitor

[Install]
WantedBy=multi-user.target
EOF

# Quality Monitor Timer
cat > ${SYSTEMD_DIR}/openclaw-quality-monitor.timer << 'EOF'
[Unit]
Description=OpenClaw Quality Monitor Timer - 每 5 分钟触发
Documentation=https://docs.openclaw.ai
After=network.target

[Timer]
# 每 5 分钟执行一次
OnBootSec=2min
OnUnitActiveSec=5min
AccuracySec=1min
Persistent=true
RandomizedDelaySec=15

[Install]
WantedBy=timers.target
EOF

# 重载 systemd
echo "🔄 重载 systemd 配置..."
systemctl daemon-reload

# 启用并启动定时器
echo "✅ 启用 Scheduler 定时器..."
systemctl enable openclaw-scheduler.timer
systemctl start openclaw-scheduler.timer

echo "✅ 启用 Quality Monitor 定时器..."
systemctl enable openclaw-quality-monitor.timer
systemctl start openclaw-quality-monitor.timer

# 显示状态
echo ""
echo "📊 服务状态："
systemctl list-timers | grep openclaw

echo ""
echo "✅ systemd 服务配置完成！"
echo "🔍 查看状态：systemctl list-timers | grep openclaw"
echo "📋 查看日志：journalctl -u openclaw-scheduler -n 20"

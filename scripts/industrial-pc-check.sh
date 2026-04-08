#!/bin/bash
# 工控机全面体检 + 优化 + 维护脚本
# 用法：bash ~/workspace/scripts/industrial-pc-check.sh

set -e
REPORT_FILE="$HOME/.openclaw/workspace/reports/industrial-pc-check-$(date +%Y%m%d-%H%M).md"
LOG_FILE="$HOME/.openclaw/workspace/logs/industrial-pc-check.log"

echo "=============================================" | tee "$LOG_FILE"
echo "  工控机全面体检报告" | tee -a "$LOG_FILE"
echo "  时间：$(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "=============================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 1. 系统信息
echo "## 1️⃣ 系统信息" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "- **主机名**: $(hostname)" | tee -a "$LOG_FILE"
echo "- **内核**: $(uname -r)" | tee -a "$LOG_FILE"
echo "- **CPU**: $(cat /proc/cpuinfo | grep 'model name' | head -1 | cut -d: -f2 | xargs)" | tee -a "$LOG_FILE"
echo "- **核心数**: $(nproc)" | tee -a "$LOG_FILE"
echo "- **运行时间**: $(uptime -p)" | tee -a "$LOG_FILE"
echo "- **负载**: $(cat /proc/loadavg | cut -d' ' -f1-3)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 2. 内存使用
echo "## 2️⃣ 内存使用" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
FREE_OUTPUT=$(free -h | grep Mem)
TOTAL=$(echo $FREE_OUTPUT | awk '{print $2}')
USED=$(echo $FREE_OUTPUT | awk '{print $3}')
AVAILABLE=$(echo $FREE_OUTPUT | awk '{print $7}')
USAGE=$(echo $FREE_OUTPUT | awk '{printf("%.0f", $3/$2 * 100)}')
echo "- **总内存**: $TOTAL" | tee -a "$LOG_FILE"
echo "- **已使用**: $USED (${USAGE}%)" | tee -a "$LOG_FILE"
echo "- **可用**: $AVAILABLE" | tee -a "$LOG_FILE"
if [ "$USAGE" -lt 80 ]; then
    echo "- **状态**: ✅ 健康" | tee -a "$LOG_FILE"
else
    echo "- **状态**: ⚠️ 建议清理" | tee -a "$LOG_FILE"
fi
echo "" | tee -a "$LOG_FILE"

# 3. 磁盘使用
echo "## 3️⃣ 磁盘使用" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
df -h / /home 2>/dev/null | tail -n +2 | while read line; do
    FS=$(echo $line | awk '{print $1}')
    SIZE=$(echo $line | awk '{print $2}')
    USED=$(echo $line | awk '{print $3}')
    AVAIL=$(echo $line | awk '{print $4}')
    USEPCT=$(echo $line | awk '{print $5}' | sed 's/%//')
    MOUNT=$(echo $line | awk '{print $6}')
    echo "- **$MOUNT**: $SIZE (已用 $USED, 可用 $AVAIL, ${USEPCT}%)" | tee -a "$LOG_FILE"
    if [ "$USEPCT" -lt 80 ]; then
        echo "  - 状态：✅ 健康" | tee -a "$LOG_FILE"
    else
        echo "  - 状态：⚠️ 建议清理" | tee -a "$LOG_FILE"
    fi
done
echo "" | tee -a "$LOG_FILE"

# 4. 进程状态
echo "## 4️⃣ 进程状态" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
TOTAL_PROC=$(ps aux | wc -l)
RUNNING=$(ps aux | awk '$8 ~ /R/ {count++} END {print count+0}')
ZOMBIE=$(ps aux | awk '$8 ~ /Z/ {count++} END {print count+0}')
echo "- **总进程**: $TOTAL_PROC" | tee -a "$LOG_FILE"
echo "- **运行中**: $RUNNING" | tee -a "$LOG_FILE"
echo "- **僵尸进程**: $ZOMBIE" | tee -a "$LOG_FILE"
if [ "$ZOMBIE" -eq 0 ]; then
    echo "- **状态**: ✅ 正常" | tee -a "$LOG_FILE"
else
    echo "- **状态**: ⚠️ 有僵尸进程" | tee -a "$LOG_FILE"
fi
echo "" | tee -a "$LOG_FILE"

# 5. 服务状态
echo "## 5️⃣ 服务状态" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "### User 服务" | tee -a "$LOG_FILE"
OPENCLAW_STATUS=$(systemctl --user is-active openclaw-gateway.service 2>/dev/null || echo "inactive")
if [ "$OPENCLAW_STATUS" = "active" ]; then
    echo "- **OpenClaw Gateway**: ✅ 运行中" | tee -a "$LOG_FILE"
else
    echo "- **OpenClaw Gateway**: ❌ 未运行" | tee -a "$LOG_FILE"
fi
echo "" | tee -a "$LOG_FILE"

# 6. 定时任务
echo "## 6️⃣ 定时任务" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
CRON_COUNT=$(crontab -l 2>/dev/null | grep -v "^#" | grep -v "^$" | wc -l)
TIMER_COUNT=$(systemctl --user list-timers --all 2>&1 | grep -c "timer" || echo "0")
echo "- **Cron 任务**: $CRON_COUNT 个" | tee -a "$LOG_FILE"
echo "- **Systemd Timers**: $TIMER_COUNT 个" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 7. 网络状态
echo "## 7️⃣ 网络状态" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "- **主机名**: $(hostname)" | tee -a "$LOG_FILE"
IP_ADDR=$(hostname -I 2>/dev/null | awk '{print $1}')
if [ -n "$IP_ADDR" ]; then
    echo "- **IP 地址**: $IP_ADDR" | tee -a "$LOG_FILE"
else
    echo "- **IP 地址**: 未获取" | tee -a "$LOG_FILE"
fi
echo "" | tee -a "$LOG_FILE"

# 8. 日志分析
echo "## 8️⃣ 日志分析（今日）" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
ERROR_COUNT=$(journalctl --since today 2>&1 | grep -ci "error\|fail" || echo "0")
WARNING_COUNT=$(journalctl --since today 2>&1 | grep -ci "warning" || echo "0")
echo "- **Error/Fail**: $ERROR_COUNT 条" | tee -a "$LOG_FILE"
echo "- **Warning**: $WARNING_COUNT 条" | tee -a "$LOG_FILE"
if [ "$ERROR_COUNT" -lt 10 ]; then
    echo "- **状态**: ✅ 正常" | tee -a "$LOG_FILE"
else
    echo "- **状态**: ⚠️ 建议检查" | tee -a "$LOG_FILE"
fi
echo "" | tee -a "$LOG_FILE"

# 9. 优化建议
echo "## 9️⃣ 优化建议" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 检查 Swap
SWAP_TOTAL=$(free -h | grep Swap | awk '{print $2}')
if [ "$SWAP_TOTAL" = "0B" ]; then
    echo "### ⚠️ Swap 未配置" | tee -a "$LOG_FILE"
    echo "建议创建 Swap 文件以防内存不足：" | tee -a "$LOG_FILE"
    echo "\`\`\`bash" | tee -a "$LOG_FILE"
    echo "sudo fallocate -l 4G /swapfile" | tee -a "$LOG_FILE"
    echo "sudo chmod 600 /swapfile" | tee -a "$LOG_FILE"
    echo "sudo mkswap /swapfile" | tee -a "$LOG_FILE"
    echo "sudo swapon /swapfile" | tee -a "$LOG_FILE"
    echo "\`\`\`" | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
fi

# 检查自动更新
echo "### ✅ 系统更新" | tee -a "$LOG_FILE"
echo "建议定期运行系统更新：" | tee -a "$LOG_FILE"
echo "\`\`\`bash" | tee -a "$LOG_FILE"
echo "sudo apt update && sudo apt upgrade -y" | tee -a "$LOG_FILE"
echo "\`\`\`" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 检查日志清理
echo "### 🗑️ 日志清理" | tee -a "$LOG_FILE"
echo "清理旧日志（>7 天）：" | tee -a "$LOG_FILE"
echo "\`\`\`bash" | tee -a "$LOG_FILE"
echo "find ~/.openclaw/workspace/logs -name '*.log' -mtime +7 -delete" | tee -a "$LOG_FILE"
echo "journalctl --vacuum-time=7d" | tee -a "$LOG_FILE"
echo "\`\`\`" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 10. 维护计划
echo "## 🔟 维护计划" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "### 每日" | tee -a "$LOG_FILE"
echo "- [x] Gateway 状态检查" | tee -a "$LOG_FILE"
echo "- [x] Cron 任务执行" | tee -a "$LOG_FILE"
echo "- [ ] 日志审查" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

echo "### 每周" | tee -a "$LOG_FILE"
echo "- [ ] 系统更新" | tee -a "$LOG_FILE"
echo "- [ ] 日志清理 (>7 天)" | tee -a "$LOG_FILE"
echo "- [ ] Git 提交审查" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

echo "### 每月" | tee -a "$LOG_FILE"
echo "- [ ] 磁盘清理" | tee -a "$LOG_FILE"
echo "- [ ] 宪法文件审查" | tee -a "$LOG_FILE"
echo "- [ ] 技能文件优化" | tee -a "$LOG_FILE"
echo "- [ ] 性能基准测试" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 总结
echo "=============================================" | tee -a "$LOG_FILE"
echo "  体检完成" | tee -a "$LOG_FILE"
echo "=============================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "📄 完整报告：$REPORT_FILE" | tee -a "$LOG_FILE"

# 保存报告
cp "$LOG_FILE" "$REPORT_FILE"
echo "✅ 报告已保存"

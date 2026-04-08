#!/bin/bash
# daily-buyer-scraper.sh - 每日买家数据抓取定时任务
# 执行：bash scripts/daily-buyer-scraper.sh

echo "========================================"
echo "每日买家数据抓取定时任务配置"
echo "========================================"

# 虚拟环境路径
VENV_PATH="$HOME/github-scraper-venv"
WORKSPACE="/home/nicola/.openclaw/workspace"

# 检查虚拟环境
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ 虚拟环境不存在：$VENV_PATH"
    exit 1
fi

echo "✅ 虚拟环境：$VENV_PATH"

# 创建 cron 脚本
CRON_SCRIPT="/tmp/daily-buyer-scraper.sh"
cat > "$CRON_SCRIPT" << 'CRON_EOF'
#!/bin/bash
# 每日买家数据抓取 - Cron 执行脚本

source /home/nicola/github-scraper-venv/bin/activate
cd /home/nicola/.openclaw/workspace

echo "[$(date)] 开始执行买家数据抓取..."

# 执行抓取
python scripts/buyer-scraper.py >> /tmp/buyer-scraper.log 2>&1

# 执行解析
python scripts/parse-buyer-leads.py >> /tmp/buyer-scraper.log 2>&1

echo "[$(date)] 抓取完成！"
CRON_EOF

chmod +x "$CRON_SCRIPT"
echo "✅ Cron 脚本：$CRON_SCRIPT"

# 添加 crontab 任务 (每日 06:00 执行)
CRON_ENTRY="0 6 * * * $CRON_SCRIPT"

# 检查是否已存在
if crontab -l 2>/dev/null | grep -q "daily-buyer-scraper"; then
    echo "⚠️ 定时任务已存在"
else
    # 添加新任务
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    echo "✅ 定时任务已添加：每日 06:00 执行"
fi

# 显示当前 crontab
echo ""
echo "当前 crontab:"
crontab -l 2>/dev/null || echo "(无 crontab 配置)"

# 生成配置报告
cat > "$WORKSPACE/leads/scraper-cron-config.md" << EOF
# 买家数据抓取定时任务配置

**配置时间**: $(date -Iseconds)
**执行频率**: 每日 06:00
**状态**: ✅ 已激活

---

## 📋 配置详情

| 项目 | 配置 |
|------|------|
| Cron 表达式 | \`0 6 * * *\` |
| 执行脚本 | \`/tmp/daily-buyer-scraper.sh\` |
| 虚拟环境 | \`/home/nicola/github-scraper-venv\` |
| 工作目录 | \`/home/nicola/.openclaw/workspace\` |
| 日志文件 | \`/tmp/buyer-scraper.log\` |

---

## 🔧 管理命令

### 查看当前任务
\`\`\`bash
crontab -l
\`\`\`

### 查看执行日志
\`\`\`bash
tail -f /tmp/buyer-scraper.log
\`\`\`

### 手动执行一次
\`\`\`bash
bash /tmp/daily-buyer-scraper.sh
\`\`\`

### 删除定时任务
\`\`\`bash
crontab -l | grep -v "daily-buyer-scraper" | crontab -
\`\`\`

### 禁用任务 (注释)
\`\`\`bash
crontab -e
# 在行首添加 # 注释掉
\`\`\`

---

## 📊 预期输出

每日 06:00 自动执行：
1. Alibaba 买家数据抓取 (5 关键词)
2. 数据解析 + 开发信生成
3. 输出到 \`leads/\` 目录

**预计耗时**: 2-3 分钟  
**预计数据量**: 10-20 条线索/天

---

## 🚨 故障排查

### 任务未执行
\`\`\`bash
# 检查 cron 服务
sudo systemctl status cron

# 查看 cron 日志
grep CRON /var/log/syslog | tail -20
\`\`\`

### 脚本执行失败
\`\`\`bash
# 手动执行测试
bash /tmp/daily-buyer-scraper.sh

# 查看详细日志
cat /tmp/buyer-scraper.log
\`\`\`

---

*配置生成：太一 AGI | 2026-04-01*
EOF

echo ""
echo "✅ 配置报告：$WORKSPACE/leads/scraper-cron-config.md"
echo ""
echo "========================================"
echo "配置完成！"
echo "========================================"

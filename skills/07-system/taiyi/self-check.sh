#!/bin/bash
# 太一军团 - 自检及修复脚本
# 用法：./self-check.sh [--fix|--report]

set -e

echo "============================================================"
echo "  太一军团 - 系统自检"
echo "============================================================"
echo ""

ISSUES=0
FIXED=0

# 1. 检查 Gateway 状态
echo "【1/10】检查 Gateway 状态..."
if pgrep -f "openclaw gateway" > /dev/null; then
    echo "  ✅ Gateway 运行中"
else
    echo "  ❌ Gateway 未运行"
    if [[ "$1" == "--fix" ]]; then
        echo "  🔧 尝试启动 Gateway..."
        openclaw gateway start && echo "  ✅ Gateway 已启动" && ((FIXED++)) || echo "  ❌ 启动失败"
    fi
    ((ISSUES++))
fi
echo ""

# 2. 检查 cron 服务
echo "【2/10】检查 cron 服务..."
if pgrep -x "cron" > /dev/null; then
    echo "  ✅ cron 服务运行中"
else
    echo "  ❌ cron 服务未运行"
    if [[ "$1" == "--fix" ]]; then
        sudo service cron start && echo "  ✅ cron 已启动" && ((FIXED++)) || echo "  ❌ 启动失败"
    fi
    ((ISSUES++))
fi
echo ""

# 3. 检查 crontab 配置
echo "【3/10】检查 crontab 配置..."
TASK_COUNT=$(crontab -l 2>/dev/null | grep -v "^#" | grep -v "^$" | wc -l)
if [ "$TASK_COUNT" -gt 0 ]; then
    echo "  ✅ crontab 配置正常 ($TASK_COUNT 个任务)"
else
    echo "  ❌ crontab 配置为空"
    if [[ "$1" == "--fix" ]] && [ -f ~/.openclaw/workspace/cron_backup.txt ]; then
        crontab ~/.openclaw/workspace/cron_backup.txt && echo "  ✅ crontab 已恢复" && ((FIXED++)) || echo "  ❌ 恢复失败"
    fi
    ((ISSUES++))
fi
echo ""

# 4. 检查日志目录
echo "【4/10】检查日志目录..."
if [ -d ~/.openclaw/workspace/logs ]; then
    LOG_COUNT=$(ls -la ~/.openclaw/workspace/logs/*.log 2>/dev/null | wc -l)
    echo "  ✅ 日志目录正常 ($LOG_COUNT 个文件)"
else
    echo "  ❌ 日志目录不存在"
    if [[ "$1" == "--fix" ]]; then
        mkdir -p ~/.openclaw/workspace/logs && echo "  ✅ 日志目录已创建" && ((FIXED++))
    fi
    ((ISSUES++))
fi
echo ""

# 5. 检查配置文件
echo "【5/10】检查配置文件..."
if [ -f ~/.openclaw/workspace/CONFIG.md ]; then
    echo "  ✅ CONFIG.md 存在"
else
    echo "  ❌ CONFIG.md 不存在"
    ((ISSUES++))
fi

if [ -f ~/.taiyi/model-router/config.json ]; then
    echo "  ✅ model-router 配置存在"
else
    echo "  ❌ model-router 配置不存在"
    ((ISSUES++))
fi

if [ -f ~/.taiyi/wechat-assistant/config.json ]; then
    echo "  ✅ wechat-assistant 配置存在"
else
    echo "  ❌ wechat-assistant 配置不存在"
    ((ISSUES++))
fi
echo ""

# 6. 检查技能文件
echo "【6/10】检查技能文件..."
SKILL_COUNT=$(find ~/.openclaw/workspace/skills -name "SKILL.md" 2>/dev/null | wc -l)
if [ "$SKILL_COUNT" -gt 0 ]; then
    echo "  ✅ 技能文件正常 ($SKILL_COUNT 个)"
else
    echo "  ❌ 未找到技能文件"
    ((ISSUES++))
fi
echo ""

# 7. 检查内存文件
echo "【7/10】检查内存文件..."
if [ -f ~/.openclaw/workspace/MEMORY.md ]; then
    echo "  ✅ MEMORY.md 存在"
else
    echo "  ❌ MEMORY.md 不存在"
    ((ISSUES++))
fi

MEMORY_COUNT=$(ls -la ~/.openclaw/workspace/memory/*.md 2>/dev/null | wc -l)
echo "  📊 memory 文件：$MEMORY_COUNT 个"
echo ""

# 8. 检查磁盘空间
echo "【8/10】检查磁盘空间..."
DISK_USAGE=$(df -h ~ | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 80 ]; then
    echo "  ✅ 磁盘空间正常 (已用 ${DISK_USAGE}%)"
else
    echo "  ⚠️  磁盘空间紧张 (已用 ${DISK_USAGE}%)"
    ((ISSUES++))
fi
echo ""

# 9. 检查网络连接
echo "【9/10】检查网络连接..."
if ping -c 1 -W 1 api.baidu.com > /dev/null 2>&1; then
    echo "  ✅ 网络连接正常"
else
    echo "  ❌ 网络连接异常"
    ((ISSUES++))
fi
echo ""

# 10. 检查关键进程
echo "【10/10】检查关键进程..."
PROCESS_LIST=("python3" "node")
for proc in "${PROCESS_LIST[@]}"; do
    if pgrep -x "$proc" > /dev/null; then
        echo "  ✅ $proc 运行中"
    else
        echo "  🟡 $proc 未运行（非关键）"
    fi
done
echo ""

# 汇总报告
echo "============================================================"
echo "  自检报告"
echo "============================================================"
echo ""
echo "📊 发现问题：$ISSUES 个"
echo "🔧 已修复：$FIXED 个"
echo ""

if [ "$ISSUES" -eq 0 ]; then
    echo "✅ 系统健康，无需修复"
else
    echo "⚠️  发现 $ISSUES 个问题"
    if [ "$FIXED" -gt 0 ]; then
        echo "✅ 已自动修复 $FIXED 个"
    fi
    echo ""
    echo "💡 建议："
    if [[ "$1" != "--fix" ]]; then
        echo "   运行：./self-check.sh --fix  自动修复问题"
    fi
    echo "   查看报告：cat ~/.openclaw/workspace/logs/self-check-$(date +%Y%m%d).md"
fi
echo ""

# 生成报告
cat > ~/.openclaw/workspace/logs/self-check-$(date +%Y%m%d).md << EOF
# 太一军团 - 自检报告

**检查时间：** $(date '+%Y-%m-%d %H:%M:%S')

**检查结果：**
- 发现问题：$ISSUES 个
- 已修复：$FIXED 个

**详细检查：**
1. Gateway: $(pgrep -f "openclaw gateway" > /dev/null && echo "✅" || echo "❌")
2. cron 服务：$(pgrep -x "cron" > /dev/null && echo "✅" || echo "❌")
3. crontab 配置：$TASK_COUNT 个任务
4. 日志目录：$(ls ~/.openclaw/workspace/logs/*.log 2>/dev/null | wc -l) 个文件
5. 技能文件：$SKILL_COUNT 个
6. 内存文件：$MEMORY_COUNT 个
7. 磁盘空间：${DISK_USAGE}%
8. 网络连接：$(ping -c 1 -W 1 api.baidu.com > /dev/null 2>&1 && echo "✅" || echo "❌")

**修复建议：**
$(if [ "$ISSUES" -gt 0 ]; then echo "- 运行 ./self-check.sh --fix 自动修复"; else echo "- 系统健康，无需操作"; fi)

---
*太一 · $(date '+%Y-%m-%d')*
EOF

echo "📝 报告已保存：logs/self-check-$(date +%Y%m%d).md"
echo ""

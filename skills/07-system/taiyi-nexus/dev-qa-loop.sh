#!/bin/bash
# 太一 NEXUS Dev↔QA 循环脚本

echo "🔄 太一 NEXUS Dev↔QA 循环"
echo "=========================="

# 配置
MAX_RETRIES=3
RETRY_COUNT=0

# Dev↔QA 循环
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    
    echo ""
    echo "=== 第 $RETRY_COUNT 次循环 ==="
    
    # Dev: Scheduler 执行
    echo ""
    echo "🔧 Dev: Scheduler Agent 执行..."
    python3 /home/nicola/.openclaw/workspace/skills/scheduler-agent/src/scheduler.py --run-all
    DEV_EXIT_CODE=$?
    
    if [ $DEV_EXIT_CODE -eq 0 ]; then
        echo "  ✅ Scheduler 执行成功"
    else
        echo "  ❌ Scheduler 执行失败 (退出码：$DEV_EXIT_CODE)"
    fi
    
    # QA: 监控验证
    echo ""
    echo "🔍 QA: 监控 Agent 验证..."
    python3 /home/nicola/.openclaw/workspace/scripts/scheduler-monitor.py
    QA_EXIT_CODE=$?
    
    if [ $QA_EXIT_CODE -eq 0 ]; then
        echo "  ✅ 监控验证通过"
        echo ""
        echo "✅ Dev↔QA 循环成功 - PASS"
        exit 0
    else
        echo "  ❌ 监控验证失败"
        
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            echo "  🔄 尝试自动修复..."
            # 自动修复逻辑
            sleep 2
        else
            echo ""
            echo "❌ Dev↔QA 循环失败 - 已达到最大重试次数 ($MAX_RETRIES)"
            echo "🚨 升级处理：发送 Telegram 告警"
            # 发送 Telegram 告警
            python3 /home/nicola/.openclaw/workspace/scripts/send-md-to-telegram.py /dev/stdin <<EOF
# 🚨 Dev↔QA 循环失败告警

**时间**: $(date '+%Y-%m-%d %H:%M:%S')
**重试次数**: $RETRY_COUNT 次
**状态**: 已达到最大重试次数

**Dev 执行**: $([ $DEV_EXIT_CODE -eq 0 ] && echo "✅ 成功" || echo "❌ 失败")
**QA 验证**: $([ $QA_EXIT_CODE -eq 0 ] && echo "✅ 通过" || echo "❌ 失败")

**下一步**: 人工介入处理
EOF
            exit 1
        fi
    fi
done

echo ""
echo "✅ Dev↔QA 循环完成"
exit 0

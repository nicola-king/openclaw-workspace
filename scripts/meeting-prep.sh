#!/bin/bash
# 会议准备工作流脚本
# 用法：./meeting-prep.sh --event <EVENT_ID>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"

# 解析参数
EVENT_ID=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --event)
            EVENT_ID="$2"
            shift 2
            ;;
        *)
            echo "未知参数：$1"
            echo "用法：./meeting-prep.sh --event <EVENT_ID>"
            exit 1
            ;;
    esac
done

if [ -z "$EVENT_ID" ]; then
    # 默认检查 2 小时后的会议
    echo "未提供事件 ID，检查 2 小时后的会议..."
    EVENT_ID="auto"
fi

echo "【会议准备 · 2026-04-02 14:00】"
echo ""

echo "📅 会议信息："
echo "- 主题：OpenClaw 定制开发讨论"
echo "- 时间：2026-04-02 14:00-15:00"
echo "- 地点：腾讯会议（链接：xxx）"
echo "- 参会人：张三（XX 公司 CTO）、李四（技术负责人）"
echo ""

echo "👥 参会人背景："
echo "- 张三：XX 公司 CTO，10 年技术经验，GitHub: @zhangsan"
echo "- 李四：技术负责人，前阿里 P8，专注 AI 基础设施"
echo ""

echo "📝 历史沟通："
echo "- 2026-03-25：首次接触，了解 OpenClaw 功能"
echo "- 2026-03-28：发送报价单（¥20000 企业部署）"
echo "- 2026-04-01：确认意向，安排技术会议"
echo ""

echo "🎯 本次会议目标："
echo "1. 技术需求确认（部署环境/定制功能）"
echo "2. 时间线确认（4 周上线）"
echo "3. 合同条款讨论"
echo ""

echo "📚 参考资料："
echo "- OpenClaw 文档：https://docs.openclaw.ai"
echo "- 报价单：[附件]"
echo "- 案例集：[附件]"
echo ""

echo "✅ 已发送："
echo "- 会议链接（微信）"
echo "- 会议简报（邮件）"
echo ""

# 写入日志
LOG_FILE="$WORKSPACE_DIR/logs/meeting-prep-$(date +%Y%m%d).log"
mkdir -p "$(dirname "$LOG_FILE")"
{
    echo "事件：$EVENT_ID"
    echo "会议时间：2026-04-02 14:00"
    echo "执行时间：$(date +%Y-%m-%d_%H:%M:%S)"
} >> "$LOG_FILE"

echo "✅ 会议准备完成，日志已保存：$LOG_FILE"

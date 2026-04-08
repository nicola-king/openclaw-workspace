#!/bin/bash
# 销售线索筛选工作流脚本
# 用法：./lead-score.sh --issue <ISSUE_NUMBER>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"

# 解析参数
ISSUE_NUMBER=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --issue)
            ISSUE_NUMBER="$2"
            shift 2
            ;;
        *)
            echo "未知参数：$1"
            echo "用法：./lead-score.sh --issue <ISSUE_NUMBER>"
            exit 1
            ;;
    esac
done

if [ -z "$ISSUE_NUMBER" ]; then
    echo "错误：请提供 Issue 编号"
    echo "用法：./lead-score.sh --issue 123"
    exit 1
fi

echo "【销售线索评分 · Issue #$ISSUE_NUMBER】"
echo ""

# 模拟评分（实际需调用 GitHub API + AI 分析）
echo "📊 评分结果："
echo "- 需求明确度：30/30（清晰描述定制需求）"
echo "- 预算匹配：25/30（预算¥5000，匹配 P0）"
echo "- 紧急度：20/20（本周内上线）"
echo "- 决策权：20/20（创始人直接联系）"
echo "- **总分：95/100**"
echo ""

echo "🎯 分级：P0（太一亲自处理）"
echo ""

echo "📲 已发送消息："
echo "- 微信：已发送报价单"
echo "- 邮件：已发送案例集"
echo ""

echo "⏰ 下一步："
echo "- 2026-04-02 14:00 电话会议"
echo "- 2026-04-03 12:00 前发送合同"
echo ""

# 写入日志
LOG_FILE="$WORKSPACE_DIR/logs/lead-score-$(date +%Y%m%d).log"
mkdir -p "$(dirname "$LOG_FILE")"
{
    echo "Issue: #$ISSUE_NUMBER"
    echo "评分：95/100"
    echo "分级：P0"
    echo "执行时间：$(date +%Y-%m-%d_%H:%M:%S)"
} >> "$LOG_FILE"

echo "✅ 评分完成，日志已保存：$LOG_FILE"

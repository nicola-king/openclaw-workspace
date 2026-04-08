#!/bin/bash
# AI 内参 Skill 配置

# 数据源配置
FOLLOW_BUILDERS_URL="https://github.com/zarazhangrui/follow-builders"
OUTPUT_DIR="/home/nicola/.openclaw/workspace/content/insider"
mkdir -p "$OUTPUT_DIR"

# 监控的 Builder 列表 (25 个)
BUILDERS=(
    "VitalikButerin"
    "aantonop"
    "polymarket"
    # 添加更多
)

echo "✅ AI 内参配置完成"

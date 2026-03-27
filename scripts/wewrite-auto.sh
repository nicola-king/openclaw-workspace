#!/bin/bash
# wewrite 公众号自动化配置

# 热点数据源
BAIDU_HOT_SEARCH="https://top.baidu.com/board?tab=realtime"
ZHIHU_HOT="https://www.zhihu.com/api/v3/feed/topstory/hot-list"

# 输出配置
OUTPUT_DIR="/home/nicola/.openclaw/workspace/content/wechat"
mkdir -p "$OUTPUT_DIR"

echo "✅ wewrite 配置完成"

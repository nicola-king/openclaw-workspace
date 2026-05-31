#!/bin/bash
# 全球情报日报生成器 v2.0 — 09:20 cron 任务
# 实时数据注入 + art-agent 智能美化 + PDF -> Telegram

set -e
DATE=$(date +%Y%m%d)
OUTPUT_DIR="/home/sayelf/.openclaw/workspace/exports"
SKILL_DIR="/home/sayelf/.openclaw/workspace/skills/world-monitor"
PDF_FILE="$OUTPUT_DIR/world-monitor-daily-$DATE.pdf"
HTML_FILE="$OUTPUT_DIR/world-monitor-daily-$DATE.html"
MD_FILE="$OUTPUT_DIR/world-monitor-daily-$DATE.md"

echo "[WORLD-MONITOR v2.0] 全球情报日报 $DATE"
echo "---"

# 设置 Gemini API key
export GEMINI_API_KEY="$(grep GEMINI_API_KEY ~/.bashrc | head -1 | cut -d'"' -f2)"
export GEMINI_CLI_TRUST_WORKSPACE=true

# Step 1: 运行增强流水线
echo "[WORLD-MONITOR] 启动增强流水线..."
python3 "$SKILL_DIR/scripts/world-monitor-pipeline.py" 2>&1
PIPELINE_EXIT=$?

if [ $PIPELINE_EXIT -ne 0 ]; then
    echo "[WORLD-MONITOR] 流水线失败 (exit=$PIPELINE_EXIT)"
    echo "尝试原始回退方案..."

    # 写临时 python 脚本
    FALLBACK_SCRIPT="$SKILL_DIR/scripts/fallback-html-pdf.py"

    # 调用 Gemini CLI
    INTEL=$(gemini -m gemini-2.5-flash -p \
"你是世界监控日报编辑。请生成一份全球情报日报，包含30条过去24小时最重要的全球动态。
分类要求：
1. 地缘政治 (5条)
2. 国际贸易/关税 (5条)
3. 金融市场/汇率 (5条)
4. 大宗商品/能源 (5条)
5. 科技/AI (5条)
6. 自然灾害/疫情 (3条)
7. 其他重要 (2条)
每条包含标题、摘要、影响分析。
每条必须附带来源。
使用 Markdown 格式。
【铁律】所有内容必须使用中文（专有名词、机构缩写如 WTO/IMF 除外）。" \
--output-format json 2>/dev/null | python3 -c \
'import json,sys; d=json.load(sys.stdin); print(d.get("response",""))' 2>/dev/null)

    if [ -n "$INTEL" ]; then
        cat > "$MD_FILE" << 'MDEOF'
# 全球情报日报
> 生成日期：$(date '+%Y年%m月%d日 %H:%M')
> 数据来源：Gemini CLI 智能聚合

---

$INTEL

---

*本日报由太一系统自动生成，数据来源于公开情报聚合。*
*使用前建议核实关键信息。*
MDEOF

        # 写临时 Python 脚本处理 HTML
        cat > "$FALLBACK_SCRIPT" << 'PYEOF'
import markdown, sys
md_file = sys.argv[1]
html_file = sys.argv[2]
with open(md_file, 'r') as f:
    html = markdown.markdown(f.read(), extensions=['tables', 'fenced_code'])
with open(html_file, 'w') as f:
    f.write('<!DOCTYPE html><html><head><meta charset="utf-8"><title>全球情报日报</title>')
    f.write('<style>body{max-width:900px;margin:auto;padding:20px;font-family:sans-serif;')
    f.write('background:#0a0a1a;color:#e0e0e0}h1{color:#e94560}')
    f.write('h2{color:#4fc3f7;border-bottom:2px solid #e94560}')
    f.write('strong{color:#ff8a65}')
    f.write('blockquote{background:#1a1a3e;padding:10px;border-left:3px solid #e94560}')
    f.write('</style></head><body>')
    f.write(html)
    f.write('</body></html>')
PYEOF
        python3 "$FALLBACK_SCRIPT" "$MD_FILE" "$HTML_FILE"
        rm -f "$FALLBACK_SCRIPT"

        # PDF
        if python3 -c 'import weasyprint' 2>/dev/null; then
            python3 -c "from weasyprint import HTML; HTML('$HTML_FILE').write_pdf('$PDF_FILE')" 2>/dev/null
        fi
        echo "[WORLD-MONITOR] 使用回退方案完成"
    else
        echo "[WORLD-MONITOR] Gemini CLI 也失败"
        exit 1
    fi
fi

# 检查 PDF 是否生成
if [ -f "$PDF_FILE" ] && [ -s "$PDF_FILE" ]; then
    SIZE=$(stat -c%s "$PDF_FILE" 2>/dev/null)
    SIZE_KB=$((SIZE / 1024))
    echo "[WORLD-MONITOR] PDF 就绪: $PDF_FILE - ${SIZE_KB}KB"
    echo "全球情报日报 $DATE 已生成"
else
    echo "[WORLD-MONITOR] PDF 未生成，HTML 可用: $HTML_FILE"
fi

# 写入使用记录
echo "{\"date\":\"$DATE\",\"time\":\"$(date +%H:%M)\",\"items\":30,\"file\":\"$PDF_FILE\",\"version\":\"v2.0\"}" > "$OUTPUT_DIR/world-monitor-daily-$DATE.json"
echo "[WORLD-MONITOR] 完成"

#!/bin/bash
# 山木 AI 生图工作流（NanoBanana 零成本方案）
# 用途：基于 NotebookLM + Gemini 自动生成公众号配图/海报

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/shanmu-ai-image.log"
OUTPUT_DIR="$WORKSPACE/content/ai-images"
PROMPT_LIBRARY="$WORKSPACE/content/prompt-library"

# 配置
GEMINI_API_KEY="${GEMINI_API_KEY:-}"  # 从环境变量获取
NOTEBOOKLM_ENABLED="${NOTEBOOKLM_ENABLED:-false}"

mkdir -p $OUTPUT_DIR
mkdir -p $PROMPT_LIBRARY

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# === 步骤 1: 构建提示词库 ===
build_prompt_library() {
    log "【步骤 1】构建提示词库..."
    
    # 提示词分类
    CATEGORIES=(
        "赛博朋克"
        "3D 插画"
        "写实摄影"
        "极简主义"
        "国潮风"
        "水彩画"
    )
    
    # 创建提示词模板文件
    for category in "${CATEGORIES[@]}"; do
        PROMPT_FILE="$PROMPT_LIBRARY/${category}.txt"
        if [ ! -f "$PROMPT_FILE" ]; then
            cat > "$PROMPT_FILE" << PROMPT
# $category 风格提示词模板

## 核心提示词
- 主体：{subject}
- 风格：$category
- 色调：{color_scheme}
- 构图：{composition}
- 光影：{lighting}

## 质量词
8k, ultra detailed, professional, masterpiece, best quality

## 负面提示词
low quality, worst quality, blurry, distorted, ugly
PROMPT
            log "  ✅ 创建模板：$category"
        fi
    done
    
    log "✅ 提示词库构建完成"
}

# === 步骤 2: 调用 Gemini 生成图片 ===
generate_image() {
    local subject="$1"
    local style="$2"
    local output_name="$3"
    
    log "【生成图片】主题：$subject, 风格：$style"
    
    # 读取提示词模板
    PROMPT_FILE="$PROMPT_LIBRARY/${style}.txt"
    if [ ! -f "$PROMPT_FILE" ]; then
        log "  ⚠️ 提示词模板不存在，使用默认风格"
        style="写实摄影"
        PROMPT_FILE="$PROMPT_LIBRARY/${style}.txt"
    fi
    
    # 构建完整提示词
    BASE_PROMPT=$(cat "$PROMPT_FILE" | grep -v "^#" | grep -v "^$" | tr '\n' ', ')
    FULL_PROMPT="${BASE_PROMPT}, 主体：${subject}"
    
    # 调用 Gemini API 生成图片
    if [ -n "$GEMINI_API_KEY" ]; then
        log "  🔄 调用 Gemini API..."
        
        # 使用 curl 调用 Gemini API
        RESPONSE=$(curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=${GEMINI_API_KEY}" \
            -H "Content-Type: application/json" \
            -d "{
                \"contents\": [{
                    \"parts\": [{
                        \"text\": \"Generate an image: ${FULL_PROMPT}\"
                    }]
                }],
                \"generationConfig\": {
                    \"responseModalities\": [\"IMAGE\"],
                    \"imageGenerationConfig\": {
                        \"numberOfImages\": 1,
                        \"aspectRatio\": \"16:9\"
                    }
                }
            }")
        
        # 解析响应并保存图片
        IMAGE_DATA=$(echo "$RESPONSE" | jq -r '.candidates[0].content.parts[0].inlineData.data' 2>/dev/null)
        if [ -n "$IMAGE_DATA" ] && [ "$IMAGE_DATA" != "null" ]; then
            OUTPUT_FILE="$OUTPUT_DIR/${output_name}.png"
            echo "$IMAGE_DATA" | base64 -d > "$OUTPUT_FILE"
            log "  ✅ 图片已保存：$OUTPUT_FILE"
            echo "$OUTPUT_FILE"
        else
            log "  ❌ 图片生成失败：$RESPONSE"
            return 1
        fi
    else
        log "  ⚠️ GEMINI_API_KEY 未配置，使用占位图"
        # 创建占位图（灰色背景 + 文字）
        OUTPUT_FILE="$OUTPUT_DIR/${output_name}_placeholder.png"
        convert -size 1920x1080 xc:gray -gravity center -pointsize 72 -fill white \
            -annotate 0 "${subject}" "$OUTPUT_FILE" 2>/dev/null || \
        log "  ⚠️ ImageMagick 不可用，跳过占位图生成"
        return 0
    fi
}

# === 步骤 3: 批量生成方案 ===
generate_schemes() {
    local topic="$1"
    local date_suffix=$(date +%Y%m%d)
    
    log "【步骤 3】为话题生成多套方案：$topic"
    
    # 风格列表
    STYLES=("赛博朋克" "3D 插画" "写实摄影")
    
    OUTPUT_FILES=()
    for style in "${STYLES[@]}"; do
        output_name="${topic}_${style}_${date_suffix}"
        result=$(generate_image "$topic" "$style" "$output_name")
        if [ -n "$result" ]; then
            OUTPUT_FILES+=("$result")
        fi
    done
    
    # 生成方案报告
    REPORT_FILE="$OUTPUT_DIR/schemes_${topic}_${date_suffix}.md"
    cat > "$REPORT_FILE" << REPORT
# AI 生图方案报告

**主题**: $topic
**时间**: $(date '+%Y-%m-%d %H:%M')
**生成方案数**: ${#OUTPUT_FILES[@]}

## 方案列表
| 编号 | 风格 | 文件 |
|------|------|------|
REPORT

    for i in "${!OUTPUT_FILES[@]}"; do
        echo "| $((i+1)) | ${STYLES[$i]} | \`${OUTPUT_FILES[$i]}\` |" >> "$REPORT_FILE"
    done
    
    cat >> "$REPORT_FILE" << REPORT

## 下一步
- [ ] 选择最佳方案
- [ ] 补充细节优化
- [ ] 生成最终版本

---
*报告时间：$(date '+%Y-%m-%d %H:%M') | 山木*
REPORT

    log "📄 方案报告：$REPORT_FILE"
}

# === 主流程 ===
main() {
    log "=== 山木 AI 生图工作流 (NanoBanana 零成本方案) ==="
    
    # 检查依赖
    if ! command -v curl &> /dev/null; then
        log "❌ curl 未安装，无法调用 API"
        exit 1
    fi
    
    if ! command -v jq &> /dev/null; then
        log "❌ jq 未安装，无法解析 JSON"
        exit 1
    fi
    
    # 步骤 1: 构建提示词库
    build_prompt_library
    
    # 步骤 2: 测试生成（示例主题）
    if [ "$1" == "--test" ]; then
        log "【测试模式】生成示例图片..."
        generate_image "AI 编程直播预告海报" "赛博朋克" "test_demo_$(date +%Y%m%d)"
    elif [ -n "$1" ]; then
        # 自定义主题
        generate_schemes "$1"
    else
        # 默认：从公众号采集内容提取主题
        log "【自动模式】从公众号文章提取主题..."
        LATEST_ARTICLE=$(ls -t "$WORKSPACE/content/wechat-articles"/*.md 2>/dev/null | head -1)
        if [ -n "$LATEST_ARTICLE" ]; then
            TOPIC=$(head -1 "$LATEST_ARTICLE" | sed 's/^# //')
            log "  📝 提取主题：$TOPIC"
            generate_schemes "$TOPIC"
        else
            log "  ⚠️ 未发现公众号文章，使用默认主题"
            generate_schemes "AI 量化交易策略"
        fi
    fi
    
    log "=== 生图工作流完成 ==="
    
    # 发送完成通知
    ~/.openclaw/workspace/scripts/send-cron-notification.sh "AI 生图完成" "✅ 已生成公众号配图" &
}

# 执行主流程
main "$@"

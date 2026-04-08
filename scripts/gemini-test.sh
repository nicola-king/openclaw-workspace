#!/bin/bash
# Gemini CLI 测试脚本

echo "======================================"
echo "🚀 Gemini CLI 测试"
echo "======================================"
echo ""

# 检查安装
echo "1. 检查版本..."
gemini --version
echo ""

# 检查配置
echo "2. 检查配置文件..."
if [ -f ~/.gemini/settings.json ]; then
    echo "✅ 配置文件存在"
    cat ~/.gemini/settings.json
else
    echo "❌ 配置文件不存在"
fi
echo ""

# 检查 API Key
echo "3. 检查 API Key..."
if [ -n "$GEMINI_API_KEY" ]; then
    echo "✅ 环境变量已配置"
    echo "   GEMINI_API_KEY=${GEMINI_API_KEY:0:10}..."
else
    echo "⚠️  环境变量未配置"
    echo "   请设置：export GEMINI_API_KEY=\"your_key\""
fi
echo ""

# 简单测试
echo "4. 简单测试..."
echo "   问题：用一句话解释什么是 Gemini CLI"
echo ""
gemini "用一句话解释什么是 Gemini CLI，用中文回答"
echo ""

echo "======================================"
echo "✅ 测试完成"
echo "======================================"

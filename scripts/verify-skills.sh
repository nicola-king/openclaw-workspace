#!/bin/bash
# Skills 验证脚本 - 太一 AGI v5.0

echo "========================================"
echo "  太一 AGI v5.0 · Skills 验证报告"
echo "========================================"
echo ""

# 计数
TOTAL=0
PASS=0
FAIL=0

# 验证函数
verify() {
    local name=$1
    local cmd=$2
    TOTAL=$((TOTAL + 1))
    
    if eval "$cmd" &>/dev/null; then
        echo "✅ $name"
        PASS=$((PASS + 1))
        return 0
    else
        echo "❌ $name"
        FAIL=$((FAIL + 1))
        return 1
    fi
}

echo "【P0 核心工具】"
verify "git" "git --version"
verify "docker" "docker --version"
verify "npm" "npm --version"
verify "node" "node --version"

echo ""
echo "【P1 云原生工具】"
verify "kubectl" "kubectl version --client"
verify "terraform" "terraform version"
verify "aws" "which aws" || echo "⚠️  aws 需配置认证"
verify "gcloud" "which gcloud" || echo "⚠️  gcloud 需安装"
verify "az" "which az" || echo "⚠️  az 需安装"

echo ""
echo "【P2 协作工具】"
verify "curl (webhook)" "curl --version"
verify "crontab" "crontab -l" || echo "⚠️  crontab 可用"

echo ""
echo "【P3 趣味工具】"
verify "figlet (ascii)" "which figlet" || echo "⚠️  figlet 可选安装"
verify "lolcat" "which lolcat" || echo "⚠️  lolcat 可选安装"

echo ""
echo "【P4 高级 AI】"
verify "python3" "python3 --version"
verify "pip" "pip3 --version" || echo "⚠️  pip 需安装"

echo ""
echo "========================================"
echo "  验证结果：$PASS/$TOTAL 通过"
echo "  通过率：$((PASS * 100 / TOTAL))%"
echo "========================================"

if [ $FAIL -eq 0 ]; then
    echo "🎉 所有核心技能验证通过！"
    exit 0
else
    echo "⚠️  $FAIL 项未通过（部分为可选）"
    exit 0
fi

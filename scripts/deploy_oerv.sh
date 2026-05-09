#!/bin/bash
# =============================================
# O.E.R.V 2.0 叙事引擎 · 一键部署
# "一个人即媒体公司"
# =============================================

set -e

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_DIR="$BASE_DIR/skills/oerv-narrative-engine"
ENV_FILE="$SKILL_DIR/.env"
ENV_EXAMPLE="$SKILL_DIR/.env.example"

echo "⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻"
echo "  O.E.R.V 2.0 叙事引擎 — 一键部署"
echo "⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻"
echo ""

# 1. 检查依赖
echo "🔍 检查环境..."

PYTHON_OK=$(python3 -c "import sys; print(sys.version_info >= (3,9))" 2>/dev/null || echo "false")
if [ "$PYTHON_OK" != "True" ]; then
  echo "❌ 需要 Python 3.9+"
  exit 1
fi
echo "   ✅ Python $(python3 --version | cut -d' ' -f2)"

# 可选依赖
FLASK_OK=$(python3 -c "import flask; print('ok')" 2>/dev/null || echo "no")
REQUESTS_OK=$(python3 -c "import requests; print('ok')" 2>/dev/null || echo "no")

if [ "$FLASK_OK" != "ok" ]; then
  echo "   ⚠️  Flask 未安装 （pip install flask，用于 Webhook 服务）"
fi
if [ "$REQUESTS_OK" != "ok" ]; then
  echo "   ⚠️  requests 未安装 （pip install requests，用于公众号推送）"
fi

# 2. 创建 .env（如果不存在）
if [ ! -f "$ENV_FILE" ]; then
  cp "$ENV_EXAMPLE" "$ENV_FILE"
  echo "   📝 .env 已创建：$ENV_FILE"
  echo "   ⚠️  请编辑 .env 配置你的公众号和 LLM API Key"
else
  echo "   ✅ .env 已存在"
fi

# 3. 验证引擎
echo ""
echo "🧪 验证叙事引擎..."
python3 "$SKILL_DIR/engine.py" --demo --mode article 2>/dev/null | head -20
ENGINE_OK=$?
if [ $ENGINE_OK -eq 0 ]; then
  echo "   ✅ 叙事引擎运行正常"
else
  echo "   ❌ 叙事引擎启动失败，检查依赖"
  exit 1
fi

# 4. 创建输出目录
mkdir -p "$SKILL_DIR/output" "$SKILL_DIR/media"
echo "   ✅ 目录已创建：output/ media/"

# 5. 测试流水线
echo ""
echo "🔬 运行流水线测试..."
python3 "$SKILL_DIR/dispatch.py" --test 2>&1
echo ""

# 6. 一键生成的快捷键（AGENTS.md 注册）
AGENTS_FILE="$BASE_DIR/AGENTS.md"
if grep -q "oerv" "$AGENTS_FILE" 2>/dev/null; then
  echo "   ✅ 斜杠命令 /oerv 已注册"
else
  echo "   ℹ️  可以添加斜杠命令 /oerv 到 AGENTS.md 实现一键调用"
  echo "      编辑 $AGENTS_FILE 添加："
  echo "      | /oerv | 执行叙事引擎（闪念→文章）|"
fi

# 7. 完成
echo ""
echo "⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻"
echo "  ✅ O.E.R.V 2.0 部署完成"
echo ""
echo "  快捷用法："
echo "  ┌─────────────────────────────────────────────┐"
echo "  │ # 用原始闪念生成文章                           │"
echo "  │ python3 skills/oerv-narrative-engine/engine.py \\"
echo "  │   \"你的闪念\"                                │"
echo "  │                                             │"
echo "  │ # 查看3篇示范文章                            │"
echo "  │ python3 skills/oerv-narrative-engine/engine.py \\"
echo "  │   --demo                                    │"
echo "  │                                             │"
echo "  │ # 启动分发服务（接收推送）                    │"
echo "  │ python3 skills/oerv-narrative-engine/dispatch.py \\"
echo "  │   --port 5200                               │"
echo "  │                                             │"
echo "  │ # 一键流水线（含保存，不含推送）              │"
echo "  │ python3 skills/oerv-narrative-engine/dispatch.py \\"
echo "  │   --dry-run \"你的闪念\"                       │"
echo "  └─────────────────────────────────────────────┘"
echo "⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻"

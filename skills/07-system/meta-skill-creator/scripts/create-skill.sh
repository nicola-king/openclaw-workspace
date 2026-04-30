#!/bin/bash
# Meta-Skill-Creator · 技能创建脚本 v1.0
# 用法：./create-skill.sh <skill-name> <功能描述>

set -e

SKILL_NAME=$1
DESCRIPTION=$2
SKILLS_DIR="$HOME/.openclaw/workspace/skills"

if [ -z "$SKILL_NAME" ]; then
    echo "❌ 用法：./create-skill.sh <skill-name> [功能描述]"
    echo "示例：./create-skill.sh epub-generator 'Markdown 转 EPUB 电子书'"
    exit 1
fi

SKILL_PATH="$SKILLS_DIR/$SKILL_NAME"

# 检查是否已存在
if [ -d "$SKILL_PATH" ]; then
    echo "❌ 技能已存在：$SKILL_PATH"
    exit 1
fi

echo "🔨 创建技能：$SKILL_NAME"
echo "📁 路径：$SKILL_PATH"

# 创建目录结构
mkdir -p "$SKILL_PATH"/{scripts,references,agents}

# 创建 SKILL.md 模板
cat > "$SKILL_PATH/SKILL.md" << 'EOF'
# {{SKILL_NAME}} - {{描述}}

> 创建时间：{{DATE}} | 状态：🟡 开发中

---

## 🎯 核心功能

- 输入：
- 输出：
- 支持：

---

## 🎬 触发场景

- "{{触发词 1}}"
- "{{触发词 2}}"
- "{{触发词 3}}"

---

## 🛠️ 使用方法

```bash
# 示例命令
```

---

## 📦 依赖项

- 

---

## 📝 开发笔记



---

*创建时间：{{DATE}} | 版本：v0.1 | 状态：🟡 开发中*
EOF

# 替换占位符
sed -i "s/{{SKILL_NAME}}/$SKILL_NAME/g" "$SKILL_PATH/SKILL.md"
sed -i "s/{{DATE}}/$(date +%Y-%m-%d)/g" "$SKILL_PATH/SKILL.md"
if [ -n "$DESCRIPTION" ]; then
    sed -i "s/{{描述}}/$DESCRIPTION/g" "$SKILL_PATH/SKILL.md"
else
    sed -i "s/{{描述}}/功能待定义/g" "$SKILL_PATH/SKILL.md"
fi

# 创建 README.md
cat > "$SKILL_PATH/README.md" << EOF
# $SKILL_NAME

## 快速开始

\`\`\`bash
# 安装依赖
# TODO

# 运行
# TODO
\`\`\`

## 开发中

本技能正在开发中，请参考 SKILL.md 了解规划。
EOF

# 创建 .env.example
cat > "$SKILL_PATH/.env.example" << EOF
# $SKILL_NAME 配置示例
# 复制此文件为 .env 并填写实际值

API_KEY=your_api_key_here
EOF

# 创建示例脚本
cat > "$SKILL_PATH/scripts/main.sh" << 'EOF'
#!/bin/bash
# {{SKILL_NAME}} 主脚本

set -e

echo "🔧 {{SKILL_NAME}} 正在运行..."

# TODO: 实现核心功能

echo "✅ 完成"
EOF

sed -i "s/{{SKILL_NAME}}/$SKILL_NAME/g" "$SKILL_PATH/scripts/main.sh"
chmod +x "$SKILL_PATH/scripts/main.sh"

# 创建 requirements.txt (Python 项目用)
cat > "$SKILL_PATH/requirements.txt" << EOF
# {{SKILL_NAME}} 依赖
# 安装：pip install -r requirements.txt

# TODO: 添加依赖
EOF

sed -i "s/{{SKILL_NAME}}/$SKILL_NAME/g" "$SKILL_PATH/requirements.txt"

echo ""
echo "✅ 技能创建成功！"
echo ""
echo "📁 目录结构:"
tree -L 2 "$SKILL_PATH" 2>/dev/null || find "$SKILL_PATH" -maxdepth 2 -type f | sort

echo ""
echo "📝 下一步:"
echo "1. 编辑 $SKILL_PATH/SKILL.md 完善功能定义"
echo "2. 在 $SKILL_PATH/scripts/ 中实现核心逻辑"
echo "3. 测试：cd $SKILL_PATH && ./scripts/main.sh"
echo "4. Git 提交：cd ~/.openclaw/workspace && git add skills/$SKILL_NAME && git commit -m 'feat: 创建 $SKILL_NAME'"

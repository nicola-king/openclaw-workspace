#!/bin/bash
# 太一 → Obsidian 同步完整性检查
# 运行：检查所有软链是否有效，无效自动重建

VAULT_DIR="/home/sayelf/下载/Taiy（工控机）/Taiyiopenclaw"
SYNC_DIR="$VAULT_DIR/太一同步"
WS="/home/sayelf/.openclaw/workspace"

LINKS=(
  "memory:$WS/memory"
  "notes:$WS/notes"
  "HEARTBEAT.md:$WS/HEARTBEAT.md"
  "MEMORY.md:$WS/MEMORY.md"
  "SOUL.md:$WS/SOUL.md"
  "core.md:$WS/memory/core.md"
  "context.md:$WS/memory/context.md"
  "evolution.md:$WS/memory/evolution.md"
)

errors=0
for entry in "${LINKS[@]}"; do
  name="${entry%%:*}"
  target="${entry##*:}"
  link="$SYNC_DIR/$name"

  if [ ! -L "$link" ] || [ ! -e "$link" ]; then
    echo "[修复] $name → $target"
    ln -sfn "$target" "$link"
    ((errors++))
  fi
done

if [ "$errors" -eq 0 ]; then
  echo "✅ 所有 $(( ${#LINKS[@]} )) 个链接正常"
else
  echo "🔧 已修复 $errors 个链接"
fi

# 检查 vault 根目录是否存在
if [ -d "$VAULT_DIR/.obsidian" ]; then
  echo "✅ Obsidian 配置目录存在"
else
  echo "⚠️ 未检测到 .obsidian 目录 — 请先在 Obsidian 中打开 vault 一次"
fi

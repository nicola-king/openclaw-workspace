#!/bin/bash
# Pre-git-backup hook: blocks secrets, checks memory integrity
# Adapted from claude-code block-secrets.sh for Taiyi system
# Called by system cron before Git backup (03:00)

BLOCKED_PATTERNS=(
  'api_key[[:space:]]*=[[:space:]]*['"'"'"]'
  'API_KEY[[:space:]]*=[[:space:]]*['"'"'"]'
  'sk-[a-zA-Z0-9]{20,}'
  'DEEPSEEK_API_KEY|ANTHROPIC_API_KEY|OPENAI_API_KEY'
  'Authorization: Bearer'
)

for pattern in "${BLOCKED_PATTERNS[@]}"; do
    if grep -rl "$pattern" /home/sayelf/.openclaw/workspace/output/ /home/sayelf/.openclaw/workspace/notes/ 2>/dev/null | head -3; then
        echo "[!] 发现敏感信息在输出文件中: $(grep -rl "$pattern" "$dir" | head -3)"
        echo "[!] 已阻止 Git 备份，请检查 output/ 和 notes/ 目录"
        exit 1
    fi
done

echo "[✓] 无敏感信息泄露"
exit 0

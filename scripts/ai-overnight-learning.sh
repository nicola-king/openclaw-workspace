#!/bin/bash
# AI 知识学习定时任务 (凌晨 1:00-6:00, 每小时)
# 搜索 X 上最新 AI 技术、资讯、专业知识

set -e

WORKSPACE=/home/nicola/.openclaw/workspace
LOG_FILE=$WORKSPACE/logs/ai-learning.log
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

log "=== AI 知识学习开始 ==="

# 搜索关键词列表
KEYWORDS=(
    "AGI artificial general intelligence"
    "LLM large language model"
    "AI agent autonomous"
    "machine learning breakthrough"
    "deep learning research"
    "AI reasoning thinking"
    "neural network architecture"
    "AI safety alignment"
    "multimodal AI vision language"
    "AI code generation programming"
)

# 搜索并保存结果
for keyword in "${KEYWORDS[@]}"; do
    log "🔍 搜索：$keyword"
    
    # 使用 web_search 搜索结果保存到文件
    SEARCH_FILE="$WORKSPACE/content/ai-learning/$(date '+%Y%m%d')-${keyword// /-}.md"
    mkdir -p "$(dirname "$SEARCH_FILE")"
    
    # 调用 OpenClaw web_search (通过 Python 脚本)
    python3 -c "
import requests
import json
from datetime import datetime

keyword = '$keyword'
url = 'https://api.duckduckgo.com/'
params = {'q': keyword, 'format': 'json'}

try:
    resp = requests.get(url, params=params, timeout=30)
    if resp.status_code == 200:
        data = resp.json()
        with open('$SEARCH_FILE', 'w') as f:
            f.write(f'# AI 学习 · {keyword}\n\n')
            f.write(f'搜索时间：{datetime.now().isoformat()}\n\n')
            f.write(f'## 搜索结果\n\n')
            if 'RelatedTopics' in data:
                for i, topic in enumerate(data['RelatedTopics'][:10], 1):
                    if 'Text' in topic and 'FirstURL' in topic:
                        f.write(f'{i}. [{topic[\"Text\"][:100]}]({topic[\"FirstURL\"]})\n')
        print(f'✅ 保存：$SEARCH_FILE')
    else:
        print(f'❌ API 失败：{resp.status_code}')
except Exception as e:
    print(f'❌ 异常：{e}')
" 2>&1 | tee -a "$LOG_FILE"
done

log "=== AI 知识学习完成 ==="

# 生成学习成果汇总文件
SUMMARY_FILE="$WORKSPACE/content/ai-learning/$(date '+%Y%m%d')-summary.md"
python3 -c "
from datetime import datetime
import os

date_str = datetime.now().strftime('%Y%m%d')
summary_file = f'$WORKSPACE/content/ai-learning/{date_str}-summary.md'

# 扫描今日学习文件
learning_dir = '$WORKSPACE/content/ai-learning'
files = [f for f in os.listdir(learning_dir) if f.startswith(date_str) and f.endswith('.md') and 'summary' not in f]

with open(summary_file, 'w') as f:
    f.write(f'# 🧠 AI 凌晨学习成果 · {datetime.now().strftime(\"%Y-%m-%d\")}\\n\\n')
    f.write(f'**学习时间**: 凌晨 1:00-6:00 (每小时)\\n')
    f.write(f'**搜索主题**: {len(files)} 个\\n\\n')
    f.write('---\\n\\n')
    f.write('## 📚 今日学习内容\\n\\n')
    for file in sorted(files):
        topic = file.replace(date_str + '-', '').replace('.md', '').replace('-', ' ').title()
        f.write(f'### {topic}\\n\\n')
        file_path = os.path.join(learning_dir, file)
        try:
            with open(file_path, 'r') as hf:
                content = hf.read()
                # 提取链接
                import re
                links = re.findall(r'\\[([^\\]]+)\\]\\(([^)]+)\\)', content)
                for i, (text, url) in enumerate(links[:5], 1):
                    f.write(f'{i}. [{text[:80]}]({url})\\n')
        except:
            pass
        f.write('\\n')
    f.write('\\n---\\n\\n*自动生成 · 太一 AGI*\\n')

print(f'✅ 学习成果汇总：{summary_file}')
" 2>&1 | tee -a "$LOG_FILE"

# 发送到 Telegram 通知（包含学习成果摘要）
python3 -c "
import requests
from datetime import datetime

BOT_TOKEN = '8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY'
CHAT_ID = '7073481596'

# 扫描今日学习文件数量
import os
date_str = datetime.now().strftime('%Y%m%d')
learning_dir = '/home/nicola/.openclaw/workspace/content/ai-learning'
files = [f for f in os.listdir(learning_dir) if f.startswith(date_str) and f.endswith('.md') and 'summary' not in f]

message = f'''🧠 AI 凌晨学习完成

📅 日期：{datetime.now().strftime(\"%Y-%m-%d\")}
⏰ 时间：凌晨 1:00-6:00
📚 学习主题：{len(files)} 个
📄 成果文件：content/ai-learning/{date_str}-summary.md

✅ 已完成，请查阅学习成果'''

url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
data = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
requests.post(url, json=data, timeout=30)
print('✅ 通知已发送')
" 2>&1 | tee -a "$LOG_FILE"

exit 0

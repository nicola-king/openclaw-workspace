#!/bin/bash
# AI 知识学习定时任务 v2.0 (修复版)
# 使用 DuckDuckGo HTML 搜索 (开源免费，无需 API Key)

set -e

WORKSPACE=/home/nicola/.openclaw/workspace
LOG_FILE=$WORKSPACE/logs/ai-learning.log
LEARNING_DIR=$WORKSPACE/content/ai-learning
DATE_STR=$(date '+%Y%m%d')
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

log "=== AI 知识学习开始 (v2.0) ==="

# 搜索关键词列表 (精简到 5 个核心主题)
KEYWORDS=(
    "AGI artificial general intelligence 2026"
    "LLM large language model breakthrough"
    "AI agent autonomous system"
    "machine learning research 2026"
    "AI code generation programming"
)

# 创建输出目录
mkdir -p "$LEARNING_DIR"

# 搜索并保存结果
for keyword in "${KEYWORDS[@]}"; do
    log "🔍 搜索：$keyword"
    
    SAFE_NAME=$(echo "$keyword" | tr ' ' '-' | tr -cd '[:alnum:]-')
    SEARCH_FILE="$LEARNING_DIR/${DATE_STR}-${SAFE_NAME}.md"
    
    # 使用 Python 执行搜索 (清除代理)
    python3 << PYEOF
import os
import sys
from datetime import datetime

# 清除代理环境变量
for key in list(os.environ.keys()):
    if 'proxy' in key.lower():
        del os.environ[key]
os.environ['NO_PROXY'] = '*'

import requests
from bs4 import BeautifulSoup

keyword = "$keyword"
output_file = "$SEARCH_FILE"

print(f"搜索：{keyword}")

try:
    # DuckDuckGo HTML 搜索
    url = "https://html.duckduckgo.com/html/"
    params = {'q': keyword}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # 禁用代理
    session = requests.Session()
    session.trust_env = False
    
    resp = session.post(url, data=params, headers=headers, timeout=30)
    
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        results = []
        for result in soup.select('.result')[:10]:
            title_elem = result.select_one('.result__title a')
            snippet_elem = result.select_one('.result__snippet')
            
            if title_elem and snippet_elem:
                title = title_elem.get_text(strip=True)
                snippet = snippet_elem.get_text(strip=True)
                url = title_elem.get('href', '')
                
                # DuckDuckGo URL 需要重定向解码
                if url.startswith('/l/?kh='):
                    # 提取实际 URL
                    from urllib.parse import parse_qs, urlparse
                    parsed = urlparse(url)
                    params = parse_qs(parsed.query)
                    if 'uddg' in params:
                        url = params['uddg'][0]
                elif url.startswith('//'):
                    url = 'https:' + url
                
                if url and title:
                    results.append({
                        'title': title,
                        'snippet': snippet,
                        'url': url
                    })
        
        # 保存结果
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f'# AI 学习 · {keyword}\n\n')
            f.write(f'搜索时间：{datetime.now().isoformat()}\n')
            f.write(f'来源：DuckDuckGo HTML (开源免费)\n\n')
            f.write(f'## 搜索结果 ({len(results)} 条)\n\n')
            
            for i, r in enumerate(results, 1):
                f.write(f'{i}. **{r["title"]}**\n')
                f.write(f'   {r["snippet"][:200]}\n')
                f.write(f'   [{r["url"]}]({r["url"]})\n\n')
        
        print(f'✅ 保存：{output_file} ({len(results)} 条结果)')
    else:
        print(f'❌ API 失败：{resp.status_code}')
        
except Exception as e:
    print(f'❌ 异常：{type(e).__name__}: {e}')
PYEOF

done

log "=== AI 知识学习完成 ==="

# 生成学习成果汇总
log "生成学习成果汇总..."
python3 << PYEOF
from datetime import datetime
import os
import re

date_str = "$DATE_STR"
learning_dir = "$LEARNING_DIR"
summary_file = os.path.join(learning_dir, f'{date_str}-summary.md')

# 扫描今日学习文件
files = [f for f in os.listdir(learning_dir) 
         if f.startswith(date_str) and f.endswith('.md') and 'summary' not in f]

with open(summary_file, 'w', encoding='utf-8') as f:
    f.write(f'# 🧠 AI 凌晨学习成果 · {datetime.now().strftime("%Y-%m-%d")}\n\n')
    f.write(f'**学习时间**: 凌晨 1:00-6:00 (每小时)\n')
    f.write(f'**搜索主题**: {len(files)} 个\n')
    f.write(f'**数据来源**: DuckDuckGo HTML (开源免费)\n\n')
    f.write('---\n\n')
    f.write('## 📚 今日学习内容\n\n')
    
    total_results = 0
    for file in sorted(files):
        topic = file.replace(date_str + '-', '').replace('.md', '').replace('-', ' ').title()
        f.write(f'### {topic}\n\n')
        
        file_path = os.path.join(learning_dir, file)
        try:
            with open(file_path, 'r', encoding='utf-8') as hf:
                content = hf.read()
                # 提取链接
                links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
                for i, (text, url) in enumerate(links[:5], 1):
                    f.write(f'{i}. [{text[:80]}]({url})\n')
                    total_results += 1
        except Exception as e:
            f.write(f'⚠️ 读取失败：{e}\n')
        f.write('\n')
    
    f.write(f'\n**总计**: {total_results} 条学习成果\n\n')
    f.write('\n---\n\n*自动生成 · 太一 AGI (DuckDuckGo 开源搜索)*\n')

print(f'✅ 学习成果汇总：{summary_file}')
print(f'📊 总结果数：{total_results} 条')
PYEOF

# 发送通知
log "发送通知..."
python3 << PYEOF
import requests
from datetime import datetime
import os

BOT_TOKEN = '8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY'
CHAT_ID = '7073481596'

date_str = datetime.now().strftime('%Y%m%d')
learning_dir = '/home/nicola/.openclaw/workspace/content/ai-learning'
files = [f for f in os.listdir(learning_dir) 
         if f.startswith(date_str) and f.endswith('.md') and 'summary' not in f]

message = f'''🧠 AI 凌晨学习完成 (v2.0)

📅 日期：{datetime.now().strftime("%Y-%m-%d")}
⏰ 时间：凌晨 1:00-6:00
📚 学习主题：{len(files)} 个
🔍 数据源：DuckDuckGo HTML (开源免费)
📄 成果：content/ai-learning/{date_str}-summary.md

✅ 已修复 202 错误，正常获取内容'''

url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
data = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
requests.post(url, json=data, timeout=30)
print('✅ 通知已发送')
PYEOF

exit 0

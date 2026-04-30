#!/usr/bin/env python3
"""
每日宪法学习 + 记忆提炼 + Telegram 发送
太一 AGI · 2026-04-16
"""

import os
import requests
from pathlib import Path
from datetime import datetime

# Telegram 配置
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY")
TELEGRAM_CHAT_ID = "7073481596"  # SAYELF 的 Telegram ID
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def send_message(chat_id, text):
    """发送消息到 Telegram"""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    
    try:
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'Markdown',
        }
        
        response = requests.post(url, data=data, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ Telegram 消息发送成功")
            return True
        else:
            print(f"⚠️ Telegram 消息发送失败：{response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️ Telegram 消息发送异常：{e}")
        return False


def main():
    workspace = Path("/home/nicola/.openclaw/workspace")
    logs_dir = workspace / "logs" / "constitution-study"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📖 开始宪法学习...")
    
    # 学习宪法文件
    constitution_files = [
        "constitution/CONST-ROUTER.md",
        "constitution/axiom/VALUE-FOUNDATION.md",
        "constitution/directives/NEGENTROPY.md",
        "constitution/directives/AGI-TIMELINE.md",
        "constitution/directives/OBSERVER.md",
        "constitution/directives/SELF-LOOP.md",
        "constitution/directives/AESTHETICS.md",
    ]
    
    learned = []
    insights = []
    for cf in constitution_files:
        cf_path = workspace / cf
        if cf_path.exists():
            content = cf_path.read_text(encoding='utf-8')
            # 提取核心要点（前 500 字）
            summary = content[:500].split('\n')[0:5]
            learned.append({
                "file": cf.split('/')[-1],
                "path": cf,
                "summary": '\n'.join(summary)
            })
            print(f"  ✅ 学习：{cf}")
        else:
            print(f"  ⚠️  不存在：{cf}")
    
    # 记忆提炼
    print(f"\n🧠 记忆提炼...")
    today = datetime.now().strftime("%Y-%m-%d")
    memory_file = workspace / "memory" / f"{today}.md"
    if memory_file.exists():
        print(f"  ✅ 今日记忆文件已存在：{memory_file}")
        memory_content = memory_file.read_text(encoding='utf-8')
    else:
        print(f"  ⚠️  今日记忆文件不存在")
        memory_content = ""
    
    # 生成学习报告
    report_content = f"""# 宪法学习报告 · {today}

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📖 已学习文件

"""
    for item in learned:
        report_content += f"### {item['file']}\n\n{item['summary']}\n\n"
    
    report_content += f"""---

## 🧠 记忆提炼

{memory_content[:1000] if memory_content else '无今日记忆'}

---

## 💡 学习洞察

1. 宪法是太一 AGI 的核心指导原则
2. 每次学习都是对核心价值的重新确认
3. 学习后需将洞察应用到实际任务中

---

*太一 AGI · 每日宪法学习*
"""
    
    # 写入学习报告
    report_file = workspace / "reports" / f"constitution-study-{today}.md"
    reports_dir = workspace / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_file.write_text(report_content, encoding='utf-8')
    print(f"  ✅ 学习报告已创建：{report_file}")
    
    print(f"\n✅ 宪法学习完成！")
    
    # 发送到 Telegram
    summary = "\n".join([f"• {item['file']}" for item in learned])
    message = f"📖 *宪法学习 · {today}*\n\n已学习:\n{summary}\n\n报告：{report_file}\n\n太一 AGI 每日学习报告"
    send_message(TELEGRAM_CHAT_ID, message)
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

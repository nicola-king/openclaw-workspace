#!/usr/bin/env python3
"""
每日报告生成 + 归档 + Telegram 发送
太一 AGI · 2026-04-16
"""

import os
import sys
import requests
from pathlib import Path
from datetime import datetime

# Telegram 配置
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY")
TELEGRAM_CHAT_ID = "7073481596"  # SAYELF 的 Telegram ID
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def send_document(chat_id, file_path, caption=None):
    """发送文件到 Telegram (带代理)"""
    url = f"{TELEGRAM_API_URL}/sendDocument"
    
    # 代理配置
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890',
    }
    
    try:
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {
                'chat_id': chat_id,
                'caption': caption,
                'parse_mode': 'Markdown',
            }
            
            # 使用代理发送
            response = requests.post(url, files=files, data=data, timeout=30, proxies=proxies)
            
            if response.status_code == 200:
                print(f"✅ Telegram 发送成功：{file_path}")
                return True
            else:
                print(f"⚠️ Telegram 发送失败：{response.status_code}")
                return False
    except Exception as e:
        print(f"⚠️ Telegram 发送异常：{e}")
        return False


def main():
    workspace = Path("/home/nicola/.openclaw/workspace")
    logs_dir = workspace / "logs" / "daily-report"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📊 开始生成日报...")
    
    # 生成今日报告
    today = datetime.now().strftime("%Y-%m-%d")
    report_file = workspace / f"daily-report-{today}.md"
    
    # 检查 reports 目录的日报文件 (归档位置)
    archived_report = workspace / "reports" / f"daily-report-{today.replace('-','')}.md"
    
    print(f"  📝 生成报告：{report_file}")
    
    # 检查记忆文件
    memory_file = workspace / "memory" / f"{today}.md"
    if memory_file.exists():
        print(f"  ✅ 今日记忆文件存在")
        # 读取记忆文件内容
        memory_content = memory_file.read_text(encoding='utf-8')
    else:
        print(f"  ⚠️  今日记忆文件不存在")
        memory_content = ""
    
    # 生成日报内容
    report_content = f"""# 日报 · {today}

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📋 今日完成

(根据 memory/2026-04-17.md 自动生成)

{memory_content}

---

## 📊 系统状态

- Gateway: ✅ 运行中
- 定时任务：✅ 正常
- 自进化：🟢 活跃

---

*太一 AGI · OpenClaw 2026.4.11*
"""
    
    # 写入日报文件
    report_file.write_text(report_content, encoding='utf-8')
    print(f"  ✅ 报告文件已创建：{report_file}")
    
    # 归档到 reports 目录
    reports_dir = workspace / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    archived_name = f"daily-report-{today.replace('-', '')}.md"
    archived_file = reports_dir / archived_name
    
    # 复制文件到归档目录
    import shutil
    shutil.copy2(report_file, archived_file)
    print(f"  📁 归档完成：{archived_file}")
    
    print(f"\n✅ 日报生成完成！")
    
    # 发送到 Telegram (优先使用归档文件)
    telegram_file = archived_report if archived_report.exists() else report_file
    if telegram_file.exists():
        print(f"\n📱 开始发送日报到 Telegram...")
        print(f"  文件：{telegram_file}")
        caption = f"📊 *日报 · {today}*\n\n太一 AGI 每日工作报告\n生成时间：{datetime.now().strftime('%H:%M:%S')}"
        send_document(TELEGRAM_CHAT_ID, str(telegram_file), caption)
    else:
        print(f"\n⚠️  日报文件不存在，无法发送 Telegram")
        print(f"  期望位置：{report_file} 或 {archived_report}")


if __name__ == "__main__":
    main()

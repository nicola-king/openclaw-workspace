#!/usr/bin/env python3
"""
Telegram 学习报告发送器

功能:
1. 读取 Markdown 学习报告
2. 格式化消息
3. 通过 Telegram Bot 发送给用户

作者：太一 AGI
创建：2026-04-10
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
REPORTS_DIR = WORKSPACE / "reports"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY")
TELEGRAM_CHAT_ID = "7073481596"  # SAYELF 的 Telegram ID


def get_latest_report():
    """获取最新的学习报告"""
    reports = list(REPORTS_DIR.glob("learning-report-*.md"))
    
    if not reports:
        return None
    
    latest = max(reports)
    with open(latest, "r", encoding="utf-8") as f:
        return f.read(), latest


def format_message(md_content):
    """格式化消息为 Telegram 格式"""
    # 提取关键信息
    lines = md_content.split('\n')
    
    title = "🌙 凌晨学习报告"
    date = datetime.now().strftime("%Y-%m-%d")
    
    # 构建消息
    message = f"""{title}
📅 日期：{date}

📊 学习统计:
"""
    
    # 提取统计信息
    in_stats = False
    for line in lines:
        if "| **学习时长** |" in line:
            in_stats = True
        if in_stats and "|" in line:
            # 解析表格行
            parts = line.split("|")
            if len(parts) >= 3:
                metric = parts[1].strip()
                value = parts[2].strip()
                if metric and value and not metric.startswith("---"):
                    message += f"  • {metric}: {value}\n"
        if in_stats and line.strip() == "" and len(message) > 200:
            break
    
    # 提取创新成果
    message += "\n💡 融合创新:\n"
    innovations = []
    for line in lines:
        if "#### " in line and any(x in line for x in ["UI", "动画", "代码", "架构"]):
            innovations.append(line.replace("#### ", "").strip())
    
    for i, inn in enumerate(innovations[:4], 1):
        message += f"  {i}. {inn}\n"
    
    # 提取能力涌现
    message += "\n🧬 能力涌现:\n"
    for line in lines:
        if "**新创建 Skill**" in line:
            parts = line.split("|")
            if len(parts) >= 2:
                message += f"  • {parts[1].strip()}\n"
    
    # 添加文件附件说明
    message += f"""
📄 完整报告:
learning-report-{date}.md

---
*太一 AGI · 凌晨学习系统*
"""
    
    return message


def send_telegram_message(message, file_path=None):
    """发送 Telegram 消息"""
    
    # 先发送文本消息
    text_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    text_data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        # 发送文本
        result = subprocess.run(
            ["curl", "-X", "POST", text_url, "-d", json.dumps(text_data)],
            capture_output=True,
            text=True
        )
        
        print(f"✅ 文本消息已发送")
        print(f"   接收者：{TELEGRAM_CHAT_ID}")
        
        # 如果有文件，发送文件
        if file_path and Path(file_path).exists():
            file_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
            
            result = subprocess.run(
                ["curl", "-X", "POST", file_url, 
                 "-F", f"chat_id={TELEGRAM_CHAT_ID}",
                 "-F", f"document=@{file_path}",
                 "-F", "caption=📄 完整学习报告"],
                capture_output=True,
                text=True
            )
            
            print(f"✅ 报告文件已发送")
            print(f"   文件：{file_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ 发送失败：{e}")
        return False


def main():
    """主函数"""
    print("📤 发送 Telegram 学习报告...")
    print("="*50)
    print()
    
    # 获取最新报告
    report_data = get_latest_report()
    
    if not report_data:
        print("❌ 未找到学习报告")
        print("   请确认凌晨学习系统是否正常运行")
        return 1
    
    md_content, report_file = report_data
    
    print(f"✅ 加载学习报告：{report_file}")
    print(f"   大小：{len(md_content)} 字符")
    print()
    
    # 格式化消息
    message = format_message(md_content)
    
    print("📝 消息预览:")
    print("-"*50)
    print(message[:500] + "..." if len(message) > 500 else message)
    print("-"*50)
    print()
    
    # 发送 Telegram
    success = send_telegram_message(message, str(report_file))
    
    if success:
        print()
        print("✅ Telegram 报告发送完成")
        return 0
    else:
        print()
        print("❌ Telegram 报告发送失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())

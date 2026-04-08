#!/usr/bin/env python3
"""
5 账号数据监控日报
每日 09:00 自动运行，推送数据到 Telegram

数据源：
- 小红书：手动更新（API 限制）
- 视频号：手动更新（API 限制）
- 公众号：手动更新（API 限制）

用法：
    python3 social-media-monitor.py --send
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import requests

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
DATA_FILE = WORKSPACE / "data" / "social-media-stats.json"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7073481596")  # 默认发给 SAYELF 本人

# 5 账号基准数据（2026-03-28）
BASELINE = {
    "xiaohongshu_shanyelf": {"name": "小红书 - SAYELF 山野精灵", "base": 4262, "unit": "粉"},
    "xiaohongshu_muse": {"name": "小红书 - AI 缪斯｜龙虾研究所", "base": 4661, "unit": "粉"},
    "videonumber_shanyelf": {"name": "视频号 - SAYELF 山野精灵", "base": 1497, "unit": "关"},
    "videonumber_weijing": {"name": "视频号 - 微景漫语", "base": 11, "unit": "关"},
    "wechat_official": {"name": "公众号 - SAYELF 山野精灵", "base": 23, "unit": "关"}
}


def load_previous_stats():
    """加载昨日数据"""
    if not DATA_FILE.exists():
        return None
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 找最近一次记录
    if data and len(data) > 0:
        return data[-1]
    return None


def save_current_stats(stats):
    """保存当前数据"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []
    
    data.append(stats)
    
    # 保留最近 90 天
    if len(data) > 90:
        data = data[-90:]
    
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_report(current_stats, previous_stats):
    """生成日报文本"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    lines = [
        f"【5 账号日报 · {today}】",
        "",
        "📕 小红书"
    ]
    
    # 小红书账号
    xiaohongshu_keys = ["xiaohongshu_shanyelf", "xiaohongshu_muse"]
    for key in xiaohongshu_keys:
        info = BASELINE[key]
        current = current_stats.get(key, info["base"])
        previous = previous_stats.get(key, info["base"]) if previous_stats else info["base"]
        change = current - previous
        
        change_str = f"+{change}" if change > 0 else str(change)
        change_icon = "↗️" if change > 0 else ("↘️" if change < 0 else "➡️")
        
        lines.append(f"- {info['name'].split(' - ')[1]}: {current}{info['unit']} ({change_icon}{change_str})")
    
    lines.append("")
    lines.append("📹 视频号")
    
    # 视频号账号
    videonumber_keys = ["videonumber_shanyelf", "videonumber_weijing"]
    for key in videonumber_keys:
        info = BASELINE[key]
        current = current_stats.get(key, info["base"])
        previous = previous_stats.get(key, info["base"]) if previous_stats else info["base"]
        change = current - previous
        
        change_str = f"+{change}" if change > 0 else str(change)
        change_icon = "↗️" if change > 0 else ("↘️" if change < 0 else "➡️")
        
        lines.append(f"- {info['name'].split(' - ')[1]}: {current}{info['unit']} ({change_icon}{change_str})")
    
    lines.append("")
    lines.append("📖 公众号")
    
    # 公众号账号
    official_key = "wechat_official"
    info = BASELINE[official_key]
    current = current_stats.get(official_key, info["base"])
    previous = previous_stats.get(official_key, info["base"]) if previous_stats else info["base"]
    change = current - previous
    
    change_str = f"+{change}" if change > 0 else str(change)
    change_icon = "↗️" if change > 0 else ("↘️" if change < 0 else "➡️")
    
    lines.append(f"- {info['name'].split(' - ')[1]}: {current}{info['unit']} ({change_icon}{change_str})")
    
    # 总计
    total_current = sum(current_stats.get(k, v["base"]) for k, v in BASELINE.items())
    total_previous = sum(previous_stats.get(k, v["base"]) for k, v in BASELINE.items()) if previous_stats else sum(v["base"] for v in BASELINE.values())
    total_change = total_current - total_previous
    total_change_str = f"+{total_change}" if total_change > 0 else str(total_change)
    
    lines.append("")
    lines.append(f"📊 总计：~{total_current:,} ({total_change_str})")
    lines.append("")
    
    # 爆款预警（如果有单篇内容数据）
    lines.append("💡 爆款预警：无")
    
    return "\n".join(lines)


def send_to_telegram(message):
    """发送消息到 Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        result = response.json()
        
        if result.get("ok"):
            print(f"✅ Telegram 推送成功")
            return True
        else:
            print(f"❌ Telegram 推送失败：{result}")
            return False
    except Exception as e:
        print(f"❌ 发送失败：{e}")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="5 账号数据监控日报")
    parser.add_argument("--send", action="store_true", help="发送到 Telegram")
    parser.add_argument("--update", action="store_true", help="手动更新数据（交互模式）")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("5 账号数据监控")
    print("=" * 60)
    
    # 加载昨日数据
    previous_stats = load_previous_stats()
    
    if args.update:
        # 手动更新模式
        print("\n【手动更新数据模式】")
        print("请输入今日数据（直接回车保持默认）：\n")
        
        current_stats = {}
        for key, info in BASELINE.items():
            default = info["base"]
            if previous_stats and key in previous_stats:
                default = previous_stats[key]
            
            user_input = input(f"{info['name']} [{default}]: ")
            if user_input.strip():
                try:
                    current_stats[key] = int(user_input.strip())
                except ValueError:
                    print(f"⚠️ 无效数字，使用默认值 {default}")
                    current_stats[key] = default
            else:
                current_stats[key] = default
        
        # 保存
        save_current_stats(current_stats)
        print(f"\n✅ 数据已保存到 {DATA_FILE}")
        
        # 生成报告
        report = generate_report(current_stats, previous_stats)
        print("\n" + "=" * 60)
        print(report)
        print("=" * 60)
        
        if args.send:
            send_to_telegram(report)
    
    else:
        # 自动模式（使用最新数据）
        current_stats = previous_stats if previous_stats else {k: v["base"] for k, v in BASELINE.items()}
        
        report = generate_report(current_stats, previous_stats)
        print("\n" + "=" * 60)
        print(report)
        print("=" * 60)
        
        if args.send:
            send_to_telegram(report)


if __name__ == "__main__":
    main()

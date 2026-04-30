#!/usr/bin/env python3
"""
全网热点聚合处理器 - 多平台支持
太一 AGI · 2026-04-17

支持平台：
- B 站、微博、知乎、抖音
- 小红书、今日头条、百度
- 知乎、虎扑、36 氪
- X/Twitter、YouTube (可选)
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
LOG_FILE = WORKSPACE / "logs" / "hot-topics.log"
CONFIG_FILE = WORKSPACE / "config" / "hot-topics-config.json"

# Telegram 配置
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY")
TELEGRAM_CHAT_ID = "7073481596"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# 平台配置 (使用聚合 API + 官方接口混合)
# 优先使用 DailyHot API (开源免费)
DAILYHOT_API = "https://api.hottops.cn/api"

# 备用 API
BACKUP_APIS = {
    "uapis": "https://uapis.cn/api/hot",
    "52api": "https://api.52api.cn/hot",
}

# 平台映射
PLATFORMS = {
    "bilibili": "B 站",
    "weibo": "微博",
    "zhihu": "知乎",
    "douyin": "抖音",
    "xiaohongshu": "小红书",
    "toutiao": "今日头条",
    "baidu": "百度",
    "hupu": "虎扑",
    "36kr": "36 氪",
    "v2ex": "V2EX",
    "github": "GitHub",
    "youtube": "YouTube",
}

# 默认启用的平台
DEFAULT_PLATFORMS = [
    "bilibili",
    "weibo",
    "zhihu",
    "douyin",
    "xiaohongshu",
    "toutiao",
]


def load_config():
    """加载配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "platforms": DEFAULT_PLATFORMS,
        "top_n": 5,
        "push_to_telegram": True,
    }


def send_telegram_message(text, parse_mode="Markdown"):
    """发送消息到 Telegram - 使用太一智能路由系统规则"""
    # 使用太一标准 Telegram 发送脚本
    import subprocess
    import tempfile
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(text)
        temp_file = f.name
    
    try:
        # 调用太一标准发送脚本
        result = subprocess.run(
            ['python3', '/home/nicola/.openclaw/workspace/scripts/send-md-to-telegram.py', temp_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✅ Telegram 推送成功 (太一智能路由)")
            return True
        else:
            print(f"⚠️ Telegram 推送失败：{result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⚠️ Telegram 推送超时")
        return False
    except Exception as e:
        print(f"⚠️ Telegram 推送异常：{e}")
        return False
    finally:
        # 清理临时文件
        try:
            os.unlink(temp_file)
        except:
            pass


def fetch_from_dailyhot(platform):
    """从 DailyHot API 获取"""
    try:
        url = f"{DAILYHOT_API}?type={platform}"
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200:
                items = data.get("data", [])
                return [{"title": item.get("title", ""), "rank": i+1, "hot": item.get("hot", "")} for i, item in enumerate(items[:10])]
    except:
        pass
    return []


def fetch_from_uapis(platform):
    """从 UAPI 获取"""
    try:
        url = f"{BACKUP_APIS['uapis']}/{platform}"
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                return [{"title": item.get("title", ""), "rank": i+1} for i, item in enumerate(data[:10])]
    except:
        pass
    return []


def fetch_bilibili_official():
    """B 站官方接口"""
    try:
        url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        data = response.json()
        items = data.get("data", {}).get("list", [])
        return [{"title": item.get("title", ""), "rank": i+1} for i, item in enumerate(items[:10])]
    except:
        return []


def fetch_hot_topics(platforms=None):
    """获取热点话题"""
    config = load_config()
    if platforms is None:
        platforms = config.get("platforms", DEFAULT_PLATFORMS)
    
    print(f"📡 获取热点：{', '.join([PLATFORMS.get(p, p) for p in platforms])}")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    for platform in platforms:
        print(f"\n🔍 {PLATFORMS.get(platform, platform)}...", end=" ")
        
        # 尝试不同数据源
        items = fetch_from_dailyhot(platform)
        if not items:
            items = fetch_from_uapis(platform)
        
        # B 站使用官方接口
        if platform == "bilibili" and not items:
            items = fetch_bilibili_official()
        
        if items:
            results[platform] = items
            print(f"✅ {len(items)} 条")
        else:
            print(f"⚠️ 无数据")
    
    return results


def generate_summary(data, top_n=5):
    """生成热点摘要"""
    summary = f"📡 全网热点聚合 · {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    
    for platform, items in data.items():
        name = PLATFORMS.get(platform, platform)
        summary += f"\n🔥 {name} Top {top_n}:\n"
        
        for i, item in enumerate(items[:top_n], 1):
            title = item.get("title", "无标题")
            hot = item.get("hot", "")
            if hot:
                summary += f"{i}. {title} 🔥{hot}\n"
            else:
                summary += f"{i}. {title}\n"
    
    summary += f"\n太一 AGI · 热点聚合"
    
    return summary


def save_to_log(summary):
    """保存日志"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*50}\n[{datetime.now()}]\n{summary}\n")
    print(f"📝 日志已保存：{LOG_FILE}")


def main():
    """主函数"""
    print("=" * 50)
    print("📡 全网热点聚合处理器")
    print("=" * 50)
    
    # 加载配置
    config = load_config()
    top_n = config.get("top_n", 5)
    push_telegram = config.get("push_to_telegram", True)
    
    # 获取热点
    data = fetch_hot_topics()
    
    if not data:
        print("\n❌ 获取失败")
        return
    
    # 生成摘要
    summary = generate_summary(data, top_n)
    print("\n" + summary)
    
    # 保存日志
    save_to_log(summary)
    
    # Telegram 推送 - 使用太一智能路由系统规则
    if push_telegram:
        print("\n📱 开始推送到 Telegram (太一智能路由)...")
        send_telegram_message(summary)
    
    print("\n✅ 处理完成")


if __name__ == "__main__":
    main()

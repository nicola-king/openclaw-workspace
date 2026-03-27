#!/bin/bash
# TurboQuant 压缩率告警通知脚本
# 当压缩率 < 3x 时发送微信/Telegram 通知

WORKSPACE="/home/nicola/.openclaw/workspace"
DATA_FILE="$WORKSPACE/dashboard/compression-data.json"
LOG_FILE="$WORKSPACE/logs/compression-alert.log"

# 告警阈值
ALERT_THRESHOLD=3.0

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 检查数据文件是否存在
if [ ! -f "$DATA_FILE" ]; then
    log "错误：数据文件不存在 $DATA_FILE"
    exit 1
fi

# 解析 JSON 数据，检查压缩率
# 使用 Python 解析 JSON（更可靠）
python3 << 'PYTHON_SCRIPT'
import json
import subprocess
import os
from datetime import datetime

DATA_FILE = "/home/nicola/.openclaw/workspace/dashboard/compression-data.json"
ALERT_THRESHOLD = 3.0

def send_wechat_notification(message):
    """发送微信通知（通过素问 Bot）"""
    try:
        # 使用 message 工具发送微信通知
        cmd = f'''
        openclaw message send --target="openclaw-weixin" --message="{message}"
        '''
        subprocess.run(cmd, shell=True, capture_output=True)
        return True
    except Exception as e:
        print(f"微信发送失败：{e}")
        return False

def send_telegram_notification(message):
    """发送 Telegram 通知（通过知几 Bot）"""
    try:
        # 使用 Telegram Bot API
        bot_token = "AAHeycXPlUQic41mOu4yCyaDcNQAKxYr61E"  # zhiji bot
        chat_id = "7073481596"  # Nicola's Telegram ID
        
        import urllib.request
        import urllib.parse
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = urllib.parse.urlencode({
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }).encode()
        
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception as e:
        print(f"Telegram 发送失败：{e}")
        return False

try:
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    alerts = []
    
    # 检查每个文件的压缩率
    for file in data.get('files', []):
        size = file.get('size', 0)
        original_size = file.get('originalSize', 0)
        
        if size > 0 and original_size > 0:
            rate = original_size / size
            if rate < ALERT_THRESHOLD:
                alerts.append({
                    'file': file['name'],
                    'rate': round(rate, 2),
                    'size': round(size / 1024, 1)
                })
    
    if alerts:
        # 生成告警消息
        alert_count = len(alerts)
        message = f"""🚨 **TurboQuant 压缩率告警**

发现 {alert_count} 个文件压缩率异常 (<{ALERT_THRESHOLD}x)

"""
        for alert in alerts[:5]:  # 最多显示 5 个
            message += f"• `{alert['file']}`: {alert['rate']}x ({alert['size']} KB)\n"
        
        if alert_count > 5:
            message += f"\n... 还有 {alert_count - 5} 个文件\n"
        
        message += f"\n请检查：/home/nicola/.openclaw/workspace/memory/"
        
        # 发送通知
        log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{log_time}] 发现 {alert_count} 个告警")
        
        # 发送微信
        if send_wechat_notification(message.replace('`', '')):
            print("✓ 微信通知已发送")
        
        # 发送 Telegram
        if send_telegram_notification(message):
            print("✓ Telegram 通知已发送")
    else:
        log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{log_time}] 压缩率正常，无需告警")

except Exception as e:
    print(f"错误：{e}")
    import traceback
    traceback.print_exc()

PYTHON_SCRIPT

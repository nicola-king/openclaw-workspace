#!/usr/bin/env python3
"""
预警通知引擎 - 整合版
功能：三级预警通知、多渠道发送、频率限制、历史记录
用法：from skills.monitoring.alert_engine import send_alert
"""

import json
import os
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

# ============================================================================
# 配置
# ============================================================================

# 预警级别
ALERT_LEVELS = {
    'normal': {'emoji': '📊', 'color': 'info', 'priority': 0},
    'warning': {'emoji': '⚠️', 'color': 'warning', 'priority': 1},
    'critical': {'emoji': '🔴', 'color': 'danger', 'priority': 2}
}

# 知几-E 预警阈值
TRADING_THRESHOLDS = {
    'daily_warning_loss': 0.05,      # -5% 预警
    'daily_stop_loss': 0.10,         # -10% 止损
    'consecutive_warning': 2,        # 连败 2 场预警
    'consecutive_limit': 3,          # 连败 3 场暂停
    'roi_warning': 0.0,              # ROI<0 预警
    'roi_critical': -0.2,            # ROI<-20% 紧急
    'cost_warning': 500,             # 日成本>¥500 预警
    'budget_warning': 0.8            # 预算使用>80% 预警
}

# 文件路径
ALERT_HISTORY_FILE = Path('/tmp/alert-history.json')
ALERT_STATE_FILE = Path('/tmp/alert-state.json')
LOG_FILE = Path('/home/nicola/.openclaw/logs/alert-engine.log')

# 通知配置 (从环境变量读取)
WECHAT_WEBHOOK_URL = os.getenv('WECHAT_WEBHOOK_URL', '')
SMS_API_KEY = os.getenv('SMS_API_KEY', '')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# 频率限制 (秒)
FREQUENCY_LIMITS = {
    'normal': 3600,      # 正常通知：1 小时
    'warning': 1800,     # 预警通知：30 分钟
    'critical': 300      # 紧急通知：5 分钟
}

# ============================================================================
# 日志函数
# ============================================================================

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}\n"
    print(log_line.strip())
    
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, 'a') as f:
            f.write(log_line)
    except Exception as e:
        pass

# ============================================================================
# 状态管理
# ============================================================================

def load_alert_history():
    """加载预警历史"""
    if ALERT_HISTORY_FILE.exists():
        with open(ALERT_HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_alert_history(history):
    """保存预警历史"""
    with open(ALERT_HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2, default=str)

def load_alert_state():
    """加载预警状态"""
    if ALERT_STATE_FILE.exists():
        with open(ALERT_STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        'trading_paused': False,
        'pause_reason': None,
        'pause_until': None,
        'consecutive_losses': 0,
        'daily_loss': 0.0,
        'daily_cost': 0.0
    }

def save_alert_state(state):
    """保存预警状态"""
    with open(ALERT_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2, default=str)

def should_send_alert(level: str, message: str) -> bool:
    """检查是否应该发送预警 (频率限制)"""
    history = load_alert_history()
    limit_seconds = FREQUENCY_LIMITS.get(level, 3600)
    now = datetime.now()
    
    # 检查相同消息是否在限制时间内发送过
    for alert in history:
        if alert['message'] == message:
            alert_time = datetime.fromisoformat(alert['timestamp'])
            if (now - alert_time).total_seconds() < limit_seconds:
                log(f"频率限制：相同消息 {limit_seconds}秒内不重复发送")
                return False
    
    return True

def record_alert(level: str, message: str, success: bool):
    """记录预警发送"""
    history = load_alert_history()
    
    # 添加新记录
    history.append({
        'timestamp': datetime.now().isoformat(),
        'level': level,
        'message': message,
        'success': success
    })
    
    # 保留最近 100 条
    if len(history) > 100:
        history = history[-100:]
    
    save_alert_history(history)

# ============================================================================
# 通知渠道
# ============================================================================

def send_wechat(message: str, title: str = "监控通知") -> bool:
    """发送微信通知 (企业微信)"""
    if not WECHAT_WEBHOOK_URL:
        log("微信 Webhook 未配置")
        return False
    
    try:
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"### {title}\n\n{message}"
            }
        }
        
        response = requests.post(WECHAT_WEBHOOK_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('errcode') == 0:
                log("✅ 微信通知发送成功")
                return True
            else:
                log(f"❌ 微信通知失败：{result}")
                return False
        else:
            log(f"❌ 微信通知失败：HTTP {response.status_code}")
            return False
    except Exception as e:
        log(f"❌ 微信通知异常：{e}")
        return False

def send_sms(message: str, phone: str = None) -> bool:
    """发送短信通知 (腾讯云)"""
    if not SMS_API_KEY:
        log("短信 API Key 未配置")
        return False
    
    # TODO: 实现腾讯云短信 API
    log("短信通知：待实现")
    return False

def send_telegram(message: str) -> bool:
    """发送 Telegram 通知"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        log("Telegram 配置未设置")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            log("✅ Telegram 通知发送成功")
            return True
        else:
            log(f"❌ Telegram 通知失败：HTTP {response.status_code}")
            return False
    except Exception as e:
        log(f"❌ Telegram 通知异常：{e}")
        return False

# ============================================================================
# 预警引擎
# ============================================================================

def send_alert(level: str, message: str, channels: list = None, force: bool = False):
    """
    发送预警通知
    
    Args:
        level: 预警级别 (normal/warning/critical)
        message: 预警消息
        channels: 通知渠道 (默认根据级别自动选择)
        force: 是否忽略频率限制
    """
    if level not in ALERT_LEVELS:
        log(f"❌ 未知预警级别：{level}")
        return False
    
    # 检查频率限制
    if not force and not should_send_alert(level, message):
        return False
    
    emoji = ALERT_LEVELS[level]['emoji']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 格式化消息
    formatted_message = f"{emoji} **{level.upper()}**\n\n{message}\n\n_时间：{timestamp}_"
    
    # 确定通知渠道
    if channels is None:
        if level == 'normal':
            channels = ['wechat']
        elif level == 'warning':
            channels = ['wechat']
        elif level == 'critical':
            channels = ['wechat', 'telegram']  # 紧急时多渠道
    
    # 发送通知
    success = False
    
    for channel in channels:
        try:
            if channel == 'wechat':
                if send_wechat(formatted_message):
                    success = True
            elif channel == 'sms':
                if send_sms(message):
                    success = True
            elif channel == 'telegram':
                if send_telegram(formatted_message):
                    success = True
        except Exception as e:
            log(f"渠道 {channel} 发送失败：{e}")
    
    # 记录发送结果
    record_alert(level, message, success)
    
    return success

# ============================================================================
# 交易预警检查
# ============================================================================

def check_trading_state(trading_stats: Dict[str, Any]) -> Optional[str]:
    """
    检查交易状态并返回预警消息
    
    Args:
        trading_stats: 交易统计数据
            - daily_loss: 日亏损率
            - consecutive_losses: 连败次数
            - roi: 当前 ROI
            - daily_cost: 日成本
            - budget_usage: 预算使用率
    
    Returns:
        预警消息或 None
    """
    state = load_alert_state()
    
    # 更新状态
    state['daily_loss'] = trading_stats.get('daily_loss', 0.0)
    state['consecutive_losses'] = trading_stats.get('consecutive_losses', 0)
    state['daily_cost'] = trading_stats.get('daily_cost', 0.0)
    
    alerts = []
    
    # 检查日亏损
    daily_loss = trading_stats.get('daily_loss', 0.0)
    if daily_loss <= -TRADING_THRESHOLDS['daily_stop_loss']:
        # 紧急：触发止损
        state['trading_paused'] = True
        state['pause_reason'] = '日亏损达到止损线'
        state['pause_until'] = (datetime.now() + timedelta(days=1)).isoformat()
        
        alerts.append({
            'level': 'critical',
            'message': f"🔴 **触发每日止损**\n\n当前亏损：{daily_loss*100:.1f}%\n止损线：{TRADING_THRESHOLDS['daily_stop_loss']*100:.0f}%\n\n操作：已自动暂停交易，明日恢复。"
        })
        
    elif daily_loss <= -TRADING_THRESHOLDS['daily_warning_loss']:
        # 预警
        alerts.append({
            'level': 'warning',
            'message': f"⚠️ **亏损预警**\n\n当前亏损：{daily_loss*100:.1f}%\n预警线：{TRADING_THRESHOLDS['daily_warning_loss']*100:.0f}%\n止损线：{TRADING_THRESHOLDS['daily_stop_loss']*100:.0f}%\n\n建议：降低仓位，等待市场回暖。"
        })
    
    # 检查连败
    consecutive = trading_stats.get('consecutive_losses', 0)
    if consecutive >= TRADING_THRESHOLDS['consecutive_limit']:
        state['trading_paused'] = True
        state['pause_reason'] = '连败次数过多'
        
        alerts.append({
            'level': 'critical',
            'message': f"🔴 **连败暂停**\n\n连败次数：{consecutive}场\n限制：{TRADING_THRESHOLDS['consecutive_limit']}场\n\n操作：已暂停交易，请调整策略。"
        })
        
    elif consecutive >= TRADING_THRESHOLDS['consecutive_warning']:
        alerts.append({
            'level': 'warning',
            'message': f"⚠️ **连败预警**\n\n连败次数：{consecutive}场\n限制：{TRADING_THRESHOLDS['consecutive_limit']}场\n\n建议：谨慎交易，提高置信度。"
        })
    
    # 检查 ROI
    roi = trading_stats.get('roi', 0.0)
    if roi <= TRADING_THRESHOLDS['roi_critical']:
        alerts.append({
            'level': 'critical',
            'message': f"🔴 **ROI 紧急**\n\n当前 ROI：{roi*100:.1f}%\n紧急线：{TRADING_THRESHOLDS['roi_critical']*100:.0f}%\n\n建议：暂停交易，复盘策略。"
        })
        
    elif roi < TRADING_THRESHOLDS['roi_warning']:
        alerts.append({
            'level': 'warning',
            'message': f"⚠️ **ROI 预警**\n\n当前 ROI：{roi*100:.1f}%\n预警线：{TRADING_THRESHOLDS['roi_warning']*100:.0f}%\n\n建议：优化策略，提高胜率。"
        })
    
    # 检查成本
    daily_cost = trading_stats.get('daily_cost', 0.0)
    if daily_cost >= TRADING_THRESHOLDS['cost_warning']:
        alerts.append({
            'level': 'warning',
            'message': f"⚠️ **成本预警**\n\n今日成本：¥{daily_cost:.0f}\n预警线：¥{TRADING_THRESHOLDS['cost_warning']:.0f}\n\n建议：控制 API 调用，优化查询策略。"
        })
    
    # 保存状态
    save_alert_state(state)
    
    # 发送预警
    if alerts:
        for alert in alerts:
            send_alert(alert['level'], alert['message'])
        return alerts[0]['message']  # 返回最高优先级预警
    
    return None

def resume_trading():
    """恢复交易 (手动调用)"""
    state = load_alert_state()
    state['trading_paused'] = False
    state['pause_reason'] = None
    state['pause_until'] = None
    state['consecutive_losses'] = 0
    save_alert_state(state)
    
    send_alert('normal', "✅ **交易恢复**\n\n交易已手动恢复，请谨慎操作。")
    log("交易已恢复")

def is_trading_paused() -> bool:
    """检查交易是否暂停"""
    state = load_alert_state()
    
    if not state.get('trading_paused'):
        return False
    
    # 检查暂停是否过期
    pause_until = state.get('pause_until')
    if pause_until:
        if datetime.now() > datetime.fromisoformat(pause_until):
            # 暂停过期，自动恢复
            resume_trading()
            return False
    
    return True

# ============================================================================
# 日报生成
# ============================================================================

def generate_daily_report(trading_stats: Dict[str, Any]) -> str:
    """生成日报内容"""
    date = datetime.now().strftime('%Y-%m-%d')
    
    report = f"""📊 **知几-E 日报**

日期：{date}

交易统计:
- 交易数：{trading_stats.get('trade_count', 0)} 笔
- 胜率：{trading_stats.get('win_rate', 0)*100:.0f}%
- 盈亏：{trading_stats.get('pnl', 0):+.0f} ({trading_stats.get('pnl_percent', 0)*100:+.1f}%)

本周累计:
- 盈亏：{trading_stats.get('weekly_pnl', 0):+.0f} ({trading_stats.get('weekly_pnl_percent', 0)*100:+.1f}%)
- ROI：{trading_stats.get('roi', 0)*100:+.0f}%

状态：{'🟢 正常' if not is_trading_paused() else '🔴 暂停'}
"""
    
    return report

# ============================================================================
# 主函数 (测试用)
# ============================================================================

def main():
    """测试预警引擎"""
    log("=" * 50)
    log("预警引擎测试")
    log("=" * 50)
    
    # 测试正常通知
    send_alert('normal', "这是一条测试通知")
    
    # 测试预警
    send_alert('warning', "这是一条测试预警")
    
    # 测试紧急通知
    send_alert('critical', "这是一条测试紧急通知")
    
    # 测试交易状态检查
    test_stats = {
        'daily_loss': -0.06,
        'consecutive_losses': 2,
        'roi': -0.05,
        'daily_cost': 300,
        'trade_count': 5,
        'win_rate': 0.6,
        'pnl': 120,
        'pnl_percent': 0.012,
        'weekly_pnl': 580,
        'weekly_pnl_percent': 0.058
    }
    
    log("")
    log("检查交易状态...")
    check_trading_state(test_stats)
    
    log("")
    log("生成日报...")
    print(generate_daily_report(test_stats))

if __name__ == '__main__':
    main()

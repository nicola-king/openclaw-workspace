#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按需响应过滤器（On-Demand Response Filter）
功能：判断消息是否需要 Bot 响应
版本：v1.0 | 创建：2026-04-03
"""

import re
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, Optional, List

# 配置
CONFIG = {
    'bot_names': ['太一', 'Taiyi', '小魔力'],
    'command_prefix': '/',
    'heartbeat_keywords': ['HEARTBEAT', 'heartbeat', '心跳', 'Read HEARTBEAT'],
    'ignore_old_messages_minutes': 5,
    'ignore_duplicate_messages_minutes': 5,
    'rate_limit_per_minute': 10,
    'rate_limit_per_hour': 100,
    'cooldown_seconds': 30,
}

# 响应缓存（内存）
response_cache = {
    'last_responses': [],  # [(timestamp, message_hash), ...]
    'message_hashes': {},  # {hash: timestamp}
}


def hash_message(message: str) -> str:
    """生成消息哈希（用于去重）"""
    return hex(hash(message.strip().lower()))[2:16]


def is_mentioned(message: str, bot_names: List[str] = None) -> bool:
    """检查消息是否@提及 Bot"""
    if bot_names is None:
        bot_names = CONFIG['bot_names']
    
    # 微信/飞书@格式：@用户名
    for name in bot_names:
        if f'@{name}' in message:
            return True
    
    # Telegram@格式：@username
    for name in bot_names:
        if re.search(rf'@\w*{name}\w*', message, re.IGNORECASE):
            return True
    
    # 中文提及（无@符号）
    for name in bot_names:
        if name in message and ('帮' in message or '请' in message or '你' in message):
            return True
    
    return False


def is_command(message: str) -> bool:
    """检查是否是命令（/开头）"""
    return message.strip().startswith(CONFIG['command_prefix'])


def is_heartbeat_poll(message: str) -> bool:
    """检查是否是心跳轮询"""
    message_lower = message.lower()
    for keyword in CONFIG['heartbeat_keywords']:
        if keyword.lower() in message_lower:
            return True
    return False


def is_direct_order(context: Dict[str, Any]) -> bool:
    """检查是否是 SAYELF 的直接指令"""
    # SAYELF 的标识（从配置或上下文获取）
    sayelf_identifiers = ['SAYELF', 'sayelf', 'nicola', ' Nicola']
    
    sender = context.get('sender', '')
    sender_id = context.get('sender_id', '')
    
    # 检查发送者是否是 SAYELF
    if any(s in str(sender) for s in sayelf_identifiers):
        return True
    if any(s in str(sender_id) for s in sayelf_identifiers):
        return True
    
    # 检查聊天类型（私聊默认是指令）
    chat_type = context.get('chat_type', '')
    if chat_type == 'direct' and any(s in str(sender) for s in sayelf_identifiers):
        return True
    
    return False


def is_imperative_message(message: str) -> bool:
    """检查消息是否是指令性语气"""
    imperative_keywords = [
        '请', '帮', '要', '需要', '必须', '应该',
        '去', '来', '做', '处理', '执行', '运行',
        '创建', '删除', '更新', '查询', '检查',
    ]
    
    # 检查是否包含指令性词汇
    for keyword in imperative_keywords:
        if keyword in message:
            return True
    
    # 检查是否是问句（可能是询问指令）
    if '?' in message or '？' in message:
        return True
    
    return False


def is_forwarded_message(context: Dict[str, Any]) -> bool:
    """检查是否是转发消息"""
    return context.get('is_forwarded', False) or context.get('forwarded_from', None) is not None


def is_media_only(message: str, context: Dict[str, Any]) -> bool:
    """检查是否是纯媒体消息（无文字）"""
    # 如果有文字内容，不是纯媒体
    if message and len(message.strip()) > 0:
        return False
    
    # 检查是否有媒体附件
    has_media = context.get('has_media', False)
    has_image = context.get('has_image', False)
    has_video = context.get('has_video', False)
    has_file = context.get('has_file', False)
    
    return has_media or has_image or has_video or has_file


def is_old_message(context: Dict[str, Any]) -> bool:
    """检查是否是旧消息（时间戳>5 分钟）"""
    message_time = context.get('timestamp')
    if not message_time:
        return False
    
    try:
        if isinstance(message_time, str):
            msg_dt = datetime.fromisoformat(message_time.replace('Z', '+00:00'))
        elif isinstance(message_time, (int, float)):
            msg_dt = datetime.fromtimestamp(message_time)
        else:
            return False
        
        now = datetime.now(msg_dt.tzinfo) if msg_dt.tzinfo else datetime.now()
        age = now - msg_dt
        
        return age > timedelta(minutes=CONFIG['ignore_old_messages_minutes'])
    except Exception:
        return False


def is_duplicate_message(message: str, context: Dict[str, Any]) -> bool:
    """检查是否是重复消息（5 分钟内相同内容）"""
    msg_hash = hash_message(message)
    now = time.time()
    
    # 清理旧缓存
    cutoff = now - (CONFIG['ignore_duplicate_messages_minutes'] * 60)
    response_cache['message_hashes'] = {
        k: v for k, v in response_cache['message_hashes'].items()
        if v > cutoff
    }
    
    # 检查是否重复
    if msg_hash in response_cache['message_hashes']:
        last_time = response_cache['message_hashes'][msg_hash]
        if now - last_time < (CONFIG['ignore_duplicate_messages_minutes'] * 60):
            return True
    
    # 更新缓存
    response_cache['message_hashes'][msg_hash] = now
    return False


def check_rate_limit() -> Tuple[bool, str]:
    """检查响应频率限制"""
    now = time.time()
    
    # 清理旧记录
    cutoff_minute = now - 60
    cutoff_hour = now - 3600
    
    response_cache['last_responses'] = [
        (t, h) for t, h in response_cache['last_responses']
        if t > cutoff_hour
    ]
    
    # 统计
    responses_minute = sum(1 for t, _ in response_cache['last_responses'] if t > cutoff_minute)
    responses_hour = len(response_cache['last_responses'])
    
    # 检查限制
    if responses_minute >= CONFIG['rate_limit_per_minute']:
        return False, "rate_limit_minute"
    
    if responses_hour >= CONFIG['rate_limit_per_hour']:
        return False, "rate_limit_hour"
    
    return True, "ok"


def record_response(message: str):
    """记录一次响应（用于频率限制）"""
    now = time.time()
    msg_hash = hash_message(message)
    response_cache['last_responses'].append((now, msg_hash))


def should_respond(message: str, context: Dict[str, Any]) -> Tuple[bool, str, str]:
    """
    判断消息是否需要 Bot 响应
    
    返回：(是否响应，原因，优先级)
    """
    # === 强制不响应的场景 ===
    
    # 1. 转发消息
    if is_forwarded_message(context):
        return False, "forwarded_message", "P4"
    
    # 2. 纯媒体消息（无文字）
    if is_media_only(message, context):
        return False, "media_only", "P4"
    
    # 3. 旧消息
    if is_old_message(context):
        return False, "old_message", "P4"
    
    # 4. 重复消息
    if is_duplicate_message(message, context):
        return False, "duplicate_message", "P4"
    
    # 5. 检查频率限制
    rate_ok, rate_reason = check_rate_limit()
    if not rate_ok:
        return False, rate_reason, "P4"
    
    # === 必须响应的场景 ===
    
    # 1. 被@提及
    if is_mentioned(message):
        return True, "mentioned", "P2"
    
    # 2. 命令触发
    if is_command(message):
        return True, "command", "P1"
    
    # 3. 心跳轮询
    if is_heartbeat_poll(message):
        return True, "heartbeat", "P3"
    
    # 4. SAYELF 的直接指令
    if is_direct_order(context) and is_imperative_message(message):
        return True, "direct_order", "P1"
    
    # 5. 错误恢复场景
    if context.get('is_error_recovery', False):
        return True, "error_recovery", "P0"
    
    # 6. 群聊中被点名（无@但有上下文）
    if context.get('chat_type') == 'group' and context.get('is_reply_to_bot', False):
        return True, "group_reply", "P2"
    
    # === 默认：不响应 ===
    return False, "no_trigger", "P4"


def get_response_priority(reason: str) -> str:
    """获取响应优先级标签"""
    priority_map = {
        'error_recovery': 'P0',
        'direct_order': 'P1',
        'command': 'P1',
        'mentioned': 'P2',
        'group_reply': 'P2',
        'heartbeat': 'P3',
    }
    return priority_map.get(reason, 'P4')


def get_response_delay(priority: str) -> int:
    """获取响应延迟（秒）"""
    delay_map = {
        'P0': 5,      # 立即
        'P1': 30,     # 快速
        'P2': 60,     # 正常
        'P3': 300,    # 按 Cron
        'P4': -1,     # 不响应
    }
    return delay_map.get(priority, -1)


# 测试
if __name__ == '__main__':
    test_cases = [
        # (message, context, expected_respond, expected_reason)
        ("@太一 今天天气如何", {'chat_type': 'group'}, True, "mentioned"),
        ("今天天气真好", {'chat_type': 'group'}, False, "no_trigger"),
        ("/日报", {'chat_type': 'direct', 'sender': 'SAYELF'}, True, "command"),
        ("帮我查一下天气", {'chat_type': 'direct', 'sender': 'SAYELF'}, True, "direct_order"),
        ("[转发] 文章标题", {'chat_type': 'direct', 'is_forwarded': True}, False, "forwarded_message"),
        ("", {'chat_type': 'direct', 'has_image': True}, False, "media_only"),
        ("HEARTBEAT_OK", {'chat_type': 'direct'}, True, "heartbeat"),
    ]
    
    print("=== 按需响应过滤器测试 ===\n")
    
    for msg, ctx, expected_respond, expected_reason in test_cases:
        respond, reason, priority = should_respond(msg, ctx)
        status = "✅" if respond == expected_respond and reason == expected_reason else "❌"
        print(f"{status} 消息：'{msg[:30]}...'")
        print(f"   响应：{respond} (期望：{expected_respond})")
        print(f"   原因：{reason} (期望：{expected_reason})")
        print(f"   优先级：{priority}")
        print()

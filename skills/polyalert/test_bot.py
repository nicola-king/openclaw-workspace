#!/usr/bin/env python3
"""
测试 PolyAlert Telegram Bot 连接
"""

import sys
sys.path.insert(0, '/home/nicola/.openclaw/workspace')

from skills.polyalert.notifier import send_telegram_message, send_welcome_message
from skills.polyalert.config import TELEGRAM_BOT_TOKEN, TELEGRAM_ADMIN_ID

print("=" * 50)
print("🔍 PolyAlert Bot 连接测试")
print("=" * 50)
print()
print(f"Bot Token: {TELEGRAM_BOT_TOKEN[:20]}...")
print(f"Admin ID: {TELEGRAM_ADMIN_ID}")
print()

# 测试 1：发送简单消息
print("📤 测试 1：发送简单消息...")
result = send_telegram_message("✅ PolyAlert Bot 连接测试成功！")
if result:
    print("✅ 消息发送成功！")
else:
    print("❌ 消息发送失败，请检查 Token 是否正确")

print()

# 测试 2：发送欢迎消息
print("📤 测试 2：发送欢迎消息...")
result = send_welcome_message()
if result:
    print("✅ 欢迎消息发送成功！")
else:
    print("❌ 欢迎消息发送失败")

print()
print("=" * 50)
print("🎉 测试完成！")
print("=" * 50)
print()
print("请在 Telegram 查看 @TrueListenBot 发送的消息")
print()

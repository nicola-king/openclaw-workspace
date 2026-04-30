"""太一旅行 - 多平台推送模块"""
from src.push.telegram import TelegramPusher
from src.push.wechat import WeChatPusher

__all__ = ["TelegramPusher", "WeChatPusher"]

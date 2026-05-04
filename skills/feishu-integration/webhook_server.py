#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书 Webhook 服务器
接收飞书消息事件并回复
"""

import json
import logging
from flask import Flask, request, jsonify

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 配置
VERIFICATION_TOKEN = "wmWId1pTZ9oiZWJr3zcnTbWWS5Be1Ub8"


@app.route('/webhook/feishu', methods=['POST'])
def webhook():
    """接收飞书 Webhook"""
    data = request.get_json()
    logger.info(f"收到请求: {json.dumps(data, ensure_ascii=False)[:200]}")
    
    # 验证 token
    token = data.get('token', '')
    if token != VERIFICATION_TOKEN:
        logger.warning(f"Token 验证失败: {token}")
        return jsonify({'error': 'invalid token'}), 403
    
    # 处理挑战请求 (首次配置)
    if 'challenge' in data:
        challenge = data['challenge']
        logger.info(f"处理挑战请求: {challenge}")
        return jsonify({'challenge': challenge})
    
    # 处理消息事件
    header = data.get('header', {})
    event_type = header.get('event_type', '')
    
    if event_type == 'im.message.receive_v1':
        event_data = data.get('event', {})
        message = event_data.get('message', {})
        
        # 获取消息内容
        content = json.loads(message.get('content', '{}'))
        text = content.get('text', '')
        
        # 获取发送者
        sender = event_data.get('sender', {}).get('sender_id', {}).get('open_id', '')
        
        logger.info(f"收到消息: '{text}' from {sender}")
        
        # 简单回复
        if text:
            reply_text = f"🤖 太一收到: {text}\n\n(功能开发中，稍后回复详细结果)"
            # TODO: 调用太一处理消息
            # send_reply(message.get('message_id'), reply_text)
        
        return jsonify({'status': 'ok'})
    
    return jsonify({'status': 'ok'})


@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({'status': 'ok', 'service': 'feishu-webhook'})


if __name__ == '__main__':
    logger.info("🚀 启动飞书 Webhook 服务器")
    logger.info("📡 监听地址: http://0.0.0.0:8080/webhook/feishu")
    app.run(host='0.0.0.0', port=8080)

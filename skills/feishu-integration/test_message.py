#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书消息发送测试
配置权限后运行此脚本测试
"""

import lark_oapi
import yaml
import json
from lark_oapi.api.auth.v3 import *
from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageRequestBody
from lark_oapi.core.model.request_option import RequestOption


def load_config():
    """加载配置"""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)


def get_token(client, config):
    """获取 Token"""
    req = InternalTenantAccessTokenRequest.builder() \
        .request_body(InternalTenantAccessTokenRequestBody.builder()
            .app_id(config['app_id'])
            .app_secret(config['app_secret'])
            .build()) \
        .build()
    
    resp = client.auth.v3.tenant_access_token.internal(req)
    raw_content = json.loads(resp.raw.content)
    return raw_content.get('tenant_access_token', '')


def send_message(client, token, receive_id, message_text):
    """发送消息"""
    req = CreateMessageRequest.builder() \
        .receive_id_type('open_id') \
        .request_body(CreateMessageRequestBody.builder()
            .receive_id(receive_id)
            .msg_type('text')
            .content(json.dumps({'text': message_text}))
            .build()) \
        .build()
    
    option = RequestOption.builder() \
        .tenant_access_token(token) \
        .build()
    
    resp = client.im.v1.message.create(req, option)
    return resp


def main():
    print("🚀 飞书消息发送测试")
    print("=" * 40)
    
    # 加载配置
    config = load_config()
    print(f"✅ 配置加载: {config['app_id']}")
    
    # 创建客户端
    client = lark_oapi.Client.builder() \
        .app_id(config['app_id']) \
        .app_secret(config['app_secret']) \
        .build()
    
    # 获取 Token
    token = get_token(client, config)
    print(f"✅ Token 获取: {token[:20]}...")
    
    # 获取接收者 open_id
    receive_id = input("\n请输入接收者的 open_id (或按回车跳过): ").strip()
    
    if not receive_id:
        print("⚠️ 未提供 open_id，跳过消息发送")
        print("\n如何获取 open_id:")
        print("1. 在飞书开放平台 -> 用户管理 查看")
        print("2. 使用 contact:user.read 权限查询")
        return
    
    # 发送消息
    message = """🤖 太一系统测试消息

时间: 2026-05-04
状态: 系统运行正常

来自太一 AI"""
    
    print(f"\n📨 发送消息到: {receive_id}")
    resp = send_message(client, token, receive_id, message)
    
    if resp.success():
        print("✅ 消息发送成功")
        data = json.loads(resp.raw.content)
        print(f"  消息ID: {data.get('data', {}).get('message_id', '')}")
    else:
        print(f"❌ 消息发送失败: {resp.msg}")
        print(f"   代码: {resp.code}")
        
        if resp.code == 99992351:
            print("\n⚠️ 需要配置权限:")
            print("  1. 访问 https://open.feishu.cn/app/")
            print("  2. 找到应用 '数字卵生'")
            print("  3. 添加权限: im:message:send")
            print("  4. 发布版本并审批")


if __name__ == '__main__':
    main()

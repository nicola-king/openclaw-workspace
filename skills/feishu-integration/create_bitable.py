#!/usr/bin/env python3
"""
📊 创建飞书多维表格 - 文件管理系统

自动创建多维表格并配置字段
支持文件导入功能

作者：太一 AGI
创建：2026-04-12
"""

import sys
import json
from pathlib import Path

# 导入客户端
sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/feishu-integration')
from feishu_client import FeishuClient


def create_file_management_bitable():
    """创建文件管理多维表格"""
    
    print("="*60)
    print("📊 创建飞书多维表格 - 文件管理系统")
    print("="*60)
    print()
    
    # 初始化客户端
    client = FeishuClient()
    
    # 测试连接
    print("1️⃣  测试连接...")
    if not client.test_connection():
        print("❌ 连接失败，请检查配置")
        return None
    
    print("✅ 连接成功\n")
    
    # 创建多维表格应用
    print("2️⃣  创建多维表格应用...")
    app_id = create_app(client)
    if not app_id:
        return None
    
    print(f"✅ App ID: {app_id}\n")
    
    # 创建表格
    print("3️⃣  创建表格...")
    table_id = create_table(client, app_id)
    if not table_id:
        return None
    
    print(f"✅ Table ID: {table_id}\n")
    
    # 保存配置
    print("4️⃣  保存配置...")
    save_config(app_id, table_id)
    print("✅ 配置已保存\n")
    
    # 完成
    print("="*60)
    print("✅ 创建完成!")
    print("="*60)
    print(f"\n📊 多维表格信息:")
    print(f"   应用名称：文件管理系统")
    print(f"   App ID: {app_id}")
    print(f"   Table ID: {table_id}")
    print(f"\n📥 使用方法:")
    print(f"   python3 /home/nicola/.openclaw/workspace/skills/feishu-integration/import_files.py <文件路径>")
    print(f"\n🔗 访问链接:")
    print(f"   https://bytedance.feishu.cn/base/{app_id}")
    print()
    
    return {"app_id": app_id, "table_id": table_id}


def create_app(client: FeishuClient) -> str:
    """创建应用"""
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps"
    payload = {"title": "文件管理系统"}
    
    result = client._request("POST", url, json=payload)
    
    if result.get('code') == 0:
        # 新 API 格式：data.app.app_token
        app_data = result.get('data', {})
        if 'app' in app_data:
            return app_data['app']['app_token']
        elif 'app_id' in app_data:
            return app_data['app_id']
        else:
            print(f"❌ 未知的响应格式：{result}")
            return None
    else:
        print(f"❌ 创建失败：{result}")
        return None


def create_table(client: FeishuClient, app_id: str) -> str:
    """创建表格"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables"
    
    # 定义字段
    fields = [
        {"field_name": "文件名", "type": 1},  # 文本
        {"field_name": "文件类型", "type": 1},  # 文本
        {"field_name": "文件大小 (KB)", "type": 2},  # 数字
        {"field_name": "创建时间", "type": 3},  # 日期
        {"field_name": "修改时间", "type": 3},  # 日期
        {"field_name": "文件路径", "type": 1},  # 文本
        {"field_name": "标签", "type": 1},  # 文本
        {"field_name": "备注", "type": 1},  # 文本
        {"field_name": "状态", "type": 4},  # 单选
    ]
    
    payload = {
        "table_name": "文件列表",
        "fields": fields
    }
    
    result = client._request("POST", url, json=payload)
    
    if result.get('code') == 0:
        return result['data']['table_id']
    else:
        print(f"❌ 创建失败：{result}")
        return None


def save_config(app_id: str, table_id: str):
    """保存配置"""
    config_path = Path("/home/nicola/.openclaw/workspace/config/feishu/config.json")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    config['bitable_app_id'] = app_id
    config['bitable_table_id'] = table_id
    config['bitable_name'] = "文件管理系统"
    config['bitable_table_name'] = "文件列表"
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    create_file_management_bitable()

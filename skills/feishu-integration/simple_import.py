#!/usr/bin/env python3
"""
📥 简化版文件导入工具

将文件数据导入到多维表格的第一列（标题列）

作者：太一 AGI
创建：2026-04-12
"""

import sys
import json
import pandas as pd
import requests
from pathlib import Path
from datetime import datetime, timedelta


class SimpleImporter:
    """简化导入器"""
    
    def __init__(self):
        config_path = "/home/nicola/.openclaw/workspace/config/feishu/config.json"
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.app_id = self.config.get('bitable_app_id')
        self.table_id = self.config.get('bitable_table_id')
        self.access_token = None
    
    def get_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.config['app_id'],
            "app_secret": self.config['app_secret']
        }
        response = requests.post(url, json=payload)
        data = response.json()
        if data.get('code') == 0:
            self.access_token = data['tenant_access_token']
            return self.access_token
        raise Exception(f"获取令牌失败：{data}")
    
    def import_excel(self, file_path):
        """导入 Excel 文件到第一列"""
        # 读取 Excel
        df = pd.read_excel(file_path)
        print(f"📄 读取文件：{file_path}")
        print(f"   列：{list(df.columns)}")
        print(f"   行数：{len(df)}")
        
        # 获取令牌
        token = self.get_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        # 获取表格字段
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_id}/tables/{self.table_id}/fields"
        response = requests.get(url, headers=headers)
        fields_data = response.json()
        
        if fields_data.get('code') != 0:
            print(f"❌ 获取字段失败：{fields_data}")
            return
        
        fields = fields_data['data']['items']
        print(f"\n📋 表格字段:")
        for f in fields:
            field_info = f.get('table_field', f)
            print(f"   - {field_info.get('field_name')} (type: {field_info.get('type')})")
        
        # 使用第一个字段（通常是标题字段）
        if fields:
            first_field = fields[0].get('table_field', fields[0])
            field_name = first_field['field_name']
            print(f"\n✅ 使用字段：{field_name}")
        else:
            field_name = "标题"
        
        # 批量创建记录
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_id}/tables/{self.table_id}/records/batch_create"
        
        records = []
        for _, row in df.iterrows():
            # 取第一列的值
            first_value = row.iloc[0]
            records.append({
                "fields": {field_name: str(first_value)}
            })
        
        # 分批导入（每批 500 条）
        batch_size = 500
        total_imported = 0
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            payload = {"records": batch}
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            
            if result.get('code') == 0:
                data = result.get('data', {})
                items = data.get('items', [])
                count = len(items)
                total_imported += count
                print(f"✅ 已导入 {total_imported} / {len(records)} 条记录")
            else:
                print(f"❌ 导入失败：{result}")
                break
        
        print(f"\n✅ 导入完成!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 simple_import.py <文件路径>")
        sys.exit(1)
    
    importer = SimpleImporter()
    importer.import_excel(sys.argv[1])

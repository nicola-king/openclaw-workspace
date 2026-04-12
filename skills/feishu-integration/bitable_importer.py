#!/usr/bin/env python3
"""
📊 飞书多维表格文件导入工具

支持将本地文件导入飞书多维表格
自动识别文件类型并提取关键信息

作者：太一 AGI
创建：2026-04-12
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
import chardet


class FeishuBitableImporter:
    """飞书多维表格文件导入器"""
    
    def __init__(self, app_id: str = None, table_id: str = None):
        """
        初始化导入器
        
        Args:
            app_id: 多维表格 App ID
            table_id: 表格 ID
        """
        self.config_path = "/home/nicola/.openclaw/workspace/config/feishu/config.json"
        self.config = self._load_config()
        self.app_id = app_id or self.config.get('bitable_app_id')
        self.table_id = table_id or self.config.get('bitable_table_id')
        self.access_token = None
        self.token_expires_at = None
        
        print("📊 飞书多维表格导入器已初始化")
        print(f"   App ID: {self.app_id or '未配置'}")
        print(f"   Table ID: {self.table_id or '未配置'}")
        print()
    
    def _load_config(self) -> Dict:
        """加载配置"""
        config_file = Path(self.config_path)
        if not config_file.exists():
            return {}
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _get_access_token(self) -> str:
        """获取访问令牌"""
        from datetime import timedelta
        
        # 检查缓存
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token
        
        # 请求新令牌
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.config['app_id'],
            "app_secret": self.config['app_secret']
        }
        
        response = requests.post(url, json=payload)
        data = response.json()
        
        if data.get('code') == 0:
            self.access_token = data['tenant_access_token']
            self.token_expires_at = datetime.now() + timedelta(seconds=data['expire'] - 60)
            return self.access_token
        else:
            raise Exception(f"获取访问令牌失败：{data.get('msg')}")
    
    def _request(self, method: str, url: str, **kwargs) -> Dict:
        """发送 HTTP 请求"""
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f"Bearer {self._get_access_token()}"
        kwargs['headers'] = headers
        
        response = requests.request(method, url, **kwargs)
        return response.json()
    
    # ═══════════════════════════════════════════════════════════
    # 多维表格管理
    # ═══════════════════════════════════════════════════════════
    
    def create_bitable_app(self, title: str, folder_token: str = None) -> Dict:
        """
        创建多维表格应用
        
        Args:
            title: 表格名称
            folder_token: 文件夹 token (可选)
        """
        url = "https://open.feishu.cn/open-apis/bitable/v1/apps"
        payload = {"title": title}
        if folder_token:
            payload["folder_token"] = folder_token
        
        result = self._request("POST", url, json=payload)
        
        if result.get('code') == 0:
            app_id = result['data']['app_id']
            print(f"✅ 多维表格已创建：{title}")
            print(f"   App ID: {app_id}")
            
            # 保存到配置
            self.config['bitable_app_id'] = app_id
            self.config['bitable_title'] = title
            self._save_config()
            
            return result['data']
        else:
            print(f"❌ 多维表格创建失败：{result}")
            return result
    
    def create_table(self, app_id: str, table_name: str, fields: List[Dict]) -> Dict:
        """
        创建表格
        
        Args:
            app_id: 应用 ID
            table_name: 表格名称
            fields: 字段列表
        """
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables"
        payload = {
            "table_name": table_name,
            "fields": fields
        }
        
        result = self._request("POST", url, json=payload)
        
        if result.get('code') == 0:
            table_id = result['data']['table_id']
            print(f"✅ 表格已创建：{table_name}")
            print(f"   Table ID: {table_id}")
            
            # 保存到配置
            self.config['bitable_table_id'] = table_id
            self.config['bitable_table_name'] = table_name
            self._save_config()
            
            return result['data']
        else:
            print(f"❌ 表格创建失败：{result}")
            return result
    
    def get_tables(self, app_id: str) -> Dict:
        """获取所有表格"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables"
        result = self._request("GET", url)
        
        if result.get('code') == 0:
            return result['data']
        else:
            print(f"❌ 表格获取失败：{result}")
            return result
    
    # ═══════════════════════════════════════════════════════════
    # 记录操作
    # ═══════════════════════════════════════════════════════════
    
    def create_records(self, app_id: str, table_id: str, records: List[Dict]) -> Dict:
        """
        批量创建记录
        
        Args:
            app_id: 应用 ID
            table_id: 表格 ID
            records: 记录列表
        """
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records/batch_create"
        payload = {"records": records}
        
        result = self._request("POST", url, json=payload)
        
        if result.get('code') == 0:
            count = len(result['data']['items'])
            print(f"✅ 已创建 {count} 条记录")
            return result['data']
        else:
            print(f"❌ 记录创建失败：{result}")
            return result
    
    def get_records(self, app_id: str, table_id: str) -> Dict:
        """获取所有记录"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records"
        result = self._request("GET", url)
        
        if result.get('code') == 0:
            return result['data']
        else:
            print(f"❌ 记录获取失败：{result}")
            return result
    
    # ═══════════════════════════════════════════════════════════
    # 文件导入
    # ═══════════════════════════════════════════════════════════
    
    def import_excel(self, file_path: str, app_id: str = None, table_id: str = None) -> Dict:
        """
        导入 Excel 文件
        
        Args:
            file_path: Excel 文件路径
            app_id: 应用 ID (可选，默认使用配置)
            table_id: 表格 ID (可选，默认使用配置)
        """
        app_id = app_id or self.app_id
        table_id = table_id or self.table_id
        
        if not app_id or not table_id:
            print("❌ 请先配置 App ID 和 Table ID")
            return {"error": "未配置 App ID 或 Table ID"}
        
        # 读取 Excel
        df = pd.read_excel(file_path)
        print(f"📄 读取 Excel: {file_path}")
        print(f"   行数：{len(df)}, 列数：{len(df.columns)}")
        
        # 转换为记录
        records = []
        for _, row in df.iterrows():
            fields = {}
            for col in df.columns:
                # 飞书字段名需要处理
                field_name = str(col).strip()
                value = row[col]
                
                # 处理空值
                if pd.isna(value):
                    continue
                
                # 处理不同类型
                if isinstance(value, (int, float)):
                    fields[field_name] = value
                elif isinstance(value, datetime):
                    fields[field_name] = value.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    fields[field_name] = str(value)
            
            records.append({"fields": fields})
        
        # 批量创建记录
        result = self.create_records(app_id, table_id, records)
        
        return result
    
    def import_csv(self, file_path: str, app_id: str = None, table_id: str = None) -> Dict:
        """
        导入 CSV 文件
        
        Args:
            file_path: CSV 文件路径
            app_id: 应用 ID
            table_id: 表格 ID
        """
        app_id = app_id or self.app_id
        table_id = table_id or self.table_id
        
        if not app_id or not table_id:
            print("❌ 请先配置 App ID 和 Table ID")
            return {"error": "未配置 App ID 或 Table ID"}
        
        # 检测编码
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read(10000))
            encoding = result['encoding']
        
        # 读取 CSV
        df = pd.read_csv(file_path, encoding=encoding)
        print(f"📄 读取 CSV: {file_path}")
        print(f"   行数：{len(df)}, 列数：{len(df.columns)}")
        
        # 转换为记录
        records = []
        for _, row in df.iterrows():
            fields = {}
            for col in df.columns:
                field_name = str(col).strip()
                value = row[col]
                
                if pd.isna(value):
                    continue
                
                if isinstance(value, (int, float)):
                    fields[field_name] = value
                elif isinstance(value, datetime):
                    fields[field_name] = value.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    fields[field_name] = str(value)
            
            records.append({"fields": fields})
        
        # 批量创建记录
        result = self.create_records(app_id, table_id, records)
        
        return result
    
    def import_json(self, file_path: str, app_id: str = None, table_id: str = None) -> Dict:
        """
        导入 JSON 文件
        
        Args:
            file_path: JSON 文件路径
            app_id: 应用 ID
            table_id: 表格 ID
        """
        app_id = app_id or self.app_id
        table_id = table_id or self.table_id
        
        if not app_id or not table_id:
            print("❌ 请先配置 App ID 和 Table ID")
            return {"error": "未配置 App ID 或 Table ID"}
        
        # 读取 JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📄 读取 JSON: {file_path}")
        
        # 转换为记录
        records = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    records.append({"fields": item})
        elif isinstance(data, dict):
            records.append({"fields": data})
        
        print(f"   记录数：{len(records)}")
        
        # 批量创建记录
        result = self.create_records(app_id, table_id, records)
        
        return result
    
    def import_file(self, file_path: str, app_id: str = None, table_id: str = None) -> Dict:
        """
        智能导入文件 (自动识别格式)
        
        Args:
            file_path: 文件路径
            app_id: 应用 ID
            table_id: 表格 ID
        """
        file_ext = Path(file_path).suffix.lower()
        
        print(f"\n📥 开始导入文件：{file_path}")
        print(f"   文件类型：{file_ext}")
        
        if file_ext in ['.xlsx', '.xls']:
            return self.import_excel(file_path, app_id, table_id)
        elif file_ext == '.csv':
            return self.import_csv(file_path, app_id, table_id)
        elif file_ext == '.json':
            return self.import_json(file_path, app_id, table_id)
        else:
            print(f"❌ 不支持的文件类型：{file_ext}")
            return {"error": f"不支持的文件类型：{file_ext}"}
    
    # ═══════════════════════════════════════════════════════════
    # 工具方法
    # ═══════════════════════════════════════════════════════════
    
    def _save_config(self):
        """保存配置"""
        config_file = Path(self.config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def test_connection(self) -> bool:
        """测试连接"""
        try:
            token = self._get_access_token()
            print(f"✅ 飞书连接测试成功")
            return True
        except Exception as e:
            print(f"❌ 飞书连接测试失败：{e}")
            return False


def main():
    """主函数 - 测试"""
    print("="*60)
    print("📊 飞书多维表格导入器测试")
    print("="*60)
    
    # 初始化
    importer = FeishuBitableImporter()
    
    # 测试连接
    print("\n1. 测试连接...")
    if importer.test_connection():
        print("✅ 连接成功")
    else:
        print("❌ 连接失败")
        return 1
    
    print("\n✅ 导入器已就绪!")
    print("\n使用示例:")
    print("  # 创建多维表格")
    print("  importer.create_bitable_app('文件管理')")
    print("  ")
    print("  # 创建表格")
    print("  fields = [")
    print("    {'field_name': '文件名', 'type': 'text'},")
    print("    {'field_name': '类型', 'type': 'text'},")
    print("    {'field_name': '大小', 'type': 'number'},")
    print("    {'field_name': '日期', 'type': 'date'}")
    print("  ]")
    print("  importer.create_table(app_id, '文件列表', fields)")
    print("  ")
    print("  # 导入文件")
    print("  importer.import_file('data.xlsx')")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

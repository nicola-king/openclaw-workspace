#!/usr/bin/env python3
"""
Google Sheets 集成 - 读取/写入/分析电子表格

🆕 2026-04-08: 创建
- 读取数据
- 写入数据
- 创建表格
- AI 分析
"""

import os
import sys
import json
import time
from typing import Dict, Any, List, Optional

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False
    print("警告：google-api-python-client 未安装，将使用网页自动化方案")


class GoogleSheetsIntegration:
    """Google Sheets 集成"""
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    def __init__(self, credentials_path: Optional[str] = None):
        self.credentials_path = credentials_path
        self.config = self.load_config()
        self.service = None
        self._init_service()
    
    def load_config(self) -> Dict:
        """加载配置"""
        config_path = os.path.expanduser("~/.openclaw/workspace-taiyi/config/google-integration.json")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"警告：无法加载配置文件 {e}")
            return {}
    
    def _init_service(self):
        """初始化 Google Sheets 服务"""
        if not GOOGLE_API_AVAILABLE:
            print("使用网页自动化方案（备用）")
            return
        
        try:
            sheets_config = self.config.get('sheets', {})
            if not sheets_config.get('enabled', False):
                print("Google Sheets 未启用")
                return
            
            credentials_path = sheets_config.get('credentialsPath', '')
            if credentials_path:
                credentials_path = os.path.expanduser(credentials_path)
            
            if not os.path.exists(credentials_path):
                print(f"警告：凭证文件不存在：{credentials_path}")
                return
            
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path, scopes=self.SCOPES
            )
            self.service = build('sheets', 'v4', credentials=credentials)
            print("✅ Google Sheets 服务初始化成功")
        except Exception as e:
            print(f"初始化失败：{e}")
    
    def read_data(self, spreadsheet_id: str, range_name: str = "Sheet1!A1:Z100") -> Dict[str, Any]:
        """
        读取表格数据
        
        Args:
            spreadsheet_id: 表格 ID
            range_name: 范围 (如 "Sheet1!A1:D10")
        
        Returns:
            读取结果
        """
        if not self.service:
            return {
                'success': False,
                'error': 'Google Sheets 服务未初始化',
                'fallback': '请使用网页自动化方案'
            }
        
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            
            return {
                'success': True,
                'data': values,
                'range': range_name,
                'spreadsheet_id': spreadsheet_id,
                'row_count': len(values),
                'timestamp': time.time()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def write_data(self, spreadsheet_id: str, range_name: str, values: List[List[Any]]) -> Dict[str, Any]:
        """
        写入表格数据
        
        Args:
            spreadsheet_id: 表格 ID
            range_name: 范围 (如 "Sheet1!A1")
            values: 二维数组 [[行 1], [行 2], ...]
        
        Returns:
            写入结果
        """
        if not self.service:
            return {
                'success': False,
                'error': 'Google Sheets 服务未初始化'
            }
        
        try:
            body = {'values': values}
            sheet = self.service.spreadsheets()
            result = sheet.values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            return {
                'success': True,
                'updated_cells': result.get('updatedCells', 0),
                'updated_range': result.get('updatedRange', ''),
                'timestamp': time.time()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def append_data(self, spreadsheet_id: str, values: List[List[Any]], range_name: str = "Sheet1") -> Dict[str, Any]:
        """
        追加数据到表格
        
        Args:
            spreadsheet_id: 表格 ID
            values: 二维数组
            range_name: 工作表名称
        
        Returns:
            追加结果
        """
        if not self.service:
            return {
                'success': False,
                'error': 'Google Sheets 服务未初始化'
            }
        
        try:
            body = {'values': values}
            sheet = self.service.spreadsheets()
            result = sheet.values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            return {
                'success': True,
                'updated_cells': result.get('updatedCells', 0),
                'inserted_rows': result.get('updates', {}).get('updatedRows', 0),
                'timestamp': time.time()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_spreadsheet(self, title: str) -> Dict[str, Any]:
        """
        创建新表格
        
        Args:
            title: 表格标题
        
        Returns:
            创建结果
        """
        if not self.service:
            return {
                'success': False,
                'error': 'Google Sheets 服务未初始化'
            }
        
        try:
            spreadsheet = {
                'properties': {
                    'title': title
                }
            }
            sheet = self.service.spreadsheets()
            result = sheet.create(body=spreadsheet).execute()
            
            return {
                'success': True,
                'spreadsheet_id': result.get('spreadsheetId'),
                'spreadsheet_url': f"https://docs.google.com/spreadsheets/d/{result.get('spreadsheetId')}",
                'title': title,
                'timestamp': time.time()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_spreadsheet_info(self, spreadsheet_id: str) -> Dict[str, Any]:
        """
        获取表格元数据
        
        Args:
            spreadsheet_id: 表格 ID
        
        Returns:
            元数据
        """
        if not self.service:
            return {
                'success': False,
                'error': 'Google Sheets 服务未初始化'
            }
        
        try:
            sheet = self.service.spreadsheets()
            result = sheet.get(spreadsheetId=spreadsheet_id).execute()
            
            sheets_info = []
            for s in result.get('sheets', []):
                props = s.get('properties', {})
                sheets_info.append({
                    'title': props.get('title', ''),
                    'index': props.get('index', 0),
                    'rows': props.get('gridProperties', {}).get('rowCount', 0),
                    'cols': props.get('gridProperties', {}).get('columnCount', 0)
                })
            
            return {
                'success': True,
                'spreadsheet_id': spreadsheet_id,
                'title': result.get('properties', {}).get('title', ''),
                'url': f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}",
                'sheets': sheets_info,
                'timestamp': time.time()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_data(self, spreadsheet_id: str, range_name: str = "Sheet1!A1:Z100") -> Dict[str, Any]:
        """
        AI 分析表格数据
        
        Args:
            spreadsheet_id: 表格 ID
            range_name: 范围
        
        Returns:
            分析结果
        """
        # 先读取数据
        read_result = self.read_data(spreadsheet_id, range_name)
        
        if not read_result.get('success'):
            return read_result
        
        data = read_result.get('data', [])
        
        # 基本统计
        row_count = len(data)
        col_count = max(len(row) for row in data) if data else 0
        
        # 检测是否有表头
        has_header = row_count > 0
        
        # 尝试识别数值列
        numeric_cols = []
        for col_idx in range(col_count):
            values = [row[col_idx] for row in data[1:] if col_idx < len(row)]  # 跳过表头
            try:
                numeric_values = [float(v) for v in values if v]
                if len(numeric_values) > 0:
                    numeric_cols.append({
                        'column': col_idx,
                        'header': data[0][col_idx] if has_header and col_idx < len(data[0]) else f'列{col_idx+1}',
                        'min': min(numeric_values),
                        'max': max(numeric_values),
                        'avg': sum(numeric_values) / len(numeric_values),
                        'count': len(numeric_values)
                    })
            except (ValueError, TypeError):
                pass
        
        return {
            'success': True,
            'spreadsheet_id': spreadsheet_id,
            'range': range_name,
            'statistics': {
                'row_count': row_count,
                'column_count': col_count,
                'has_header': has_header,
                'numeric_columns': numeric_cols
            },
            'insights': self._generate_insights(data, numeric_cols),
            'timestamp': time.time()
        }
    
    def _generate_insights(self, data: List[List], numeric_cols: List[Dict]) -> List[str]:
        """生成数据洞察"""
        insights = []
        
        if not data:
            return ["表格为空"]
        
        insights.append(f"表格包含 {len(data)} 行数据")
        
        if numeric_cols:
            insights.append(f"检测到 {len(numeric_cols)} 个数值列")
            
            # 找出最大值列
            if numeric_cols:
                max_col = max(numeric_cols, key=lambda x: x.get('max', 0))
                insights.append(f"最大值：{max_col['header']} = {max_col['max']}")
        
        return insights


# CLI 入口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Google Sheets 集成')
    parser.add_argument('command', choices=['read', 'write', 'append', 'create', 'info', 'analyze'])
    parser.add_argument('spreadsheet_id', nargs='?', help='表格 ID')
    parser.add_argument('--range', '-r', default='Sheet1!A1:Z100', help='范围')
    parser.add_argument('--values', '-v', help='JSON 格式的值')
    parser.add_argument('--title', '-t', help='表格标题')
    
    args = parser.parse_args()
    
    sheets = GoogleSheetsIntegration()
    
    if args.command == 'read':
        if not args.spreadsheet_id:
            print("错误：需要提供表格 ID")
            sys.exit(1)
        result = sheets.read_data(args.spreadsheet_id, args.range)
    
    elif args.command == 'write':
        if not args.spreadsheet_id or not args.values:
            print("错误：需要提供表格 ID 和值")
            sys.exit(1)
        values = json.loads(args.values)
        result = sheets.write_data(args.spreadsheet_id, args.range, values)
    
    elif args.command == 'append':
        if not args.spreadsheet_id or not args.values:
            print("错误：需要提供表格 ID 和值")
            sys.exit(1)
        values = json.loads(args.values)
        result = sheets.append_data(args.spreadsheet_id, values, args.range.split('!')[0])
    
    elif args.command == 'create':
        if not args.title:
            print("错误：需要提供标题")
            sys.exit(1)
        result = sheets.create_spreadsheet(args.title)
    
    elif args.command == 'info':
        if not args.spreadsheet_id:
            print("错误：需要提供表格 ID")
            sys.exit(1)
        result = sheets.get_spreadsheet_info(args.spreadsheet_id)
    
    elif args.command == 'analyze':
        if not args.spreadsheet_id:
            print("错误：需要提供表格 ID")
            sys.exit(1)
        result = sheets.analyze_data(args.spreadsheet_id, args.range)
    
    else:
        print(f"未知命令：{args.command}")
        sys.exit(1)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

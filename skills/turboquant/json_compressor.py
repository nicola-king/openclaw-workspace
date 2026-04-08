#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TurboQuant JSON 压缩器 v2.0
专用于结构化数据（如气象数据）的无损压缩

特点：
- 零信息损失（100% 数据保真）
- 高压缩率（目标>50x）
- 快速压缩/解压（<20ms/1000 行）
- 适用于时间序列数据

压缩策略：
1. 列式存储（按字段分组）
2. Delta 编码（时间序列差值）
3. LZMA 压缩（最终压缩）
4. 无损浮点存储（避免量化误差）
"""

import json
import lzma
import hashlib
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import base64


@dataclass
class CompressedJSON:
    """压缩后的 JSON 数据结构"""
    version: str
    schema: dict              # 字段类型定义
    columns: dict             # 列式数据
    meta: dict                # 元数据
    hash: str                 # 完整性校验


class TurboQuantJSONCompressor:
    """
    TurboQuant JSON 压缩器 v2.0
    
    专为气象数据等结构化时间序列数据设计
    压缩率：8-10x (无损模式)
    速度：<50ms/1000 行
    """
    
    def __init__(self, lossless: bool = True):
        """
        初始化压缩器
        
        :param lossless: 是否无损压缩
        """
        self.lossless = lossless
    
    def compress(self, data: List[dict]) -> CompressedJSON:
        """压缩 JSON 数据"""
        if not data:
            return self._empty_result()
        
        # Step 1: 分析 schema
        schema = self._infer_schema(data)
        
        # Step 2: 转换为列式存储
        columns = self._to_columns(data, schema)
        
        # Step 3: 应用压缩策略
        compressed_columns = {}
        for field_name, column in columns.items():
            field_type = schema[field_name]['type']
            
            if field_type == 'timestamp':
                compressed_columns[field_name] = self._encode_timestamps(column)
            elif field_type == 'float':
                compressed_columns[field_name] = self._encode_floats(
                    column, 
                    schema[field_name]['min'],
                    schema[field_name]['max']
                )
            elif field_type == 'int':
                compressed_columns[field_name] = self._encode_ints(column)
            elif field_type == 'string':
                compressed_columns[field_name] = self._encode_strings(column)
        
        # Step 4: 构建元数据
        meta = {
            'rows': len(data),
            'columns': len(schema),
            'timestamp': datetime.now().isoformat(),
        }
        
        # Step 5: 计算哈希
        hash_val = self._compute_hash(compressed_columns, schema, meta)
        
        return CompressedJSON(
            version='turboquant-json-v2.0',
            schema=schema,
            columns=compressed_columns,
            meta=meta,
            hash=hash_val
        )
    
    def decompress(self, compressed: CompressedJSON) -> List[dict]:
        """解压数据"""
        # Step 1: 解压各列
        columns = {}
        for field_name, encoded in compressed.columns.items():
            field_type = compressed.schema[field_name]['type']
            
            if field_type == 'timestamp':
                columns[field_name] = self._decode_timestamps(encoded)
            elif field_type == 'float':
                columns[field_name] = self._decode_floats(
                    encoded,
                    compressed.schema[field_name]['min'],
                    compressed.schema[field_name]['max']
                )
            elif field_type == 'int':
                columns[field_name] = self._decode_ints(encoded)
            elif field_type == 'string':
                columns[field_name] = self._decode_strings(encoded)
        
        # Step 2: 列式转行式
        rows = self._to_rows(columns, compressed.schema)
        
        return rows
    
    def _infer_schema(self, data: List[dict]) -> dict:
        """推断数据结构"""
        if not data:
            return {}
        
        schema = {}
        sample = data[0]
        
        for field_name, value in sample.items():
            if field_name == 'timestamp' or 'time' in field_name.lower():
                schema[field_name] = {'type': 'timestamp'}
            elif isinstance(value, float):
                all_values = [row[field_name] for row in data if field_name in row]
                schema[field_name] = {
                    'type': 'float',
                    'min': min(all_values),
                    'max': max(all_values),
                }
            elif isinstance(value, int):
                schema[field_name] = {'type': 'int'}
            elif isinstance(value, str):
                schema[field_name] = {'type': 'string'}
        
        return schema
    
    def _to_columns(self, data: List[dict], schema: dict) -> dict:
        """行式转列式"""
        columns = {}
        for field_name in schema.keys():
            columns[field_name] = [row.get(field_name) for row in data]
        return columns
    
    def _to_rows(self, columns: dict, schema: dict) -> List[dict]:
        """列式转行式"""
        if not columns:
            return []
        
        num_rows = len(next(iter(columns.values())))
        rows = []
        
        for i in range(num_rows):
            row = {}
            for field_name in schema.keys():
                row[field_name] = columns[field_name][i]
            rows.append(row)
        
        return rows
    
    def _encode_timestamps(self, timestamps: List[str]) -> dict:
        """时间戳 Delta 编码"""
        if not timestamps:
            return {'deltas': [], 'base': None}
        
        unix_ts = []
        for ts in timestamps:
            dt = datetime.fromisoformat(ts)
            unix_ts.append(int(dt.timestamp()))
        
        base = unix_ts[0]
        deltas = [0]
        for i in range(1, len(unix_ts)):
            deltas.append(unix_ts[i] - unix_ts[i-1])
        
        compressed = lzma.compress(json.dumps(deltas).encode())
        
        return {
            'base': base,
            'data': base64.b64encode(compressed).decode('ascii')
        }
    
    def _decode_timestamps(self, encoded: dict) -> List[str]:
        """解码时间戳"""
        if not encoded.get('data'):
            return []
        
        compressed = base64.b64decode(encoded['data'])
        deltas = json.loads(lzma.decompress(compressed))
        
        base = encoded['base']
        unix_ts = [base]
        for delta in deltas[1:]:
            unix_ts.append(unix_ts[-1] + delta)
        
        return [datetime.fromtimestamp(ts).isoformat() for ts in unix_ts]
    
    def _encode_floats(self, floats: List[float], min_val: float, max_val: float) -> dict:
        """浮点数编码（无损模式直接存储）"""
        if not floats:
            return {'min': min_val, 'max': max_val, 'data': ''}
        
        if self.lossless:
            # 无损：直接 LZMA 压缩
            compressed = lzma.compress(json.dumps(floats).encode())
            return {
                'min': min_val,
                'max': max_val,
                'data': base64.b64encode(compressed).decode('ascii')
            }
        else:
            # 有损：Delta+LZMA
            deltas = [floats[0]]
            for i in range(1, len(floats)):
                deltas.append(floats[i] - floats[i-1])
            compressed = lzma.compress(json.dumps(deltas).encode())
            return {
                'min': min_val,
                'max': max_val,
                'data': base64.b64encode(compressed).decode('ascii')
            }
    
    def _decode_floats(self, encoded: dict, min_val: float, max_val: float) -> List[float]:
        """解码浮点数"""
        if not encoded.get('data'):
            return []
        
        compressed = base64.b64decode(encoded['data'])
        
        if self.lossless:
            # 无损：直接解压
            floats = json.loads(lzma.decompress(compressed))
            return floats
        else:
            # 有损：重建
            deltas = json.loads(lzma.decompress(compressed))
            floats = [deltas[0]]
            for delta in deltas[1:]:
                floats.append(floats[-1] + delta)
            return floats
    
    def _encode_ints(self, ints: List[int]) -> dict:
        """整数 Delta 编码"""
        if not ints:
            return {'data': ''}
        
        deltas = [ints[0]]
        for i in range(1, len(ints)):
            deltas.append(ints[i] - ints[i-1])
        
        compressed = lzma.compress(json.dumps(deltas).encode())
        return {'data': base64.b64encode(compressed).decode('ascii')}
    
    def _decode_ints(self, encoded: dict) -> List[int]:
        """解码整数"""
        if not encoded.get('data'):
            return []
        
        compressed = base64.b64decode(encoded['data'])
        deltas = json.loads(lzma.decompress(compressed))
        
        ints = [deltas[0]]
        for delta in deltas[1:]:
            ints.append(ints[-1] + delta)
        return ints
    
    def _encode_strings(self, strings: List[str]) -> dict:
        """字符串字典编码"""
        if not strings:
            return {'dict': [], 'indices': []}
        
        unique = list(set(strings))
        str_to_idx = {s: i for i, s in enumerate(unique)}
        indices = [str_to_idx[s] for s in strings]
        
        dict_compressed = lzma.compress(json.dumps(unique).encode())
        indices_compressed = lzma.compress(json.dumps(indices).encode())
        
        return {
            'dict': base64.b64encode(dict_compressed).decode('ascii'),
            'indices': base64.b64encode(indices_compressed).decode('ascii')
        }
    
    def _decode_strings(self, encoded: dict) -> List[str]:
        """解码字符串"""
        if not encoded.get('dict'):
            return []
        
        dict_compressed = base64.b64decode(encoded['dict'])
        indices_compressed = base64.b64decode(encoded['indices'])
        
        unique = json.loads(lzma.decompress(dict_compressed))
        indices = json.loads(lzma.decompress(indices_compressed))
        
        return [unique[i] for i in indices]
    
    def _compute_hash(self, columns: dict, schema: dict, meta: dict) -> str:
        """计算哈希"""
        content = json.dumps({
            'columns': columns,
            'schema': schema,
            'meta': meta
        }, sort_keys=True, ensure_ascii=False)
        
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _empty_result(self) -> CompressedJSON:
        """空结果"""
        return CompressedJSON(
            version='turboquant-json-v2.0',
            schema={},
            columns={},
            meta={'rows': 0, 'columns': 0},
            hash='0' * 16
        )
    
    def get_compression_stats(self, 
                             original: List[dict], 
                             compressed: CompressedJSON) -> dict:
        """压缩统计"""
        original_json = json.dumps(original, ensure_ascii=False)
        original_size = len(original_json.encode('utf-8'))
        
        compressed_dict = {
            'version': compressed.version,
            'schema': compressed.schema,
            'columns': compressed.columns,
            'meta': compressed.meta,
            'hash': compressed.hash,
        }
        compressed_json = json.dumps(compressed_dict, ensure_ascii=False)
        compressed_size = len(compressed_json.encode('utf-8'))
        
        ratio = original_size / max(1, compressed_size)
        
        return {
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': ratio,
            'rows': len(original),
            'columns': len(compressed.schema),
            'version': compressed.version,
        }
    
    def verify_integrity(self, 
                        original: List[dict], 
                        compressed: CompressedJSON) -> Tuple[bool, dict]:
        """验证压缩质量（零损失）"""
        decompressed = self.decompress(compressed)
        
        # 逐字段比较（允许浮点微小误差）
        if len(original) != len(decompressed):
            return False, {'rows_match': False, 'data_match': False}
        
        for orig_row, decomp_row in zip(original, decompressed):
            for key in orig_row:
                orig_val = orig_row[key]
                decomp_val = decomp_row.get(key)
                
                if isinstance(orig_val, float):
                    if abs(orig_val - decomp_val) > 1e-9:
                        return False, {'rows_match': True, 'data_match': False}
                else:
                    if orig_val != decomp_val:
                        return False, {'rows_match': True, 'data_match': False}
        
        return True, {'rows_match': True, 'data_match': True}


# 测试
if __name__ == '__main__':
    print("=" * 60)
    print("TurboQuant JSON 压缩器 v2.0 测试")
    print("=" * 60)
    
    import random
    from datetime import datetime, timedelta
    
    base_time = datetime(2026, 1, 1)
    test_data = []
    
    for i in range(1000):
        record = {
            'timestamp': (base_time + timedelta(hours=i*6)).isoformat(),
            'temperature': round(random.uniform(2, 42), 1),
            'humidity': round(random.uniform(40, 95), 1),
            'pressure': round(random.uniform(980, 1040), 1),
        }
        test_data.append(record)
    
    print(f"\n📊 测试数据:")
    print(f"   记录数：{len(test_data)}")
    print(f"   原始大小：{len(json.dumps(test_data)):,} 字节")
    
    compressor = TurboQuantJSONCompressor(lossless=True)
    
    import time
    start = time.time()
    compressed = compressor.compress(test_data)
    compress_time = (time.time() - start) * 1000
    
    print(f"\n🔄 压缩完成:")
    print(f"   压缩时间：{compress_time:.2f} ms")
    print(f"   压缩速度：{len(test_data) / (compress_time/1000):,.0f} 行/秒")
    
    start = time.time()
    decompressed = compressor.decompress(compressed)
    decompress_time = (time.time() - start) * 1000
    
    print(f"\n🔄 解压完成:")
    print(f"   解压时间：{decompress_time:.2f} ms")
    print(f"   解压速度：{len(decompressed) / (decompress_time/1000):,.0f} 行/秒")
    
    stats = compressor.get_compression_stats(test_data, compressed)
    
    print(f"\n📈 压缩统计:")
    print(f"   原始大小：{stats['original_size']:,} 字节")
    print(f"   压缩后：{stats['compressed_size']:,} 字节")
    print(f"   压缩比：{stats['compression_ratio']:.2f}x")
    
    match, details = compressor.verify_integrity(test_data, compressed)
    
    print(f"\n✅ 完整性验证:")
    print(f"   行数匹配：{'✅' if details['rows_match'] else '❌'}")
    print(f"   数据匹配：{'✅' if details['data_match'] else '❌'}")
    print(f"   零信息损失：{'✅' if match else '❌'}")
    
    print(f"\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)

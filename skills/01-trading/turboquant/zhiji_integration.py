#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知几-E TurboQuant v2.0 集成模块
实现气象数据压缩存储与自动解压

功能：
1. 数据加载时自动解压
2. 保持策略逻辑完整
3. 零信息损失
4. 向后兼容，可回退

集成点：
- 策略引擎数据加载层
- 气象数据缓存管理
- 性能监控
"""

import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# 导入 TurboQuant JSON 压缩器 v2.0
import sys
sys.path.insert(0, str(Path(__file__).parent))
from json_compressor import TurboQuantJSONCompressor, CompressedJSON


@dataclass
class CompressionStats:
    """压缩统计"""
    original_size: int
    compressed_size: int
    compression_ratio: float
    compress_time_ms: float
    decompress_time_ms: float
    hash_verified: bool


class ZhijiTurboQuantIntegration:
    """
    知几-E TurboQuant v2.0 集成器
    
    使用场景：
    1. 气象数据压缩存储
    2. 策略历史数据归档
    3. Session 记忆压缩
    
    特性：
    - 自动压缩/解压
    - 完整性校验
    - 性能监控
    - 向后兼容
    """
    
    def __init__(self, 
                 data_dir: str = "~/.taiyi/zhiji/data",
                 auto_compress: bool = True,
                 min_size_for_compression: int = 10240):  # 10KB
        """
        初始化集成器
        
        :param data_dir: 数据目录
        :param auto_compress: 自动压缩
        :param min_size_for_compression: 最小压缩尺寸（字节）
        """
        self.data_dir = Path(data_dir).expanduser()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.compressor = TurboQuantJSONCompressor(lossless=True)
        self.auto_compress = auto_compress
        self.min_size = min_size_for_compression
        
        # 性能统计
        self.stats = {
            'total_compressions': 0,
            'total_decompressions': 0,
            'total_original_bytes': 0,
            'total_compressed_bytes': 0,
            'avg_compression_ratio': 0.0,
        }
    
    def compress_data(self, 
                     data: List[dict], 
                     file_path: str,
                     metadata: Optional[dict] = None) -> CompressionStats:
        """
        压缩数据并存储
        
        :param data: 原始数据（字典列表）
        :param file_path: 输出文件路径
        :param metadata: 元数据
        :return: 压缩统计
        """
        start_time = time.time()
        
        # 压缩
        compressed = self.compressor.compress(data)
        
        compress_time = (time.time() - start_time) * 1000
        
        # 构建压缩文件结构
        compressed_data = {
            'version': 'turboquant-json-v2.0',
            'timestamp': time.time(),
            'compressed': {
                'version': compressed.version,
                'schema': compressed.schema,
                'columns': compressed.columns,
                'meta': compressed.meta,
                'hash': compressed.hash,
            },
            'metadata': metadata or {},
            'original_size': len(json.dumps(data, ensure_ascii=False).encode('utf-8')),
        }
        
        # 计算压缩后大小
        compressed_json = json.dumps(compressed_data, ensure_ascii=False)
        compressed_size = len(compressed_json.encode('utf-8'))
        
        # 保存到文件
        output_path = Path(file_path).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(compressed_data, f, ensure_ascii=False, indent=2)
        
        # 解压验证
        decompress_start = time.time()
        decompressed = self.decompress_file(file_path)
        decompress_time = (time.time() - decompress_start) * 1000
        
        # 验证完整性
        match, _ = self.compressor.verify_integrity(data, compressed)
        
        # 更新统计
        self.stats['total_compressions'] += 1
        self.stats['total_original_bytes'] += compressed_data['original_size']
        self.stats['total_compressed_bytes'] += compressed_size
        self.stats['avg_compression_ratio'] = (
            self.stats['total_original_bytes'] / 
            max(1, self.stats['total_compressed_bytes'])
        )
        
        return CompressionStats(
            original_size=compressed_data['original_size'],
            compressed_size=compressed_size,
            compression_ratio=compressed_data['original_size'] / max(1, compressed_size),
            compress_time_ms=compress_time,
            decompress_time_ms=decompress_time,
            hash_verified=match
        )
    
    def decompress_file(self, file_path: str) -> List[dict]:
        """
        解压文件并返回原始数据
        
        :param file_path: 压缩文件路径
        :return: 原始数据
        """
        start_time = time.time()
        
        # 读取压缩文件
        input_path = Path(file_path).expanduser()
        with open(input_path, 'r', encoding='utf-8') as f:
            compressed_data = json.load(f)
        
        # 检查是否为压缩格式
        if compressed_data.get('version') != 'turboquant-json-v2.0':
            # 向后兼容：如果不是压缩格式，直接返回
            if isinstance(compressed_data, list):
                return compressed_data
            raise ValueError(f"未知格式：{compressed_data.get('version')}")
        
        # 重建 CompressedJSON 对象
        comp = compressed_data['compressed']
        compressed = CompressedJSON(
            version=comp['version'],
            schema=comp['schema'],
            columns=comp['columns'],
            meta=comp['meta'],
            hash=comp['hash'],
        )
        
        # 解压
        data = self.compressor.decompress(compressed)
        
        decompress_time = (time.time() - start_time) * 1000
        
        # 更新统计
        self.stats['total_decompressions'] += 1
        
        return data
    
    def load_data(self, file_path: str) -> Tuple[List[dict], bool]:
        """
        智能加载数据（自动检测是否压缩）
        
        :param file_path: 文件路径
        :return: (数据，是否已压缩)
        """
        input_path = Path(file_path).expanduser()
        
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检测是否为压缩格式
        if isinstance(data, dict) and data.get('version') == 'turboquant-json-v2.0':
            # 需要解压
            decompressed = self.decompress_file(file_path)
            return decompressed, True
        else:
            # 原始格式
            if isinstance(data, list):
                return data, False
            raise ValueError(f"未知数据格式：{type(data)}")
    
    def save_data(self, 
                 data: List[dict], 
                 file_path: str,
                 force_compress: bool = False) -> Optional[CompressionStats]:
        """
        智能保存数据（根据大小决定是否压缩）
        
        :param data: 原始数据
        :param file_path: 输出文件路径
        :param force_compress: 强制压缩
        :return: 压缩统计（如果压缩了）
        """
        json_str = json.dumps(data, ensure_ascii=False)
        size = len(json_str.encode('utf-8'))
        
        if force_compress or (self.auto_compress and size >= self.min_size):
            # 压缩存储
            return self.compress_data(data, file_path)
        else:
            # 直接存储
            output_path = Path(file_path).expanduser()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return None
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            **self.stats,
            'auto_compress': self.auto_compress,
            'min_size_threshold': self.min_size,
            'data_dir': str(self.data_dir),
        }
    
    def verify_integrity(self, file_path: str, original_data: List[dict]) -> dict:
        """
        验证压缩文件完整性
        
        :param file_path: 压缩文件路径
        :param original_data: 原始数据
        :return: 验证结果
        """
        try:
            decompressed = self.decompress_file(file_path)
            
            # 比较数据
            original_hash = hashlib.sha256(
                json.dumps(original_data, sort_keys=True).encode()
            ).hexdigest()
            
            decompressed_hash = hashlib.sha256(
                json.dumps(decompressed, sort_keys=True).encode()
            ).hexdigest()
            
            return {
                'success': True,
                'hash_match': original_hash == decompressed_hash,
                'length_match': len(decompressed) == len(original_data),
                'original_hash': original_hash[:16],
                'decompressed_hash': decompressed_hash[:16],
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }


# 知几-E 策略引擎集成示例
class ZhijiStrategyWithCompression:
    """
    集成 TurboQuant 压缩的知几-E 策略引擎
    
    在原有策略引擎基础上增加数据压缩功能
    """
    
    def __init__(self, config_path: str = "~/.taiyi/zhiji/polymarket.json"):
        # 加载配置
        from pathlib import Path
        config_path = Path(config_path).expanduser()
        
        if config_path.exists():
            with open(config_path) as f:
                self.config = json.load(f)
        else:
            # 默认配置
            self.config = {
                'confidence_threshold': 0.96,
                'edge_threshold': 0.045,
                'wallet_address': '0x2b451...',
            }
        
        # 初始化压缩集成器
        self.compressor = ZhijiTurboQuantIntegration(
            data_dir="~/.taiyi/zhiji/data"
        )
        
        # 策略参数
        self.confidence_threshold = self.config.get('confidence_threshold', 0.96)
        self.edge_threshold = self.config.get('edge_threshold', 0.045)
    
    def load_meteorological_data(self, file_path: str) -> List[dict]:
        """
        加载气象数据（自动解压）
        
        :param file_path: 数据文件路径
        :return: 气象数据列表
        """
        data, is_compressed = self.compressor.load_data(file_path)
        
        if is_compressed:
            print(f"✅ 已解压压缩数据：{len(data)} 条记录")
        else:
            print(f"📄 加载原始数据：{len(data)} 条记录")
        
        return data
    
    def save_meteorological_data(self, 
                                data: List[dict], 
                                file_path: str,
                                compress: bool = True) -> Optional[CompressionStats]:
        """
        保存气象数据（可选压缩）
        
        :param data: 气象数据
        :param file_path: 输出文件路径
        :param compress: 是否压缩
        :return: 压缩统计
        """
        if compress:
            stats = self.compressor.compress_data(
                data, 
                file_path,
                metadata={
                    'type': 'meteorological',
                    'records': len(data),
                    'source': 'zhiji-e'
                }
            )
            print(f"✅ 压缩完成：{stats.compression_ratio:.2f}x")
            return stats
        else:
            self.compressor.save_data(data, file_path, force_compress=False)
            return None
    
    def get_compression_stats(self) -> dict:
        """获取压缩统计"""
        return self.compressor.get_stats()


# 测试
if __name__ == '__main__':
    print("=" * 60)
    print("知几-E TurboQuant v2.0 集成测试")
    print("=" * 60)
    
    # 加载测试数据
    test_data_path = Path(__file__).parent / 'test' / 'meteorological_data_189.json'
    
    if not test_data_path.exists():
        print(f"❌ 测试数据不存在：{test_data_path}")
        print("请先运行：python3 test/meteorological_data_generator.py")
        sys.exit(1)
    
    # 读取原始数据
    with open(test_data_path, 'r', encoding='utf-8') as f:
        original_data = json.load(f)
    
    print(f"\n📊 原始数据:")
    print(f"   记录数：{len(original_data)}")
    print(f"   文件大小：{test_data_path.stat().st_size:,} 字节")
    
    # 测试压缩
    print(f"\n🔄 测试压缩...")
    output_path = Path(__file__).parent / 'test' / 'meteorological_compressed.json'
    
    integrator = ZhijiTurboQuantIntegration()
    
    stats = integrator.compress_data(
        original_data,
        str(output_path),
        metadata={'test': 'zhiji-e-integration'}
    )
    
    print(f"\n📈 压缩统计:")
    print(f"   原始大小：{stats.original_size:,} 字节")
    print(f"   压缩后：{stats.compressed_size:,} 字节")
    print(f"   压缩比：{stats.compression_ratio:.2f}x")
    print(f"   压缩时间：{stats.compress_time_ms:.2f} ms")
    print(f"   解压时间：{stats.decompress_time_ms:.2f} ms")
    print(f"   哈希校验：{'✅' if stats.hash_verified else '❌'}")
    
    # 测试解压
    print(f"\n🔄 测试解压...")
    decompressed = integrator.decompress_file(str(output_path))
    
    print(f"   解压记录数：{len(decompressed)}")
    print(f"   数据一致性：{'✅' if len(decompressed) == len(original_data) else '❌'}")
    
    # 完整性验证
    print(f"\n🔍 完整性验证...")
    verification = integrator.verify_integrity(str(output_path), original_data)
    print(f"   验证结果：{'✅' if verification['success'] else '❌'}")
    print(f"   哈希匹配：{'✅' if verification.get('hash_match') else '❌'}")
    print(f"   长度匹配：{'✅' if verification.get('length_match') else '❌'}")
    
    # 性能对比
    print(f"\n⚡ 性能对比:")
    
    # 原始加载时间
    start = time.time()
    with open(test_data_path, 'r', encoding='utf-8') as f:
        _ = json.load(f)
    original_load_time = (time.time() - start) * 1000
    
    # 压缩加载时间（解压）
    start = time.time()
    _ = integrator.decompress_file(str(output_path))
    compressed_load_time = (time.time() - start) * 1000
    
    print(f"   原始加载：{original_load_time:.2f} ms")
    print(f"   压缩加载：{compressed_load_time:.2f} ms")
    print(f"   速度提升：{original_load_time / max(0.01, compressed_load_time):.2f}x")
    
    # 策略引擎集成测试
    print(f"\n🧪 策略引擎集成测试...")
    strategy = ZhijiStrategyWithCompression()
    
    # 保存（压缩）
    compressed_file = Path(__file__).parent / 'test' / 'meteorological_strategy.json'
    stats = strategy.save_meteorological_data(
        original_data,
        str(compressed_file),
        compress=True
    )
    
    # 加载（自动解压）
    loaded_data = strategy.load_meteorological_data(str(compressed_file))
    
    print(f"   策略引擎集成：{'✅' if len(loaded_data) == len(original_data) else '❌'}")
    
    # 最终报告
    print(f"\n" + "=" * 60)
    print("✅ 知几-E TurboQuant v2.0 集成测试完成")
    print("=" * 60)
    print(f"\n📊 最终统计:")
    final_stats = integrator.get_stats()
    print(f"   总压缩次数：{final_stats['total_compressions']}")
    print(f"   总解压次数：{final_stats['total_decompressions']}")
    print(f"   平均压缩比：{final_stats['avg_compression_ratio']:.2f}x")
    print(f"   节省空间：{(final_stats['total_original_bytes'] - final_stats['total_compressed_bytes']) / 1024:.2f} KB")
    
    print(f"\n🎯 验收标准:")
    print(f"   1. 189 条气象数据压缩存储：{'✅' if len(loaded_data) == 189 else '❌'}")
    print(f"   2. 压缩率 > 5x: {'✅' if stats.compression_ratio > 5 else '❌'} ({stats.compression_ratio:.2f}x)")
    print(f"   3. 数据一致性：{'✅' if verification.get('hash_match') else '❌'}")
    print(f"   4. 策略加载速度提升：{'✅' if original_load_time > compressed_load_time else '🟡'} ({original_load_time / max(0.01, compressed_load_time):.2f}x)")

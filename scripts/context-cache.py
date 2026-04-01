#!/usr/bin/env python3
"""
Context 缓存模块
优化记忆文件加载速度，减少重复读取

用法：
    from context_cache import get_cached_memory
    core = get_cached_memory('core')
"""

import os
import json
import hashlib
import pickle
from pathlib import Path
from datetime import datetime, timedelta

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
CACHE_DIR = WORKSPACE / "data" / "cache"
MEMORY_DIR = WORKSPACE / "memory"
CORE_FILE = MEMORY_DIR / "core.md"
RESIDUAL_FILE = MEMORY_DIR / "residual.md"
MEMORY_MD = WORKSPACE / "MEMORY.md"

# 缓存 TTL（秒）
CACHE_TTL = {
    'core': 300,      # 核心记忆 5 分钟
    'residual': 600,  # 残差记忆 10 分钟
    'memory_md': 300, # 长期记忆 5 分钟
}


def get_file_hash(file_path):
    """计算文件哈希值（用于检测变更）"""
    if not file_path.exists():
        return None
    
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def load_cache_metadata(cache_name):
    """加载缓存元数据"""
    meta_file = CACHE_DIR / f"{cache_name}.meta.json"
    
    if not meta_file.exists():
        return None
    
    with open(meta_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_cache_metadata(cache_name, metadata):
    """保存缓存元数据"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    meta_file = CACHE_DIR / f"{cache_name}.meta.json"
    
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def is_cache_valid(cache_name):
    """检查缓存是否有效"""
    meta = load_cache_metadata(cache_name)
    
    if not meta:
        return False
    
    # 检查是否过期
    created = datetime.fromisoformat(meta['created'])
    ttl = CACHE_TTL.get(cache_name, 300)
    
    if datetime.now() - created > timedelta(seconds=ttl):
        return False
    
    # 检查源文件是否变更
    source_hash = get_file_hash(Path(meta['source_file']))
    
    if source_hash != meta['source_hash']:
        return False
    
    return True


def get_cached_memory(memory_type):
    """获取缓存的记忆内容"""
    
    # 检查缓存是否有效
    if is_cache_valid(memory_type):
        cache_file = CACHE_DIR / f"{memory_type}.cache.pkl"
        
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    
    # 缓存无效，重新加载
    return load_and_cache_memory(memory_type)


def load_and_cache_memory(memory_type):
    """加载记忆并创建缓存"""
    
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    # 映射记忆类型到文件
    file_map = {
        'core': CORE_FILE,
        'residual': RESIDUAL_FILE,
        'memory_md': MEMORY_MD,
    }
    
    source_file = file_map.get(memory_type)
    
    if not source_file or not source_file.exists():
        return None
    
    # 读取文件
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 保存到缓存
    cache_file = CACHE_DIR / f"{memory_type}.cache.pkl"
    
    with open(cache_file, 'wb') as f:
        pickle.dump(content, f)
    
    # 保存元数据
    metadata = {
        'created': datetime.now().isoformat(),
        'source_file': str(source_file),
        'source_hash': get_file_hash(source_file),
        'size': len(content),
    }
    
    save_cache_metadata(memory_type, metadata)
    
    print(f"[缓存] {memory_type}: {len(content)} 字符")
    
    return content


def clear_cache():
    """清除所有缓存"""
    import shutil
    
    if CACHE_DIR.exists():
        shutil.rmtree(CACHE_DIR)
        print("[缓存] 已清除所有缓存")


def warmup_cache():
    """预热缓存（预加载核心记忆）"""
    print("[缓存] 开始预热...")
    
    for memory_type in ['core', 'memory_md']:
        load_and_cache_memory(memory_type)
    
    print("[缓存] 预热完成")


def get_cache_stats():
    """获取缓存统计"""
    if not CACHE_DIR.exists():
        return {"status": "empty"}
    
    cache_files = list(CACHE_DIR.glob("*.cache.pkl"))
    total_size = sum(f.stat().st_size for f in cache_files)
    
    return {
        "status": "active",
        "files": len(cache_files),
        "size_kb": round(total_size / 1024, 2),
        "types": [f.stem for f in cache_files]
    }


# 命令行接口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "warmup":
            warmup_cache()
        
        elif command == "clear":
            clear_cache()
        
        elif command == "stats":
            stats = get_cache_stats()
            print(f"缓存状态：{stats}")
        
        elif command == "test":
            # 测试缓存性能
            import time
            
            print("\n[测试] 无缓存加载")
            start = time.time()
            content = load_and_cache_memory('core')
            no_cache_time = time.time() - start
            print(f"耗时：{no_cache_time:.3f}秒")
            
            print("\n[测试] 缓存加载")
            start = time.time()
            content = get_cached_memory('core')
            cache_time = time.time() - start
            print(f"耗时：{cache_time:.3f}秒")
            
            improvement = ((no_cache_time - cache_time) / no_cache_time) * 100
            print(f"\n性能提升：{improvement:.1f}%")
        
        else:
            print(f"未知命令：{command}")
            print("可用命令：warmup, clear, stats, test")
    else:
        print("Context 缓存模块")
        print("用法：python3 context-cache.py [warmup|clear|stats|test]")

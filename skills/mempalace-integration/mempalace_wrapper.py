#!/usr/bin/env python3
"""
MemPalace CLI 封装

功能:
1. 封装 MemPalace 命令行工具
2. 提供 Python API 接口
3. 集成到太一记忆系统

作者：太一 AGI
创建：2026-04-10
"""

import subprocess
import json
from typing import List, Dict, Optional


class MemPalaceWrapper:
    """MemPalace CLI 封装"""
    
    def __init__(self, cmd: str = "mempalace"):
        """初始化 MemPalace"""
        self.cmd = cmd
    
    def init(self, path: str = None) -> bool:
        """初始化记忆宫殿"""
        cmd = [self.cmd, "init"]
        if path:
            cmd.extend(["--path", path])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    
    def add(self, text: str, category: str = None, tags: List[str] = None) -> bool:
        """添加记忆"""
        cmd = [self.cmd, "add", text]
        
        if category:
            cmd.extend(["--category", category])
        
        if tags:
            for tag in tags:
                cmd.extend(["--tag", tag])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    
    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """搜索记忆"""
        cmd = [self.cmd, "search", query, "--limit", str(limit)]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            try:
                # 解析 JSON 输出
                return json.loads(result.stdout)
            except:
                # 解析文本输出
                return [{"text": line.strip()} for line in result.stdout.split('\n') if line.strip()]
        
        return []
    
    def list_memories(self, category: str = None, limit: int = 10) -> List[Dict]:
        """列出记忆"""
        cmd = [self.cmd, "list"]
        
        if category:
            cmd.extend(["--category", category])
        
        cmd.extend(["--limit", str(limit)])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            try:
                return json.loads(result.stdout)
            except:
                return [{"text": line.strip()} for line in result.stdout.split('\n') if line.strip()]
        
        return []
    
    def delete(self, memory_id: str) -> bool:
        """删除记忆"""
        cmd = [self.cmd, "delete", memory_id]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    
    def stats(self) -> Dict:
        """获取统计信息"""
        cmd = [self.cmd, "stats"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            try:
                return json.loads(result.stdout)
            except:
                return {"raw": result.stdout}
        
        return {}


def main():
    """主函数 - 测试"""
    print("🏰 MemPalace CLI 封装测试")
    print("="*60)
    
    wrapper = MemPalaceWrapper()
    
    # 测试初始化
    print("\n1. 初始化测试...")
    # init_result = wrapper.init()
    # print(f"✅ 初始化：{'成功' if init_result else '跳过 (可能已初始化)'}")
    print("⏭️  跳过 (需要实际运行 mempalace init)")
    
    # 测试添加记忆
    print("\n2. 添加记忆测试...")
    # add_result = wrapper.add("太一是硅基生命", category="identity", tags=["AGI", "硅基生命"])
    # print(f"✅ 添加：{'成功' if add_result else '失败'}")
    print("⏭️  跳过 (需要先初始化)")
    
    # 测试搜索
    print("\n3. 搜索测试...")
    # results = wrapper.search("硅基生命", limit=3)
    # print(f"✅ 搜索到 {len(results)} 条结果")
    print("⏭️  跳过 (需要先添加数据)")
    
    # 测试统计
    print("\n4. 统计测试...")
    # stats = wrapper.stats()
    # print(f"✅ 统计：{stats}")
    print("⏭️  跳过 (需要先初始化)")
    
    print("\n✅ MemPalace CLI 封装测试完成!")
    print("\n📝 使用说明:")
    print("1. 运行 'mempalace init' 初始化")
    print("2. 使用 wrapper.add() 添加记忆")
    print("3. 使用 wrapper.search() 搜索记忆")
    print("4. 使用 wrapper.stats() 查看统计")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

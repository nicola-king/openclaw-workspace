#!/usr/bin/env python3
"""
Jina Reader 集成脚本
用途：通用网页抓取，转 Markdown 格式
集成到：罔两 Bot (数据采集)
"""

import requests
import json
from datetime import datetime

class JinaReader:
    """Jina Reader API 封装"""
    
    def __init__(self):
        self.base_url = "https://r.jina.ai/"
        self.headers = {
            "X-Retain-Images": "none",  # 不保留图片
            "X-With-Generated-Alt": "true"  # 生成图片描述
        }
    
    def read_url(self, url: str) -> dict:
        """读取网页内容"""
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={"url": url},
                timeout=30
            )
            response.raise_for_status()
            
            return {
                "success": True,
                "content": response.text,
                "timestamp": datetime.now().isoformat(),
                "source": url
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def search(self, query: str) -> dict:
        """搜索网页"""
        try:
            response = requests.get(
                f"https://s.jina.ai/{query}",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            return {
                "success": True,
                "content": response.text,
                "timestamp": datetime.now().isoformat(),
                "query": query
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


def main():
    """测试 Jina Reader"""
    reader = JinaReader()
    
    # 测试读取
    print("📖 测试 Jina Reader...")
    result = reader.read_url("https://example.com")
    print(f"读取结果：{result['success']}")
    
    # 测试搜索
    print("🔍 测试搜索...")
    result = reader.search("AI Agent news")
    print(f"搜索结果：{result['success']}")
    
    print("✅ Jina Reader 集成完成")


if __name__ == "__main__":
    main()

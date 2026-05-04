#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google 搜索优化解析器
针对 Google 搜索结果页面优化
"""

import re
import urllib.parse
from typing import List, Dict


class GoogleSearchParser:
    """Google 搜索结果解析器"""
    
    @staticmethod
    def parse(response) -> List[Dict]:
        """
        解析 Google 搜索结果
        
        支持多种 Google 页面布局
        """
        results = []
        html = response.text
        
        # 方法 1: 标准搜索结果 (div.g)
        items = response.css('div.g')
        if items:
            for item in items:
                result = GoogleSearchParser._parse_standard_item(item)
                if result:
                    results.append(result)
        
        # 方法 2: 新版布局 (div.tF2Cxc)
        if not results:
            items = response.css('div.tF2Cxc')
            for item in items:
                result = GoogleSearchParser._parse_new_item(item)
                if result:
                    results.append(result)
        
        # 方法 3: 通用解析 (通过 h3 和链接)
        if not results:
            results = GoogleSearchParser._parse_generic(response)
        
        return results
    
    @staticmethod
    def _parse_standard_item(item) -> Dict:
        """解析标准搜索结果项"""
        title = item.css('h3::text').get('')
        url = item.css('a::attr(href)').get('')
        description = item.css('div.VwiC3b::text').get('')
        
        if title and url:
            return {
                "title": title,
                "url": url,
                "description": description or '',
                "source": "google",
            }
        return None
    
    @staticmethod
    def _parse_new_item(item) -> Dict:
        """解析新版搜索结果项"""
        title = item.css('h3::text').get('')
        url = item.css('a::attr(href)').get('')
        description = item.css('span.aCOpRe::text').get('')
        
        if title and url:
            return {
                "title": title,
                "url": url,
                "description": description or '',
                "source": "google",
            }
        return None
    
    @staticmethod
    def _parse_generic(response) -> List[Dict]:
        """通用解析方法"""
        results = []
        
        # 查找所有 h3 标题
        titles = response.css('h3::text').getall()
        links = response.css('a[href^="http"]::attr(href)').getall()
        
        # 匹配标题和链接
        for i, title in enumerate(titles[:10]):
            if i < len(links):
                results.append({
                    "title": title,
                    "url": links[i],
                    "description": '',
                    "source": "google",
                })
        
        return results
    
    @staticmethod
    def is_blocked(response) -> bool:
        """检查是否被反爬阻止"""
        html = response.text.lower()
        
        block_signals = [
            'unusual traffic',
            'captcha',
            'robot',
            'blocked',
            'sorry',
        ]
        
        for signal in block_signals:
            if signal in html:
                return True
        
        # 检查是否有结果
        if len(response.text) < 1000:
            return True
        
        return False


# 便捷函数
def search_google(query: str, fetcher, max_results: int = 10) -> List[Dict]:
    """
    使用 Scrapling 搜索 Google
    
    Args:
        query: 搜索关键词
        fetcher: Scrapling Fetcher 实例
        max_results: 最大结果数
    
    Returns:
        搜索结果列表
    """
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    
    response = fetcher.get(search_url, timeout=15)
    
    # 检查是否被阻止
    if GoogleSearchParser.is_blocked(response):
        print("⚠️  Google 反爬阻止，尝试其他方法")
        return []
    
    # 解析结果
    results = GoogleSearchParser.parse(response)
    
    return results[:max_results]

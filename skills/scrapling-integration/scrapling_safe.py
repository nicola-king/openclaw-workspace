#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrapling 安全封装
限制 file:// 协议访问
"""

from scrapling import Fetcher as BaseFetcher
from urllib.parse import urlparse


class SafeFetcher(BaseFetcher):
    """安全封装的 Fetcher"""
    
    ALLOWED_PROTOCOLS = ['http', 'https']
    
    def get(self, url, **kwargs):
        """安全的 GET 请求"""
        parsed = urlparse(url)
        
        if parsed.scheme not in self.ALLOWED_PROTOCOLS:
            raise ValueError(f"❌ 禁止的协议: {parsed.scheme}:// (仅允许 http/https)")
        
        return super().get(url, **kwargs)
    
    def post(self, url, **kwargs):
        """安全的 POST 请求"""
        parsed = urlparse(url)
        
        if parsed.scheme not in self.ALLOWED_PROTOCOLS:
            raise ValueError(f"❌ 禁止的协议: {parsed.scheme}:// (仅允许 http/https)")
        
        return super().post(url, **kwargs)


# 导出安全版本
Fetcher = SafeFetcher


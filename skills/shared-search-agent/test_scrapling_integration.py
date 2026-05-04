#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrapling 集成测试
验证 Scrapling 是否正确集成到共享搜索服务
"""

import sys
sys.path.insert(0, '/home/sayelf/.openclaw/workspace')

from skills.shared_search_agent.shared_search_service import (
    TaiyiSharedSearchService,
    SearchRequest,
    SearchMode,
    AgentType,
)


def test_scrapling_mode():
    """测试 Scrapling 搜索模式"""
    print("=" * 60)
    print("🕷️  Scrapling 集成测试")
    print("=" * 60)
    
    service = TaiyiSharedSearchService()
    
    # 测试 1: 显式使用 Scrapling 模式
    print("\n📦 测试 1: 显式 Scrapling 模式")
    request = SearchRequest(
        query="OpenClaw AI",
        agent_type=AgentType.GENERAL.value,
        search_mode="scrapling",
        max_results=5,
    )
    
    result = service.search(request)
    print(f"  成功: {result.success}")
    print(f"  结果数: {len(result.results)}")
    print(f"  来源: {result.source}")
    print(f"  耗时: {result.duration_ms:.0f}ms")
    
    if result.results:
        print(f"  第一个结果: {result.results[0]['title'][:50]}...")
    
    # 测试 2: 自动选择模式 (高保护网站)
    print("\n📦 测试 2: 自动选择模式 (Google)")
    request = SearchRequest(
        query="site:google.com OpenClaw",
        agent_type=AgentType.CROSS_BORDER.value,
        search_mode="auto",
        max_results=3,
    )
    
    result = service.search(request)
    print(f"  成功: {result.success}")
    print(f"  来源: {result.source}")
    print(f"  耗时: {result.duration_ms:.0f}ms")
    
    # 测试 3: 统计信息
    print("\n📊 测试 3: 服务统计")
    stats = service.get_stats()
    print(f"  总请求: {stats['total_requests']}")
    print(f"  缓存命中率: {stats['cache_hit_rate']}")
    
    print("\n" + "=" * 60)
    print("✅ Scrapling 集成测试完成")
    print("=" * 60)


if __name__ == '__main__':
    test_scrapling_mode()

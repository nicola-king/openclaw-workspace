"""
太一共享搜索服务

使用方式:
    from skills.shared_search_agent import search, get_shared_search_service
    
    # 便捷搜索
    result = search("关键词", agent_type="cross_border_trade")
    
    # 使用服务实例
    service = get_shared_search_service()
    result = service.search_for_cross_border("关键词")
    result = service.search_for_travel("关键词")
    result = service.search_for_geo("关键词")
    result = service.search_for_osint("关键词")
"""

from .shared_search_service import (
    TaiyiSharedSearchService,
    SearchRequest,
    SearchResult,
    SearchMode,
    AgentType,
    get_shared_search_service,
    search,
)

__all__ = [
    'TaiyiSharedSearchService',
    'SearchRequest',
    'SearchResult',
    'SearchMode',
    'AgentType',
    'get_shared_search_service',
    'search',
]

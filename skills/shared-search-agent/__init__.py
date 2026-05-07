"""
太一统一情报引擎 (Taiyi Unified Intelligence)
所有 Agent 的共享搜索/情报/验证入口。

使用:
    from shared_search_agent.shared_search_service import (
        TaiyiSharedSearchService,
        get_shared_search_service,
        SearchRequest, SearchResult
    )

    svc = get_shared_search_service()
    result = svc.search(SearchRequest(query="...", agent_type="..."))
"""

from .shared_search_service import (
    TaiyiSharedSearchService,
    get_shared_search_service,
    search,
    SearchRequest,
    SearchResult,
    AgentType,
    SearchMode,
    COUNTRY_DB,
    resolve_country,
    generate_country_search_links,
)

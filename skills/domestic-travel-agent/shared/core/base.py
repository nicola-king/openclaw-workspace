#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一旅游探路者 v2.0 - 基础模块

所有核心模块的基类，提供数据库访问和搜索能力复用。

作者：太一 AGI
创建：2026-05-04
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

WORKSPACE = Path("/home/sayelf/.openclaw/workspace")
SKILLS_DIR = WORKSPACE / "skills"

# 动态添加 travel-db-common 到路径
sys.path.insert(0, str(SKILLS_DIR))

# 尝试导入共享搜索服务
try:
    from shared_search_agent.shared_search_service import (
        TaiyiSharedSearchService, SearchResult
    )
    HAS_SHARED_SEARCH = True
except ImportError:
    HAS_SHARED_SEARCH = False

# 尝试导入数据库公共模块
try:
    from travel_db_common.travel_db import TravelDatabase
    HAS_TRAVEL_DB = True
except ImportError:
    HAS_TRAVEL_DB = False

logger = logging.getLogger('travel-agent-base')


class TravelCoreModule:
    """所有核心模块的基类"""

    def __init__(self, agent_type: str = 'domestic', db_dir: Optional[Path] = None):
        self.agent_type = agent_type  # 'domestic' or 'international'
        if db_dir is None:
            if agent_type == 'domestic':
                db_dir = WORKSPACE / "skills" / "domestic-travel-agent" / "data"
            else:
                db_dir = WORKSPACE / "skills" / "international-travel-agent" / "data"

        self.db_dir = db_dir
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = db_dir / "travel.db"

        # 初始化数据库
        if HAS_TRAVEL_DB:
            self.db = TravelDatabase(self.db_path)
        else:
            self.db = None

        # 初始化共享搜索服务
        if HAS_SHARED_SEARCH:
            self.search_service = TaiyiSharedSearchService()
        else:
            self.search_service = None

    def search_web(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """通过共享搜索服务搜索网络"""
        if self.search_service:
            result = self.search_service.search_for_travel(query, max_results=max_results)
            items = result.to_dict().get('items', [])
            return items if items else []
        return []

    def save_json(self, data: Any, filename: str, subdir: str = '') -> Path:
        """保存 JSON 到数据目录"""
        save_dir = self.db_dir
        if subdir:
            save_dir = self.db_dir / subdir
        save_dir.mkdir(parents=True, exist_ok=True)
        from datetime import datetime
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = save_dir / f"{filename}_{ts}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return filepath

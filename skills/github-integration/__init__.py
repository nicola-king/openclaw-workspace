#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一 GitHub 集成包

采用系统内部信息架构，不依赖外部 API
"""

from .github_integration import (
    GitHubIntegration,
    GitCommit,
    GitBranch,
    get_github_integration,
    quick_commit,
    sync_system_config,
)

__all__ = [
    "GitHubIntegration",
    "GitCommit",
    "GitBranch",
    "get_github_integration",
    "quick_commit",
    "sync_system_config",
]

__version__ = "1.0.0"

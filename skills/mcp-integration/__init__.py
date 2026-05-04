#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一 MCP 集成包

Model Context Protocol 标准实现
"""

from .mcp_server import (
    TaiyiMCPServer,
    MCPTool,
    MCPResource,
)

__all__ = [
    "TaiyiMCPServer",
    "MCPTool",
    "MCPResource",
]

__version__ = "1.0.0"

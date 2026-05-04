#!/usr/bin/env python3
"""
GEO 外贸开发模块测试
"""

import unittest
import json
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import GeoOutbound


class TestGeoOutbound(unittest.TestCase):
    """GEO 外贸开发测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.agent = GeoOutbound()
    
    def test_market_analysis(self):
        """测试市场分析"""
        result = self.agent.execute(task="market_analysis", hs_code="8507.60", market="澳大利亚")
        self.assertEqual(result["status"], "success")
        self.assertIn("market_analysis", result)
        self.assertEqual(result["market_analysis"]["hs_code"], "8507.60")
    
    def test_lead_generation(self):
        """测试潜客生成"""
        result = self.agent.execute(task="lead_generation", hs_code="8507.60", market="澳大利亚")
        self.assertEqual(result["status"], "success")
        self.assertIn("prospects", result)
        self.assertGreater(result["total"], 0)
    
    def test_content_marketing(self):
        """测试内容营销"""
        result = self.agent.execute(task="content_marketing", topics=["折叠房屋"])
        self.assertEqual(result["status"], "success")
        self.assertIn("content", result)
    
    def test_monitor(self):
        """测试监测"""
        result = self.agent.execute(task="monitor")
        self.assertEqual(result["status"], "success")
        self.assertIn("ai_citations", result)
    
    def test_health_check(self):
        """测试健康检查"""
        result = self.agent.health_check()
        self.assertEqual(result["status"], "healthy")
        self.assertEqual(result["module"], "geo-outbound")
        self.assertEqual(result["version"], "9.0.0")
    
    def test_properties(self):
        """测试属性"""
        self.assertEqual(self.agent.name, "geo-outbound")
        self.assertEqual(self.agent.version, "9.0.0")
        self.assertIn("cross-border-core", self.agent.dependencies)


if __name__ == "__main__":
    unittest.main()

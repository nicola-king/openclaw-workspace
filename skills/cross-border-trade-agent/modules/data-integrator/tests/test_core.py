#!/usr/bin/env python3
"""
数据源整合模块测试
"""

import unittest
import json
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import DataIntegrator


class TestDataIntegrator(unittest.TestCase):
    """数据源整合测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.agent = DataIntegrator()
        self.agent.initialize({})
    
    def test_fetch_customs(self):
        """测试海关数据获取"""
        result = self.agent.execute(task="fetch", source="customs", query="折叠房屋")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["source"], "customs")
        self.assertIn("data", result)
    
    def test_fetch_ecommerce(self):
        """测试电商数据获取"""
        result = self.agent.execute(task="fetch", source="ecommerce", query="折叠房屋")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["source"], "ecommerce")
    
    def test_sync(self):
        """测试数据同步"""
        result = self.agent.execute(task="sync", sources=["customs", "ecommerce"])
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["total"], 2)
    
    def test_verify(self):
        """测试数据验证"""
        result = self.agent.execute(task="verify", data={"test": "data"})
        self.assertEqual(result["status"], "success")
        self.assertIn("quality_score", result)
    
    def test_health_check(self):
        """测试健康检查"""
        result = self.agent.health_check()
        self.assertEqual(result["status"], "healthy")
        self.assertEqual(result["module"], "data-integrator")
        self.assertEqual(result["version"], "9.0.0")
        self.assertIn("sources", result)
    
    def test_properties(self):
        """测试属性"""
        self.assertEqual(self.agent.name, "data-integrator")
        self.assertEqual(self.agent.version, "9.0.0")
        self.assertIn("cross-border-core", self.agent.dependencies)


if __name__ == "__main__":
    unittest.main()

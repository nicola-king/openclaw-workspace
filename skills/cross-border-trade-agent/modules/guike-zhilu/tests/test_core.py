#!/usr/bin/env python3
"""
贵客之路模块测试
"""

import unittest
import json
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import GuikeZhilu


class TestGuikeZhilu(unittest.TestCase):
    """贵客之路测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.agent = GuikeZhilu()
    
    def test_search(self):
        """测试搜索功能"""
        result = self.agent.execute(task="search", product="折叠房屋", market="澳大利亚")
        self.assertEqual(result["status"], "success")
        self.assertIn("prospects", result)
        self.assertGreater(result["total"], 0)
    
    def test_verification(self):
        """测试验证功能"""
        prospects = [
            {"name": "Test Company", "score": 95},
            {"name": "Test Company 2", "score": 75}
        ]
        result = self.agent.execute(task="verification", prospects=prospects)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["verified"][0]["level"], "S")
        self.assertEqual(result["verified"][1]["level"], "A")
    
    def test_outreach(self):
        """测试触达功能"""
        prospects = [{"name": "Test Company"}]
        result = self.agent.execute(task="outreach", prospects=prospects)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["total"], 1)
    
    def test_nurturing(self):
        """测试培育功能"""
        prospects = [{"name": "Test Company"}]
        result = self.agent.execute(task="nurturing", prospects=prospects)
        self.assertEqual(result["status"], "success")
        self.assertIn("stages", result)
    
    def test_health_check(self):
        """测试健康检查"""
        result = self.agent.health_check()
        self.assertEqual(result["status"], "healthy")
        self.assertEqual(result["module"], "guike-zhilu")
        self.assertEqual(result["version"], "9.0.0")
    
    def test_properties(self):
        """测试属性"""
        self.assertEqual(self.agent.name, "guike-zhilu")
        self.assertEqual(self.agent.version, "9.0.0")
        self.assertIn("cross-border-core", self.agent.dependencies)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""
自我进化系统模块测试
"""

import unittest
import json
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import SelfEvolution


class TestSelfEvolution(unittest.TestCase):
    """自我进化系统测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.agent = SelfEvolution()
    
    def test_browser_healing(self):
        """测试浏览器自愈"""
        result = self.agent.execute(task="healing")
        self.assertEqual(result["status"], "success")
        self.assertIn("healing", result)
        self.assertIn("total_healings", result)
    
    def test_skill_crystallization(self):
        """测试技能结晶"""
        result = self.agent.execute(task="crystallization", task_type="search")
        self.assertEqual(result["status"], "success")
        self.assertIn("skill_library", result)
    
    def test_token_efficiency_monitor(self):
        """测试 Token 效率监控"""
        result = self.agent.execute(task="token_monitor")
        self.assertEqual(result["status"], "success")
        self.assertIn("usage", result)
    
    def test_health_check(self):
        """测试健康检查"""
        result = self.agent.health_check()
        self.assertEqual(result["status"], "healthy")
        self.assertEqual(result["module"], "self-evolution")
        self.assertEqual(result["version"], "9.0.0")
    
    def test_properties(self):
        """测试属性"""
        self.assertEqual(self.agent.name, "self-evolution")
        self.assertEqual(self.agent.version, "9.0.0")
        self.assertIn("cross-border-core", self.agent.dependencies)


if __name__ == "__main__":
    unittest.main()

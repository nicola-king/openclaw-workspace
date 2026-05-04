#!/usr/bin/env python3
"""
转化优化中心模块测试
"""

import unittest
import json
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import ConversionOptimizer


class TestConversionOptimizer(unittest.TestCase):
    """转化优化中心测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.agent = ConversionOptimizer()
    
    def test_funnel_analysis(self):
        """测试漏斗分析"""
        result = self.agent.execute(task="funnel", product="折叠房屋")
        self.assertEqual(result["status"], "success")
        self.assertIn("funnel", result)
        self.assertIn("conversion_rate", result)
    
    def test_roi_tracking(self):
        """测试 ROI 追踪"""
        result = self.agent.execute(task="roi", product="折叠房屋")
        self.assertEqual(result["status"], "success")
        self.assertIn("roi", result)
    
    def test_channel_comparison(self):
        """测试渠道对比"""
        result = self.agent.execute(task="channel", product="折叠房屋")
        self.assertEqual(result["status"], "success")
        self.assertIn("channels", result)
        self.assertIn("best_channel", result)
    
    def test_ab_testing(self):
        """测试 A/B 测试"""
        result = self.agent.execute(task="ab_test", product="折叠房屋")
        self.assertEqual(result["status"], "success")
        self.assertIn("test", result)
    
    def test_health_check(self):
        """测试健康检查"""
        result = self.agent.health_check()
        self.assertEqual(result["status"], "healthy")
        self.assertEqual(result["module"], "conversion-optimizer")
        self.assertEqual(result["version"], "9.0.0")
    
    def test_properties(self):
        """测试属性"""
        self.assertEqual(self.agent.name, "conversion-optimizer")
        self.assertEqual(self.agent.version, "9.0.0")
        self.assertIn("cross-border-core", self.agent.dependencies)


if __name__ == "__main__":
    unittest.main()

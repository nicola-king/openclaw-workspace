#!/usr/bin/env python3
"""
智能分析中心模块测试
"""

import unittest
import json
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import IntelligenceHub


class TestIntelligenceHub(unittest.TestCase):
    """智能分析中心测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.agent = IntelligenceHub()
    
    def test_competitor_analysis(self):
        """测试竞品分析"""
        result = self.agent.execute(task="competitor", product="折叠房屋", market="澳大利亚")
        self.assertEqual(result["status"], "success")
        self.assertIn("competitors", result)
        self.assertGreater(result["total"], 0)
        self.assertIn("analysis", result)
    
    def test_product_scoring(self):
        """测试选品评分"""
        result = self.agent.execute(task="scoring", product="折叠房屋")
        self.assertEqual(result["status"], "success")
        self.assertIn("total_score", result)
        self.assertIn("dimensions", result)
    
    def test_manufacturer_recommendation(self):
        """测试厂家推荐"""
        result = self.agent.execute(task="manufacturer", product="折叠房屋")
        self.assertEqual(result["status"], "success")
        self.assertIn("manufacturers", result)
        self.assertGreater(result["total"], 0)
    
    def test_trend_forecast(self):
        """测试趋势预测"""
        result = self.agent.execute(task="forecast", product="折叠房屋", period="12m")
        self.assertEqual(result["status"], "success")
        self.assertIn("forecast", result)
    
    def test_health_check(self):
        """测试健康检查"""
        result = self.agent.health_check()
        self.assertEqual(result["status"], "healthy")
        self.assertEqual(result["module"], "intelligence-hub")
        self.assertEqual(result["version"], "9.0.0")
    
    def test_properties(self):
        """测试属性"""
        self.assertEqual(self.agent.name, "intelligence-hub")
        self.assertEqual(self.agent.version, "9.0.0")
        self.assertIn("cross-border-core", self.agent.dependencies)
        self.assertIn("data-integrator", self.agent.dependencies)


if __name__ == "__main__":
    unittest.main()

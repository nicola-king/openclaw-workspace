#!/usr/bin/env python3
"""
交易支持中心模块测试
"""

import unittest
import json
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import TransactionSupport


class TestTransactionSupport(unittest.TestCase):
    """交易支持中心测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.agent = TransactionSupport()
    
    def test_logistics_optimization(self):
        """测试物流优化"""
        result = self.agent.execute(task="logistics", product="折叠房屋", from_loc="中国", to_loc="澳大利亚")
        self.assertEqual(result["status"], "success")
        self.assertIn("options", result)
        self.assertIn("recommended", result)
    
    def test_price_comparison(self):
        """测试价格对比"""
        result = self.agent.execute(task="price", product="折叠房屋")
        self.assertEqual(result["status"], "success")
        self.assertIn("prices", result)
        self.assertIn("best_price", result)
    
    def test_sales_forecast(self):
        """测试销售预测"""
        result = self.agent.execute(task="forecast", product="折叠房屋", period="12m")
        self.assertEqual(result["status"], "success")
        self.assertIn("forecast", result)
    
    def test_multilingual_support(self):
        """测试多语言客服"""
        result = self.agent.execute(task="multilingual", language="en")
        self.assertEqual(result["status"], "success")
        self.assertIn("templates", result)
    
    def test_health_check(self):
        """测试健康检查"""
        result = self.agent.health_check()
        self.assertEqual(result["status"], "healthy")
        self.assertEqual(result["module"], "transaction-support")
        self.assertEqual(result["version"], "9.0.0")
    
    def test_properties(self):
        """测试属性"""
        self.assertEqual(self.agent.name, "transaction-support")
        self.assertEqual(self.agent.version, "9.0.0")
        self.assertIn("cross-border-core", self.agent.dependencies)


if __name__ == "__main__":
    unittest.main()

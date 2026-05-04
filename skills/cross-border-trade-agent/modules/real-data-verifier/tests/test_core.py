#!/usr/bin/env python3
"""
真实数据验证模块测试
"""

import unittest
import json
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import RealDataVerifier


class TestRealDataVerifier(unittest.TestCase):
    """真实数据验证测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.agent = RealDataVerifier()
    
    def test_company_verification(self):
        """测试公司验证"""
        result = self.agent.execute(task="company", name="Aus Modular Homes", website="https://www.ausmodularhomes.com.au")
        self.assertEqual(result["status"], "success")
        self.assertIn("company", result)
        self.assertTrue(result["company"]["verified"])
    
    def test_phone_verification(self):
        """测试电话验证"""
        result = self.agent.execute(task="phone", phone="+61-2-98765432")
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["valid"])
    
    def test_email_verification(self):
        """测试邮箱验证"""
        result = self.agent.execute(task="email", email="info@ausmodularhomes.com.au")
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["valid"])
    
    def test_website_verification(self):
        """测试官网验证"""
        result = self.agent.execute(task="website", url="https://www.ausmodularhomes.com.au")
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["valid"])
    
    def test_health_check(self):
        """测试健康检查"""
        result = self.agent.health_check()
        self.assertEqual(result["status"], "healthy")
        self.assertEqual(result["module"], "real-data-verifier")
        self.assertEqual(result["version"], "9.0.0")
    
    def test_properties(self):
        """测试属性"""
        self.assertEqual(self.agent.name, "real-data-verifier")
        self.assertEqual(self.agent.version, "9.0.0")
        self.assertIn("cross-border-core", self.agent.dependencies)
        self.assertIn("data-integrator", self.agent.dependencies)


if __name__ == "__main__":
    unittest.main()

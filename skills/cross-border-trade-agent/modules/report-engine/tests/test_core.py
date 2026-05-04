#!/usr/bin/env python3
"""
报告系统模块测试
"""

import unittest
import json
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import ReportEngine


class TestReportEngine(unittest.TestCase):
    """报告系统测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.agent = ReportEngine()
    
    def test_intelligence_report(self):
        """测试智能报告"""
        result = self.agent.execute(task="intelligence", product="折叠房屋")
        self.assertEqual(result["status"], "success")
        self.assertIn("report", result)
    
    def test_report_delivery(self):
        """测试报告推送"""
        report = {"title": "Test Report"}
        result = self.agent.execute(task="delivery", report=report, channels=["telegram", "email"])
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["total"], 2)
    
    def test_es_engine_report(self):
        """测试 ES 引擎报告"""
        result = self.agent.execute(task="es_engine", product="折叠房屋")
        self.assertEqual(result["status"], "success")
        self.assertIn("report", result)
    
    def test_md_report_generator(self):
        """测试 Markdown 报告生成"""
        result = self.agent.execute(task="md_generator", product="折叠房屋")
        self.assertEqual(result["status"], "success")
        self.assertIn("markdown", result)
    
    def test_health_check(self):
        """测试健康检查"""
        result = self.agent.health_check()
        self.assertEqual(result["status"], "healthy")
        self.assertEqual(result["module"], "report-engine")
        self.assertEqual(result["version"], "9.0.0")
    
    def test_properties(self):
        """测试属性"""
        self.assertEqual(self.agent.name, "report-engine")
        self.assertEqual(self.agent.version, "9.0.0")
        self.assertIn("cross-border-core", self.agent.dependencies)


if __name__ == "__main__":
    unittest.main()

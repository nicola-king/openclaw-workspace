#!/usr/bin/env python3
"""card-generator 模块测试"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core import cardgeneratorModule

class TestcardgeneratorModule(unittest.TestCase):
    def setUp(self):
        self.module = cardgeneratorModule()
    
    def test_execute(self):
        result = self.module.execute(task="test")
        self.assertEqual(result["status"], "success")
    
    def test_health_check(self):
        result = self.module.health_check()
        self.assertEqual(result["status"], "healthy")
    
    def test_properties(self):
        self.assertEqual(self.module.name, "card-generator")
        self.assertEqual(self.module.version, "1.0.0")
        self.assertIn("aesthetic-filter", self.module.dependencies)

if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""
额度感知路由测试
"""

import unittest
from quota_router import QuotaRouter, QuotaStatus, ModelState


class TestQuotaRouter(unittest.TestCase):
    """测试额度路由器"""
    
    def setUp(self):
        self.router = QuotaRouter()
    
    def test_select_model_bailian_available(self):
        """测试：百炼可用时选择百炼"""
        # 模拟百炼可用
        self.router.cache["bailian"] = {"used": 0}
        self.router.cache["gemini"] = {"used": 0}
        
        model = self.router.select_model()
        self.assertTrue(model.startswith("bailian"))
        self.assertEqual(self.router.state, ModelState.BAILIAN_PRIMARY)
    
    def test_select_model_bailian_unavailable(self):
        """测试：百炼不可用时切换到 Gemini"""
        # 模拟百炼额度耗尽
        self.router.cache["bailian"] = {"used": 999999}
        self.router.cache["gemini"] = {"used": 0}
        
        model = self.router.select_model()
        self.assertTrue(model.startswith("gemini"))
        self.assertEqual(self.router.state, ModelState.GEMINI_BACKUP)
    
    def test_select_model_both_unavailable(self):
        """测试：双额度耗尽时切换到本地"""
        # 模拟双额度耗尽
        self.router.cache["bailian"] = {"used": 999999}
        self.router.cache["gemini"] = {"used": 9999}
        
        model = self.router.select_model()
        self.assertTrue(model.startswith("local"))
        self.assertEqual(self.router.state, ModelState.LOCAL_FALLBACK)
    
    def test_track_usage(self):
        """测试：额度追踪"""
        initial_used = self.router.cache.get("bailian", {}).get("used", 0)
        
        self.router.track_usage("bailian/qwen3.5-plus", 1000, 2000)
        
        new_used = self.router.cache.get("bailian", {}).get("used", 0)
        self.assertEqual(new_used, initial_used + 3000)
    
    def test_get_status(self):
        """测试：获取状态"""
        status = self.router.get_status()
        
        self.assertIn("state", status)
        self.assertIn("bailian", status)
        self.assertIn("gemini", status)
        self.assertIn("current_model", status)


if __name__ == "__main__":
    unittest.main()

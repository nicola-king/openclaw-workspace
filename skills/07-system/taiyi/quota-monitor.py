#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
额度监控器 - 百炼 + Gemini

功能:
- 监控每日免费额度
- 智能告警
- 降级建议
"""

import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('QuotaMonitor')

class QuotaMonitor:
    """额度监控器"""
    
    def __init__(self):
        # Gemini 配置
        self.gemini_daily_limit = 1500  # 1500 次/天
        self.gemini_warning_threshold = 1200  # 80% 告警
        self.gemini_reserved = 200  # 保留 200 次备用
        
        # 百炼配置 (40 元/月，目标 90% 使用率)
        self.bailian_monthly_fee = 40  # 40 元/月
        self.bailian_monthly_limit = 10000  # 假设月度额度 (需确认)
        self.bailian_usage_target = 0.90  # 90% 使用目标
        self.bailian_warning_threshold = 0.95  # 95% 告警
        
        # 使用量
        self.gemini_used_today = 0
        self.bailian_used_today = 0
        
        # 日期追踪
        self.last_reset_date = datetime.now().date()
    
    def reset_if_new_day(self):
        """如果是新的一天，重置计数器"""
        today = datetime.now().date()
        if today > self.last_reset_date:
            logger.info("新的一天，重置额度计数器")
            self.gemini_used_today = 0
            self.bailian_used_today = 0
            self.last_reset_date = today
    
    def use_gemini(self):
        """使用一次 Gemini"""
        self.reset_if_new_day()
        self.gemini_used_today += 1
        logger.info(f"Gemini 使用量：{self.gemini_used_today}/{self.gemini_daily_limit}")
        
        # 检查告警
        if self.gemini_used_today >= self.gemini_warning_threshold:
            logger.warning(f"⚠️ Gemini 额度即将用完：{self.gemini_used_today}/{self.gemini_daily_limit}")
            return False  # 建议降级
        
        return True  # 可以继续使用
    
    def use_bailian(self):
        """使用一次百炼"""
        self.reset_if_new_day()
        self.bailian_used_today += 1
        logger.info(f"百炼使用量：{self.bailian_used_today}/{self.bailian_daily_limit}")
        
        # 检查告警
        if self.bailian_used_today >= self.bailian_warning_threshold:
            logger.warning(f"⚠️ 百炼额度即将用完：{self.bailian_used_today}/{self.bailian_daily_limit}")
            return False  # 建议降级
        
        return True  # 可以继续使用
    
    def should_use_gemini(self):
        """是否应该使用 Gemini"""
        self.reset_if_new_day()
        remaining = self.gemini_daily_limit - self.gemini_used_today
        return remaining > self.gemini_reserved  # 保留备用额度
    
    def should_use_bailian(self):
        """是否应该使用百炼"""
        self.reset_if_new_day()
        remaining = self.bailian_daily_limit - self.bailian_used_today
        return remaining > 100  # 保留 100 次备用
    
    def get_gemini_remaining(self):
        """获取 Gemini 剩余额度"""
        self.reset_if_new_day()
        return self.gemini_daily_limit - self.gemini_used_today
    
    def get_bailian_remaining(self):
        """获取百炼剩余额度"""
        self.reset_if_new_day()
        return self.bailian_daily_limit - self.bailian_used_today
    
    def get_status(self):
        """获取状态报告"""
        self.reset_if_new_day()
        
        # 计算百炼使用率 (月度)
        bailian_usage_rate = self.bailian_used_today / self.bailian_monthly_limit if self.bailian_monthly_limit > 0 else 0
        
        status = f"""
📊 额度监控报告
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Gemini (免费):
  已用：{self.gemini_used_today}/{self.gemini_daily_limit}
  剩余：{self.get_gemini_remaining()}
  状态：{'⚠️ 即将用完' if self.gemini_used_today >= self.gemini_warning_threshold else '✅ 正常'}

百炼 (40 元/月):
  已用：{self.bailian_used_today}/{self.bailian_monthly_limit}
  使用率：{bailian_usage_rate*100:.1f}%
  目标：90%
  状态：{'✅ 使用率良好' if bailian_usage_rate >= 0.85 else '⚠️ 需增加使用'}

成本效益:
  百炼：{'✅ 充分利用' if bailian_usage_rate >= 0.85 else '⚠️ 未充分利用 (已付费 40 元)'}
  Gemini: {'✅ 免费额度充足' if self.get_gemini_remaining() > 500 else '⚠️ 免费额度紧张'}

建议:
  Gemini: {'使用本地降级' if not self.should_use_gemini() else '可继续使用'}
  百炼：{'✅ 优先使用 (已付费)' if bailian_usage_rate < 0.90 else '⚠️ 接近上限'}
"""
        return status


def main():
    """测试主函数"""
    monitor = QuotaMonitor()
    
    # 模拟使用
    print("模拟使用 Gemini...")
    for i in range(5):
        monitor.use_gemini()
    
    print("\n模拟使用百炼...")
    for i in range(5):
        monitor.use_bailian()
    
    # 打印状态
    print(monitor.get_status())


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直播数据采集 PoC (Proof of Concept)

功能:
- 模拟视频号直播数据采集
- 测试数据实时性
- 验证技术可行性

使用:
python3 poc_data_collector.py --live-id TEST123

作者：素问 + 太一
时间：2026-04-19
"""

import asyncio
import json
import time
import random
from datetime import datetime
from typing import Dict, Optional
import argparse


class WeChatLiveCollector:
    """视频号直播数据采集器 (PoC 版本)"""
    
    def __init__(self, app_id: str = "", secret: str = ""):
        self.app_id = app_id
        self.secret = secret
        self.base_url = "https://api.weixin.qq.com/channels"
        self.is_api_available = bool(app_id and secret)
        
    async def fetch_live_info(self, live_id: str) -> Optional[Dict]:
        """
        获取直播间实时信息
        
        Args:
            live_id: 直播间 ID
            
        Returns:
            直播数据字典，失败返回 None
        """
        if self.is_api_available:
            # TODO: 实现真实 API 调用
            # return await self._call_wechat_api(live_id)
            pass
        
        # PoC: 模拟数据
        return self._mock_live_data(live_id)
    
    def _mock_live_data(self, live_id: str) -> Dict:
        """模拟直播数据 (用于 PoC 测试)"""
        base_time = int(time.time())
        
        # 模拟实时数据变化
        base_viewers = 1000
        viewer_noise = random.randint(-100, 100)
        viewer_trend = int(50 * (base_time % 60) / 60)  # 逐渐上升趋势
        
        return {
            "live_id": live_id,
            "status": "live",  # live/ended/not_started
            "viewer_count": base_viewers + viewer_noise + viewer_trend,
            "total_viewer": base_viewers * 5 + random.randint(0, 500),
            "like_count": base_viewers * 10 + random.randint(0, 1000),
            "comment_count": base_viewers * 2 + random.randint(0, 200),
            "share_count": random.randint(50, 200),
            "start_time": base_time - random.randint(600, 3600),
            "duration": base_time - (base_time - random.randint(600, 3600)),
            "anchor": {
                "name": "测试主播",
                "follower_count": 50000
            },
            "products": [
                {
                    "id": "P001",
                    "name": "测试商品 1",
                    "price": 99.0,
                    "click_count": random.randint(100, 500),
                    "order_count": random.randint(10, 50)
                },
                {
                    "id": "P002",
                    "name": "测试商品 2",
                    "price": 199.0,
                    "click_count": random.randint(50, 300),
                    "order_count": random.randint(5, 30)
                }
            ],
            "timestamp": base_time,
            "collected_at": datetime.now().isoformat()
        }
    
    async def fetch_comments(self, live_id: str, limit: int = 50) -> Dict:
        """获取评论列表"""
        # PoC: 模拟评论数据
        comments = []
        for i in range(limit):
            comments.append({
                "user": f"用户{random.randint(1000, 9999)}",
                "content": random.choice([
                    "这个多少钱？",
                    "质量怎么样？",
                    "已下单",
                    "主播好漂亮",
                    "666",
                    "想要想要",
                    "什么时候发货？",
                    "有优惠吗？"
                ]),
                "timestamp": int(time.time()) - random.randint(0, 300),
                "like_count": random.randint(0, 50)
            })
        
        # 热词分析
        all_text = " ".join([c["content"] for c in comments])
        hot_words = {}
        for word in ["多少钱", "质量", "下单", "优惠", "想要"]:
            count = all_text.count(word)
            if count > 0:
                hot_words[word] = count
        
        return {
            "comments": comments,
            "hot_words": hot_words,
            "total_count": limit,
            "timestamp": int(time.time())
        }


class LiveDataMonitor:
    """直播实时监控器"""
    
    def __init__(self, collector: WeChatLiveCollector, live_id: str):
        self.collector = collector
        self.live_id = live_id
        self.history = []
        self.is_running = False
        
    async def start_monitoring(self, interval: int = 5, duration: int = 300):
        """
        开始实时监控
        
        Args:
            interval: 采集间隔 (秒)
            duration: 监控时长 (秒)
        """
        self.is_running = True
        start_time = time.time()
        
        print(f"🎥 开始监控直播间：{self.live_id}")
        print(f"📊 采集间隔：{interval}秒 | 监控时长：{duration}秒")
        print("-" * 60)
        
        while self.is_running and (time.time() - start_time) < duration:
            try:
                # 采集数据
                data = await self.collector.fetch_live_info(self.live_id)
                
                if data:
                    # 存储历史
                    self.history.append(data)
                    
                    # 显示数据
                    self._display_data(data)
                    
                    # 异常检测
                    anomaly = self._detect_anomaly(data)
                    if anomaly:
                        self._show_alert(anomaly)
                
                await asyncio.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n⚠️  用户中断监控")
                break
            except Exception as e:
                print(f"❌ 采集错误：{e}")
                await asyncio.sleep(interval)
        
        self.is_running = False
        print("-" * 60)
        print("✅ 监控结束")
        self._generate_summary()
    
    def _display_data(self, data: Dict):
        """显示实时数据"""
        now = datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] "
              f"👁️ 在线:{data['viewer_count']:,} | "
              f"📈 累计:{data['total_viewer']:,} | "
              f"❤️ 点赞:{data['like_count']:,} | "
              f"💬 评论:{data['comment_count']:,}")
    
    def _detect_anomaly(self, current: Dict) -> Optional[Dict]:
        """检测数据异常"""
        if len(self.history) < 5:
            return None
        
        # 计算移动平均
        recent_viewers = [h['viewer_count'] for h in self.history[-5:]]
        avg_viewers = sum(recent_viewers) / len(recent_viewers)
        
        # 检测人流暴跌
        if current['viewer_count'] < avg_viewers * 0.7:
            drop_rate = (avg_viewers - current['viewer_count']) / avg_viewers
            return {
                'type': 'viewer_drop',
                'severity': 'high' if drop_rate > 0.5 else 'medium',
                'message': f'人流暴跌 {drop_rate*100:.1f}%',
                'suggestion': '建议立即发福利/抽奖'
            }
        
        return None
    
    def _show_alert(self, anomaly: Dict):
        """显示告警"""
        emoji = "🚨" if anomaly['severity'] == 'high' else "⚠️"
        print(f"{emoji} 告警：{anomaly['message']} - {anomaly['suggestion']}")
    
    def _generate_summary(self):
        """生成监控摘要"""
        if not self.history:
            return
        
        viewers = [h['viewer_count'] for h in self.history]
        peak = max(viewers)
        avg = sum(viewers) / len(viewers)
        
        print(f"\n📊 监控摘要:")
        print(f"  采集次数：{len(self.history)}")
        print(f"  最高在线：{peak:,}")
        print(f"  平均在线：{avg:,.0f}")
        print(f"  当前在线：{viewers[-1]:,}")


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='直播数据采集 PoC')
    parser.add_argument('--live-id', type=str, default='TEST123',
                       help='直播间 ID')
    parser.add_argument('--interval', type=int, default=5,
                       help='采集间隔 (秒)')
    parser.add_argument('--duration', type=int, default=60,
                       help='监控时长 (秒)')
    
    args = parser.parse_args()
    
    # 创建采集器
    collector = WeChatLiveCollector()
    
    # 创建监控器
    monitor = LiveDataMonitor(collector, args.live_id)
    
    # 开始监控
    await monitor.start_monitoring(
        interval=args.interval,
        duration=args.duration
    )


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
# multi-channel-scraper.py - 多渠道开源爬虫
# 依赖：pip install scrapling cloudscraper
# 等级：Tier 1 · 永久核心
# 创建：2026-04-01 20:58

import json
import time
from datetime import datetime
from pathlib import Path

try:
    from scrapling import StealthyFetcher
    SCRAPLING_AVAILABLE = True
except ImportError:
    SCRAPLING_AVAILABLE = False
    print("警告：Scrapling 未安装，运行 pip install scrapling")

try:
    import cloudscraper
    CLOUDSCRAPER_AVAILABLE = True
except ImportError:
    CLOUDSCRAPER_AVAILABLE = False
    print("警告：cloudscraper 未安装，运行 pip install cloudscraper")


class OpenScraper:
    """GitHub 开源免费爬虫 - 多渠道智能抓取"""
    
    def __init__(self):
        self.fetcher = StealthyFetcher() if SCRAPLING_AVAILABLE else None
        # Scrapling 配置优化 (超时 30 秒)
        if SCRAPLING_AVAILABLE:
            try:
                StealthyFetcher.configure(timeout=30000, wait_until='networkidle2')
            except Exception as e:
                print(f"Scrapling 配置警告：{e}")
        self.scraper = cloudscraper.create_scraper() if CLOUDSCRAPER_AVAILABLE else None
        self.results = []
        self.failures = []
        self.stats = {
            "total_requests": 0,
            "successful": 0,
            "failed": 0,
            "scrapling_success": 0,
            "cloudscraper_success": 0,
            "start_time": datetime.now()
        }
    
    def fetch_scrapling(self, url, timeout=30, headers=None):
        """Scrapling 抓取 (Plan A)"""
        if not self.fetcher:
            return {"status": "failed", "error": "Scrapling not available", "method": "scrapling"}
        
        try:
            html = self.fetcher.fetch(url, timeout=timeout)
            self.stats["scrapling_success"] += 1
            return {
                "status": "success",
                "data": html if isinstance(html, str) else html.body,
                "method": "scrapling",
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "size_bytes": len(html) if html else 0
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "method": "scrapling",
                "url": url,
                "timestamp": datetime.now().isoformat()
            }
    
    def fetch_cloudscraper(self, url, timeout=30, headers=None):
        """cloudscraper 抓取 (Plan B)"""
        if not self.scraper:
            return {"status": "failed", "error": "cloudscraper not available", "method": "cloudscraper"}
        
        try:
            response = self.scraper.get(url, timeout=timeout, headers=headers or {})
            if response.status_code == 200:
                return {
                    "status": "success",
                    "data": response.text,
                    "method": "cloudscraper",
                    "url": url,
                    "timestamp": datetime.now().isoformat(),
                    "size_bytes": len(response.text),
                    "status_code": response.status_code
                }
            else:
                return {
                    "status": "failed",
                    "error": f"HTTP {response.status_code}",
                    "method": "cloudscraper",
                    "url": url,
                    "timestamp": datetime.now().isoformat(),
                    "status_code": response.status_code
                }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "method": "cloudscraper",
                "url": url,
                "timestamp": datetime.now().isoformat()
            }
    
    def fetch(self, url, fallback=True, delay=3):
        """智能抓取 (自动切换渠道)"""
        self.stats["total_requests"] += 1
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        print(f"[{timestamp}] 开始抓取：{url}")
        
        # Plan A: Scrapling
        if self.fetcher:
            result_a = self.fetch_scrapling(url)
            if result_a["status"] == "success":
                print(f"  ✅ Scrapling 成功 ({result_a.get('size_bytes', 0)} bytes)")
                self.results.append(result_a)
                self.stats["successful"] += 1
                time.sleep(delay)  # 频率控制
                return result_a["data"]
            else:
                print(f"  ❌ Scrapling 失败：{result_a.get('error', 'unknown')}")
                self.failures.append(result_a)
        
        # Plan B: cloudscraper (fallback)
        if fallback and self.scraper:
            time.sleep(1)  # 短暂延迟
            result_b = self.fetch_cloudscraper(url)
            if result_b["status"] == "success":
                print(f"  ✅ cloudscraper 成功 ({result_b.get('size_bytes', 0)} bytes, fallback)")
                self.results.append(result_b)
                self.stats["successful"] += 1
                time.sleep(delay)
                return result_b["data"]
            else:
                print(f"  ❌ cloudscraper 失败：{result_b.get('error', 'unknown')}")
                self.failures.append(result_b)
        
        # All failed
        self.stats["failed"] += 1
        print(f"  ⚠️  所有渠道失败")
        return None
    
    def fetch_batch(self, urls, delay=3, max_failures=5):
        """批量抓取"""
        print(f"\n开始批量抓取 {len(urls)} 个 URL...")
        consecutive_failures = 0
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] {url}")
            result = self.fetch(url, delay=delay)
            
            if result is None:
                consecutive_failures += 1
                if consecutive_failures >= max_failures:
                    print(f"\n⚠️  连续 {max_failures} 次失败，停止批量抓取")
                    break
            else:
                consecutive_failures = 0
            
            # 进度汇报
            if i % 10 == 0:
                self.print_stats()
        
        return self.results
    
    def print_stats(self):
        """打印统计信息"""
        elapsed = (datetime.now() - self.stats["start_time"]).total_seconds()
        print(f"\n--- 统计 ---")
        print(f"总请求：{self.stats['total_requests']}")
        print(f"成功：{self.stats['successful']} ({self.stats['successful']/max(1,self.stats['total_requests'])*100:.1f}%)")
        print(f"失败：{self.stats['failed']}")
        print(f"Scrapling 成功：{self.stats['scrapling_success']}")
        print(f"cloudscraper 成功：{self.stats['cloudscraper_success']}")
        print(f"耗时：{elapsed:.1f}秒")
        print(f"速度：{self.stats['total_requests']/max(1,elapsed)*60:.1f} 请求/分钟")
        print("--------------\n")
    
    def get_report(self):
        """生成执行报告"""
        elapsed = (datetime.now() - self.stats["start_time"]).total_seconds()
        return {
            "timestamp": datetime.now().isoformat(),
            "elapsed_seconds": round(elapsed, 2),
            "statistics": {
                "total_requests": self.stats["total_requests"],
                "successful": self.stats["successful"],
                "failed": self.stats["failed"],
                "success_rate": round(self.stats["successful"]/max(1,self.stats["total_requests"])*100, 1),
                "scrapling_success": self.stats["scrapling_success"],
                "cloudscraper_success": self.stats["cloudscraper_success"],
                "requests_per_minute": round(self.stats["total_requests"]/max(1,elapsed/60), 1)
            },
            "results": self.results,
            "failures": self.failures
        }
    
    def save_report(self, output_path):
        """保存执行报告"""
        report = self.get_report()
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n报告已保存：{output_path}")
        return output_file


def main():
    """测试示例"""
    print("=" * 60)
    print("GitHub 开源爬虫测试")
    print("=" * 60)
    print()
    
    scraper = OpenScraper()
    
    # 测试 URL 列表
    test_urls = [
        "https://httpbin.org/html",  # 测试服务器
        "https://www.linkedin.com/sales/search/people",  # LinkedIn (可能受保护)
        "https://rfq.alibaba.com/post.htm?rfqName=prefab%20house",  # Alibaba RFQ
        "https://httpbin.org/status/403",  # 测试 403 处理
        "https://httpbin.org/delay/5",  # 测试超时处理
    ]
    
    # 执行测试
    results = scraper.fetch_batch(test_urls, delay=2, max_failures=3)
    
    # 打印统计
    scraper.print_stats()
    
    # 保存报告
    report_path = scraper.save_report("/tmp/github-scraper-test-report.json")
    
    # 显示摘要
    report = scraper.get_report()
    print("\n" + "=" * 60)
    print("测试完成！")
    print(f"成功：{report['statistics']['successful']}/{report['statistics']['total_requests']}")
    print(f"成功率：{report['statistics']['success_rate']}%")
    print(f"耗时：{report['elapsed_seconds']}秒")
    print("=" * 60)


if __name__ == "__main__":
    main()

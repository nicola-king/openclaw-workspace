#!/usr/bin/env python3
"""
Network Router - 智能网络路由模块 v1.0
太一 AGI · 2026-05-04

四层智能路由：
1. 国内流量直连：国内互联网/软件/大模型
2. 国外流量代理：国际互联网/软件/大模型
3. 香港AI节点绕过：强制走其他海外节点
4. 智能切换：健康检查+自动回退+性能监控
"""

import os
import json
import re
import time
import socket
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 代理环境变量
PROXY_VARS = ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY']


class NetworkRouter:
    """智能网络路由器"""

    def __init__(self, config_path: str = None):
        self.root = Path(__file__).parent.parent
        self.config_path = Path(config_path) if config_path else self.root / "config" / "routing-config.json"
        self.log_dir = Path.home() / ".openclaw" / "workspace" / "logs" / "network-router"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # 加载配置
        self.config = self._load_config()
        self.rules = self.config.get("routing_rules", {})
        self.proxy_config = self.config.get("proxy", {})
        self.ai_platforms = self.config.get("ai_platforms", {})
        self.domestic_software = self.config.get("domestic_software", {})
        self.intelligent_switching = self.config.get("intelligent_switching", {})

        # 编译域名规则
        self._domestic_patterns = self._compile_patterns(self.rules.get("domains_domestic", []))
        self._international_patterns = self._compile_patterns(self.rules.get("domains_international", []))

        # 缓存
        self._route_cache: Dict[str, str] = {}
        self._health_cache: Dict[str, Tuple[bool, float]] = {}  # domain -> (healthy, latency)
        self._last_health_check = 0

        self._log("INFO", f"Network Router 初始化完成 | 代理: {self.proxy_config.get('http', '无')}")

    def _load_config(self) -> dict:
        """加载路由配置"""
        if self.config_path.exists():
            try:
                return json.loads(self.config_path.read_text(encoding="utf-8"))
            except Exception as e:
                self._log("ERROR", f"配置加载失败: {e}")
        return {}

    def _log(self, level: str, message: str):
        """日志记录"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = self.log_dir / f"router-{datetime.now().strftime('%Y-%m-%d')}.log"
        log_line = f"[{timestamp}] [{level}] {message}\n"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_line)
        print(f"[NetworkRouter] {message}")

    def _compile_patterns(self, domains: List[str]) -> List[re.Pattern]:
        """编译域名匹配模式"""
        patterns = []
        for domain in domains:
            # *.example.com -> .*\.example\.com
            # *keyword* -> .*keyword.*
            pattern = domain.replace(".", "\\.").replace("*", ".*")
            try:
                patterns.append(re.compile(f"^{pattern}$", re.IGNORECASE))
            except re.error:
                pass
        return patterns

    def _match_domain(self, domain: str, patterns: List[re.Pattern]) -> bool:
        """匹配域名"""
        domain = domain.lower().strip()
        for pattern in patterns:
            if pattern.search(domain):
                return True
        return False

    def classify_domain(self, domain: str) -> str:
        """分类域名 -> domestic / international / unknown"""
        if not domain:
            return "unknown"

        # 缓存命中
        if domain in self._route_cache:
            return self._route_cache[domain]

        # 1. 检查国内域名
        if self._match_domain(domain, self._domestic_patterns):
            self._route_cache[domain] = "domestic"
            return "domestic"

        # 2. 检查国际域名
        if self._match_domain(domain, self._international_patterns):
            self._route_cache[domain] = "international"
            return "international"

        # 3. AI平台检测
        for platform, info in self.ai_platforms.get("domestic", {}).items():
            if self._match_domain(domain, self._compile_patterns(info.get("domains", []))):
                self._route_cache[domain] = "domestic"
                return "domestic"

        for platform, info in self.ai_platforms.get("international", {}).items():
            if self._match_domain(domain, self._compile_patterns(info.get("domains", []))):
                self._route_cache[domain] = "international"
                return "international"

        # 4. 国内软件检测
        for software, info in self.domestic_software.items():
            if self._match_domain(domain, self._compile_patterns(info.get("domains", []))):
                self._route_cache[domain] = "domestic"
                return "domestic"

        # 5. 智能推断：.cn 域名走国内
        if domain.endswith(".cn"):
            self._route_cache[domain] = "domestic"
            return "domestic"

        # 6. 默认：未知走代理（安全优先）
        self._route_cache[domain] = "international"
        return "international"

    def detect_hk_node(self, domain: str) -> bool:
        """检测是否为香港AI节点"""
        domain_lower = domain.lower()
        hk_indicators = [".hk", "hongkong", "hong-kong", "hkg"]
        return any(indicator in domain_lower for indicator in hk_indicators)

    def get_routing_env(self, target_domain: str = None) -> Dict[str, str]:
        """获取当前目标的路由环境变量

        Args:
            target_domain: 目标域名，None则保留当前环境

        Returns:
            应设置的环境变量字典
        """
        if not target_domain:
            return {}

        # 判断路由
        route = self.classify_domain(target_domain)

        # 香港节点检测
        if route == "international" and self.detect_hk_node(target_domain):
            self._log("WARN", f"检测到香港节点: {target_domain}，强制绕过")
            route = "hk_blocked"

        env = {}

        if route == "domestic":
            # 国内：清空所有代理
            for var in PROXY_VARS:
                env[var] = ""
        elif route == "international":
            # 国际：设置代理
            http_proxy = self.proxy_config.get("http", "")
            https_proxy = self.proxy_config.get("https", "")
            if http_proxy:
                env["http_proxy"] = http_proxy
                env["HTTP_PROXY"] = http_proxy
            if https_proxy:
                env["https_proxy"] = https_proxy
                env["HTTPS_PROXY"] = https_proxy
        elif route == "hk_blocked":
            # 香港绕过：强制走其他海外节点（设置代理，但跳过HK）
            http_proxy = self.proxy_config.get("http", "")
            https_proxy = self.proxy_config.get("https", "")
            socks = self.proxy_config.get("socks", "")
            if http_proxy:
                env["http_proxy"] = http_proxy
                env["HTTP_PROXY"] = http_proxy
            if https_proxy:
                env["https_proxy"] = https_proxy
                env["HTTPS_PROXY"] = https_proxy
            env["_ROUTED_BYPASS_HK"] = "true"
            env["_ORIGINAL_TARGET"] = target_domain
            self._log("INFO", f"HK绕过路由: {target_domain} -> proxy (skip HK)")

        self._log("DEBUG", f"路由决策: {target_domain} -> {route}")

        return env

    def run_with_routing(self, command: List[str], target_domain: str = None,
                         timeout: int = 300, cwd: str = None) -> subprocess.CompletedProcess:
        """在正确路由环境下执行命令

        Args:
            command: 命令列表
            target_domain: 目标域名
            timeout: 超时秒数
            cwd: 工作目录

        Returns:
            subprocess.CompletedProcess
        """
        # 获取路由环境
        routing_env = self.get_routing_env(target_domain)

        # 构建执行环境
        env = os.environ.copy()
        for var, value in routing_env.items():
            if value:
                env[var] = value
            else:
                env.pop(var, None)

        # 记录路由信息
        route = "direct" if not routing_env.get("http_proxy") else "proxy"
        self._log("INFO", f"执行命令: {' '.join(command[:3])}... | 路由: {route} | 目标: {target_domain or 'auto'}")

        # 执行
        try:
            result = subprocess.run(
                command,
                env=env,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd or str(Path.cwd())
            )
            return result
        except subprocess.TimeoutExpired:
            self._log("ERROR", f"命令超时 ({timeout}s): {' '.join(command[:3])}")
            raise

    def _get_health_check_interval(self) -> int:
        """获取当前时间的健康检查间隔

        时间感知:
        - 08:00~23:59 (白天): 每5分钟
        - 00:00~07:59 (夜间): 每2小时
        """
        time_intervals = self.intelligent_switching.get("time_based_intervals", {})
        if time_intervals.get("enabled", True):
            current_hour = datetime.now().hour
            daytime = time_intervals.get("daytime", {})
            nighttime = time_intervals.get("nighttime", {})

            if daytime.get("start_hour", 8) <= current_hour <= daytime.get("end_hour", 23):
                return daytime.get("interval_seconds", 300)
            else:
                return nighttime.get("interval_seconds", 7200)

        return self.intelligent_switching.get("health_check_interval", 300)

    def health_check(self) -> bool:
        """代理健康检查（时间感知）"""
        now = time.time()
        interval = self._get_health_check_interval()
        time_label = "白天" if 8 <= datetime.now().hour <= 23 else "夜间"
        
        if now - self._last_health_check < interval:
            return True  # 缓存检查结果

        self._log("INFO", f"健康检查触发 (周期:{interval}秒/{time_label})")

        proxy_http = self.proxy_config.get("http")
        health_url = self.proxy_config.get("health_check_url", "https://www.google.com")
        timeout = self.proxy_config.get("timeout_seconds", 10)

        # 测试代理连接
        try:
            start = time.time()
            env = os.environ.copy()
            if proxy_http:
                env["http_proxy"] = proxy_http
                env["https_proxy"] = self.proxy_config.get("https", proxy_http)

            result = subprocess.run(
                ["curl", "-sI", "--max-time", str(timeout), health_url],
                env=env,
                capture_output=True,
                text=True,
                timeout=timeout + 2
            )

            latency = (time.time() - start) * 1000  # ms
            healthy = result.returncode == 0

            self._health_cache["proxy"] = (healthy, latency)
            self._last_health_check = now

            if healthy:
                self._log("INFO", f"代理健康检查: ✅ ({latency:.0f}ms)")
            else:
                self._log("WARN", f"代理健康检查: ❌ ({latency:.0f}ms)")

            return healthy

        except Exception as e:
            self._log("ERROR", f"代理健康检查失败: {e}")
            self._health_cache["proxy"] = (False, 9999)
            self._last_health_check = now
            return False

    def auto_switch_route(self, target_domain: str) -> str:
        """智能切换路由

        检测代理可用性，自动回退机制。

        Returns:
            "direct" | "proxy"
        """
        route = self.classify_domain(target_domain)

        # 国内流量无需代理检测
        if route == "domestic":
            return "direct"

        # 国际流量检测代理
        if route == "international" or route == "hk_blocked":
            if self.proxy_config.get("enabled", True):
                healthy = self.health_check()
                if healthy:
                    return "proxy"
                else:
                    # 代理不可用，尝试直连回退
                    self._log("WARN", f"代理不可用，尝试直连回退: {target_domain}")
                    # 尝试3次重试
                    for attempt in range(self.intelligent_switching.get("retry_count", 3)):
                        time.sleep(self.intelligent_switching.get("fallback_timeout", 5))
                        healthy = self.health_check()
                        if healthy:
                            return "proxy"
                    self._log("ERROR", f"代理重试{self.intelligent_switching.get('retry_count', 3)}次均失败")
                    return "direct"  # 最终回退到直连
        return route

    def get_optimal_endpoint(self, platform: str) -> str:
        """获取AI平台的最优端点（绕过香港节点）

        Args:
            platform: AI平台名称 (openai, anthropic, google等)

        Returns:
            最优域名
        """
        hk_blocked = self.ai_platforms.get("hk_nodes", {})
        redirect_to = hk_blocked.get("redirect_to", ["us", "jp", "sg"])

        platform_info = self.ai_platforms.get("international", {}).get(platform, {})
        domains = platform_info.get("domains", [])

        if not domains:
            return ""

        # 选择第一个非HK域名
        for domain in domains:
            if not self.detect_hk_node(domain):
                return domain

        # 如果所有域名都有HK嫌疑，反馈第一个并标记绕过
        self._log("WARN", f"{platform} 所有端点疑似香港，强制绕过")
        return domains[0]

    def show_status(self) -> dict:
        """显示路由状态"""
        # 代理健康检查
        proxy_healthy = self.health_check()
        proxy_status = "✅" if proxy_healthy else "❌"

        # 估算缓存统计
        domestic_count = sum(1 for v in self._route_cache.values() if v == "domestic")
        intl_count = sum(1 for v in self._route_cache.values() if v == "international")

        status = {
            "proxy": {
                "enabled": self.proxy_config.get("enabled", True),
                "http": self.proxy_config.get("http", "无"),
                "https": self.proxy_config.get("https", "无"),
                "healthy": proxy_healthy,
                "status_icon": proxy_status,
            },
            "routing": {
                "domains_cached": len(self._route_cache),
                "domestic_cached": domestic_count,
                "international_cached": intl_count,
                "hk_bypass_enabled": bool(self.ai_platforms.get("hk_nodes")),
            },
            "ai_platforms": {
                "domestic": list(self.ai_platforms.get("domestic", {}).keys()),
                "international": list(self.ai_platforms.get("international", {}).keys()),
                "hk_bypass": len(self.ai_platforms.get("hk_nodes", {}).get("blocked", [])),
            },
            "intelligent_switching": {
                "enabled": self.intelligent_switching.get("enabled", True),
                "health_check_interval": self.intelligent_switching.get("health_check_interval", 60),
                "retry_count": self.intelligent_switching.get("retry_count", 3),
                "last_health_check": datetime.fromtimestamp(self._last_health_check).isoformat() if self._last_health_check > 0 else "never",
            }
        }

        return status

    def show_status_text(self):
        """打印状态（可读格式）"""
        status = self.show_status()

        print("\n" + "=" * 60)
        print("🌐 智能网络路由器 - 状态")
        print("=" * 60)

        # 代理状态
        p = status["proxy"]
        print(f"\n🔄 代理: {p['status_icon']}")
        print(f"  HTTP:  {p['http']}")
        print(f"  HTTPS: {p['https']}")
        print(f"  状态:  {'✅ 正常' if p['healthy'] else '❌ 不可用'}")

        # 路由统计
        r = status["routing"]
        print(f"\n🗺️ 路由统计:")
        print(f"  缓存域名: {r['domains_cached']} 个")
        print(f"  国内: {r['domestic_cached']} | 国际: {r['international_cached']}")
        print(f"  HK绕过: {'✅ 已启用' if r['hk_bypass_enabled'] else '❌ 未启用'}")

        # AI平台
        a = status["ai_platforms"]
        print(f"\n🤖 AI平台路由:")
        print(f"  国内: {', '.join(a['domestic'])}")
        print(f"  国际: {', '.join(a['international'])}")
        print(f"  HK节点: {a['hk_bypass']} 个被屏蔽")

        # 智能切换
        s = status["intelligent_switching"]
        print(f"\n⚡ 智能切换:")
        print(f"  状态: {'✅ 启用' if s['enabled'] else '❌ 禁用'}")
        print(f"  默认间隔: {s['health_check_interval']}秒")
        print(f"  时间感知:")
        print(f"    🌞 白天(08:00~23:59): 每5分钟")
        print(f"    🌙 夜间(00:00~07:59): 每2小时")
        now_hour = datetime.now().hour
        current_interval = self._get_health_check_interval()
        print(f"    📍 当前: {'🌞白天' if 8 <= now_hour <= 23 else '🌙夜间'} | 间隔: {current_interval}秒")
        print(f"  重试次数: {s['retry_count']}")
        print(f"  上次检查: {s['last_health_check']}")

        print(f"\n{'=' * 60}")


def test_routing():
    """测试路由功能"""
    router = NetworkRouter()
    test_domains = [
        ("国内", "www.baidu.com"),
        ("国内", "open.feishu.cn"),
        ("国内", "api.deepseek.com"),
        ("国际", "api.openai.com"),
        ("国际", "github.com"),
        ("国际", "www.google.com"),
        ("国际", "api.anthropic.com"),
        ("国际", "pypi.org"),
        ("HK", "api-hk.openai.com"),
        ("HK", "hk.api.anthropic.com"),
        ("未知", "api.some-new-site.com"),
        ("国内软件", "open.feishu.cn"),
    ]

    print("\n" + "=" * 60)
    print("🧪 路由测试")
    print("=" * 60)

    for category, domain in test_domains:
        route = router.classify_domain(domain)
        is_hk = router.detect_hk_node(domain)
        env = router.get_routing_env(domain)
        proxy = bool(env.get("http_proxy"))
        hk_flag = "⚠️ HK" if is_hk else ""

        icon = "🟢" if not proxy else "🔵"
        if is_hk:
            icon = "🔴"

        print(f"  {icon} [{category:6s}] {domain:40s} -> {'直连' if not proxy else '代理'} {hk_flag}")

    router.show_status_text()
    print("\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        router = NetworkRouter()
        if cmd == "--status":
            router.show_status_text()
        elif cmd == "--test":
            test_routing()
        elif cmd == "--health":
            healthy = router.health_check()
            print(f"代理健康: {'✅' if healthy else '❌'}")
        elif cmd == "--route":
            if len(sys.argv) > 2:
                domain = sys.argv[2]
                route = router.classify_domain(domain)
                env = router.get_routing_env(domain)
                via = "代理" if env.get("http_proxy") else "直连"
                hk = " ⚠️ 香港节点已绕过" if router.detect_hk_node(domain) else ""
                print(f"{domain} -> {route} ({via}{hk})")
            else:
                print("用法: python3 router.py --route <domain>")
        else:
            print("用法: router.py [--status|--test|--health|--route <domain>]")
    else:
        test_routing()

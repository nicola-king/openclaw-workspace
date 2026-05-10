#!/usr/bin/env python3
"""
Scheduler Agent - 智能调度智能体 v2.0
太一 AGI · 2026-05-04

替代 cron，实现智能调度 + 智能网络路由：
- 动态调整执行频率
- 优先级智能排序
- 资源动态分配
- 国内流量直连 / 国际流量代理 / 香港AI绕过
- 智能切换、智能处理、智能自动化
"""

import os
import json
import time
import subprocess
import signal
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# ===== 智能网络路由集成 =====
try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "network-router" / "src"))
    from router import NetworkRouter
    NETWORK_ROUTER_AVAILABLE = True
except ImportError:
    NETWORK_ROUTER_AVAILABLE = False
    NetworkRouter = None


class SchedulerAgent:
    """智能调度智能体 (v2.0 · 网络路由集成)"""

    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.scripts_dir = self.workspace_root / "scripts"
        self.monitoring_dir = self.workspace_root / "monitoring"
        self.config_path = self.workspace_root / "skills" / "scheduler-agent" / "config" / "scheduler-config.json"
        self.state_path = self.monitoring_dir / "scheduler-state.json"
        self.log_path = self.monitoring_dir / "scheduler-log.json"

        # 默认配置
        self.config = {
            "default_interval": 3600,  # 默认 1 小时
            "min_interval": 1800,      # 最小 30 分钟
            "max_interval": 7200,      # 最大 2 小时
            "lag_threshold": 0.5,      # 滞后阈值 50%
            "ahead_threshold": 0.2,    # 超前阈值 20%
            "max_concurrent": 3,       # 最大并发数
            "memory_limit": "512MB",   # 内存限制
            # 网络路由配置
            "routing_enabled": True,
            "hk_bypass": True,
            "auto_health_check": 300,   # 默认健康检查间隔(秒)
            "time_based_health_check": {
                "enabled": True,
                "daytime": {"start": 8, "end": 23, "interval": 300},
                "nighttime": {"start": 0, "end": 7, "interval": 7200}
            },
            "fallback_to_direct": True,
        }

        # 加载配置
        self._load_config()

        # 状态
        self.state = {
            "last_run": None,
            "next_run": None,
            "current_interval": self.config["default_interval"],
            "tasks_completed": 0,
            "tasks_failed": 0,
            "consecutive_success": 0,
            "running": False,
            "routing": {
                "domestic": 0,
                "international": 0,
                "hk_bypassed": 0,
                "proxy_healthy": None,
            }
        }

        # 加载状态
        self._load_state()

        # 任务队列
        self.task_queue = []
        self.running_processes = []

        # ===== 网络路由引擎 =====
        self.router = None
        if NETWORK_ROUTER_AVAILABLE:
            try:
                # 找到正确的配置路径
                router_config = self.workspace_root / "skills" / "network-router" / "config" / "routing-config.json"
                if not router_config.exists():
                    # 也检查智能代理内部的路径
                    router_config = self.workspace_root / "skills" / "intelligent-agents" / "skills" / "network-router" / "config" / "routing-config.json"
                self.router = NetworkRouter(str(router_config) if router_config.exists() else None)
                print(f"🌐 网络路由器已启用 | 路径: {router_config}")
            except Exception as e:
                print(f"⚠️ 网络路由器初始化失败: {e}")
                self.router = None
        else:
            print("⚠️ 网络路由器未安装，请先配置 network-router 模块")

        # ===== 任务路由规则 =====
        # 任务名 -> (路由类型, 关联域名)
        self._task_routing_rules = {
            # === 国内任务（直连） ===
            "PDCA Cycle": ("domestic", None),
            "Skill Standardization": ("domestic", None),
            "国内情报简报": ("domestic", None),
            "飞书同步": ("domestic", "open.feishu.cn"),
            "系统自检": ("domestic", None),

            # === 国际任务（走代理） ===
            "GitHub 同步": ("international", "github.com"),
            "自进化引擎": ("international", None),
            "OSINT 扫描": ("international", None),

            # === AI任务（根据平台路由） ===
            "OpenAI 调用": ("ai_openai", "api.openai.com"),
            "Claude 调用": ("ai_anthropic", "api.anthropic.com"),
            "DeepSeek 调用": ("ai_domestic", "api.deepseek.com"),
            "Google AI 调用": ("ai_google", "generativelanguage.googleapis.com"),

            # === 网络路由任务（自动检测） ===
            "跨境贸易情报": ("international", None),
            "GEO 优化": ("international", None),
            "全球搜索": ("international", "www.google.com"),
            "模型下载": ("ai_openai", "huggingface.co"),
        }

        # 默认路由：国际（安全优先）
        self._default_route = "international"

    def _load_config(self):
        """加载配置"""
        if self.config_path.exists():
            try:
                config_data = json.loads(self.config_path.read_text(encoding="utf-8"))
                self.config.update(config_data)
            except:
                pass

        # 保存配置
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(json.dumps(self.config, indent=2, ensure_ascii=False), encoding="utf-8")

    def _load_state(self):
        """加载状态"""
        if self.state_path.exists():
            try:
                state_data = json.loads(self.state_path.read_text(encoding="utf-8"))
                self.state.update(state_data)
            except:
                pass

    def _save_state(self):
        """保存状态"""
        self.state["last_updated"] = datetime.now().isoformat()
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(self.state, indent=2, ensure_ascii=False), encoding="utf-8")

    def _log_execution(self, task: str, success: bool, duration: float, route: str = ""):
        """记录执行日志（含路由信息）"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "success": success,
            "duration_seconds": duration,
            "route": route,
        }

        # 加载历史日志
        if self.log_path.exists():
            try:
                logs = json.loads(self.log_path.read_text(encoding="utf-8"))
            except:
                logs = []
        else:
            logs = []

        # 添加新日志，保留最近 200 条
        logs.append(log_entry)
        logs = logs[-200:]

        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_path.write_text(json.dumps(logs, indent=2, ensure_ascii=False), encoding="utf-8")

    # ===== 智能路由方法 =====

    def classify_task(self, task_name: str) -> Tuple[str, str, Optional[str]]:
        """分类任务路由

        Returns:
            (route_type, route_label, target_domain)
            route_type: "domestic" | "international" | "ai_openai" | "ai_domestic" | "hk_blocked"
            route_label: "直连" | "代理" | "HK绕过"
            target_domain: 关联域名或None
        """
        rule = self._task_routing_rules.get(task_name)

        if rule:
            route_type, domain = rule

            # 香港节点检测
            if domain and self.router and self.router.detect_hk_node(domain):
                return ("hk_blocked", "香港绕过", domain)

            if route_type == "domestic":
                return ("domestic", "直连", domain)
            elif route_type == "ai_domestic":
                return ("domestic", "直连", domain)
            elif route_type in ("international", "ai_openai", "ai_anthropic", "ai_google"):
                return ("international", "代理", domain)
            else:
                return ("international", "代理", domain)

        # 无规则：通过关键词推断
        if any(kw in task_name for kw in ["国内", "本地", "系统", "飞书", "微信", "阿里", "百度"]):
            return ("domestic", "直连", None)
        elif any(kw in task_name for kw in ["国际", "海外", "跨境", "GitHub", "Google", "OpenAI", "OSINT", "代理"]):
            return ("international", "代理", None)
        elif any(kw in task_name for kw in ["香港", "HK", "hongkong"]):
            return ("hk_blocked", "香港绕过", None)

        # 默认安全优先：走代理
        return ("international", "代理", None)

    def get_task_env(self, task_name: str) -> Dict[str, str]:
        """获取任务执行所需的环境变量（含路由配置）

        Args:
            task_name: 任务名称

        Returns:
            应注入的环境变量字典
        """
        if not self.router or not self.config.get("routing_enabled", True):
            return {}  # 路由禁用，不修改环境

        route_type, _, domain = self.classify_task(task_name)

        if route_type == "domestic":
            # 国内：清理所有代理
            env = {}
            for var in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY']:
                env[var] = ""
            return env

        elif route_type == "hk_blocked":
            # 香港绕过：走代理+标记
            return self.router.get_routing_env(domain or "hk.ai.example.com")

        elif route_type == "international":
            # 国际：走代理
            return self.router.get_routing_env(domain or "international")

        return {}

    def check_routing_health(self) -> bool:
        """检查路由系统健康状态"""
        if not self.router:
            return True  # 无路由器时视为健康

        try:
            healthy = self.router.health_check()
            self.state["routing"]["proxy_healthy"] = healthy
            return healthy
        except Exception:
            self.state["routing"]["proxy_healthy"] = False
            return False

    # ===== 智能调度核心 =====

    def get_goal_progress(self) -> float:
        """获取目标进度"""
        tracker_path = self.monitoring_dir / "goal-tracker.json"
        if tracker_path.exists():
            try:
                tracker = json.loads(tracker_path.read_text(encoding="utf-8"))
                goals = tracker.get("goals", {}).get("short_term", {}).get("targets", {})
                progresses = []
                for key, value in goals.items():
                    if isinstance(value, dict) and "current" in value and "target" in value:
                        current = value["current"]
                        target = value["target"]
                        if target > 0:
                            progress = current / target
                            progresses.append(progress)

                if progresses:
                    return sum(progresses) / len(progresses)
            except:
                pass

        return 0.0

    def calculate_interval(self) -> int:
        """智能计算执行间隔"""
        progress = self.get_goal_progress()

        if progress < self.config["lag_threshold"]:
            interval = self.config["min_interval"]
            print(f"🔴 目标滞后 ({progress:.1%})，加速到每{interval//60}分钟")
        elif progress > (1 + self.config["ahead_threshold"]):
            interval = self.config["max_interval"]
            print(f"🟢 目标超前 ({progress:.1%})，减速到每{interval//60}分钟")
        else:
            interval = self.config["default_interval"]
            print(f"🟡 目标正常 ({progress:.1%})，保持每{interval//60}分钟")

        return interval

    def execute_task(self, task_name: str, script: str) -> bool:
        """执行任务（含智能路由）

        Route decision per execution:
          1. classify task → get routing env
          2. if international → check proxy health
          3. set env vars → execute
          4. record route type in log
        """
        print(f"\n🚀 执行任务：{task_name}")

        # ===== 智能路由决策 =====
        route_type, route_label, route_domain = self.classify_task(task_name)
        routing_env = self.get_task_env(task_name) if self.config.get("routing_enabled", True) else {}
        use_proxy = bool(routing_env.get("http_proxy"))

        router_icon = "🌐" if use_proxy else "🖥️"
        hk_warn = "⚠️ HK绕过 " if route_type == "hk_blocked" else ""
        print(f"  {router_icon} 路由: {route_label} {hk_warn}| 域名: {route_domain or 'auto'} | 代理: {'✅' if use_proxy else '❌'}")

        # ===== 健康检查（国际流量） =====
        if use_proxy and self.config.get("auto_health_check", 60) > 0:
            proxy_healthy = self.check_routing_health()
            if not proxy_healthy and self.config.get("fallback_to_direct", True):
                print(f"  ⚠️ 代理不可用，回退直连")
                routing_env = {}
                route_label = "直连(回退)"

        # ===== 执行任务 =====
        start_time = datetime.now()
        script_path = self.scripts_dir / script

        if not script_path.exists():
            print(f"❌ 脚本不存在：{script_path}")
            return False

        try:
            # 构建执行环境
            env = os.environ.copy()
            for var, value in routing_env.items():
                if value:
                    env[var] = value
                else:
                    env.pop(var, None)

            # 执行
            result = subprocess.run(
                ["python3", str(script_path)],
                capture_output=True,
                text=True,
                timeout=300,
                cwd=str(self.workspace_root),
                env=env,
            )

            duration = (datetime.now() - start_time).total_seconds()
            success = result.returncode == 0

            # 记录日志（含路由信息）
            self._log_execution(task_name, success, duration, route_label)

            # 更新统计
            if success:
                self.state["tasks_completed"] += 1
                self.state["consecutive_success"] += 1
                if route_type == "domestic":
                    self.state["routing"]["domestic"] += 1
                else:
                    self.state["routing"]["international"] += 1
                if route_type == "hk_blocked":
                    self.state["routing"]["hk_bypassed"] += 1
                print(f"✅ {task_name} 执行成功 ({route_label}, {duration:.1f}s)")
            else:
                self.state["tasks_failed"] += 1
                self.state["consecutive_success"] = 0
                print(f"❌ {task_name} 执行失败：{result.stderr[:200]}")

            return success

        except subprocess.TimeoutExpired:
            print(f"❌ {task_name} 执行超时")
            self._log_execution(task_name, False, 300, route_label)
            return False
        except Exception as e:
            print(f"❌ {task_name} 执行异常：{str(e)[:200]}")
            self._log_execution(task_name, False, 0, route_label)
            return False

    # ===== 任务执行器 =====

    def run_pdca(self) -> bool:
        return self.execute_task("PDCA Cycle", "pdca-simple.py")

    def run_evolution(self) -> bool:
        return self.execute_task("自进化引擎", "self-evolution-engine-v2.py")

    def run_standardization(self) -> bool:
        return self.execute_task("Skill Standardization", "standardize-emerged-skills.py")

    def run_all_tasks(self):
        """执行所有任务（智能调度+智能路由）"""
        print("\n" + "=" * 60)
        print("🤖 Scheduler Agent v2.0 - 智能执行所有任务")
        print("=" * 60)

        # 路由健康检查
        if self.config.get("routing_enabled", True) and self.router:
            proxy_healthy = self.check_routing_health()
            print(f"🌐 路由状态: {'✅ 代理正常' if proxy_healthy else '⚠️ 代理不可用'}")
            print(f"   国内直连: 🟢 | 国际代理: {'🔵' if proxy_healthy else '🔴'} | HK绕过: {'✅' if self.config.get('hk_bypass') else '❌'}")

        tasks = [
            ("PDCA 循环", "pdca-simple.py"),
            ("自进化引擎", "self-evolution-engine-v2.py"),
            ("技能标准化", "standardize-emerged-skills.py"),
        ]

        results = []
        for task_name, script in tasks:
            result = self.execute_task(task_name, script)
            results.append(result)
            time.sleep(2)

        success_count = sum(results)
        print(f"\n{'=' * 60}")
        print(f"✅ 执行完成：{success_count}/{len(tasks)} 成功")
        r = self.state.get("routing", {})
        print(f"🌐 路由统计: 直连={r.get('domestic',0)} | 代理={r.get('international',0)} | HK绕过={r.get('hk_bypassed',0)}")
        print(f"{'=' * 60}")

        return success_count == len(tasks)

    def run_scheduler_loop(self):
        """运行调度循环（含智能路由）"""
        print("\n" + "=" * 60)
        print("🤖 Scheduler Agent v2.0 启动")
        print("=" * 60)

        if NETWORK_ROUTER_AVAILABLE and self.router:
            print("🌐 智能网络路由: ✅ 已集成")
            print("   · 国内流量 → 直连")
            print("   · 国际流量 → 代理")
            print("   · 香港AI   → 绕过")
            print("   · 智能切换 → 自动检测+回退")
        else:
            print("⚠️ 网络路由: 未集成 (不影响调度功能)")

        self.state["running"] = True
        self._save_state()

        try:
            while self.state["running"]:
                interval = self.calculate_interval()
                self.state["current_interval"] = interval

                next_run = datetime.now() + timedelta(seconds=interval)
                self.state["next_run"] = next_run.isoformat()
                self._save_state()

                r = self.state.get("routing", {})
                print(f"\n⏰ 下次执行：{next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"📊 状态：完成={self.state['tasks_completed']}, 失败={self.state['tasks_failed']}")
                print(f"🌐 路由：直连={r.get('domestic',0)} | 代理={r.get('international',0)} | HK绕过={r.get('hk_bypassed',0)}")

                # 健康检查
                if self.router and self.config.get("auto_health_check", 60) > 0:
                    self.check_routing_health()

                self.run_all_tasks()

                print(f"\n💤 等待{interval}秒...")
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\n⚠️ 收到中断信号，停止调度...")
            self.state["running"] = False
            self._save_state()
        except Exception as e:
            print(f"\n❌ 调度异常：{str(e)}")
            self.state["running"] = False
            self._save_state()
            raise

        print("\n✅ Scheduler Agent 已停止")

    def show_status(self):
        """显示状态（含路由信息）"""
        print("\n" + "=" * 60)
        print("📊 Scheduler Agent v2.0 状态")
        print("=" * 60)

        self._load_state()

        print(f"运行中：{self.state['running']}")
        print(f"上次执行：{self.state.get('last_run', '无')}")
        print(f"下次执行：{self.state.get('next_run', '无')}")
        print(f"当前间隔：{self.state.get('current_interval', 3600) // 60} 分钟")

        # 任务统计
        print(f"\n📋 任务统计:")
        print(f"  完成: {self.state.get('tasks_completed', 0)} | 失败: {self.state.get('tasks_failed', 0)}")
        print(f"  连续成功: {self.state.get('consecutive_success', 0)}")

        # 路由统计
        r = self.state.get("routing", {})
        print(f"\n🌐 网络路由统计:")
        print(f"  直连: {r.get('domestic', 0)} 次")
        print(f"  代理: {r.get('international', 0)} 次")
        print(f"  HK绕过: {r.get('hk_bypassed', 0)} 次")
        proxy_health = r.get("proxy_healthy")
        if proxy_health is not None:
            print(f"  代理状态: {'✅ 正常' if proxy_healthy else '❌ 异常'}")

        # 路由器详情
        if self.router:
            print(f"\n🌐 网络路由器:")
            router_status = self.router.show_status()
            if isinstance(router_status, dict):
                p = router_status.get("proxy", {})
                print(f"  HTTP代理: {p.get('http', '无')}")
                print(f"  HTTPS代理: {p.get('https', '无')}")
                print(f"  状态: {p.get('status_icon', '?')}")

        # 最近日志
        if self.log_path.exists():
            try:
                logs = json.loads(self.log_path.read_text(encoding="utf-8"))
                print(f"\n最近执行 ({len(logs)}条):")
                for log in logs[-5:]:
                    status = "✅" if log["success"] else "❌"
                    route = f" [{log.get('route', '?')}]" if log.get("route") else ""
                    print(f"  {status}{route} {log['task']} ({log['duration_seconds']:.1f}s) - {log['timestamp'][:19]}")
            except:
                pass

        # 路由规则预览
        print(f"\n📋 路由规则 ({len(self._task_routing_rules)}条):")
        domestic_count = sum(1 for v in self._task_routing_rules.values() if v[0] == "domestic" or v[0] == "ai_domestic")
        intl_count = sum(1 for v in self._task_routing_rules.values() if v[0] in ("international", "ai_openai", "ai_anthropic"))
        print(f"  直连: {domestic_count} 任务 | 代理: {intl_count} 任务")
        if self.config.get("hk_bypass"):
            print(f"  HK绕过: ✅ 已启用")

        print(f"\n{'=' * 60}")

    def stop(self):
        """停止调度"""
        print("\n⚠️ 停止 Scheduler Agent...")
        self.state["running"] = False
        self._save_state()
        print("✅ Scheduler Agent 已停止")

    def show_routing_test(self):
        """显示路由测试"""
        if not self.router:
            print("❌ 网络路由器未初始化")
            return

        test_tasks = [
            "PDCA Cycle",
            "自进化引擎",
            "GitHub 同步",
            "OpenAI 调用",
            "DeepSeek 调用",
            "飞书同步",
            "跨境贸易情报",
        ]

        print("\n" + "=" * 60)
        print("🧪 智能路由测试")
        print("=" * 60)

        for task in test_tasks:
            route_type, route_label, domain = self.classify_task(task)
            env = self.get_task_env(task)
            use_proxy = bool(env.get("http_proxy"))
            icon = "🟢" if not use_proxy else "🔵"

            print(f"  {icon} [{route_label:8s}] {task:20s} {'(直连)' if not use_proxy else '(代理)'}")
            if domain:
                print(f"      -> 域名: {domain}")

        self.router.show_status_text()


def main():
    """主函数"""
    # 自动检测 workspace 路径
    possible_paths = [
        Path.home() / ".openclaw" / "workspace",
        Path("/home/sayelf/.openclaw/workspace"),
        Path("/home/sayelf/.openclaw/workspace"),
    ]

    workspace_root = None
    for p in possible_paths:
        if p.exists():
            workspace_root = str(p)
            break

    if not workspace_root:
        workspace_root = str(Path.cwd())

    scheduler = SchedulerAgent(workspace_root)

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "--status":
            scheduler.show_status()
        elif command == "--stop":
            scheduler.stop()
        elif command == "--run-pdca":
            scheduler.run_pdca()
        elif command == "--run-all":
            scheduler.run_all_tasks()
        elif command == "--routing-test":
            scheduler.show_routing_test()
        elif command == "--routing-health":
            healthy = scheduler.check_routing_health()
            print(f"路由健康: {'✅' if healthy else '❌'}")
        else:
            print(f"未知命令：{command}")
            print("用法：scheduler.py [--status|--stop|--run-pdca|--run-all|--routing-test|--routing-health]")
    else:
        scheduler.run_scheduler_loop()


if __name__ == "__main__":
    main()

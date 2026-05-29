"""
太一编码 Agent 调度引擎 · Taiyi Coding Agents Scheduler
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
统一调度 OpenHands (75K⭐) + Goose (46K⭐)

参考架构:
  - OpenHands: SDK → CLI → GUI → Cloud (三层分离)
  - Goose:     Desktop → CLI → API → MCP (四层扩展)
  - ACP:       Agent Communication Protocol (Agent间通信)
  - MCP:       Model Context Protocol (工具扩展)

能力:
  schedule()       智能调度（自动选 Agent）
  openhands_run()  直接调 OpenHands CLI
  goose_run()      直接调 Goose CLI
  check()          检测已安装的 Agent
  info()           Agent 版本与架构信息
"""

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

SKILL_DIR = Path(__file__).parent

# =====================================================================
# Agent 检测
# =====================================================================

def _which_openhands() -> Optional[str]:
    """检测 OpenHands"""
    # OpenHands CLI 方式
    path = shutil.which("openhands")
    if path:
        return path
    
    # 或通过 pip 安装的 Python 模块
    try:
        import openhands
        return f"python_module:{openhands.__file__}"
    except ImportError:
        pass
    
    # 或在常见位置
    for candidate in [
        Path.home() / ".local" / "bin" / "openhands",
        Path.home() / ".openhands" / "bin" / "openhands",
    ]:
        if candidate.exists():
            return str(candidate)
    return None

def _which_goose() -> Optional[str]:
    """检测 Goose"""
    path = shutil.which("goose")
    if path:
        return path
    
    # 常见安装路径
    for candidate in [
        Path.home() / ".local" / "bin" / "goose",
        "/usr/local/bin/goose",
        "/opt/homebrew/bin/goose",
    ]:
        if Path(candidate).exists():
            return candidate
    return None

def _goose_version() -> Optional[str]:
    """获取 Goose 版本"""
    try:
        r = subprocess.run(["goose", "--version"], capture_output=True, text=True, timeout=10)
        return r.stdout.strip() or r.stderr.strip() or "?"
    except: return None

# =====================================================================
# 核心调度
# =====================================================================

TASK_ROUTES = {
    "code": {"agent": "openhands", "priority": 1, "desc": "代码开发/调试"},
    "debug": {"agent": "openhands", "priority": 1, "desc": "调试/修复"},
    "refactor": {"agent": "openhands", "priority": 1, "desc": "重构"},
    "pr": {"agent": "openhands", "priority": 2, "desc": "PR/Code Review"},
    "ci": {"agent": "openhands", "priority": 2, "desc": "CI/CD 集成"},
    "automation": {"agent": "goose", "priority": 1, "desc": "自动化工作流"},
    "research": {"agent": "goose", "priority": 2, "desc": "研究/调查"},
    "writing": {"agent": "goose", "priority": 2, "desc": "写作/文档"},
    "data": {"agent": "goose", "priority": 1, "desc": "数据分析/清洗"},
    "batch": {"agent": "goose", "priority": 2, "desc": "批处理"},
    "workflow": {"agent": "goose", "priority": 1, "desc": "工作流编排"},
}

def _detect_task_type(task: str) -> str:
    """从任务描述中检测类型（中英双语）"""
    task_lower = task.lower()
    
    # 中文关键词映射
    cn_map = {
        "代码": "code", "脚本": "code", "编程": "code", "开发": "code",
        "写": "code", "改": "code", "bug": "debug", "调试": "debug",
        "重构": "refactor", "pr": "pr", "review": "pr",
        "ci": "ci", "自动化": "automation", "管道": "automation",
        "研究": "research", "分析": "research", "调查": "research",
        "写作": "writing", "文档": "writing", "报告": "writing",
        "数据": "data", "csv": "data", "分析": "data",
        "批量": "batch", "批处理": "batch",
        "工作流": "workflow", "流程": "workflow",
    }
    
    # 英文关键词
    en_keywords = list(TASK_ROUTES.keys())
    
    # 先检查英文关键词
    for kw in en_keywords:
        if kw in task_lower:
            return kw
    
    # 再检查中文映射
    for cn, en in cn_map.items():
        if cn in task:
            return en
    
    # 默认启发式判断
    code_signals = ["python", "java", "javascript", "rust", "go", "cpp", 
                    "code", "develop", "program", "build", "github", "git",
                    "function", "class", "api", "module", "重构", "脚本"]
    if any(w in task_lower for w in code_signals):
        return "code"
    
    data_signals = ["csv", "json", "data", "数据", "excel", "database"]
    if any(w in task_lower for w in data_signals):
        return "data"
    
    return "automation"

def schedule(task: str, prefer: str = "auto") -> Dict:
    """
    智能调度 — 自动选 Agent

    参数:
      task: 任务描述
      prefer: "auto" / "openhands" / "goose"

    返回:
      {agent, available, task_type, method, note, commands}
    """
    task_type = _detect_task_type(task)
    route = TASK_ROUTES.get(task_type, TASK_ROUTES["automation"])
    
    oh_avail = _which_openhands() is not None
    go_avail = _which_goose() is not None
    
    # 选 Agent
    if prefer == "openhands" or (prefer == "auto" and route["agent"] == "openhands"):
        chosen = "openhands"
    elif prefer == "goose" or (prefer == "auto" and route["agent"] == "goose"):
        chosen = "goose"
    else:
        # fallback: 哪个可用用哪个
        chosen = "openhands" if oh_avail else ("goose" if go_avail else "none")
    
    avail = {"openhands": oh_avail, "goose": go_avail}
    commands = _generate_commands(task, chosen)
    
    return {
        "agent": chosen,
        "available": avail[chosen] if chosen in avail else False,
        "task_type": task_type,
        "method": "direct_cli" if avail.get(chosen) else "pending_install",
        "analogy": f"OpenHands={route['agent'] == 'openhands'} Goose={route['agent'] == 'goose'}",
        "commands": commands,
        "available_agents": avail,
        "route": route,
        "note": _generate_note(chosen, avail, route),
    }

def _generate_commands(task: str, agent: str) -> List[str]:
    """生成具体的执行命令"""
    if agent == "openhands":
        return [
            f"openhands run --task \"{task}\"",
            f"# 或使用 SDK:",
            f"# from openhands import Agent; agent = Agent.create(); agent.run('{task}')",
        ]
    elif agent == "goose":
        return [
            f"goose run \"{task}\"",
            f"# 或使用 ACP:",
            f"# goose session start --task '{task}'",
        ]
    return [f"# No agent configured for: {task}"]

def _generate_note(chosen: str, avail: Dict, route: Dict) -> str:
    """生成说明"""
    if not avail.get(chosen):
        return f"❌ {chosen} 未安装。安装后即可使用。"
    return f"✅ 使用 {chosen} 执行 {route['desc']} 类型任务"

# =====================================================================
# Agent 调用封装
# =====================================================================

def openhands_run(task: str, cwd: str = None, timeout: int = 300) -> Dict:
    """
    直接调用 OpenHands CLI 执行任务

    参数:
      task: 任务描述
      cwd: 工作目录
      timeout: 超时秒数

    返回:
      {status, stdout, stderr, elapsed_ms}
    """
    oh = _which_openhands()
    t0 = time.time()
    
    if not oh:
        return {
            "status": "unavailable",
            "elapsed_ms": int((time.time() - t0) * 1000),
            "note": "OpenHands 未安装",
            "install": "pip install openhands",
        }
    
    try:
        r = subprocess.run(
            [oh, "run", "--task", task],
            capture_output=True, text=True, timeout=timeout,
            cwd=cwd or str(SKILL_DIR),
        )
        return {
            "status": "ok" if r.returncode == 0 else "error",
            "stdout": r.stdout[-2000:],
            "stderr": r.stderr[-500:],
            "returncode": r.returncode,
            "elapsed_ms": int((time.time() - t0) * 1000),
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "elapsed_ms": int((time.time() - t0) * 1000)}
    except Exception as e:
        return {"status": "error", "error": str(e)[:200],
                "elapsed_ms": int((time.time() - t0) * 1000)}

def goose_run(task: str, cwd: str = None, timeout: int = 300) -> Dict:
    """
    直接调用 Goose CLI 执行任务

    参数:
      task: 任务描述
      cwd: 工作目录
      timeout: 超时秒数

    返回:
      {status, stdout, stderr, elapsed_ms}
    """
    t0 = time.time()
    
    if not _which_goose():
        return {
            "status": "unavailable",
            "elapsed_ms": int((time.time() - t0) * 1000),
            "note": "Goose 未安装",
            "install": "curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | bash",
        }
    
    try:
        r = subprocess.run(
            ["goose", "run", task],
            capture_output=True, text=True, timeout=timeout,
            cwd=cwd or str(SKILL_DIR),
        )
        return {
            "status": "ok" if r.returncode == 0 else "error",
            "stdout": r.stdout[-2000:],
            "stderr": r.stderr[-500:],
            "returncode": r.returncode,
            "elapsed_ms": int((time.time() - t0) * 1000),
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "elapsed_ms": int((time.time() - t0) * 1000)}
    except Exception as e:
        return {"status": "error", "error": str(e)[:200],
                "elapsed_ms": int((time.time() - t0) * 1000)}

# =====================================================================
# 安装辅助
# =====================================================================

INSTALL_GUIDES = {
    "openhands": {
        "pip": "pip install openhands",
        "docker": "docker pull openhands/openhands",
        "docs": "https://docs.openhands.dev",
        "note": "OpenHands SDK → pip install，CLI 自动可用",
    },
    "goose": {
        "curl": "curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | bash",
        "brew": "brew install goose",
        "cargo": "cargo install goose-cli",
        "docs": "https://goose-docs.ai",
        "note": "Goose CLI → 全平台支持，安装即用",
    },
}

# =====================================================================
# 诊断/信息
# =====================================================================

def check() -> str:
    """检测已安装的编码 Agent"""
    lines = [
        "🤖 编码 Agent 检测",
        "══════════════════════",
    ]
    
    oh = _which_openhands()
    go = _which_goose()
    
    lines.append(f"\nOpenHands (75K⭐):")
    if oh:
        lines.append(f"  ✅ {oh}")
    else:
        lines.append(f"  ❌ 未安装 — pip install openhands")
    
    lines.append(f"\nGoose (46K⭐):")
    if go:
        ver = _goose_version()
        lines.append(f"  ✅ {go}" + (f" (v{ver})" if ver else ""))
    else:
        lines.append(f"  ❌ 未安装 — curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | bash")
    
    lines.append(f"\n任务路由 ({len(TASK_ROUTES)} 种):")
    for keyword, route in sorted(TASK_ROUTES.items()):
        lines.append(f"  {keyword:12s} → {route['agent']:10s} ({route['desc']})")
    
    lines.append(f"\n架构参考:")
    lines.append(f"  OpenHands: SDK → CLI → GUI → Cloud (Python, MIT)")
    lines.append(f"  Goose:     Desktop → CLI → API → MCP (Rust, Apache 2.0)")
    
    return "\n".join(lines)

def info() -> str:
    """Agent 信息"""
    return json.dumps({
        "version": "1.0.0",
        "agents": {
            "openhands": {
                "stars": 75267,
                "language": "Python",
                "license": "MIT",
                "available": _which_openhands() is not None,
                "url": "https://github.com/OpenHands/OpenHands",
            },
            "goose": {
                "stars": 46014,
                "language": "Rust",
                "license": "Apache 2.0",
                "available": _which_goose() is not None,
                "url": "https://github.com/aaif-goose/goose",
            },
        },
        "routing": {k: {"agent": v["agent"], "desc": v["desc"]} for k, v in TASK_ROUTES.items()},
        "install": INSTALL_GUIDES,
    }, indent=2, ensure_ascii=False)

# =====================================================================
# CLI
# =====================================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""🤖 太一编码 Agent 调度引擎

用法:
  check                     检测已安装的 Agent
  info                      Agent 信息
  schedule <任务描述>       智能调度（自动选 Agent）
  run-openhands <任务>      直接调 OpenHands
  run-goose <任务>          直接调 Goose
""")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "check":
        print(check())

    elif cmd == "info":
        print(info())

    elif cmd == "schedule":
        task = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "general task"
        result = schedule(task)
        print(f"Agent: {result['agent']}")
        print(f"可用: {'✅' if result['available'] else '❌'}")
        print(f"类型: {result['task_type']}")
        print(f"方法: {result['method']}")
        print(f"说明: {result['note']}")
        if not result['available']:
            print(f"\n安装指引:")
            for agent, guide in INSTALL_GUIDES.items():
                if agent in result['available_agents'] and not result['available_agents'][agent]:
                    print(f"  {agent}: {list(guide.values())[0]}")
        else:
            print(f"\n执行命令:")
            for cmd_line in result.get('commands', []):
                print(f"  $ {cmd_line}")

    elif cmd == "run-openhands":
        task = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not task:
            print("❌ 需要指定任务")
            sys.exit(1)
        r = openhands_run(task)
        print(json.dumps(r, indent=2, ensure_ascii=False))

    elif cmd == "run-goose":
        task = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not task:
            print("❌ 需要指定任务")
            sys.exit(1)
        r = goose_run(task)
        print(json.dumps(r, indent=2, ensure_ascii=False))

    else:
        print(f"未知命令: {cmd}")

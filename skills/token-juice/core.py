#!/usr/bin/env python3
"""
太一 · TokenJuice 智能压缩模块 v1.0
====================================
借鉴 OpenHuman TokenJuice (27611⭐) 设计理念。

三层规则覆盖：
  Layer 0 — 内置规则（适用于所有工具输出）
  Layer 1 — 用户规则（个人目录覆盖）
  Layer 2 — 项目规则（项目目录覆盖）

压缩策略：
  - truncate: 截断到指定行数
  - dedup: 去重连续行
  - fold: 折叠空白符
  - regex_drop: 正则匹配删除
  - summarize: 用 LLM 做摘要（仅在必要时）
  - keep_header: 保留头部 N 行 + 尾部 N 行

安装：
  pip install pygments  # 可选，用于更好的格式检测
"""

import json
import logging
import re
from pathlib import Path
from typing import Optional

logger = logging.getLogger("taiyi.tokenjuice")

# ═══════════════════════════════════════════════
# §1 内置压缩规则（Layer 0）
# ═══════════════════════════════════════════════

BUILTIN_RULES = {
    # 通用
    "default": {
        "patterns": [".*"],
        "strategies": [
            {"type": "fold", "max_lines": 500},
            {"type": "dedup", "consecutive": 3},
            {"type": "regex_drop", "pattern": r"(?i)(debug|trace|verbose).*"},
        ],
    },
    # Git
    "git_status": {
        "patterns": ["git status", "git diff.*"],
        "strategies": [
            {"type": "keep_header", "header_lines": 3, "tail_lines": 30},
        ],
    },
    "git_log": {
        "patterns": ["git log"],
        "strategies": [
            {"type": "truncate", "max_lines": 50},
        ],
    },
    # 搜索结果
    "search_result": {
        "patterns": ["search.*", "find.*", "grep.*"],
        "strategies": [
            {"type": "truncate", "max_lines": 30},
        ],
    },
    # 错误输出
    "error_output": {
        "patterns": [".*error.*", ".*traceback.*", ".*exception.*"],
        "strategies": [
            {"type": "keep_header", "header_lines": 2, "tail_lines": 20},
        ],
    },
    # JSON
    "json_output": {
        "patterns": [".*\\.json$", "curl.*json"],
        "strategies": [
            {"type": "truncate", "max_lines": 100},
        ],
    },
    # 列表/目录
    "ls_output": {
        "patterns": ["ls.*", "dir.*"],
        "strategies": [
            {"type": "truncate", "max_lines": 50},
            {"type": "dedup", "consecutive": 1},
        ],
    },
}


# ═══════════════════════════════════════════════
# §2 压缩引擎
# ═══════════════════════════════════════════════

class TokenJuice:
    """
    智能 Token 压缩引擎。
    
    在工具输出进入 LLM 上下文之前压缩，减少 token 消耗。
    借鉴 OpenHuman TokenJuice 三层规则架构。
    """

    def __init__(self):
        self.rules = {}
        self.stats = {"total_processed": 0, "total_saved_chars": 0}
        self._load_rules()

    def _load_rules(self):
        """加载所有规则（三层合并）"""
        rules = {}
        
        # Layer 0: 内置规则
        for name, rule in BUILTIN_RULES.items():
            rules[name] = rule
        
        # Layer 1: 用户规则
        user_rules_dir = Path.home() / ".config" / "tokenjuice" / "rules"
        self._load_rules_from_dir(user_rules_dir, rules)
        
        # Layer 2: 项目规则
        project_rules_dir = Path.cwd() / ".tokenjuice" / "rules"
        self._load_rules_from_dir(project_rules_dir, rules)
        
        self.rules = rules

    def _load_rules_from_dir(self, directory: Path, rules: dict):
        """从目录加载规则文件"""
        if not directory.exists():
            return
        for f in directory.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                for name, rule in data.items():
                    rules[name] = rule
                    logger.info(f"  ✅ 加载规则: {name} ({f})")
            except Exception as e:
                logger.warning(f"  ⚠️ 规则加载失败 {f}: {e}")

    def compress(self, tool_name: str, output: str, 
                 max_chars: int = 10000) -> str:
        """
        压缩工具输出。
        
        Args:
            tool_name: 工具名称或命令
            output: 原始输出
            max_chars: 最大字符数（硬限制）
        
        Returns:
            压缩后的输出
        """
        if not output:
            return output
        
        self.stats["total_processed"] += 1
        original_len = len(output)
        
        # 找到匹配的规则
        matched_rules = self._match_rules(tool_name)
        
        compressed = output
        for rule_name in matched_rules:
            rule = self.rules[rule_name]
            for strategy in rule.get("strategies", []):
                compressed = self._apply_strategy(compressed, strategy)
        
        # 硬限制
        if len(compressed) > max_chars:
            compressed = compressed[:max_chars] + "\n... [truncated by TokenJuice]"
        
        saved = original_len - len(compressed)
        self.stats["total_saved_chars"] += saved
        
        if saved > 0:
            ratio = saved / original_len * 100
            logger.info(f"  TokenJuice: {tool_name} → {saved} chars ({ratio:.0f}%)")
        
        return compressed

    def _match_rules(self, tool_name: str) -> list:
        """找到匹配的规则"""
        matched = []
        for name, rule in self.rules.items():
            for pattern in rule.get("patterns", []):
                try:
                    if re.search(pattern, tool_name, re.IGNORECASE):
                        matched.append(name)
                        break
                except re.error:
                    if pattern in tool_name:
                        matched.append(name)
                        break
        return matched

    def _apply_strategy(self, text: str, strategy: dict) -> str:
        """应用单个压缩策略"""
        stype = strategy.get("type", "")
        lines = text.split("\n")
        
        if stype == "truncate":
            max_lines = strategy.get("max_lines", 100)
            if len(lines) > max_lines:
                lines = lines[:max_lines]
                lines.append(f"... [TokenJuice: truncated to {max_lines} lines]")
                return "\n".join(lines)
        
        elif stype == "dedup":
            consecutive = strategy.get("consecutive", 3)
            result = []
            count = 0
            prev = None
            for line in lines:
                if line == prev:
                    count += 1
                    if count <= consecutive:
                        result.append(line)
                else:
                    count = 0
                    result.append(line)
                prev = line
            return "\n".join(result)
        
        elif stype == "fold":
            max_lines = strategy.get("max_lines", 500)
            if len(lines) > max_lines:
                # 保留前 50% 和后 20%
                head_end = max_lines // 2
                tail_start = len(lines) - max_lines // 5
                head = lines[:head_end]
                tail = lines[tail_start:]
                head.append(f"... [TokenJuice: folded {len(lines) - head_end - len(tail)} lines]")
                return "\n".join(head + tail)
        
        elif stype == "regex_drop":
            pattern = strategy.get("pattern", "")
            try:
                return "\n".join(
                    line for line in lines
                    if not re.search(pattern, line)
                )
            except re.error:
                pass
        
        elif stype == "keep_header":
            header = strategy.get("header_lines", 3)
            tail = strategy.get("tail_lines", 20)
            if len(lines) > header + tail:
                head = lines[:header]
                body_len = len(lines) - header - tail
                tail_part = lines[-tail:]
                head.append(f"... [TokenJuice: omitted {body_len} lines]")
                return "\n".join(head + tail_part)
        
        return text

    def stats_report(self) -> dict:
        return {
            "processed": self.stats["total_processed"],
            "saved_chars": self.stats["total_saved_chars"],
            "saved_tokens_est": self.stats["total_saved_chars"] // 2,
        }


# ═══════════════════════════════════════════════
# §3 全局实例
# ═══════════════════════════════════════════════

_instance = None

def get_compressor() -> TokenJuice:
    global _instance
    if _instance is None:
        _instance = TokenJuice()
    return _instance


# ═══════════════════════════════════════════════
# §4 CLI & 测试
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    tj = get_compressor()
    
    print("╔═══════════════════════════════════════════╗")
    print("║  太一 · TokenJuice 测试                   ║")
    print("╚═══════════════════════════════════════════╝")
    print()
    
    # 测试 1: Git 输出
    git_output = """On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  modified:   src/core.py
  modified:   src/utils.py
  modified:   tests/test_core.py
  modified:   tests/test_utils.py

Untracked files:
  new_file.py
  temp_cache/
debug: loading config
debug: connecting to database
debug: query executed in 0.3s
trace: function enter: process_data
trace: function enter: validate_input
trace: function exit: validate_input
debug: cache miss for key: user_123
debug: cache miss for key: user_456
debug: cache miss for key: user_789
trace: function exit: process_data"""
    
    compressed = tj.compress("git status", git_output)
    print(f"📄 Git 输出: {len(git_output)} → {len(compressed)} chars ({len(git_output)-len(compressed)} 节省)")
    print(f"   结果:\n{compressed}")
    print()
    
    # 测试 2: 搜索结果
    search_output = "\n".join([f"result_{i}: some data here for testing" for i in range(200)])
    compressed2 = tj.compress("search", search_output)
    print(f"🔍 搜索结果: {len(search_output)} → {len(compressed2)} chars ({len(search_output)-len(compressed2)} 节省)")
    
    # 测试 3: 统计
    print(f"\n📊 总计: 处理 {tj.stats['total_processed']} 次, 节省 {tj.stats['total_saved_chars']} chars (~{tj.stats['total_saved_chars']//2} tokens)")

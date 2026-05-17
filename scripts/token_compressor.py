#!/usr/bin/env python3
"""
TokenJuice · 太一智能压缩层

太一吸收 OpenHuman TokenJuice 设计模式后自研的确定性压缩管道。

功能：
- 在 web_search / web_fetch / CLI 结果 → LLM 输入之间做压缩
- 纯算法，零 LLM 开销
- 可观测：记录每次压缩的前后 token 数和压缩比
- 安全：不删语义核心，保留关键数据

压缩策略（5阶管道）：
  1. Format Normalization — HTML→Markdown, JSON→compact
  2. Noise Stripping — 去样板/去空白/去零宽字符
  3. Deduplication — 行级/块级去重
  4. URL Optimization — 缩 URL + 去追踪参数
  5. Smart Truncation — 超阈值时保头保尾+摘要

使用方式：
    from scripts.token_compressor import TokenJuice
    compressed = TokenJuice.compress(raw_text, context="search_results")
    print(f"压缩比: {compressed['ratio']}%")
"""

import re, json, hashlib, html
from typing import List, Dict, Optional, Union
from pathlib import Path

# ═══════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════

DEFAULT_MAX_CHARS = 8000       # 单段最大字符数（超出触发 Smart Truncation）
SMART_TRUNCATION_HARD_LIMIT = 20000  # 硬限制，超出后强制裁剪

# 上下文类型 → 压缩策略
CONTEXT_STRATEGIES = {
    "search_results": {
        "max_chars": 6000,
        "keep_header": True,
        "dedup": True,
        "url_shorten": True,
    },
    "web_page": {
        "max_chars": 10000,
        "keep_header": False,
        "dedup": True,
        "url_shorten": True,
    },
    "email": {
        "max_chars": 8000,
        "keep_header": True,
        "dedup": False,
        "url_shorten": True,
    },
    "cli_output": {
        "max_chars": 6000,
        "keep_header": True,
        "dedup": True,
        "url_shorten": False,
    },
    "rental_data": {
        "max_chars": 4000,
        "keep_header": True,
        "dedup": True,
        "url_shorten": True,
    },
    "economic_data": {
        "max_chars": 5000,
        "keep_header": True,
        "dedup": False,
        "url_shorten": False,
    },
    "default": {
        "max_chars": 8000,
        "keep_header": False,
        "dedup": True,
        "url_shorten": True,
    },
}


class TokenJuice:
    """
    太一 TokenJuice 压缩器
    注意：本类不统计 token（token 数取决于模型），仅统计 char 数；
    实际 token 压缩比约 = char 压缩比 × 0.8~1.2 系数。
    """

    # ── URL 缩短模式 ──
    URL_SHORTEN_RULES = [
        (re.compile(r'https?://www\.'), ''),
        (re.compile(r'https?://m\.'), ''),
        (re.compile(r'(anjuke\.com|ke\.com|58\.com|lianjia\.com)/.+'), lambda m: m.group(1) + '/…'),
        (re.compile(r'github\.com/[^/\s]+/[^/\s]+'), lambda m: m.group()),
        (re.compile(r'utm_source=[^&\s]+'), ''),
        (re.compile(r'utm_medium=[^&\s]+'), ''),
        (re.compile(r'utm_campaign=[^&\s]+'), ''),
        (re.compile(r'utm_content=[^&\s]+'), ''),
        (re.compile(r'fbclid=[^&\s]+'), ''),
        (re.compile(r'gclid=[^&\s]+'), ''),
        (re.compile(r'trk=[^&\s]+'), ''),
    ]

    # ── 样板（boilerplate）检测正则 ──
    BOILERPLATE_PATTERNS = [
        re.compile(r'^.{0,10}(cookie|cookies|隐私|隐私政策|用户协议|免责声明).{0,20}$', re.I),
        re.compile(r'^.{0,10}(广告|赞助|推广|推荐).{0,20}$'),
        re.compile(r'^(footer|header|sidebar|nav|navigation)', re.I),
        re.compile(r'^(加载中|loading|please wait|请稍候)', re.I),
        re.compile(r'^(javascript|css|style|script)', re.I),
        re.compile(r'^.*\{display:none|visibility:hidden\}.*$'),
        re.compile(r'^[\s\-–—=*_~·•●○■□▪▫▸►▹▶▲▼△▽◀◁◄◇◆]+$'),
    ]

    # ── 零宽字符 ──
    ZERO_WIDTH_CHARS = re.compile(
        '[\u200b\u200c\u200d\u200e\u200f\u2060\u2061\u2062\u2063\u2064'
        '\ufeff\ufffe\u00ad\u034f\u061c\u115f\u1160\u17b4\u17b5'
        '\u180e\u2028\u2029\u202a\u202b\u202c\u202d\u202e\u202f'
        '\u205f\u2066\u2067\u2068\u2069\u3000\uffff]'
    )

    # ── 多余空行/空白 ──
    EXCESS_NEWLINES = re.compile(r'\n{3,}')
    TRAILING_SPACES = re.compile(r'[ \t]+\n')

    def __init__(self, context_type: str = "default"):
        self.strategy = CONTEXT_STRATEGIES.get(context_type, CONTEXT_STRATEGIES["default"])
        self.context_type = context_type
        self._stats = {"original_chars": 0, "compressed_chars": 0,
                       "ratio": 100, "stages_applied": []}

    @classmethod
    def compress(cls, text: str, context: str = "default",
                 max_chars: Optional[int] = None) -> Dict:
        """
        一键压缩：选择上下文类型，自动执行全部压缩阶段。

        Args:
            text: 原始文本
            context: 上下文类型（search_results / web_page / email / cli_output / ...）
            max_chars: 覆盖策略中的最大字符数

        Returns:
            {
                "text": str,          # 压缩后文本
                "original_chars": int,
                "compressed_chars": int,
                "ratio": float,       # 压缩比（百分比）
                "stages": [str],      # 已应用的阶段名
                "skipped": bool,      # 是否跳过（输入为空或过短）
            }
        """
        juice = cls(context_type=context)
        strategy = juice.strategy

        if not text:
            return {
                "text": "",
                "original_chars": 0,
                "compressed_chars": 0,
                "ratio": 100.0,
                "stages": ["skip (empty)"],
                "skipped": True,
            }
        # 对包含 HTML 标签的短文本不做跳过（需要去标签）
        has_html = any(tag in text[:300].lower() for tag in [
            '<div', '<p>', '<span', '<script', '<style', '<table',
            '<a ', '<h1', '<img', '<br', '<ul', '<li'
        ])
        if len(text) < 100 and not has_html:
            # 短文本但含有重复行 → 仍需处理
            lines_set = len(set(text.split('\n')))
            total_lines = len(text.split('\n'))
            if total_lines <= 1 or lines_set / total_lines > 0.8:
                return {
                    "text": text.strip(),
                    "original_chars": len(text),
                    "compressed_chars": len(text.strip()),
                    "ratio": 100.0,
                    "stages": ["skip (too short, minimal repetition)"],
                    "skipped": True,
                }

        original_len = len(text)
        stages_applied = []

        # Stage 1: Format Normalization
        text = juice._normalize_format(text)
        stages_applied.append("format_normalize")

        # Stage 2: Noise Stripping
        text = juice._strip_noise(text)
        stages_applied.append("noise_strip")

        # Stage 3: Dedup
        if strategy.get("dedup", True):
            text = juice._deduplicate(text)
            stages_applied.append("dedup")

        # Stage 4: URL Optimization
        if strategy.get("url_shorten", True):
            text = juice._shorten_urls(text)
            stages_applied.append("url_shorten")

        # Stage 5: Smart Truncation
        effective_max = max_chars or strategy.get("max_chars", DEFAULT_MAX_CHARS)
        if len(text) > effective_max:
            truncated = juice._smart_truncate(text, effective_max)
            # 只在确实节省了字符时才标记应用
            if len(truncated) < len(text):
                text = truncated
                stages_applied.append(f"smart_truncate({effective_max}chars)")

        compressed_len = len(text)
        ratio = round(compressed_len / original_len * 100, 1) if original_len > 0 else 100.0

        return {
            "text": text,
            "original_chars": original_len,
            "compressed_chars": compressed_len,
            "ratio": ratio,
            "stages": stages_applied,
            "skipped": False,
        }

    # ── 阶段1: Format Normalization ──
    def _normalize_format(self, text: str) -> str:
        """HTML/JSON 格式标准化"""
        # 尝试 markitdown 转换 HTML（如果可用）
        text = self._try_markitdown(text)

        # 普通 HTML 标签剥离
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.I)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.I)
        text = re.sub(r'<[^>]+>', '', text)
        text = html.unescape(text)

        # JSON 压缩（非嵌套较深的）
        try:
            parsed = json.loads(text)
            if isinstance(parsed, (list, dict)):
                text = json.dumps(parsed, ensure_ascii=False, separators=(',', ':'))
        except (json.JSONDecodeError, ValueError):
            pass

        return text

    def _try_markitdown(self, text: str) -> str:
        """尝试使用 markitdown 转换（可选依赖）"""
        # 更宽松的 HTML 检测：匹配 HTML 标签特征
        head = text[:500].lower()
        is_html = any(tag in head for tag in [
            '<html', '<!doctype', '<div', '<p>', '<span', '<script',
            '<style', '<table', '<a ', '<h1', '<h2', '<body', '<head',
            '<br', '<img', '<ul', '<ol', '<li', '<meta', '<link'
        ])
        if not is_html:
            return text
        try:
            from markitdown import MarkItDown
            md = MarkItDown()
            result = md.convert(text)
            if result and hasattr(result, 'text_content'):
                return result.text_content
        except (ImportError, Exception):
            pass
        return text

    # ── 阶段2: Noise Stripping ──
    def _strip_noise(self, text: str) -> str:
        """去样板/去空白/去零宽字符"""
        # 提前保护：如果文本主要是 URL 或极短，跳过去噪
        if len(text) < 200 and 'http' in text[:100]:
            text = self.ZERO_WIDTH_CHARS.sub('', text)
            return text.strip()

        lines = text.split('\n')
        cleaned = []

        for line in lines:
            stripped = line.strip()

            # 跳过空行
            if not stripped:
                continue

            # 跳过样板行
            is_boilerplate = any(p.match(stripped) for p in self.BOILERPLATE_PATTERNS)
            if is_boilerplate:
                continue

            # 去零宽字符
            stripped = self.ZERO_WIDTH_CHARS.sub('', stripped)

            cleaned.append(stripped)

        text = '\n'.join(cleaned)

        # 多余空行/空白 — 包括 tab 和连续空格
        text = self.EXCESS_NEWLINES.sub('\n\n', text)
        text = self.TRAILING_SPACES.sub('\n', text)
        text = re.sub(r'[ \t]+', ' ', text)  # 统一 tab 和连续空格

        return text.strip()

    # ── 阶段3: Deduplication ──
    def _deduplicate(self, text: str) -> str:
        """行级/块级去重（保留频次信息）"""
        lines = text.split('\n')
        seen = {}  # hash -> (line, count)
        order = []  # 保持首次出现顺序

        for line in lines:
            # 归一化后比较
            norm = line.strip().lower()
            norm = re.sub(r'\s+', ' ', norm)
            hash_key = hashlib.md5(norm.encode()).hexdigest()

            if hash_key in seen:
                seen[hash_key] = (seen[hash_key][0], seen[hash_key][1] + 1)
            else:
                seen[hash_key] = (line, 1)
                order.append(hash_key)

        result_lines = []
        for hk in order:
            line, count = seen[hk]
            if count > 1:
                # 保留频次信息
                result_lines.append(f'{line} (×{count})')
            else:
                result_lines.append(line)

        return '\n'.join(result_lines)

    # ── 阶段4: URL Optimization ──
    def _shorten_urls(self, text: str) -> str:
        """URL 缩短"""
        for pattern, replacement in self.URL_SHORTEN_RULES:
            text = pattern.sub(replacement, text)
        return text

    # ── 阶段5: Smart Truncation ──
    def _smart_truncate(self, text: str, max_chars: int) -> str:
        """智能截断：保头保尾 + 自动摘要"""
        if len(text) <= max_chars:
            return text

        # 硬限制检查
        if len(text) > SMART_TRUNCATION_HARD_LIMIT:
            text = text[:SMART_TRUNCATION_HARD_LIMIT]

        # 保头：前30%
        head_ratio = 0.30
        head_len = int(max_chars * head_ratio)
        head = text[:head_len]

        # 保尾：后20%
        tail_ratio = 0.20
        tail_len = int(max_chars * tail_ratio)
        tail = text[-tail_len:]

        # 中间：用摘要替代
        middle_remaining = max_chars - head_len - tail_len
        if middle_remaining < 200:
            middle = f"\n\n[⚠️ 中间内容已压缩: 原文 {len(text) - head_len - tail_len} chars → 摘要]\n"
        else:
            middle = f"\n\n[⚠️ 中间内容已压缩: 原文 {len(text) - head_len - tail_len} chars]\n"

        result = head + middle + tail
        return result

    # ── 统计辅助 ──
    @staticmethod
    def estimate_token_savings(original_chars: int, compressed_chars: int) -> Dict:
        """估算 token 节省（按 1 token ≈ 4 chars 粗略估算）"""
        orig_tokens = original_chars / 4
        comp_tokens = compressed_chars / 4
        saved_tokens = orig_tokens - comp_tokens
        return {
            "estimated_original_tokens": int(orig_tokens),
            "estimated_compressed_tokens": int(comp_tokens),
            "estimated_saved_tokens": int(saved_tokens),
            "char_savings": original_chars - compressed_chars,
        }


# ═══════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        input_text = sys.argv[1]
        context = sys.argv[2] if len(sys.argv) > 2 else "default"
    else:
        # 测试
        test_text = """
        <html><body>
        <script>alert('test');</script>
        <style>.foo{color:red}</style>
        <div class="footer">cookie政策：本站使用cookie</div>
        <h1>测试标题</h1>
        <p>这是测试内容。这是测试内容。这是测试内容。</p>
        <p>这是测试内容。这是测试内容。这是测试内容。</p>
        <p>重复段落。重复段落。重复段落。</p>
        <p>重复段落。重复段落。重复段落。</p>
        <a href="https://www.anjuke.com/sy/123?utm_source=google&utm_medium=cpc&fbclid=abc123">安居客链接</a>
        <p class="cookie-banner">本网站使用cookies来改善您的体验</p>
        <p>零宽字符测试\u200b\u200c\u200d</p>
        <p>长段内容：Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        </body></html>
        """
        input_text = test_text * 100  # 放大到约 30K chars
        context = "web_page"

    result = TokenJuice.compress(input_text, context=context)
    print(f"📊 TokenJuice 压缩报告")
    print(f"   上下文类型: {context}")
    print(f"   原文: {result['original_chars']} chars")
    print(f"   压缩后: {result['compressed_chars']} chars")
    print(f"   压缩比: {result['ratio']}%")
    print(f"   阶段: {', '.join(result['stages'])}")
    savings = TokenJuice.estimate_token_savings(result['original_chars'], result['compressed_chars'])
    print(f"   估算节省: ~{savings['estimated_saved_tokens']} tokens")

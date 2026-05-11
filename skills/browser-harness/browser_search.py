#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器搜索引擎 — OpenClaw Browser 真实渲染
=========================================
当 API 搜索/requests 爬取失败时，回退到 Chromium headless 真实渲染搜索。

使用 OpenClaw 的 browser 工具（CDP + Playwright）进行：
- 轻量搜索: 打开搜索引擎 → snapshot 取结果
- 深度搜索: 输入查询 → 点击 → 滚动 → 提取
- 页面抓取: 渲染 JS 后提取内容

"""

import json
import logging
import time
import urllib.parse
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# ── 搜索配置 ──────────────────────────────────────────
SEARCH_ENGINES = {
    "google": {
        "url": "https://www.google.com/search?q={query}&num={count}",
        "result_selector": "div.g",  # Google result block
        "link_selector": "a[href^='http']",
        "title_selector": "h3",
        "snippet_selector": "div.VwiC3b, span.aCOpRe",
    },
    "bing": {
        "url": "https://www.bing.com/search?q={query}&count={count}",
        "result_selector": "li.b_algo",
        "link_selector": "h2 a",
        "title_selector": "h2",
        "snippet_selector": ".b_caption p, .b_lineclamp2",
    },
    "duckduckgo": {
        "url": "https://lite.duckduckgo.com/lite/?q={query}",
        "result_selector": "tr.result",
        "link_selector": "a.result-link",
        "title_selector": "a.result-link",
        "snippet_selector": "td.result-snippet",
    },
}

# ── 数据结构 ──────────────────────────────────────────

@dataclass
class SearchRequest:
    query: str
    engine: str = "google"
    count: int = 10
    timeout_ms: int = 30000

@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str = ""

@dataclass
class SearchResponse:
    success: bool
    results: List[SearchResult]
    source: str = "browser"
    engine: str = ""
    duration_ms: float = 0
    error: str = ""

# ── 浏览器搜索引擎核心 ──────────────────────────────────

class BrowserHarnessSearch:
    """基于 OpenClaw Browser Plugin 的真实浏览器搜索引擎"""

    def __init__(self):
        self._browser_available = False
        self._check_browser()

    def _check_browser(self):
        """检查 browser 工具是否可用"""
        try:
            # 尝试通过 OpenClaw 浏览器控制 API 检活
            import subprocess
            result = subprocess.run(
                ["openclaw", "browser", "status", "--json"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                status = json.loads(result.stdout)
                self._browser_available = True
                logger.info(f"浏览器就绪: {status}")
            else:
                logger.warning(f"浏览器未就绪: {result.stderr}")
        except Exception as e:
            logger.warning(f"浏览器检查失败: {e}")

    @property
    def available(self) -> bool:
        return self._browser_available

    def search(self, query: str, engine: str = "google",
               count: int = 10) -> SearchResponse:
        """轻量浏览器搜索 — 直开搜索引擎取 snapshot"""
        start = time.time()
        engine_config = SEARCH_ENGINES.get(engine, SEARCH_ENGINES["google"])
        url = engine_config["url"].format(
            query=urllib.parse.quote(query),
            count=min(count, 20)
        )

        try:
            results = self._browser_search(url, query, engine, count)
            dur = (time.time() - start) * 1000
            return SearchResponse(
                success=True,
                results=results,
                engine=engine,
                duration_ms=dur
            )
        except Exception as e:
            dur = (time.time() - start) * 1000
            logger.error(f"浏览器搜索失败: {e}")
            return SearchResponse(
                success=False,
                results=[],
                engine=engine,
                duration_ms=dur,
                error=str(e)
            )

    def search_deep(self, query: str, engine: str = "google",
                    count: int = 10) -> SearchResponse:
        """深度浏览器搜索 — 输入查询框 + 点击提交 + 滚动加载"""
        start = time.time()
        try:
            results = self._browser_search_deep(query, engine, count)
            dur = (time.time() - start) * 1000
            return SearchResponse(
                success=True,
                results=results,
                engine=engine,
                duration_ms=dur,
                source="browser_deep"
            )
        except Exception as e:
            dur = (time.time() - start) * 1000
            logger.error(f"深度浏览器搜索失败: {e}")
            return SearchResponse(
                success=False,
                results=[],
                engine=engine,
                duration_ms=dur,
                error=str(e)
            )

    def fetch_page(self, url: str) -> Optional[str]:
        """用浏览器渲染 JS 页面并返回文本内容"""
        try:
            import subprocess
            result = subprocess.run(
                ["openclaw", "browser", "navigate", url, "--json"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                return None

            # 等待页面加载后取 snapshot
            time.sleep(2)
            snap = subprocess.run(
                ["openclaw", "browser", "snapshot", "--json"],
                capture_output=True, text=True, timeout=15
            )
            if snap.returncode == 0:
                data = json.loads(snap.stdout)
                # 提取文本内容
                if isinstance(data, dict) and "content" in data:
                    return data["content"]
                return str(data)
            return None
        except Exception as e:
            logger.error(f"页面抓取失败: {e}")
            return None

    def _browser_search(self, url: str, query: str,
                        engine: str, count: int) -> List[SearchResult]:
        """通过 OpenClaw browser CLI 进行搜索"""
        import subprocess
        # 打开搜索引擎
        result = subprocess.run(
            ["openclaw", "browser", "navigate", url, "--json"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            raise RuntimeError(f"导航失败: {result.stderr}")

        # 等待渲染
        time.sleep(2.5)

        # 取 snapshot
        snap = subprocess.run(
            ["openclaw", "browser", "snapshot", "--urls", "--json"],
            capture_output=True, text=True, timeout=15
        )
        if snap.returncode != 0:
            raise RuntimeError(f"snapshot 失败: {snap.stderr}")

        data = json.loads(snap.stdout)
        return self._extract_results(data, count)

    def _browser_search_deep(self, query: str, engine: str,
                             count: int) -> List[SearchResult]:
        """通过输入框 + 提交按钮做深度搜索"""
        import subprocess
        engine_urls = {
            "google": "https://www.google.com",
            "bing": "https://www.bing.com",
            "duckduckgo": "https://duckduckgo.com",
        }
        url = engine_urls.get(engine, engine_urls["google"])

        # 打开搜索引擎首页
        subprocess.run(
            ["openclaw", "browser", "navigate", url, "--json"],
            capture_output=True, text=True, timeout=30
        )
        time.sleep(2)

        # 获取 snapshot 找输入框 ref
        snap = subprocess.run(
            ["openclaw", "browser", "snapshot", "--interactive", "--json"],
            capture_output=True, text=True, timeout=15
        )
        if snap.returncode != 0:
            raise RuntimeError(f"snapshot 失败: {snap.stderr}")

        snap_data = json.loads(snap.stdout)
        search_box_ref = self._find_search_box(snap_data)
        if not search_box_ref:
            # 回退到直接 URL 搜索
            return self._browser_search(
                SEARCH_ENGINES[engine]["url"].format(
                    query=urllib.parse.quote(query),
                    count=count
                ), query, engine, count
            )

        # 输入查询
        subprocess.run(
            ["openclaw", "browser", "act", "type", search_box_ref, query],
            capture_output=True, text=True, timeout=10
        )
        time.sleep(0.5)

        # 按 Enter
        subprocess.run(
            ["openclaw", "browser", "act", "press", "Enter"],
            capture_output=True, text=True, timeout=10
        )
        time.sleep(3)

        # 取结果 snapshot
        result_snap = subprocess.run(
            ["openclaw", "browser", "snapshot", "--urls", "--json"],
            capture_output=True, text=True, timeout=15
        )
        if result_snap.returncode != 0:
            raise RuntimeError(f"结果 snapshot 失败: {result_snap.stderr}")

        data = json.loads(result_snap.stdout)
        return self._extract_results(data, count)

    def _find_search_box(self, snapshot_data: dict) -> Optional[str]:
        """从 snapshot 中找搜索输入框的 ref"""
        # AI snapshot: 搜索 textbox/combobox input
        if isinstance(snapshot_data, dict):
            content = snapshot_data.get("content", "")
            refs = snapshot_data.get("refs", [])
            # 优先用 refs 列表
            for ref in refs:
                name = (ref.get("name", "") or "").lower()
                role = (ref.get("role", "") or "").lower()
                desc = (ref.get("description", "") or "").lower()
                if "search" in name or "search" in role or "search" in desc:
                    return str(ref.get("ref"))
                if "query" in name or "q" == name:
                    return str(ref.get("ref"))
            # 尝试从文本中找 e refs
            if content:
                import re
                # 找 search box text input
                matches = re.findall(
                    r'\[ref=e(\d+)\].*?(?:search|Search|搜索)', content
                )
                if matches:
                    return f"e{matches[0]}"
                # 找 role=searchbox
                matches = re.findall(
                    r'\[ref=e(\d+)\].*?searchbox', content, re.I
                )
                if matches:
                    return f"e{matches[0]}"
        return None

    def _extract_results(self, snapshot_data: Any,
                         max_results: int) -> List[SearchResult]:
        """从 snapshot 输出中提取搜索结果"""

        def extract_url(link_text: str) -> str:
            """从文本中提取 URL"""
            import re
            urls = re.findall(
                r'https?://[^\s\'\"<>{}|\\^`\[\]]+',
                link_text
            )
            return urls[0] if urls else ""

        results = []

        # 方式1: snapshot 包含 urls 字段
        if isinstance(snapshot_data, dict):
            urls = snapshot_data.get("urls", [])
            for u in urls:
                url = u.get("url", "")
                title = u.get("title", "") or u.get("text", "")
                if url and title and len(results) < max_results:
                    results.append(SearchResult(
                        title=title.strip(),
                        url=url,
                        snippet=u.get("description", "")
                    ))

            # 方式2: 从文本内容解析
            if not results:
                content = snapshot_data.get("content", "")
                if content:
                    import re
                    # 解析 AI snapshot 格式
                    lines = content.split("\n")
                    i = 0
                    while i < len(lines) and len(results) < max_results:
                        line = lines[i]
                        # 找链接行
                        url_match = re.search(
                            r'https?://[\w./?=&%-]+', line
                        )
                        if url_match and "google.com" not in url_match.group():
                            url = url_match.group()
                            title = re.sub(
                                r'\[ref=\w+\]\s*', '', line
                            ).strip()
                            title = re.sub(r'https?://\S+', '', title).strip()
                            snippet = ""
                            if i + 1 < len(lines):
                                snippet = lines[i + 1].strip()
                                snippet = re.sub(r'\[ref=\w+\]\s*', '', snippet)
                            if title:
                                results.append(SearchResult(
                                    title=title[:100],
                                    url=url,
                                    snippet=snippet[:300]
                                ))
                        i += 1

        return results[:max_results]

    def close(self):
        """清理浏览器"""
        import subprocess
        try:
            subprocess.run(
                ["openclaw", "browser", "stop"],
                capture_output=True, timeout=10
            )
        except Exception:
            pass


# ── 便捷函数 ──────────────────────────────────────────

_shared_instance: Optional[BrowserHarnessSearch] = None


def get_browser_harness() -> BrowserHarnessSearch:
    """获取浏览器搜索引擎单例"""
    global _shared_instance
    if _shared_instance is None:
        _shared_instance = BrowserHarnessSearch()
    return _shared_instance


def search(query: str, engine: str = "google",
           count: int = 10, mode: str = "light") -> SearchResponse:
    """便捷搜索接口

    Args:
        query: 搜索关键词
        engine: 搜索引擎 (google/bing/duckduckgo)
        count: 结果数
        mode: 模式 (light=轻量 / deep=深度输入框)
    """
    harness = get_browser_harness()
    if mode == "deep":
        return harness.search_deep(query, engine, count)
    return harness.search(query, engine, count)


def fetch_page(url: str) -> Optional[str]:
    """浏览器渲染抓取页面"""
    harness = get_browser_harness()
    return harness.fetch_page(url)


# ── 测试 ──────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("🧪 浏览器搜索引擎测试")
    print("=" * 50)

    # 测试轻量搜索
    print("📦 测试: 轻量搜索 Google")
    r = search("test search", engine="google")
    print(f"  成功: {r.success}, 结果: {len(r.results)}, 耗时: {r.duration_ms:.0f}ms")
    for i, res in enumerate(r.results[:3]):
        print(f"  {i+1}. {res.title}")
        print(f"     {res.url}")

    print("=" * 50)
    print("✅ 测试完成")

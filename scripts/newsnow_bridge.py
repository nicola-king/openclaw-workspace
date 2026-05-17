#!/usr/bin/env python3
"""
NewsNow 新闻桥 — 太一情报晚报新闻源

直接调用 NewsNow API (bypass MCP server)
GET /api/s?id={source_id}

支持 50+ 新闻源，结构化数据直接返回
"""

import json, requests, os, sys
from typing import List, Dict, Optional
from datetime import datetime

BASE_URL = os.environ.get("NEWSNOW_BASE_URL", "https://newsnow.busiyi.world")
TIMEOUT = 15

# ── 情报晚报默认新闻源 ──

EVENING_BRIEF_SOURCES = [
    {"id": "wallstreetcn-quick", "label": "华尔街见闻·快讯", "category": "财经"},
    {"id": "cls-telegraph", "label": "财联社·电报", "category": "财经"},
    {"id": "jin10", "label": "金十数据", "category": "财经"},
    {"id": "36kr-quick", "label": "36氪·快讯", "category": "科技创投"},
    {"id": "ithome", "label": "IT之家", "category": "科技"},
    {"id": "sspai", "label": "少数派", "category": "科技"},
    {"id": "github-trending-today", "label": "GitHub Trending", "category": "开源"},
    {"id": "hackernews", "label": "Hacker News", "category": "科技国际"},
    {"id": "zhihu", "label": "知乎·热门", "category": "综合"},
    {"id": "baidu", "label": "百度热搜", "category": "社会"},
    {"id": "thepaper", "label": "澎湃新闻·热榜", "category": "时政"},
    {"id": "zaobao", "label": "联合早报", "category": "国际"},
    {"id": "producthunt", "label": "Product Hunt", "category": "产品"},
]

# ── 晨间简报源（更精简） ──

MORNING_BRIEF_SOURCES = [
    {"id": "wallstreetcn-quick", "label": "华尔街见闻", "category": "财经"},
    {"id": "jin10", "label": "金十数据", "category": "财经"},
    {"id": "36kr-quick", "label": "36氪", "category": "科技"},
    {"id": "hackernews", "label": "HN", "category": "国际科技"},
    {"id": "baidu", "label": "百度热搜", "category": "社会"},
]


class NewsNow:
    """NewsNow 新闻获取器（直接 HTTP API）"""

    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
        })

    def get_news(self, source_id: str, count: int = 10) -> List[Dict]:
        """
        获取指定源的新闻

        Returns:
            [{ "title": str, "url": str, "source": str }]
        """
        url = f"{BASE_URL}/api/s?id={source_id}"
        try:
            resp = self._session.get(url, timeout=TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
            items = data.get("items", [])
            return [
                {"title": item.get("title", ""),
                 "url": item.get("url", ""),
                 "source": source_id}
                for item in items[:count]
                if item.get("title")
            ]
        except Exception as e:
            print(f"  ⚠️ {source_id}: {e}", file=sys.stderr)
            return []

    def get_brief(self, sources: Optional[List[Dict]] = None) -> Dict[str, List[Dict]]:
        """
        获取多源新闻，按分类组织

        Returns:
            { "财经": [{title, url, source, label}], "科技": [...], ... }
        """
        if sources is None:
            sources = EVENING_BRIEF_SOURCES

        result = {}
        for src in sources:
            news = self.get_news(src["id"], count=8)
            if news:
                cat = src["category"]
                if cat not in result:
                    result[cat] = []
                for item in news:
                    item["_label"] = src["label"]
                result[cat].extend(news)

        return result

    def format_brief_for_llm(self, brief: Dict[str, List[Dict]]) -> str:
        """将简报格式化为 LLM 可处理的文本"""
        lines = [f"# NewsNow 简报 ({datetime.now().strftime('%m-%d %H:%M')})", ""]
        total = 0
        for cat, items in brief.items():
            lines.append(f"## {cat} ({len(items)} 条)")
            for item in items[:5]:
                title = item.get("title", "").strip()
                if title:
                    lines.append(f"- [{item.get('_label', '')}] {title}")
            if len(items) > 5:
                lines.append(f"  ... 还有 {len(items)-5} 条")
            lines.append("")
            total += len(items)
        if total == 0:
            return "⚠️ 未获取到新闻数据"
        lines.insert(1, f"> 共 {total} 条，来自 {len(brief)} 个分类")
        return "\n".join(lines)

    def to_markdown(self, brief: Dict[str, List[Dict]]) -> str:
        """转为 Markdown 格式"""
        return self.format_brief_for_llm(brief)


# ── 可用新闻源列表（全部 50+） ──

def list_sources() -> List[Dict]:
    """返回所有可用新闻源的分类列表"""
    return [
        {"id": "finance", "label": "财经 · 6 源", "items": [
            ("wallstreetcn-quick", "华尔街见闻·快讯"),
            ("cls-telegraph", "财联社·电报"),
            ("cls-depth", "财联社·深度"),
            ("cls-hot", "财联社·热门"),
            ("jin10", "金十数据"),
            ("xueqiu-hotstock", "雪球·热门股票"),
            ("gelonghui", "格隆汇·事件"),
            ("fastbull-express", "法布财经·快讯"),
        ]},
        {"id": "tech", "label": "科技 · 8 源", "items": [
            ("36kr-quick", "36氪·快讯"),
            ("36kr-renqi", "36氪·人气榜"),
            ("ithome", "IT之家"),
            ("sspai", "少数派"),
            ("solidot", "Solidot"),
            ("juejin", "稀土掘金"),
            ("freebuf", "Freebuf·网络安全"),
            ("pcbeta-windows11", "远景论坛·Win11"),
        ]},
        {"id": "china", "label": "国内 · 12 源", "items": [
            ("zhihu", "知乎·热门"),
            ("weibo", "微博·实时热搜"),
            ("baidu", "百度热搜"),
            ("toutiao", "今日头条"),
            ("thepaper", "澎湃新闻·热榜"),
            ("ifeng", "凤凰网·热点资讯"),
            ("bilibili-hot-search", "B站·热搜"),
            ("douyin", "抖音"),
            ("hupu", "虎扑·主干道热帖"),
            ("tieba", "百度贴吧·热议"),
            ("douban", "豆瓣·热门电影"),
            ("nowcoder", "牛客"),
        ]},
        {"id": "world", "label": "国际 · 6 源", "items": [
            ("zaobao", "联合早报"),
            ("sputniknewscn", "卫星通讯社"),
            ("cankaoxiaoxi", "参考消息"),
            ("kaopu", "靠谱新闻"),
            ("hackernews", "Hacker News"),
            ("producthunt", "Product Hunt"),
        ]},
        {"id": "oss", "label": "开源 · 3 源", "items": [
            ("github-trending-today", "GitHub Trending Today"),
            ("steam", "Steam·在线人数"),
            ("chongbuluo-latest", "虫部落·最新"),
        ]},
        {"id": "special", "label": "专项 · 5 源", "items": [
            ("tencent-hot", "腾讯新闻·综合早报"),
            ("qqvideo-tv-hotsearch", "腾讯视频·电视剧热搜"),
            ("iqiyi-hot-ranklist", "爱奇艺·热播榜"),
            ("coolapk", "酷安·今日最热"),
            ("v2ex-share", "V2EX·最新分享"),
        ]},
    ]


# ── CLI 入口 ──

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="NewsNow 新闻桥")
    parser.add_argument("action", nargs="?", default="brief",
                        choices=["brief", "source", "sources", "morning"],
                        help="操作")
    parser.add_argument("--id", default="hackernews", help="新闻源 ID")
    parser.add_argument("--count", type=int, default=5, help="条数")

    args = parser.parse_args()
    nn = NewsNow()

    if args.action == "sources":
        for group in list_sources():
            print(f"\n📂 {group['label']}:")
            for sid, label in group["items"]:
                print(f"  {sid:35s} {label}")

    elif args.action == "source":
        print(f"📰 {args.id} 最新 {args.count} 条:")
        news = nn.get_news(args.id, count=args.count)
        for i, item in enumerate(news, 1):
            print(f"  {i}. {item['title'][:100]}")

    elif args.action == "morning":
        print("🌅 晨间新闻简报:\n")
        brief = nn.get_brief(MORNING_BRIEF_SOURCES)
        print(nn.format_brief_for_llm(brief))

    else:  # brief
        print("📰 情报晚报备料:\n")
        brief = nn.get_brief()
        print(nn.format_brief_for_llm(brief))

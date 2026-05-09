#!/usr/bin/env python3
"""
买家情报 RSS 馈送模块 — 三轨接入之一

用法:
  python3 rss_feed.py                        # 输出到 stdout
  python3 rss_feed.py --output feed.xml       # 写文件
  python3 rss_feed.py --mode daily --output feed.xml  # 日报模式
"""
import json, os, sys
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import BuyerIntel

SITE = "https://taiyi.trade/buyer-intel"
FEED_TITLE = "太一跨境贸易 · 买家情报"
FEED_DESC = "太一精选高价值买家线索与采购机会 — 钢结构集成房 / 变压器 / 储能 / 摩配"


class RSSFeed:
    """RSS 2.0 馈送生成器"""

    def __init__(self, mode="selected", limit=20):
        self.bi = BuyerIntel()
        self.mode = mode
        self.limit = limit

    def generate(self, output_path=None):
        """生成 RSS XML"""
        data = self.bi.query(mode=self.mode, tier="pro")
        items = data.get("items", [])

        rss = Element("rss", version="2.0",
            attrib={"xmlns:atom": "http://www.w3.org/2005/Atom"})
        channel = SubElement(rss, "channel")

        # 频道元信息
        SubElement(channel, "title").text = FEED_TITLE
        SubElement(channel, "link").text = f"{SITE}/rss"
        SubElement(channel, "description").text = FEED_DESC
        SubElement(channel, "language").text = "zh-cn"
        SubElement(channel, "pubDate").text = self._now()

        # atom:self link
        atom = SubElement(channel, "{http://www.w3.org/2005/Atom}link",
            href=f"{SITE}/rss",
            rel="self",
            type="application/rss+xml")

        for item in items[:self.limit]:
            entry = SubElement(channel, "item")

            title = item.get("project_name") or item.get("title", "买家线索")
            SubElement(entry, "title").text = title

            brief = item.get("project_brief") or item.get("summary", "")
            SubElement(entry, "description").text = brief

            url = item.get("url") or item.get("source", "")
            SubElement(entry, "link").text = url

            guid = SubElement(entry, "guid", isPermaLink="false")
            guid.text = item.get("id", title)

            updated = item.get("last_updated") or item.get("date", "")
            SubElement(entry, "pubDate").text = self._date_rss(updated)

            if item.get("country"):
                SubElement(entry, "category").text = item["country"]

        # 美化输出
        rough = tostring(rss, encoding="unicode")
        dom = minidom.parseString(rough.encode("utf-8"))
        xml = dom.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(xml)
            print(f"✅ RSS 已写入: {output_path}", file=sys.stderr)
        else:
            print(xml)

    def _now(self):
        return datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0800")

    def _date_rss(self, date_str):
        if not date_str:
            return self._now()
        try:
            dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
            return dt.strftime("%a, %d %b %Y %H:%M:%S +0800")
        except:
            return self._now()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="买家情报 RSS 生成器")
    parser.add_argument("--mode", choices=["selected", "daily", "all"], default="selected")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--output", "-o", help="输出文件路径")
    args = parser.parse_args()

    feed = RSSFeed(mode=args.mode, limit=args.limit)
    feed.generate(output_path=args.output)


if __name__ == "__main__":
    main()

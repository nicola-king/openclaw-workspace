#!/usr/bin/env python3
"""
买家情报引擎 v2 — 三路由架构
借鉴 AI HOT 精选/日报/全量 模式

路由层次:
  selected (精选) — 活跃高优项目/线索，默认
  daily    (日报) — 聚合报告，按国家/品类打包
  all      (全量) — 全部线索，含冷数据
"""
import json, os, re
from datetime import datetime, timedelta

DATA_DIR = os.path.dirname(__file__) + "/data"
BUYER_FILE = f"{DATA_DIR}/buyers.json"

class BuyerIntel:
    TIERS = {
        "free": {"name": "免费", "visible_fields": ["project_name","country","sectors","status"],
                 "max_results": 3, "price_monthly": 0},
        "free_trial": {"name": "试用", "visible_fields": "__all__",
                       "max_results": 10, "price_monthly": 0},
        "basic": {"name": "基础版", "visible_fields": ["project_name","country","sectors","status",
                    "budget_usd","procurement_needs","buyer_type"],
                  "max_results": 20, "price_monthly": 299},
        "pro": {"name": "专业版", "visible_fields": "__all__", "max_results": 999, "price_monthly": 999},
    }

    def __init__(self):
        self.records = self._load()

    def _load(self):
        path = BUYER_FILE
        if not os.path.exists(path): return []
        with open(path) as f: return json.load(f)

    # ═══════════════════════════════════════════
    # 三层路由 (AI HOT 模式)
    # ═══════════════════════════════════════════

    def query(self, mode="selected", **kwargs):
        """
        统一查询入口 — 按 mode 自动路由到三层之一

        mode 说明:
          selected — 精选（活跃高优，默认）
          daily    — 日报（按国家/品类打包的聚合报告）
          all      — 全量（全部线索，含冷数据）
        """
        mode = mode or "selected"
        if mode == "selected":
            return self._selected(**kwargs)
        elif mode == "daily":
            return self._daily(**kwargs)
        elif mode == "all":
            return self._all(**kwargs)
        else:
            return {"status": "error", "error": f"无效 mode: {mode}，可选: selected / daily / all"}

    def _selected(self, q="", country=None, sector=None, days=7, tier="pro"):
        """
        精选层 — 默认路由
        返回活跃高优项目/线索，按更新时间倒序
        """
        r = self._search(q=q, country=country, sector=sector)
        # 精选 = 最近 days 天内活跃 + 已验证
        cutoff = datetime.now() - timedelta(days=days)
        hot = [x for x in r if self._is_hot(x, cutoff)]
        if not hot:
            # 降级：没有精选时，返回最近可用的
            hot = sorted(r, key=lambda x: self._updated_ts(x), reverse=True)[:5]
        return self._paginate(hot, tier, label="精选")

    def _daily(self, country=None, sector=None, tier="pro"):
        """
        日报层 — 聚合报告
        按国家/品类打包，含简要统计
        """
        r = self.records
        if country:
            r = [x for x in r if x.get("country","").lower() == country.lower()]
        if sector:
            r = [x for x in r if any(sector.lower() in s.lower() for s in x.get("sectors",[]))]
        if not r:
            return {"status": "error", "error": f"暂无{country or sector}的日报数据", "suggestion": "试试其他国家或品类"}

        # 按国家+品类分组
        groups = {}
        for x in r:
            c = x.get("country","未知")
            secs = x.get("sectors",["其他"])[0] if x.get("sectors") else "其他"
            key = f"{c} / {secs}"
            if key not in groups: groups[key] = []
            groups[key].append(x)

        report = {
            "mode": "daily",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total": len(r),
            "groups": {k: self._mask(v, tier) for k, v in groups.items()},
        }
        return report

    def _all(self, q="", country=None, sector=None, days=None, tier="pro"):
        """
        全量层 — 全部线索，含冷数据
        无时间默认，给所有
        """
        r = self._search(q=q, country=country, sector=sector)
        # 按日期排序
        r.sort(key=lambda x: self._updated_ts(x), reverse=True)
        return self._paginate(r, tier, label="全量")

    # ═══════════════════════════════════════════
    # 内部工具
    # ═══════════════════════════════════════════

    def _search(self, q="", country=None, sector=None):
        r = self.records
        if q:
            ql = q.lower()
            r = [x for x in r if ql in json.dumps(x, ensure_ascii=False).lower()]
        if country:
            r = [x for x in r if x.get("country","").lower() == country.lower()]
        if sector:
            r = [x for x in r if any(sector.lower() in s.lower() for s in x.get("sectors",[]))]
        return r

    def _is_hot(self, item, cutoff):
        """判断是否为精选（活跃高优）"""
        # 已验证+无负面标记+更新在窗口内
        verified = item.get("verified", {})
        vcount = sum(1 for v in verified.values() if v)
        if vcount < 2:
            return False
        updated = self._updated_ts(item)
        return updated >= cutoff

    def _updated_ts(self, item):
        """获取更新时间戳"""
        raw = item.get("updated_at") or item.get("created_at", "2000-01-01")
        try:
            return datetime.strptime(raw[:10], "%Y-%m-%d")
        except:
            return datetime(2000, 1, 1)

    def _paginate(self, items, tier, label="精选", max_items=50):
        """加权限层分页"""
        tc = self.TIERS.get(tier, self.TIERS["pro"])
        out = []
        for x in items[:min(tc["max_results"], max_items)]:
            if tc["visible_fields"] == "__all__":
                out.append(x)
            else:
                out.append({k: x.get(k) for k in tc["visible_fields"] if k in x})
        return {
            "mode": label,
            "count": len(out),
            "items": out,
        }

    def _mask(self, items, tier):
        """按权限屏蔽字段"""
        tc = self.TIERS.get(tier, self.TIERS["pro"])
        if tc["visible_fields"] == "__all__":
            return items
        return [{k: x.get(k) for k in tc["visible_fields"] if k in x} for x in items]

    # ═══════════════════════════════════════════
    # 兼容旧接口
    # ═══════════════════════════════════════════

    def search(self, q="", filters=None, tier="pro"):
        """旧接口 — 映射到 selected"""
        f = filters or {}
        return self._selected(
            q=q,
            country=f.get("country"),
            sector=f.get("sector"),
            days=f.get("days", 7),
            tier=tier
        )

    def projects(self, country=None, tier="pro"):
        return self.query("selected", country=country, tier=tier)

    def leads(self, country=None, tier="pro"):
        return self._all(country=country, tier=tier)

    def daily_report(self, country=None, sector=None, tier="pro"):
        return self._daily(country=country, sector=sector, tier=tier)


    # ═══════════════════════════════════════════
    # 健康检查
    # ═══════════════════════════════════════════

    def health_check(self):
        return {
            "module": "buyer-intel",
            "version": "2.0",
            "records": len(self.records),
            "mode": "三层路由: selected/daily/all",
            "tiers": list(self.TIERS.keys()),
        }


if __name__ == "__main__":
    bi = BuyerIntel()
    print("=== Health ===")
    print(json.dumps(bi.health_check(), indent=2, ensure_ascii=False))
    print("=== Selected (默认) ===")
    print(json.dumps(bi.query("selected"), indent=2, ensure_ascii=False)[:300])
    print("=== Daily ===")
    print(json.dumps(bi.query("daily", country=None), indent=2, ensure_ascii=False)[:300])
    print("=== All ===")
    print(json.dumps(bi.query("all"), indent=2, ensure_ascii=False)[:300])

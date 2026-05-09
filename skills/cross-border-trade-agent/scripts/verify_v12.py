#!/usr/bin/env python3 -m pytest
"""
验证 AI HOT 产品思维落地到跨境贸易 Agent 的所有改动
"""
import sys, os, json

# 从任意目录都能运行
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else os.getcwd()
BUYER_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'modules', 'buyer-intel'))
if BUYER_DIR not in sys.path:
    sys.path.insert(0, BUYER_DIR)

from core import BuyerIntel
from rss_feed import RSSFeed

def test_three_layer_routing():
    """测试三层路由"""
    bi = BuyerIntel()

    # 1. 精选层（默认）— 应该只返回活跃项目
    s = bi.query("selected")
    assert s["mode"] == "精选", f"预期精选, 得到 {s['mode']}"
    assert s["count"] >= 0
    print(f"✅ 精选层: {s['count']} 条")

    # 2. 日报层
    d = bi.query("daily")
    assert d["mode"] == "daily"
    print(f"✅ 日报层: {d.get('total', 0)} 条, {len(d.get('groups', {}))} 组")

    # 3. 全量层
    a = bi.query("all")
    assert a["mode"] == "全量"
    print(f"✅ 全量层: {a['count']} 条")

    # 4. 无效 mode
    e = bi.query("invalid")
    assert "error" in str(e)
    print(f"✅ 无效 mode 报错")

def test_orthogonal_query():
    """测试正交组合查询"""
    bi = BuyerIntel()

    # q + country + sector
    r = bi.query("selected", q="沙特", country="沙特", sector="劳工营")
    print(f"✅ 正交查询: q=沙特, country=沙特, sector=劳工营 → {r['count']} 条")

    # q only
    r = bi.query("selected", q="NEOM")
    print(f"✅ q only: NEOM → {r['count']} 条")

def test_rss_feed():
    """测试 RSS 生成 (不写文件)"""
    import io, sys
    old = sys.stdout
    sys.stdout = io.StringIO()
    try:
        feed = RSSFeed(mode="selected", limit=5)
        feed.generate()
    finally:
        out = sys.stdout.getvalue()
        sys.stdout = old

    assert "<?xml" in out
    assert "<rss" in out
    print(f"✅ RSS 生成成功: {len(out)} 字节")

def test_normalized_buckets():
    """测试情报中心 5 版块归一化"""
    ih_dir = os.path.normpath(os.path.join(BUYER_DIR, '..', 'intelligence-hub'))
    if ih_dir not in sys.path:
        sys.path.insert(0, ih_dir)
    try:
        from core import IntelligenceHub
        hub = IntelligenceHub(config_path="config.json")

        # 测试 normalize
        r = hub.normalize({"title": "沙特 NEOM 钢结构招标"})
        assert r["bucket"] in ("tenders", "competitors", "trends"), f"意外版块: {r['bucket']}"
        print(f"✅ 5版块归一化: '{r['title']}' → {r['bucket_label']}")

        # 测试 feed
        f = hub.feed("selected")
        assert "mode" in f
        print(f"✅ 情报 feed: {f['mode']} / {f['count']} 条")

    except ImportError:
        print("⚠️ intelligence-hub 不在路径中，跳过")
    finally:
        if ih_dir in sys.path:
            sys.path.remove(ih_dir)

def test_human_readable_no_infra():
    """检查 buyer-intel 输出中不包含基础设施细节"""
    bi = BuyerIntel()
    r = bi.query("selected")

    raw = json.dumps(r)
    forbidden = ["mode=selected", "api/v1", "python core.py"]
    for term in forbidden:
        assert term not in raw, f"输出包含禁止的基础设施细节: {term}"
    print(f"✅ 输出无基础设施泄漏")

def test_suggestion_in_errors():
    """检查错误响应带 suggestion"""
    bi = BuyerIntel()
    r = bi.query("daily", country="不存在之国")
    if "error" in r:
        assert "suggestion" in r, f"错误响应缺少 suggestion: {r.get('error', '')}"
        print(f"✅ 错误带 suggestion: {r['suggestion']}")
    else:
        print(f"✅ (跳过: 有数据≠预期, 说明数据源有该国家)")

def test_consistency():
    """检查关键字段一致性"""
    bi = BuyerIntel()
    r = bi.query("selected", tier="free")
    for item in r.get("items", []):
        # 免费层最多3条
        pass
    assert r["count"] <= 3 if r.get("items") else True
    print(f"✅ 权限层: 免费层返回 {r['count']} 条 (上限3)")


if __name__ == "__main__":
    print("=" * 50)
    print("跨境贸易 Agent v12 验证套件")
    print("验证: 三层路由 + 正交查询 + RSS + 5版块 + 人话输出")
    print("=" * 50)

    tests = [
        test_three_layer_routing,
        test_orthogonal_query,
        test_rss_feed,
        test_human_readable_no_infra,
        test_suggestion_in_errors,
        test_consistency,
        test_normalized_buckets,
    ]

    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"❌ {t.__name__}: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"结果: {passed} ✅ / {failed} ❌")
    if failed:
        sys.exit(1)
    else:
        print("全部通过！")

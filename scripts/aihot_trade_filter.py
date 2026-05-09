#!/usr/bin/env python3
"""
AI HOT → 跨境贸易 Agent 适配过滤器 v1.0

从 aihot.virxact.com 拉取精选 AI 动态，按模块相关性分类，
生成针对跨境贸易 Agent 18 个模块的适配建议。

用法:
  python3 scripts/aihot_trade_filter.py [--days 7] [--push]
  --push    推送结果到 Telegram（需配置 tell 推送通道）
"""

import json, os, sys, subprocess, argparse
from datetime import datetime, timezone, timedelta

# ── 模块相关性定义 ──────────────────────────────────────────
# 每个模块：关键词 + 权重描述
MODULES = {
    "intelligence-hub": {
        "label": "情报中心",
        "tags": ["market analysis", "trend", "competitor", "industry", "竞品", "市场趋势", "行业报告"],
        "weight": "竞品监控 / 趋势预警 / 选品评分"
    },
    "guike-zhilu": {
        "label": "贵客之路",
        "tags": ["search", "outreach", "lead", "prospect", "搜索", "线索", "开发", "触达"],
        "weight": "搜索→清洗→触达→培育闭环"
    },
    "geo-outbound": {
        "label": "GEO优化",
        "tags": ["content", "seo", "marketing", "social media", "content marketing",
                 "广告", "社媒", "内容营销", "推广", "自动化内容", "生成"],
        "weight": "市场分析 / 潜客名单 / 内容营销"
    },
    "company-enricher": {
        "label": "公司富化",
        "tags": ["enrich", "verify", "company data", "linkedin", "data enrichment",
                 "数据清洗", "验证", "公司信息"],
        "weight": "自动爬虫/搜索/验证"
    },
    "buyer-intel": {
        "label": "买家情报引擎",
        "tags": ["buyer", "procurement", "project", "tender", "采购", "项目",
                 "招标", "买家"],
        "weight": "项目雷达 / 采购机会 / 人脉库"
    },
    "quote-engine": {
        "label": "报价引擎",
        "tags": ["price", "quote", "pricing", "cost", "报价", "定价", "成本计算"],
        "weight": "FOB/CFR/退税"
    },
    "compliance-engine": {
        "label": "合规引擎",
        "tags": ["compliance", "regulation", "saso", "certification", "hs code",
                 "合规", "法规", "认证", "HS编码"],
        "weight": "HS退税 / SASO合规"
    },
    "cultural-adapter": {
        "label": "跨文化适配",
        "tags": ["translation", "localization", "multilingual", "voice", "tts",
                 "翻译", "本地化", "多语言", "语音"],
        "weight": "内容本地化 / 多语言 / SEO"
    },
    "conversion-optimizer": {
        "label": "转化优化",
        "tags": ["conversion", "funnel", "roi", "analytics", "ab test",
                 "转化", "漏斗", "A/B测试", "ROI"],
        "weight": "漏斗分析 / ROI / 渠道对比 / AB测试"
    },
    "transaction-support": {
        "label": "交易支持",
        "tags": ["logistics", "shipment", "payment", "shipping", "supply chain",
                 "物流", "支付", "运输", "供应链"],
        "weight": "物流优化 / 比价 / 销售预测 / 多语言客服"
    },
    "self-evolution": {
        "label": "自我进化",
        "tags": ["agent", "skill", "workflow", "pipeline", "automation", "optimization",
                 "智能体", "技能", "工作流", "自动化", "token优化", "推理"],
        "weight": "技能结晶 / Token效率 / 推理优化"
    },
    "risk-manager": {
        "label": "风险管理",
        "tags": ["risk", "security", "fraud", "compliance", "预警", "风险",
                 "风控", "欺诈", "安全"],
        "weight": "风险识别 / 预警 / 对冲策略"
    },
    "data-integrator": {
        "label": "数据整合",
        "tags": ["data", "api", "integration", "crawl", "scrape",
                 "数据", "API", "集成", "爬虫", "搜索"],
        "weight": "7源整合"
    },
    "report-engine": {
        "label": "报告引擎",
        "tags": ["report", "dashboard", "visualization", "pdf", "报告", "图表", "可视化"],
        "weight": "智能报告生成"
    },
    "product-catalog": {
        "label": "产品目录 RAG",
        "tags": ["rag", "embedding", "search", "semantic", "vector", "RAG", "语义搜索",
                 "向量", "目录"],
        "weight": "TF-IDF / 语义搜索 / 产品匹配"
    },
    "supplier-matcher": {
        "label": "供应商匹配",
        "tags": ["supplier", "vendor", "match", "工厂", "供应商", "匹配"],
        "weight": "9厂评分排名"
    },
    "contract-legal": {
        "label": "合同模板",
        "tags": ["contract", "legal", "arbitration", "合同", "法律", "仲裁"],
        "weight": "中英双语 / SASO / 仲裁"
    },
    "payment-settlement": {
        "label": "支付结算",
        "tags": ["payment", "settlement", "exchange", "crypto", "wallet",
                 "支付", "结算", "汇率", "加密货币"],
        "weight": "支付通道 / 汇率管理"
    },
    "cross-border-core": {
        "label": "核心框架",
        "tags": ["architecture", "framework", "event", "bus", "orchestration",
                 "架构", "框架", "事件总线", "编排"],
        "weight": "路由 / 调度 / Bot协作"
    }
}

# ── 分类映射 ──────────────────────────────────────────────
CATEGORY_MODULE_MAP = {
    "ai-models":   ["self-evolution", "product-catalog", "data-integrator"],
    "ai-products": ["self-evolution", "geo-outbound", "data-integrator", "cultural-adapter",
                    "cross-border-core", "transaction-support"],
    "industry":    ["intelligence-hub", "guike-zhilu", "risk-manager"],
    "paper":       ["self-evolution", "product-catalog", "intelligence-hub"],
    "tip":         ["self-evolution", "report-engine", "conversion-optimizer",
                    "geo-outbound", "cultural-adapter"],
    None:          ["intelligence-hub"]
}

def fetch_aihot(days=7):
    """拉取 AI HOT 精选条目"""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    url = f"https://aihot.virxact.com/api/public/items?mode=selected&since={since}&take=100"

    try:
        result = subprocess.run(
            ["curl", "-s", "-H", f"User-Agent: {ua}", url],
            capture_output=True, text=True, timeout=30
        )
        data = json.loads(result.stdout)
        return data.get("items", [])
    except Exception as e:
        print(f"❌ 拉取 AI HOT 失败: {e}")
        return []

def classify_item(item):
    """对单条 item 做模块相关性分类"""
    title = (item.get("title") or "") + " " + (item.get("summary") or "")
    title_lower = title.lower()
    category = item.get("category")

    hits = {}

    # 1. 按 category 预分配
    pre_match = CATEGORY_MODULE_MAP.get(category, [])
    for mod in pre_match:
        hits.setdefault(mod, 0)
        hits[mod] += 1  # category 匹配 +1

    # 2. 按标签关键词匹配
    for mod_key, mod_info in MODULES.items():
        score = 0
        for tag in mod_info["tags"]:
            if tag.lower() in title_lower:
                score += 2  # 关键词命中 +2
        if score > 0:
            hits[mod_key] = hits.get(mod_key, 0) + score

    # 3. 综合评分
    results = []
    for mod_key, score in hits.items():
        info = MODULES[mod_key]
        results.append({
            "module": mod_key,
            "label": info["label"],
            "weight": info["weight"],
            "score": score,
            "reason": f"类别={category}, 关键词匹配{score}分"
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def generate_report(items):
    """生成过滤报告"""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # 全部模块的聚合计数
    module_hits = {k: {"label": v["label"], "count": 0, "items": []} for k, v in MODULES.items()}

    for item in items:
        classifications = classify_item(item)
        for c in classifications:
            mod = c["module"]
            module_hits[mod]["count"] += 1
            module_hits[mod]["items"].append({
                "title": item.get("title", ""),
                "source": item.get("source", ""),
                "url": item.get("url", ""),
                "category": item.get("category", ""),
                "score": c["score"]
            })

    # 按命中数排序
    sorted_modules = sorted(module_hits.values(), key=lambda x: x["count"], reverse=True)
    active_modules = [m for m in sorted_modules if m["count"] > 0]

    # 构建报告
    lines = []
    lines.append(f"# AI HOT → 跨境贸易 Agent 适配报告")
    lines.append(f"")
    lines.append(f"> 生成时间: {now}")
    lines.append(f"> 数据源: aihot.virxact.com")
    lines.append(f"> 条目数: {len(items)} 条精选")
    lines.append(f"> 命中模块: {len(active_modules)}/{len(MODULES)}")
    lines.append(f"")

    if not active_modules:
        lines.append("本次 AI HOT 数据未命中任何跨境贸易 Agent 模块。")
        return "\n".join(lines)

    lines.append("## 模块适配优先级")
    lines.append(f"")
    for i, m in enumerate(active_modules, 1):
        score_indicator = "🟢" if m["count"] >= 5 else ("🟡" if m["count"] >= 2 else "⚪")
        lines.append(f"### {i}. {score_indicator} {m['label']} — {m['count']} 条相关")
        lines.append(f"")
        for it in m["items"][:5]:  # 最多显示5条
            title = it["title"]
            source = it["source"]
            url = it["url"]
            cat = it["category"] or "其他"
            lines.append(f"- **{title}**")
            lines.append(f"  - 📂 {cat} | 📰 {source} | ⭐ {it['score']}分")
            if url:
                lines.append(f"  - 🔗 {url}")
        if len(m["items"]) > 5:
            lines.append(f"  - ...还有 {len(m['items'])-5} 条")
        lines.append(f"")

    # 快速落地建议
    lines.append("## 高价值落地建议")
    lines.append("")
    top_modules = sorted_modules[:3]
    for m in top_modules:
        if m["count"] >= 3:
            sample = m["items"][0]
            lines.append(f"**{m['label']}** ({m['count']}条相关):")
            lines.append(f"- 参考: {sample['title']}")
            lines.append(f"- 动作: 评估是否直接植入对应模块 README/notes")
            lines.append(f"")

    return "\n".join(lines)

def write_to_memory(report_text):
    """写入今日 memory"""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    mem_path = os.path.expanduser(f"~/.openclaw/workspace/memory/{today}.md")

    section = f"\n\n## [AI HOT 适配] {datetime.now(timezone.utc).strftime('%H:%M UTC')}\n"
    section += "```\n"
    # 只保留前 50 行 + 建议
    lines = report_text.split("\n")
    keep = [l for l in lines if not l.startswith("#") and l.strip()]
    keep_text = "\n".join(keep[:30])
    section += keep_text
    if len(keep) > 30:
        section += "\n...(截断)"
    section += "\n```\n"

    try:
        with open(mem_path, "a") as f:
            f.write(section)
        print(f"✅ 已写入 {mem_path}")
    except Exception as e:
        print(f"⚠️ 写入 memory 失败: {e}")

def main():
    parser = argparse.ArgumentParser(description="AI HOT → 跨境贸易 Agent 适配过滤器")
    parser.add_argument("--days", type=int, default=7, help="拉取最近 N 天数据")
    parser.add_argument("--push", action="store_true", help="推送结果到 Telegram")
    args = parser.parse_args()

    print(f"🔍 拉取 AI HOT 最近 {args.days} 天数据...")
    items = fetch_aihot(args.days)
    print(f"📦 获取 {len(items)} 条精选条目")

    if not items:
        print("❌ 无数据，终止")
        sys.exit(1)

    report = generate_report(items)
    print(report)

    # 写入 memory
    write_to_memory(report)

    # 可选推送
    if args.push:
        try:
            subprocess.run(
                ["openclaw", "tell", "--to", "telegram:7073481596",
                 "--text", report[:3000]],
                timeout=30
            )
            print("📤 已推送 Telegram")
        except Exception as e:
            print(f"⚠️ 推送失败: {e}")

if __name__ == "__main__":
    main()

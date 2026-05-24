# 贸易画像 Agent v1.0

> **版本**: 1.0.0
> **创建**: 2026-05-24（P0 改进#2：用户画像跨模块传播）
> **职责**: 构建/传播/更新用户贸易画像，一次定义全模块复用
> **注册**: skill-registry → `trade-profile.profile`
> **位置**: modules/trade-profile/

---

## 解决的问题

- ❌ 每次查询孤立——每次重复问"做什么产品/目标市场/认证"
- ✅ 一次画像定义 → 所有模块自动感知
- ✅ 画像随业务推进自动更新（触达记录/转化率/反馈）

---

## 数据结构

```python
{
  "profile_id": "PROF-2026-05-24-001",
  "company": {
    "name": "重庆兴旺工具",
    "name_en": "Chongqing Xingwang Tools",
    "website": "",
    "phone": "",
    "email": ""
  },
  "products": [
    {
      "name": "电动工具",
      "hs_code": "8467.29",
      "keywords": ["electric drill", "power tools", "angle grinder"],
      "certifications": ["CE", "ISO9001"]
    }
  ],
  "markets": [
    {
      "country": "澳大利亚",
      "priority": 1,
      "tariff_rate": 5.0,
      "cert_required": ["RCM", "AS/NZS"],
      "status": "active"  # active | researching | paused | closed
    }
  ],
  "capabilities": {
    "moq": 100,
    "lead_time_days": 30,
    "payment_terms": ["T/T", "L/C"],
    "trade_terms": ["FOB", "CIF", "CFR"]
  },
  "history": [
    {"date": "2026-05-20", "action": "search_outreach", "target": "Aus Modular Homes", "result": "sent"},
    {"date": "2026-05-22", "action": "quote_request", "target": "Melbourne Prefab", "result": "pending"}
  ],
  "metrics": {
    "lead_generated": 5,
    "outreach_sent": 12,
    "reply_rate": 0.25,
    "conversion_rate": 0.08,
    "last_updated": "2026-05-24T08:00:00Z"
  },
  "consolidated_insights": {
    "market_opportunity": "澳大利亚模块化建筑市场年增长15%，适合切入",
    "compliance_gaps": ["缺少RCM认证 — 建议1个月内补办"],
    "competitor_threats": ["Karmod 在中东低价竞争，澳洲市场暂未进入"],
    "recommended_actions": ["优先开发AU-001 (Aus Modular Homes)"]
  }
}
```

---

## API

```python
from modules.trade_profile.core import TradeProfile

tp = TradeProfile()

# 创建画像
profile = tp.create(
    company="重庆兴旺工具",
    products=["电动工具", "园林机械"],
    markets=["澳大利亚"]
)

# 获取画像（含跨模块聚合洞察）
profile = tp.get("PROF-2026-05-24-001")

# 更新画像
tp.update("PROF-2026-05-24-001", {"metrics": {"reply_rate": 0.30}})

# 关联模块
profile = tp.consolidate("PROF-2026-05-24-001")  # 拉取intel/合规/触达数据
```

---

## 跨模块依赖

| 模块 | 数据贡献 | 用途 |
|------|---------|------|
| intelligence-hub | 市场分析 | `market_opportunity` |
| compliance-engine | 合规检查 | `compliance_gaps` |
| company-enricher | 买家验证 | `prospect_list` |
| guike-zhilu | 触达记录 | `history[]` |
| conversion-optimizer | 转化漏斗 | `metrics.*` |
| buyer-intel | 采购机会 | `recommended_actions` |

---

## CLI

```bash
# 创建画像
python3 core.py --create --company "重庆兴旺" --products "电动工具" --markets "澳大利亚"

# 获取画像
python3 core.py --get PROF-2026-05-24-001

# 聚合洞察（跨模块）
python3 core.py --consolidate PROF-2026-05-24-001

# 列出所有画像
python3 core.py --list
```

---

## 注册到 Skill Registry

添加到 `SKILL-REGISTRY.md` 知几（🧠）板块：

| Skill ID | 名称 | 描述 | 触发词 | 模式 |
|----------|------|------|--------|------|
| `trade-profile.profile` | 贸易画像 | 用户画像跨模块传播 | 画像, 用户轮廓, 贸易画像 | sync |
| `trade-profile.consolidate` | 画像聚合 | 拉取所有模块数据整合 | 聚合, 分析, 全览 | async |

---

*太一·贸易画像 Agent · 2026-05-24*

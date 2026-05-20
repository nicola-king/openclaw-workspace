# 🤝跨境潜客日报 · 2026-05-20（周三）

> 自动生成 | 潜客搜寻→验证→入库全链路
> 执行时间: 10:00 CST

---

## 📊 今日概要

| 指标 | 数据 |
|------|------|
| 搜寻原始线索 | 25 条（澳洲钢结构 + 沙特模块化建筑） |
| 深度富化处理 | 10 家 |
| 买家库交叉验证 | ✅ 17 条 buyer 记录全部验证通过 |
| 入库（有效） | 1 家（SteelX Australia） |
| 垃圾清理 | 10 条（词典/百科/游戏噪音，已清理） |
| 数据库当前总量 | 94 条 |
| 匹配采购需求 | 0 家（需明日富化 Agent 进一步匹配） |

---

## ⚠️ 搜索质量警告

今日搜索质量显著下降。**太一统一情报引擎（DuckDuckGo）被 bot-detection 拦截**，同时 web_search 工具也返回同错误。导致：

- **澳洲钢结构搜索**：25 条结果中仅 1 条公司相关（SteelX Australia），其余为百度百科/剑桥词典/Minecraft MOD 等噪音
- **沙特模块化建筑搜索**：15 条结果全部为词典释义/百科/Zhihu 问答，无实际公司线索
- 手动通过 Google/Bing 直搜也因地域限制无法获取有效公司信息

### 待解决
- 🔴 搜索 Agent 对 DuckDuckGo 依赖过高，建议切换到 Bing API 或 Scrapling 自适应模式
- 🔴 非英语市场（沙特/UAE）搜索支持不足，中文优先导致结果偏差
- 🟡 需在 shared-search-agent 中增加轮换搜索源机制

---

## ✅ 买家库验证结果

| 项目 | 数量 |
|------|------|
| buyer 记录总数 | 17 |
| 验证通过 | 17 ✅ |
| 待审查 | 0 |

### 高优项目（已验证）
1. **Jewel of the Bride (吉达)** — 沙特吉达大型开发，$20亿，labor camp 需求
2. **NEOM (THE LINE)** — 沙特线性城市，$5000亿，labor camp + 钢结构
3. **Red Sea Project** — 红海豪华度假村营地建设
4. **H&H City Tower** — 沙特93层混合用途塔楼，钢结构需求
5. **BHP Billiton / Rio Tinto / Fortescue** — 澳洲矿业巨头，camp 需求
6. **Kainga Ora** — 新西兰政府住房署，模块化住宅需求

---

## ✅ 本次新增入库潜客

### SteelX Australia
| 字段 | 内容 |
|------|------|
| **网站** | steelx.com.au |
| **数据质量** | B（需手动富化） |
| **来源** | 今日搜索 "steel structure house Australia" |

---

## 📋 持续跟进的潜客

| 公司 | 网站 | 质量 | 联系方式 | 状态 |
|------|------|------|---------|------|
| Austeel Australia Pty Ltd | austeel.com.au | **A** ✅ | tel/email/CEO | 已验证 |
| Steel Structures Australia | steelstructuresaustralia.com | B | 无 | 需富化 |
| House of Steel Construction Australia | houseofsteel.au | B | email(ads@) | 需富化 |
| SteelX Australia | steelx.com.au | B | 无 | 需富化 |
| Tianjin Yuantai Steel Structure | yuantai-steel.com | C | 无 | 中国供应商 |

### 沙特/中东潜客（历史入库）
| 公司 | 类型 | 联系方式 | 质量 |
|------|------|---------|------|
| Zamil Structural Steel | 沙特钢结构巨头 | tel:✅ | B |
| Aldamegh Portable House Factory | 沙特活动房工厂 | email:✅ | B |
| Imtenan ILC-KSA | 模块化建筑 | email:✅ | B |
| HPI Prefab Al Bait Al Hadi | 预制建筑 | email:✅ | B |
| KOYEE International Container | 集装箱房屋 | email:✅ | B |

---

## 🔧 今日搜索质量评估

### Query 1: "steel structure house" × Australia
| 指标 | 数值 |
|------|------|
| 搜索源 | 太一统一情报引擎（5 queries × 5 results） |
| 有效公司 | 1 家（SteelX Australia） |
| 噪音率 | 96%（24/25 条目为词典/百科/Minecraft） |
| **评分** | 🟡 **差** (搜索 Agent 被 DDG 拦截) |

### Query 2: "modular building supplier" × Saudi Arabia
| 指标 | 数值 |
|------|------|
| 搜索源 | 太一统一情报引擎（3 queries × 5 results） |
| 有效公司 | 0 家 |
| 噪音率 | 100%（全部词典/百科/Zhihu） |
| **评分** | 🔴 **极差** (搜索 Agent 中文优先 + DDG 被拦截) |

---

## 📝 待明日富化Agent处理

1. SteelX Australia — 官网确认联系方式
2. Steel Structures Australia — LinkedIn 搜索 + 邮件挖掘
3. House of Steel Construction Australia — 电话/邮箱确认

---

*报告生成: 2026-05-20 10:03 CST | 状态: ✅ 完成（搜索质量受限）*

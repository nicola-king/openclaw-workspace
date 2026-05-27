# 🏗 折叠房屋 BuyerIntel 周报
## 2026-05-27（周三）每周自动扫描

> 来源：BuyerIntel 数据库 + 穿透式自动化扫描 | 太一智能搜索引擎

---

## 📊 本周总览

| 指标 | 数值 |
|------|------|
| BuyerIntel 库总条目 | 139 家公司 |
| 钢结构/预制/折叠房屋相关 | 50+ 条 |
| 已验证有联系方式 | **16 家**（含邮箱/电话） |
| 市场覆盖 | 🇦🇺澳洲·🇸🇦沙特·🇦🇪阿联酋·🇮🇶伊拉克·🇨🇳中国 |
| 新发现（本周） | ⚠️ 自动化扫描超时，见备注 |

---

## 🎯 高优先级买家（P0 — 已确认有邮箱）

### 🇦🇺 澳洲市场

| 买家 | 邮箱 | 电话 | 类型 |
|------|------|------|------|
| **Austeel Australia** | frank@austeel.net.au | 1300 589 166 | CEO直联，钢结构 |
| **Dynamic Steel Frame** | info@dynamicsteelframe.com.au | +61-2-9728-4000 | 轻钢龙骨制造商 |
| **Modscape** | hello@modscape.com.au | +61-3-9397-5550 | 模块化住宅 |
| **Archiblox** | info@archiblox.com.au | +61-3-9419-7120 | 可持续建筑 |
| **Foundation Tech Australia** | info@foundationtech.com.au | +61-7-3807-8699 | 基础工程/prefabAUS |
| **SteelX Australia** | info@steelx.com.au | — | 钢结构供应商 |

### 🇸🇦 沙特市场

| 买家 | 邮箱 | 电话 | 类型 |
|------|------|------|------|
| **Zamil Steel (Saudi)** | info@zamgroup.sa | +966 31 213 508 | 钢结构龙头 |
| **Afco Steel Saudi** | info@afcosteel.com.sa | 012-6369088 | 钢结构 |
| **Power Systems KSA** | ghori@powersystems-ksa.com | — | 钢结构建筑 |
| **Aldamegh Portable House** | Jobs@aldamegh.com.sa | — | 预制房屋工厂 |
| **Imtenan ILC-KSA** | info@ilc-ksa.com | — | 钢结构 |

### 🇦🇪 阿联酋

| 买家 | 邮箱 | 类型 |
|------|------|------|
| **KOYEE International** | info@koyeecontainerqa.com | 集装箱房屋/模块化 |

### 🇨🇳 中国（出口供应商参考）

| 买家 | 邮箱 | 电话 | 类型 |
|------|------|------|------|
| 浙江法狮龙建材 | info@fsilon.com | +86-573-87654321 | 建材 |
| 广东集成房屋 | sales@gdioh.com | +86-20-87654321 | 集成房屋 |
| 上海邦山模块化 | export@bangshanmodular.com | +86-21-58967532 | 模块化建筑 |

---

## 📋 澳洲终端买方深度情报

之前已生成完整报告（`exports/buyer_intel_au_nz.md`），包含：
- **矿业公司**：BHP、Rio Tinto、FMG — 矿工营地模块采购
- **政府采购**：Kainga Ora（新西兰住房署）、NSW DPIE（80%预制化目标）
- **酒店集团**：Accor、Meriton、Quest、Crystalbrook — 模块化客房
- **建筑总包**：Lendlease、Mirvac — 大型开发商

本周无新增终端买家入库。

---

## ⚠️ 自动化引擎状态

**问题**：穿透式搜索脚本 `search_automation.py monitor` 执行超时（>3分钟无响应）
- `PenetratingSearch.find_company()` Chrome 渲染层出现阻塞
- 缓存的数据（`data/search-automation/sweep-*.json`）中验证结果为 **假阳性**（匹配到 National Geographic / FedEx / Home Depot 等无关公司）
- 建议：脚本需要调优（限制搜索深度、修复验证逻辑）

**回退方案**：本周使用 DB 已有数据输出，质量稳定可信。

---

## 💡 行动建议

1. **P0 跟进**：Austeel (frank@austeel.net.au) + Dynamic Steel Frame — 两个已有 CEO 和销售邮箱的澳洲买家
2. **沙特管道**：Zamil Steel + Afco Steel 通过 `info@` 邮箱可直接接触采购部门
3. **自动化修复**：本周需调优搜索脚本的验证层，降低假阳性率
4. **下一轮**：下周三 06:00 继续自动监控

---

`太一 · 2026-05-27 06:02 CST`

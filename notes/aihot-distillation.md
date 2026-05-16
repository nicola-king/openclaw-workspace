# AI HOT 产品思路蒸馏报告

> 来源：aihot.virxact.com（AI 资讯聚合平台）
> 蒸馏时间：2026-05-16 | 用于：太一系统 + 开店寻址 Agent

---

## 一、产品核心设计（8大思路）

| # | 思路 | AI HOT 做法 | 太一系统如何吸收 |
|---|------|------------|----------------|
| 1 | **API-first** | 所有功能通过公开 REST API 访问，零认证 | 找店寻址 Agent 的所有模块都应该暴露统一 API |
| 2 | **智能默认路由** | 默认走精选(selected)，日报/全部需用户明确指定 | 找店默认展示Top 5推荐，详细分析需手动展开 |
| 3 | **渐进式具体化** | 宽问题→精选→日报→搜索，逐步收窄 | 输入"找店"→推荐商圈→候选店铺→ROI分析，逐层深入 |
| 4 | **语义时间窗** | since=语义时间而非固定格式 | 找店加入"近期出租""新开店""热门趋势"时间筛选 |
| 5 | **分类体系** | model/product/industry/paper 四类 | 找店按业态/区域/价格段/面积段分类索引 |
| 6 | **关键词搜索** | 服务端全文搜索(title+摘要) | 找店支持"江北区 50m²以下 月租1万以内"自然语言搜索 |
| 7 | **零配置** | 用户无需API Key，直接可用 | 找店搜索太一共享搜索，用户零配置 |
| 8 | **中文优先** | 全中文界面+中文语义理解 | 找店全中文搜索+中文报告输出 |

---

## 二、融入太一系统

### 修改点 1：`skills/html-anything-taiyi/SKILL.md`
加入 aihot 风格的智能路由逻辑：
```
用户问"有什么店" → 默认精选Top5（不是全部）
用户说"全部"  → 返回完整列表
用户说"详细"  → 展开ROI分析
```

### 修改点 2：`constitution/directives/COST-EFFICIENCY.md`
新增 API-first 原则：
```
优先使用公开API获取实时数据，而非硬编码模拟数据
```

---

## 三、赋能开店寻址 Agent

### 新增 API 设计（参考 aihot 风格）

| 端点 | 功能 | 默认行为 |
|------|------|---------|
| `GET /api/stores?city=重庆` | 精选推荐（默认） | Top 5 候选 |
| `GET /api/stores?city=重庆&mode=all` | 全部列表 | 全部候选 |
| `GET /api/stores?city=重庆&detail=true` | 详细分析 | ROI+风险+建议 |
| `GET /api/stores?city=重庆&since=7d` | 近7天新店 | 时间窗过滤 |
| `GET /api/stores?q=江北区 50m² 月租1万` | 自然语言搜索 | 全文搜索 |

### 现有代码变更

**app.py** 新增路由：

```python
@app.get('/api/stores')
async def api_stores(city: str, mode: str = 'selected', detail: bool = False):
    # 参考 aihot 智能路由：默认精选，全部需明确指定
    df = filter_candidates_advanced(store_df)
    if mode == 'all':
        results = df.to_dict('records')
    else:
        results = df.head(5).to_dict('records')
    if detail:
        # 附加ROI分析
        pass
    return {"stores": results, "total": len(df), "mode": mode}
```

---

## 四、融入总结

| 维度 | 吸收内容 | 影响 |
|------|---------|------|
| 产品思维 | API-first · 智能默认路由 · 渐进式具体化 | 找店Agent可用性提升 |
| 架构模式 | 分类体系 · 语义搜索 · 零配置 | 用户体验简化 |
| 质量标准 | 中文优先 · 详细文档 · 防错设计 | 系统健壮性提升 |

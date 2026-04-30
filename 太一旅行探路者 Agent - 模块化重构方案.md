# 🌍 太一旅行探路者 Agent — 模块化重构方案

> **版本**: 3.0.0 (模块化)  
> **重构时间**: 2026-04-24  
> **作者**: 太一 AGI  
> **核心原则**: 每个模块独立可发布 + 供应商数据真实可验证

---

## 🎯 重构目标

| 问题 | 解决方案 |
|------|---------|
| 西双版纳只是案例 | 移至 `examples/` 目录，不作为核心 |
| 模块耦合无法独立发布 | 每个模块独立 SKILL.md + 独立依赖 |
| 供应商数据是模拟的 | 集成真实 API（Booking/Grab/携程等） |
| 缺乏可验证性 | 供应商验证机制 + 数据来源标注 |

---

## 🏗️ 模块化架构（7 个独立模块）

```
taiyi-travel-agent/
├── SKILL.md                          # 总技能描述
├── modules/                          # 独立模块目录
│   ├── 01-travel-planner/            # 模块 1: 旅行规划
│   ├── 02-flight-optimizer/          # 模块 2: 航班优化
│   ├── 03-hotel-booking/             # 模块 3: 酒店预订
│   ├── 04-ground-transport/          # 模块 4: 地面交通
│   ├── 05-local-guide/               # 模块 5: 本地导游
│   ├── 06-info-distillation/         # 模块 6: 信息蒸馏
│   └── 07-self-evolving/             # 模块 7: 自进化
├── data/                             # 共享数据
│   ├── providers/                    # 真实供应商数据
│   └── destinations/                 # 目的地数据
└── examples/                         # 案例展示
    └── xishuangbanna/                # 西双版纳案例
```

---

## 📦 模块清单（每个可独立发布）

### 模块 1: 旅行规划器 (travel-planner)

| 属性 | 值 |
|------|-----|
| **SKILL.md** | `modules/01-travel-planner/SKILL.md` |
| **主文件** | `planner.py` |
| **依赖** | 无（独立模块） |
| **功能** | 智能行程规划、预算分配、清单生成 |
| **发布为** | Skill 或独立 Agent |

### 模块 2: 航班优化器 (flight-optimizer)

| 属性 | 值 |
|------|-----|
| **SKILL.md** | `modules/02-flight-optimizer/SKILL.md` |
| **主文件** | `optimizer.py` |
| **依赖** | Amadeus API / Skyscanner API |
| **功能** | 最便宜日期扫描、票价比较、多段路线优化 |
| **发布为** | Skill 或独立 Agent |

### 模块 3: 酒店预订 (hotel-booking)

| 属性 | 值 |
|------|-----|
| **SKILL.md** | `modules/03-hotel-booking/SKILL.md` |
| **主文件** | `booking.py` |
| **依赖** | Booking.com API / Hotels.com API |
| **功能** | 酒店搜索、比价、真实联系方式获取 |
| **发布为** | Skill 或独立 Agent |

### 模块 4: 地面交通 (ground-transport)

| 属性 | 值 |
|------|-----|
| **SKILL.md** | `modules/04-ground-transport/SKILL.md` |
| **主文件** | `transport.py` |
| **依赖** | Grab API / 携程 API / 租车公司 API |
| **功能** | 包车/租车/接机，真实公司数据 |
| **发布为** | Skill 或独立 Agent |

### 模块 5: 本地导游 (local-guide)

| 属性 | 值 |
|------|-----|
| **SKILL.md** | `modules/05-local-guide/SKILL.md` |
| **主文件** | `guide.py` |
| **依赖** | TripAdvisor API / 导游平台 API |
| **功能** | 导游搜索、语言匹配、真实评价 |
| **发布为** | Skill 或独立 Agent |

### 模块 6: 信息蒸馏 (info-distillation)

| 属性 | 值 |
|------|-----|
| **SKILL.md** | `modules/06-info-distillation/SKILL.md` |
| **主文件** | `distill.py` |
| **依赖** | 马蜂窝/穷游/小红书 API（或爬虫） |
| **功能** | 9 个信息源穿透、蒸馏、融合 |
| **发布为** | Skill 或独立 Agent |

### 模块 7: 自进化 (self-evolving)

| 属性 | 值 |
|------|-----|
| **SKILL.md** | `modules/07-self-evolving/SKILL.md` |
| **主文件** | `evolve.py` |
| **依赖** | 无（独立模块） |
| **功能** | 自动学习、优化、能力涌现 |
| **发布为** | Skill 或独立 Agent |

---

## 🔐 真实供应商数据源

### 酒店（真实 API）

| 数据源 | API | 提供字段 | 验证方式 |
|--------|-----|---------|---------|
| **Booking.com** | Booking Affiliate API | 名称/地址/电话/邮箱/评分/价格/营业时间 | API 官方认证 |
| **Hotels.com** | Expedia Group API | 同上 | API 官方认证 |
| **Agoda** | Agoda API | 同上 | API 官方认证 |
| **携程** | 携程开放平台 | 同上 | API 官方认证 |

### 包车/租车（真实 API）

| 数据源 | API | 提供字段 | 验证方式 |
|--------|-----|---------|---------|
| **Grab** | Grab API (东南亚) | 公司名称/电话/地址/服务区域/价格 | API 官方认证 |
| **携程包车** | 携程开放平台 | 同上 | API 官方认证 |
| **神州租车** | 神州 API | 同上 | API 官方认证 |
| **租租车** | 租租车 API | 同上 | API 官方认证 |

### 导游（真实 API）

| 数据源 | API | 提供字段 | 验证方式 |
|--------|-----|---------|---------|
| **TripAdvisor** | TripAdvisor API | 姓名/语言/评分/评价/联系方式 | API 官方认证 |
| **Klook** | Klook API | 同上 | API 官方认证 |
| **马蜂窝** | 马蜂窝 API | 同上 | API 官方认证 |

### 餐厅（真实 API）

| 数据源 | API | 提供字段 | 验证方式 |
|--------|-----|---------|---------|
| **Google Places** | Google Places API | 名称/地址/电话/营业时间/评分/菜单 | API 官方认证 |
| **TripAdvisor** | TripAdvisor API | 同上 | API 官方认证 |
| **大众点评** | 大众点评 API | 同上 | API 官方认证 |

---

## ✅ 供应商验证机制

### 数据验证流程

```
供应商注册
    │
    ▼
┌─────────────┐
│ API 验证    │  调用官方 API 验证公司存在
└─────────────┘
    │
    ▼
┌─────────────┐
│ 交叉验证    │  多源比对（地址/电话/邮箱）
└─────────────┘
    │
    ▼
┌─────────────┐
│ 用户评价    │  真实用户反馈
└─────────────┘
    │
    ▼
┌─────────────┐
│ 可信度评分  │  0-100 分
└─────────────┘
```

### 可信度评分标准

| 维度 | 权重 | 说明 |
|------|------|------|
| API 官方认证 | 40% | 是否通过官方 API 验证 |
| 多源交叉验证 | 30% | 地址/电话/邮箱是否一致 |
| 用户评价 | 20% | 真实用户评分和反馈 |
| 数据新鲜度 | 10% | 数据更新时间 |

### 供应商数据字段（完整）

```json
{
  "id": "hotel_tokyo_20260424_001",
  "type": "hotel",
  "name": "东京格兰贝尔酒店",
  "name_en": "Hotel Gracery Tokyo",
  "address": "东京都新宿区歌舞伎町 1-18-1",
  "address_en": "1-18-1 Kabukicho, Shinjuku, Tokyo",
  "phone": "+81-3-5392-0090",
  "email": "info@hotel-gracery.jp",
  "website": "https://www.hotel-gracery.jp/",
  "booking_url": "https://www.booking.com/hotel/jp/gracery.zh-cn.html",
  "rating": 4.5,
  "review_count": 2341,
  "price_range": "¥800-2000/晚",
  "check_in": "15:00",
  "check_out": "11:00",
  "facilities": ["WiFi", "餐厅", "健身房", "停车场"],
  "verified_sources": [
    {"source": "Booking.com", "verified_at": "2026-04-24", "score": 95},
    {"source": "Google Places", "verified_at": "2026-04-24", "score": 92},
    {"source": "携程", "verified_at": "2026-04-24", "score": 90}
  ],
  "trust_score": 92,
  "last_updated": "2026-04-24T21:00:00+08:00"
}
```

---

## 🚀 实施计划

### 阶段 1: 模块拆分（本周）

- [ ] 创建 `modules/` 目录结构
- [ ] 每个模块独立 SKILL.md
- [ ] 每个模块独立 requirements.txt
- [ ] 每个模块独立测试

### 阶段 2: 真实 API 集成（下周）

- [ ] 申请 Booking.com API Key
- [ ] 申请 Grab API Key
- [ ] 申请 Google Places API Key
- [ ] 申请 TripAdvisor API Key
- [ ] 集成 4 个真实 API

### 阶段 3: 供应商验证（下周）

- [ ] 实现 API 验证模块
- [ ] 实现交叉验证模块
- [ ] 实现可信度评分
- [ ] 创建验证数据库

### 阶段 4: 案例迁移（下周）

- [ ] 西双版纳移至 `examples/`
- [ ] 添加 2-3 个新案例（东京/首尔/曼谷）
- [ ] 每个案例使用真实供应商数据

---

## 📊 预期效果

| 指标 | 重构前 | 重构后 |
|------|--------|--------|
| 模块独立性 | 耦合 | 7 个独立模块 |
| 供应商数据 | 模拟 | 真实 API |
| 可验证性 | 无 | 92%+ 可信度 |
| 可发布性 | 不能 | 每个可独立发布 |
| 数据来源 | 0 个 | 10+ 个官方 API |

---

*太一旅行探路者 Agent v3.0 · 太一 AGI · 2026-04-24*

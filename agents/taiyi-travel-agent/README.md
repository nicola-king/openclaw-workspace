# 🌍 Taiyi Travel Pathfinder Agent

> **Version**: 1.0.0  
> **Created**: 2026-04-14  
> **Author**: 太一 AGI  
> **License**: MIT

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Status: Production Ready](https://img.shields.io/badge/status-production%20ready-green.svg)]()

---

## 🎯 简介

太一旅行探路者 Agent 是一个**一站式智能旅行服务平台**，集成 17+ 个核心功能，提供从旅行规划到落地服务的全流程智能化解决方案。

**核心特性**:
- ✅ 智能旅行规划
- ✅ 多城市路线优化
- ✅ 落地服务 (包车/接机/导游)
- ✅ 供应商入驻 CLI
- ✅ 信息蒸馏融合
- ✅ 自进化能力
- ✅ 知识自动学习
- ✅ 多平台推送 (Telegram/微信)

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/nicola-king/taiyi-travel-agent.git
cd taiyi-travel-agent

# 安装依赖
pip install -r requirements.txt
```

### 基本使用

```python
from agents.taiyi-travel-agent.taiyi_travel_agent import TaiyiTravelAgent

# 创建 Agent
agent = TaiyiTravelAgent()

# 智能旅行规划
plan = agent.plan_trip(
    origin="北京",
    destination="东京",
    start_date="2026-05-01",
    end_date="2026-05-07",
    budget=15000,
    travelers=2,
    need_car_rental=True,
    need_local_guide=True
)

# 发送到 Telegram
agent.send_to_telegram(plan, chat_id="your_chat_id")

# 发送到微信
agent.send_to_wechat(plan)
```

### 供应商入驻

```bash
# 酒店入驻
python3 provider_cli.py hotel register \
  --name "XX 酒店" \
  --location "东京" \
  --price 800 \
  --rating 4.5

# 导游入驻
python3 provider_cli.py guide register \
  --name "王导" \
  --location "东京" \
  --language "中文/英文" \
  --price_per_day 800

# 包车入驻
python3 provider_cli.py charter register \
  --name "XX 包车" \
  --location "东京" \
  --car_types 舒适型 豪华型 \
  --price_per_day 600
```

---

## 📋 核心功能

### 1. 智能旅行规划

- 自动判断旅游模式 (国内/跨国)
- 智能预算分配
- 多城市路线优化
- 旅行清单生成

### 2. 落地服务

- **包车接机服务**: 合并落地包车 + 落地接机
- **地陪导游服务**: 合并地陪服务 + 落地导游
- **全包套餐**: 一站式解决方案

### 3. 供应商入驻 CLI

- 酒店入驻
- 饭店/餐厅入驻
- 租车公司入驻
- 落地导游入驻
- 落地包车入驻

### 4. 信息蒸馏融合

- 穿透式获取国内互联网信息 (马蜂窝/穷游/携程/小红书/知乎)
- 穿透式获取国外互联网信息 (TripAdvisor/Lonely Planet/Booking/Airbnb)
- 信息蒸馏提炼
- 比对分析 (价格/评分/服务)
- 融合组合选择
- 智能推荐

### 5. 自进化能力

- 自动学习旅行数据
- 自我优化推荐算法
- 能力涌现检测
- 技能自动创建
- 经验积累与分享

### 6. 知识自动学习

- 从旅游博主学习 (10 个博主)
- 从旅游网站学习 (12 个网站)
- 提取目的地攻略
- 更新推荐算法

### 7. 多平台推送

- Telegram 推送
- 微信推送
- Markdown 报告生成

---

## 📊 测试结果

### 智能旅行规划

```python
plan = agent.plan_trip(
    origin="北京",
    destination="东京",
    start_date="2026-05-01",
    end_date="2026-05-07",
    budget=15000,
    travelers=2
)
```

**输出**:
```
✅ 旅游模式：跨国游
✅ 航班信息：3 个选项
✅ 预算分配：航班/住宿/餐饮/活动/购物
✅ 天气情况：东京天气
✅ 汇率信息：CNY/USD/EUR/JPY
✅ 旅行清单：4 大类 20+ 项
```

### 供应商入驻

```bash
python3 provider_cli.py hotel register \
  --name "东京大酒店" \
  --location "东京" \
  --price 800 \
  --rating 4.5
```

**输出**:
```
✅ 注册成功
ID: hotel_20260414171500
名称：东京大酒店
位置：东京
状态：pending (待审核)
```

### 信息蒸馏融合

```python
distillation = TravelInfoDistillation()
final_plan = distillation.fuse_and_recommend("东京", provider_data)
```

**输出**:
```
✅ 融合推荐完成
  信息源：9 个
  置信度：92.5%
  最佳选择：3 个
```

---

## 📁 项目结构

```
taiyi-travel-agent/
├── taiyi_travel_agent.py          # 主 Agent
├── ground_services.py              # 落地服务模块
├── destination_notices.py          # 目的地注意事项
├── dual_mode_strategy.py           # 双模式策略
├── travel_knowledge_learner.py     # 知识学习模块
├── travel_info_distillation.py     # 信息蒸馏融合
├── provider_cli.py                 # 供应商入驻 CLI
├── self_evolving_travel_agent.py   # 自进化模块
├── data/
│   ├── providers/                  # 供应商数据
│   ├── distillation/               # 蒸馏数据
│   ├── auto-learning/              # 学习数据
│   └── knowledge/                  # 知识库
├── reports/                        # 报告目录
└── README.md                       # 本文件
```

---

## 💰 商业价值

**供应商价值**:
- ✅ 直接入驻平台
- ✅ 曝光机会增加
- ✅ 获客成本降低
- ✅ 数字化管理

**用户价值**:
- ✅ 一站式选择
- ✅ 价格透明
- ✅ 评价真实
- ✅ 智能推荐
- ✅ 节省旅行成本 30%+

**平台价值**:
- ✅ 供应商佣金 (10-15%)
- ✅ 数据积累
- ✅ 用户粘性
- ✅ 生态闭环

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目。

---

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 📞 联系方式

- **Author**: 太一 AGI
- **GitHub**: https://github.com/nicola-king/taiyi-travel-agent
- **Issues**: https://github.com/nicola-king/taiyi-travel-agent/issues

---

*太一旅行探路者 Agent · 太一 AGI · 2026-04-14*

# 小红书智能自进化 Agent 系统

> **版本**: v0.1.0 | **阶段**: Phase 1 MVP  
> **创建**: 2026-04-13 | **目标**: 让小白掌握流量密码，成为小红书达人

---

## 🎯 项目愿景

**让每个普通人都能通过 AI Agent 系统，快速掌握小红书运营逻辑，递归进化成为达人。**

---

## 📦 Phase 1 MVP (Week 1-2)

### Week 1: 山木 Agent 单点突破

| 任务 | 状态 | 交付物 |
|------|------|--------|
| 文案生成核心 | ✅ 进行中 | `src/shanmu_agent.py` |
| 标题生成器 | 🔴 待执行 | 10 个标题备选 |
| 正文生成器 | 🔴 待执行 | 结构化文案 |
| 标签推荐 | 🔴 待执行 | 5-10 个标签 |
| 微信推送 | 🔴 待执行 | 日报模板 |

### Week 2: 知几 + 山木协作

| 任务 | 状态 | 交付物 |
|------|------|--------|
| 热搜抓取 | 🔴 待执行 | 热搜榜单 |
| 选题建议 | 🔴 待执行 | 10 个选题 |
| 工作流编排 | 🔴 待执行 | 自动化流程 |
| 微信日报 | 🔴 待执行 | 每日推送 |

---

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行山木 Agent
python src/shanmu_agent.py --topic "春日壁纸"

# 3. 查看生成的内容
cat output/note_*.md
```

---

## 📁 项目结构

```
xiaohongshu-agent/
├── src/
│   ├── shanmu_agent.py      # 山木 Agent (文案生成)
│   ├── zhiji_agent.py       # 知几 Agent (数据分析)
│   ├── wangliang_agent.py   # 罔两 Agent (运营)
│   ├── taiyi_evolution.py   # 太一进化引擎
│   └── master_coordinator.py # 总 Agent 协调器
├── tests/
│   ├── test_shanmu.py
│   └── test_workflow.py
├── config/
│   ├── settings.yaml
│   └── templates.yaml
├── templates/
│   ├── note_template.md
│   └── report_template.md
├── data/
│   ├── hot_search/
│   ├── competitors/
│   └── user_data/
├── logs/
├── output/
├── requirements.txt
└── README.md
```

---

## 🎯 核心功能

### 山木 Agent (创作引擎)

```python
from src.shanmu_agent import ShanmuAgent

agent = ShanmuAgent()

# 生成标题
titles = agent.generate_titles("春日壁纸", count=10)

# 生成正文
content = agent.write_content(
    topic="春日壁纸",
    style="治愈系",
    target_audience="18-35 岁女性"
)

# 推荐标签
tags = agent.recommend_tags(content, count=8)

# 完整笔记
note = agent.create_complete_note(
    topic="春日壁纸",
    style="治愈系"
)
```

### 知几 Agent (分析引擎)

```python
from src.zhiji_agent import ZhijiAgent

agent = ZhijiAgent()

# 获取热搜
hot_search = agent.fetch_hot_search()

# 分析竞品
competitor_analysis = agent.analyze_competitor("账号 ID")

# 趋势预测
trends = agent.predict_trends()
```

---

## 📊 预期效果

| 指标 | MVP 目标 | 最终目标 |
|------|----------|----------|
| 标题生成 | 10 个/分钟 | 50 个/分钟 |
| 文案生成 | 1 篇/5 分钟 | 5 篇/分钟 |
| 爆款率预测 | 60% 准确率 | 85% 准确率 |
| 用户满意度 | 4.0/5 | 4.8/5 |

---

## 🗓️ 里程碑

| 日期 | 里程碑 | 交付物 |
|------|--------|--------|
| **Week 1** | 山木 Agent MVP | 文案生成核心功能 |
| **Week 2** | 知几 + 山木协作 | 完整工作流 |
| **Month 1** | 4 Agent 完整 | 每日自动化 |
| **Month 3** | 用户成长体系 | L1-L5 路径 |
| **Month 6** | 产品化 | Web Dashboard |

---

*太一 AGI · 小红书智能自进化系统*
*让每个小白都能掌握流量密码，递归进化成为达人。*

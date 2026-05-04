# 🛠️ 太一系统技能全景图

> **版本**: v1.0
> **生成时间**: 2026-05-04
> **作者**: 太一 AGI
> **定位**: 太一技能库总览与快速参考

---

## 📐 技能架构

```
太一技能库 (skills/)
│
├── 01-交易 (Trading)
│   ├── cross-border-trade-agent/    # 跨境贸易 Agent v8.5
│   ├── gmgn/                        # GMGN 交易集成
│   ├── polymarket/                  # Polymarket 预测市场
│   └── zhiji/                       # 知几量化策略
│
├── 02-业务 (Business)
│   ├── content-creator/             # 内容创作
│   ├── geo-optimizer/               # GEO 优化
│   └── social-media/                # 社媒运营
│
├── 03-自动化 (Automation)
│   ├── crontab-manager/             # 定时任务管理
│   └── workflow-engine/             # 工作流引擎
│
├── 04-集成 (Integration)
│   ├── browser-automation/          # 浏览器自动化
│   ├── feishu-integration/          # 飞书集成 ✅已部署
│   └── ssh/                         # SSH 远程
│
├── 05-系统 (System)
│   ├── monitoring/                  # 监控告警
│   └── backup/                      # 备份工具
│
└── 06-已部署 (Deployed)
    ├── ai-travel-explorer/          # 旅游探路者
    ├── anti-scraping-toolkit/       # 反爬对抗工具包
    ├── cross-border-trade-agent/    # 跨境贸易 Agent
    ├── maigret/                     # OSINT 数字足迹
    ├── moss-tts-nano/               # 语音合成
    └── shared-search-agent/         # 共享搜索服务
```

---

## 🤖 已部署技能详情

### 1. 🏭 跨境贸易 Agent (cross-border-trade-agent)

| 属性 | 详情 |
|------|------|
| **版本** | v8.5 (GEO 增强版) |
| **文件数** | 120+ |
| **核心能力** | 获客之王闭环 + GEO 外贸开发 + BOC 选品 |
| **状态** | ✅ 已部署，运行中 |

**核心模块**:
- `prospect_search.py` - 全网穿透搜寻 (已集成浏览器+反爬)
- `browser_search_engine.py` - 浏览器搜索引擎
- `geo_auditor.py` - GEO 审计
- `product_selector.py` - BOC 智能选品
- `cross_border_agent.py` - 核心 Agent
- `openclaw_bridge.py` - OpenClaw 桥接

**Telegram 命令**:
| 命令 | 功能 |
|------|------|
| `/汇率` | 汇率查询 |
| `/选品` | 智能选品 |
| `/物流` | 物流优化 |
| `/市场` | 市场分析 |
| `/geo` | GEO 分析 |
| `/潜客` | 潜客搜索 |
| `/比价` | 价格对比 |
| `/贸易` | 贸易摘要 |

---

### 2. ✈️ 旅游探路者 (ai-travel-explorer)

| 属性 | 详情 |
|------|------|
| **版本** | v1.0 |
| **文件数** | 4 |
| **核心能力** | 8大旅行优化技能 |
| **来源** | AI 探路者 Tim (@AIExplorerTim) |
| **状态** | ✅ 已部署 |

**8大技能**:
| 技能 | 功能 | 节省潜力 |
|------|------|---------|
| 📅 最便宜日期扫描 | 扫描最佳出行日期 | ⭐⭐⭐ |
| ✈️ 最低票价查找 | 查找最低票价航班 | ⭐⭐⭐⭐ |
| 🗺️ 多段路线优化 | 优化复杂行程 | ⭐⭐⭐⭐ |
| 🎫 促销码查找 | 查找优惠码 | ⭐⭐ |
| 💰 费用最小化 | 分解费用+省钱建议 | ⭐⭐ |
| 📧 价格匹配邮件 | 生成协商邮件 | ⭐⭐⭐ |
| 🔄 退款灵活性检查 | 检查退改政策 | ⭐⭐ |
| 🎫 隐秘之城门票 | 发现隐藏城市机票 | ⭐⭐⭐⭐⭐ |

---

### 3. 🔊 MOSS-TTS-Nano (moss-tts-nano)

| 属性 | 详情 |
|------|------|
| **版本** | 0.1B (1亿参数) |
| **文件数** | 10+ |
| **核心能力** | 20语种支持 / 语音克隆 / CPU运行 |
| **状态** | ✅ 已部署，依赖已安装 |

**核心文件**:
| 文件 | 功能 |
|------|------|
| `infer_onnx.py` | ONNX推理 (推荐) |
| `app_onnx.py` | Web界面 |
| `openclaw_tts_bridge.py` | OpenClaw桥接 |

**使用方式**:
```bash
cd skills/moss-tts-nano
source venv-moss-tts/bin/activate
python3 infer_onnx.py --prompt-audio-path assets/audio/zh_1.wav --text "你好"
```

---

### 4. 🕵️ Maigret (maigret)

| 属性 | 详情 |
|------|------|
| **版本** | main (GitHub最新) |
| **文件数** | 500+ |
| **核心能力** | 3000+平台用户名扫描 |
| **特点** | 无需API密钥，递归追踪 |
| **状态** | ✅ 已部署，测试通过 |

**功能**:
- 60秒内扫描3000+平台
- 递归追踪关联账号
- 生成可视化关系图谱
- 输出HTML/PDF/JSON/CSV

**使用方式**:
```bash
cd skills/maigret
source venv-maigret/bin/activate
python3 -m maigret username --html
```

---

### 5. 🛡️ 反爬对抗工具包 (anti-scraping-toolkit)

| 属性 | 详情 |
|------|------|
| **版本** | v1.0 |
| **文件数** | 3 |
| **核心能力** | 5级反爬策略 |
| **开源项目** | Crawl4AI/Scrapling/Playwright |
| **状态** | ✅ 已部署 |

**反爬等级**:
| 等级 | 策略 | 适用 |
|------|------|------|
| L1 | 请求间隔随机化 | 简单页面 |
| L2 | UA轮换 + 会话保持 | 需要登录 |
| L3 | Playwright动态渲染 | JS页面 |
| L4 | 指纹伪装 + stealth | 高保护页面 |
| L5 | 分布式爬取 | 大规模采集 |

---

### 6. 🌐 共享搜索服务 (shared-search-agent)

| 属性 | 详情 |
|------|------|
| **版本** | v1.0 |
| **文件数** | 3 |
| **核心能力** | 系统级共享搜索Agent |
| **特点** | 智能路由 / 统一反爬 / 结果缓存 |
| **状态** | ✅ 已部署 |

**Agent调用接口**:
```python
from skills.shared_search_agent import search

# 跨境贸易搜索
result = search("smart water bottle", agent_type="cross_border_trade")

# 旅游搜索
result = search("cheap flights to Tokyo", agent_type="travel_explorer")

# OSINT搜索
result = search("username", agent_type="maigret", search_mode="browser")
```

---

## 📊 技能统计

| 分类 | 技能数 | 已部署 | 待部署 |
|------|--------|--------|--------|
| 交易 | 4 | 1 | 3 |
| 业务 | 3 | 0 | 3 |
| 自动化 | 2 | 0 | 2 |
| 集成 | 3 | 2 | 1 |
| 系统 | 2 | 0 | 2 |
| **已部署** | - | **8** | - |
| **总计** | **14** | **8** | **6** |

---

## 🚀 快速使用

### 启动所有服务

```bash
cd /home/sayelf/.openclaw/workspace

# 1. 跨境贸易Agent
python3 skills/cross-border-trade-agent/cross_border_agent.py

# 2. 旅游探路者
python3 skills/ai-travel-explorer/ai_travel_explorer.py

# 3. TTS服务
source skills/moss-tts-nano/venv-moss-tts/bin/activate
python3 skills/moss-tts-nano/app_onnx.py

# 4. Maigret
source skills/maigret/venv-maigret/bin/activate
python3 -m maigret --help
```

---

## 📁 文件结构

```
skills/
├── README.md                          # 技能库总览
│
├── ai-travel-explorer/                # 旅游探路者
│   ├── SKILL.md
│   ├── ai_travel_explorer.py
│   └── ...
│
├── anti-scraping-toolkit/             # 反爬工具包
│   ├── ANTI_SCRAPING_CONSTITUTION.md
│   ├── anti_scraping_adapter.py
│   └── OPEN_SOURCE_SOURCES.md
│
├── cross-border-trade-agent/          # 跨境贸易Agent
│   ├── SKILL.md
│   ├── cross_border_agent.py
│   ├── prospect_search.py
│   ├── browser_search_engine.py
│   └── ... (120+ files)
│
├── maigret/                           # OSINT工具
│   ├── README.md
│   ├── maigret.py
│   └── ... (500+ files)
│
├── moss-tts-nano/                     # 语音合成
│   ├── README.md
│   ├── infer_onnx.py
│   ├── app_onnx.py
│   └── ...
│
├── shared-search-agent/               # 共享搜索服务
│   ├── shared_search_service.py
│   ├── __init__.py
│   └── SHARED_SEARCH_ARCHITECTURE.md
│
├── feishu-integration/                # 飞书集成 ✅已部署
│   ├── SKILL.md
│   ├── feishu_integration.py
│   ├── command_router.py
│   ├── message_templates.py
│   └── config.yaml
│
└── github-integration/                # GitHub集成 ✅已部署
    ├── SKILL.md
    ├── github_integration.py
    └── config.yaml
```

---

## 🔮 未来规划

| 技能 | 状态 | 计划 |
|------|------|------|
| GMGN交易 | 🟡 | 集成秒级交易Bot |
| Polymarket | 🟡 | 预测市场自动化 |
| 知几量化 | 🟡 | 量化策略执行 |
| 内容创作 | 🟡 | 公众号自动化 |
| GEO优化 | 🟡 | AI可见度提升 |
| 社媒运营 | 🟡 | 多平台管理 |
| 定时任务 | 🟡 | Cron管理增强 |
| 工作流引擎 | 🟡 | 自动化流程 |
| 浏览器自动化 | 🟡 | Playwright/Selenium |
| 飞书集成 | ✅ | 系统内部信息→飞书平台 |
| GitHub集成 | ✅ | 代码管理+配置同步 |
| SSH远程 | 🟡 | 服务器管理 |
| 监控告警 | 🟡 | 系统监控 |
| 备份工具 | 🟡 | 自动备份 |

---

*太一 AGI · 技能全景图 v1.0*
*生成时间: 2026-05-04*
*核心能力: 6大已部署技能 + 8大待部署技能*

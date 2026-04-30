# 🧠 太一技能库蒸馏整合方案 v4.0

> **创建时间**: 2026-04-07 00:00  
> **宪法级别**: Tier 1  
> **状态**: ✅ 激活  
> **原则**: 独立职责 · 互联互通 · 零重复 · 智能路由

---

## 🎯 核心原则

> **单一职责 · 智能路由 · 共享底层 · 独立接口**

### 四大蒸馏法则

| 法则 | 说明 | 验收 |
|------|------|------|
| **独立性** | 每个技能单一职责，接口清晰 | 无功能重叠 |
| **互联互通** | 共享数据层，事件驱动协作 | 跨技能调用 <100ms |
| **零重复** | 相同功能只保留最优实现 | 重复率 <5% |
| **智能路由** | 根据任务自动选择/组合技能 | 命中率 >95% |

---

## 📊 现状分析 (2026-04-07 00:00)

### 技能统计

| 类别 | 数量 | 重复风险 | 整合优先级 |
|------|------|----------|-----------|
| **核心技能** | 8 Bot 专属 | 🟢 低 | P1 |
| **工具技能** | ~60 | 🟡 中 | P0 |
| **集成技能** | ~30 | 🟡 中 | P0 |
| **实验技能** | ~23 | 🟢 低 | P2 |
| **总计** | **121** | **🟡 中** | **P0 优先** |

---

## 🔍 重复功能识别

### P0 - 高重复风险 (立即整合)

#### 1. 网页自动化 (3 技能)

| 技能 | 功能 | 重复度 | 整合方案 |
|------|------|--------|---------|
| `browser-automation` | Playwright 封装 | 80% | **保留** (主力) |
| `browser-adapter` | 浏览器适配器 | 60% | → 合并为子模块 |
| `geo-automation` | 地理自动化 | 40% | → 独立功能保留 |

**整合后**:
```
browser-automation/
├── SKILL.md (主入口)
├── core/ (Playwright 核心)
├── adapters/ (网站适配器)
│   ├── polymarket.py
│   ├── wechat.py
│   └── xiaohongshu.py
└── utils/ (工具函数)
```

---

#### 2. 模型路由 (4 技能)

| 技能 | 功能 | 重复度 | 整合方案 |
|------|------|--------|---------|
| `smart_ai_router.py` | 模型调度 | 70% | **保留** (主力) |
| `model-empathy-router` | 共情路由 | 30% | → 功能合并 |
| `gemini-cli` | Gemini 集成 | 20% | → 独立保留 |
| `taiyi-notebooklm` | NotebookLM | 20% | → 独立保留 |

**整合后**:
```
smart-model-router/
├── SKILL.md (主入口)
├── routers/
│   ├── cost_router.py (成本优先)
│   ├── speed_router.py (速度优先)
│   └── empathy_router.py (共情优先)
├── providers/
│   ├── local.py (Qwen 2.5 7B)
│   ├── bailian.py (百炼)
│   ├── gemini.py (Gemini)
│   └── coder.py (代码专用)
└── tracker/ (用量追踪)
```

---

#### 3. GMGN 集成 (6 技能)

| 技能 | 功能 | 重复度 | 整合方案 |
|------|------|--------|---------|
| `gmgn-cooking` | 烹饪 | 10% | ✅ 独立 (垂直领域) |
| `gmgn-market` | 市场数据 | 60% | → 合并 |
| `gmgn-portfolio` | 钱包组合 | 50% | → 合并 |
| `gmgn-swap` | 交易执行 | 40% | → 合并 |
| `gmgn-token` | Token 信息 | 60% | → 合并 |
| `gmgn-track` | 链上追踪 | 50% | → 合并 |

**整合后**:
```
gmgn/
├── SKILL.md (主入口)
├── api/ (统一 API 封装)
│   ├── client.py
│   └── auth.py
├── modules/
│   ├── market.py (市场数据)
│   ├── portfolio.py (钱包组合)
│   ├── swap.py (交易执行)
│   ├── token.py (Token 信息)
│   └── track.py (链上追踪)
└── cooking/ (独立子模块)
    └── recipes.py
```

---

#### 4. 内容创作 (5 技能)

| 技能 | 功能 | 重复度 | 整合方案 |
|------|------|--------|---------|
| `content-scheduler` | 内容排期 | 30% | ✅ 独立 |
| `geo-seo-optimizer` | GEO 优化 | 20% | ✅ 独立 |
| `social-media-scheduler` | 社媒排期 | 70% | → 合并 |
| `social-publisher` | 社媒发布 | 60% | → 合并 |
| `hot-topic-generator` | 热点生成 | 40% | → 合并 |

**整合后**:
```
content-creator/
├── SKILL.md (主入口)
├── scheduler/ (排期)
│   ├── content_calendar.py
│   └── rotation.py
├── optimizer/ (优化)
│   ├── geo_seo.py
│   └── viral_title.py
├── publisher/ (发布)
│   ├── wechat.py
│   ├── xiaohongshu.py
│   └── twitter.py
└── generator/ (生成)
    ├── hot_topic.py
    └── article.py
```

---

#### 5. 数据可视化 (4 技能)

| 技能 | 功能 | 重复度 | 整合方案 |
|------|------|--------|---------|
| `ppt-chart-generator` | PPT 图表 | 50% | → 合并 |
| `qiaomu-info-card-designer` | 信息卡片 | 40% | → 合并 |
| `ascii-art` | ASCII 艺术 | 20% | ✅ 独立 |
| `image-generator` | 图片生成 | 30% | ✅ 独立 |

**整合后**:
```
visual-designer/
├── SKILL.md (主入口)
├── charts/ (图表)
│   ├── ppt.py
│   └── markdown.py
├── cards/ (卡片)
│   ├── info_card.py
│   └── magazine_style.py
└── art/ (艺术)
    ├── ascii.py
    └── ai_image.py
```

---

### P1 - 中重复风险 (本周整合)

#### 6. CLI 工具集 (8 技能)

| 技能 | 功能 | 整合方案 |
|------|------|---------|
| `aws-cli` | AWS 命令行 | → cli-toolkit 子模块 |
| `azure-cli` | Azure 命令行 | → cli-toolkit 子模块 |
| `gcp-cli` | GCP 命令行 | → cli-toolkit 子模块 |
| `docker-ctl` | Docker 控制 | → cli-toolkit 子模块 |
| `k8s-deploy` | K8s 部署 | → cli-toolkit 子模块 |
| `git-integration` | Git 集成 | ✅ 独立保留 |
| `gemini-cli` | Gemini CLI | ✅ 独立保留 |
| `jimeng-cli` | 即梦 CLI | ✅ 独立保留 |

**整合后**:
```
cli-toolkit/
├── SKILL.md (主入口)
├── cloud/
│   ├── aws.py
│   ├── azure.py
│   └── gcp.py
├── devops/
│   ├── docker.py
│   └── k8s.py
└── wrappers/ (独立 CLI 包装)
    ├── gemini.py
    └── jimeng.py
```

---

#### 7. 监控告警 (5 技能)

| 技能 | 功能 | 整合方案 |
|------|------|---------|
| `api-monitor` | API 监控 | → monitoring 子模块 |
| `polyalert` | Polymarket 告警 | → monitoring 子模块 |
| `self-check` | 自检 | → monitoring 子模块 |
| `upgrade-guard` | 升级守卫 | → monitoring 子模块 |
| `yi-alert` | 羿信号 | ✅ 独立 (Bot 专属) |

**整合后**:
```
monitoring/
├── SKILL.md (主入口)
├── api_monitor.py
├── alert_engine.py
├── self_check.py
└── upgrade_guard.py
```

---

#### 8. 金融交易 (6 技能)

| 技能 | 功能 | 整合方案 |
|------|------|---------|
| `binance-trader` | 币安交易 | → trading 子模块 |
| `polymarket` | Polymarket | → trading 子模块 |
| `zhiji` | 知几策略 | ✅ 独立 (Bot 专属) |
| `zhiji-sentiment` | 情绪分析 | → zhiji 子模块 |
| `torchtrade-integration` | TorchTrade | → trading 子模块 |
| `portfolio-tracker` | 组合追踪 | ✅ 独立 |

**整合后**:
```
trading/
├── SKILL.md (主入口)
├── binance/
│   ├── client.py
│   └── strategies.py
├── polymarket/
│   ├── client.py
│   └── strategies.py
└── torchtrade/
    └── integration.py
```

---

### P2 - 低重复风险 (本月优化)

#### 9. 工具技能 (10 技能)

| 技能 | 功能 | 状态 |
|------|------|------|
| `feishu` | 飞书集成 | ✅ 独立 |
| `ssh` | SSH 远程 | ✅ 独立 |
| `tts` | 语音合成 | ✅ 独立 |
| `weather` | 天气查询 | ✅ 独立 |
| `news-fetcher` | 新闻获取 | ✅ 独立 |
| `unsplash-image` | 图片搜索 | ✅ 独立 |
| `coingecko-price` | 币价查询 | ✅ 独立 |
| `alpha-vantage` | 股票数据 | ✅ 独立 |
| `public-apis-index` | API 索引 | ✅ 独立 |
| `webhook-relay` | Webhook 中继 | ✅ 独立 |

**决策**: 保持独立，功能清晰无重复

---

## 🏗️ 新架构设计

### 三层技能架构

```
┌─────────────────────────────────────────────────┐
│  Layer 1: Bot 专属技能 (8 个)                      │
│  太一/知几/山木/素问/罔两/庖丁/羿/守藏吏            │
│  特点：职责清晰 · 独立接口 · 不合并               │
└─────────────────────────────────────────────────┘
              ↓ 调用
┌─────────────────────────────────────────────────┐
│  Layer 2: 通用技能 (~40 个)                       │
│  整合后：browser/gmgn/content/visual/cli/...     │
│  特点：模块化 · 共享底层 · 智能路由               │
└─────────────────────────────────────────────────┘
              ↓ 依赖
┌─────────────────────────────────────────────────┐
│  Layer 3: 工具技能 (~20 个)                       │
│  独立工具：feishu/ssh/tts/weather/...            │
│  特点：单一功能 · 零依赖 · 即插即用               │
└─────────────────────────────────────────────────┘
```

---

## 🔌 互联互通机制

### 1. 共享数据层

**位置**: `skills/shared/`

```python
# skills/shared/database.py
class SharedDatabase:
    """所有技能共享的数据库连接"""
    _instance = None
    
    def __init__(self):
        self.db = sqlite3.connect('~/.openclaw/shared.db')
    
    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = SharedDatabase()
        return cls._instance

# skills/shared/cache.py
class SharedCache:
    """所有技能共享的缓存层"""
    def __init__(self):
        self.cache = {}
    
    def get(self, key):
        return self.cache.get(key)
    
    def set(self, key, value, ttl=3600):
        self.cache[key] = {
            'value': value,
            'expires': time.time() + ttl
        }
```

---

### 2. 事件总线

**位置**: `skills/shared/event_bus.py`

```python
class EventBus:
    """技能间事件驱动通信"""
    _instance = None
    
    def __init__(self):
        self.subscribers = {}
    
    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
    
    def publish(self, event_type, data):
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(data)

# 使用示例
# 技能 A 发布事件
event_bus.publish('data.updated', {'table': 'users', 'id': 123})

# 技能 B 订阅事件
event_bus.subscribe('data.updated', lambda data: refresh_cache(data))
```

---

### 3. 统一配置中心

**位置**: `skills/shared/config.py`

```python
class SharedConfig:
    """所有技能共享的配置"""
    def __init__(self):
        self.config = self._load_config()
    
    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    def set(self, key, value):
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

# 使用示例
config = SharedConfig()
api_key = config.get('gemini.api_key')
config.set('gmgn.wallet.solana', '5C1bQnC9wSnVUbzUsXPNQ8eB6VvmYPx6DvQrvvbw9zCq')
```

---

## 🤖 智能路由引擎

### 位置：`skills/smart-router/`

```python
class SmartRouter:
    """智能技能路由引擎"""
    
    def __init__(self):
        self.skills = self._discover_skills()
        self.usage_stats = self._load_usage_stats()
    
    def route(self, task_description):
        """根据任务描述自动选择技能"""
        # 1. 语义分析
        intent = self._analyze_intent(task_description)
        
        # 2. 技能匹配
        candidates = self._match_skills(intent)
        
        # 3. 成本优化
        best_skill = self._optimize_cost(candidates)
        
        # 4. 执行路由
        return self._execute(best_skill, task_description)
    
    def _analyze_intent(self, description):
        """分析用户意图"""
        # 使用本地模型快速分类
        from skills.smart_model_router import call_local_model
        
        prompt = f"""
        分析以下任务的意图，返回 JSON：
        {{
          "category": "browser|trading|content|visual|cli|...",
          "complexity": "easy|medium|hard",
          "estimated_tokens": 1000,
          "preferred_model": "local|cloud"
        }}
        
        任务：{description}
        """
        
        response = call_local_model(prompt)
        return json.loads(response)
    
    def _match_skills(self, intent):
        """匹配候选技能"""
        matches = []
        for skill_name, skill_meta in self.skills.items():
            if skill_meta['category'] == intent['category']:
                score = self._calculate_match_score(skill_meta, intent)
                matches.append((skill_name, score))
        
        return sorted(matches, key=lambda x: x[1], reverse=True)
    
    def _optimize_cost(self, candidates):
        """成本优化选择"""
        best = None
        best_score = -1
        
        for skill_name, score in candidates:
            # 考虑：匹配度 + 历史成功率 + 成本 + 速度
            success_rate = self.usage_stats.get(skill_name, {}).get('success_rate', 0.5)
            avg_cost = self.usage_stats.get(skill_name, {}).get('avg_cost', 0)
            avg_time = self.usage_stats.get(skill_name, {}).get('avg_time', 10)
            
            composite_score = (
                score * 0.4 +           # 匹配度 40%
                success_rate * 0.3 +     # 成功率 30%
                (1 - avg_cost/10) * 0.2 + # 成本 20%
                (1 - avg_time/60) * 0.1   # 速度 10%
            )
            
            if composite_score > best_score:
                best_score = composite_score
                best = skill_name
        
        return best
```

---

## 📋 整合执行计划

### P0 - 本周执行 (2026-04-07 至 2026-04-13)

| 任务 | 负责 | 产出 | 验收 |
|------|------|------|------|
| **browser-automation 整合** | 素问 | 统一浏览器模块 | 3 技能→1 技能 |
| **smart-model-router 整合** | 素问 | 统一模型路由 | 4 技能→1 技能 |
| **gmgn 整合** | 知几 | 统一 GMGN 模块 | 6 技能→2 技能 |
| **content-creator 整合** | 山木 | 统一内容创作 | 5 技能→1 技能 |
| **visual-designer 整合** | 山木 | 统一视觉设计 | 4 技能→1 技能 |
| **shared 共享层创建** | 素问 | 数据库/缓存/事件总线 | 3 个共享模块 |
| **smart-router 路由引擎** | 太一 | 智能路由核心 | 自动选择技能 |

**目标**: 121 技能 → 85 技能 (减少 30%)

---

### P1 - 下周执行 (2026-04-14 至 2026-04-20)

| 任务 | 负责 | 产出 | 验收 |
|------|------|------|------|
| **cli-toolkit 整合** | 素问 | 统一 CLI 工具集 | 8 技能→3 技能 |
| **monitoring 整合** | 羿 | 统一监控告警 | 5 技能→1 技能 |
| **trading 整合** | 知几 | 统一交易模块 | 6 技能→3 技能 |
| **技能注册表** | 太一 | skills/registry.yaml | 自动发现技能 |
| **路由测试** | 太一 | 100 次路由测试 | 命中率 >95% |

**目标**: 85 技能 → 65 技能 (累计减少 46%)

---

### P2 - 本月优化 (2026-04-21 至 2026-04-30)

| 任务 | 负责 | 产出 | 验收 |
|------|------|------|------|
| **文档完善** | 山木 | 技能使用手册 | 每个技能 README |
| **性能优化** | 素问 | 技能调用延迟 <100ms | 性能报告 |
| **自动化测试** | 素问 | 技能测试覆盖率 >80% | 测试报告 |
| **技能市场** | 罔两 | 技能上架流程 | 3 个付费技能 |

**目标**: 65 技能 → 60 技能 (累计减少 50%)

---

## 📊 验收标准

### 功能性验收

| 指标 | 基线 | 目标 | 验收 |
|------|------|------|------|
| **技能数量** | 121 | 60 | 减少 50% |
| **重复率** | ~30% | <5% | 代码审计 |
| **调用延迟** | ~200ms | <100ms | 性能测试 |
| **路由命中率** | N/A | >95% | 100 次测试 |

---

### 独立性验收

| 检查项 | 标准 | 验收方式 |
|--------|------|---------|
| **单一职责** | 每个技能只做一件事 | 代码审查 |
| **接口清晰** | 输入输出明确定义 | SKILL.md 检查 |
| **无循环依赖** | 依赖图无环 | 静态分析 |
| **可独立测试** | 单元测试覆盖率>80% | 测试报告 |

---

### 互联互通验收

| 检查项 | 标准 | 验收方式 |
|--------|------|---------|
| **共享数据层** | 所有技能使用统一 DB | 代码审查 |
| **事件总线** | 跨技能事件驱动 | 集成测试 |
| **配置中心** | 统一配置管理 | 配置审计 |
| **智能路由** | 自动选择最优技能 | 路由测试 |

---

## 🔧 迁移指南

### 技能整合流程

```bash
# 1. 备份原技能
cp -r skills/browser-automation skills/.backup/
cp -r skills/browser-adapter skills/.backup/
cp -r skills/geo-automation skills/.backup/

# 2. 创建新结构
mkdir -p skills/browser-automation/{core,adapters,utils}

# 3. 迁移代码
mv skills/browser-automation/*.py skills/browser-automation/core/
mv skills/browser-adapter/*.py skills/browser-automation/adapters/

# 4. 更新 SKILL.md
# 编辑 skills/browser-automation/SKILL.md

# 5. 测试验证
python3 -m pytest skills/browser-automation/tests/

# 6. 更新注册表
python3 scripts/update-skill-registry.py
```

---

### 兼容性保障

```python
# skills/shared/compatibility.py
class CompatibilityLayer:
    """旧技能 API 兼容层"""
    
    @staticmethod
    def browser_automation_call(func_name, *args, **kwargs):
        """兼容旧 browser-automation 调用"""
        from skills.browser_automation.core import PlaywrightWrapper
        
        wrapper = PlaywrightWrapper()
        return getattr(wrapper, func_name)(*args, **kwargs)
    
    @staticmethod
    def smart_ai_router_call(model, prompt):
        """兼容旧 smart_ai_router 调用"""
        from skills.smart_model_router import route_request
        
        return route_request(model, prompt)
```

---

## 📈 预期收益

### 效率提升

| 指标 | 提升 | 说明 |
|------|------|------|
| **技能查找** | 60% 更快 | 智能路由自动选择 |
| **代码复用** | 50% 提升 | 共享底层模块 |
| **维护成本** | 40% 降低 | 减少重复代码 |
| **新功能开发** | 30% 加速 | 复用现有模块 |

---

### 成本优化

| 项目 | 基线 | 目标 | 节省 |
|------|------|------|------|
| **技能数量** | 121 | 60 | 50% |
| **重复代码** | ~30% | <5% | 83% |
| **调用延迟** | ~200ms | <100ms | 50% |
| **维护时间** | 10h/周 | 6h/周 | 40% |

---

## 🎯 智能自动化响应

### 任务自动路由示例

**用户请求**: "帮我分析一下 Polymarket 上的气象市场，然后生成一份研报发到小红书"

**智能路由流程**:

```python
# 1. 意图分析
intent = router.analyze_intent(user_request)
# {
#   "steps": [
#     {"type": "data_fetch", "source": "polymarket"},
#     {"type": "analysis", "method": "sentiment"},
#     {"type": "report_generation", "style": "professional"},
#     {"type": "publish", "platform": "xiaohongshu"}
#   ]
# }

# 2. 技能选择
skills_needed = [
    'polymarket',          # 数据获取
    'zhiji-sentiment',     # 情绪分析
    'shanmu-reporter',     # 研报生成
    'social-publisher'     # 发布到小红书
]

# 3. 自动执行
results = []
for skill in skills_needed:
    result = router.execute(skill, previous_results)
    results.append(result)

# 4. 返回结果
return results[-1]  # 发布成功
```

---

### 跨技能协作示例

**场景**: 知几-E 策略执行

```python
# 知几-E 自动调用多个技能
class ZhijiE:
    def __init__(self):
        self.polymarket = Skills.get('polymarket')
        self.sentiment = Skills.get('zhiji-sentiment')
        self.timesfm = Skills.get('timesfm-forecast')
        self.database = SharedDatabase.get_instance()
        self.event_bus = EventBus.get_instance()
    
    def execute_strategy(self, market_id):
        # 1. 获取市场数据
        market_data = self.polymarket.get_market(market_id)
        
        # 2. 情绪分析
        sentiment = self.sentiment.analyze(market_data['description'])
        
        # 3. 气象预测
        forecast = self.timesfm.forecast(market_data['resolution_source'])
        
        # 4. 综合决策
        decision = self._make_decision(market_data, sentiment, forecast)
        
        # 5. 发布事件 (其他技能可订阅)
        self.event_bus.publish('zhiji.decision', {
            'market_id': market_id,
            'decision': decision
        })
        
        return decision
```

---

## 📄 相关文件

| 文件 | 用途 | 状态 |
|------|------|------|
| `skills/README.md` | 技能库总览 | ✅ 待更新 |
| `skills/registry.yaml` | 技能注册表 | ✅ 待创建 |
| `skills/shared/` | 共享模块 | ✅ 待创建 |
| `skills/smart-router/` | 智能路由 | ✅ 待创建 |
| `docs/skill-integration-guide.md` | 整合指南 | ✅ 待创建 |

---

## 🚀 立即执行

### P0 任务分解

| 任务 | 开始时间 | 预计完成 | 负责人 |
|------|---------|---------|--------|
| browser-automation 整合 | 2026-04-07 00:00 | 2026-04-07 02:00 | 素问 |
| smart-model-router 整合 | 2026-04-07 02:00 | 2026-04-07 04:00 | 素问 |
| gmgn 整合 | 2026-04-07 04:00 | 2026-04-07 06:00 | 知几 |
| shared 共享层创建 | 2026-04-07 06:00 | 2026-04-07 08:00 | 素问 |
| smart-router 路由引擎 | 2026-04-07 08:00 | 2026-04-07 10:00 | 太一 |

**晨会检查**: 2026-04-07 06:00 (宪法学习时间)

---

*版本：v4.0 | 创建时间：2026-04-07 00:00 | 状态：✅ 激活*

*「独立职责 · 互联互通 · 零重复 · 智能路由」*

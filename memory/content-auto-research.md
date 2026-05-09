# 内容自动化增强方案研究

> 调研时间：2026-05-09 07:17
> 调研主题：Luma Agents (创意广告生成) + Perplexity Agent Skill 构建方法论 → 赋能 geo-outbound 模块

---

## 调研摘要

对 Luma Agents 的创意工作流架构和 Perplexity 的 Agent Skill 内部手册进行了深度分析，提炼出可直接注入 geo-outbound 模块的内容自动化增强方案。

---

## 一、Luma Agents — 创意广告生成能力

### 1. 核心定位
Luma Agents（2026年3月发布）是一个**统一多模态创意协作系统**，而非单纯的视频生成工具。它能端到端执行创意工作：从brief到交付，跨文本/图像/视频/音频。

### 2. 三层架构

| 层 | 功能 | 对应 geo-outbound 启示 |
|---|---|---|
| **Project Organization** | 可视化 Board 组织创意项目，资产/版本/探索分组对比，语义搜索 | → 内容素材库→Board化组织+版本管理 |
| **Creative Agents** | 自然语言驱动执行，路由多模型，保持项目上下文记忆 | → 开发信生成Agent+多模型支持 |
| **Capabilities** | 编排业界领先 GenAI 模型（Ray/Veo/Kling/Uni-1/Seedream等） | → 多LLM后端的封装层 |

### 3. 关键能力
- **视频广告生成**：Text-to-Video / Image-to-Video / 关键帧插值
- **图像广告**：照片级生成 / 风格化插画 / Outpainting / HDR编辑
- **音频**：音效生成 / 音乐 / 情感化配音 / 词级转写
- **Lip Sync**：音频对口型 + 表情控制 + 角色动画
- **合成**：程序化编辑视频和运动元素/字幕/过渡/合成

### 4. 对 geo-outbound 的启发
1. **统一 Board 架构** → 重构 ContentMaterialLibrary 为 Board 模式，支持多版本/多格式资产追溯
2. **上下文持续记忆** → 开发信生成保留回合上下文（产品规格→定制话术→多轮优化）
3. **模型编排层** → 解耦 LLM 调用，支持 A/B 测试不同模型输出效果
4. **多模态资产生成** → 视频广告+产品展示+语音解说 一站式 Pipeline

---

## 二、Perplexity Agent Skill 构建方法论

### 1. 核心发现：Skill ≠ 传统代码

Perplexity 明确指出：**Skill 是上下文，不是软件**。传统软件工程的许多最佳实践（Simple/Explicit/Sparse/Special Cases/Easy to Explain）在 Skill 构建中是反模式。

### 2. Skill 四大属性

| 属性 | 含义 | geo-outbound 应用 |
|---|---|---|
| **Skill is a Directory** | 不是单SKILL.md，而是hub-and-spoke文件夹结构（SKILL.md + scripts/ + references/ + assets/ + config.json） | → 每个内容品类一个Skill目录 |
| **Skill is a Format** | 严格的frontmatter：name + description（路由触发词，非内部文档） | → 开发信模板标准化frontmatter |
| **Skill is Invocable** | 按需加载，渐进式注入，三层context成本模型 | → 内容模块按场景条件加载 |
| **Skill is Progressive** | Index(100tok/Skill) → Load(5000tok) → Runtime(unbounded) | → 内容素材三级预算控制 |

### 3. 三层 Context 成本模型

| 层级 | 预算 | 何时付 | geo-outbound 对应 |
|---|---|---|---|
| **Index** | ~100 tok/Skill | 每个 session，每个用户，一直付 | → 内容品类索引（简短、精准） |
| **Load** | ~5000 tok | 当 Skill 被加载时 | → 开发信/社媒模板全内容 |
| **Runtime** | 不限 | 仅当 agent 读取时 | → 产品规格/FAQ/条件分支 |

### 4. Skill 构建五步法

| 步骤 | 操作 | geo-outbound 改造 |
|---|---|---|
| **Step 0: Evals** | 先写评测：真实用户查询/已知失败/领域边界混淆 | → 开发信生成评估集（A/B测试基座） |
| **Step 1: Description** | 最难的一行。"Load when..." 是路由触发器，不是文档 | → 内容类型路由描述（精准触发） |
| **Step 2: Body** | 跳过显而易见的（模型已会的），专注 gotchas/负例 | → 开发信规则：仅写文化禁忌/法规红线 |
| **Step 3: Hierarchy** | 条件性/沉重内容放到 spoke 文件 | → scripts/ → 脚本化模板变量填充 |
| **Step 4: Iterate** | 分支迭代，积累 hero query 集 | → A/B测试流程 + 效果回传 |
| **Step 5: Ship** | 带评测集的一次性提交 | → 内容模板版本发布流程 |

### 5. Gotchas 飞轮（核心维护机制）

```
Agent 失败 → 添加一条 gotcha
Agent 错误加载 → 收紧 description + 添加负例 eval
Agent 应加载未加载 → 添加关键词 + 正例 eval
System Prompt 变化 → 检查冲突或重复
```

**关键洞察**：Skills 是 append-mostly（主要追加）。gotchas 区域是随时间积累价值最高的部分，比指令更改更安全。

### 6. Eval Suites 体系

| 评测类型 | 检查内容 | geo-outbound 对应 |
|---|---|---|
| Skill Loading | 精度/召回/禁止检查 | → 内容类型路由精度测试 |
| Progressive Loading | 是否读取附属文件 | → 多级模板加载验证 |
| End-to-End Domain | LLM Judge + 评分标准 | → 开发信/社媒AB测试自动化判断 |

---

## 三、增强方案：geo-outbound 内容自动化升级

### 3.1 模块改动说明

#### 当前架构问题
1. `core.py` execute() 是粗粒度任务分发，缺乏内容品类路由
2. `self_media_engine.py` 是独立 JSON 存储，缺乏 Skill 式渐进加载
3. 内容生成全是硬编码模板，无 gotchas 机制
4. 无 A/B 测试框架
5. 无评测集和自动反馈闭环

#### 目标架构

```
geo-outbound/
├── core.py                          # 增强：Skill 式渐进加载 + 三层 budget
├── config.json                      # 增强：品类路由配置 + model routing
├── content/
│   ├── __init__.py
│   ├── skill_engine.py              # [NEW] Skill 式内容引擎
│   ├── skill_index.json             # [NEW] 内容品类索引（~100 tok/条）
│   ├── cold_email/
│   │   ├── SKILL.md                 # [NEW] 开发信 Skill（frontmatter + gotchas）
│   │   ├── scripts/
│   │   │   └── template_filler.py   # [MOVE] 模板变量填充
│   │   ├── references/
│   │   │   ├── CULTURAL_TABOOS.md   # [NEW] 文化禁忌（条件加载）
│   │   │   └── REGULATIONS.md      # [NEW] 法规红线（条件加载）
│   │   └── assets/
│   │       ├── templates/           # [MOVE] 多版本模板
│   │       └── ab_test_results/     # [NEW] A/B 结果集
│   ├── linkedin/
│   │   └── ...                      # 同上结构
│   ├── self_media/                  # 增强：Skill 式渐进
│   │   └── ...
│   ├── video_ads/                   # [NEW] Luma 集成层
│   │   └── SKILL.md + scripts/
│   └── ab_test/
│       ├── evaluator.py             # [NEW] LLM Judge 评测
│       └── test_suites/             # [NEW] 评测集
├── earned_media_data/
│   └── ...
└── monitor/
    └── gotchas_flywheel.py          # [NEW] Gotchas 飞轮
```

### 3.2 关键代码逻辑

#### 3.2.1 Skill Index 路由引擎（skill_index.json）

```json
{
  "skills": [
    {
      "name": "cold-email",
      "description": "Load when writing cold outreach emails for cross-border trade prospects. Triggers: 'write email', 'draft outreach', '开发信', 'cold email'",
      "budget_index": 95,
      "budget_load": 4800,
      "depends": ["cross-border-core"]
    },
    {
      "name": "linkedin-content",
      "description": "Load when generating LinkedIn posts for B2B trade. Triggers: 'linkedin post', '社媒内容', 'professional content'",
      "budget_index": 98,
      "budget_load": 3200,
      "depends": []
    }
  ]
}
```

#### 3.2.2 Skill 引擎核心逻辑（skill_engine.py）

```python
class SkillEngine:
    """Skill 式内容引擎 - 借鉴 Perplexity 三层 Context 模型"""
    
    TIER_INDEX = 1    # ~100 tok/skill，所有 session 一直付
    TIER_LOAD = 2     # ~5000 tok，加载时付
    TIER_RUNTIME = 3  # 不限，仅条件读取时付
    
    def __init__(self, skill_index_path: str):
        self.skill_index = self._load_index(skill_index_path)
        self.gotchas = self._load_gotchas()
        self.evals = EvalSuite()
    
    def route(self, intent: str, context: Dict) -> Optional[str]:
        """Step 1: 品类路由 - 基于 description 匹配"""
        # 使用 embedding 相似度或关键词匹配
        matched = self._match_skill(intent, self.skill_index)
        return matched.name if matched else None
    
    def load_skill(self, name: str) -> Dict:
        """Step 2: 加载 Skill Body（付 Load tier 成本）"""
        skill_dir = self._resolve_skill_dir(name)
        skill_md = self._read_skill_md(skill_dir / "SKILL.md")
        # 剥离 frontmatter（路由信息不注入 context）
        body = self._strip_frontmatter(skill_md)
        # 注入 gotchas
        gotchas = self.gotchas.get(name, [])
        return {
            "body": body,
            "gotchas": gotchas,
            "scripts": skill_dir / "scripts",
            "references": {},
            "loaded": True
        }
    
    def load_reference(self, skill_name: str, ref_name: str) -> str:
        """Step 3: Runtime 条件加载（仅付 tier=3 成本）"""
        ref_path = self._resolve_skill_dir(skill_name) / "references" / ref_name
        return ref_path.read_text() if ref_path.exists() else ""

class EvalSuite:
    """评测集 - Step 0 先行"""
    
    def __init__(self):
        self.test_cases = []
    
    def add_positive(self, intent: str, expected_skill: str):
        """正例：应该路由到的 Skill"""
        self.test_cases.append(("positive", intent, expected_skill))
    
    def add_negative(self, intent: str, forbidden_skills: List[str]):
        """负例：不应该路由到的 Skill"""
        self.test_cases.append(("negative", intent, forbidden_skills))
    
    def run(self, engine: SkillEngine) -> Dict:
        results = {"precision": 0, "recall": 0, "errors": []}
        for case_type, intent, expected in self.test_cases:
            result = engine.route(intent, {})
            if case_type == "positive" and result != expected:
                results["errors"].append(f"Expected {expected}, got {result}")
            elif case_type == "negative" and result in expected:
                results["errors"].append(f"Should not route to {result}")
        results["precision"] = 1 - len(results["errors"]) / len(self.test_cases)
        return results

class GotchasFlywheel:
    """Gotchas 飞轮 - append-mostly 维护"""
    
    def __init__(self, gotchas_path: str):
        self.gotchas = self._load(gotchas_path)
    
    def record_failure(self, skill_name: str, failure: Dict):
        """每次 Agent 失败 → 添加一条 gotcha"""
        gotcha = {
            "trigger": failure.get("input"),
            "failure": failure.get("output"),
            "correction": failure.get("expected"),
            "added_at": datetime.now().isoformat()
        }
        self.gotchas.setdefault(skill_name, []).append(gotcha)
        self._save()
    
    def tighten_description(self, skill_name: str, negative_examples: List[str]):
        """Agent 错误加载 → 收紧 description + 添加负例"""
        pass
```

#### 3.2.3 Cold Email Skill 模板示例（SKILL.md）

```markdown
---
name: cold-email
description: >
  Load when writing cold outreach emails for cross-border trade prospects.
  Triggers: "write email", "draft outreach", "开发信", "cold email",
  "初接触", "开发客户信". Do NOT load for reply emails or follow-ups.
depends: ["cross-border-core"]
metadata:
  tier: "load"
  budget: 4800
---

## 开发信生成规则

### 禁止（Gotchas — 不断追加）
- ❌ 第一句就推销产品
- ❌ 使用中文式礼貌用语 "如有打扰请谅解"
- ❌ 在邮件中包含附件（第一次接触）
- ❌ 使用 "Dear Sir/Madam"（缺乏个性化）
- ❌ 提及价格（除非客户主动问）
- ❌ 超过 150 字（B2B 决策者注意力）

### 必做
- ✅ 第一句：证明你研究过客户
  > "I noticed {company} has been expanding into {market}..."
- ✅ 第二句：价值主张（非产品描述）
  > "We help companies like yours reduce {pain_point} by {metric}."
- ✅ CTA：给出低承诺选项
  > "Is it worth a 10-min call to see if this fits?"
- ✅ PS: 行业洞察/链接（展现专业度）

### 多版本生成（A/B 测试支持）
- Version A：问题导向（"Are you struggling with...")
- Version B：洞察导向（"I noticed a trend in {industry}...")
- Version C：价值导向（"We helped {similar_company} achieve...")

### 模板填充
参见 scripts/template_filler.py
```

#### 3.2.4 Luma 集成层（video_ads/SKILL.md）

```markdown
---
name: video-ad-generation
description: >
  Load when needing to generate product showcase videos or video ads.
  Triggers: "video ad", "产品视频", "广告片", "showcase video",
  "YouTube ad", "社媒视频素材"
depends: []
---

## 视频广告生成流程

### 输入
- 产品图片/规格/描述
- 目标市场（国家/文化）
- 广告形式（LinkedIn Video / YouTube / TikTok）

### 输出
- 30-60秒产品展示视频
- 字幕文件（多语言可选）
- 语音配音（情感控制）
- 关键帧概览

### 编排模型
- 脚本生成：首选 LLM（qwen3.5-plus / claude）
- 语音合成：Luma Audio（emotional voiceover）
- 视频主体：Luma / Ray / Veo（按效果选择）
- 字幕合成：程序化合成模块
- Lip Sync（如有角色）：Luma Lip Sync

### A/B 测试指标
- 完播率 > 30% 为合格
- 点击率 > 2% 为优秀
- 第5秒留存 > 70% 为合格
```

### 3.3 A/B 测试自动化流程

借鉴 Perplexity evals + Luma 持续迭代思想：

```
[输入内容模板种类]
    │
    ├─ Version A（问题导向/30字/配图）
    ├─ Version B（洞察导向/50字/配图）
    └─ Version C（价值导向/40字/无图）
    │
    ├─ ▶ 分批发发送
    │
    ├─ 24h 后回采数据
    │   ├─ 打开率
    │   ├─ 回复率
    │   └─ 转化率
    │
    ├─ LLM Judge 自动判断胜者
    │   └─ 写入 Gotchas（负例）+ 模板权重调整
    │
    └─ 下一轮：胜者 + 变体 × 2
```

关键类：

```python
class ABTestManager:
    def __init__(self):
        self.test_id = None
        self.variants = []
        self.winner = None
    
    def create_test(self, skill_name: str, templates: Dict, split: str = "even"):
        """创建 A/B 测试"""
        self.test_id = f"AB_{skill_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.variants = [
            {"id": k, "template": v, "sent": 0, "opens": 0, "replies": 0}
            for k, v in templates.items()
        ]
    
    async def run(self, send_fn, prospects: List[Dict], batch_size: int = 20):
        """分批发送 + 自动暂停表现差的变体"""
        # 第1批：均发
        # 第2批：按打开率权重分配
        # 第3批：淘汰低于阈值的变体
    
    def evaluate(self, judge_model: str = "auto") -> Dict:
        """LLM Judge 评估胜者"""
        prompt = f"""
        分析以下 A/B 测试结果：
        Variant A: opens={self.variants[0].opens}, replies={self.variants[0].replies}
        Variant B: opens={self.variants[1].opens}, replies={self.variants[1].replies}
        
        1. 哪个变体胜出？为什么？
        2. 有哪些模式值得固化到 gotchas？
        3. 建议下一轮变体方向。
        """
        # 调用 LLM Judge
        ...
```

### 3.4 自演进闭环

```
对geo-outbound的深度改造：

┌─────────────────────────────────────────────────┐
│                  数据回流层                       │
│  (回复率/打开率/转化率)                          │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│            Gotchas 飞轮 (append-mostly)           │
│  "回复中客户问价格→加 gotcha: 价格在第三轮再谈"    │
│  "LinkedIn 发周一没人看→加 gotcha: 周三/四发"     │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│            Skill 路由优化 (description 微调)       │
│  正例evals + 负例evals 持续积累                   │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│            内容模板版本迭代                        │
│  SKILL.md + scripts/ 渐进式更新                   │
└─────────────────────────────────────────────────┘
```

---

## 四、执行计划

### Phase 1: 基础设施搭建（1周）
- [ ] 创建 `content/skill_engine.py`（Skill 路由 + 三层 Budget）
- [ ] 创建 `content/skill_index.json`（品类索引）
- [ ] 创建 `content/ab_test/evaluator.py`（LLM Judge 评测器）
- [ ] 创建 `monitor/gotchas_flywheel.py`（Gotchas 飞轮）

### Phase 2: 品类 Skill 改造（2周）
- [ ] 重构 `cold-email` 为 Skill 目录结构（SKILL.md + scripts/ + references/ + assets/）
- [ ] 重构 `linkedin-content` 为 Skill 目录结构
- [ ] 重构 `self-media` 为 Skill 目录结构
- [ ] 将所有硬编码模板迁移到 `assets/templates/`

### Phase 3: A/B 测试集成（1周）
- [ ] `ABTestManager` 创建/分发/评估全流程
- [ ] 数据回流 → Gotchas 飞轮自动写入
- [ ] A/B 结果可视化（report 模块）

### Phase 4: Luma 视频广告层（2周，按需）
- [ ] `content/video_ads/SKILL.md` + scripts
- [ ] Luma API 集成封装
- [ ] 视频广告 → 社媒自动发布 Pipeline

### Phase 5: 评测体系（持续）
- [ ] 每周运行 EvalSuite 检查路由精度
- [ ] 每月 review Gotchas 积累
- [ ] 季度 Skill 重构（删除无用，合并重叠）

---

## 五、预计工作量

| 阶段 | 工程工作量 | 文案工作量 | 风险等级 |
|------|-----------|-----------|---------|
| Phase 1 基础设施 | 3人日 | 0 | 低 |
| Phase 2 品类改造 | 4人日 | 4人日 | 中 |
| Phase 3 A/B 集成 | 2人日 | 1人日 | 中 |
| Phase 4 视频层 | 5人日 | 3人日 | 高（依赖Luma API稳定） |
| Phase 5 持续 | 0.5人日/周 | 1人日/月 | 低 |

**总计首期（Phase 1-3）：** 14人日（工程）
**文案素材准备：** 5人日（行业知识+文化禁忌+gotchas）

---

## 六、关键发现总结

### 从 Perplexity 学到的最重要三件事

1. **Skill ≠ 代码**：传统软件工程的"简单优于复杂"在 Skill 中是反模式。Skill 的复杂度就是功能。
2. **Description 是最难的一行**：它是路由触发器，不是功能说明。"Load when..." 格式 + 50字上限。
3. **Gotchas 飞轮 > 指令修改**：持续追加失败案例 → 比重写指令更安全、副作用更小。

### 从 Luma 学到的最重要三件事

1. **统一 Board 替代散落文件**：多模态资产在同一上下文下迭代，避免"切换工具"的信息断裂。
2. **模型编排层**：不让业务代码直接依赖某个模型，而是通过编排层交换模型。
3. **持续上下文记忆**：创意工作不是单次生成，而是多轮迭代，需要跨回合记忆。

### 对 geo-outbound 的直接影响

| 问题点 | 增强前 | 增强后 |
|--------|--------|--------|
| 内容品类路由 | 无（全量加载） | Skill Index 渐进加载 |
| 开发信质量 | 硬编码模板 | Gotchas 飞轮 + 文化禁忌条件加载 |
| A/B 测试 | 无 | ABTestManager + LLM Judge |
| 模板维护 | 直接改代码 | SKILL.md append-mostly |
| 评测 | 无 | EvalSuite 双周跑 |
| 视频广告 | 不支持 | Luma 编排层可选 |

---

*更新：2026-05-09 07:17*
*来源：Luma Agents 官方文档 + Perplexity Research Blog "Designing, Refining, and Maintaining Agent Skills at Perplexity"*

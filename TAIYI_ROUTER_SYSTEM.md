# 🧠 太一智能路由系统

> **版本**: v1.0
> **生成时间**: 2026-05-04
> **作者**: 太一 AGI
> **定位**: 太一系统智能路由中枢

---

## 📐 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    太一智能路由系统 (Taiyi Router)                  │
│                         三级加载 + 模型调度                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      Tier 1 · 永久核 (强制加载)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ 价值基石    │  │ 数据真实    │  │ 验证优先    │             │
│  │ VALUE       │  │ TRUTH-DATA  │  │ VERIFICATION│             │
│  │ FOUNDATION  │  │             │  │ FIRST       │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ 负熵法则    │  │ 观察者协议  │  │ AGI时间线   │             │
│  │ NEGENTROPY  │  │ OBSERVER    │  │ AGI-TIMELINE│             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ 自驱动闭环  │  │ 美学法则    │  │ 智能分离    │             │
│  │ SELF-LOOP   │  │ AESTHETICS  │  │ TURBOQUANT  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              模型调度协议 (MODEL-ROUTING)                  │   │
│  │  默认: qwen3.5-plus │ 代码: qwen3-coder │ 长文: Gemini   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Tier 2 · 上下文激活 (按需加载)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  分析/判断/决策 ──────→ directives/ELON-FRAMEWORK.md             │
│  理解动机/对话 ───────→ skills/PSYCHOLOGY.md                     │
│  接入新模块 ──────────→ quality-gates/DISTILLATION.md            │
│  成果输出 ────────────→ workflows/OUTPUT-VERIFICATION.md         │
│  编码/开发 ───────────→ directives/KARPATHY-CODING.md            │
│  CLI/终端 ────────────→ directives/RTK-TOKEN-EFFICIENCY.md       │
│  爬虫/数据采集 ───────→ skills/ANTI_SCRAPING_CONSTITUTION.md     │
│  软件安装/新增 ───────→ security/SOFTWARE-INSTALL-SECURITY.md    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Tier 3 · 热插拔 (按需激活)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  extensions/ 下新模块自动发现                                     │
│  激活命令: sed -i 's/enabled: false/enabled: true/' 文件路径      │
│           openclaw gateway reload                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 路由决策流程

```
用户请求
    ↓
┌─────────────────┐
│ 1. 意图识别     │
│ 分析请求类型    │
└─────────────────┘
    ↓
┌─────────────────┐
│ 2. 路由匹配     │
│ 匹配 Tier 1/2/3 │
└─────────────────┘
    ↓
┌─────────────────┐
│ 3. 模型选择     │
│ 根据任务选模型  │
└─────────────────┘
    ↓
┌─────────────────┐
│ 4. 执行处理     │
│ 调用对应 Agent  │
└─────────────────┘
    ↓
┌─────────────────┐
│ 5. 结果输出     │
│ 格式化响应      │
└─────────────────┘
```

---

## 🧠 意图识别规则

| 关键词/模式 | 路由目标 | 加载文件 |
|-----------|---------|---------|
| "分析" "判断" "决策" | Elon 框架 | ELON-FRAMEWORK.md |
| "为什么" "动机" "心理" | 心理学 | PSYCHOLOGY.md |
| "新增" "接入" "模块" | 蒸馏协议 | DISTILLATION.md |
| "输出" "报告" "文档" | 输出验证 | OUTPUT-VERIFICATION.md |
| "代码" "编程" "开发" | Karpathy 编码 | KARPATHY-CODING.md |
| "命令" "终端" "CLI" | Token 效率 | RTK-TOKEN-EFFICIENCY.md |
| "爬虫" "抓取" "数据" | 反爬宪法 | ANTI_SCRAPING_CONSTITUTION.md |
| "安装" "软件" "新增" | 安全评估 | SOFTWARE-INSTALL-SECURITY.md |

---

## 🤖 模型调度策略

### 默认模型

| 模型 | 用途 | 成本 |
|------|------|------|
| qwen3.5-plus | 日常任务 | 低 |
| qwen3-coder-plus | 代码任务 | 低 |
| moonshot/kimi-k2.6 | 创意写作 | 中 |
| Gemini 2.5 Pro | 长文本 (>50页) | 高 |

### 切换策略

```
context 使用率:
  <70%  → 继续使用当前模型
  70-90% → 优化提示，减少上下文
  >90%  → 立即建议切换新对话
```

---

## 📊 路由统计

| 路由类型 | 加载次数 | 平均响应 | 命中率 |
|---------|---------|---------|--------|
| Tier 1 (永久核) | 每次 session | <10ms | 100% |
| Tier 2 (上下文) | 按需 | <50ms | 85% |
| Tier 3 (热插拔) | 手动 | <100ms | 60% |

---

## 🔧 配置示例

### 路由配置

```yaml
# constitution/CONST-ROUTER.md
router:
  tier1:
    - axiom/VALUE-FOUNDATION.md
    - directives/NEGENTROPY.md
    - skills/MODEL-ROUTING.md
  
  tier2:
    analysis: directives/ELON-FRAMEWORK.md
    coding: directives/KARPATHY-CODING.md
    install: security/SOFTWARE-INSTALL-SECURITY.md
  
  tier3:
    path: extensions/
    auto_discover: true
```

### 模型配置

```yaml
# skills/MODEL-ROUTING.md
models:
  default: qwen3.5-plus
  coding: qwen3-coder-plus
  creative: moonshot/kimi-k2.6
  long_context: Gemini-2.5-Pro
  
switch_threshold:
  context_warning: 0.7
  context_critical: 0.9
```

---

## 🚀 使用方式

### 1. 查看当前路由状态

```bash
# 查看已加载的宪法文件
ls constitution/*/

# 查看当前模型
openclaw status
```

### 2. 手动激活 Tier 3 模块

```bash
# 激活模块
sed -i 's/enabled: false/enabled: true/' extensions/new-module.yaml

# 重载网关
openclaw gateway reload
```

### 3. 强制加载特定协议

```python
# 在对话中强制加载
load_directive("directives/ELON-FRAMEWORK.md")
```

---

## 📁 文件结构

```
constitution/
├── CONST-ROUTER.md              # 路由协议 (本文件)
│
├── axiom/                        # Tier 1: 公理层
│   ├── VALUE-FOUNDATION.md       # 价值基石
│   ├── TRUTH-DATA.md            # 数据真实
│   └── VERIFICATION-FIRST.md    # 验证优先
│
├── directives/                   # Tier 1/2: 指令层
│   ├── NEGENTROPY.md            # 负熵法则
│   ├── OBSERVER.md              # 观察者协议
│   ├── AGI-TIMELINE.md          # AGI时间线
│   ├── SELF-LOOP.md             # 自驱动闭环
│   ├── AESTHETICS.md            # 美学法则
│   ├── TURBOQUANT.md            # 智能分离
│   ├── ELON-FRAMEWORK.md        # Elon五步算法
│   ├── KARPATHY-CODING.md       # Karpathy编码
│   └── RTK-TOKEN-EFFICIENCY.md  # Token效率
│
├── skills/                       # Tier 1: 技能层
│   └── MODEL-ROUTING.md         # 模型调度
│
├── security/                     # Tier 2: 安全层
│   └── SOFTWARE-INSTALL-SECURITY.md  # 安全评估
│
├── quality-gates/                # Tier 2: 质量门
│   └── DISTILLATION.md          # 蒸馏协议
│
├── workflows/                    # Tier 2: 工作流
│   └── OUTPUT-VERIFICATION.md   # 输出验证
│
└── extensions/                   # Tier 3: 扩展层
    └── (按需激活)
```

---

## 🎯 未来扩展

| 功能 | 优先级 | 说明 |
|------|--------|------|
| 动态路由 | P1 | 根据历史自动优化路由 |
| 多模态路由 | P1 | 图片/音频/视频路由 |
| 分布式路由 | P2 | 多实例负载均衡 |
| 自适应模型 | P2 | 根据任务自动选择模型 |

---

*太一 AGI · 智能路由系统 v1.0*
*生成时间: 2026-05-04*
*核心能力: 三级加载 · 模型调度 · 意图识别*

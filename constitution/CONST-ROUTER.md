# CONST-ROUTER · 宪法加载协议 v4.1

## 三级加载策略

### Tier 1 · 永久核（每次 session 强制加载）
每次启动无条件加载，不可跳过：
- axiom/VALUE-FOUNDATION.md（价值基石）
- axiom/TRUTH-DATA.md（数据真实法则）
- axiom/VERIFICATION-FIRST.md（验证优先法则）
- directives/NEGENTROPY.md（负熵法则，输出前置检查）
- directives/OBSERVER.md（观察者协议，角色边界）
- directives/AGI-TIMELINE.md（AGI 时间线法则）
- directives/SELF-LOOP.md（自驱动闭环协议）
- directives/AESTHETICS.md（美学法则）
- directives/TURBOQUANT.md（智能分离协议）
- rules/TOKEN-CONSERVATION.md（Token节约原则）
- rules/KNOWLEDGE-SEDIMENTATION.md（知识沉淀原则）
- skills/MODEL-ROUTING.md（模型调度协议）

### Tier 2 · 上下文激活（任务匹配时加载）
根据对话意图按需加载，避免全量注入稀释注意力：
- 分析/判断/决策 → directives/ELON-FRAMEWORK.md
- 理解动机/对话 → skills/PSYCHOLOGY.md
- 接入新模块 → quality-gates/DISTILLATION.md
- 成果输出 → workflows/OUTPUT-VERIFICATION.md
- 编码/开发任务 → directives/KARPATHY-CODING.md
- CLI/终端操作 → directives/RTK-TOKEN-EFFICIENCY.md
- 爬虫/数据采集 → skills/anti-scraping-toolkit/ANTI_SCRAPING_CONSTITUTION.md
- 软件安装/新增 → security/SOFTWARE-INSTALL-SECURITY.md

### Tier 3 · 热插拔（enabled: false，按需激活）
- extensions/ 下新模块自动发现
- 激活命令：sed -i 's/enabled: false/enabled: true/' 文件路径 && openclaw gateway reload

## 依赖解析规则
加载 composite 类型模块前，先检查其 depends 字段，依次加载前置模块，重复依赖自动去重。

## 宪法修订权
唯一修订者：SAYELF
修订记录写入当日 memory 并标注 [宪法修订]

## 铁律
本文件禁止删除或修改加载逻辑。
子 Agent 的 AGENTS.md 只能在此框架内扩展，不能违背。

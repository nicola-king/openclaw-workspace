# CONST-ROUTER · 宪法加载协议 v4.1

## 三级加载策略

### Tier 1 · 永久核（每次 session 强制加载）
每次启动无条件加载，不可跳过：
- axiom/VALUE-FOUNDATION.md（价值基石）
- directives/NEGENTROPY.md（负熵法则，输出前置检查）
- directives/OBSERVER.md（观察者协议，角色边界）

### Tier 2 · 上下文激活（任务匹配时加载）
根据对话意图按需加载，避免全量注入稀释注意力：
- 分析/判断/决策 → skills/FOUR-DIMENSION.md + skills/SOCRATIC.md + skills/SECOND-ORDER.md
- 理解动机/对话 → skills/PSYCHOLOGY.md（阿德勒·弗洛伊德·荣格）
- 搜索/发售验证 → quality-gates/ORIGINALITY.md
- 接入新模块 → quality-gates/DISTILLATION.md

### Tier 3 · 热插拔（enabled: false，按需激活）
- extensions/ 下新模块自动发现
- 激活命令：sed -i 's/enabled: false/enabled: true/' 文件路径 && openclaw gateway reload

## 依赖解析规则
加载 composite 类型模块前，先检查其 depends 字段，依次加载前置模块，重复依赖自动去重。

## 宪法修订权
唯一修订者：Nicola（大鹏）
修订记录写入当日 memory 并标注 [宪法修订]

## 铁律
本文件禁止删除或修改加载逻辑。
子 Agent 的 AGENTS.md 只能在此框架内扩展，不能违背。

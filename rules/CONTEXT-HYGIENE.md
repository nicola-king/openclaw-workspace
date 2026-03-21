---
name: context-hygiene
type: rule
always-apply: true
---
# 上下文卫生原则（渐进式披露）

## 核心原则
不被动灌输，主动按需获取。

## 执行规则
1. Session 启动时只加载 Tier 1（3 个文件）+ AGENTS.md
2. 需要分析任务时，再读 FOUR-DIMENSION.md
3. 需要理解动机时，再读 PSYCHOLOGY.md
4. 需要验证创新时，再读 ORIGINALITY.md
5. 不确定是否需要某个模块时 → 不读，先尝试，卡住了再读

## 主动构建上下文
遇到不确定的历史决策：
→ 主动搜索 memory/ 目录
→ grep 关键词找到相关记录
→ 只提取精确答案，不重读整个文件

## 禁止行为
- 禁止 session 开始就把所有 memory 文件全读一遍
- 禁止把不相关的背景信息带入当前任务
- 禁止依赖对话记忆，必须依赖文件记忆

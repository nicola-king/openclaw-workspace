Karpathy Stack · 架构图 v2

# LLM 知识库 的 工程化蓝图

从「乱贴笔记」到「可审计、可纠错、可复用」的第二大脑 —— 这是我读完 Karpathy 的分享后画的一张系统图。

KEY INSIGHTKarpathy 原版缺一块：
反馈闭环让错误能回流纠正。

Pipeline · End-to-end

STEP 01

采集

浏览器剪藏、PDF、Podcast 转写、聊天记录

STEP 02

去噪

清洗导航栏、广告、重复段落、低信噪素材

STEP 03 · CORE

Wiki 化

结构化成双链笔记，实体、关系、属性全在一起

STEP 04

使用

Agent 随时检索、回答、再写入

Blueprint · v2 · 2026.0401 / 08

Chapter One

# 为什么 笔记 不够用了

当你的知识量超过记忆容量，
你需要的不是更多文件，而是一张**可导航的图**。

Section · Chapter 102 / 08

Problem · Solution

# 原版 vs 升级版

原版 Karpathy

#### 一次性写入

采集 → 转写 → 存档，错了就错了。没有回路，没有修正机制，笔记越多越混乱。

升级 v2

#### 反馈闭环

AI 使用知识库时记录每次 miss / 幻觉 / 过期事实，自动回灌到源文件，让笔记会自我修正。

普通节点

核心节点 · 反馈回路入口

—— 数据流    ┈┈ 反馈回路

Content · Compare03 / 08

Implementation · Skill Manifest

# 反馈回路 怎么实现

一个 100 行的 Agent Skill，把「AI 用得顺不顺」回写成 vault 的一条条修订记录。

```
# skills/wiki-feedback/SKILL.md
name: wiki-feedback
trigger: "after every retrieval"

on_hit:     record(query, path, used=true)
on_miss:    record(query, reason="not-in-vault")
on_wrong:   record(query, correction, path)

nightly:
  - aggregate misses → suggest new notes
  - aggregate wrongs → diff-patch old notes
  - commit to git, open PR for human review
```

Content · Code04 / 08

System Diagram

# 反馈回路全貌

Sources
web · pdf · chat

Clean + Split
defuddle / chunker

Vault (Wiki)
markdown · links
bases · canvas

Agent Use
retrieve / answer

FEEDBACK · wrong / miss

NIGHTLY · suggest new sources

Diagram · Feedback Loop05 / 08

After 6 Months

# 升级版 跑了半年 的数据

13

关键优化项 · 全部落地

#### -62%

幻觉率（相比无反馈回路版本）

#### +4.1×

单次检索命中率

#### 自动修订 227 条

其中 189 条被人工批准合并，38 条被拒绝（数据已归档）。

#### 新增笔记 412 篇

从 miss 日志聚类而来，每篇都有来源追溯。

Content · Stats06 / 08

Next Step

# 开始你的 Wiki v2

不用重写所有笔记。先接一条回路，让 AI 的每次使用都在「改好」你的 vault。

TONIGHT

装 Skill

pnpm i -g @lewis/wiki-feedback

DAY 2

跑 7 天

观察 miss log 自动累积

DAY 8 · CORE

第一次审 PR

花 15 分钟 review 自动生成的修订

MONTH 1

开始信它

你的 vault 会变成活的

CTA07 / 08

END · blueprint v2

# 谢谢 · thanks

图纸、Skill、笔记模板都在 **github.com/lewis/karpathy-wiki-v2**

End of deck08 / 08